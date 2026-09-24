# LATTICE Integration Specification

Version 0.1, draft for review. Companion to the [design specification](design-spec.md), whose
principles (AP, DP) and decisions (D) it cites by number. Baseline: LATTICE `main` at
`65ac4a8` (2026-09-24), which includes the scoped scheme binding patch.

Logical expressions use description logic notation: ⊑ subsumption, ≡ equivalence, ⊓ ⊔ ¬
conjunction, disjunction and negation, ∃ ∀ restrictions, {a} a nominal, ⊥ ⊤ bottom and top,
≤n =n ≥n qualified cardinality.

---

## 1. Scope

This specification settles four things:

1. how the LATTICE ontologies enter this repository and are resolved (§3)
2. which LATTICE terms Open DARE specialises and which it instantiates (§4)
3. the description logic encoding Open DARE commits to (§5)
4. how the compiled forms of design-spec §6.5 reuse LATTICE's toolchain, and how Persistence
   declares data-access expectations (§6, §7)

It does not specify implementation (AP1).

## 2. Layers

| Layer | Ontology IRI at baseline | Use | How |
|---|---|---|---|
| Foundation | `…/foundation/0.0.7` | identity, versions, governance state, valid time, evidence | `owl:imports` |
| Vocabulary | `…/vocabulary/0.0.2` | scheme contracts, editions, scoped bindings | `owl:imports` |
| Quantification | `…/quantification/0.0.1` | amounts, bounds, ranges, recurrences, ordinals | `owl:imports`, after L1 |
| Party | `…/party/0.0.3` | actors, roles, role occupancy, participation, delegation | `owl:imports` |
| Eligibility | `…/eligibility/0.0.1` | authority scopes as admission profiles, three-valued decisions | `owl:imports`, after L7 |
| Instrument | `…/instrument/0.0.1` | alignment of statement kinds | `owl:imports`, after L6 |
| Behaviour | `…/behaviour/0.0.1` | lifecycle state spaces, triggers, guards, allowances | `owl:imports`, after L6 (it imports Instrument) |
| Surface | `…/surface/0.0.1` | compilation contracts and derived records | imported by the compilation module only |
| MORK and Executable | `http://www.nebularis.org/ontologies/Mork`, `…/lattice/executable/0.0.1` | mapping graph, compiler provenance | imported by the compilation module only |
| Persistence | `…/lattice/persistence/0.1.0` | data-access profile | referenced by IRI, never imported (its own design, §7) |
| SPC | provisional | protocol execution | reference only |

`…` is `https://www.nebularis.org/neuro-semantic`. Ontology IRIs and term namespaces differ in
LATTICE (ontology `…/foundation`, terms `…/lattice/foundation#`). Imports always use the
`owl:versionIRI`.

## 3. Repository Integration

### 3.1 Requirements

| # | Requirement |
|---|---|
| R1 | Pin exact content, not a version label. Vocabulary's content changed at `65ac4a8` under an unchanged `0.0.2` versionIRI, so a versionIRI alone does not identify content |
| R2 | Resolve `owl:imports` offline. LATTICE's versionIRIs did not resolve over the network when checked (2026-09-24) |
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
| Resolve by IRI over the network | none | no | n/a | n/a | fails R1 and R2 today |

### 3.3 Recommendation

1. **Submodule** at `imports/lattice`, pinned to a commit. Sparse checkout of `ontology/` is
   documented as optional.
2. **Catalog.** An OASIS XML catalog, `ontology/catalog-v001.xml`, maps each LATTICE
   versionIRI to its file under `imports/lattice/ontology/…`. Protégé and the OWL API read it
   directly. The validation tools read the same file. LATTICE's own catalogs point at absolute
   paths on one machine and are not used.
