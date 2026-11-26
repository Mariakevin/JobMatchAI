# JobMatch AI documentation

JobMatch AI is a student-side internship decision-support application. It analyses a resume against internship descriptions and returns explicit eligibility evaluations, evidence-backed skill matches, practical-fit details, listing-risk indicators, and a traceable profile-fit score.

## Choose a guide

| I want to… | Read |
|---|---|
| Understand the problem, goals, scope, and requirements | [Project overview](project-overview.md) |
| Install and run the application locally | [Getting started](getting-started.md) |
| Use the application from the browser | [User guide](user-guide.md) |
| Understand the application architecture and data flow | [Architecture](architecture.md) |
| Understand eligibility, evidence, scoring, and warnings | [Decision model](decision-model.md) |
| Integrate with the backend API | [API reference](api-reference.md) |
| Run tests and understand security boundaries | [Testing and security](testing-security.md) |
| Navigate the source tree and contribute changes | [Development guide](development.md) |
| Review documentation conventions and external references | [References](references.md) |

## Documentation principles

This documentation separates four reader needs: a guided setup, task-oriented instructions, technical reference, and conceptual explanation. That organisation follows the [Diátaxis framework](https://diataxis.fr/) and GitHub's guidance to write for a defined audience, use meaningful headings, and keep content scannable.

The supplied academic project reports were used as structural references for the project overview: problem definition, objectives, scope, system analysis, requirements, architecture, implementation, testing, limitations, and conclusion. Those report sections are adapted here into maintainable software documentation rather than copied as a single long report.

## Important product boundary

JobMatch AI is a decision-support tool, not a hiring system. It does not predict acceptance probability, guarantee selection, verify an employer's identity, or make applications on a student's behalf. Extracted facts and heuristic warnings must be checked against the original posting and confirmed with the employer.

For implementation details, the source code is authoritative. Where a feature is not implemented, the documentation identifies it as a limitation or future work rather than describing it as an existing capability.
