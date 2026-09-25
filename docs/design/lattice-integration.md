# LATTICE Integration Specification

Version 0.4, draft for review. Companion to the [design specification](design-spec.md), whose
principles (AP, DP) and decisions (D) it cites by number. Baseline: LATTICE `main` at
`ddeaecf` (2026-09-25). Since the design specification's baseline (`558650b`) LATTICE has
taken scoped scheme binding, semantic versioning (ADR-A86), consumer import resolution
(ADR-A88), the applied ontology readiness unit and a test-only reasoning harness (ADR-A83).
Of §8, only L11's CI enforcement, L13 and L14 remain open.

Logical expressions use description logic notation: ⊑ subsumption, ≡ equivalence, ⊓ ⊔ ¬
conjunction, disjunction and negation, ∃ ∀ restrictions, {a} a nominal, ⊥ ⊤ bottom and top,
≤n =n ≥n qualified cardinality.

---

## 1. Scope

This specification settles four things:

1. how the LATTICE ontologies enter this repository and are resolved (§3)
2. which LATTICE terms Open CBAA specialises and which it instantiates (§4)
3. the description logic encoding Open CBAA commits to (§5)
4. how the compiled forms of design-spec §6.5 reuse LATTICE's toolchain, and how Persistence
   declares data-access expectations (§6, §7)

It does not specify implementation (AP1).

## 2. Layers

| Layer | `owl:versionIRI` at baseline | Use | How |
|---|---|---|---|
| Foundation | `…/lattice/foundation/0.3.0` | identity, versions, governance state, valid time, evidence, derived artefacts | `owl:imports` |
| Vocabulary | `…/lattice/vocabulary/0.3.0` | scheme contracts, editions, scoped bindings | `owl:imports` |
| Quantification | `…/lattice/quantification/0.5.0` | amounts, bounds, ranges, recurrences, ordinals | `owl:imports` (Party, Eligibility and later layers import it too) |
| Party | `…/lattice/party/0.5.0` | actors, roles, role occupancy, participation, delegation | `owl:imports` |
| Eligibility | `…/lattice/eligibility/0.6.0` | authority scopes as admission profiles, three-valued decisions | `owl:imports` |
| Instrument | `…/lattice/instrument/0.6.0` | alignment of statement kinds | `owl:imports` |
| Behaviour | `…/lattice/behaviour/0.6.0` | lifecycle state spaces, triggers, guards, allowances | `owl:imports` |
| Surface | `…/lattice/surface/0.5.0` | compilation contracts and derived records | imported by the compilation module only |
| MORK and Executable | `http://www.nebularis.org/ontologies/Mork/0.4.0`, `…/lattice/executable/0.5.0` | mapping graph, compiler provenance | imported by the compilation module only |
| Persistence | `…/lattice/persistence/0.2.1` | data-access profile | referenced by IRI, never imported (its own design, §7) |
| SPC | `http://example.org/spc/0.2.0` | protocol execution | reference only |

