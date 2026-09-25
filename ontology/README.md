# LMA Wordings Information Model — OWL 2 Ontology

Structural ontology for the LMA Wordings Information Model (WIM), derived from
[reference/lma-wordings-information-model.md](../reference/lma-wordings-information-model.md).
This is the first stratum: the Object Class Hierarchy, its Typing/Sub-Typing, and the
part-whole relation between them. The [design review](#design-review-cbaa-modules-m1m14)
below assesses it against the CBAA module drafts (M1–M14) and proposes further strata. The
[design specification](design/design-spec.md) turns that review into a concrete design, with
the agreed architecture principles and a decision log, and the
[LATTICE integration specification](design/lattice-integration.md) covers how LATTICE is
brought in and the description logic encoding. Neither is implemented yet. The
[LATTICE design review](design/design-review.md) records the challenge to depending on LATTICE
and its outcome.

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
base: `https://nebularis.github.io/open-cbaa/ontology/lma-wim`.

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

## Design review (CBAA modules M1–M14)

Evidence, with clause references, is in
[reference/cbaa-spec-observations.md](../reference/cbaa-spec-observations.md). Lattice was
consulted for comparison only. M7 (Evidence of Policies Bound), M11 (Management of Monies)
and M15 (Definitions) are not yet available. Other modules reference M7 and M11 often, so
the review assumes M7 governs policy documents and M11 monetary flows and settlement, and
treats both as unverified.

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

- The WIM structure holds across M1–M14. Nested component groups (CG09.1–CG09.3 inside
  CG09), conditional components and sub-components all fit the `comprises` restrictions, and
  no module needs a component to contain a component group.
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
| Inclusion modes (mandatory, variation slot, optional, conditional) at every level from component group to inline text, with conditions and slot-to-slot dependencies | all modules | absent |
| Governing variables as the vocabulary of conditions (GOV 3, 4, 7/8, 20/21, 79–81), some sourced from questions to the Contract Creator | M4, M5, M9 | `GoverningVariable` class only |
| Variable declarations: stable id, agreement-wide scope shared across modules, value space, population method, derived defaults, min/max and cross-variable constraints, composite and multi-valued types | endnotes, all modules | absent |
| Wording matrices keyed by governing variables (territory × authority level) and jurisdiction-scoped defined terms | M9 table | absent |
| Referenced objects: Table Objects, Document Objects (annexes, not digitised), module and component cross-references, external instruments incorporated with options (EU SCC) | cbaa.md, M13, all modules | placeholder classes |
| Guidance Objects as one family (Defined Terms, Technical, System) | cbaa.md | three unrelated classes |
| Ordered inline composition of text objects, dynamic numbering, object ids `CGnn`/`Cnn.X`/`SCnn.X.Y` | M5, M6, M8, M9, M10 | absent |
| Table templates: rows with optionality and rendering fragments, segments or arrangements as columns, derived tables (policy data specification) | M5, M10 | Dynamic/Static only |
| Activities as a shared vocabulary (quote, bind, extend, cancel and replace, FNOL, complaints, redress, reporting, sub-delegation) | M4, M8, M9, M10, M12, M14 | absent |
| Authority grants per activity with level, scope (segment, territory, trading location) and limits | M5, M8, M9, M14 | absent |
| Parties and roles, including natural persons, assigned per segment, data stream, territory or activity (Coverholder, Lead/Follow Insurer by platform, Broker, claims, reporting, data protection roles) | M1, M3, M4, M8, M10, M13, tables | absent |
| Agreement Segment as the unit of authority, remuneration, claims and reporting arrangements | M5, M6, M8, M10 | absent |
| Controlled vocabularies (territory to city, regulatory territory groupings, insurable interest, perils, claims basis, level of authority, data items), CDR and v5.2 aligned | M5, M9, M10 | absent |
| Quantities: money with ISO currency, durations with business or calendar basis, percentages of a base, recurrence | M3, M6, M8, M10, M12, M13 | absent |
| Jurisdiction tags and regulatory sources (Crystal+, PBQA, bulletins, LMA wordings) on clauses | M4, M5, M10 | absent |
| Identity criteria: new Coverholder entity, Lead Insurer or broker number means a new Agreement | M3 3.2.1, M12 12.17.1 | absent |
| Versions, acceptance events, agreed, effective and operational dates | M2, M3 | absent |
| Lifecycle states with state-specific authority, event, power, timer and notice transitions | M12 | absent |
| Obligations, prohibitions, permissions and powers with bearer, trigger, deadline, recurrence and survival | all modules | absent |
| Precedence rules between the Agreement, annexes, laws and versions | M1, M3, M12, M13 | absent |
| Registers and data specifications with required fields | M9, M10 | absent |

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

### Wording and meaning

M9–M14 show many wording variants that express the same norm with a different scope
reference (M9 9.2.8A and B differ only in whether authority is agreement-wide or territory
specific, M10 10.4A and B only in single vs multiple reporting arrangements). The library
should therefore keep wording (text objects, variants, variables) separate from meaning
(definitions, authority grants, obligations, permissions, powers), linked by an `expresses`
relation. Wording is what the renderer produces and what drafters govern. Meaning is what
criteria and behaviour evaluate. Several variants can express one norm, and a norm can be
checked for conflicts regardless of how it is worded (the drafters already flag conflicts,
e.g. M14 14.19 vs 14.23.1).

Most meaning is organised around activities. The same activity vocabulary is referenced by:

- authority grants: activity, level, scope and limits (M5 underwriting, M8 claims, M9
  complaints with redress limits, M14 sub-delegation)
- responsibilities assigned to named people (M4 table)
- role assignments per segment or data stream (M10)
- lifecycle-state overlays, where each M12 state lists what the Coverholder has or has no
  authority to do

The effective authority at a point in time is the grants for the activity, restricted by the
current lifecycle state, and extended by any special acceptances.

### Proposed strata

The design specification refines this table: meaning as attached statements
([§3](design/design-spec.md#3-what-a-clause-expresses)), vocabulary tiers and scoped binding
([§4](design/design-spec.md#4-vocabulary)), and quantification taken from LATTICE
([§5](design/design-spec.md#5-quantification-evaluation-of-lattice)).

| Stratum | Content | Profile and mechanism |
|---|---|---|
| foundation | persistent identity vs version, provenance, bitemporal scope, governance state | OWL 2 DL, SHACL, PROV-O alignment |
| quantification | money with ISO currency, durations with business or calendar basis, business calendars by jurisdiction, percentages of a base, recurrence | OWL 2 DL and SHACL, arithmetic in compiled rules |
| vocabulary | territories and regulatory groupings, insurable interests, perils, bases, activities, levels of authority, data items (v5.2), CDR mappings | SKOS, with an optional OWL 2 EL projection for classification over large hierarchies |
| wim | this stratum | OWL 2 DL |
| library | wording: text object IR, inclusion modes at every level, variation slots and their dependencies, conditions over governing variables, Contract Creator questions, variable declarations, wording matrices, table templates, tags, regulatory sources, materiality designation, external instruments with options | OWL 2 DL and SHACL, conditions held as data |
| norms | meaning: jurisdiction-scoped definitions, authority grants, obligations, prohibitions, permissions and powers (bearer, counterparty, activity, scope, trigger, deadline, recurrence, survival), precedence rules | OWL 2 DL and SHACL |
| party | parties, natural persons, role assignments scoped by segment, territory, data stream or activity with validity periods, capacity participation, segments | OWL 2 DL and SHACL, role assignments reified |
| instance | agreement identity and versions, selections, bindings, amendments, acceptances | OWL 2 DL and SHACL |
| criteria | evaluation of authority grants for any activity, with lifecycle-state overlays and special acceptances, match strategies, three-valued outcomes (permitted, denied, undetermined, where undetermined maps to referral) | conditions as data compiled for runtime, DL at design time |
| behaviour | state spaces for agreement (M12), amendment, referral, FNOL and complaints lifecycles, with event, power, timer and notice transitions, deemed-receipt rules | declarations in OWL, compiled state machines, occurrences recorded as events |
| market mix-ins | Lloyd's (syndicates, year of account, annual transfer, LIC, Crystal+, v5.2 reporting), US surplus lines, Australian Code of Practice, others | modules adding axioms, shapes and conditions to market-neutral strata |
| projections | CDR and ACORD mappings, derived data specifications, reporting subsets, API schemas | generated |

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
- **Norm conflict checks.** With norms classified by bearer, activity and scope, an
  obligation and a prohibition over overlapping scopes are detectable before publication.
  The same classification finds duplicated provisions across modules (M1 1.19 and M14 14.4).

### State and executability

State spaces (agreement lifecycle, amendment approval, special acceptance, prior-submit
referral, FNOL and complaints handling) are declared in the T-Box as ground truth and
executed by compiled state machines in operational services. The A-Box records state
occupancy and transitions as bitemporal events for audit and market queries. It is not the
execution mechanism. This keeps reasoning off the request path and keeps the graph an
evidential record.

M12 confirms this split and adds three requirements:

- **State-dependent authority.** Each state carries its own authority overlay, so the state
  machine and the criteria evaluation must share the activity vocabulary.
- **Transitions from any party.** Transitions can be triggered by events concerning any
  party, including follow insurers and the broker, by powers a party chooses to exercise,
  and by timers measured in business or calendar days.
- **Guards over operational data.** Run-off ends only when every policy has expired and every
  claim is resolved, which is an aggregate over operational data. Guards of this kind are
  evaluated in the operational tier and reported to the state machine as events.

### Decisions

Decisions taken and still open are recorded in the design specification's
[decision log](design/design-spec.md#12-decision-log).

## Validation

No build pipeline yet. Modules are parsed with `rdflib`, merged with `owl:imports` removed
(the `nebularis.github.io` IRIs are not yet published), and classified with HermiT via
`owlready2`. Current result: valid OWL 2 DL, no unsatisfiable classes.

## Not yet modelled

Everything in [Alignment gaps](#alignment-gaps). LATTICE is to be imported per the
[integration specification](design/lattice-integration.md), whose §9 sets the order of work.
