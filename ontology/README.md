# LMA Wordings Information Model — OWL 2 Ontology

Structural ontology for the LMA Wordings Information Model (WIM), derived from
[reference/lma-wordings-information-model.md](../reference/lma-wordings-information-model.md).
This is the first stratum: the Object Class Hierarchy, its Typing/Sub-Typing, and the
part-whole relation between them. The [design review](#design-review-cbaa-modules-m1m8)
below assesses it against the CBAA module drafts (M1–M8) and proposes further strata, which
are not yet implemented.

## Files

| File | Namespace | Contents |
|---|---|---|
| [core.ttl](core.ttl) | `.../lma-wim/core#` | Contract, Component Group, Component, Data Element, `comprises`/`directlyComprises`, `AgreementRelated`/`PolicyRelated` mixins, Typing leaves with no further Sub-Typing (Module, Endorsement/Complex Component, Schedule, Definition, System Guidance, Technical Guidance) |
| [agreement.ttl](agreement.ttl) | `.../lma-wim/agreement#` | Agreement, Binding Authority, Line Slip, Consortium, DCAA |
| [policy.ttl](policy.ttl) | `.../lma-wim/policy#` | Policy, Insurance, Reinsurance |
| [clause.ttl](clause.ttl) | `.../lma-wim/clause#` | Clause and its Sub-Typing (Scope of Authority/Coverage Clause, Contractual Provision), plus the document/analogue-for-now artifacts |
| [data-element.ttl](data-element.ttl) | `.../lma-wim/data-element#` | Text, Table, Variable, Metadata, Reference and their Sub-Typing |
| [lma-wim.ttl](lma-wim.ttl) | `.../lma-wim#` | Umbrella. Imports all of the above and adds the one cross-branch axiom (Agreement disjoint from Policy) |

The four branch modules import only `core.ttl` and are independent of each other. Namespace
base: `https://nebularis.github.io/open-dare/ontology/lma-wim`.

## OWL Profile

OWL 2 DL for this stratum. The `comprises` restrictions need `allValuesFrom`, which EL
forbids. Profiles for later strata are discussed under [Proposed strata](#proposed-strata).

## Modelling patterns

- **`comprises`** is transitive. `directlyComprises` is its asserted, simple (irreflexive,
  asymmetric) sub-property. Instance data asserts direct edges only, and skip-level
  containment (a Contract comprising a Data Element with no intervening Component Group) is
  entailed. Per-class `allValuesFrom` restrictions on `comprises` fix which levels each class
  may comprise (Component may comprise Component or Data Element, never Component Group).
  OWL 2 DL forbids irreflexivity and asymmetry on a transitive ("non-simple") property, so
  those characteristics sit on `directlyComprises`.
- **Typing and Sub-Typing** are both `rdfs:subClassOf` chains.
- **Legend colours** (Agreement-related, Policy-related, Both) are the `AgreementRelated` and
  `PolicyRelated` mixins. A mixin is asserted on the class the source colours, never on a
  parent whose sub-types differ. Clause is coloured "Both" because its sub-types span both,
  so the mixins sit on Scope of Authority Clause, Scope of Coverage Clause and Contractual
  Provision rather than on Clause.
- **`GrantsOfCoverage` and `Limitations`** are deliberately not disjoint. The source lists
  "Exclusion & Limited Writeback" and "Affirmation & Limited Exclusion" under both, so those
  leaves subclass both.
- **Document/analogue-for-now artifacts** carry `core:representationStatus "document"`. They
  correspond to the specs' Document Objects (see [alignment gaps](#alignment-gaps)).
- **`de:linksTo`** (Reference to Definition, internal object, external document or Table) is
  an object property, not a subtype relation.

## Design review (CBAA modules M1–M8)

Evidence, with clause references, is in
[reference/cbaa-spec-observations.md](../reference/cbaa-spec-observations.md). Lattice was
consulted for comparison only.

### Intended use

DARE's stated aims for the CBAA are continuous compliance checking, automated data sharing
and integration across market platforms. The behaviours a market-wide DA platform needs from
the model follow from that.

| Behaviour | When | Semantics required |
|---|---|---|
| Assemble and validate an instance: pick variations, include optional and conditional clauses from governing facts, bind variables, render | authoring | closed-world completeness, deterministic rendering |
| Check a quote, bind or bordereau row against authority | point of bind, and after the fact | hierarchy matching, numeric bounds, exclusion sets, portfolio aggregates, outcomes of permit, deny or refer |
| Govern amendments: materiality, required approvers by insurer role, agreed vs effective date | agreement lifecycle | version diffs, bitemporality, role-based approval |
| Monitor obligations: event-triggered deadlines, notifications, reporting | operations | events, business calendars, state |
| Oversee the market: which live agreements a regulatory change affects, which use a given clause version | portfolio | provenance, jurisdiction tags, version lineage |

"Executable" in this setting means the contract yields decisions, obligations with due dates,
and required approvals, which people and systems then act on. It does not mean
self-enforcing. M3 3.19.4 makes the electronic version the definitive record, so the rendered
wording is a projection of the model, and the renderer needs the governance of a compiler.

### What the current layer enables and prevents

- It supports consistency checking of part-whole typing, transitive containment queries,
  and a shared WIM terminology.
- Every class is primitive, so the reasoner infers little beyond what is asserted. DL pays
  off through defined classes that classify individuals by their properties, e.g. a
  subscription agreement as an Agreement with at least two participating insurers. Several
  inclusion conditions in the specs are classifications of this kind ("more than one
  insurer", "subscription market CBAA").
- Under the open-world assumption OWL cannot report a missing mandatory variable or an
  unselected variation. Completeness checks belong in SHACL.
- OWL cannot compare two data values, so "sum insured must not exceed this agreement's
  maximum limit" needs rules, generated code, or a per-agreement T-Box that fixes the limit
  as a datatype facet.
- Aggregates such as GWP income limits across all policies bound are outside DL.
- The ontology models WIM types as classes, which suits them. It has nothing yet for library
  objects (versioned, published clause templates in the WOL) or agreement instances. Those
  are individuals. Modelling each clause variation as a class would not scale, and would put
  governed, versioned content in the T-Box.
- This review found and fixed a mixin defect: Clause carried both mixins, so every clause
  sub-type inherited both.

### Alignment gaps

| Spec concept | Source | Current ontology |
|---|---|---|
| Inclusion modes (mandatory, variation slot, optional, conditional) with conditions | all modules | absent |
| Governing variables as the vocabulary of conditions (GOV 3, 4, 7/8, 20/21, 79–81) | M4, M5 | `GoverningVariable` class only |
| Variable declarations: stable id, value space, population method, reuse across clauses | endnotes, all modules | absent |
| Referenced objects: Table Objects, Document Objects (annexes, not digitised), module and component cross-references | cbaa.md, all modules | placeholder classes |
| Guidance Objects as one family (Defined Terms, Technical, System) | cbaa.md | three unrelated classes |
| Ordered inline composition of text objects, dynamic numbering, object ids `CGnn`/`Cnn.X`/`SCnn.X.Y` | M5, M6, M8 | absent |
| Table templates: rows with optionality and rendering fragments, Agreement Segments as columns | M5 base tables | Dynamic/Static only |
| Parties and roles (Coverholder, Lead/Follow Insurer by platform, Broker, Producing Intermediary, claims roles, Regulatory Body) | M1, M3, M4, M8, Insurer Capacity Table | absent |
| Agreement Segment as the unit of authority, remuneration and claims arrangements | M5, M6, M8 | absent |
| Controlled vocabularies (territory to city, insurable interest, perils, claims basis, level of authority), CDR-aligned | M5 tables | absent |
| Jurisdiction tags and regulatory sources (Crystal+, PBQA, bulletins) on clauses | M4, M5 | absent |
| Identity criteria: new Coverholder entity, Lead Insurer or broker number means a new Agreement | M3 3.2.1 | absent |
| Versions, acceptance events, agreed, effective and operational dates | M2, M3 | absent |
| Obligations, permissions, prohibitions with bearer, trigger and deadline | all modules | absent |

### Architectural and operational semantics

Architectural semantics serve market alignment: a terminological reference in OWL 2 DL and
SKOS, open-world, mapped to CDR and ACORD GRLC, changing slowly under DAWG and CBAA Steer
governance. Operational semantics serve systems acting on instances: closed-world
validation, rules, arithmetic, time, aggregates and state. The T-Box is the source from
which shapes, rule sets, state machines and API schemas are generated, not an engine
consulted at runtime.

Content falls into three tiers with different homes and governance.

| Tier | Examples | Home | Scale | Governance and provenance |
|---|---|---|---|---|
| Library | WOL objects, variations, conditions, variable declarations, table templates | A-Box of library strata, versioned and published | thousands | authoring status, legal review, publication, deprecation, regulatory source per object |
| Instance | a CBAA with its selections, bindings, parties, versions | A-Box in an instance store | tens of thousands | acceptance per version, approvals by role and materiality, bitemporal effective dating |
| Operation | quotes, policies bound, FNOLs, bordereaux, obligation occurrences | operational stores referencing instance version IRIs, plus an event record | millions | decision explanations: condition applied, facts used, source of each fact |

DL reasoning is worth its cost at the library and instance tiers. The operation tier needs
compiled evaluation.

If the primary aim were a compiler from wording to code, the library strata would become an
intermediate representation: ordered text nodes, variable and reference nodes, guard
expressions, with SHACL as the type checker. The WIM Data Element types already are that
node set, lacking order and inline composition. If the primary aim were a runtime graph, the
same T-Box would serve as schema, with inferences materialised on load and validation on
write, and no reasoner on the request path. The proposal below supports both by keeping
conditions and templates as data.

### Proposed strata

| Stratum | Content | Profile and mechanism |
|---|---|---|
| foundation | persistent identity vs version, provenance, bitemporal scope, governance state | OWL 2 DL, SHACL, PROV-O alignment |
| vocabulary | territories, insurable interests, perils, bases, levels of authority, CDR mappings | SKOS, with an optional OWL 2 EL projection for classification over large hierarchies |
| wim | this stratum | OWL 2 DL |
| library | text object IR, inclusion modes, variation slots, conditions over governing variables, variable declarations, table templates, tags, regulatory sources, materiality designation | OWL 2 DL and SHACL, conditions held as data |
| party | parties, roles, capacity participation, segments | OWL 2 DL and SHACL |
| instance | agreement identity and versions, selections, bindings, amendments, acceptances | OWL 2 DL and SHACL |
| criteria | authority envelopes per segment, match strategies, three-valued outcomes (permitted, denied, undetermined, where undetermined maps to referral) | conditions as data compiled for runtime, DL at design time |
| behaviour | obligations (bearer, counterparty, trigger, deadline), state spaces for agreement, amendment, referral and FNOL lifecycles | declarations in OWL, compiled state machines, occurrences recorded as events |
| market mix-ins | Lloyd's (syndicates, year of account, annual transfer, LIC, Crystal+), US surplus lines, others | modules adding axioms, shapes and conditions to market-neutral strata |
| projections | CDR and ACORD mappings, reporting subsets, API schemas | generated |

Mix-ins are needed because the CBAA is intended for company-only binders as well as Lloyd's.
Lloyd's-specific content (annual transfer, LIC provisions, Crystal+ checks) should import the
market-neutral strata rather than sit inside them.

On the earlier intent to use EL for criteria: authority envelopes need exclusions ("but
excluding" sub-divisions, excluded perils) and numeric bounds, and EL supports neither. EL
suits the vocabulary hierarchies, where classification at scale matters. Criteria are better
held as data and compiled.

DL reasoning has design-time uses that procedural code handles poorly:

- **Materiality by subsumption.** Compile the authority envelopes of versions N and N+1 into
  defined classes. If the new envelope is not subsumed by the old one, authority has
  expanded, which M3 3.9.1 treats as material (additional territories or insurable interests,
  higher limits). Required approvers then follow from insurer amendment roles.
- **Envelope checks.** An unsatisfiable segment authorises nothing. Overlapping segments with
  different remuneration are detectable.
- **Condition checks.** The conditions of a variation slot should be pairwise disjoint and
  jointly exhaustive over the governing variables' value spaces, which is a satisfiability
  question.

### State and executability

State spaces (agreement lifecycle, amendment approval, special acceptance, prior-submit
referral, FNOL handling) are declared in the T-Box as ground truth and executed by compiled
state machines in operational services. The A-Box records state occupancy and transitions as
bitemporal events for audit and market queries. It is not the execution mechanism. This
keeps reasoning off the request path and keeps the graph an evidential record.

### Decisions needed before implementation

1. Next increment: library and party strata first (they unblock authoring and conditions),
   or foundation first.
2. Criteria: conditions as data evaluated by an engine, per-agreement T-Box compilation, or
   both (data for runtime, compiled classes for design-time checks as proposed above).
3. Vocabularies: SKOS concept schemes or OWL class hierarchies, and which CDR release is
   the source of truth.
4. Ordering of text nodes: `rdf:List` or an explicit sequence index.
5. External alignment: PROV-O and OWL-Time, or minimal local terms (Lattice aligns with
   PROV-O and declines OWL-Time).

## Validation

No build pipeline yet. Modules are parsed with `rdflib`, merged with `owl:imports` removed
(the `nebularis.github.io` IRIs are not yet published), and classified with HermiT via
`owlready2`. Current result: valid OWL 2 DL, no unsatisfiable classes.

## Not yet modelled

Everything in [Alignment gaps](#alignment-gaps). Lattice remains a reference only.
