# JobMatch AI — Implementation Task for the Coding Agent

**Project:** JobMatch AI — Intelligent Internship Matching and Eligibility Assistant
**Task type:** Product enhancement / core MVP implementation  
**Research checked:** 14 November 2026  
**Primary objective:** Turn a student's resume and a collection of internship descriptions into a transparent, evidence-backed assessment of eligibility, fit, missing skills, practical constraints, and potential listing risks.

---

## 1. Mission

Build JobMatch AI as a **student-side internship decision-support tool**. A student should be able to upload a resume, review the information extracted from it, add one or more internship descriptions, and understand:

1. Whether they appear to meet each explicit eligibility condition.
2. Which skills and experiences in their profile support the internship requirements.
3. Which requirements are not evidenced in their resume, which are genuinely missing according to the student's confirmation, and which are unknown.
4. Whether practical details such as location, work mode, duration, start date, weekly hours, and stipend align with their preferences.
5. What they can improve before applying.
6. Whether the description contains warning signs that deserve manual verification.

The product must explain **why** it produced a result. Do not build a black-box resume percentage generator.

### Product positioning

> JobMatch AI helps students decide which internships are worth pursuing and what they should clarify or improve before applying. It does not predict selection, guarantee an interview, verify an employer, or make hiring decisions.

This is an analysis tool for internships supplied by the user. It is not an internship marketplace in this task.

---

## 2. Existing-market research and product gaps

The following findings are based on publicly documented product features reviewed on 14 November 2026. They are not a claim that every competitor lacks every feature; the scope is what the cited public documentation describes.

### 2.1 What existing products already do

| Product | Publicly documented capabilities | Product implication for JobMatch AI |
|---|---|---|
| LinkedIn | Job-match insights compare a member's profile/resume with required and preferred qualifications and provide a match summary. LinkedIn also offers natural-language job search and recommendations. | Basic profile-to-description matching and match summaries are not differentiators. Go deeper into internship-specific eligibility rules and evidence. |
| Handshake | AI-supported job discovery and personalized ranking; an optional job assistant can compare a student's profile/resume with a job and suggest profile improvements. | A conversational assistant and generic recommendations are not enough. Make every assessment auditable and student-controlled. |
| Simplify | Job-specific keyword match, missing-keyword feedback, resume content/format checks, job tracking, and application assistance. Its documentation explicitly says its scores are feedback, not an employer ATS score or an interview prediction. | Do not present a percentage as an acceptance probability. Show the underlying criteria, evidence, uncertainty, and limitations. |
| AICTE National Internship Portal | The portal publicly describes an AI matcher using branch, year, city, and skills; it also describes a common student profile, application tracking, stipend information, and verified postings. | Basic internship matching on branch/year/location/skills is already claimed by an Indian national portal. JobMatch AI should focus on deep analysis of documents the student supplies, not claim to replace the portal or offer equivalent listing verification. |

### 2.2 Gaps worth addressing

Implement the following as product opportunities. Phrase them as JobMatch AI's strengths, not as universal claims that competitors never support them.

