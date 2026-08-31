# AI Job Description Analyzer

An AI-powered web application that evaluates cybersecurity job descriptions and provides practical recommendations to improve their quality, clarity, specificity, professionalism, and inclusivity.

**Live Demo:** https://ai-job-description-analyzer.streamlit.app/

---

## 1. Project Overview

The AI Job Description Analyzer was developed as an AI/ML internship project for a cybersecurity services context.

Poorly written job descriptions can attract unsuitable candidates, create confusion about role expectations, and unintentionally introduce biased or exclusionary language. The goal of this project was to build a practical MVP that allows HR teams, hiring managers, and internal teams to evaluate a cybersecurity job description before publishing it.

The application accepts a job description as text, sends it to an LLM for structured analysis, and presents the results through a professional Streamlit interface.

---

## 2. Problem Statement

Cybersecurity organizations often need to create job descriptions that are technically accurate, professional, inclusive, and clear enough for candidates to understand.

A weak job description may contain:

- Vague responsibilities
- Generic technical requirements
- Missing experience or qualification information
- Informal or unprofessional wording
- Potentially biased language
- Missing information about the work arrangement or reporting structure

Manually reviewing these areas can be repetitive and inconsistent.

This project addresses the problem by providing an AI-assisted first-pass review of a cybersecurity job description.

---

## 3. Objective

The main objective was to design and build a working MVP that can:

1. Accept a job description as input.
2. Evaluate its overall quality.
3. Score important quality dimensions.
4. Identify specific issues.
5. Detect potentially biased language.
6. Compare the JD against a strong-job-description checklist.
7. Provide actionable recommendations.
8. Generate an improved sample job description based only on the information available in the original JD.
9. Present the analysis through a clean and usable web interface.

---

## 4. Target Users

The intended users include:

- HR teams
- Hiring managers
- Recruitment teams
- Cybersecurity team leads
- Internal business teams
- Analysts reviewing client-facing job descriptions

The solution is particularly suited to cybersecurity-related hiring because the analyzer considers technical context and evaluates requirements according to the role rather than blindly requiring the same tools for every cybersecurity position.

---

## 5. Key Features

### Core Features

#### Job Description Input

Users can paste a complete job description into the application.

The analyzer works with different levels of JD quality, from extremely short descriptions to detailed professional descriptions.

#### AI Quality Scoring

The application provides scores from 0 to 100 across five dimensions:

- Clarity
- Completeness
- Specificity
- Professionalism
- Inclusivity

An overall quality score is also calculated.

#### Issue Detection

The system identifies weaknesses in the JD and explains:

- What the issue is
- Which category it belongs to
- Its severity
- Why it matters
- How it can be improved

Issues are categorized using:

- Low
- Medium
- High

#### Bias-Language Detection

The analyzer identifies potentially biased or exclusionary wording.

For each detected phrase, it provides:

- The phrase
- The potential concern
- A neutral alternative

The system is intentionally designed not to make legal conclusions. It identifies potentially problematic wording and explains why it may affect inclusivity.

#### JD Quality Checklist

The application checks whether the JD contains important candidate-facing information.

The checklist evaluates:

- Clear job title
- Role summary
- Key responsibilities
- Required skills
- Experience requirements
- Preferred skills
- Education requirements
- Relevant cybersecurity technologies/tools
- Work arrangement
- Reporting structure

Checklist items are classified as either:

- Essential
- Recommended

An item is marked as present only when the JD provides meaningful, candidate-useful information.

#### Recommended Improvements

The system generates practical recommendations based on the weaknesses found in the submitted JD.

Recommendations focus on concrete changes rather than generic statements.

#### Improved Job Description

The application can provide a sample improved version of the job description.

The generated version is intended as a starting point for the user. Users should replace or verify specifications such as:

- Job title
- Experience level
- Technologies
- Qualifications
- Work arrangement
- Reporting structure
- Organization-specific requirements

The system does not intentionally invent company-specific facts.

---

## 6. Evaluation Dimensions

### Clarity

Measures whether candidates can quickly understand:

- What the role is
- Why the role exists
- What its main responsibilities are
- What is expected from the candidate

### Completeness

Measures whether the JD contains important information needed to understand and evaluate the opportunity.

