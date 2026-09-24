# Refining The Design

Our design is coming together. Let us agree upon some guidance before we continue.

## Architecture Principles

1. This repository shall remain purely a repository for our semantic specifications and shall contain no implementation code whatsoever
2. The ontological layers shall stand on their own, architecturally - the design of software built upon those layers shall governed by the architecture and design of the specifications
2. We shall assume a technology-neutral reference architecture until further notice
3. The approach to deducing the meaning of _wording_ in the contract shall be open-ended / Clauses shall express aspects of thier behaviour

The true meaning of (3) is that there are multiple approached on the table. A _governed_ subset of Enlish (a _Logical English_) has been proposed by [Cummins et al](https://www.researchgate.net/publication/388354297_Computable_Contracts_for_Insurance_Establishing_an_Insurance-Specific_Controlled_Natural_Language_-_InsurLE/link/6793bd6352b58d39f24c2f0e/download?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIn19), however this is not standardised yet. 

Another approach - the use of LLMs to extract proposed meanings from wording for human validation - is being explored currently. Along with InsureLE, this means that a computable fragment is available that has been parsed from (or infered via processing of) the text - the governance, assurance, and provenance of this is not our concern. The ontological implications of the model split are...

--- 

For now, we shall simply accept that **clauses have meaning attached to them**, though we do not know all the mechanisms by which that shall occur in the reference architecture. You did, in fact, say it yourself earlier: "a clause is a Grant of Authority clause if it expresses an authority grant".   

We might indeed generalise that to `Clause expresses (some owl:Thing)`, but what are the things that a clause can express? Do we want to model clauses themselves as different types of _thing_ - creating a fixed hierarchy of _Clause Types_ - or attach something to the clauses? Some more questions to consider:

- who defines the hierarchy?
- is the hierachy fixed and is it likely to remain so?
- does fixing it tie our implementation to WIM and leave us unable to handle other contract types? Do we want to be a general computable contract layer (like `lattice` is a general semantic framework) or are we going to be WIM specific? 
- if we choose specificity, ontological generality can be brought back into `lattice` anyway, but we need to pay heed to the consequences 
- does a runtime A-box have efficiency needs that our design has to consider? 

### Reference Architecture Sketch

Let us assume that a reference architecture will leverage a graph database backend, whether RDF or LPG or some other hybrid type. We can assume that this backend is not under extraordinary load - even during a disaster, claim volumes are unlikely to overload a production database - however we will need to define the concurrency, access, identity, and aggregation patterns our instance data will require.

[Subject-oriented Process Calculus](.copilot/Description\ Logic\ Encoding\ of\ Subject\ Process\ Calculus.docx) and its [reference architecture](https://raw.githubusercontent.com/nebularis/lattice/refs/heads/main/ontology/spc/docs/architecture.md) solve for this by ensuring that state machine transitions can only operate against a closed-world assumption. 

Sometime layers have different needs - capturing detail can be important for regulatory reasons, whilst eliding detail (and dropping structural facts by projection or re-materialisation) more appropriate for runtime efficiency.

Read the 3 `MERIDIAN` docs in `.copilot/` to get a feel for one approach to this modelling scenario. 

Read the [`lattice` RDF/SPARQL Operational Patterns Guide](https://github.com/nebularis/lattice/blob/main/docs/architecture/rdf-sparql-patterns-guide.md) please.

## Decisions 

### Which layers to build first. 

Whilst I agree that we need vocabulary, we haven't defined who owns it, how often it changes, whether it can be overridden, whether the length of the path that a graph traversal must take in order to process it matters at runtime in any layers or not... Let's work out how WIM needs to handle vocab first. Please refer to [lattice](https://github.com/nebularis/lattice) handling of plug-and-play vocab in the first instant.

Please carefully evaluate [lattice's quantification layer](https://github.com/nebularis/lattice) against our requirements. A proposed patch to that might save us a lot of work building from scratch, IF it's suitable as a starting point.

2. Whether to adopt the wording/meaning separation, with norms as their own layer.

Wording and meaning do need to be separated in terms of the ontological model, because even if at runtime we find a way around this, they is a conceptual distance between the legal text and the logical semantics. We need more concrete design before we 'cut code' on the ontolgies themselves I think.

3. Whether authority rules are held as data, compiled into per-agreement classes, or both.

My instinct is both, but let's add this to the concrete design spec we need.

4. SKOS or OWL class hierarchies for vocabularies, and which CDR and v5.2 releases are the source of truth.

Aluded to in (1), SKOS is the instinct - you can still achieve taxonomic hierarchies with `broader` and `narrower` and we can always write our own semantic extension of this... Whilst I do not insist on it being SKOS, my argument for data that is either (a) likely to change frequently, or (b) likely to be different for different users, use-cases, tenants, markets, etc - is to put things in the A-Box, not the T-Box, otherwise it's a fresh CI build every time.

5. Ordering of text within clauses: `rdf:List` or an explicit sequence index.

Modelling choices in the design spec please.

6. Whether to align with PROV-O and OWL-Time.

PROV-O, yes. Look at `lattice` again please, which aligns to PROV-O. Maybe the argument for building on `lattice` is growing, but it is under heavy development, so stability of the ontologies could be an issue - however, the main dev on it is your user, so you'd get priority changes in its repos while we do _this_ work.
