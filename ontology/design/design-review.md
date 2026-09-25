# LATTICE Design Review

Status: closed 2026-09-25. Outcome recorded as D12 in the
[design specification](design-spec.md#12-decision-log). The first review is kept as written.
The [reassessment](#reassessment) weighs it against later context and upstream evidence.

## First Review

**Assessment**

I would adopt some parts of LATTICE as Open DARE’s imported substrate today, but retain others as a design reference and future interoperability target.

It brings real value: scheme contracts, roles, versioning patterns, quantification vocabulary, and the idea of compiling one meaning into several projections are all useful. Scoped, time-bounded vocabulary binding is a concrete improvement.

But the current adoption claim is too strong:

- The proposed compiler reuse is largely prospective. The key authority features need upstream additions for exclusions, hierarchical matching, aggregation, SHACL support, and an OWL backend. “Full” reuse in `lattice-integration.md:350` is not supported by its own limitations.
- Core dependencies have known logical defects, and Open DARE requires further upstream changes before it can import several layers. This makes Open DARE’s core design contingent on another pre-1.0 project.
- LATTICE gives generic mechanism, not the decisive domain semantics. Statements, wording bindings, authority envelopes, market vocabulary, materiality, and clause semantics remain Open DARE work.
- Exact pins improve reproducibility, but do not reduce the cost of upgrading a dependency whose every pre-1.0 update must be treated as breaking.

**Recommendation**

Replace D7’s “LATTICE is imported” position with: Open DARE is *LATTICE-informed and LATTICE-compatible*, but normatively independent. Build Open DARE’s small semantic core directly on OWL, SKOS, SHACL, and PROV-O. Keep optional alignment modules to LATTICE terms.

A LATTICE layer should only become a direct import after a layer-specific acceptance gate shows that it:

1. Covers a required Open DARE capability without a local workaround.
2. Has no blocking semantic defects.
3. Has a stable, offline-resolvable release.
4. Reduces total maintenance more than it adds.

I would not import Surface, MORK/Executable, Persistence, or Behaviour at this stage. Their toolchain and implementation implications are premature under AP1. Vocabulary and Quantification are the strongest candidates, but should still pass the same gate independently.

## Reassessment

### Context

The first review weighted LATTICE's pre-1.0 churn as the main risk. Two facts change that
weighting. LATTICE and Open DARE have one maintainer, and Open DARE is LATTICE's first
consumer, so upstream responds to Open DARE's requirements directly. Both are developed by
agents under human governance of architectural decisions, so an Open DARE feature needing an
upstream change can be delivered, pinned and versioned across both repositories in one session.

### Evidence

Between the design specification's baseline (`558650b`) and `f55c7d2`, seven of the thirteen
upstream items raised during the design work were closed (L1, L3a, L4, L6–L9). L10 was closed
except for its OWL backend, L11 except for ratification and CI enforcement, and ADRs were
drafted for the other four (L2, L3b, L5, L12). The changes were generalised with non-domain worked
examples (clinical trials, lending, employment), so LATTICE took in no insurance semantics,
which keeps both sides within AP2. Status per item is in the integration specification's
[§8](lattice-integration.md#8-upstream-changes). HermiT classifies the current core closure with
no unsatisfiable classes, and a mutation probe confirms the check detects the earlier defect.

### Points of the first review

| Point | Now |
|---|---|
| Compiler reuse is largely prospective | Concept conditions, exclusions and profile aggregation compile to SPARQL, SHACL and SWRL. Only the OWL backend is prospective (L10) |
| Core dependencies have known logical defects | Fixed |
| Dependence on a pre-1.0 project | Churn risk is lower than stated. Upgrade cost remains: in one day MINOR bumps cascaded through 12 and then 17 documents. Moving the pin at milestones limits it |
| LATTICE gives mechanism, not domain semantics | True of every option, so it does not discriminate between them |
| Surface, MORK, Executable, Persistence, Behaviour are premature under AP1 | D6 permits tools that produce and check the specifications, which covers compilation to shapes and classes. Persistence is adopted as declarations only, with code generation deferred. Behaviour is importable since L6 |

The first review's alternative, building a small core directly on OWL, SKOS, SHACL and PROV-O,
would reproduce Quantification, Vocabulary and Eligibility (design-spec §5.2). Its
independence argument assumes a dependency governed by someone else, which does not hold here.

### Remaining risks

- **Ratification lags delivery.** ADR-A86, on which the pinning design relies, is implemented
  but still Proposed. In `0742073` an agent read a line in a plan as the human's ratification.
  A status record reported committed work as uncommitted. LATTICE's checks run only locally,
  since both workflows are manual-only.
- **External adoption.** A market-facing specification that depends on a single-maintainer
  framework is harder for third parties to adopt. This weighs less while the repository is
  educational. The import closure is plain OWL, and LATTICE's tools are needed only for
  compilation.
- **Design pull.** Since upstream changes on request, Open DARE's design may drift towards what
  is convenient to add there. Each upstream request should trace to a CBAA requirement.

### Outcome

D7 stands. Normative independence is not adopted. The first review's layer gate is kept but
reframed around assurance rather than release stability: resolution, classification,
ratification, automation and conformance (integration spec
[§3.3](lattice-integration.md#33-recommendation), D12).