1. **Eligibility is not the same as skill similarity.** A candidate can have strong technical skills but fail a formal condition such as degree, discipline, semester, graduation window, or minimum marks. Conversely, a resume may not mention a condition at all. Keep hard eligibility separate from skill-fit scoring.
2. **Internship eligibility can be conditional and multi-part.** A posting can specify course level, year/semester completed, marks thresholds, enrolment status, result-declaration windows, or alternative qualifying paths. Extract these into explicit rules, preserving `AND` / `OR` logic and the original wording.
3. **A missing resume keyword is not proof that a student lacks a skill.** Show the evidence source and use states such as `demonstrated`, `self-reported`, `not found in resume`, `student confirmed not yet learned`, and `unknown`. Never silently convert absence of evidence into a negative fact.
4. **A single match score hides important trade-offs.** Separate hard eligibility, skill fit, project/experience evidence, educational relevance, and practical preference fit. Let students see the score components and their supporting evidence.
5. **Student constraints deserve first-class treatment.** Include availability, semester timetable, weekly hours, location/relocation, remote/hybrid/on-site preference, duration, start window, and minimum acceptable stipend. A technically relevant role may still be impossible for the student to take.
6. **Students need an actionable gap analysis.** Distinguish mandatory skills from preferred skills, identify which project or experience already demonstrates a requirement, and suggest a realistic next step for unproven requirements.
7. **Internship listings can carry financial and personal-data risks.** Flag explicit requests for application fees, deposits, paid training as a condition of placement, premature sensitive-data requests, or vague employer/role information. These are warning indicators, not proof of fraud.
8. **Extraction must be correctable.** Students should be able to review and edit parsed resume facts and internship requirements before trusting the result. Ambiguous or contradictory text must be surfaced instead of guessed.

### 2.3 Research-based design principles

- Treat match scores as guidance, not predicted hiring outcomes. Simplify explicitly distinguishes its resume/keyword feedback from an employer ATS score or interview prediction.
- Make the matching logic inspectable. Recent literature reviews of AI recruitment/job-recommendation systems identify opacity, bias, weak semantic interpretability, and explainability as persistent concerns.
- Use a hybrid system: an LLM may extract and explain information, but deterministic application code must evaluate explicit eligibility rules and calculate the final score.
- Keep the user in control. Suggestions must not rewrite a resume, add skills, or apply to an internship without the student's explicit action.

---

## 3. Scope

### In scope — MVP

- Resume upload and text extraction.
- Review/edit of parsed student profile.
- Student preferences and practical constraints.
- Upload or paste one or more internship descriptions.
- Structured extraction of internship details and requirements.
- Review/edit of extracted internship details.
- Deterministic hard-eligibility evaluation with `ELIGIBLE`, `NOT_ELIGIBLE`, and `NEEDS_CONFIRMATION` outcomes.
- Explainable fit score with component breakdown.
- Evidence-backed skill matching and skill-gap analysis.
- Basic listing-risk indicators with quoted evidence.
- Results dashboard, internship detail view, and comparison view.
- Saving analysis history using the project's existing persistence/authentication patterns, if available.
- Unit, integration, and end-to-end tests.

### Explicitly out of scope for this task

- Scraping LinkedIn, Internshala, Handshake, AICTE, or other job boards.
- Bypassing platform restrictions, authentication, CAPTCHAs, or rate limits.
- Building a public internship marketplace or employer portal.
- Verifying an employer's legal identity or guaranteeing that a listing is genuine.
- Predicting selection probability, interview probability, or recruiter response.
- Automatic applications, email outreach, or resume submission.
- Rewriting the student's resume automatically or inventing achievements/skills.
- Training a custom foundation model.
- Making a final hiring or rejection decision about a person.

Do not expand scope into these areas without a separate task.

---

## 4. Required user journey

### A. Add student profile

1. Student uploads a resume.
2. System extracts text and structured information.
3. Student reviews and edits the extracted profile before matching.
4. Student fills any important missing details and preferences.

Profile fields should support at least:

- Education level and degree (for example, diploma, BCA, B.Tech, MCA, M.Tech, MBA, PhD).
- Discipline/branch and specialization.
- Institution name (optional for matching unless a posting explicitly requires it).
- Current year, semester, and current enrolment status.
- Expected graduation month/year or completion date.
- CGPA/percentage and grading scale, where supplied.
- Skills, with source/provenance for each skill.
- Projects, work experience, certifications, coursework, and relevant achievements.
- Current city/state/country.
- Preferred work modes: remote, hybrid, on-site.
- Willingness/ability to relocate or commute, if applicable.
- Earliest start date and availability window.
- Available hours per week.
- Preferred duration.
- Minimum acceptable stipend and stipend period (monthly, weekly, total, unpaid/volunteer acceptable).

