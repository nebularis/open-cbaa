# Open CBAA

An open standards based exploration of Delegated (Binding) Authority, as realised for example, by the Lloyd's Market Association.

**The Material In This Repository Is For Educational Purposes Only**

Formerly Open DARE. Prompts written before the rename keep the old name.

## Evoling Ontology Using AI

Each commit to this repository is either a prompt (+ reference data) or an agentic response, updating artefacts in the repository. Each gen-ai commit will bear the model and (if used) tool-chain and other relevant information.

### Architecture Principles

The principles governing this repository and anything built on it are set out in the
[design specification](docs/design/design-spec.md#1-architecture-principles).

### Repository Structure

- `ontology/` — normative OWL 2 ontology sources and their [README](ontology/README.md)
- `docs/design/` — the [design specification](docs/design/design-spec.md), the [LATTICE integration specification](docs/design/lattice-integration.md), the [LATTICE design review](docs/design/design-review.md) and the [vision and demo ideation](docs/design/ideation.md)
- `docs/development/` — the working [plan](docs/development/plan.md)
- `docs/discovery/` — a single-page, dependency-free illustration of the [vision and demo ideation](docs/design/ideation.md), and [prototype architecture discovery notes](docs/discovery/poc-ideas.md)
- `reference/` — reference documents, data, and notes
- `prompts/` — reusable prompts and prompt templates
- `tools/` — tools that produce or check the specifications, e.g. the CBAA spec extractor, and their own [README](tools/README.md)
