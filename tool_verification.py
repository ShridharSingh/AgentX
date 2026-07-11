# Tool Verification Programme
# Run this file any time you add a new tool or encounter an unexpected bug.
# It tests every tool directly - without requiring LLM or API calls.
# HOW TO USE: type 'python tool_verification.py' in the terminal

import traceback
from tools import calculate, get_current_datetime, web_search, get_real_weather

# ── Colour helpers (work on Windows, Mac, Linux) ──────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def passed(msg): print(f"  {GREEN}✔ PASS{RESET}  {msg}")
def failed(msg): print(f"  {RED}✖ FAIL{RESET}  {msg}")
def info(msg):   print(f"  {YELLOW}→{RESET}      {msg}")

# ── Test runner ───────────────────────────────────────────────────────────────

results = [] # collects (tool_name, test_name, passed: bool) for the summary 

def run_test(tool_name: str, test_name: str, fn, *args, **kwargs):
    """
    Runs a single test case.
    fn      - the tool function to call
    args    - positional arguments to pass to fn
    kwargs  - keyword arguments to pass to fn

    A test passes if:
        1. The function does not raise an exception
        2. The return value is a non-empty string
        3. The return value does not start with "Error:"
    """

    try: 
        result = fn(*args, **kwargs)

        # Check 1 - must return something 
        if results is None:
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
        info(f"Output: {result[:20]}{'...' if len(result) > 120 else ''}")
        results.append((tool_name, test_name, True))

    except Exception:
        failed("{test_name}-> raised an exception.")
        print(f"{RED}{traceback.format_exc()}{RESET}")
        results.append((tool_name, test_name, False))

# ── Individual tool test suites ───────────────────────────────────────────────

def test_calculate():
    print(f"\n{CYAN}{BOLD}── calculate ─────────────────────────────────────{RESET}")
    run_test("calculate", "Basic multiplication",       calculate, "47 * 83")
    run_test("calculate", "Square root - math.sqrt()",  calculate, "math.sqrt(144)")
    run_test("calculate", "Square root - squrt()",      calculate, "sqrt(144)")
    run_test("calculate", "Order of operations",        calculate, "(100 + 50) * 2")
    run_test("calculate", "Division",                   calculate, "200 / 8")
    run_test("calculate", "Power",                      calculate, "2 ** 10")
    run_test("calculate", "Invalid expression",         calculate, "not_a_number * 5")
    # Note: the last test expects an error message - that is the CORRECT behaviour for an invalid output, so we check it manually
    result = calculate("not_a_number * 5")

    if result.lower().startswith("error"):
        passed("Invalid expression -> correctly returned an error message")
    else:
        failed(f"Invalid expression -> should have returned error, got: {result}")

def test_get_current_datetime():
    print(f"\n{CYAN}{BOLD}── get_current_datetime ──────────────────────────{RESET}")
    run_test("get_current_datetime", "Returns a string",   get_current_datetime)
    # Check the output contains expected date components
    result = get_current_datetime()
    if result:
        checks = {
            "Contains 'Date:'":  "Date:" in result,
            "Contains 'Time:'":  "Time:" in result,
            "Contains year":     "2026" in result or "2025" in result,
        }
        for check_name, check_result in checks.items():
            if check_result:
                passed(f"Format check — {check_name}")
            else:
                failed(f"Format check — {check_name} | Got: {result}")
    
def test_web_search():
    print(f"\n{CYAN}{BOLD}── web_search ────────────────────────────────────{RESET}")
    run_test("web_search", "Basic query",           web_search, "Python programming language")
    run_test("web_search", "News query",            web_search, "latest AI news 2026")
    run_test("web_search", "Specific factual query",web_search, "capital city of France")
    
    # Check the output contains expected fields
    result = web_search("Python programming language")
    if result and isinstance(result, str):
        checks = {
            "Contains 'Title:'":    "Title:" in result,
            "Contains 'Summary:":   "Summary:" in result,
            "Contains 'URL':":      "URL:" in result,
        }
        for check_name, check_result in checks.items():
            if check_result:
                passed(f"Format check - {check_name}")
            else:
                failed(f"Format check - {check_name} | Got: {result[:200]}")

def test_get_real_weather():
    print(f"\n{CYAN}{BOLD}── get_real_weather ──────────────────────────────{RESET}")
    
    # Check API key is configured before running any tests
    import os
    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        print(f"  {YELLOW}⚠ SKIP{RESET}   OPENWEATHERMAP_API_KEY not found in .env — skipping live tests")
        return
    
    run_test("get_real_weather", "Default city — Durban",     get_real_weather)
    run_test("get_real_weather", "Explicit city — London",    get_real_weather, "London")
    run_test("get_real_weather", "Explicit city — New York",  get_real_weather, "New York")
    
    # Invalid city should return graceful message not a crash
    result = get_real_weather("NotARealCityXYZ123")
    if "could not find" in result.lower() or "error" in result.lower():
        passed("Invalid city → returned graceful error message")
    else:
        failed(f"Invalid city → unexpected result: {result}")


# ── Summary report ────────────────────────────────────────────────────────────

def print_summary():
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
        status = f"{GREEN}ALL PASS{RESET}" if passes == total else f"{RED}{passes}/{total} PASSED{RESET}"
        print(f" {tool:<30} {status}")
        if passes < total:
            all_passed = False
    
    print(f"{BOLD}{'=' * 50}{RESET}")
    if all_passed:
        print(f"{GREEN}{BOLD}ALL tools verified successfully.{RESET}")
        print(f" AgentX is ready to run!\n")
    else:
        print(f" {RED}{BOLD}Some tools failed. Fix the errors above before running AgentX.{RESET}")


if __name__ == "__main__":
    print(f"\n{BOLD}{'=' * 50}{RESET}")
    print(f"{BOLD}  AgentX — Tool Verification{RESET}")
    print(f"{BOLD}{'=' * 50}{RESET}")
    print(f"  Testing all tools independently of the LLM.")
    print(f"  No API key required for most tools.")

    test_calculate()
    test_get_current_datetime()
    test_web_search()
    test_get_real_weather()

    print_summary()