Do not require unnecessary personal information. Name, photo, date of birth, gender, religion, caste, marital status, and other sensitive or irrelevant attributes must not affect matching.

### B. Add internship descriptions

Allow the student to:

- Upload supported files (at minimum PDF and DOCX if compatible with the current stack).
- Paste the full description as text.
- Add multiple internships in one session.
- Enter or retain the source URL manually as a reference; do not fetch/scrape the URL in this MVP.

For each description, extract and let the student review:

- Role/title and organization name.
- Role/domain and responsibilities.
- Work location and mode.
- Duration, start/end date, and weekly hours, when stated.
- Stipend amount, currency, and payment period; clearly distinguish unpaid, not disclosed, and negotiable.
- Application deadline.
- Eligible degrees, disciplines, years/semesters, enrolment status, graduation windows, marks/CGPA thresholds, and other formal conditions.
- Required skills, preferred skills, required experience, and tools/technologies.
- Required documents or application steps.
- Fees, deposits, paid training, or sensitive-data requests, if mentioned.
- Original source text and page/section location for each extracted requirement where technically available.

### C. Analyse and compare

For every internship:

1. Evaluate explicit hard eligibility conditions.
2. Assess skill and experience alignment.
3. Assess practical constraints/preferences.
4. Identify unknown or contradictory information.
5. Calculate a fit score only with a clear explanation of what it represents.
6. Show evidence and next steps.

Allow the student to compare several internships by eligibility, component scores, stipend, duration, work mode, location, deadline, and unresolved questions.

---

## 5. Core matching model

### 5.1 Separate hard eligibility from fit scoring

Implement a deterministic eligibility engine. The LLM may convert natural-language requirements into structured conditions, but it must not make the final eligibility decision by free-form reasoning.

Each formal condition must have:

- `condition_id`
- `condition_type` (degree, discipline, year, semester, enrolment, graduation_date, marks, location, citizenship/work_authorization if explicitly stated, availability, other)
- `operator` and normalized value(s)
- `logic_group` to preserve nested `AND` / `OR` conditions
- `is_mandatory`
- `original_text`
- `source_reference` (document/page/section/paragraph when available)
- `extraction_confidence`

Evaluate each condition as:

- `PASS` — the profile explicitly satisfies it.
- `FAIL` — the profile explicitly contradicts it.
- `UNKNOWN` — the profile or posting does not contain enough information.
- `CONFLICT` — the posting or profile contains contradictory values that need review.

Overall eligibility:

- `NOT_ELIGIBLE` only when an explicit mandatory condition is conclusively failed under the extracted AND/OR logic.
- `NEEDS_CONFIRMATION` when a mandatory condition is unknown, conflicting, or ambiguously extracted.
- `ELIGIBLE` when all explicit mandatory conditions pass and none remain unknown/conflicting.
- If the posting does not specify formal eligibility conditions, state `No explicit formal eligibility criteria found`; do not invent conditions.

Important rules:

- Do not infer that a student is ineligible because the resume omits a field.
- Do not infer eligibility from vague wording.
- Distinguish `not stated by the employer` from `not provided by the student`.
- Preserve alternative pathways. Example: `B.Tech or BCA` must not become `B.Tech only`.
- Preserve ranges and date boundaries. Confirm inclusive/exclusive interpretation where the wording is ambiguous.
- Treat minimum marks/CGPA as a hard condition only if the posting explicitly states it as such.
- A skill marked `required` is a skill-fit requirement. Its absence from the resume means `not evidenced`, not automatically `the student does not possess it`.
- Student confirmation can update a profile fact, but must retain provenance (`student_confirmed`) and timestamp.

### 5.2 Skill and experience matching

Build a normalized skill-matching layer:

