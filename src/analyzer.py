import os

from dotenv import load_dotenv
from google import genai

from schemas import JDAnalysis
from prompts import SYSTEM_INSTRUCTION


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the environment.")

client = genai.Client(api_key=api_key)


def analyze_job_description(job_description: str) -> JDAnalysis:

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    prompt = f"""
{SYSTEM_INSTRUCTION}

Analyze the following job description.

JOB DESCRIPTION:
----------------
{job_description}
----------------
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": JDAnalysis,
        },
    )

    return JDAnalysis.model_validate_json(response.text)


if __name__ == "__main__":

    sample_jd = """
    Job Title: SOC Analyst

    We are looking for a young and energetic cybersecurity
    professional to join our team.

    The successful candidate should have good knowledge of
    cybersecurity and be able to work under pressure.

    Responsibilities:
    - Monitor security systems.
    - Handle security incidents.
    - Perform cybersecurity tasks.

    Requirements:
    - Bachelor's degree in Computer Science or related field.
    - Good communication skills.
    - Knowledge of cybersecurity.
    - Ability to work in a fast-paced environment.
    """

    analysis = analyze_job_description(sample_jd)

    print("\n========== JOB DESCRIPTION ANALYSIS ==========\n")

    print(f"Overall Score: {analysis.overall_score}/100")

    print("\n--- Score Breakdown ---")

    print(f"Clarity:          {analysis.score_breakdown.clarity}")
    print(f"Completeness:     {analysis.score_breakdown.completeness}")
    print(f"Specificity:      {analysis.score_breakdown.specificity}")
    print(f"Professionalism:  {analysis.score_breakdown.professionalism}")
    print(f"Inclusivity:      {analysis.score_breakdown.inclusivity}")

    print("\n--- Summary ---")
    print(analysis.summary)

    print("\n--- Issues ---")

    for issue in analysis.issues:
        print(f"\n[{issue.severity}] {issue.issue}")
        print(f"Category: {issue.category}")
        print(f"Explanation: {issue.explanation}")
        print(f"Suggestion: {issue.suggestion}")

    print("\n--- Potential Bias ---")

    if analysis.bias_flags:
        for flag in analysis.bias_flags:
            print(f"\nPhrase: {flag.phrase}")
            print(f"Concern: {flag.concern}")
            print(f"Alternative: {flag.suggested_alternative}")
    else:
        print("No potential bias detected.")

    print("\n--- JD Checklist ---")

    for item in analysis.checklist:
        status = "✓" if item.present else "✗"
        print(f"{status} {item.item}: {item.comment}")

    print("\n--- Recommendations ---")

    for recommendation in analysis.recommendations:
        print(f"- {recommendation}")