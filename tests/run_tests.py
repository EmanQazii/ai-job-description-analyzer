import json
import sys
from pathlib import Path

from src.analyzer import analyze_job_description

def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"

    with open(test_file, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    test_cases = load_test_cases()

    print("=" * 70)
    print("AI JOB DESCRIPTION ANALYZER - TEST SUITE")
    print("=" * 70)
    
    passed = 0 
    failed = 0

    for test_case in test_cases:

        print(f"\n\nTest: {test_case['title']}")
        print("-" * 70)

        try:
            result, overall_score = analyze_job_description(
                test_case["job_description"]
            )

            print(f"Overall Score: {overall_score}/100")

            print("\nScore Breakdown:")
            print(f"  Clarity:         {result.score_breakdown.clarity}")
            print(f"  Completeness:    {result.score_breakdown.completeness}")
            print(f"  Specificity:     {result.score_breakdown.specificity}")
            print(f"  Professionalism: {result.score_breakdown.professionalism}")
            print(f"  Inclusivity:     {result.score_breakdown.inclusivity}")

            print(f"\nIssues Found: {len(result.issues)}")
            print(f"Bias Flags: {len(result.bias_flags)}")

            print("\nChecklist:")
            for item in result.checklist:
                status = "PASS" if item.present else "MISSING"
                print(f"  [{status}] {item.item}")
            
            print("\nImproved JD:") 
            if result.improved_jd and result.improved_jd.strip(): 
                print(" [PASS] Improved JD generated") 
                print(f" Length: {len(result.improved_jd)} characters") 
            else: 
                print(" [FAIL] Improved JD is missing") 
                failed += 1 
                continue 
             # Basic validation 
            if overall_score < 0 or overall_score > 100: 
                print(" [FAIL] Overall score outside 0-100 range") 
                failed += 1 
                continue 
            
            print("\nResult: PASS") 
            passed += 1 

        except Exception as error:
            print(f"ERROR: {error}")
            failed += 1
    print("\n") 
    print("=" * 70) 
    print("TEST SUMMARY") 
    print("=" * 70) 
    print(f"Passed: {passed}") 
    print(f"Failed: {failed}") 
    print(f"Total: {passed + failed}") 
    if failed > 0: 
        print("\nSome tests failed.") 
    else: 
        print("\nAll tests passed.")

if __name__ == "__main__":
    main()