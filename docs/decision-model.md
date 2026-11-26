# Decision model

This page explains the current rule-based analysis. It is intended to make the outputs auditable, not to imply that heuristic extraction is always correct.

## 1. Separation of decision dimensions

The system does not reduce every decision to a single condition. It calculates and displays separate results:

1. **Formal eligibility:** whether extracted mandatory requirements are satisfied, failed, or unresolved.
2. **Skill evidence:** whether requested skills are supported by the supplied profile and its evidence.
3. **Practical fit:** whether known work and stipend preferences align.
4. **Profile fit score:** a weighted score across the components that can be evaluated.
5. **Listing risk indicators:** text patterns that warrant additional scrutiny.

A strong score does not erase a mandatory eligibility failure. A warning is not a fraud verdict. An absent resume keyword is not proof that a student lacks the skill.

## 2. Formal eligibility evaluation

Each extracted EligibilityCondition has a condition type, operator, expected value, mandatory flag, original source text, and logic-group name.

Individual conditions can produce:

| State | Meaning |
|---|---|
| PASS | The available student profile satisfies the extracted condition. |
| FAIL | The available student profile does not satisfy the extracted condition. |
| UNKNOWN | The profile does not supply enough information or the criterion cannot be interpreted. |
| CONFLICT | The internship parser identified a contradiction in the posting. |

### Boolean grouping

Within one mandatory logic group, conditions are treated as alternatives (OR): a group passes when at least one condition passes. Across distinct mandatory groups, all groups must pass (AND).

In simplified form:

~~~text
Overall mandatory result =
    AND over groups (
        OR over conditions within each group
    )
~~~

A group containing a conflict is unresolved unless another mandatory group conclusively fails; any mandatory failed group produces NOT_ELIGIBLE. If no mandatory condition fails but at least one group is unknown or conflicting, the result is NEEDS_CONFIRMATION. When all extracted mandatory groups pass, the result is ELIGIBLE.

If the listing has no extracted formal criteria and no contradiction, the result is NO_FORMAL_CRITERIA. This means the parser found no formal condition to evaluate; it does not mean that the employer has no requirements.

Non-mandatory conditions are displayed as evaluations but are excluded from the overall mandatory-group decision.

## 3. Skill evidence and provenance

The skill matcher normalises student and internship skill names using aliases from the project's taxonomy. It evaluates required and preferred skills separately.

| Evidence state | Interpretation |
|---|---|
| DEMONSTRATED | A matching skill has supporting evidence in a project, experience, coursework, certification, or resume evidence reference. |
| SELF_REPORTED | The skill is listed in the student's skills, but no supporting detail was found by the evidence search. |
| NOT_FOUND_IN_RESUME | The skill was not found in the supplied profile. This is not proof of inability. |
| CONFIRMED_GAP | The student explicitly marked the skill as a current gap. |
| UNKNOWN | The matcher cannot resolve the evidence state with confidence. |

The output can include a supporting excerpt and an evidence source. The profile editor supports student correction, and the workspace requests re-analysis after a correction.

## 4. Profile-fit score

The default component weights are:

| Component | Weight |
|---|---:|
| Required-skill evidence | 30% |
| Preferred-skill relevance | 15% |
| Project and experience evidence | 25% |
| Education relevance | 15% |
| Practical preference fit | 15% |

The implementation calculates a component only when it has enough input to evaluate that component. It then renormalises the weighted average over the evaluable components:

~~~text
Profile Fit =
  round(
    sum(component_score × component_weight for evaluable components)
    /
    sum(component_weight for evaluable components)
  )
~~~

Coverage is the sum of the original weights of evaluable components, expressed as a percentage. A score is returned as “Not enough information” when evaluable weight is below 20%. Otherwise, the score is marked provisional when formal eligibility needs confirmation or coverage is below 70%.

### Component rules

**Required skills:** DEMONSTRATED contributes 1.0, SELF_REPORTED contributes 0.75, while NOT_FOUND_IN_RESUME and CONFIRMED_GAP contribute 0.0. The component is the mean over extracted required skills.

**Preferred skills:** the same demonstrated/self-reported credit scheme is used over preferred skills. This component is evaluated only when preferred skills were extracted.

**Project and experience:** when the profile has projects or experience, the score is based on the fraction of matched skills marked DEMONSTRATED, plus a 20-point uplift, capped at 100. When there are no matched skills, the implementation uses 75 when projects exist and 50 when only experience exists. The component is unavailable when neither projects nor experience exist.

**Education relevance:** starts at 60 when education is present. The current implementation adds 30 for a normalised discipline in Computer Science, Information Technology, Data Science, or Artificial Intelligence. It adds 10 when the supplied CGPA is at least 75% of its stated scale, with a maximum of 100.

**Practical preferences:** this is the mean of the available practical comparisons. Comparisons are included only where the profile and posting provide enough data. See the next section.

### Important interpretation

The score is a heuristic measure of profile evidence and preference alignment. It is not calibrated against historical hiring outcomes, interview rates, or employer decisions. It must not be described as a probability of selection.

A NOT_ELIGIBLE outcome changes the score label to “Not eligible (academic/formal criteria unmet)”; it does not turn the numeric score into an eligibility pass. Always read the eligibility result and score as separate dimensions.

## 5. Practical preference comparisons

Only supplied values that can be compared contribute to practical fit.

| Dimension | Current comparison behaviour |
|---|---|
| Work mode | Matches if the posting's mode is in the student's preferred modes; an unspecified mode is not scored. |
| Location | Compared when a location and preferred locations exist for a non-remote role; a substring match or willingness to relocate counts as a match. |
| Duration | Exact or one-month difference counts as a match; a larger difference receives partial credit. |
| Weekly hours | Matches if the student's stated available hours cover the posting's required hours; otherwise it receives partial credit. |
| Unpaid work | Match when unpaid work is acceptable; mismatch otherwise. |
| Stipend | Compared only when both amounts are supplied and currencies match. Periods are normalised to monthly values when possible. |

No currency exchange rates are applied. A stipend expressed in another currency is left incomparable. The current output leaves the start-date comparison unknown; do not rely on it as an evaluated criterion.

## 6. Listing risk indicators

The internship parser uses text patterns and surrounding clauses to identify selected indicators. Categories include:

- Application or registration fee.
- Security deposit or equipment fee.
- Paid training requirement.
- Guaranteed selection or guaranteed job claims.
- Early requests for sensitive information such as bank details, passport copy, or Aadhaar.
- Very brief or vague postings when no other extractable facts are found.

Each RiskIndicator can include a severity, a title, the triggering excerpt, and an explanation. These rules are intentionally conservative signals. They cannot establish whether an organisation is fraudulent, legally compliant, or trustworthy.

## 7. Extraction uncertainty and limitations

Resume and internship extraction are heuristic. They depend on text layout, headings, wording, and known aliases. A missing extracted field may be caused by unsupported phrasing or parser limitations. In particular:

- Image-only and scanned PDF resumes are not OCR-processed.
- Resume parsing supports PDF, DOCX, and UTF-8 TXT, not image uploads.
- Internship extraction is not a general natural-language understanding model.
- Dates and some eligibility phrasing may remain unparsed.
- The current matching pipeline does not invoke an external generative model.

Review the original documents before acting on an analysis. The parsers and rule implementations in api/ are authoritative if this page and the code diverge.
