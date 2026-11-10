"""Tool verification suite for AgentX.

Tests each tool directly, without calling the LLM, using both valid and
invalid inputs, and prints a pass/fail summary.

Run this file whenever you add a new tool or hit an unexpected bug:
    python tool_verification.py
"""

import os
import traceback
from datetime import datetime

from tools import calculate, get_current_datetime, get_real_weather, web_search

# ── Colour helpers (work on Windows, Mac, Linux) ──────────────────────────────

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def passed(msg):
    """Print a green PASS line."""
    print(f"  {GREEN}✔ PASS{RESET}  {msg}")


def failed(msg):
    """Print a red FAIL line."""
    print(f"  {RED}✖ FAIL{RESET}  {msg}")


def info(msg):
    """Print a yellow detail line, such as a test's output."""
    print(f"  {YELLOW}→{RESET}      {msg}")


# ── Test runner ───────────────────────────────────────────────────────────────

results = []  # collects (tool_name, test_name, passed: bool) for the summary


def run_test(tool_name: str, test_name: str, fn, *args, **kwargs):
    """Run a single test case and record the result.

    Args:
        tool_name: Name of the tool being tested, used for the summary.
        test_name: Short description of this test case.
        fn: The tool function to call.
        *args: Positional arguments passed to fn.
        **kwargs: Keyword arguments passed to fn.

    A test passes if the function:
        1. Does not raise an exception
        2. Does not return None
        3. Returns a non-empty string
        4. Returns output that does not start with "error"
    """
    try:
        result = fn(*args, **kwargs)

        # Check 1 - must return something
        if result is None:
            failed(f"{test_name} -> returned None (missing return statement?)")
            results.append((tool_name, test_name, False))
            return

        # Check 2 - must be a string
        if not isinstance(result, str):
            failed(f"{test_name} -> returned {type(result).__name__} instead of str")
            results.append((tool_name, test_name, False))
            return

        # Check 3 - must not be empty
        if result.strip() == "":
            failed(f"{test_name} -> returned an empty string")
            results.append((tool_name, test_name, False))
            return

        # Check 4 - must not be an error message
        if result.lower().startswith("error"):
            failed(f"{test_name} -> tool returned an error: {result}")
            results.append((tool_name, test_name, False))
            return

        passed(f"{test_name}")
        info(f"Output: {result[:120]}{'...' if len(result) > 120 else ''}")
        results.append((tool_name, test_name, True))

    except Exception:
        failed(f"{test_name} -> raised an exception.")
        print(f"{RED}{traceback.format_exc()}{RESET}")
        results.append((tool_name, test_name, False))


# ── Individual tool test suites ───────────────────────────────────────────────


def test_calculate():
    """Test calculate with valid expressions and one invalid expression."""
    print(f"\n{CYAN}{BOLD}── calculate ─────────────────────────────────────{RESET}")
    run_test("calculate", "Basic multiplication", calculate, "47 * 83")
    run_test("calculate", "Square root - math.sqrt()", calculate, "math.sqrt(144)")
    run_test("calculate", "Square root - sqrt()", calculate, "sqrt(144)")
    run_test("calculate", "Order of operations", calculate, "(100 + 50) * 2")
    run_test("calculate", "Division", calculate, "200 / 8")
    run_test("calculate", "Power", calculate, "2 ** 10")
    # Invalid input should return an error message - that is the CORRECT behaviour, so we check it manually
    result = calculate("not_a_number * 5")

    if result.lower().startswith("error"):
        passed("Invalid expression -> correctly returned an error message")
    else:
        failed(f"Invalid expression -> should have returned error, got: {result}")


def test_get_current_datetime():
    """Test that get_current_datetime returns the current date and time in the expected format.

    Reads the system clock before and after calling the tool and checks that
    the tool's reported time falls between them, so a delay or a change of
    day during the test cannot cause a false failure.
    """
    print(f"\n{CYAN}{BOLD}── get_current_datetime ──────────────────────────{RESET}")
    run_test("get_current_datetime", "Returns a string", get_current_datetime)

    test_name = "Date and time are correctly formatted and current"
    before = datetime.now().replace(microsecond=0)
    result = get_current_datetime()
    after = datetime.now()

    try:
        tool_time = datetime.strptime(result, "Date: %A %d %B %Y | Time: %H:%M:%S")
        ok = before <= tool_time <= after
        if ok:
            passed(test_name)
        else:
            failed(f"{test_name} -> time outside expected window, got: {result}")
    except (ValueError, TypeError):
        ok = False
        failed(f"{test_name} -> wrong format, got: {result}")

    results.append(("get_current_datetime", test_name, ok))