The analyzer considers information such as:

- Role summary
- Responsibilities
- Qualifications
- Experience
- Skills
- Practical job information

Optional information is not treated as equally important as essential information.

### Specificity

Measures whether the responsibilities and requirements are concrete, measurable, and technically meaningful.

Examples of vague language include:

- "Good knowledge"
- "Good communication"
- "Cybersecurity tasks"
- "Work under pressure"
- "Good at computers"

The analyzer encourages specific and job-relevant descriptions instead.

### Professionalism

Evaluates:

- Tone
- Wording
- Structure
- Readability
- Informal expressions
- Subjective language
- Unnecessary jargon

### Inclusivity

Evaluates whether the JD uses neutral, job-relevant language and avoids potentially exclusionary wording.

The system does not automatically label a phrase as discriminatory. It flags potentially problematic language and explains the concern.

---

## 7. Cybersecurity-Aware Analysis

The analyzer does not require every cybersecurity job description to mention the same technologies.

Technical expectations depend on the actual role and seniority.

For example, a SOC Analyst may reasonably mention:

- SIEM
- EDR
- Incident response
- Log analysis
- Threat detection

A GRC Analyst may instead mention:

- Security frameworks
- Risk assessment
- Compliance
- Policy management
- Audit processes

The prompt therefore instructs the model to evaluate technical relevance instead of applying a fixed technology checklist to every role.

---

## 8. System Workflow

The application follows this general workflow:

```text
User enters Job Description
          |
          v
Streamlit Web Interface
          |
          v
Analyzer Function
          |
          v
System Prompt + Job Description
          |
          v
Gemini LLM API
          |
          v
Structured Analysis Response
          |
          v
Schema Validation / Processing
          |
          v
Overall Score Calculation
          |
          v
Streamlit Results Interface
          |
          +--> Score Breakdown
          +--> Summary
          +--> Issues
          +--> Potential Bias
          +--> JD Checklist
          +--> Recommended Improvements
          +--> Improved JD
```

---

## 9. Technical Approach

The project uses an LLM-based evaluation pipeline rather than training a machine learning model from scratch.

The main approach was:

1. Define the business problem.
2. Identify the information a strong JD should contain.
3. Design evaluation dimensions.
4. Create a structured system instruction for the LLM.
5. Define a schema for the expected analysis.
6. Connect the application to the Gemini API.
7. Process the returned structured analysis.
8. Calculate/display the overall score.
9. Build a Streamlit interface.
10. Create realistic test cases.
11. Test both strong and poor job descriptions.
12. Deploy the application using Streamlit Community Cloud.
13. Polish the UI and documentation for portfolio use.

---

## 10. Prompt Engineering

A major part of the project was designing a detailed system instruction for the LLM.

The system instruction establishes the model's role as an AI Job Description Quality Analyst working in a cybersecurity services context.

It defines:

- The five scoring dimensions
- Scoring range
- Issue structure
- Severity levels
- Bias detection behavior
- Checklist requirements
- Cybersecurity context
- Recommendation requirements
- Restrictions against inventing information

The prompt also explicitly instructs the model to analyze only information contained in the submitted job description.

This helps make the output more consistent and prevents the model from casually inventing company details, salaries, technologies, locations, or requirements.

---

## 11. Structured Output

Instead of relying on unstructured text from the LLM, the project uses a defined response schema.

The analysis is organized into logical sections such as:

- Score breakdown
- Summary
- Issues
- Bias flags
- Checklist
- Recommendations
- Improved job description

This makes the output easier for the Python application to process and allows the Streamlit interface to display each part separately.

---

## 12. Project Structure

```text
ai-job-description-analyzer/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── analyzer.py
│   ├── prompts.py
│   └── schemas.py
│
└── tests/
    ├── run_tests.py
    └── test_cases.json
```

### Important Files

#### `app.py`

Contains the Streamlit application and user-facing interface.

It handles:

- Job description input
- Analysis trigger
- Result presentation
- Score visualization
- Issue presentation
- Bias presentation
- Checklist presentation
- Recommendations
- Improved JD presentation

#### `src/analyzer.py`

Contains the main analysis logic.

It is responsible for:

- Reading the Gemini API configuration
- Sending the JD to Gemini
- Processing the response
- Validating structured output
- Calculating/returning the overall analysis

#### `src/prompts.py`

Contains the system instruction used to guide the LLM.

The prompt defines how the model should evaluate job descriptions.

#### `src/schemas.py`

Defines the expected structure of the AI-generated analysis.

This helps keep the application response consistent and easier to process.

#### `tests/test_cases.json`

Contains realistic test cases used to evaluate the analyzer.

#### `tests/run_tests.py`

Runs the test cases through the analyzer and prints the results.

---

## 13. Environment Setup

### Requirements

The project was developed using:

- Python
- Streamlit
- Google Gemini API
- Pydantic
- python-dotenv
- Git
- GitHub

A virtual environment was used during development.

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

A `.env.example` file is included so the required configuration can be understood without exposing the real API key.

The actual `.env` file should not be committed to GitHub.

---

## 14. Running the Application Locally

From the project root:

```bash
streamlit run app.py
```

The application will start on a local Streamlit URL, normally:

```text
http://localhost:8501
```

---

## 15. Running the Test Suite

The project includes a separate test suite containing multiple realistic scenarios.

Run:

```bash
python tests/run_tests.py
```

The test suite evaluates examples such as:

### Strong SOC Analyst JD

A detailed JD containing:

- Clear role title
- Role summary
- Responsibilities
- Technical skills
- Experience
- Education
- Cybersecurity technologies
- Work arrangement
- Reporting structure

Expected result: high overall quality.

### Poor SOC Analyst JD

A deliberately weak description containing vague requirements and insufficient role information.

Expected result: low overall quality and relevant issue/bias detection.

### Extremely Short JD

Tests how the analyzer handles minimal input.

Expected result: low completeness and specificity.

### Potentially Biased JD

Tests the bias-detection capability using phrases such as age-related or subjective language.

Expected result: low inclusivity and multiple bias flags.

### Incomplete Cybersecurity JD

Tests a partially developed but professional-looking JD with important missing information.

Expected result: moderate/low completeness and specific recommendations.

---

## 16. Testing Results

The analyzer was tested using both strong and intentionally weak cybersecurity job descriptions.

Example behavior observed during testing:

| Test Case | General Result |
|---|---|
| Strong SOC Analyst JD | High-quality score |
| Poor SOC Analyst JD | Very low-quality score |
| Extremely Short JD | Very low-quality score |
| Potentially Biased JD | Very low inclusivity score with bias flags |
| Incomplete Cybersecurity JD | Moderate score with missing checklist items |

One strong SOC Analyst test case reached approximately **94/100**, demonstrating that the analyzer can recognize a detailed and professionally written JD.

A deliberately poor JD containing phrases such as "Cybersecurity Ninja", "young and energetic", "good at computers", and "cybersecurity stuff" received an extremely low score and generated relevant issues and bias flags.

---

## 17. Example Poor Job Description

```text
Job Title: Cybersecurity Ninja

We need a young and energetic person who is good at computers.

You will do cybersecurity stuff and work under pressure.

Good communication skills required.
```

The analyzer identifies problems including:

- Informal job title
- Potential age/personality bias
- Vague responsibilities
- Vague technical requirements
- Generic communication requirement
- Missing experience
- Missing education
- Missing cybersecurity technologies
- Missing work arrangement
- Missing reporting structure

---

## 18. Example Strong Job Description

```text
We are seeking a SOC Analyst to join our Security Operations team. The analyst will monitor security events, investigate alerts, and support incident response activities to protect client environments.

Responsibilities include monitoring SIEM alerts, investigating suspicious authentication and network activity, documenting incidents in the ticketing system, escalating confirmed incidents according to established procedures, and contributing to threat-hunting activities.

Required qualifications include a bachelor's degree in cybersecurity, computer science, or a related field, 1-2 years of experience in a SOC or security monitoring role, understanding of TCP/IP and common attack techniques, and hands-on experience with SIEM platforms such as Splunk or Microsoft Sentinel.

Familiarity with EDR platforms and scripting with Python or PowerShell is preferred. The role is hybrid and reports to the SOC Manager.
```