3. **Lock record.** `ontology/lattice.lock.ttl` records, per imported module, the versionIRI,
   the path, the submodule commit and the SHA-256 of the file. It is described in RDF using
   Surface's read-set vocabulary (`srf:ReadSetEntry`, `srf:readHash`, `srf:readVersion`), so
   the same staleness rule applies to our imports as to any compiled artefact: an import is
   stale when its current hash differs from the recorded one.
4. **Update procedure.** Move the submodule to a new commit, regenerate the lock record, run
   the gate (HermiT classification and the SHACL suites over the import closure), and record the
   change in the design specification's decision log.

Fallback if submodules prove unworkable for contributors: a vendored snapshot of the same
folders with the same lock record. The catalog and lock format do not change.

## 4. What Open DARE Authors on LATTICE

Open DARE subclasses a LATTICE class only where it adds structure (DP2). Otherwise it authors
individuals of LATTICE classes. It never restates or redefines a LATTICE term.

### 4.1 Foundation

| LATTICE term | Open DARE use | Source |
|---|---|---|
| `fnd:PersistentIdentity`, `fnd:Version`, `fnd:supersededBy` | agreement identity and agreement versions. Identity-breaking changes mint a new identity, not a version | M3 3.2.1 |
| `fnd:Version`, `fnd:Governable` | published library object versions and their authoring state | WOL |
| `fnd:TemporallyScoped` | effective periods of agreement versions, amendments, role occupancies | M2, M3 |
| `fnd:Evidence` | acceptance and signature evidence | M2 2.3–2.8 |

Foundation has no term for the date an amendment was agreed or the date it is operationally
implemented before its legal effect (M3 3.22). Open DARE declares both locally.

### 4.2 Vocabulary

| LATTICE term | Open DARE use |
|---|---|
| `voc:SchemeContract` | one per concept-valued property (design-spec §4.5) |
| `voc:ConceptScheme` | each V2 and V3 edition, e.g. an insurable interest scheme edition |
| `voc:BindingScope` | markets (Lloyd's, Lloyd's Europe, company market) and deployments |
| `voc:SchemeBinding` | market-scoped schemes, e.g. Lloyd's risk codes bound only in the Lloyd's scope |
| `voc:resolvedUnder` | each agreement version records the bindings it was made under (design-spec §4.2) |

### 4.3 Quantification

| LATTICE term | Open DARE use | Source |
|---|---|---|
| `qnt:ValueSpace`, `qnt:UnitContract` | money (units bound to ISO 4217 through a scheme contract), temporal position, temporal extent, percentage, ratio | all modules |
| `qnt:Quantity`, `qnt:Bound`, `qnt:Range` | limits, thresholds, comparator variables | M5, M6 |
| `qnt:AnchorBinding` | deadlines relative to a trigger | M8, M10 |
| `qnt:Recurrence` | reporting periods, year of account | M10, M2 2.9 |
| `qnt:OrdinalValue` | levels of underwriting and complaints authority on ordered spaces | M5, M9 |
| `qnt:Comparison` | recorded quantitative outcomes, including `Undetermined` | design-spec §6.3 |

### 4.4 Party

| LATTICE term | Open DARE use | Source |
|---|---|---|
| `pty:Actor` | legal entities and named people | M1, M4 |
| `pty:Role` | CBAA roles as individuals of an Open DARE role scheme: Coverholder, Lead Insurer, Follow Insurer, Broker, Producing Intermediary, DCA, FNOL Handling Party, Claims Determination and Settlement Party, Data Formatter, Data Controller, Data Processor, Regulatory Body | M1–M14 |
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
| flat concept set (contract type, policyholder class) | `elg:SetMembershipCondition` | `elg:SetMembership` |
| hierarchical concept set (territory, insurable interest, peril) | condition with `elg:constrainedByContract` naming the dimension's scheme contract | `elg:HierarchicalMatch` |
| bound (limit, duration, advance days) | `elg:IntervalCondition` with a `qnt:RangeSet` | `elg:IntervalContainment` |

