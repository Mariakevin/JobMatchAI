# Architecture

## 1. Architectural style

JobMatch AI uses a separated frontend/backend architecture. The browser interface is a React and TypeScript application served by Vite. It communicates with a Python FastAPI service through JSON and multipart HTTP requests. The backend uses Pydantic models to represent profiles, internship postings, eligibility evaluations, skill evidence, and match results.

The analysis pipeline is deliberately composed of parsing and deterministic application logic. The current backend does not call an external LLM to produce match calculations or explanations.

## 2. Context and data flow

~~~mermaid
flowchart TD
    U[Student] --> UI[React workspace]
    UI -->|Resume file or pasted text| API[FastAPI]
    UI -->|Internship description| API
    API --> RP[Resume parser]
    API --> IP[Internship parser]
    RP --> P[StudentProfile]
    IP --> J[InternshipDetail]
    P --> O[Matching orchestrator]
    J --> O
    O --> E[Eligibility engine]
    O --> S[Skill matcher]
    O --> F[Practical fit and score]
    O --> R[Listing risk analysis]
    E --> M[MatchResponse]
    S --> M
    F --> M
    R --> M
    M --> UI
    UI --> V[Results and comparison views]
~~~

## 3. Frontend structure

The frontend entry point is src/main.tsx. src/App.tsx composes the main workspace and delegates stateful workflows to the useWorkspace hook.

| Path | Responsibility |
|---|---|
| src/App.tsx | Page composition and workspace wiring |
| src/hooks/useWorkspace.ts | Resume state, posting state, request sequencing, cancellation, analysis, corrections, and filters |
| src/lib/api.ts | HTTP requests, timeouts, cancellation forwarding, and API error normalization |
| src/lib/defaults.ts | Initial student preferences, demo profile, and example internship |
| src/lib/format.ts | Display formatting helpers |
| src/lib/matchFilters.ts | Result filtering and counts |
| src/types.ts | TypeScript representations of API data |
| src/components/profile/ | Resume source, profile snapshot, editor, preferences, and skill controls |
| src/components/internships/ | Posting editor, extracted preview, and condition editor |
| src/components/results/ | Eligibility, fit score, evidence, warnings, gaps, and comparison views |
| src/components/ui/ | Reusable interface primitives |
| src/styles/ | Design tokens and base, layout, form, card, results, and modal styles |

The workspace manages asynchronous operations using AbortController and request sequence identifiers. This helps prevent a late response from an earlier upload or analysis from overwriting a newer interaction. Pasted resume text is parsed with a 500 ms debounce.

## 4. Backend structure

| Module | Responsibility |
|---|---|
| api/main.py | FastAPI application, request schemas, routes, CORS, error handling |
| api/models.py | Pydantic models and enums shared across the pipeline |
| api/resume_parser.py | PDF/DOCX/TXT text extraction and heuristic profile parsing |
| api/internship_parser.py | Internship attribute extraction and listing-risk indicators |
| api/taxonomy.py | Canonical names and aliases for degrees, disciplines, skills, and currencies |
| api/eligibility_engine.py | Individual condition evaluation and overall eligibility |
| api/skill_matcher.py | Required/preferred skill matching, provenance, and gap report |
| api/fit_scorer.py | Practical preference comparison and weighted fit score |
| api/orchestrator.py | Runs the independent analysis stages and sorts results |
| api/matcher.py | Legacy matching path retained for compatibility |

## 5. Analysis sequence

1. The frontend sends resume content for extraction or text parsing.
2. The backend extracts document text (when a file is supplied) and builds a StudentProfile.
3. For each internship, the frontend sends its title, company, and description to the internship extraction endpoint.
4. The parser creates an InternshipDetail with the fields it can identify.
5. The frontend allows the student to review and edit information and extracted conditions.
6. The structured profile and internship details are submitted to the matching endpoint.
7. The orchestrator independently evaluates listing risks, mandatory eligibility, skill evidence, practical preferences, and profile fit.
8. The orchestrator sorts results by eligibility group, score, and title.
9. The frontend renders the MatchResponse and allows filtering, expansion, correction, re-analysis, and comparison.

## 6. Backend component interactions

~~~mermaid
flowchart LR
    API[main.py] --> RP[resume_parser.py]
    API --> IP[internship_parser.py]
    API --> ORCH[orchestrator.py]
    ORCH --> EL[eligibility_engine.py]
    ORCH --> SK[skill_matcher.py]
    ORCH --> FS[fit_scorer.py]
    IP --> TX[taxonomy.py]
    RP --> TX
    EL --> TX
    SK --> TX
    FS --> TX
    ORCH --> MODELS[models.py]
    API --> MODELS
~~~

## 7. Data model overview

The main domain objects are:

- StudentProfile: education, skill provenance, projects, experience, certifications, coursework, preferences, and original extracted text.
- InternshipDetail: identity and description, work arrangement, location, compensation, timing, formal conditions, skills, and contradiction metadata.
- EligibilityResult: overall eligibility state, summary, unresolved mandatory count, and condition evaluations.
- SkillMatchItem: requested skill, evidence state, source, excerpt, and confidence.
- FitScore: whole-number score (when enough data exists), provisional flag, coverage, component breakdown, and unresolved reasons.
- RiskIndicator: category, severity, title, matching excerpt, and explanation.
- GapReport: skill or requirement gaps and questions for the employer.
- InternshipMatchAnalysis: all analysis outputs for one posting.
- MatchResponse: the student profile, sorted posting analyses, and scoring weights.

Pydantic model definitions in api/models.py are authoritative for the complete field-level schema.

## 8. Runtime boundaries

The current repository contains no database layer, authentication subsystem, background worker, or external AI service integration. The FastAPI service is a synchronous analysis API with asynchronous file upload handling and thread-pool execution for document extraction/parsing. The frontend and backend are separate development processes.

For route contracts, see [API reference](api-reference.md). For rule details, see [Decision model](decision-model.md).
