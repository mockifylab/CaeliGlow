// CaeliGlow - unit tests for version comparison and the update-checker model.
//
// These tests exercise only the pure logic (no network), so they compile and
// run standalone with a C++23 compiler and nlohmann-json headers:
//   g++ -std=c++23 -Isrc/caeliglow tests/test_update_model.cpp -o build/test_update
// In the CaeliGlow build they are also registered with Meson (`just test`).
//
// Required scenarios covered: current version, newer version, network failure,
// rate limit, malformed data, and missing release notes.

#include <cstdio>
#include <cstdlib>
#include <string>

#include "update_model.hpp"
#include "version.hpp"

using namespace caeliglow;

static int g_failures = 0;

#define CHECK(cond)                                                         \
  do {                                                                      \
    if (!(cond)) {                                                          \
      std::printf("  FAIL: %s  (%s:%d)\n", #cond, __FILE__, __LINE__);     \
      ++g_failures;                                                         \
    }                                                                       \
  } while (0)

static void test_version_compare() {
  std::printf("test_version_compare\n");
  CHECK(compareVersion("1.0.0", "1.0.0") == 0);
  CHECK(compareVersion("1.0.1", "1.0.0") > 0);
  CHECK(compareVersion("1.1.0", "1.0.9") > 0);
  CHECK(compareVersion("2.0.0", "10.0.0") < 0);
  CHECK(compareVersion("v1.2.3", "1.2.3") == 0);   // leading v tolerated
  CHECK(compareVersion("1.2", "1.2.0") == 0);      // missing patch = 0
  CHECK(compareVersion("1.0.0-rc.1", "1.0.0") < 0);  // prerelease < release
  CHECK(compareVersion("1.0.0+b2", "1.0.0+b1") == 0);  // build meta ignored
  CHECK(!parseVersion("not-a-version").has_value());
  CHECK(!parseVersion("").has_value());
  CHECK(!parseVersion("1.2.3.4").has_value());
  CHECK(parseVersion("01.02.03").has_value());  // leading zeros tolerated
}

static std::string one_release(const std::string& tag, const std::string& name, const std::string& body,
                               bool pre = false) {
  // Build a small GitHub-shaped release array using raw string to avoid
  // depending on a JSON writer in the test.
  std::string esc_body = body;
  std::string esc_name = name;
  return "[{\"tag_name\":\"" + tag + "\",\"name\":\"" + esc_name + "\",\"body\":\"" + esc_body +
         "\",\"prerelease\":" + (pre ? "true" : "false") + "}]";
}

static void test_up_to_date() {
  std::printf("test_up_to_date\n");
  auto body = one_release("v1.0.0", "CaeliGlow 1.0.0", "Initial release.");
  auto res = evaluate("1.0.0", 200, body);
  CHECK(res.state == UpdateState::UpToDate);
  CHECK(res.message.find("latest CaeliGlow release") != std::string::npos);
}

static void test_update_available() {
  std::printf("test_update_available\n");
  auto body = one_release("v1.1.0", "CaeliGlow 1.1.0", "* Adds hover behavior");
  auto res = evaluate("1.0.0", 200, body);
  CHECK(res.state == UpdateState::UpdateAvailable);
  CHECK(res.latestVersion == "v1.1.0");
  CHECK(res.notes == "* Adds hover behavior");  // returned verbatim as plain text
}

static void test_missing_notes() {
  std::printf("test_missing_notes\n");
  auto body = one_release("v1.2.0", "CaeliGlow 1.2.0", "");
  auto res = evaluate("1.0.0", 200, body);
  CHECK(res.state == UpdateState::UpdateAvailable);
  CHECK(res.notes.empty());  // must not crash or fabricate notes
}

static void test_no_releases() {
  std::printf("test_no_releases\n");
  auto res = evaluate("1.0.0", 200, "[]");
  CHECK(res.state == UpdateState::NoReleases);
}

static void test_offline() {
  std::printf("test_offline\n");
  auto res = evaluate("1.0.0", 0, "");
  CHECK(res.state == UpdateState::Offline);
}

static void test_rate_limited() {
  std::printf("test_rate_limited\n");
  CHECK(evaluate("1.0.0", 403, "{\"message\":\"rate limit\"}").state == UpdateState::RateLimited);
  CHECK(evaluate("1.0.0", 429, "").state == UpdateState::RateLimited);
}

static void test_malformed() {
  std::printf("test_malformed\n");
  // Not JSON at all.
  CHECK(evaluate("1.0.0", 200, "<html>not json</html>").state == UpdateState::Error);
  // Valid JSON but wrong shape (object, not array).
  CHECK(evaluate("1.0.0", 200, "{\"oops\":true}").state == UpdateState::Error);
  // Array with garbage entries (no tag_name) -> no usable releases.
  CHECK(evaluate("1.0.0", 200, "[{\"foo\":1}, 2, \"x\"]").state == UpdateState::NoReleases);
}

static void test_prerelease_policy() {
  std::printf("test_prerelease_policy\n");
  // Installed stable: prerelease on the server is ignored.
  auto body = one_release("v2.0.0-rc.1", "RC", "notes", /*pre=*/true);
  auto res = evaluate("1.0.0", 200, body);
  CHECK(res.state == UpdateState::NoReleases);  // only a prerelease -> not offered to stable users
  // Installed prerelease: the rc becomes eligible.
  auto res2 = evaluate("1.0.0-rc.0", 200, body);
  CHECK(res2.state == UpdateState::UpdateAvailable);
  CHECK(res2.latestVersion == "v2.0.0-rc.1");
}

static void test_picks_highest_among_many() {
  std::printf("test_picks_highest_among_many\n");
  std::string body =
      "[{\"tag_name\":\"v1.0.0\",\"name\":\"\",\"body\":\"\",\"prerelease\":false},"
      "{\"tag_name\":\"v1.5.0\",\"name\":\"\",\"body\":\"mid\",\"prerelease\":false},"
      "{\"tag_name\":\"v1.3.0\",\"name\":\"\",\"body\":\"\",\"prerelease\":false}]";
  auto res = evaluate("1.0.0", 200, body);
  CHECK(res.state == UpdateState::UpdateAvailable);
  CHECK(res.latestVersion == "v1.5.0");
}

int main() {
  test_version_compare();
  test_up_to_date();
  test_update_available();
  test_missing_notes();
  test_no_releases();
  test_offline();
  test_rate_limited();
  test_malformed();
  test_prerelease_policy();
  test_picks_highest_among_many();

  if (g_failures == 0) {
    std::printf("\nALL UPDATE/VERSION TESTS PASSED\n");
    return 0;
  }
  std::printf("\n%d CHECK(S) FAILED\n", g_failures);
  return 1;
}