`…` is `https://www.nebularis.org/neuro-semantic`. Each layer's `spec` and `vocab` documents
are versioned independently (the table lists `spec`). Imports always use the exact
`owl:versionIRI`. The ontology IRIs themselves were not moved by the baseline reset
(Foundation's is still `…/foundation`, not `…/lattice/foundation`), so version IRI and ontology
IRI do not share a base (L11).

HermiT classification of Foundation through Behaviour at the baseline, spec and vocab documents
merged, finds no unsatisfiable classes among its 96 named classes. A mutation probe that makes
`ins:Obligation` unsatisfiable is detected, so the check detects the defect class it guards.
Mork and the Executable closure are consistent under HermiT since ADR-A97 made MORK's order
relations OWL 2 DL.

## 3. Repository Integration

### 3.1 Requirements

| # | Requirement |
|---|---|
| R1 | Pin exact content. Under ADR-A86 an ontology document's `owl:versionIRI` changes whenever its content does, so a version IRI identifies an ontology document's content. Files that declare no `owl:Ontology` (shapes, projections, generated execution artefacts) carry no version of their own and are identified only by commit |
| R2 | Resolve `owl:imports` offline. LATTICE's version IRIs do not dereference, and publishing them is deferred (ADR-A88) |
| R3 | Carry only what is used. LATTICE also holds platform code, applications and packages |
| R4 | Keep the upstream patch flow short, since patches are expected (§8) |
| R5 | Work with standard tooling (Protégé, OWL API, rdflib, HermiT) and no package manager |
| R6 | Consume LATTICE files unmodified, so their MPL-2.0 terms place no obligation on this repository |

### 3.2 Options

| Option | R1 | R2 | R3 | R4 | Notes |
|---|---|---|---|---|---|
| Git submodule | commit pin | with a catalog | whole repository | patch in place, push, bump | LATTICE is small (15 MB checkout, 4.5 MB history) |
| Submodule plus sparse checkout | commit pin | with a catalog | `ontology/` only | as above | sparse checkout is per-clone configuration, not versioned |
| Git subtree | copied in | yes | prefix only | awkward (`subtree push`) | copies drift and invite local edits, against R6 |
| Vendored snapshot plus lock file | hash pin | yes | chosen folders | copy back by hand | needs a sync tool, loses history |
| Resolve by IRI over the network | version IRI | no | n/a | n/a | fails R2 today, and covers no unversioned files |
| Pin by repository tag | tag | with a catalog | whole repository | as submodule | the existing tags (`v0.1.2`, `v0.1.3`) predate ADR-A86, and one repository tag cannot express per-document versions |

### 3.3 Recommendation

1. **Submodule** at `imports/lattice`, pinned to a commit. The commit pins everything,
   including the unversioned shapes Open CBAA validates with. Sparse checkout of `ontology/` is
   documented as optional.
2. **Imports as the dependency statement.** Open CBAA modules import LATTICE by exact version
   IRI, as LATTICE's own layers do. Those imports, not a separate manifest, state which
   document versions Open CBAA depends on.
3. **Catalog.** ADR-A88's consumer pattern. An OASIS XML catalog, `ontology/catalog-v001.xml`,
   maps Open CBAA's own ontology and version IRIs and chains to LATTICE's generated root
   catalog, `imports/lattice/ontology/catalog-v001.xml`, with `nextCatalog`. LATTICE's catalog
   maps every LATTICE IRI, including MORK's unversioned one. Protégé and the OWL API follow
   the chain. Python tooling uses the resolver in LATTICE's `tools/ontology_catalog.py`,
   since `rdflib` has no catalog support. That tool generates Open CBAA's own entries, but
   cannot yet emit the chain entry (L14).
4. **Gate.** Checked before any LATTICE layer is first imported and on every upgrade (D12):
   - *resolution*: every version IRI Open CBAA imports is declared by the file the catalog
     chain maps it to
   - *classification*: the import closure classifies with no unsatisfiable classes other than
     known upstream defects recorded in §8, and passes the SHACL suites
   - *ratification*: every LATTICE ADR whose decision an imported term depends on is Accepted
   - *automation*: LATTICE's versioning and catalog checks run in its CI
   - *conformance*: where Open CBAA relies on a layer's evaluation semantics (comparison,
     matching, resolution, transitions), a non-domain conformance case upstream covers it. Terms
     used only for typing need only the classification check
5. **Upgrade procedure.** LATTICE's import-pinning cascade checklist, applied to Open CBAA's
   modules: move the submodule, list the imported documents whose version IRI changed, update
   every Open CBAA `owl:imports` naming them in the same change, re-run the enumeration until
   no old IRI remains, and run the gate. Every LATTICE layer is at major version zero, where
   SemVer promises no stability, so a MINOR or PATCH bump is gated exactly like a MAJOR one
   until a layer reaches `1.0.0`. The pin moves at LATTICE milestones, a completed work unit
   whose ADRs are accepted, not at every commit. A single day of upstream work cascaded MINOR
   bumps through 12 and then 17 documents (`9a12da4`, `54caeb6`), so per-commit pinning would
   repeat that cascade here. The change is recorded in the design specification's decision
   log.

Fallback if submodules prove unworkable for contributors: a vendored snapshot of the same
folders, with its source commit recorded. The catalog and gate do not change.

### 3.4 Versioning Open CBAA's own documents

Open CBAA's ontology documents currently carry `owl:versionInfo "0.1.0"` and no
`owl:versionIRI`. The proposal (I5) is to adopt ADR-A86's policy for them unchanged, now that
ADR-A86 is Accepted upstream:

- one `owl:versionIRI` per `owl:Ontology` document, of the form
  `https://nebularis.github.io/open-cbaa/ontology/<path>/<version>`, e.g.
  `…/open-cbaa/ontology/lma-wim/core/0.1.0`, with `owl:versionInfo` dropped so the version IRI is
  the single signal
- LATTICE's MAJOR, MINOR and PATCH table, including its treatment of silent semantic
  redefinition as MAJOR
- the mechanical check reused from the submodule, with no copy in this repository:
  `python imports/lattice/tools/ontology_version_check.py --root . --base-ref <ref>`, which
  compares every `.ttl` under this repository's `ontology/` that declares `owl:Ontology` with
  the given ref. It runs against this repository today and passes its six documents. It
  reports a document with no version IRI only under a `spec/` or `vocab/` directory, which
  Open CBAA's flat layout does not use. So it protects Open CBAA's documents only once they
  carry version IRIs, or once they move into that layout