Outcomes are `elg:EligibilityDecision` individuals valued `elg:Permitted`, `elg:Denied` or
`elg:Undetermined`. Exclusions ("but excluding") have no Eligibility construct today (L7).

### 4.6 Behaviour

| LATTICE term | Open DARE use | Source |
|---|---|---|
| `bhv:StateSpace`, `bhv:State` | lifecycles: agreement, amendment approval, prior-submit referral, FNOL, complaint | M12, M3, M5, M8, M9 |
| `bhv:TransitionDefinition` with `bhv:ExternalStimulus` | event-driven transitions: insolvency of any party, notice served | M12 12.15, 12.23 |
| with `bhv:ScheduledTrigger` | timers: rectification periods, notice expiry | M12 12.22.2 |
| with `bhv:DerivedTrigger` | conditions over operational data: run-off ends when every policy has expired and every claim is resolved | M12 12.28 |
| `bhv:ImmediateActivation` and `bhv:ManualActivation` | automatic suspension, and a power a party chooses to exercise | M12 12.15, 12.22 |
| `bhv:GuardDefinition` → `elg:AdmissionProfile` | guards on transitions | |
| `bhv:AllowanceDefinition`, `bhv:AllowanceAccount` | aggregate limits: allowance space money, reset recurrence the GWP limit period. The account is the accumulator of design-spec §6.4 | M5 |

State-dependent authority (design-spec §6.3, mode S) is an Open DARE property relating a
statement to the states in which it applies. It is not part of any envelope class (DP6).

### 4.7 Instrument

After L6, Open DARE's `Obligation` is a subclass of `ins:Obligation`, and bound statements use
`ins:obligor`/`ins:obligee` to role occupancies. Open DARE does not use `ins:inProvision` for
attaching meaning: it is functional, so one obligation could not be expressed by two wording
variants, which the CBAA needs (M9 9.2.8A and B). Attachment stays with Open DARE's `expresses`
(design-spec §3.4). L12 raises this upstream.

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
    Obligation ⊑ ins:Obligation                              (after L6)

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

**Hierarchy classes.** For each concept c on a hierarchical dimension R, under a pinned
edition, generate a primitive class Within_R(c), "valued at c or below", with the SKOS hierarchy
compiled into subsumption:

    ∃R.{c} ⊑ Within_R(c)                  for every concept c
    Within_R(d) ⊑ Within_R(c)             for every d with d skos:broader c
    Within_R(c) ⊓ Within_R(c′) ⊑ ⊥        for siblings c and c′, only where the scheme is
                                          declared a partition and R is functional

All three forms are in OWL 2 EL. This is where subsumption-aware matching (design-spec §4.4)
enters the T-Box. Without the partition declaration, the checks below err towards reporting an
overlap or an expansion, never towards missing one.

**Envelope classes.** For each bound authority grant g, one class over the static dimensions
(modes A and Q only, DP6). For a grant covering insurance, risks in France except Corsica, and
sums insured up to GBP 5,000,000:

    Env_g ≡ Case
            ⊓ ∃contractType.{Insurance}
            ⊓ Within_riskLocation(France) ⊓ ¬Within_riskLocation(Corsica)
            ⊓ ∃sumInsured_GBP.xsd:decimal[≤ 5000000]

Amounts in different currencies are separate dimensions. Cross-currency comparison needs a rate
and is decided outside DL (`Undetermined` without a conversion context).

**Checks the reasoner answers.** No A-Box is involved, so the open world does not distort the
answers:

| Question | DL task | CBAA use |
|---|---|---|
| Did an amendment expand authority? | Env_g′ ⋢ Env_g, for g′ the amended grant | materiality (M3 3.9.1) |
| Does a segment authorise anything? | satisfiability of Env_g | envelope sanity |
| Do two segments overlap? | satisfiability of Env_g ⊓ Env_h | overlapping remuneration or claims arrangements |
| Are a slot's inclusion conditions exclusive? | satisfiability of Cond_i ⊓ Cond_j | variation slots |
| Do an obligation and a prohibition clash? | satisfiability of Scope_o ⊓ Scope_p for the same bearer and activity | norm conflicts (M14 14.19 vs 14.23.1) |

