# LMA Wordings Information Model — OWL 2 Ontology

Initial structural ontology for the LMA Wordings Information Model (WIM), derived from
[reference/lma-wordings-information-model.md](../reference/lma-wordings-information-model.md).
This is the first stratum: the Object Class Hierarchy, its Typing/Sub-Typing, and the
part-whole relation between them. It does not yet model the executable coverage/criteria
semantics (limits, exclusions, conditions as evaluable logic) — that is a later stratum,
per the note in [lma-wim.ttl](lma-wim.ttl).

## Files

| File | Ontology IRI (namespace + `#`) | Contents |
|---|---|---|
| [core.ttl](core.ttl) | `.../lma-wim/core#` | Contract, Component Group, Component, Data Element; `comprises`/`directlyComprises`; `AgreementRelated`/`PolicyRelated` mixins; Typing leaves with no further Sub-Typing (Module, Endorsement/Complex Component, Schedule, Definition, System Guidance, Technical Guidance) |
| [agreement.ttl](agreement.ttl) | `.../lma-wim/agreement#` | Agreement, Binding Authority, Line Slip, Consortium, DCAA |
| [policy.ttl](policy.ttl) | `.../lma-wim/policy#` | Policy, Insurance, Reinsurance |
| [clause.ttl](clause.ttl) | `.../lma-wim/clause#` | Clause and its full Sub-Typing tree (Scope of Authority/Coverage Clause, Contractual Provision), plus the document/analogue-for-now artifacts |
| [data-element.ttl](data-element.ttl) | `.../lma-wim/data-element#` | Text, Table, Variable, Metadata, Reference and their Sub-Typing |
| [lma-wim.ttl](lma-wim.ttl) | `.../lma-wim#` | Umbrella: imports all of the above, adds the one cross-branch axiom (Agreement disjoint from Policy) |

`agreement.ttl`, `policy.ttl`, `clause.ttl`, and `data-element.ttl` each import only `core.ttl`
and are independent of each other, so any one branch can be extended without touching the
others. Namespace base: `https://nebularis.github.io/open-dare/ontology/lma-wim` (a GitHub
Pages URL tied to this repo, chosen over a placeholder domain or a `w3id.org` redirect).

## OWL Profile

OWL 2 DL, not a tractable profile (EL/RL/QL), for this stratum. The `comprises` restrictions
need `allValuesFrom` (universal restrictions), which EL forbids, and the domain has real
disjointness/negation needs (e.g. exclusions) that a tractable profile would fight rather
than express. Later strata — e.g. a "criteria" stratum modelling coverage/limit evaluation —
may target OWL 2 EL where tractable classification matters more than expressivity, and should
sit alongside this ontology (importing it) rather than inside it.

## Modeling patterns

- **`comprises`** is transitive; `directlyComprises` is its asserted, simple (irreflexive,
  asymmetric) sub-property. Only direct edges should be asserted in instance data — the
  diagram's skip-level containment (e.g. Contract comprising a Data Element with no
  intervening Component Group) is entailed by transitivity, not asserted. Per-class
  `allValuesFrom` restrictions on `comprises` encode exactly which levels each class may
  comprise (e.g. Component may comprise Component or Data Element, never Component Group).
  OWL 2 DL forbids declaring a transitive ("non-simple") property irreflexive/asymmetric
  directly, which is why those characteristics live on `directlyComprises` instead.
- **Typing and Sub-Typing** (the diagram's dashed "is a subtype of" arrows, and even the
  plain column-adjacency like Contract–Agreement) are both `rdfs:subClassOf` chains. There
  is no separate relation for "Typing" versus "Sub-Typing" in this ontology.
- **Cross-cutting colour-coding** (Agreement-related / Policy-related / Both) is modelled as
  the `AgreementRelated`/`PolicyRelated` mixins in `core.ttl`; a "Both"-coloured class
  (e.g. `Clause`, `Schedule`) multiply-inherits from both rather than duplicating structure.
- **`GrantsOfCoverage` and `Limitations`** (in `clause.ttl`) are deliberately not disjoint:
  the source diagram lists "Exclusion & Limited Writeback" and "Affirmation & Limited
  Exclusion" under both groupings, so their leaf classes are subclasses of both. Verified
  satisfiable — see Validation below.
- **Document/analogue-for-now artifacts** (Schedule document, Contract Jacket, Certificate
  of Insurance, IPID, List of Benefits, Notice, Assessment) carry the `core:representationStatus
  "document"` annotation rather than a distinct class hierarchy, since the distinction is a
  lifecycle/implementation status, not a taxonomic kind. They are not asserted as subtypes of
  Contractual Provision despite being drawn adjacent to it in the source, pending clarification
  of the intended link.
- **`Reference`'s "links to"** (`de:linksTo`, targeting Definition / an internal object / an
  external document / Table) is an object property, not a subtype relation — distinct from
  every other dashed arrow in the source diagram.

## Validation

No formal build pipeline yet. Files are checked by parsing with `rdflib` and classifying with
the HermiT reasoner (via `owlready2`, which bundles it) — merge the modules into one graph,
strip `owl:imports` (they'd otherwise try to fetch these `nebularis.github.io` IRIs over the
network), and run `sync_reasoner_hermit`. Confirms: valid OWL 2 DL, no unsatisfiable classes,
and specifically that `AffirmationAndLimitedExclusion`/`ExclusionAndLimitedWriteback` remain
satisfiable under the shared-grouping pattern above.

## Not yet modelled

- Executable coverage/criteria semantics (limits, exclusions, conditions as evaluable logic)
- Instance-level data (actual contracts, modules, clauses)
- Any relationship to [Lattice](https://github.com/nebularis/lattice) — reference only for now