The reclassification (design-spec §11, D9) removes classes, which is MAJOR under the policy.
At major version zero that is permitted, and it moves the affected documents to `0.2.0`.

## 4. What Open CBAA Authors on LATTICE

Open CBAA subclasses a LATTICE class only where it adds structure (DP2). Otherwise it authors
individuals of LATTICE classes. It never restates or redefines a LATTICE term.

### 4.1 Foundation

| LATTICE term | Open CBAA use | Source |
|---|---|---|
| `fnd:PersistentIdentity`, `fnd:Version`, `fnd:supersededBy` | agreement identity and agreement versions. Identity-breaking changes mint a new identity, not a version | M3 3.2.1 |
| `fnd:Version`, `fnd:Governable` | published library object versions and their authoring state | WOL |
| `fnd:TemporallyScoped` | effective periods of agreement versions, amendments, role occupancies | M2, M3 |
| `fnd:Evidence` | acceptance and signature evidence | M2 2.3–2.8 |
| `fnd:DerivedArtefact`, `fnd:DerivationRun` | compiled artefacts and the runs that produce them, as `prov:Entity` and `prov:Activity` | design-spec §6.5, §9 |

Foundation has no term for the date an amendment was agreed or the date it is operationally
implemented before its legal effect (M3 3.22). Open CBAA declares both locally.

### 4.2 Vocabulary

| LATTICE term | Open CBAA use |
|---|---|
| `voc:SchemeContract` | one per concept-valued property (design-spec §4.5) |
| `voc:ConceptScheme` | each V2 and V3 edition, e.g. an insurable interest scheme edition |
| `voc:BindingScope` | markets (Lloyd's, Lloyd's Europe, company market) and deployments |
| `voc:SchemeBinding` | market-scoped schemes, e.g. Lloyd's risk codes bound only in the Lloyd's scope |
| `voc:resolvedUnder` | each agreement version records the bindings it was made under (design-spec §4.2) |

### 4.3 Quantification

| LATTICE term | Open CBAA use | Source |
|---|---|---|
| `qnt:ValueSpace`, `qnt:UnitContract` | money (units bound to ISO 4217 through a scheme contract), temporal position, temporal extent, percentage, ratio | all modules |
| `qnt:Quantity`, `qnt:Bound`, `qnt:Range` | limits, thresholds, comparator variables | M5, M6 |
| `qnt:AnchorBinding` | deadlines relative to a trigger | M8, M10 |
| `qnt:Recurrence` | reporting periods, year of account | M10, M2 2.9 |
| `qnt:OrdinalValue` | levels of underwriting and complaints authority on ordered spaces | M5, M9 |
| `qnt:Comparison`, `qnt:UnresolvedValue` | recorded quantitative outcomes, including `Undetermined`, and values known to be unknown | design-spec §6.3, M9 9.2.9 |
| `qnt:DerivedValueSpace` | percentages of a base: commission of GWP, leader fee | M6, M5 |
| `qnt:CalendarUnit`, `qnt:Calendar` | business-day extents, the calendar resolved as a scheme edition | M3, M8, M12 |
| `qnt:alternativeBound` | one limit stated in several currencies, each read in its own unit | M5 SoUA row 42 |

### 4.4 Party

| LATTICE term | Open CBAA use | Source |
|---|---|---|
| `pty:Actor` | legal entities and named people | M1, M4 |
| `pty:Role` | CBAA roles as individuals of an Open CBAA role scheme: Coverholder, Lead Insurer, Follow Insurer, Broker, Producing Intermediary, DCA, FNOL Handling Party, Claims Determination and Settlement Party, Data Formatter, Data Controller, Data Processor, Regulatory Body | M1–M14 |
| `pty:RoleOccupancy` | who holds each role in an agreement version, time-scoped, so outgoing and incoming underwriting members of an annual transfer are distinct occupancies | M2 2.9 |
| `pty:ParticipationGroup`, `pty:GroupMembership`, `pty:SeveralOnly` | the insurers of an agreement, each membership's share being its signed share, liability several and not joint | M1 1.19, M14 14.4, Insurer Capacity Table |
| `pty:Delegation` | a performing occupancy discharging an accountable one: the broker performing Coverholder activities, sub-delegation | M4 4.4, M14 14.48 |

The generic roles `pty:Obligor` and `pty:Obligee` are used on bound statements. The CBAA roles
above say who a party is in the agreement.

### 4.5 Eligibility

An `AuthorityGrant`'s scope (design-spec §6.2) is an `elg:AdmissionProfile` with
`elg:AllRequired`, holding one condition per dimension:

| Dimension kind | Condition | Strategy |
|---|---|---|
| flat concept set (contract type, policyholder class) | `elg:SetMembershipCondition` with `elg:requiredConcept` and `elg:excludedConcept` | `elg:SetMembership` |
| hierarchical concept set (territory, insurable interest, peril) | condition with `elg:constrainedByContract` naming the dimension's scheme contract, and required and excluded concepts | `elg:HierarchicalMatch` |
| bound (limit, duration, advance days) | `elg:IntervalCondition` with a `qnt:RangeSet` | `elg:IntervalContainment` |

Exclusions follow ADR-A87's decision table: an exclusion beats an inclusion, and a case valued
strictly above an excluded concept (France, where Corsica is excluded) is `Undetermined`. The
SoUA territory tables' include and exclude rows at every level map directly.

Candidates are read from the case through an `elg:EvidenceBinding` on Open CBAA's own
properties (`riskLocation`, `sumInsured`), not from `elg:Question` individuals (ADR-A91). Scheme
resolution needs an explicit instant and scope (ADR-A89), which come from the bindings the
agreement version was made under (design-spec §4.2).

Outcomes are `elg:EligibilityDecision` individuals valued `elg:Permitted`, `elg:Denied` or
`elg:Undetermined`.

### 4.6 Behaviour

| LATTICE term | Open CBAA use | Source |
|---|---|---|
| `bhv:StateSpace`, `bhv:State` | lifecycles: agreement, amendment approval, prior-submit referral, FNOL, complaint | M12, M3, M5, M8, M9 |
| `bhv:TransitionDefinition` with `bhv:ExternalStimulus` | event-driven transitions: insolvency of any party, notice served | M12 12.15, 12.23 |
| with `bhv:ScheduledTrigger` | timers: rectification periods, notice expiry | M12 12.22.2 |
| with `bhv:DerivedTrigger` | conditions over operational data: run-off ends when every policy has expired and every claim is resolved | M12 12.28 |
| `bhv:ImmediateActivation` and `bhv:ManualActivation` | automatic suspension, and a power a party chooses to exercise | M12 12.15, 12.22 |
| `bhv:GuardDefinition` → `elg:AdmissionProfile` | guards on transitions | |
| `bhv:AllowanceDefinition`, `bhv:AllowanceAccount` | aggregate limits: allowance space money, reset recurrence the GWP limit period. The account is the accumulator of design-spec §6.4 | M5 |

State-dependent authority (design-spec §6.3, mode S) is an Open CBAA property relating a
statement to the states in which it applies. It is not part of any envelope class (DP6).

### 4.7 Instrument

Open CBAA's `Obligation` is a subclass of `ins:Obligation`, and bound statements use
`ins:obligor`/`ins:obligee` to role occupancies. Attachment to wording is Open CBAA's
`expresses` (design-spec §3.4). ADR-A96 made `ins:inProvision` non-functional, so one
obligation can be expressed by two wording variants (M9 9.2.8A and B). Whether attachment
aligns with it is I6.

### 4.8 Surface, MORK and Persistence

These hold compilation and data-access declarations, not domain content. They are covered in
§6 and §7.

## 5. Description Logic Encoding

### 5.1 Commitments

| # | Commitment |
|---|---|
| C1 | OWL 2 DL throughout (SROIQ(D)). No OWL Full. Punning only where OWL 2 DL permits it, as in Surface's punned symbols |
| C2 | Reasoning is T-Box-first and at design time: subsumption and satisfiability over authored and generated classes. No decision depends on A-Box entailment |
| C3 | Open world for terminology. Closed world for completeness, validation and decisions, in SHACL and SPARQL (DP7) |
| C4 | No unique name assumption. Where a value must be exclusive, SHACL checks it |
| C5 | SWRL artefacts are DL-safe and positive only. They never derive `Denied` or `Undetermined`, following LATTICE's own rule |
| C6 | Three-valued logic lives in compiled evaluators and `elg:Decision` values, not in DL |

### 5.2 Fragments per stratum

| Stratum | Constructs | Fragment | Reasoning task |
|---|---|---|---|
| LATTICE substrate | as authored upstream | SROIQ(D) | consistency of the import closure |
| WIM structure | transitive and inverse roles, role hierarchy, irreflexive and asymmetric simple roles, ∀, ⊔, disjointness | SHI with role characteristics | consistency, containment typing |
| Meaning (statements) | qualified cardinality, disjoint kinds, datatype properties | SHIQ(D) | satisfiability of kinds |
| Generated nominal and hierarchy classes | ⊓, ∃R.{c}, subsumption between atomic classes, disjointness | EL++ | classification and subsumption at scale |
| Generated envelope classes | ⊓, ⊔, ¬, ∃R.C, nominals, datatype facets | ALCO(D) | subsumption, satisfiability |
| Vocabulary content | SKOS in the A-Box | none | none. `skos:broader` is not transitive and is never read as `rdfs:subClassOf` |

