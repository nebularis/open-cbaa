# Open CBAA

An open standards based exploration of Delegated (Binding) Authority, as realised for example, by the Lloyd's Market Association.

**The Material In This Repository Is For Educational Purposes Only**

### Architecture Principles

The principles governing this repository and anything built on it are set out in the
[design specification](docs/design/design-spec.md#1-architecture-principles).

### Repository Structure

- `ontology/` — the OWL 2 ontologies (`wim`, `statement`, `agreement`, `risk`, each with `spec/`, `vocab/` and `shapes/`), provisional `schemes/`, `governance/` shapes, a worked `examples/` agreement, the `open-cbaa.ttl` umbrella, their [README](ontology/README.md), and `catalog-v001.xml`, which Protégé reads to resolve imports, LATTICE's included, without a LATTICE checkout
- `docs/design/` — the [design specification](docs/design/design-spec.md), the [LATTICE integration specification](docs/design/lattice-integration.md), the [LATTICE design review](docs/design/design-review.md), the [WIM design review](docs/design/wim-review.md) and the [vision and demo ideation](docs/design/ideation.md)
- `docs/architecture.md` — a narrative [walkthrough](docs/architecture.md) of how the ontologies, compilation and runtime fit together
- `docs/development/` — the working [plan](docs/development/plan.md)
- `docs/discovery/` — a single-page, dependency-free illustration of the [vision and demo ideation](docs/design/ideation.md), and [prototype architecture discovery notes](docs/discovery/poc-ideas.md)
- `reference/` — reference documents, data, and notes
- `tools/` — tools that produce or check the specifications: the catalog generator, the ontology check and the CBAA spec extractor, with their own [README](tools/README.md)