- Normalize casing, punctuation, common abbreviations, and known aliases (for example, `JS` / `JavaScript` where equivalent).
- Keep a small editable alias/taxonomy file or table. Do not create broad equivalences that are technically false (for example, Java is not JavaScript).
- Use semantic matching only as a candidate suggestion when exact/alias matching is insufficient. Record the proposed equivalence and why it was suggested.
- Do not mark two skills as equivalent solely because an embedding similarity is high.
- Let students confirm or reject uncertain skill equivalences.

For each internship requirement, show one of:

- `DEMONSTRATED` — supported by a project, experience, certification, coursework, or a specific resume excerpt.
- `SELF_REPORTED` — student lists/confirms the skill but no concrete evidence is found.
- `NOT_FOUND_IN_RESUME` — not detected in the supplied document; this is not proof of absence.
- `CONFIRMED_GAP` — student explicitly confirms they do not currently have the skill/experience.
- `UNKNOWN` — extraction or evidence is inconclusive.

For each matched skill, show:

- Internship requirement text.
- Normalized skill.
- Student skill/evidence.
- Evidence source (resume section, project, experience, or student confirmation).
- Short supporting excerpt, where available.
- Confidence or review-needed state.

Do not fabricate project details, skill proficiency, work history, or qualifications.

### 5.3 Explainable fit score

The fit score is separate from formal eligibility and must never be labelled as a probability of being selected or hired.

For the MVP, implement a transparent, configurable 0–100 score with these default components:

| Component | Weight | What it measures |
|---|---:|---|
| Required-skill evidence | 30% | How many explicitly required skills are evidenced by the profile, with demonstrated evidence distinguished from self-report. |
| Preferred-skill relevance | 15% | Alignment with preferred/nice-to-have skills. |
| Project and experience evidence | 25% | Relevance of projects, work experience, coursework, and certifications to the responsibilities. |
| Education relevance | 15% | Alignment between the student's degree/discipline and the role, excluding formal conditions already evaluated by the eligibility engine. |
| Practical preference fit | 15% | Location/work mode, availability/start date, duration, weekly hours, and stipend preferences. |

Implementation requirements:

- Keep weights in one central configuration object, not scattered through UI code.
- Show component scores and the weight used; document the formula.
- Show `Not enough information` for components that cannot be evaluated. Do not silently treat unknown as zero.
- Normalize the score using only evaluable components and clearly show coverage/completeness; alternatively suppress the total until enough information exists. Pick one consistent approach and test it.
- Show the matched and missing evidence behind each component.
- Do not let a high skills score override `NOT_ELIGIBLE`.
- For `NEEDS_CONFIRMATION`, label any score as `provisional` and list the unresolved conditions prominently.
- Avoid false precision: display a whole-number score and a clear label such as `Profile fit`, not `chance of selection`.

### 5.4 Actionable skill-gap report

For each internship, generate a prioritised gap report:

- Required skills not found in the resume.
- Requirements the student confirmed they do not yet meet.
- Preferred skills not found.
- Missing proof that could potentially be added only if truthful (for example, a project exists but is not described in the resume).
- Questions to ask the employer or verify in the original posting.
- Suggested learning/project next steps for a small number of high-priority gaps.

Do not advise students to add keywords or claim skills they cannot substantiate. Clearly distinguish `learn this` from `document existing experience more clearly`.

### 5.5 Listing risk indicators

Detect and display warning indicators with the exact excerpt that triggered them. Include at least:

- Application/registration fee or payment required to apply.
- Security deposit, equipment fee, or payment to receive an offer.
- Paid training presented as a condition for getting the internship.
- Guaranteed selection/job claims that lack clear conditions.
- Requests for bank details, government ID numbers, or other sensitive information unusually early in the process.
- Missing or vague organization identity, role responsibilities, stipend terms, or contact/application details.

Risk labels must use careful language such as `Review carefully` or `Potential warning sign`. Never declare `fraud`, `scam`, or `verified` based only on text analysis. Do not assume every unpaid internship is fraudulent; show the unpaid status transparently and let the student apply their own preferences.

