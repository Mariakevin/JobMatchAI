# User guide

This guide explains the browser workflow. It describes the current interface and its decision-support output.

## 1. Add your resume

In **Your profile source**, either choose a file or paste resume text.

Supported upload types:

| Format | Notes |
|---|---|
| PDF | Text-based PDFs; selectable text must be present |
| DOCX | Word documents |
| TXT | UTF-8 text files |

The upload limit is 5 MB. PDFs are limited to 100 pages and extracted or pasted text is limited to 60,000 characters. The application does not OCR scanned documents.

When text is pasted, parsing is triggered automatically after you stop typing for approximately 500 ms. The extracted profile includes supported education details, skills, projects, experience, certifications, and coursework.

## 2. Review the student profile

Use **Review & edit profile** to inspect or correct the profile fields and preferences used by analysis. Pay particular attention to:

- Degree, academic level, discipline, current year or semester, enrolment status, graduation date, and marks/CGPA.
- Skills that are actually known.
- Project or experience descriptions that substantiate those skills.
- Preferred work modes and locations.
- Relocation willingness, available hours, preferred internship duration, stipend minimum, and whether unpaid work is acceptable.

A resume parser is a heuristic extractor. A value shown in the profile is not proof that the original document stated it correctly. Correct extraction mistakes before analysis.

## 3. Add internship opportunities

In **Internship opportunities**, enter a title, company name, and the full description of each opportunity. Use **Extract criteria** to parse the description into supported structured fields.

The interface supports up to 20 postings per analysis. Review the extraction preview. The parser may identify:

- Work mode and location.
- Duration and weekly hours.
- Stipend amount, currency, and period, or unpaid status.
- Selected degree, discipline, academic, and other formal eligibility conditions.
- Required and preferred skills.
- Selected contradictions in duration or stipend statements.

Extraction is pattern-based. It does not understand every possible phrasing. A field left blank means the parser did not extract it; it does not establish that the employer did not specify it. Inspect the original listing and correct available inputs or remove erroneous extracted conditions before analysing.

## 4. Run the analysis

Select **Analyze** after adding a usable resume profile and at least one internship description. The backend evaluates each posting and sorts results by eligibility class, then descending profile-fit score, then title.

The result board includes filters for all postings, eligible postings, postings needing confirmation, and postings marked not eligible.

## 5. Read the results

Each result contains several independent views:

### Eligibility

The eligibility ledger shows each extracted condition, its expected value, the candidate fact used for comparison, and a reason. Possible condition states are:

- **PASS:** the available profile data satisfies the condition.
- **FAIL:** the available profile data does not satisfy the condition.
- **UNKNOWN:** the necessary profile information is not available or cannot be interpreted.
- **CONFLICT:** the listing contains a contradiction flagged by the parser.

The overall outcome is one of **ELIGIBLE**, **NOT_ELIGIBLE**, **NEEDS_CONFIRMATION**, or **NO_FORMAL_CRITERIA**. Read the reasons; do not treat missing facts as confirmed disqualifications.

### Skill evidence

Required and preferred skills are shown with one of the evidence states:

- **DEMONSTRATED:** a supporting match was found in a project, experience, coursework, certification, or recognised resume evidence.
- **SELF_REPORTED:** the skill appears in the resume skill list but no supporting project or experience evidence was found.
- **NOT_FOUND_IN_RESUME:** the skill was not found in the supplied resume.
- **CONFIRMED_GAP:** the student explicitly confirmed they do not currently have the skill.
- **UNKNOWN:** the matcher could not confidently resolve the evidence state.

Not found in a resume is not the same as not knowing a skill. Use the skill correction controls to self-report a skill or confirm a gap when appropriate. The workspace re-runs the analysis after a correction.

### Profile fit score

The score is a weighted measure of profile evidence and practical alignment. Its component breakdown and coverage percentage show which inputs contributed. A score may be provisional when eligibility needs confirmation or less than 70% of the possible component weight is evaluable.

The score is **not** a hiring probability, selection prediction, or guarantee. It cannot turn a failed mandatory eligibility rule into an eligible result.

### Practical fit

Practical fit compares supported work-mode, location, duration, available-hours, and stipend information. A comparison may remain unknown when either side does not supply enough information or when currencies cannot be compared directly.

### Listing risk indicators

Warnings may quote wording related to an application or registration fee, a security deposit or equipment fee, paid training, guaranteed selection claims, requests for sensitive information, or an unusually brief/vague description.

These are text-pattern indicators. They are not a background check, proof of fraud, or a legal assessment of an organisation. Verify the employer, vacancy, and terms independently before sharing sensitive information or paying money.

### Gap guidance

The gap report distinguishes missing required skills, missing preferred skills, confirmed gaps, and skills that are listed without supporting evidence. It may also provide questions to ask the employer.

## 6. Compare opportunities

When at least two results are available, select **Compare postings** to inspect them side by side. Use the comparison to review differences in eligibility, score, evidence, practical alignment, and warnings. Return to each expanded result for the full rationale.

## 7. A safe decision workflow

1. Compare the structured extraction with the original resume and internship page.
2. Correct student profile facts that are inaccurate.
3. Verify all mandatory eligibility conditions directly in the source listing.
4. Treat UNKNOWN and CONFLICT as follow-up work, not as a pass.
5. Investigate listing warnings using independent employer verification.
6. Make the application decision yourself; JobMatch AI does not submit applications.

For the exact calculation and rule behaviour, see [Decision model](decision-model.md).
