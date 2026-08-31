import streamlit as st

from src.analyzer import analyze_job_description


st.set_page_config(
    page_title="AI Job Description Analyzer",
    page_icon="",
    layout="wide",
)


st.title("AI Job Description Analyzer")

st.write(
    "Analyze your cybersecurity job description for clarity, "
    "completeness, specificity, professionalism, and inclusivity."
)

st.divider()

st.subheader("Job Description")

job_description = st.text_area(
    "Paste your job description below",
    height=350,
    placeholder=(
        "Example:\n\n"
        "We are looking for a SOC Analyst to join our "
        "Security Operations team..."
    ),
)

analyze_button = st.button(
    "Analyze Job Description",
    type="primary",
    use_container_width=True,
)


if analyze_button:

    if not job_description.strip():

        st.warning(
            "Please enter a job description before analyzing."
        )

    else:

        with st.spinner("Analyzing job description..."):

            try:

                analysis, overall_score = analyze_job_description(
                    job_description
                )

                st.divider()

                st.subheader("Analysis Results")

                st.metric(
                    label="Overall Score",
                    value=f"{overall_score}/100",
                )

                st.subheader("Score Breakdown")

                col1, col2, col3, col4, col5 = st.columns(5)

                col1.metric(
                    "Clarity",
                    analysis.score_breakdown.clarity,
                )

                col2.metric(
                    "Completeness",
                    analysis.score_breakdown.completeness,
                )

                col3.metric(
                    "Specificity",
                    analysis.score_breakdown.specificity,
                )

                col4.metric(
                    "Professionalism",
                    analysis.score_breakdown.professionalism,
                )

                col5.metric(
                    "Inclusivity",
                    analysis.score_breakdown.inclusivity,
                )

                st.subheader("Summary")

                st.write(analysis.summary)
                
                st.subheader("Issues Found")
                if analysis.issues:
                    for issue in analysis.issues:
                        with st.expander(
                            f"{issue.severity} — {issue.issue}"
                        ):
                            st.write(
                                f"**Category:** {issue.category}"
                            )
                            st.write(
                                f"**Explanation:** {issue.explanation}"
                            )
                            st.write(
                                f"**Suggested Fix:** {issue.suggestion}"
                            )
                else:
                    st.success("No significant issues were identified.")

                st.subheader("Suggested Improvements")
                if analysis.recommendations:
                    for recommendation in analysis.recommendations:
                        st.write(f"- {recommendation}")
                else:
                    st.info("No additional recommendations were generated.")
                    
            except Exception as error:

                st.error(
                    f"An error occurred while analyzing the job description: "
                    f"{error}"
                )