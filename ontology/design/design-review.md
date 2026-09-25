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