---

## 6. Suggested data structures

Adapt these to the existing database and naming conventions. Do not introduce a second data layer if the project already has an equivalent.

### StudentProfile

- `id`, `user_id`
- `education[]`
- `skills[]` with `name`, `normalized_name`, `source`, `evidence_refs[]`, `student_confirmed`, `confidence`
- `projects[]`, `experience[]`, `certifications[]`, `coursework[]`
- `preferences` containing location, work modes, relocation, start availability, weekly hours, duration, minimum stipend, stipend period
- `profile_completeness` and `last_reviewed_at`

### ResumeDocument

- `id`, `user_id`, private storage key, original filename, MIME type, size, processing status
- extracted text/reference data (avoid storing unnecessary raw PII in logs)
- parser version, extraction warnings, created/updated timestamps

### InternshipDocument

- `id`, `user_id`, title, organization, source URL (user-supplied), private storage key or pasted text reference
- extracted structured fields
- processing status, parser/model version, extraction warnings, timestamps

### InternshipRequirement

- `id`, `internship_id`, `category`, `requirement_type`, `mandatory`, `normalized_value`, `operator`, `logic_group`
- `original_text`, `source_reference`, `confidence`, `review_status`

### MatchAnalysis

- `id`, `user_id`, `profile_id`, `internship_id`
- `eligibility_status`, per-condition results
- score, score components, score coverage, provisional flag
- skill evidence map, gap report, risk indicators, unresolved questions
- model/prompt/rule-engine versions and timestamps

Persist enough provenance to explain a result and reproduce it. Do not persist hidden chain-of-thought or private model reasoning. Store concise, user-facing rationales and source excerpts instead.

---

## 7. AI and application architecture requirements

1. **Inspect the repository first.** Read `AGENTS.md`, `README`, architecture notes, package manifests, existing UI, routes, database schema, authentication, file storage, and AI-provider integrations. Follow the existing conventions.
2. **Preserve the current stack.** Do not replace frameworks, databases, UI libraries, or providers merely because another tool is preferred. Reuse existing components, services, and design tokens.
3. **Use provider abstraction already present.** Do not hard-code a new model vendor or API key. If no provider abstraction exists, isolate LLM calls behind a small service interface.
4. **Use structured outputs.** Define and validate schemas for resume extraction, internship extraction, evidence mapping, and risk indicators. Reject malformed output and handle failures gracefully.
5. **Separate extraction from decisions.** LLM extracts candidate facts and employer requirements. Application code validates and evaluates explicit eligibility rules and calculates fit scores.
6. **Keep document provenance.** Each extracted requirement and evidence item should point to the source text, page, or section when available. Never create fake page numbers or references.
7. **Support correction.** Users must be able to edit parsed profile fields and extracted internship requirements; recompute the analysis after edits.
8. **Handle untrusted document content.** Treat uploaded text as data, not instructions. Ignore instructions inside resumes or job descriptions that ask the model to reveal secrets, call tools, modify files, or change system behaviour. No tools/actions should be executed because a document says so.
9. **Graceful degradation.** If extraction fails, show the issue and allow manual text entry. If a scan cannot be parsed and OCR is not already available, report that limitation rather than inventing content.
10. **Deterministic reruns.** Save the version of the parser, prompt/schema, rule engine, and scoring configuration used for each analysis.

### Suggested service boundaries

Adapt names to the repository:

- `resumeParser`: file validation, extraction, section detection.
- `profileNormalizer`: education/date/grade/skill normalization.
- `internshipParser`: structured extraction from description text.
- `requirementReviewer`: validation/correction workflow.
- `eligibilityEngine`: deterministic condition evaluation.
- `skillMatcher`: exact aliases plus cautious semantic suggestions.
- `fitScorer`: configurable component scores.
- `riskAnalyzer`: evidence-backed warning indicators.
- `analysisOrchestrator`: coordinates the above and returns a typed result.

