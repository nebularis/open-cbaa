# Instructions for Copilot

## Agentic Development Contract

This governs how implemented code is validated. It exists to conserve tokens and keep the human in control of what runs.

The general approach is that we work iteratively together, with the agent suggesting what we should build next, and the human verifying the approach along the way.

At all times, the following files MUST be kept up to date with changes:

- the root directory `README.md` (any new structure/folders/projects must be documented here)
- any project-level `README.md` files (significant changes must be documented appropriately)

### Pause For Architectural Guidance

DO NOT make design decisions unilaterally without consulting your user for architectural guidance.

### Architecture Principles

These govern all work in this repository. The [design specification](../docs/design/design-spec.md#1-architecture-principles) is authoritative if the two ever differ.

1. The ontological design is completed before a reference implementation is attempted. This repository holds semantic specifications and the tools used to produce and check them (`tools/`). It holds no implementation of the reference architecture.
2. The ontological layers stand on their own. Software built on them is governed by their architecture and design, not the reverse.
3. The reference architecture is technology-neutral until further notice.
4. Clauses have meaning attached to them. How that meaning is produced is open, and its governance and assurance are outside this repository's scope.

### Repository Topology

- `prompts/` contains reusable prompts and prompt templates 
- `ontology/` owns semantic assets only: normative ontology sources, shapes, vocabularies, projections, semantic examples, semantic fixtures, and semantic documentation.
- `reference/` contains reference documents, data, and notes to help you with your work
- `tools/` contains tools that produce or check the specifications, such as source extraction. It holds no reference implementation

You MAY write your own notes and memories to `reference` to help you with your work.

### Changing an ontology

[ontology/README.md](../ontology/README.md) describes how the documents fit together. When you change one:

- bump its `owl:versionIRI` under LATTICE's policy (ADR-A86): spec, vocab and each scheme independently, and a shapes directory's `.version` file instead of the spec, then update every `owl:imports` of the old version IRI
- regenerate the catalog with `tools/lattice_catalog.py`
- ask the user to run `tools/ontology_check.py` and LATTICE's `ontology_version_check.py` (commands in the ontology README §10)
- record design decisions once, in the ontology README, and propose them in the design specification's decision log

## General Guidelines

- Do not use semi-colons in English text. Use periods or commas instead.
- Be concise, do not repeat yourself. Avoid unnecessary verbosity.
- Avoid over-explaining. Say things once and cross-reference if really needed.
- Avoid superlatives.

### Documenting DL/OWL/TTL Ontologies

Try not to explain your design decisions in multiple places. Avoid explaining why you did not use a certain pattern or construct, especially if you've just explained why you did use a different one. If you feel the need to explain your design decisions, do so in a single place and cross-reference it from other places.

### Thinking / Reasoning for Coding and Design activities

Your user may present design collateral, architectural guidance, and coding standards. These must be adhered to at all times. Readability and clarity of intent is as important as working code that passes tests.

Always consider the architectural quanta of the code you are writing and carefully consider whether your code might implicitly or explicitly change the dependencies within the codebase. If in chat mode (as opposed to agentic / co-work), prefer to clarify impacts with your user before making them.

### Thinking / Reasoning for Writing

Your primary mode of operation should be critical thinking - looking for logical consistency and challenging logical errors, gaps, or misunderstandings.

You should consider whether to present your own arguments as hypotheses or determined facts, generally adopting a stance of curiosity rather than dogmatism. This must be balanced against the need to maintain a clear and concise writing style (see below).

### Writing Style / Voice 

Regardless of the style your user has requested (formal, informal, etc), try to be concise and avoid unnecessary verbosity. Where your user has requested that you provide output that is "comprehensive" and "detailed", this refers to the depth of subject matter understanding and analysis required, not the number of words used.

### What To Avoid

The following MUST be avoided if at all possible, breaking these rules only under exceptional circumstances.

- Do not use semi-colons in English text. Use periods or commas instead.
- Be concise, do not repeat yourself. Avoid unnecessary verbosity.
- Avoid over-explaining. Say things once and cross-reference if really needed.
- Avoid superlative adjectives. These must be reserved for factual extremes (e.g., "the tallest building") and are banned from use for emphasis (e.g., "the best solution," "the ultimate guide"). 
- Try to avoid "It's not X, it's Y" binary reframes, replace them with direct statements. 
- Avoid formulaic transitions such as "Furthermore," "Moreover," "Additionally," and "In conclusion" at the start of sentences. 
- Avoid vague meta-commentary like "It is important to note that," "In today's digital age," and "This serves as a testament to." Keep it short and succinct.

### What To Reduce

The following styles should be kept to a minimum.

- Rhetorical questions that are followed immediately by an answer. In general, do not pose rhetorical questions and, if you choose to, do not give their answer (as doing so ruins the rhetoric)
- Emphasis via short sentences, e.g., "Short sentences. For Emphasis. Often in threes."
- Excessive use of metaphores, e.g., "A symphony of the unnecessary tapestry of metaphores".