### 5.3 Structure (current, retained)

    directlyComprises ⊑ comprises
    comprises ∘ comprises ⊑ comprises
    Irr(directlyComprises)          Asy(directlyComprises)
    Contract       ⊑ ∀comprises.(ComponentGroup ⊔ Component ⊔ DataElement)
    ComponentGroup ⊑ ∀comprises.(ComponentGroup ⊔ Component ⊔ DataElement)
    Component      ⊑ ∀comprises.(Component ⊔ DataElement)
    DataElement    ⊑ ∀comprises.⊥
    Disj(Contract, ComponentGroup, Component, DataElement)

### 5.4 Typing after reclassification (design-spec §11)

Classifications become SKOS concepts, so the T-Box carries properties, not subclasses:

    Contract ⊑ ∃contractCategory.⊤
    contractCategory is functional, and its values come from the scheme bound to its contract

Where a class is useful, it is generated, not authored (Surface `NominalClass`):

    σ(BindingAuthority) ≡ Contract ⊓ ∃contractCategory.{BindingAuthority}

The current axiom that no contract is both an Agreement and a Policy becomes a SHACL check
(C4): OWL cannot conclude that two concepts from an external scheme are distinct individuals.

### 5.5 Meaning

Statement kinds are pairwise disjoint classes:

    Disj(Obligation, Prohibition, Permission, Power, AuthorityGrant,
         Definition, Classification, Precedence)
    Obligation ⊑ ins:Obligation

Library templates and agreement-bound statements are distinguished orthogonally to kind:

    StatementTemplate ⊓ BoundStatement ⊑ ⊥
    BoundStatement ⊑ =1 boundFrom.StatementTemplate
    boundFrom ⊑ prov:wasDerivedFrom

Attachment to wording is provenance:

    expressedBy ≡ expresses⁻
    expressedBy ⊑ prov:wasDerivedFrom
    StatementTemplate ⊑ ∃expressedBy.WimObject

Parameters sit on the statement as nodes (DP4). Templates name roles, bound statements name
occupancies:

    Obligation ⊓ StatementTemplate ⊑ =1 bearer.pty:Role ⊓ =1 activity.⊤
    Obligation ⊓ BoundStatement    ⊑ =1 ins:obligor.pty:RoleOccupancy
    AuthorityGrant ⊑ =1 activity.⊤ ⊓ =1 grantee.pty:Role
                     ⊓ =1 scope.elg:AdmissionProfile ⊓ ≤1 level.qnt:OrdinalValue

DL gives kinds and parameter structure. It does not give deontic semantics: an obligation and a
prohibition over the same activity are not a DL inconsistency. Conflict detection uses
generated classes (§5.6).

### 5.6 Generated classes for design-time checks

These classes, and the reasoner tasks in the table below, are those of LATTICE's design-time
OWL backend (ADR-A90). Open CBAA uses that backend and does not generate the classes itself
(D14). The reasoner runs in LATTICE's test-only harness (ADR-A83), through the `check-classes`
command of `mork_compilers`.

**Hierarchy classes.** For each concept c of a hierarchical dimension's pinned scheme edition,
a class Within(c) of the concepts at c or below, with the SKOS hierarchy compiled into
subsumption:

    {c} ⊑ Within(c)                       for every concept c
    Within(d) ⊑ Within(c)                 for every d with d skos:broader c
    Within(c) ⊓ Within(c′) ⊑ ⊥            for siblings c and c′, top concepts included, only
                                          when the compilation requests it (I9)

A case valued at or below c on dimension R is ∃R.Within(c). All three forms are in OWL 2 EL.
This is where subsumption-aware matching (design-spec §4.4) enters the T-Box. Disjointness is
refused for a scheme in which a concept has several broader concepts. Without it, the checks
below err towards reporting an overlap or an expansion, never towards missing one. Concepts a
module names are declared distinct (C4 holds for everything else).

**Single-valued paths.** A condition reads its candidate through an `elg:EvidenceBinding`
(§4.5). The backend compiles only a binding that claims `elg:singleValued`, and restricts
each step of its path to at most one value. It also generates a SHACL shape that checks the
claim on data. A dimension on which a case may hold several values has no class (I7).

**Envelope classes.** For each bound authority grant g, one class over the static dimensions
(modes A and Q only, DP6): the class of the grant's `elg:AdmissionProfile`, the intersection of
its condition classes. For a grant covering insurance, risks in France except Corsica, and sums
insured up to GBP 5,000,000:

    Env_g ≡ Case
            ⊓ ≤1 contractType ⊓ ∃contractType.{Insurance}
            ⊓ ≤1 riskLocation ⊓ ∃riskLocation.(Within(France) ⊓ ¬Within(Corsica))
            ⊓ ≤1 sumInsured ⊓ ∃sumInsured.(∃qnt:inUnit.{GBP}
                                             ⊓ ∃qnt:numericValue.owl:real[≤ 5000000])