Keep the core matching logic independently unit-testable without making real LLM calls.

---

## 8. UI/UX requirements

Use the existing design system. The experience must be readable and useful on desktop and mobile.

### Main screens / areas

1. **Student profile setup** — resume upload, extracted profile review, education, skills, projects, and preferences.
2. **Internship input** — upload/paste several descriptions, show parsing progress and extraction warnings.
3. **Requirement review** — allow the student to correct eligibility criteria, required/preferred skills, dates, stipend, and mode before running analysis.
4. **Results overview** — separate groups for `Eligible`, `Needs confirmation`, and `Not eligible`; sort eligible results by fit score, not by an opaque default.
5. **Internship analysis detail** — eligibility checklist, score breakdown, supporting evidence, skill gaps, practical-fit assessment, risk indicators, and questions to verify.
6. **Comparison view** — compare at least two saved analyses side by side.

### Required interaction details

- Every status must have text; do not rely on colour alone.
- `NOT_FOUND_IN_RESUME` must not be styled as `FAIL`.
- Put unresolved mandatory conditions above the fit score.
- Let students expand the exact source excerpt used for a decision.
- Clearly mark information entered by the student versus extracted by AI.
- Show extraction errors and unsupported formats in plain language.
- Provide edit/reanalyse controls and clear loading, empty, and error states.

---

## 9. Security, privacy, and safety

- Reuse existing authentication and authorization. A student must only access their own profile, documents, and analyses.
- Store resumes and internship documents in private storage. Do not expose permanent public file URLs.
- Validate file extension, MIME type, size, and file contents where supported. Generate safe storage names; do not trust uploaded filenames.
- Do not put full resume text, phone numbers, email addresses, or sensitive identifiers into application logs, analytics, or error messages.
- Avoid sending direct identifiers to the LLM when they are not needed for matching. Retain the minimum profile information required for the task.
- State what is stored and how the user can delete it. Deletion should remove the related database records and stored files where the existing architecture permits.
- Do not use protected or sensitive attributes to rank candidates. Do not infer them.
- Do not claim to have verified a company, listing, credential, or stipend unless a separate trusted verification source actually supports that claim.
- Do not auto-apply or make irreversible decisions.

---

## 10. Acceptance criteria

The task is complete only when all applicable criteria below pass.

### Upload and extraction

- [ ] A student can upload a supported resume and receive a structured profile draft.
- [ ] A student can edit the extracted profile before matching.
- [ ] A student can paste or upload multiple internship descriptions.
- [ ] The app clearly handles unsupported, empty, corrupt, or unparseable files.
- [ ] Extracted internship requirements can be reviewed and corrected.

### Eligibility correctness

- [ ] Hard eligibility is evaluated separately from skill fit.
- [ ] Every mandatory criterion has a `PASS`, `FAIL`, `UNKNOWN`, or `CONFLICT` result and a human-readable reason.
- [ ] `UNKNOWN` never silently becomes `FAIL` or `PASS`.
- [ ] Alternative criteria and AND/OR conditions are preserved.
- [ ] A student is marked `NOT_ELIGIBLE` only when an explicit mandatory condition is conclusively failed.
- [ ] If no formal eligibility conditions are stated, the system says so and does not invent them.

### Matching and explainability

- [ ] The fit score has a visible, documented component breakdown and is not described as selection probability.
- [ ] A score cannot override a failed hard-eligibility condition.
- [ ] For every matched requirement, the user can inspect the supporting profile evidence or see that it is self-reported.
- [ ] A missing skill in the resume is labelled `NOT_FOUND_IN_RESUME`, not `student lacks this skill`.
- [ ] The user can correct a skill equivalence or extracted fact and rerun analysis.
- [ ] Skill-gap recommendations distinguish truthful resume improvement from learning a new skill.

### Practical fit and risk review