### 5.7 Not in DL

Aggregates over populations, arithmetic, cross-currency comparison, time arithmetic in business
days, precedence resolution, scheme-binding resolution, completeness and value exclusivity.
These are SHACL, SPARQL or compiled evaluators, each with PROV-O provenance.

## 6. Compilation Toolchain

### 6.1 What LATTICE provides

| Component | Input | Output | Provenance |
|---|---|---|---|
| `tools/mork_compilers` | `elg:IntervalCondition` declarations | a shared IR (`IntervalPlan`), then SPARQL `mork:QueryTemplate`, SHACL shapes (readiness and containment), structured SWRL | `exe:ExecutablePlan`, `exe:producesArtefact`, `exe:derivedFrom…Node` |
| `tools/surface` | `srf:IndexContract`, `srf:PromotionContract`, `srf:ProjectionContract`, `srf:SurfaceProfile` | generated symbols (nominal classes, memberships, closure relations, promoted properties), and lowering of projections into MORK | `srf:GeneratedSurface`, `srf:ReadSetEntry` with content hashes, `srf:LawDischarge` |
| MORK ontology | mapping graph | `mork:GenerativeMapping` kinds (projection, rule, shape, transform), `mork:OwlAxiom`/`mork:OwlClass` for T-Box generation, intent nodes, uncertain mappings | generative mappings are `fnd:Version` and `fnd:Governable` |
| `tools/persistence` | `dal:` profiles | SPARQL operation templates, identity-minting recipes | compiled profile records |

Current limits of `mork_compilers`: only interval containment is compiled. Set membership,
hierarchical match, exclusion and profile-level aggregation are not, and there is no OWL-class
backend.

### 6.2 Open DARE's compiled forms

| Compiled form (design-spec §6.5) | Route | Reuse |
|---|---|---|
| Runtime envelope table | Surface `IndexContract` with `ClosureRelation` over `skos:broader` and a `ContractBoundPopulation` per hierarchical dimension. `PromotionContract` flattens grant parameters. A `ProjectionContract` (`JoinProjection`) assembles rows, lowered to MORK, compiled to SPARQL | full |
| SHACL validation of bordereau rows | `mork_compilers` shared IR and SHACL backend over the grant's Eligibility conditions | IR and backend, extended by L10 |
| Envelope and hierarchy classes (§5.6) | the same shared IR with a new OWL backend, emitting `mork:OwlClass` nodes under a `mork:GenerativeMapping` | IR, extended by L10 |

Routing all three through one IR gives one reading of a grant's conditions. The lookup table,
the shapes and the classes cannot then disagree about what a grant means, which is the reason
LATTICE introduced the shared IR (ADR-A24).

### 6.3 A data-driven pipeline

Every compilation is declared in the graph before it runs:

| Element | Declared as |
|---|---|
| What to compile | a Surface contract or a MORK mapping, authored in an Open DARE compilation module |
| Order | `mork:dependsOnMapping`, a declared DAG |
| How | an `srf:SurfaceProfile`: generator version, canonicalisation version, entailment regime, naming. A profile change is a new profile version and a full regeneration |
| What was read | `srf:ReadSetEntry` per input, with its content hash |
| What was produced | `srf:DerivedArtefact` records and `exe:` plans |
| What was proven | `srf:LawDischarge` for runtime-conformance laws |

The same staleness rule then covers every artefact and our LATTICE imports (§3.3): stale when
any recorded read hash differs from the current one.

**Uniform provenance.** Surface, Executable and MORK each carry their own provenance terms and
none is aligned with PROV-O, which Open DARE adopted (D5). L8 proposes the alignment
(`srf:DerivedArtefact ⊑ prov:Entity`, a generation run as `prov:Activity`,
`exe:derivedFrom…Node ⊑ prov:wasDerivedFrom`). One query then answers "where did this come from"
across meaning extraction, compilation and runtime decisions.

