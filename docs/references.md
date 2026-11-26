# References and documentation methodology

## 1. Supplied project-report references

The project overview and academic structure were informed by the two reports supplied for this task:

1. **REPORT READER AI – Medical Report Explanation Assistant** (16 pages). Its structure was used as a reference for the abstract, introduction, existing-system limitations, proposed-system features, system analysis, feasibility, requirements, architecture, module descriptions, testing, test cases, and conclusion.
2. **STOCKQUERY AI: Predictive Inventory Intelligence – Value Added Course Project Report** (15 pages). Its more compact MCA project-report organisation informed the numbered chapter structure, contents/navigation, abbreviations and terminology, problem definition, objectives, scope, system environment, literature study, use-case perspective, architecture, structural and behavioural design, code design, test report, implementation, conclusion, and references.

The reports describe different applications. Their medical-report OCR pipeline and predictive inventory algorithms are not components of JobMatch AI and have not been presented as such. Their document organisation and explanatory patterns were adapted to JobMatch AI's actual codebase.

## 2. External documentation guidance

The technical documentation is organised using the four documentation needs described by Diátaxis: tutorials, how-to guides, reference, and explanation. These are distinct reader goals, so installation, task instructions, conceptual explanations, and API details are separated rather than combined into one long page.

- [Diátaxis — A systematic approach to technical documentation](https://diataxis.fr/). Primary structure used for the documentation set.
- [GitHub Docs — About README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes). Guidance on the README as the first entry point for what a project does, why it is useful, how to start, where to get help, and who maintains it.
- [GitHub Docs — Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories). Repository-level discoverability and security guidance.
- [FastAPI — Features](https://fastapi.tiangolo.com/features/). OpenAPI-based API descriptions and interactive documentation.
- [W3C — Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/). Accessibility reference for web content.

## 3. Method used to document JobMatch AI

The repository's default branch was inspected, including its README, requirements, package metadata, backend modules, frontend types and components, Vite configuration, design research, and automated test files. Feature descriptions and API contracts were written from those source files.

The following rules were applied:

- Source code is authoritative over aspirational or stale README wording.
- A feature is described as implemented only when repository code supports the claim.
- Unimplemented features are identified as limitations or future work.
- Example payloads are labelled illustrative when shortened.
- Numeric scoring and eligibility behaviour are described separately.
- Heuristic outputs are described with their uncertainty and limitations.

## 4. Maintenance

Review the documentation whenever a route, Pydantic model, TypeScript type, parser rule, score weight, eligibility state, upload limit, or runtime dependency changes. Do not let code examples or test counts drift from the repository.