This type of JD provides the analyzer with enough information to evaluate the role positively across most dimensions.

---

## 19. UI / UX Design

The interface was designed to make the analysis useful to an HR or management user rather than simply displaying raw LLM output.

The results are organized into digestible sections.

The UI includes:

- Overall score
- Quality label
- Dimension score cards
- Summary
- Issue cards
- Bias section
- Checklist
- Recommended improvements
- Improved JD section

The purpose of this design is to prevent the analysis from becoming a large wall of text.

The application prioritizes the most important information visually while keeping detailed explanations available within individual sections.

---

## 20. Improved JD Feature

A major improvement added beyond the basic analyzer is the ability to produce a sample improved job description.

The purpose is not to automatically publish the generated JD.

Instead, it gives the HR or hiring team a practical starting point based on the weaknesses identified by the analyzer.

The user should review and replace organization-specific information before publishing.

For example:

```text
Generated content:
"Experience with SIEM platforms such as Splunk or Microsoft Sentinel."

The user should verify whether these tools are actually used or required by their organization.
```

This prevents the generated draft from being treated as an authoritative source of company requirements.

---

## 21. Error Handling

The application includes error handling around the analysis process so that API or processing problems can be presented to the user without exposing a raw application traceback.

One development issue encountered during implementation was a circular import caused by an accidental import of `analyze_job_description` from `src.analyzer` inside `src/analyzer.py`.

The issue was resolved by correcting the module imports and keeping the analyzer function defined and imported from the appropriate module.

Another issue encountered was the Gemini API free-tier quota limit.

The API returned a `429 RESOURCE_EXHAUSTED` response after the project's free-tier request limit was reached.

This demonstrated an important real-world consideration when building applications around external LLM APIs: API quotas, rate limits, billing restrictions, and error handling must be considered during development and deployment.

---

## 22. Security Considerations

API credentials are stored in environment variables rather than hard-coded into the source code.

The project uses:

```text
.env
```

for local secrets and:

```text
.env.example
```

to document the required variable.

The `.env` file should remain excluded from Git.

When deploying, the Gemini API key should be configured through the hosting platform's secret/environment-variable settings rather than committed to the repository.

---

## 23. Deployment

The application was deployed using Streamlit Community Cloud.

### Live Application

https://ai-job-description-analyzer.streamlit.app/

The deployed application allows users to:

1. Enter a job description.
2. Run the AI analysis.
3. Review the overall score.
4. Inspect score breakdowns.
5. Review issues.
6. Check potential bias.
7. Review the JD quality checklist.
8. Read recommended improvements.
9. Review the generated improved JD.

---

## 24. Git and GitHub

Git was used for version control throughout development.

The project was structured as a Git repository with source code, tests, configuration examples, and documentation.

Sensitive configuration was intentionally excluded from version control.

Important files such as `.env.example`, `requirements.txt`, `README.md`, source code, and test files can be safely included in the repository.

---

## 25. Challenges Faced

### 1. Designing a Useful LLM Prompt

A basic prompt produced inconsistent or overly generic evaluations.

The solution was to create a detailed system instruction that explicitly defined:

- Evaluation dimensions
- Scoring rules
- Issue format
- Severity levels
- Bias behavior
- Checklist requirements
- Cybersecurity context
- Output expectations
- Anti-hallucination constraints

### 2. Making the Analysis Structured

Raw LLM text is difficult for an application to reliably display.

The solution was to use a structured schema so that the application could access individual fields such as scores, issues, bias flags, checklist items, and recommendations.

### 3. Balancing Completeness and Practicality

A JD should contain useful information, but not every optional field should cause a large penalty.

The scoring prompt was refined so that essential information has more importance while optional information such as reporting structure or preferred skills does not automatically make an otherwise strong JD poor.

### 4. Handling Cybersecurity Role Differences

Different cybersecurity positions have different technical requirements.

The solution was to make the analyzer context-aware instead of requiring a fixed list of tools.

### 5. API Quota Handling

During testing and UI development, the Gemini free-tier request limit was reached.

The API returned:

```text
429 RESOURCE_EXHAUSTED
```

This highlighted the importance of designing applications that account for external API limitations.

---

## 26. Skills Demonstrated