- [ ] Work mode, location, duration, dates, weekly hours, and stipend are compared when the posting and profile provide the information.
- [ ] Unstated details are shown as unknown/not disclosed, not guessed.
- [ ] Potential fees/deposit/sensitive-data indicators show the triggering excerpt.
- [ ] Risk indicators are warnings, not definitive accusations or verification claims.

### Reliability and quality

- [ ] Eligibility and scoring logic have unit tests independent of the LLM.
- [ ] Parser/schema validation has tests for malformed and incomplete model output.
- [ ] API/data access tests verify user-level authorization.
- [ ] At least one end-to-end test covers resume upload → profile review → internship upload → analysis → correction → reanalysis.
- [ ] No real API key or secret is committed.
- [ ] Loading, no-data, partial-data, and error states are implemented.
- [ ] Documentation explains setup, supported formats, limitations, scoring, and deletion behaviour.

---

## 11. Mandatory test scenarios

Create fixtures and automated tests for these cases. Use synthetic student data and synthetic internship descriptions; do not commit real resumes or personal data.

1. **Straightforward eligible student:** Candidate's degree, current semester, marks, and graduation date satisfy all explicit conditions.
2. **Degree mismatch:** Posting explicitly accepts B.Tech only; profile is BCA. Eligibility must fail with the exact reason.
3. **Alternative degrees:** Posting accepts B.Tech OR BCA; profile is BCA. Do not incorrectly reject.
4. **Unknown marks:** Posting requires a minimum CGPA, but the student's profile has no CGPA. Return `NEEDS_CONFIRMATION`, not `NOT_ELIGIBLE`.
5. **Resume omission:** Posting requires Python; resume does not mention Python. Show `NOT_FOUND_IN_RESUME`; do not assert the student cannot use Python.
6. **Student-confirmed gap:** Student explicitly says they do not know Python. Show `CONFIRMED_GAP` and update the analysis.
7. **Alias match:** `JS` and `JavaScript` may match through an explicit alias; `Java` and `JavaScript` must not.
8. **Required versus preferred:** Missing preferred skill affects the preferred-skill component, not hard eligibility.
9. **Compound eligibility:** Posting requires an enrolled postgraduate student AND one of two specified disciplines. Evaluate the boolean logic correctly.
10. **Graduation window:** Posting has an explicit graduation-date range. Test dates before, inside, and after the range, including boundary dates.
11. **Contradictory posting:** Same description gives inconsistent stipend/duration/eligibility details. Return `CONFLICT` or a review warning; do not choose arbitrarily.
12. **Practical mismatch:** Student requires remote work, posting is explicitly on-site. Show a preference mismatch without automatically declaring academic ineligibility.
13. **Unpaid internship:** Show unpaid status and compare against the student's preference; do not label it a scam.
14. **Fee request:** Posting asks for a payment to apply. Show a warning with the exact evidence excerpt, without asserting fraud as fact.
15. **Prompt injection in document:** A description contains instructions directed at the AI. Treat them as untrusted text and continue only with ordinary extraction.
16. **Low-quality scan:** If text extraction fails, show a useful recovery path or manual paste option; do not create inferred fields.

---

## 12. Implementation order

Execute in this order. Keep the application runnable after each phase.

### Phase 0 — Repository audit

- Read the repository instructions and architecture.
- Identify existing upload, parsing, auth, database, AI, and UI components.
- Record what can be reused and any blockers.
- Do not pause after the audit; proceed with implementation using the existing architecture.

### Phase 1 — Domain models and ingestion

- Add/update types and database schema.
- Implement resume and internship-description upload/paste flows.
- Add file validation, private storage, and extraction-status handling.

### Phase 2 — Structured extraction and review

- Implement resume profile extraction.
- Implement internship detail/requirement extraction.
- Validate LLM output against schemas.
- Build editable review screens and persist student corrections.

### Phase 3 — Eligibility engine

