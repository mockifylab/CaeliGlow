// CaeliGlow - canonical version and semantic version comparison.
//
// This is dependency-light (C++23 std only) so it can be unit tested in
// isolation and reused by both the native Settings "About" section and the
// build/release tooling. The single canonical version string lives in the
// repository's VERSION file; it is baked in at configure time (see meson /
// build scripts) and exposed through kCaeliGlowVersion below. No other place
// in the app hard-codes a version string.
#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

namespace caeliglow {

// Baked-in canonical version. The build defines CAELIGLOW_VERSION from the
// VERSION file; this provides a safe fallback so headers remain usable in
// contexts (e.g. unit tests) that do not define the macro.
#ifndef CAELIGLOW_VERSION
#define CAELIGLOW_VERSION "0.0.0"
#endif

inline constexpr std::string_view kCaeliGlowVersion = CAELIGLOW_VERSION;

// A parsed semantic version. Supports an optional "v" prefix and an optional
// pre-release suffix (e.g. "1.2.3-rc.1"). Only numeric major/minor/patch are
// used for ordering; pre-release presence makes a version sort before its
// release counterpart (1.0.0-rc.1 < 1.0.0).
struct Semver {
  std::int64_t major = 0;
  std::int64_t minor = 0;
  std::int64_t patch = 0;
  std::string pre;  // empty when absent

  bool prerelease() const { return !pre.empty(); }
};

// Parse a version string such as "v1.2.3", "1.2", "1.2.3-rc.1". Leading "v"
// and surrounding whitespace are tolerated. Returns nullopt on malformed input.
inline std::optional<Semver> parseVersion(std::string_view raw) {
  auto trim = [](std::string_view s) {
    std::size_t b = s.find_first_not_of(" \t\r\n");
    if (b == std::string_view::npos) {
      return std::string_view{};
    }
    std::size_t e = s.find_last_not_of(" \t\r\n");
    return s.substr(b, e - b + 1);
  };

  std::string_view s = trim(raw);
  if (!s.empty() && (s.front() == 'v' || s.front() == 'V')) {
    s.remove_prefix(1);
  }
  if (s.empty()) {
    return std::nullopt;
  }

  Semver out;
  // Split off a pre-release / build suffix at the first '-' or '+'.
  std::size_t sep = s.find_first_of("-+");
  std::string_view core = (sep == std::string_view::npos) ? s : s.substr(0, sep);
  if (sep != std::string_view::npos) {
    out.pre = std::string(s.substr(sep));
    // A '+' build suffix is not part of precedence ordering; drop it.
    if (auto plus = out.pre.find('+'); plus != std::string::npos) {
      out.pre = out.pre.substr(0, plus);
    }
    if (out.pre.size() > 1 && out.pre.front() == '-') {
      out.pre.erase(out.pre.begin());  // strip leading '-'
    }
  }

  std::vector<std::string_view> parts;
  std::size_t pos = 0;
  while (true) {
    std::size_t dot = core.find('.', pos);
    parts.push_back(core.substr(pos, dot == std::string_view::npos ? std::string_view::npos : dot - pos));
    if (dot == std::string_view::npos) {
      break;
    }
    pos = dot + 1;
  }
  if (parts.empty() || parts.size() > 3) {
    return std::nullopt;
  }

  auto number = [](std::string_view tok, std::int64_t& into) {
    if (tok.empty()) {
      return false;
    }
    std::int64_t acc = 0;
    for (char c : tok) {
      if (c < '0' || c > '9') {
        return false;
      }
      acc = acc * 10 + (c - '0');
    }
    into = acc;
    return true;
  };

  if (!number(parts[0], out.major)) {
    return std::nullopt;
  }
  if (parts.size() > 1 && !number(parts[1], out.minor)) {
    return std::nullopt;
  }
  if (parts.size() > 2 && !number(parts[2], out.patch)) {
    return std::nullopt;
  }
  return out;
}

// Three-way compare: negative if a<b, 0 if equal, positive if a>b.
// Pre-release ordering follows the common semver rule: a version with a
// pre-release sorts before the same version without one.
inline int compareVersion(const Semver& a, const Semver& b) {
  if (a.major != b.major) {
    return a.major < b.major ? -1 : 1;
  }
  if (a.minor != b.minor) {
    return a.minor < b.minor ? -1 : 1;
  }
  if (a.patch != b.patch) {
    return a.patch < b.patch ? -1 : 1;
  }
  if (a.pre == b.pre) {
    return 0;
  }
  if (a.pre.empty()) {
    return 1;  // release > prerelease
  }
  if (b.pre.empty()) {
    return -1;
  }
  return a.pre < b.pre ? -1 : 1;
}

inline std::optional<int> compareVersion(std::string_view a, std::string_view b) {
  auto pa = parseVersion(a);
  auto pb = parseVersion(b);
  if (!pa || !pb) {
    return std::nullopt;
  }
  return compareVersion(*pa, *pb);
}

}  // namespace caeliglow
