# Clarifying Design Details

Let's work through some of the design choices then.

You mention (for `Authority`) that items are "held as data, compiled three ways: runtime lookup tables, per-agreement OWL 2 DL classes for design-time checks, and SHACL shapes. Evaluation modes are adapted from MERIDIAN. Lifecycle state never enters envelope comparison"

I am assuming "held as data" means instantiated in the A-box, so this actually become a compilation tool-chain we can re-use across multiple strata: convert to lookup, create DL classes (for reasoning), generate SHACL. Since `lattice` adds SWRL and SPARQL compilation upstream in its toolchain for `eligibility`, I'd like you to review the implementation and look for re-use opportunities. 

## Compiler Use

Since we are defining compilation pipelines for data, to what extent is the pipeline itself data-driven? For example, `lattice` has a `surface` projection mechanism that re-uses its `mork` ontology to define mapping rules as graph nodes. There is a lot to be said for uniform provenance across a tool-chain. Please explore.

Question: will we leverage `persistence` to define our behavioural expecations? And if so, any of its code (e.g., SPARQL) compiler chain? Note that the IRI handling for `persistence` is mid-work-package right now, but we could - if there is value - adopt the configuration vocabulary for the time being, and leverage the code-gen at a later date.

## Decisions Needed

1. Let's allow for the code in `tools` for now. You may lighten the principle to reflect this: we wish to complete the ontological design first, before we attempt to build a reference implementation.

2. Import Lattice: yes, but let's think about how we will incorporate it into the repository. There is no package management system to assist us with this, so will we leverage git submodules or use some other approach? 

3. The remaining decisions:

- adopt the statement kinds (yes)
- apply the reclassification of the current ontology described in §11 (yes)
- patch scoped vocabulary binding upstream: (this has been done upstream)
- copy the principles into .github/copilot-instructions.md (yes)

Please proceed with a design spec for incorporating `lattice`. I not only want to understand how you'll integrate the repo (or better, depend upon subfolders in it that contain the ontologies somehow), but how you are going to leverage the T-Box/Assertions in its ontology layers. Please ensure the design explains the DL encoding we are going for. (Please avoid using latex when generating any logical expressions by the way - stick to unicode instead)
