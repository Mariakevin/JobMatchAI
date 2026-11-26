# Development guide

## Repository layout

~~~text
JobMatchAI/
├── api/
│   ├── main.py
│   ├── models.py
│   ├── resume_parser.py
│   ├── internship_parser.py
│   ├── taxonomy.py
│   ├── eligibility_engine.py
│   ├── skill_matcher.py
│   ├── fit_scorer.py
│   ├── orchestrator.py
│   └── matcher.py
├── docs/
├── src/
│   ├── components/
│   │   ├── internships/
│   │   ├── layout/
│   │   ├── profile/
│   │   ├── results/
│   │   └── ui/
│   ├── hooks/
│   ├── lib/
│   ├── styles/
│   ├── App.tsx
│   ├── main.tsx
│   └── types.ts
├── tests/
├── index.html
├── package.json
├── package-lock.json
├── requirements.txt
├── vite.config.ts
└── README.md
~~~

## Local development

Start the backend and frontend in separate terminals. Follow [Getting started](getting-started.md) for the complete environment setup.

Backend:

~~~bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
~~~

Frontend:

~~~bash
npm run dev
~~~

## Change workflow

1. Create a focused branch for the change.
2. Identify the owning module before changing behaviour.
3. Update Pydantic models and TypeScript types together when API contracts change.
4. Update the parser or decision engine and add targeted tests.
5. Run the Python test suite and frontend production build.
6. Review the user-facing wording, validation states, and unknown/error cases.
7. Update the relevant documentation page and README navigation.
8. Open a pull request describing the behaviour change, test evidence, and any known limitations.

## Coding boundaries

- Keep extraction distinct from evaluation. Parsers produce structured candidate facts; deterministic engines evaluate them.
- Preserve original excerpts and reasons when producing auditable outputs.
- Do not treat missing resume evidence as a confirmed skill gap without student confirmation.
- Keep eligibility independent from the profile-fit score.
- Never describe a profile-fit score as hiring or selection probability.
- Do not interpret listing warnings as proof of fraud.
- Avoid adding network calls or third-party AI dependencies without documenting data flow, privacy, failure handling, and configuration.
- Keep frontend API types aligned with backend Pydantic models.
- Preserve cancellation and request sequencing in the workspace hook.

## Documentation changes

Documentation is organised by reader need:

- Getting started: installation and first local run.
- User guide: accomplishing tasks in the application.
- Explanation: project overview, architecture, and decision model.
- Reference: API contracts, module responsibilities, and configuration.
- Maintenance: testing, security, and contribution workflow.

Keep examples runnable, mark abbreviated JSON as illustrative, and distinguish implemented behaviour from intended or planned behaviour.

## Pull request checklist

- [ ] The change has a focused scope and clear description.
- [ ] Tests cover expected behaviour and important edge cases.
- [ ] Python tests pass.
- [ ] Frontend build passes.
- [ ] API schema and TypeScript types are consistent.
- [ ] User-facing errors and accessibility states are understandable.
- [ ] Documentation and README navigation are updated.
- [ ] No secrets, personal resume data, or generated local files were committed.
