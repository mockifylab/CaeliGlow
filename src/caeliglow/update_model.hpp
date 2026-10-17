// CaeliGlow - update checker model (feature #5).
//
// The transport layer (HTTP fetch) lives in the native Settings integration and
// in build tooling; this header contains only the pure, testable decision logic
// so it can be unit tested with mocked responses for: current version, newer
// version, network failure, rate limit, malformed data, and missing notes.
//
// Privacy/safety guarantees enforced by design here and in callers:
//   * The request is a GET to GitHub's public releases endpoint with NO
//     authentication, NO user config, NO machine identifiers.
//   * Release notes are treated strictly as text. They are never parsed as
//     HTML/Markdown-as-code and never executed. Installation is never implicit:
//     evaluate() only reports state; a separate, explicit user action runs the
//     update script, which itself backs up and validates before touching files.
#pragma once

#include <string>
#include <vector>

#include <nlohmann/json.hpp>

#include "version.hpp"

namespace caeliglow {

// The states the About/update UI can display.
enum class UpdateState {
  Checking,         // request in flight
  UpToDate,         // installed is the newest known release
  UpdateAvailable,  // a newer release exists
  NoReleases,       // repository reachable but has no releases yet
  Offline,          // network failure / timeout / no connectivity
  RateLimited,      // GitHub API rate limit (HTTP 403/429)
  Error,            // malformed or otherwise unusable response
};

// A minimal view of one GitHub release record.
struct ReleaseInfo {
  std::string tag;      // e.g. "v1.2.0"
  std::string name;     // human title, may be empty
  std::string notes;    // body, may be empty
  bool prerelease = false;
};

// A release with its parsed semantic version, used for ordering.
struct ParsedRelease {
  ReleaseInfo info;
  Semver version;
};

struct UpdateResult {
  UpdateState state = UpdateState::Checking;
  std::string installedVersion;
  std::string latestVersion;  // tag of newest release when UpdateAvailable
  std::string notes;          // release notes when UpdateAvailable
  std::string message;        // human-readable summary for the UI
};

inline const char* toString(UpdateState s) {
  switch (s) {
    case UpdateState::Checking: return "checking";
    case UpdateState::UpToDate: return "up-to-date";
    case UpdateState::UpdateAvailable: return "update-available";
    case UpdateState::NoReleases: return "no-releases";
    case UpdateState::Offline: return "offline";
    case UpdateState::RateLimited: return "rate-limited";
    case UpdateState::Error: return "error";
  }
  return "unknown";
}

// Parse a GitHub "/releases" JSON array into release records. Tolerant of
// missing fields; a non-array or structurally broken body yields an empty
// vector and lets the caller distinguish NoReleases from Error via jsonOk.
inline std::vector<ReleaseInfo> parseReleases(const std::string& body, bool& jsonOk) {
  jsonOk = false;
  std::vector<ReleaseInfo> out;

  nlohmann::json root;
  try {
    root = nlohmann::json::parse(body);
  } catch (const nlohmann::json::exception&) {
    return out;  // malformed JSON
  }
  if (!root.is_array()) {
    return out;  // unexpected shape
  }
  jsonOk = true;

  for (const auto& item : root) {
    if (!item.is_object()) {
      continue;
    }
    ReleaseInfo r;
    if (item.contains("tag_name") && item["tag_name"].is_string()) {
      r.tag = item["tag_name"].get<std::string>();
    }
    if (item.contains("name") && item["name"].is_string()) {
      r.name = item["name"].get<std::string>();
    }
    if (item.contains("body") && item["body"].is_string()) {
      r.notes = item["body"].get<std::string>();
    }
    if (item.contains("prerelease") && item["prerelease"].is_boolean()) {
      r.prerelease = item["prerelease"].get<bool>();
    }
    if (!r.tag.empty()) {
      out.push_back(std::move(r));
    }
  }
  return out;
}

// Return the highest-versioned, non-prerelease release that parses as semver.
// Prereleases are ignored unless the installed version is itself a prerelease,
// matching a conservative "stable channel" policy.
inline std::optional<ParsedRelease> selectLatest(const std::vector<ReleaseInfo>& releases,
                                                 const Semver& installed) {
  std::optional<ParsedRelease> best;
  bool allowPre = installed.prerelease();
  for (const auto& r : releases) {
    if (r.prerelease && !allowPre) {
      continue;
    }
    auto v = parseVersion(r.tag);
    if (!v) {
      continue;
    }
    if (!best || compareVersion(*v, best->version) > 0) {
      best = ParsedRelease{.info = r, .version = *v};
    }
  }
  return best;
}

// Decide the UI state from an HTTP status code + body and the installed version.
// status == 0 signals a transport failure (offline/timeout).
inline UpdateResult evaluate(const std::string& installedVersion, int status, const std::string& body) {
  UpdateResult res;
  res.installedVersion = installedVersion;

  auto installed = parseVersion(installedVersion);
  if (!installed) {
    // Unknown/invalid local version: do not compare, surface as error.
    res.state = UpdateState::Error;
    res.message = "Could not determine the installed CaeliGlow version.";
    return res;
  }

  if (status == 0) {
    res.state = UpdateState::Offline;
    res.message = "Unable to reach GitHub. Check your network connection and try again.";
    return res;
  }
  if (status == 403 || status == 429) {
    res.state = UpdateState::RateLimited;
    res.message = "GitHub is rate-limiting update checks right now. Try again in a few minutes.";
    return res;
  }
  if (status < 200 || status >= 300) {
    res.state = UpdateState::Error;
    res.message = "The update check failed (HTTP " + std::to_string(status) + ").";
    return res;
  }

  bool jsonOk = false;
  auto releases = parseReleases(body, jsonOk);
  if (!jsonOk) {
    res.state = UpdateState::Error;
    res.message = "The update server returned an unexpected response.";
    return res;
  }
  if (releases.empty()) {
    res.state = UpdateState::NoReleases;
    res.message = "No CaeliGlow releases have been published yet.";
    return res;
  }

  auto latest = selectLatest(releases, *installed);
  if (!latest) {
    res.state = UpdateState::NoReleases;
    res.message = "No stable CaeliGlow release is available yet.";
    return res;
  }

  res.latestVersion = latest->info.tag;
  if (compareVersion(latest->version, *installed) > 0) {
    res.state = UpdateState::UpdateAvailable;
    res.notes = latest->info.notes;  // rendered as plain text by the UI
    std::string title = latest->info.name.empty() ? latest->info.tag : latest->info.name;
    res.message = "CaeliGlow " + title + " is available.";
  } else {
    res.state = UpdateState::UpToDate;
    res.message = "You\u2019re using the latest CaeliGlow release.";
  }
  return res;
}

}  // namespace caeliglow