A limit stated in several currencies (ADR-A95) is a union of such restrictions, one per unit.
A sum insured in any other currency matches none of them. Cross-currency comparison needs a
rate and is decided outside DL (`Undetermined` without a conversion context).

**Checks the reasoner answers.** No A-Box is involved, so the open world does not distort the
answers:

| Question | DL task | CBAA use |
|---|---|---|
| Did an amendment expand authority? | Env_g′ ⋢ Env_g, for g′ the amended grant | materiality (M3 3.9.1) |
| Does a segment authorise anything? | satisfiability of Env_g | envelope sanity |
| Do two segments overlap? | satisfiability of Env_g ⊓ Env_h | overlapping remuneration or claims arrangements |
| Are a slot's inclusion conditions exclusive? | satisfiability of Cond_i ⊓ Cond_j | variation slots, once the conditions are authored as profiles (I8) |
| Do an obligation and a prohibition clash? | satisfiability of Scope_o ⊓ Scope_p for the same bearer and activity | norm conflicts (M14 14.19 vs 14.23.1), once scopes are authored as profiles (I8) |

### 5.7 Not in DL

Aggregates over populations, arithmetic, cross-currency comparison, time arithmetic in business
days, precedence resolution, scheme-binding resolution, completeness and value exclusivity.
These are SHACL, SPARQL or compiled evaluators, each with PROV-O provenance.

## 6. Compilation Toolchain

### 6.1 What LATTICE provides

| Component | Input | Output | Provenance |
|---|---|---|---|
| `tools/mork_compilers` | Eligibility conditions (interval, exact, set membership, hierarchical match, with required and excluded concepts) and `AllRequired`/`AnySufficient` profiles, with candidates read through evidence bindings | a shared IR (interval and concept plans), then SPARQL `mork:QueryTemplate` for all three outcomes, SHACL shapes, structured SWRL, and design-time OWL classes with subsumption, satisfiability and overlap checks | `exe:ExecutablePlan`, `exe:ConceptMatchPlan`, `exe:producesArtefact`, `exe:derivedFrom…Node`, `exe:OwlArtefact`, `exe:DesignTimeCheck`, aligned to PROV-O. Every `Undetermined` carries an `exe:Diagnostic` |
| `tools/surface` | `srf:IndexContract`, `srf:PromotionContract`, `srf:ProjectionContract`, `srf:SurfaceProfile` | generated symbols (nominal classes, memberships, closure relations, promoted properties), and lowering of projections into MORK | `srf:GeneratedSurface`, `srf:ReadSetEntry` with content hashes and the scheme binding each read resolved under, `srf:LawDischarge` |
| MORK ontology | mapping graph | `mork:GenerativeMapping` kinds (projection, rule, shape, transform), `mork:OwlAxiom`/`mork:OwlClass` for T-Box generation, intent nodes, uncertain mappings | generative mappings are `fnd:Version` and `fnd:Governable` |
| `tools/persistence` | `dal:` profiles | SPARQL operation templates, identity-minting recipes | compiled profile records |
| `tools/ontology_catalog.py`, `tools/ontology_version_check.py` | a repository's ontology documents | catalogs, import closures, version-bump findings | none |

Current limits of `mork_compilers`: SHACL and SWRL compile concept conditions only over
`Expanded` closures, enumerated from one scheme edition at compile time. The OWL backend
compiles only bound conditions with a claimed single-valued path (§5.6). SWRL interval rules
are not yet checked under a reasoner, since HermiT does not evaluate SWRL builtins.
`elg:DimensionConsistent` profiles are refused, having no evaluable definition.

### 6.2 Open CBAA's compiled forms

| Compiled form (design-spec §6.5) | Route | Reuse |
|---|---|---|
| Runtime envelope table | Surface `IndexContract` with `ClosureRelation` over `skos:broader` and a `ContractBoundPopulation` per hierarchical dimension. `PromotionContract` flattens grant parameters. A `ProjectionContract` (`JoinProjection`) assembles rows, lowered to MORK, compiled to SPARQL | Surface as it stands, not yet exercised on an Open CBAA contract |
| SHACL validation of bordereau rows | `mork_compilers` shared IR and SHACL backend over the grant's Eligibility conditions | as it stands, `Expanded` closure over the pinned edition |
| Envelope and hierarchy classes (§5.6) | the same shared IR with ADR-A90's OWL backend | as it stands, for single-valued dimensions (I7) |

Routing all three through one IR gives one reading of a grant's conditions. The lookup table,
the shapes and the classes cannot then disagree about what a grant means, which is the reason
LATTICE introduced the shared IR (ADR-A24).