- Implement the condition representation and AND/OR evaluation.
- Implement PASS/FAIL/UNKNOWN/CONFLICT logic.
- Add the mandatory eligibility unit tests before connecting the UI.

### Phase 4 — Skill matching and fit scoring

- Implement skill normalization and explicit alias mappings.
- Implement evidence provenance and student-confirmed skills/gaps.
- Implement the configurable score and component breakdown.
- Add gap-analysis output with non-fabrication safeguards.

### Phase 5 — Risk indicators and results UI

- Implement evidence-backed listing warnings.
- Build result groups, detail view, and comparison view.
- Add edit/reanalyse and history flows using existing app conventions.

### Phase 6 — Hardening and documentation

- Add authorization, privacy, file-handling, and prompt-injection tests.
- Add end-to-end coverage.
- Update project documentation and environment examples.
- Run formatter, linter, type-checker, test suite, and production build. Fix regressions introduced by this task.

---

## 13. Agent working rules

- Make changes in the existing repository; do not create a parallel demo app.
- Read and follow `AGENTS.md` and any nested project instructions.
- Do not overwrite working features or replace the existing stack without a demonstrated technical necessity.
- Prefer small, cohesive modules and typed interfaces over one large prompt or component.
- Do not hard-code secrets, personal data, model responses, or demo-only matching outcomes.
- Do not use fake data in the actual user workflow. Synthetic fixtures are allowed in tests and clearly labelled demo content only.
- If an external service or credential is unavailable, implement a clear adapter/error state rather than pretending the feature works.
- Do not silently skip failing tests. Report any unrelated pre-existing failures separately.
- After implementation, provide a concise completion report covering files changed, architecture decisions, tests run, known limitations, and any manual setup required.

---

## 14. Research references

1. **LinkedIn Help — Find how you match up with jobs** (job-match insights compare profile/resume data with required and preferred qualifications):  
   https://www.linkedin.com/help/linkedin/answer/a7120158
2. **LinkedIn Help — Discover new opportunities with AI-powered job search** (natural-language job search and personalized relevance):  
   https://www.linkedin.com/help/linkedin/answer/a6889044
3. **Handshake Help Center — About AI-powered features in Handshake for students** (AI-assisted job discovery, job assistant, profile/resume-based coaching, student control):  
   https://support.joinhandshake.com/hc/en-us/articles/38856960612631-About-AI-powered-features-in-Handshake-for-students
4. **Simplify Help Center — Understand Resume Score and keyword matching** (keyword coverage, resume feedback, and explicit limitation that scores are not an ATS score or interview prediction):  
   https://help.simplify.jobs/help/articles/2175778-understand-resume-score-and-keyword-matching
5. **AICTE National Internship Portal** (publicly describes matching by branch, year, city, and skills, plus application tracking and internship information):  
   https://internship.aicte-india.org/
6. **Explainable artificial intelligence in the talent recruitment process — a literature review (2025)** (discusses resume parsing, explainability, bias, and interpretability issues):  
   https://doi.org/10.1080/23311975.2025.2570881
7. **Representing jobs and job seekers in AI-based recommender systems: A literature review (2026)** (discusses semantic representation, bias, opacity, interpretability, and hybrid approaches):  
   https://www.sciencedirect.com/science/article/pii/S0952197626007311
8. **NITI Aayog Internship Scheme guidelines (2018 PDF)** (an example of multi-part academic eligibility conditions; use only as an illustration of rule complexity, not as current eligibility policy for other internships):  
   https://workforindia.niti.gov.in/intern/PDF/NITI_Internship_Guidelines.pdf

---

## Definition of done

A student can upload a resume and several internship descriptions, review the extracted data, receive a defensible eligibility result, understand the fit score and its evidence, see what is missing or unknown, identify practical mismatches and potential warning signs, correct the extracted information, and rerun the analysis. The system must be useful without scraping job boards, must not invent candidate qualifications, and must not imply that its score predicts selection.