**Meaning extraction.** MORK's uncertain mappings, hypotheses and intent nodes are a ready
home for meanings proposed by LLM extraction and later validated (AP4). Open DARE records only
the provenance link. Assurance of the extraction stays out of scope.

## 7. Persistence

### 7.1 What it is for

Persistence declares data-access behaviour: aggregate boundaries, concurrency, ordering,
receipts, uniqueness, identity minting, epoch and privacy. Contract behaviour (obligations,
lifecycles) belongs to Behaviour and SPC. So Persistence is where Open DARE states its
data-access expectations (design-spec §8). Contract behaviour is declared elsewhere.

### 7.2 Profile module

An Open DARE profile module declares `dal:` individuals that target Open DARE classes by IRI.
Persistence imports nothing and is imported by nothing, so no Open DARE ontology depends on it.

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

| # | Layer | Change | Blocks |
|---|---|---|---|
| L1 | Quantification | widen `qnt:unresolvedReason`'s domain so `UnresolvedValue` is satisfiable | referral on unresolved values |
| L2 | Quantification | derived rate values (a percentage of a base) | remuneration (M6) |
| L3a | Vocabulary | scoped, time-bounded binding | **done** at `65ac4a8` |
| L3b | Quantification | calendar binding for business-day extents | deadlines in business days |
| L4 | Foundation | derived-artefact contract. Surface's `srf:DerivedArtefact` now serves, so this lowers to lifting it into Foundation | nothing for Open DARE |
| L5 | Quantification | one bound stated in several currencies | M5 SoUA equivalents |
| L6 | Instrument | remove `ins:Element` from the disjointness axiom that makes its subclasses unsatisfiable | importing Instrument and Behaviour |
| L7 | Eligibility | an exclusion construct, e.g. an excluded set on a condition or a none-matching operation | authority scopes |
| L8 | Surface, Executable, MORK | PROV-O alignment of derived records and plans | uniform provenance |
| L9 | Surface, Eligibility | honour `voc:SchemeBinding` where they read `voc:boundScheme` | market-scoped vocabularies at compile time |
| L10 | `mork_compilers` | set membership, hierarchical match, exclusion, profile aggregation, OWL backend | compiled forms 2 and 3 (§6.2) |
| L11 | all | advance `owl:versionIRI` on content change and tag releases | using versionIRI as a content pin |
| L12 | Instrument | `ins:inProvision` is functional, so one obligation cannot be expressed by several provisions | aligning attachment with Instrument |

## 9. Sequencing

1. Upstream L6, L1 and L11, which are small.
2. Add the submodule, catalog and lock record, import Foundation, Vocabulary, Quantification and
   Party, and run the gate.
3. Apply the reclassification (design-spec §11), with schemes as `voc:ConceptScheme` editions
   and properties bound by `voc:SchemeContract`.
4. Add the meaning module (statement kinds, §5.5) on Party, Eligibility and Instrument.
5. Add the compilation module (Surface contracts, profile) and the Persistence profile module.
6. Declare the lifecycles on Behaviour (M12, M3, referral, FNOL, complaints).

Step 3 waits for step 2 because the reclassified schemes are `voc:` individuals.

## 10. Open Questions

| # | Question | Recommendation |
|---|---|---|
| I1 | Submodule path and catalog location | `imports/lattice`, `ontology/catalog-v001.xml` (§3.3) |
| I2 | Import Instrument and Behaviour before L6 lands | no, wait for L6 |
| I3 | Agreement version boundary: named graph, or a composite boundary walking a shape over `directlyComprises` | named graph for accepted, immutable versions |
| I4 | Envelope classes from an extended `mork_compilers` IR, or a new Surface backend | extend the IR (§6.2) |