### 6.3 A data-driven pipeline

Every compilation is declared in the graph before it runs:

| Element | Declared as |
|---|---|
| What to compile | a Surface contract or a MORK mapping, authored in an Open CBAA compilation module |
| Order | `mork:dependsOnMapping`, a declared DAG |
| How | an `srf:SurfaceProfile`: generator version, canonicalisation version, entailment regime, naming. A profile change is a new profile version and a full regeneration |
| What was read | `srf:ReadSetEntry` per input, with its content hash and, for a scheme, the instant, scope and binding it was resolved under |
| What was produced | `srf:DerivedArtefact` records and `exe:` plans |
| What was proven | `srf:LawDischarge` for runtime-conformance laws |

The same staleness rule then covers every compiled artefact: stale when any recorded read hash
differs from the current one. A read of a LATTICE ontology document can also record its version
IRI (`srf:readVersion`), which under ADR-A86 changes whenever its content does.

**Uniform provenance.** Foundation's derived-artefact contract is aligned with PROV-O, which
Open CBAA adopted (D5): `fnd:DerivedArtefact ⊑ prov:Entity`, `fnd:DerivationRun ⊑
prov:Activity`, and `srf:DerivedArtefact ⊑ fnd:DerivedArtefact`. Executable aligns directly:
`exe:ExecutablePlan` and `exe:GeneratedArtefact ⊑ prov:Entity`, `exe:derivedFrom…Node ⊑
prov:wasDerivedFrom` (ADR-A92). One query then answers "where did this come from" across
meaning extraction, compilation and runtime decisions.

**Meaning extraction.** MORK's uncertain mappings, hypotheses and intent nodes are a ready
home for meanings proposed by InsurLE compilation or LLM extraction and later validated by a
person (design-spec §3.7). Open CBAA records the provenance. Assurance of the extraction stays
out of scope (AP4).

## 7. Persistence

### 7.1 What it is for

Persistence declares data-access behaviour: aggregate boundaries, concurrency, ordering,
receipts, uniqueness, identity minting, epoch and privacy. Contract behaviour (obligations,
lifecycles) belongs to Behaviour and SPC. So Persistence is where Open CBAA states its
data-access expectations (design-spec §8). Contract behaviour is declared elsewhere.

### 7.2 Profile module

An Open CBAA profile module declares `dal:` individuals that target Open CBAA classes by IRI.
Persistence imports nothing and is imported by nothing, so no Open CBAA ontology depends on it.

| Design-spec §8 | `dal:` declaration |
|---|---|
| agreement version aggregate | `dal:NamedGraphBoundary`, one graph per accepted version |
| agreement identity | `dal:Optimistic` concurrency, `dal:CommitGrain`, `dal:PatchLog` receipts (amendment diffs feed materiality checks) |
| library object versions, vocabulary editions | `dal:ProvidedConcurrency` (single writer, immutable) |
| operational streams | `dal:AppendOnly`, `dal:EventGrain` |
| accumulators | `dal:Optimistic`, one version row per accumulator key |
| named people, complainants | `dal:PersonalData`, `dal:PerSubjectGraphDrop`, `dal:ReceiptOnly` |
| UMR unique per market | `dal:UniquenessConstraint` with the market as scope property |
| agreement identity minting | `dal:SurrogateClaimedIdentity` with the UMR constraint as its claim |

Persistence refuses personal data under a replay-capable receipt model unless it is scoped per
subject or crypto-shredded. That confirms design-spec §8.6: people live in their own aggregates,
and the agreement aggregate holds references, so it can keep a patch log.

### 7.3 Adoption

- **Now:** the configuration vocabulary for boundaries, concurrency, ordering, receipts,
  uniqueness and privacy. These declarations are data (AP1 permits them) and cost nothing if
  the code generator is never run.
- **Later:** identity-minting declarations, once LATTICE's identity work package settles, and
  code generation when a reference implementation starts.
- **Deployment-owned:** epoch authority and shard counts. The reference module sets defaults
  at low `dal:priority` for deployments to override.

## 8. Upstream Changes

Status at the baseline `ddeaecf`. Items closed upstream stay listed, since other documents cite
them by number.

