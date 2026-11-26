# Project overview

## Abstract

JobMatch AI is a web application intended to help students evaluate internship opportunities from the candidate's perspective. It accepts resume content and internship descriptions, extracts structured information, evaluates explicit academic eligibility conditions, checks skills against resume evidence, compares practical preferences, and highlights selected warning indicators in a listing.

The system is designed around explainability. Eligibility is evaluated by deterministic application logic. Skill matches retain evidence states and supporting excerpts. The profile-fit score exposes its component breakdown and data coverage. Listing warnings quote the text that triggered them. The score is not an estimate of selection probability and cannot override a failed mandatory condition.

## 1. Problem definition

Students often compare internships by reading lengthy job descriptions and manually checking whether their degree, semester, marks, skills, location, schedule, and stipend meet the stated requirements. Generic keyword-based matching can obscure the difference between an explicit eligibility requirement and a preferred skill. It can also treat a skill missing from a resume as proof that the student does not know it.

A single similarity percentage is not sufficient for an application decision. A high skill similarity score should not hide a mandatory degree mismatch. Missing information should not automatically become a failure. Students also need to notice potentially concerning listing language, such as a request for an application fee or security deposit, without treating an automated warning as a final fraud determination.

## 2. Objectives

The current project aims to:

1. Extract text from supported resume formats and build a structured student profile.
2. Convert internship descriptions into structured role details and formal eligibility conditions.
3. Evaluate mandatory conditions with explicit PASS, FAIL, UNKNOWN, and CONFLICT states.
4. Distinguish demonstrated skills, self-reported skills, skills absent from the supplied resume, and student-confirmed gaps.
5. Calculate an explainable profile-fit score from available evidence and disclose its coverage.
6. Compare work mode, location, duration, weekly hours, and stipend preferences when the required information exists.
7. Highlight selected listing-risk indicators with their triggering excerpts.
8. Give students an opportunity to review and correct profile information before relying on an analysis.

## 3. Scope

### Included in the current implementation

- Resume upload for PDF, DOCX, and UTF-8 TXT files, subject to documented size and page limits.
- Resume text paste and automatic parsing.
- Internship title, company, and description entry.
- Rule-based extraction of selected role details, skills, stipend, work mode, duration, hours, and formal eligibility statements.
- Deterministic eligibility, skill-evidence, practical-fit, and score calculations.
- Listing-risk heuristics with quoted excerpts.
- Match filtering, expanded result details, skill corrections, and side-by-side comparison.
- A React frontend and a FastAPI backend.

### Not included in the current implementation

- OCR or image/scanned-resume processing. Image-only or scanned PDFs without extractable text are not supported.
- Live internship discovery, web scraping, or employer verification.
- A predictive model for hiring or interview probability.
- Automated application submission or messaging to employers.
- Persistent user accounts, database-backed profiles, or saved analysis history.
- Currency conversion between different stipend currencies.
- Reliable evaluation of application dates or date-window preferences.
- An external LLM service in the current request-processing pipeline.

These boundaries are intentional documentation of the repository as it exists, not a statement that the features could never be added.

## 4. Existing approach and proposed approach

| Aspect | Manual or keyword-only comparison | JobMatch AI approach |
|---|---|---|
| Academic requirements | Manually inspect the posting | Evaluate extracted mandatory conditions separately |
| Missing profile facts | Easy to interpret as a mismatch | Preserve unknown or missing evidence |
| Skills | Keyword overlap | Normalised skill names plus provenance |
| Fit summary | Often one opaque percentage | Weighted components, coverage, and reasons |
| Practical constraints | Often checked informally | Compare supported preferences when both sides disclose values |
| Listing concerns | Rely on the reader noticing the wording | Show heuristic warnings and the triggering excerpt |

## 5. System users

The primary user is a student or early-career candidate. The student supplies their resume and the internship descriptions they want to assess. The application does not have a recruiter or employer decision-making role.

## 6. Functional requirements

| ID | Requirement |
|---|---|
| FR-01 | Accept PDF, DOCX, and UTF-8 TXT resumes up to the configured upload limit. |
| FR-02 | Accept pasted resume text and parse it into a structured profile. |
| FR-03 | Accept and analyse up to 20 internship descriptions in one matching request. |
| FR-04 | Extract supported role attributes and formal eligibility conditions. |
| FR-05 | Evaluate mandatory eligibility conditions without silently converting unknown facts into failures. |
| FR-06 | Match required and preferred skills while preserving evidence status. |
| FR-07 | Calculate and display profile-fit components and coverage. |
| FR-08 | Compare supported practical preferences. |
| FR-09 | Display heuristic listing warnings with their source excerpts. |
| FR-10 | Allow profile corrections and re-analysis. |
| FR-11 | Filter results and compare multiple internship postings. |

## 7. Non-functional requirements

- **Explainability:** show the reason behind eligibility states, skill evidence, and warning indicators.
- **Usability:** present results in a readable, keyboard-accessible interface.
- **Input validation:** constrain upload size, document length, and request field lengths.
- **Reliability:** return structured validation and processing errors rather than silently accepting malformed input.
- **Maintainability:** keep parsing, eligibility, scoring, orchestration, API, and UI responsibilities in separate modules.
- **Privacy by default:** the current application does not implement accounts or a database-backed history; avoid treating the local prototype as a hardened production service.

## 8. System environment

| Layer | Current technology |
|---|---|
| Frontend | React 18, TypeScript 5.7, Vite 6 |
| Styling | Plain CSS with project design tokens |
| Icons | lucide-react |
| Backend | Python, FastAPI, Pydantic models, Uvicorn |
| Resume extraction | pypdf and python-docx |
| Tests | Python unittest |
| Development proxy | Vite proxies /api to http://localhost:8000 |

See [Getting started](getting-started.md) for versions and commands, and [Architecture](architecture.md) for module responsibilities.