### AI / ML

- LLM application development
- Prompt engineering
- Structured LLM output
- AI-assisted text analysis
- Evaluation design
- Bias-language detection
- Domain-specific AI analysis

### Python

- API integration
- Environment variables
- Modular project structure
- Data/schema handling
- Error handling
- Automated testing

### Web Development

- Streamlit
- Interactive UI
- Result visualization
- User input handling
- Responsive presentation

### Software Engineering

- Git/GitHub
- Virtual environments
- Project organization
- Configuration management
- Testing
- Debugging
- Deployment

### Professional Skills

- Problem definition
- Requirement analysis
- User-focused design
- Iterative development
- Technical documentation
- Portfolio presentation

---

## 27. What I Learned

This project strengthened my understanding of how to move from a real-world problem to a working AI application.

Key lessons include:

- An LLM application needs more than a single prompt.
- Structured output makes AI responses much easier to integrate into software.
- Prompt instructions strongly influence the consistency and usefulness of results.
- Domain context matters when evaluating technical content.
- AI-generated recommendations should be actionable rather than generic.
- UI design is important because even useful AI output becomes difficult to use when presented as a wall of text.
- External APIs introduce real-world constraints such as quotas and rate limits.
- Testing AI applications requires diverse input cases, including both strong and intentionally poor examples.
- Deployment and documentation are part of delivering a complete software product.

---

## 28. Future Improvements

Potential future versions could include:

- PDF/DOCX job description upload
- Job-description version comparison
- Before/after score comparison
- Role-specific evaluation templates
- Custom company JD checklists
- Industry-specific terminology checks
- More advanced bias detection
- Explainable score calculations
- Saved analysis history
- Export analysis as PDF
- Authentication and user accounts
- Analytics dashboard
- Human review workflow
- Multi-model support
- More robust automated evaluation benchmarks

---

## 29. Limitations

The application is an AI-assisted analysis tool and should not be treated as a final authority.

Important limitations include:

- LLM output can vary between requests.
- Scores are qualitative AI assessments rather than scientifically validated hiring metrics.
- Bias detection can produce false positives or miss subtle wording.
- The analyzer cannot know company-specific requirements unless they are provided.
- Generated improvements should be reviewed by a human before publication.
- External API availability and quotas can affect the application.

The tool is intended to support HR and hiring teams, not replace human judgment.

---

## 30. Portfolio Summary

**AI Job Description Analyzer** is an LLM-powered Streamlit application designed for cybersecurity organizations to review and improve job descriptions before publication.

The application evaluates JDs across five dimensions — clarity, completeness, specificity, professionalism, and inclusivity — while also identifying potential bias, checking essential JD components, generating actionable recommendations, and producing a sample improved description.

The project demonstrates practical AI application development, prompt engineering, structured LLM integration, Python development, Streamlit UI development, testing, Git/GitHub workflow, API configuration, error handling, and cloud deployment.

**Live Demo:** https://ai-job-description-analyzer.streamlit.app/

---

## 31. Project Status

Completed.

- [x] Problem understood and defined
- [x] Research and planning completed
- [x] Development environment configured
- [x] Gemini API integrated
- [x] Core JD analysis implemented
- [x] Five scoring dimensions implemented
- [x] Issue detection implemented
- [x] Bias-language detection implemented
- [x] JD quality checklist implemented
- [x] Recommendations implemented
- [x] Improved JD generation implemented
- [x] Streamlit UI completed
- [x] Test cases created
- [x] Test suite executed
- [x] Error handling added
- [x] Git/GitHub repository prepared
- [x] Application deployed
- [x] Documentation prepared

---

## 32. Demo

Live application:

https://ai-job-description-analyzer.streamlit.app/

For a portfolio demonstration, a short screen recording can show:

1. Opening the application.
2. Entering a poor cybersecurity job description.
3. Running the analysis.
4. Showing the low overall score.
5. Showing detected issues and potential bias.
6. Showing the checklist.
7. Showing recommended improvements.
8. Showing the improved job description.
9. Repeating the process with a strong JD to demonstrate how the scores change.

---

## 33. Author

Developed as part of an AI/ML internship project focused on building practical, real-world AI applications.