| # | Layer | Change | Status | Blocks while open |
|---|---|---|---|---|
| L1 | Quantification | widen `qnt:unresolvedReason`'s domain so `UnresolvedValue` is satisfiable | done, `9a12da4` | |
| L2 | Quantification | derived rate values (a percentage of a base) | done, `ddeaecf`, ADR-A93 | |
| L3a | Vocabulary | scoped, time-bounded binding | done, `65ac4a8`, ADR-A85 | |
| L3b | Quantification | calendar binding for business-day extents | done, `ddeaecf`, ADR-A94 | |
| L4 | Foundation | derived-artefact contract | done, `54caeb6`, ADR-A92 | |
| L5 | Quantification | one bound stated in several currencies | done, `ddeaecf`, ADR-A95, with unit selection in every compiler backend | |
| L6 | Instrument | remove `ins:Element` from the disjointness axiom that makes its subclasses unsatisfiable | done, `9a12da4` | |
| L7 | Eligibility | an exclusion construct | done, `9a12da4`, ADR-A87 | |
| L8 | Surface, Executable | PROV-O alignment of derived records and plans | done, `54caeb6`, ADR-A92 | |
| L9 | Surface, Eligibility | honour `voc:SchemeBinding` where they read `voc:boundScheme` | done, `284dbe5`, `0742073` | |
| L10 | `mork_compilers` | set membership, hierarchical match, exclusion, profile aggregation, OWL backend | done, `6e9acb1`, `ddeaecf`, ADR-A89, A-90 (single-valued paths), A-91, with the ADR-A83 harness | |
| L11 | all | semantic versioning and its enforcement | ADR-A86 and A-88 Accepted, policy and consumer catalog in place. Open: run the versioning and catalog checks in CI (both workflows are manual-only), decide whether ontology IRIs move under `…/lattice/`, and extend the missing-version-IRI check beyond `spec/` and `vocab/` directories for consumers | the gate's automation condition (§3.3), and version checking of Open CBAA's flat layout (§3.4) |
| L12 | Instrument | `ins:inProvision` is functional, so one obligation cannot be expressed by several provisions | done, `ddeaecf`, ADR-A96 | |
| L13 | Quantification | a non-domain conformance corpus, its own acceptance criterion (README §14) | open | the gate's conformance condition for comparisons (design-spec §6.3, mode Q) |
| L14 | tools | `ontology_catalog.py write` emits a consumer's `nextCatalog` chain and takes the consumer's external imports | open | a generated Open CBAA catalog with no hand edits |

## 9. Sequencing

1. Upstream: run the versioning and catalog checks in CI and extend the version check to
   consumers (L11), and L14. These meet the gate's automation condition for every layer.
2. Add the submodule and catalog, give Open CBAA's documents version IRIs (§3.4), import
   Foundation, Vocabulary and Party (Party brings Quantification), and run the gate.
3. Apply the reclassification (design-spec §11), with schemes as `voc:ConceptScheme` editions
   and properties bound by `voc:SchemeContract`.
4. Add the meaning module (statement kinds, §5.5) on Party, Eligibility and Instrument.
5. Upstream L13. Add the compilation module (Surface contracts, profile) and the Persistence
   profile module. The design-time classes (§5.6) follow L10.
6. Declare the lifecycles on Behaviour (M12, M3, referral, FNOL, complaints).

Step 3 waits for step 2 because the reclassified schemes are `voc:` individuals. Step 5's
design-time classes need I7 and I8 settled.

## 10. Open Questions

| # | Question | Recommendation |
|---|---|---|
| I1 | Submodule path and catalog location | `imports/lattice`, `ontology/catalog-v001.xml` chained to LATTICE's catalog (§3.3) |
| I2 | Import Instrument and Behaviour before L6 lands | closed: L6 is fixed (D13) |
| I3 | Agreement version boundary: named graph, or a composite boundary walking a shape over `directlyComprises` | named graph for accepted, immutable versions |
| I4 | Envelope classes from an extended `mork_compilers` IR, or a new Surface backend | closed: ADR-A90 extends the IR (D14) |
| I5 | Adopt ADR-A86's versioning policy for Open CBAA's own ontology documents | yes, ADR-A86 is Accepted (§3.4) |
| I6 | Align attachment with Instrument, now that ADR-A96 is accepted | yes for obligations only: a sub-property of both `expressedBy` and `ins:inProvision`, with WIM objects that express obligations typed `ins:Provision`. Other statement kinds keep `expressedBy` alone |
| I7 | Dimensions on which a case holds several values (risk locations, perils, classes of business) have no design-time class under single-valued paths (§5.6) | open |
| I8 | Author variation-slot inclusion conditions and statement scopes as `elg:AdmissionProfile`s, so the last two checks of §5.6 come from the same backend | open |
| I9 | Where sibling disjointness is declared: an option of each compilation, or a Vocabulary declaration on the scheme edition (ADR-A90's open question) | open |
| I10 | How suggested meaning (design-spec §3.7) is held apart from accepted statements, and in which plane (design-spec §8.1): MORK uncertain mappings or hypotheses in LATTICE, or an Open CBAA suggestion class | open. Leaning to MORK's nodes in a staging graph, promoted to a statement on acceptance, since the library plane holds only published versions |