def test_web_search():
    """Test web_search with sample queries and check the result format."""
    print(f"\n{CYAN}{BOLD}── web_search ────────────────────────────────────{RESET}")
    run_test("web_search", "Basic query", web_search, "Python programming language")
    run_test("web_search", "News query", web_search, "latest AI news 2026")
    run_test(
        "web_search", "Specific factual query", web_search, "capital city of France"
    )

    # Check the output contains expected fields
    result = web_search("Python programming language")
    if result and isinstance(result, str):
        checks = {
            "Contains 'Title:'": "Title:" in result,
            "Contains 'Summary:": "Summary:" in result,
            "Contains 'URL':": "URL:" in result,
        }
        for check_name, check_result in checks.items():
            if check_result:
                passed(f"Format check - {check_name}")
            else:
                failed(f"Format check - {check_name} | Got: {result[:200]}")


def test_get_real_weather():
    """Test get_real_weather against the live OpenWeatherMap API.

    Skips all tests if OPENWEATHERMAP_API_KEY is not set. Checks the default
    city, explicit cities, and that an invalid city returns a graceful message.
    """
    print(f"\n{CYAN}{BOLD}── get_real_weather ──────────────────────────────{RESET}")

    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        print(
            f"  {YELLOW}⚠ SKIP{RESET}   OPENWEATHERMAP_API_KEY not found in .env — skipping live tests"
        )
        return

    run_test("get_real_weather", "Default city — Durban", get_real_weather)
    run_test("get_real_weather", "Explicit city — London", get_real_weather, "London")
    run_test(
        "get_real_weather", "Explicit city — New York", get_real_weather, "New York"
    )

    # Invalid city should return graceful message not a crash
    result = get_real_weather("NotARealCityXYZ123")
    if "could not find" in result.lower() or "error" in result.lower():
        passed("Invalid city → returned graceful error message")
    else:
        failed(f"Invalid city → unexpected result: {result}")


# ── Summary report ────────────────────────────────────────────────────────────


def print_summary():
    """Print a per-tool pass/fail summary of all recorded results."""
    print(f"\n{BOLD}{'=' * 50}{RESET}")
    print(f"{BOLD} VERIFICATION SUMMARY{RESET}")
    print(f"{BOLD}{'=' * 50}{RESET}")

    # Group by tool
    tools_seen = []
    for tool_name, _, _ in results:
        if tool_name not in tools_seen:
            tools_seen.append(tool_name)

    all_passed = True
    for tool in tools_seen:
        tool_results = [(t, p) for (tn, t, p) in results if tn == tool]
        passes = sum(1 for _, p in tool_results if p)
        total = len(tool_results)
        status = (
            f"{GREEN}ALL PASS{RESET}"
            if passes == total
            else f"{RED}{passes}/{total} PASSED{RESET}"
        )
        print(f" {tool:<30} {status}")
        if passes < total:
            all_passed = False

    print(f"{BOLD}{'=' * 50}{RESET}")
    if all_passed:
        print(f"{GREEN}{BOLD}ALL tools verified successfully.{RESET}")
        print(" AgentX is ready to run!\n")
    else:
        print(
            f" {RED}{BOLD}Some tools failed. Fix the errors above before running AgentX.{RESET}"
        )


if __name__ == "__main__":
    print(f"\n{BOLD}{'=' * 50}{RESET}")
    print(f"{BOLD}  AgentX — Tool Verification{RESET}")
    print(f"{BOLD}{'=' * 50}{RESET}")
    print("  Testing all tools independently of the LLM.")
    print("  No API key required for most tools.")

    test_calculate()
    test_get_current_datetime()
    test_web_search()
    test_get_real_weather()

    print_summary()
