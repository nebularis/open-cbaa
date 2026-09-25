# Open CBAA

An open standards based exploration of Delegated (Binding) Authority, as realised for example, by the Lloyd's Market Association.

**The Material In This Repository Is For Educational Purposes Only**

Formerly Open DARE. Prompts written before the rename keep the old name.

## Evoling Ontology Using AI

Each commit to this repository is either a prompt (+ reference data) or an agentic response, updating artefacts in the repository. Each gen-ai commit will bear the model and (if used) tool-chain and other relevant information.

### Architecture Principles

The principles governing this repository and anything built on it are set out in the
[design specification](ontology/design/design-spec.md#1-architecture-principles).

### Repository Structure

- `ontology/` — normative OWL 2 ontology sources, their [README](ontology/README.md), the [design specification](ontology/design/design-spec.md), the [LATTICE integration specification](ontology/design/lattice-integration.md) and the [LATTICE design review](ontology/design/design-review.md)
- `reference/` — reference documents, data, and notes
- `prompts/` — reusable prompts and prompt templates
- `tools/` — tools that produce or check the specifications, e.g. the CBAA spec extractor, and their own [README](tools/README.md)
