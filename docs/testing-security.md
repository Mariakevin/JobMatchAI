# Testing and security

## 1. Test suite

The repository uses Python's built-in unittest framework. Test files are under tests/.

| Test file | Focus |
|---|---|
| test_api.py | API route behaviour and validation |
| test_e2e_workflow.py | End-to-end matching workflow |
| test_hardening.py | Input edge cases, parser hardening, and adversarial text cases |
| test_matcher.py | Legacy matcher behaviour |
| test_scenarios.py | Mandatory eligibility, evidence, practical-fit, and warning scenarios |

The current source contains 72 test methods across these five test modules (5 + 1 + 46 + 4 + 16). This count is a source inspection, not a claim that the suite was executed during documentation generation.

Run tests from the repository root with the virtual environment activated:

~~~bash
python -m unittest discover -s tests -v
~~~

Build the frontend separately:

~~~bash
npm run build
~~~

When changing a parser, decision rule, or result model, add or update tests for both typical inputs and failure/unknown cases. For a behaviour that is visible in the UI, add coverage at the API or workflow level where practical.

## 2. Test design principles

Recommended test cases include:

- Resume file type, size, page count, encoding, corrupted-document, empty-document, and maximum text-length boundaries.
- Resume extraction with missing section headings, alternate headings, and misleading numeric content.
- Internship extraction with alternative phrasing, negated phrases, absent values, multiple stipend statements, and duration contradictions.
- Eligibility with alternative conditions in one logic group, mandatory conditions across groups, missing profile facts, and posting contradictions.
- Skill alias matching without conflating similar names; for example, Java and JavaScript must remain distinct.
- Profile-fit calculation when all components are evaluable, when some components are missing, and when evaluable coverage is below the minimum.
- Currency mismatch and stipend-period normalisation.
- Risk indicators that quote the correct passage and avoid triggering on explicitly negated language.
- Request cancellation and overlapping frontend operations.

## 3. Input and document handling

The resume parser accepts PDF, DOCX, and UTF-8 TXT. It enforces a 5 MiB file limit, a 100-page PDF limit, and a 60,000-character text limit. It rejects unsupported formats and documents from which no readable text can be extracted.

The current parser reads embedded PDF text and DOCX paragraphs. It does not run OCR, and it does not implement image upload. Scanned/image-only reports are therefore outside the supported input scope.

Internship extraction and listing-risk checks are heuristic. Treat all source documents and job descriptions as untrusted input. Never interpret their contents as executable instructions.

## 4. Privacy and deployment boundaries

The current source tree has no database or authentication module. The API returns structured profile data, including the original raw text field, to the caller. The frontend holds working data in application state. Do not assume that this provides account isolation, access control, deletion guarantees, or production-grade data retention controls.

Before deploying for real student resumes:

- Require HTTPS.
- Add an appropriate authentication and authorisation model if the service is shared.
- Define retention and deletion behaviour for uploaded and parsed resume data.
- Avoid logging resume contents or unnecessary personal data.
- Restrict upload size and request rates at the application and hosting layers.
- Keep dependencies updated and review dependency alerts.
- Store secrets outside source control.
- Review CORS origins; the current allow-list is for local development only.
- Review hosting, backups, telemetry, and error reporting for personal-data exposure.

## 5. Prompt injection and AI boundaries

The current analysis pipeline does not call a generative AI model. Resume and listing content is processed by deterministic parsers and rule-based functions. This reduces the risk of a document instructing an LLM to change system behaviour, but it does not make arbitrary uploaded files intrinsically safe.

If a generative AI feature is introduced later, treat resume and listing text as untrusted data, isolate it from system instructions, validate all structured model output, and keep eligibility and numeric scoring in deterministic code. Do not let an LLM invent missing profile facts or override an explicit mandatory rule.

## 6. Listing warning interpretation

Listing-risk indicators are not definitive fraud classification. They are heuristics designed to ask the student to review exact wording and confirm terms with the organisation. False positives and missed phrasing are possible. The UI should continue to communicate uncertainty and should never present warnings as verified accusations.

## 7. Accessibility

The existing design research documents target WCAG 2.2 AA-oriented practices, including semantic status labels, keyboard focus, contrast, and reduced-motion considerations. A design target is not a formal accessibility conformance statement. Use keyboard-only checks and assistive technology testing alongside automated audits for changes to interactive components.

Reference: [W3C Web Content Accessibility Guidelines (WCAG) overview](https://www.w3.org/WAI/standards-guidelines/wcag/).
