# API reference

The backend is a FastAPI application defined in api/main.py. It accepts JSON requests and multipart resume uploads. Request validation is implemented with Pydantic models and FastAPI field constraints.

## Base URL

Local development default: http://127.0.0.1:8000

Interactive Swagger UI: /docs  
OpenAPI JSON: /openapi.json

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | /api/health | Service health and API version |
| POST | /api/resume/extract | Extract text from an uploaded resume and return a structured profile |
| POST | /api/resume/parse-text | Parse pasted resume text |
| POST | /api/internship/extract | Extract supported fields from one internship description |
| POST | /api/match | Analyse a structured request or the legacy resume-text request |
| POST | /api/reanalyze | Re-run structured matching after profile changes |

## GET /api/health

Example response:

~~~json
{
  "status": "ok",
  "version": "0.2.0"
}
~~~

## POST /api/resume/extract

Content type: multipart/form-data  
Field: file

Accepted extensions: .pdf, .docx, .txt

Limits:
- 5 MiB maximum file size.
- 100 pages maximum for PDF.
- 60,000 extracted characters maximum.

The PDF implementation extracts embedded text. It does not perform OCR. Empty or image-only documents return a validation error.

Example response shape:

~~~json
{
  "text": "Extracted resume text...",
  "filename": "candidate.pdf",
  "structured_profile": {
    "id": "profile_1",
    "education": [],
    "skills": [],
    "projects": [],
    "experience": [],
    "certifications": [],
    "coursework": [],
    "preferences": {},
    "raw_text": "Extracted resume text..."
  }
}
~~~

The complete StudentProfile schema is defined in api/models.py and reflected by the generated OpenAPI schema.

## POST /api/resume/parse-text

Content type: application/json

Request:

~~~json
{
  "text": "EDUCATION
MCA ...
SKILLS
Python, SQL..."
}
~~~

The text must be non-empty and no longer than 60,000 characters. Response:

~~~json
{
  "structured_profile": {
    "id": "profile_1"
  }
}
~~~

The example response is abbreviated; the actual profile includes all fields defined by StudentProfile.

## POST /api/internship/extract

Content type: application/json

Request fields:
- title: required string, 1–200 characters.
- company: optional string, maximum 200 characters; defaults to an empty string.
- description: required string, 1–20,000 characters.
- source_url: optional string.

Example request:

~~~json
{
  "title": "Python Developer Intern",
  "company": "Example Organisation",
  "description": "Work mode: hybrid. Duration: 3 months. Required skills: Python, FastAPI. Eligibility: MCA or B.Tech.",
  "source_url": "https://example.org/internship"
}
~~~

Example response shape:

~~~json
{
  "internship": {
    "id": "0",
    "title": "Python Developer Intern",
    "company": "Example Organisation",
    "work_mode": "hybrid",
    "duration_months": 3,
    "required_skills": ["python", "fastapi"],
    "preferred_skills": [],
    "eligibility_conditions": []
  }
}
~~~

The response above is illustrative and abbreviated. Exact extracted values depend on the description and parser patterns.

## POST /api/match

This endpoint supports two request forms.

### Structured request (recommended)

~~~json
{
  "profile": {
    "id": "student_1",
    "education": [],
    "skills": [],
    "projects": [],
    "experience": [],
    "certifications": [],
    "coursework": [],
    "preferences": {
      "preferred_work_modes": ["remote", "hybrid", "on-site"],
      "preferred_locations": [],
      "willing_to_relocate": false,
      "available_hours_per_week": 20,
      "preferred_duration_months": 3,
      "minimum_stipend": null,
      "stipend_currency": "USD",
      "stipend_period": "monthly",
      "unpaid_acceptable": false
    },
    "raw_text": ""
  },
  "internships": [
    {
      "id": "role_1",
      "title": "Python Developer Intern",
      "company": "Example Organisation",
      "description": "MCA students. Required skills: Python, FastAPI.",
      "domain": "",
      "responsibilities": [],
      "work_mode": "remote",
      "location": "",
      "duration_months": 3,
      "start_date": null,
      "end_date": null,
      "weekly_hours": 20,
      "stipend_amount": 10000,
      "stipend_currency": "INR",
      "stipend_period": "monthly",
      "stipend_disclosed": true,
      "is_unpaid": false,
      "application_deadline": null,
      "eligibility_conditions": [],
      "required_skills": ["python", "fastapi"],
      "preferred_skills": [],
      "tools_and_tech": [],
      "has_contradictions": false,
      "contradiction_details": []
    }
  ]
}
~~~

The profile and internship objects must conform to StudentProfile and InternshipDetail. The endpoint accepts between 1 and 20 internship objects. Pydantic defaults and optional fields are defined in api/models.py.

The response is a MatchResponse containing the profile, sorted matches, and scoring weights. Each match contains eligibility, fit score, skill matches, practical fit, risk indicators, gap report, and the parsed internship detail.

### Legacy request form

The endpoint also accepts:

~~~json
{
  "resume_text": "Resume text...",
  "internships": [
    {
      "title": "Python Developer Intern",
      "company": "Example Organisation",
      "description": "MCA students; Python required."
    }
  ]
}
~~~

The legacy path runs the legacy matcher and also returns a structured response. New integrations should use the structured request so profile and posting corrections can be supplied explicitly.

## POST /api/reanalyze

Content type: application/json

Accepts the same structured body as /api/match. It runs the structured orchestrator again and returns a MatchResponse. This endpoint is used after a student changes profile or skill information.

## Validation and errors

FastAPI/Pydantic validation errors use standard HTTP validation responses. The application also returns explicit errors for unsupported resume extensions, oversized uploads, invalid document data, text exceeding limits, and unreadable documents.

Common status codes include:
- 400: malformed or unreadable document input.
- 413: uploaded resume exceeds the file-size limit.
- 415: unsupported resume extension.
- 422: invalid request fields, unsupported document content, page limit, or text-length limit.
- 500: unexpected server failure or matching failure.

Unexpected exceptions are logged server-side and returned with a generic message. Do not expose stack traces or private resume content to end users.

## Frontend client behaviour

The frontend client is in src/lib/api.ts. It:
- Uses relative /api paths unless VITE_API_BASE_URL is set.
- Applies a 30-second request timeout.
- Forwards AbortSignal cancellation from workspace operations.
- Converts API error bodies into user-facing messages.

## Versioning note

The FastAPI app currently declares version 0.2.0. There is no separately documented public API compatibility policy yet. Check api/main.py and the OpenAPI schema before depending on a field or behaviour.
