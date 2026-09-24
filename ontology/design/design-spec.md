# Open DARE Semantic Design Specification

Version 0.1, draft for review. Nothing here has been applied to the `*.ttl` files yet. Section
[12](#12-decision-log) records what is decided and what is open.

Inputs: the CBAA module drafts M1–M14 (evidence in
[reference/cbaa-spec-observations.md](../../reference/cbaa-spec-observations.md)), the
[design review](../README.md#design-review-cbaa-modules-m1m14), the MERIDIAN CSO, FBO and
unified architecture documents, the SPC description logic encoding and its reference
architecture, and the LATTICE Foundation, Vocabulary, Quantification and Instrument layers and
RDF/SPARQL Operational Patterns Guide (commit `558650b`).

---

## 1. Architecture Principles

As agreed. Numbering is normalised (the brief numbered two principles "2").

| # | Principle |
|---|---|
| AP1 | The ontological design is completed before a reference implementation is attempted. This repository holds semantic specifications and the tools used to produce and check them (`tools/`). It holds no implementation of the reference architecture. |
| AP2 | The ontological layers stand on their own. Software built on them is governed by their architecture and design, not the reverse. |
| AP3 | The reference architecture is technology-neutral until further notice. |
| AP4 | Clauses have meaning attached to them. How that meaning is produced (a controlled natural language such as InsurLE, LLM extraction with human validation, manual encoding) is open, and its governance and assurance are outside this repository's scope. |

## 2. Design Principles

Derived from the principles above and from the reviewed sources. Each is stated once here and
referenced elsewhere by number.

| # | Principle | Source |
|---|---|---|
| DP1 | **Thin T-Box, governed A-Box vocabulary.** Data that changes often, or differs by user, market, tenant or use case, lives in the A-Box as SKOS, not in class hierarchies. | brief, MERIDIAN DP-4 |
| DP2 | **Class or concept.** Introduce an OWL class when instances need different properties, axioms or shapes. Use a SKOS concept when instances differ only in how they are classified. | this spec |
| DP3 | **Wording and meaning are separate strata**, joined by an `expresses` attachment (§3). | AP4, design review |
| DP4 | **Intrinsic on nodes, relational on edges.** A parameter understandable from one construct belongs on it. A parameter needing two belongs on an edge. | MERIDIAN DP-5 |
| DP5 | **Compile, do not interpret, on hot paths.** Runtime artefacts (hierarchy closures, authority envelopes, state tables, shapes) are derived deterministically, reproducible from pinned inputs, and traceable to their sources. Detail needed for regulation stays in the source planes and is elided from runtime projections. | MERIDIAN §8, SPC, brief |
| DP6 | **State never enters structural comparison.** Lifecycle state may gate evaluation. It must not take part in comparing authority envelopes, detecting materiality or detecting gaps. | MERIDIAN §6.5 |
| DP7 | **Open world for terminology, closed world for transitions.** Reasoning over vocabulary and structure is open-world. Validation and state transitions operate on a closed snapshot. | SPC |
| DP8 | **Every concept-valued property names a scheme contract.** A range of plain `skos:Concept` is a defect. | MERIDIAN FBO §6.4.1 |
| DP9 | **Use an `Any` concept, never the empty set**, for an unconstrained dimension. | MERIDIAN §6.6 |
| DP10 | **Identity is not position.** Clause numbers are display, derived after inclusion is resolved. Object identity is the WIM object id (`Cnn.X`) and its version. | CBAA "numbering for reference only" |

## 3. What a Clause Expresses

### 3.1 The choice

Three ways to make a clause's meaning machine-readable:

| Option | Shape | Consequence |
|---|---|---|
| A. Fixed clause-type hierarchy | `GrantOfAuthority ⊑ ScopeOfAuthorityClause ⊑ Clause` (the current `clause.ttl`) | Meaning is the clause's class. Every change to the classification is a T-Box release. |
| B. Attached meaning | `Clause expresses Statement`, where a small, fixed set of statement kinds carries parameters | Meaning is data attached to wording. Classifications become vocabularies. |
| C. Hybrid (MERIDIAN) | B, plus named classes generated where axioms or shapes need a target | Attached meaning at authoring time, classes only as compiled artefacts. |

This specification adopts **C**.

### 3.2 Answers to the questions posed

**Who defines the hierarchy?** The WIM clause sub-typing (Scope of Authority, Scope of
Coverage, Contractual Provision and their leaves) is defined by the LMA through the DA Wordings
Group and CBAA Steer. It is an externally governed classification, and by DP1 it belongs in the
A-Box as a SKOS scheme bound by a scheme contract. The statement kinds (§3.3) are
ontology-intrinsic mechanism. They are defined here and change only with an ontology release.

**Is the hierarchy fixed?** No. The WIM is a draft, and each module read so far has added
distinctions it does not name (complaints authority levels in M9, data protection roles in M13,
reporting roles in M10). Its own structure shows it is a classification rather than a set of
kinds: two leaves appear under both Grants of Coverage and Limitations, which a class hierarchy
can only represent through multiple inheritance.

**Does fixing it tie us to WIM?** Yes. A T-Box of clause types describes one market's wordings.
A policy wording, an MRC slip, a treaty or another market's binder would need a different
T-Box. Under option C another classification scheme binds to the same property and the
statement kinds are unchanged.

**General or WIM-specific?** General in mechanism, specific in content:

| Layer | Content | General or specific |
|---|---|---|
| Statement kinds, `expresses`, parameters | §3.3 | general |
| WIM structure (Contract, Component Group, Component, Data Element, `comprises`) | current `core.ttl` | WIM-normative, kept in the T-Box |
| Classifications (WIM clause types, element types, agreement types) | SKOS schemes | specific, A-Box |
| CBAA library content | wording objects, variables, attached statements | specific, A-Box |

Generality belongs upstream in LATTICE where LATTICE already has a layer for it (§10). Until
that decision is taken, the general mechanism is specified here in a form that can move
upstream unchanged.

**Does a runtime A-Box have efficiency needs this must consider?** Yes, and option C serves
them. Classification by SKOS concept is one triple, where classification by subclass needs
reasoning or materialised types. The extra hop from clause to statement never occurs at
runtime, because runtime artefacts are compiled from statements and do not traverse wording
(DP5). The source graph keeps the full wording-to-meaning chain for regulatory and audit use.

### 3.3 Statement kinds

A statement is the unit of attached meaning. Kinds are separated by DP2: each has a different
parameter structure. The prescriptive/constitutive split follows LegalRuleML.

| Kind | Meaning | CBAA example |
|---|---|---|
| **Prescriptive** | | |
| Obligation | bearer must perform an activity | FNOL onward transfer within 1 business day (M8 8.1.2A) |
| Prohibition | bearer must not perform an activity | must not bind New York risks unless excess lines licensed (M5 5.15.10) |
| Permission | bearer may perform an activity | may offer redress to resolve complaints (M9 9.1.2) |
| Power | bearer may change legal relations by an act | Right of Immediate Termination (M12 12.22) |
| AuthorityGrant | a power and permission delegated over an activity, with scope, level and limits | underwriting authority per SoUA table (M5), complaints authority (M9 9.1) |
| **Constitutive** | | |
| Definition | a term means something, optionally scoped to a jurisdiction | "Complaint – United Kingdom" (M9 table) |
| Classification | something counts as a category | agreement has US Classification "Surplus Lines" (M4 4.3.36B), communication deemed received (M12 12.10) |
| **Meta** | | |
| Precedence | one source prevails over another | the Agreement prevails over annexes (M1 1.2.1) |

`AuthorityGrant` is a named kind rather than a Power plus a Permission because the authority
envelope mechanism (§6) hangs off it.

A coverage grant, exclusion and limit for the Policy branch of the WIM are foreseen as further
kinds (MERIDIAN's TermApplication and Facet model covers them) but are out of scope for CBAA.

What is *not* a kind:

- **Conditions.** The WIM's Condition Precedent and Warranty classify how a breach of an
  obligation is treated. They become a SKOS classification on the obligation, not a kind.
- **Survival and temporal scope.** These qualify when a statement applies (M14 14.49,
  M13 13.8). They are parameters, not kinds.
- **Recitals.** Some clauses carry no computable content (M2 2.9 acknowledgement, M14 14.29
  modern slavery). A clause may express no statement. Its encoding status records whether that
  is a finding or simply not yet assessed.

### 3.4 Attachment

- `expresses` has domain *any WIM object*, not only Clause. A SoUA table (Data Element)
  expresses an authority grant's parameters. A conditional component group (M9 CG09.1)
  expresses nothing itself but gates inclusion of its members.
- Meaning is attached **once, to the library wording object version**, as statement templates
  whose parameters are bound to variable declarations. An agreement instance's statements are
  derived by binding variable values, not re-extracted. Extraction therefore runs once per
  published wording variant, not once per contract. Only bespoke free-text clauses (M3 3.7.1.3,
  M5 5.17, M12 12.24.1.5) need meaning attached per instance.
- Every statement records `prov:wasDerivedFrom` its wording version and may record
  `prov:wasGeneratedBy` the activity that produced it (§9). Assurance of that activity is not
  modelled (AP4).

### 3.5 Parameters

Following DP4 and MERIDIAN's TermApplication/Facet chain, a statement's parameters are nodes,
not literals on the statement.

| Parameter | Carried by | Source |
|---|---|---|
| bearer, counterparty | role (not party) | party stratum |
| activity | concept | activity scheme (§4) |
| scope | qualifier over dimensions (§6.2) | vocabulary |
| level | ordinal value | `qnt:OrdinalValue` over a level-of-authority scheme |
| limits, thresholds | ranges and bounds | `qnt:Range`, `qnt:Bound` |
| trigger | event type plus applicability condition | behaviour stratum |
| deadline | range anchored on the trigger's occurrence | `qnt:AnchorBinding` |
| recurrence | recurrence declaration | `qnt:Recurrence` |
| temporal scope, survival | validity relative to lifecycle states | foundation plus behaviour |

### 3.6 Two kinds of condition

These are distinct and must not share a mechanism:

| | Inclusion condition | Applicability condition |
|---|---|---|
| Attached to | wording object (library) | statement (meaning) |
| Decides | whether wording appears in an instance | whether a norm applies to a situation |
| Evaluated over | governing variables of the agreement | operational facts (a complaint, a policy, a claim) |
| Evaluated | once, at assembly and on amendment | at runtime, per event |
| Example | M1 1.6.3.1 included only if a broker is engaged | M9 9.2.10 refer if redress would exceed authority |

## 4. Vocabulary

### 4.1 Tiers

| Tier | Owner | Change | Home | Examples |
|---|---|---|---|---|
| V1 mechanism-intrinsic | this ontology | ontology release | `vocab/` beside the T-Box | inclusion modes, statement kinds' enumerations, day-count basis, population methods, comparison senses |
| V2 market standard | LMA, Lloyd's, LIMOSS (CDR), ISO, ACORD | published editions | A-Box, bound by scheme contract | insurable interest, perils, claims basis, sum insured basis, policyholder classification, level of authority, WIM clause classification, activities, Lloyd's risk codes, CRS v5.2 data items, ISO 3166 and 4217 |
| V3 deployment | a platform, market or tenant | at will | A-Box, extending V2 by mapping | an agent's internal class codes, regulatory territory groupings where a market body has not published one |

V2 content is never authored here. Where no published scheme exists yet (activities, regulatory
territory groupings such as "Europe A"), a provisional scheme is marked as such and replaced
when the owner publishes.

### 4.2 Scheme contracts and binding scope

Every concept-valued property declares a scheme contract (DP8), following LATTICE Vocabulary.
Two things are missing from LATTICE's mechanism for this domain:

1. **Scoped binding.** `voc:boundScheme` is functional and global, so a contract has one
   binding everywhere. CBAA needs bindings scoped by market or deployment (Lloyd's risk codes
   apply only with Lloyd's capacity) and by time.
2. **Pinned editions.** An agreement version must record the scheme editions it was made
   against. "Europe A" or an insurable interest group means what it meant when the agreement
   was accepted, not what a later edition says.

Patched upstream (D10): `voc:SchemeBinding` carries the contract, the edition, zero or more
`voc:BindingScope`s and a temporal scope, with `voc:boundScheme` retained as the unscoped
default, and `voc:resolvedUnder` records the binding a record was resolved under.

### 4.3 Override

A published edition is immutable. An override is a V3 scheme that extends a V2 edition, adding
narrower concepts or restricting membership, with `skos:broadMatch`/`skos:exactMatch` mappings
into the V2 edition. Governance checks follow MERIDIAN's obligations: mapping targets resolve,
mapping strengths do not contradict, bound schemes are populated.

### 4.4 Traversal cost

Path length matters in two places only: authority checks at the point of bind, and runtime
condition evaluation. Territory, insurable interest and peril are hierarchical and need
subsumption-aware membership (MERIDIAN Rule 2: flat membership produces false negatives).

- Design-time and regulatory queries may traverse `skos:broader*` freely.
- Runtime uses a compiled closure per pinned edition: either materialised
  `skos:broaderTransitive` assertions or an interval encoding (pre/post-order numbers, so
  ancestor tests are two comparisons). This is a derived artefact under DP5 and is regenerated
  when an edition changes.

### 4.5 Initial scheme contract catalogue

| Property (to be defined) | Dimension | Tier | Hierarchical | Runtime-critical |
|---|---|---|---|---|
| `riskLocation` | territory (country to city) | V2 ISO 3166 plus V3 | yes | yes |
| `policyholderLocation` | territory | V2 plus V3 | yes | yes |
| `territorialLimit` | territory | V2 plus V3 | yes | yes |
| `insurableInterest` | insurable interest | V2 CDR | yes | yes |
| `peril` | peril | V2 CDR | yes | yes |
| `policyholderClassification` | customer type | V2 | no | yes |
| `contractType` | insurance / reinsurance | V1 | no | yes |
| `riskCode` | Lloyd's risk code | V2 Lloyd's | no | yes, Lloyd's only |
| `activity` | activity | V2 (provisional) | yes | yes |
| `authorityLevel` | level of authority | V2, ordinal | no (ordered) | yes |
| `clauseClassification` | WIM clause types | V2 LMA | yes | no |
| `elementType` | Title, Paragraph, Numbered Clause, ... | V2 LMA | no | no |
| `agreementType` | Binding Authority, Line Slip, Consortium, DCAA | V2 LMA | no | no |
| `currency` | ISO 4217 | V2 ISO | no | yes |
| `claimsBasis`, `sumInsuredBasis` | bases | V2 CDR | no | yes |
| `dataItem` | reporting data items | V2 Lloyd's CRS v5.2 | no | no |

## 5. Quantification: Evaluation of LATTICE

### 5.1 Requirements against constructs

| Requirement (CBAA source) | LATTICE construct | Fit |
|---|---|---|
| Amount with ISO currency (M6, M9, M14) | `Quantity` on a currency `ValueSpace` with `UnitContract` | yes |
| "or equivalent in other currencies" (M9 9.1.3) | `Conversion` of kind `Contextual`, `ConversionContext` at a date | yes. A missing rate yields `Undetermined`, which maps to referral |
| Authored equivalents in several currencies (M5 SoUA row 42) | none | **gap** (L5) |
| Comparator as a variable, "equal to" or "not exceeding" (M6 6.1B) | `Bound` with `boundSense` and `boundClosure`, degenerate `Range` for equality | yes |
| Limits, maximum durations, advance binding days (M5) | `Range`, `Bound` | yes |
| Levels of authority and complaints authority as ordered values (M3 3.9.1.6, M5, M9) | `OrdinalValue` on a `TotalOrder` space | yes |
| Percentage of a base: commission 5% of each GWP, leader fee 10% of GWP, GWP trigger % (M6, M5) | `OperationCapability` of kind `Ratio` only. Derived rate spaces are open question 4 | **gap** (L2) |
| Relative change: increase of more than 10% (M3 3.9.1.1B) | `AnchorBinding` with a `Proportional` offset on the old value | yes |
| Deadlines relative to an event: within 1 business day of receipt, 10 business days before binding (M8, M4) | `AnchorBinding` of a temporal `Range` on the trigger occurrence | yes |
| Business vs calendar days, per jurisdiction (M3, M8, M12) | `UnitContract` plus `ConversionContext`. Calendar binding is open question 2 | **gap** (L3) |
| Recurring obligations: monthly, within 15 days of period end (M10), annual testing (M14) | `Recurrence`, `RecurrenceBin`, then `AnchorBinding` on the bin end | yes |
| Year of account and anniversary transfer (M2 2.9) | `Recurrence` with anchor | yes |
| 24:00 end-of-day convention (M2 guidance) | `Bound` closure and granularity | yes |
| Local time at the Coverholder's address (M2 2.1) | contextual conversion with a time-zone context | yes, via L3 |
| Loss ratio below 50% (M12 12.24.2.4.2) | `Quantity` in a ratio space | yes |
| Variable value constraints: at least 7 years, at least 24 hours (M10, M13) | `Range` as the admissible set of a variable declaration | yes |
| Unknown or disputed values, e.g. a complainant's eligibility in doubt (M9 9.2.9) | `UnresolvedValue` | **defect** (L1) |
| Totals across policies bound: GWP income limits (M5) | none, by design | out of scope. Belongs to criteria (§6.4) |
| Retained, explained results | `Comparison` with `OperationalProfile` | yes |

### 5.2 Verdict

LATTICE Quantification is a suitable starting point. It covers 13 of the 18 in-scope
requirements above directly, and a fourteenth once L3 lands. Its design stances match ours: it ships no units, currencies or
calendars (DP1), it distinguishes coarse values from unresolved ones, and its three-valued
comparison gives referral a principled home. Building an equivalent from scratch would
reproduce it.

Adoption has costs:

- It imports LATTICE Foundation 0.0.7 and Vocabulary 0.0.2, so it cannot be taken alone.
- Its own acceptance criteria are not yet met. The SHACL shapes are mostly empty, and it
  records a blocking dependency on a Foundation derived-artefact contract that does not exist.
- The patches in §10 are needed before CBAA can rely on it.

## 6. Authority: Data and Compiled Forms

Decided in principle: both (§12). This section specifies how.

### 6.1 Source of truth

Authority grants are data: `AuthorityGrant` statements (§3.3) attached to library wording and
bound per agreement version. Nothing about a particular agreement is authored in the T-Box.

### 6.2 Scope dimensions

A grant's scope is a qualifier over dimensions, after MERIDIAN's ScopeQualifier, with
subsumption-aware membership on hierarchical dimensions and `Any` for unconstrained ones (DP9).
Each dimension holds an include set and an optional exclude set, because the SoUA tables
include and exclude at every territorial level.

| Dimension | Hierarchical | Source |
|---|---|---|
| contract type | no | M5 5.1 |
| risk location, policyholder location, territorial limit | yes | M5 territory tables |
| insurable interest | yes | SoUA table |
| perils included, excluded | yes | SoUA table |
| policyholder classification | no | SoUA table |
| risk code | no | SoUA table (Lloyd's) |
| agreement segment | no | SoUA, MRAT, claims arrangements |
| trading location | no | M9 9.1.4, SoUA table |
| currency | no | M11 (unverified) |

### 6.3 Evaluation modes

| Mode | Question | Inputs | Mechanism |
|---|---|---|---|
| A, static admission | is the case within scope? | case facts, pinned vocabulary closure | set membership with subsumption |
| Q, quantitative | are amounts, durations and dates within bounds? | case values, grant ranges | `qnt:Comparison` |
| P, portfolio | do totals stay within aggregate limits? | accumulators (§6.4) | comparison on accumulated values |
| S, state | does the current lifecycle state permit the activity? | agreement state, special acceptances | state overlay (M12) |

The outcome is three-valued. `Permitted` needs every applicable mode true. `Denied` needs one
false. `Undetermined` covers missing or coarse data and maps to referral, carrying the reason.

By DP6, modes A and Q alone are used for comparing envelopes, detecting materiality and finding
overlaps. Mode S is used only when evaluating a case.

### 6.4 Accumulators

Aggregate limits (GWP income limits per table or agreement, per period) are stateful resources.
An accumulator is keyed by agreement identity, segment and recurrence bin, fed by operational
events, and read by mode P. This is MERIDIAN's capacity tank in a different domain: exhaustion
is an event, and the notification trigger (M5 SoUA row 47) is a threshold on the accumulator.

### 6.5 Compiled forms

All are derived artefacts under DP5, recording their inputs and generation profile.

| Artefact | Use | Logic |
|---|---|---|
| Runtime envelope table per agreement version | modes A and Q at the point of bind | flattened, closure-expanded concept sets and bounds. No reasoner |
| Per-agreement defined classes | design-time checks: materiality by subsumption between versions, unsatisfiable segments, overlapping segments | OWL 2 DL. Exclusions need negation and bounds need datatype facets, neither available in EL |
| SHACL shapes | closed-world validation of bordereau rows against the envelope | SHACL-SPARQL |

Regeneration follows MERIDIAN's invalidation table: a vocabulary edition change regenerates the
closures and the envelopes that use them, and a new agreement version regenerates that
agreement's artefacts only.

## 7. Ordering

Three different ordering problems, with different answers. The LATTICE patterns guide (Chapter
12) sets the options: `rdf:List`, an integer index, or a lexicographic rank key.

| Problem | Choice | Reason |
|---|---|---|
| Children within a structural parent (components in a group, clauses in a component) in library authoring | lexicographic rank key on the membership | drafting inserts clauses between others, and a rank key inserts without renumbering. Unchanged siblings keep unchanged keys, so version diffs, and therefore materiality detection, see only real changes |
| Variants within a variation slot | no order. The slot holds the position, variants are alternatives | exactly one variant is included |
| Inline segments within one text object version (text, variable reference, object reference) | integer index, with SHACL requiring indices 0..n−1, unique and contiguous | a published text object version is immutable, so renumbering never happens. The shape gives closed-world completeness without `rdf:List`'s query cost |
| Displayed clause numbers | derived after inclusion is resolved, never stored as identity | DP10 |

A rendering template (the text object as one literal with typed placeholders) may be compiled
from the segments for renderers. It is a derived artefact, not the source.

## 8. Instance Data: Reference Architecture Patterns

Technology-neutral (AP3). The backend is a graph store, RDF, LPG or hybrid, under moderate load.

### 8.1 Planes

| Plane | Content | Write pattern | Retention |
|---|---|---|---|
| Schema | T-Box, shapes, V1 vocabulary | ontology release | versioned |
| Vocabulary | V2 and V3 editions, scheme bindings | publication of editions | immutable editions |
| Library | WOL wording objects, variants, variable declarations, attached statements | single writer (authoring tool), publication | immutable published versions |
| Instance | agreements, versions, selections, bindings, parties and roles | compare-and-set per agreement | full history |
| Operational | quotes, policies bound, bordereau rows, FNOLs, complaints, obligation occurrences, state transitions | append-only streams | per policy, subject to erasure (§8.6) |
| Compiled | closures, envelopes, state tables, shapes, rendering templates | regenerated from inputs | replaceable |
| Governance | scheme-contract compliance, parity, provenance completeness | validation runs | audit |

Regulatory detail lives in the library, instance and operational planes. Runtime reads the
compiled plane (DP5).

### 8.2 Aggregates

The LATTICE patterns guide names aggregate boundaries as its largest missing decision (§30.3).
The WIM supplies one: the `comprises` tree.

- **Agreement version aggregate:** one named graph holding the Contract, its component groups,
  components and data elements, attached statements, bound variable values and pinned scheme
  editions. Immutable once accepted.
- **Agreement identity:** a persistent identity with a version row (current head, sequence)
  kept separate from payload, per the guide's Chapter 17.
- **Library object:** one named graph per published wording object version.

### 8.3 Identity

- Agreement identity must be an opaque surrogate, not derived from the UMR. The UMR can change
  within one agreement (M3 3.7.1.2) and some changes to it end the agreement (M3 3.9.1.16
  guidance). The UMR is a claimed key, unique per market, using the guide's key-claim pattern.
- The identity criteria that end an agreement (replacing a Coverholder legal entity, the Lead
  Insurer or the broker number) are checked when an amendment is proposed. They produce a new
  identity, not a version.
- Deterministic IRIs from natural keys where the key is stable: ISO codes, legal entity
  identifiers, Lloyd's syndicate numbers, wording object ids with version.

### 8.4 Concurrency

| Plane | Profile (patterns guide) |
|---|---|
| Library | baseline: single writer, immutable versions |
| Instance | strong: compare-and-set on the agreement version row, receipts, transaction claims |
| Operational | baseline plus a dense per-agreement stream sequence, for gap detection in reporting |
| Accumulators | strong, one version row per accumulator key |

### 8.5 Time

Transaction time is recorded on every write. Valid time is required on agreement versions
(effective from), amendments (effective date, which may be retrospective, M3 3.20) and
statements with survival (M14 14.49). Two further domain times are needed and are not provided
by LATTICE Foundation: the date an amendment was agreed, and the date from which it is
operationally implemented before its legal effect (M3 3.22).

### 8.6 Access and sharing

Access follows aggregates: named graphs make graph-level control possible. The "agreed subsets"
shared with Lloyd's, DCOM and LMA Insight (overview Model A) are projections compiled from the
instance and operational planes, not access rules over individual triples. Personal data (named
people in M4, complainants in M9) sits in per-subject aggregates so erasure can drop a graph
(patterns guide §24.5).

### 8.7 Transitions

Lifecycle protocols (agreement lifecycle M12, amendment approval M3, prior-submit referral,
FNOL M8, complaints M9) follow the SPC arrangement:

1. Protocols are declared as A-Box individuals over a fixed behaviour T-Box and verified at
   design time.
2. Inputs arrive as typed individuals through validated mappings (the MORK boundary), so
   guards check labels, not payloads.
3. Runtime interprets compiled state tables over a closed snapshot (DP7), with an explicit
   error transition for rejected input.

Guards that depend on operational aggregates, such as run-off ending only when every policy has
expired and every claim is resolved (M12 12.28), are evaluated in the operational plane and
delivered to the state machine as events.

## 9. Provenance

PROV-O is adopted.

| Thing | PROV-O |
|---|---|
| Library object version, agreement version, statement, compiled artefact | `prov:Entity` |
| Statement derived from wording | `prov:wasDerivedFrom` the wording object version |
| Meaning extraction, compilation, acceptance, amendment | `prov:Activity`, `prov:wasGeneratedBy` |
| Drafter, extraction tool, reviewer, signatory, platform | `prov:Agent` |
| Compiled artefact to its inputs | `prov:wasDerivedFrom` each input, plus the generation profile |

This gives the trace MERIDIAN relies on (tank → facet → clause) in our terms: runtime decision →
envelope → statement → wording object version. Assurance of extraction activities is not
modelled (AP4).

## 10. LATTICE

### 10.1 Assessment

| Layer | Version | Use here | Notes |
|---|---|---|---|
| Foundation | 0.0.7 | adopt | identity vs version, supersession, governance state, valid time and PROV-O alignment match §8 and §9. Missing: derived artefacts, agreed and operational dates |
| Vocabulary | 0.0.2 | adopt with L3 | scheme contracts are DP8's mechanism |
| Quantification | 0.0.1 | adopt with L1, L2, L4, L5 | §5 |
| Party | 0.0.3 | reference | role occupancy is a candidate for bearer and counterparty |
| Eligibility | 0.0.1 | reference | three-valued decisions and match strategies align with §6.3 |
| Instrument | 0.0.1 | reference | models obligations only. Defect L6 |
| SPC | provisional namespace | reference | §8.7 |

HermiT classification of Foundation through Instrument, run for this review, found two
unsatisfiable-class defects (L1, L6).

### 10.2 Proposed upstream changes

| # | Layer | Change |
|---|---|---|
| L1 | Quantification | **Defect.** `qnt:unresolvedReason` has domain `qnt:Comparison`, and `qnt:UnresolvedValue` requires one, so every unresolved value is inferred to be a Comparison, which is disjoint from Value. `UnresolvedValue` is unsatisfiable. Widen the domain to `Comparison ⊔ UnresolvedValue` |
| L2 | Quantification | Derived rate spaces (its open question 4): a proportional value, ratio times a referenced base, for commission and fees as a percentage of GWP |
| L3 | Quantification, Vocabulary | Calendar binding (its open question 2): business-day extents converted against a jurisdiction's calendar. The scoped scheme binding part is done (D10) |
| L4 | Foundation | The derived-artefact contract Quantification already depends on, reused for our compiled plane |
| L5 | Quantification | Authored equivalents on a bound: one limit stated in several currencies without conversion |
| L6 | Instrument | **Defect.** `Provision`, `Obligation` and `Qualifier` are subclasses of `Element` but listed with it in one `AllDisjointClasses`, so all three are unsatisfiable. Remove `Element` from the disjointness axiom |

### 10.3 Integration

Decided (D7). How LATTICE is brought in, which layers are imported, how Open DARE uses their
T-Box and assertions, the description logic encoding, toolchain reuse and the upstream changes
still needed are specified in the [LATTICE integration specification](lattice-integration.md).
It supersedes the table in §10.1 for Party, Eligibility, Instrument and Behaviour, whose fit
against CBAA content it establishes, and replaces §10.2's list with its own §8.

## 11. Consequences for the Current Ontology

Not yet applied. Applying DP1 and DP2 to the files in this directory:

| Current | Proposed |
|---|---|
| `Agreement` subclasses Binding Authority, Line Slip, Consortium, DCAA | concepts in an agreement-type scheme |
| `Policy` subclasses Insurance, Reinsurance | concepts in a contract-type scheme |
| Clause sub-typing tree in `clause.ttl` | concepts in a WIM clause-classification scheme, with the overlap (two leaves under two groups) as ordinary `skos:broader` links |
| `AgreementRelated`, `PolicyRelated` mixins | an applicability annotation on the classification concepts |
| Contractual Provision leaves (Claims, Complaints, ...) | concepts, aligned with the activity scheme |
| Text leaves (Title, Paragraph, ...) | concepts in an element-type scheme |
| Document/analogue artifacts | Document Objects referenced by `de:linksTo`, with `representationStatus` retained |
| Contract, Component Group, Component, Data Element, `comprises`, Text, Table, Variable, Metadata, Reference | kept as classes (structurally distinct) |
| none | `expresses` and the statement kinds (§3) in a new meaning module |

## 12. Decision Log

### Decided

| # | Decision | Date |
|---|---|---|
| D1 | Principles AP1–AP4 | 2026-09-24 |
| D2 | Wording and meaning are separated in the ontological model | 2026-09-24 |
| D3 | Vocabulary that changes often or varies by user lives in the A-Box. SKOS is the working choice | 2026-09-24 |
| D4 | Authority is held as data and compiled, both (§6 is the design) | 2026-09-24 |
| D5 | PROV-O alignment | 2026-09-24 |
| D6 | AP1 permits the tools used to produce and check the specifications. Reference implementation waits for the ontological design (was O1) | 2026-09-24 |
| D7 | LATTICE is imported. The mechanism is the subject of the integration specification (was O2) | 2026-09-24 |
| D8 | Option C and the statement kinds of §3.3 (was O3) | 2026-09-24 |
| D9 | Apply §11 to the current ontology (was O4). Sequenced after LATTICE is imported, since the reclassified schemes are `voc:` individuals (integration spec §9) | 2026-09-24 |
| D10 | Scoped scheme binding patched upstream, LATTICE `65ac4a8` (was O5) | 2026-09-24 |
| D11 | AP1–AP4 recorded in `.github/copilot-instructions.md` (was O6) | 2026-09-24 |

### Open

The integration specification's [open questions](lattice-integration.md#10-open-questions)
(I1–I4).
