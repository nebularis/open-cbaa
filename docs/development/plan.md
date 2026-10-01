## Questions
### 1. Can the OWL backend handle multi-valued claims?

Half right. OWL itself can express several values: "every value" is `∀path.F ⊓ ∃path.⊤`, and "some value" is `∃path.F`. The limit is in Eligibility's decision table:
- the SPARQL reference returns `Undetermined` (`exe:SeveralCandidates`) for a subject with several values;
- the OWL classes must agree with it, so option B refuses unclaimed paths.

"One case per location" has a catch. An admission profile needs **all its conditions read from one subject class**, and `compile_profile` refuses a mix. So one case per location only works if every other dimension is also single-valued from that same case.

The CBAA helps here. M5 and M4 consistently say "policyholder or risk is **deemed** to be located in…". A deemed location is a single regulatory location per risk, and a separate one for the policyholder. So:
- **the case should be the risk**, not the policy;
- `riskLocation` and `policyholderLocation` are then two single-valued dimensions;
- a policy covering several risks gives several cases, which is what the regulation does anyway;
- paths such as risk → policy → policyholder location stay single-valued.

That leaves genuinely multi-valued dimensions such as perils or risk-code splits. For those there are two routes:
- **(a) a finer case**, for example one per risk section;
- **(b) an upstream ADR** adding a quantified reading to evidence bindings ("every value" or "some value"), with its decision table and OWL encoding.

I haven't yet checked which CBAA dimensions are truly multi-valued per risk. That's the first job for I7.

### 2. Is there a design decision in the §5.6 differences?

Only one, I9. The rest is text:
- The `Within(c)` encoding gives the same entailments as ours. Just a text update, now done.
- The "R functional" precondition is replaced by the single-valued claim. Also text, and folded into I7.
- **I9: where does "these siblings are mutually exclusive" come from?** Today it's a per-compilation option. The alternative is a declaration on the scheme edition in Vocabulary, which is ADR-A90's own open question. It's a fact about the scheme, which argues for Vocabulary. But that is an upstream change that cascades through every layer.
  - Disjointness is also refused for polyhierarchies. A territory scheme mixing countries with groupings like the EU or EEA would need its tree split from its groupings to use it.
  - Without disjointness, overlap checks can report overlaps that aren't real, but never miss one.

### 3. What happens if slot conditions and statement scopes are authored as `elg:AdmissionProfile`s?

**Gains:**
- They join the shared IR, so each scope gets SPARQL, SHACL, SWRL and OWL for free (D14 extends to them).
- Clash and exclusivity become `satisfiable(P ⊓ Q)` checks.
- There's one reading of a scope everywhere.

**Consequences:**
- **Scope versus modality.** A profile captures only *where* a statement applies, not its deontic kind. Pairing an obligation with a prohibition over the same bearer and activity stays an Open CBAA query. The reasoner answers only whether their scopes intersect.
- **The decision vocabulary means applicability.** Runtime outputs are `elg:EligibilityDecision` records with `Permitted`, `Denied` or `Undetermined`. For an obligation scope, "Permitted" would mean "applies". Harmless, but it has to be stated once in the design spec, or it will be misread.
- **The same constraints apply as for grants:**
  - one subject class per profile;
  - single-valued paths (I7 again);
  - only `AllRequired` and `AnySufficient`;
  - only interval, exact, set and hierarchical conditions.

  Mode S (state-dependent authority) can't be expressed. That fits DP6, which already keeps it outside envelopes.
- **Slot conditions read agreement parameters**, so their subject class is the agreement version, not the case. That's fine within one profile. A clash check between a grant scope (subject: the case) and a slot condition (subject: the agreement) doesn't make sense, and wouldn't be attempted.
- **No upstream change is needed.**

### 4. No waivers

Then the gate decides timing, and nothing is waived. The gate's own conditions attach to *uses*:
- L11 CI and L14 block the first import;
- L13 blocks only the step that first relies on Quantification comparison semantics, which is the compilation step, because interval conditions compare quantities.

## The plan

| Step | Where | Work | Needs |
|---|---|---|---|
| 1 | LATTICE | L11: the versioning and catalog checks run on push and pull request. The missing-version check covers consumer layouts. (L14 is superseded by the tag-based catalog, D16) | nothing |
| 2 | here | Submodule `imports/lattice` at the step-1 commit replaces the ignored symlink, for LATTICE's tooling. `ontology/catalog-v001.xml` already resolves LATTICE imports by release tag (D16). Version IRIs on our six documents (I5), all at `0.1.0` under `open-cbaa`. Import Foundation, Vocabulary and Party. Run the gate | step 1 |
| 3 | here | Reclassification (design-spec §11): schemes as `voc:ConceptScheme` editions, properties bound by `voc:SchemeContract` | step 2 |
| 4 | here | Meaning module: statement kinds, templates and bound statements, on Party, Eligibility and Instrument, with attachment per I6. Designed as the target of InsurLE compilation and LLM extraction (design-spec §3.7): parameters in Quantification terms, scopes as Eligibility profiles, and suggestion provenance expressible | step 3, I6, I8, I10 |
| 5 | LATTICE, then here | L13 upstream first. Then the compilation module (Surface contracts, profile), the Persistence profile module and the design-time classes | L13, I7, I9 |
| 6 | here | Lifecycles on Behaviour (M12, M3, referral, FNOL, complaints) | step 4 |

### Status (2026-09-26)

| Step | State |
|---|---|
| 1 | not started |
| 2 | the catalog (D16) and version IRIs are done. The ontologies import Foundation, Vocabulary, Quantification, Party, Eligibility, Instrument and Behaviour by release tag. The submodule and the gate run are not |
| 3 | done statically: `ontology/wim` 0.2.0 and the provisional schemes (D18) |
| 4 | done statically: `ontology/statement`, with `ontology/agreement` and `ontology/risk`, shapes and the worked example BA-2026-001. Proposed decisions D17 to D26 answer I6 to I8 for this step, pending ratification |
| 5 | not started. No compilation yet |
| 6 | M12 declared in agreement-vocab. M3, referral, FNOL and complaints remain |

[ontology/README.md](../../ontology/README.md) describes the result, and
`tools/ontology_check.py` validates it (HermiT, SHACL, 25 probes).

## Decisions

| # | Decision | Options | My recommendation | Blocks |
|---|---|---|---|---|
| I7 | Multi-valued dimensions | (a) the case is the risk, with finer cases where needed, (b) upstream "every/some value" readings | (a) now: the case is the risk, and location is its deemed location. Survey which dimensions remain multi-valued, and raise (b) only if some do | step 5 classes |
| I8 | Statement scopes and slot conditions as profiles | profiles, or our own classes | profiles, with "Permitted = applies" stated once | step 4 |
| I9 | Where sibling disjointness is declared | compile option, or a Vocabulary declaration | compile option, set in our compilation module per scheme. Split tree and groupings in the territory scheme | step 5 |
| I6 | Obligation attachment | as recommended in §10 | revised: not now (D23), since `ins:ProvisionShape` needs an `ins:Obligation` that library wording has only as a template | step 4 |
| I10 | Suggested meaning, held apart from accepted statements (design-spec §3.7) | MORK nodes, proposed statement instances, or an Open CBAA suggestion class. Which plane | ADR-A13's Mapping graph role as a staging graph: MORK nodes for templates, proposed instances for bespoke clauses, promoted on acceptance. The library plane holds only published versions | step 4 |
| I3 | Agreement version boundary | named graph, or composite boundary | named graph, as recommended | step 5 (Persistence) |
| L11 | Whether ontology IRIs move under `…/lattice/` | move now, or leave | leave. It's a LATTICE-wide MAJOR change with no need from us | nothing |
| I1 | Submodule path | `imports/lattice` | as recommended. A new top-level directory, so the README must document it | step 2 |

## Next Steps

Ratify or amend D17 to D26 (design-spec §12). Then the next concrete work is step 1 in LATTICE. That needs a LATTICE plan and ADR check under its own rules, and I'll draft it once you've answered I7 to I9. None of those block step 1, so we could start it now if you prefer.

## Upstream: LATTICE computable contract substrate (2026-09-30)

LATTICE proposes to take the general parts of this repository's wording and meaning upstream
([plan](https://github.com/nebularis/lattice/blob/main/docs/developer/plans/computable-contract-substrate.md),
[sketch](https://github.com/nebularis/lattice/blob/main/docs/developer/sketches/computable-contract-substrate.md)).
Nothing in `wim:` is specific to binding authorities, so it becomes a LATTICE Wording layer between
Eligibility and Instrument. Instrument is rewritten around terms and legal relations, taking
statement kinds, templates, parameter bindings and encoding status. Behaviour moves below
Instrument and gains relation occasions and records. L15 is fixed (LATTICE C10, merged
2026-10-01). LATTICE's plan §7 keeps the current list of what changes, and this section mirrors it
(updated 2026-10-01).

| Module | After migration |
|---|---|
| `wim` | removed. Its structure is LATTICE's Wording layer (ADR-A112, released as `wording` 0.1.0). The LMA WIM profile (the four levels as element types, containment rules as shapes, the LMA typing schemes and `applicableTo`) is in LATTICE's `applied/insurance/wording/` (CC-D3), and is imported here |
| `stm` | `AuthorityGrant ⊑ ins:Power` with its envelope mechanism. Other kinds, templates, parameter bindings and encoding status come from Instrument |
| `agr` | UMR, markets, CBAA roles. The M12 lifecycle becomes regimes from LATTICE's template library (CC-D8). Agreement versions become `ins:Instrument`s expressed in `wrd:AssembledWording`s |
| `rsk` | unchanged, with `rsk:BoundPolicy ⊑ ins:Instrument` and `rsk:boundUnder ⊑ ins:boundUnder` |
| BA-2026-001 | re-expressed, joined by renderings of the binding authority scenarios the LATTICE sketch catalogues from the CBAA modules and the IUA 09-069 agreement |

Effect on decisions here: D22 holds (only bound relations are evaluated). D23 is resolved, since
attachment becomes `ins:expressedIn` from a template term to a library element. D25 changes, since
an agreement version is no longer an `ins:Element`. I6 closes. L15 is fixed upstream. D19 is
replaced, and D21 moves upstream:

| Here | Upstream | Upstream decision |
|---|---|---|
| `wim:Segment`, `segmentIndex`, `segmentText` | `wrd:TextPart`, `partIndex`, `partText` | sketch §3.2 |
| D19: a variation slot outside the tree, its variants comprised by its parent | `wrd:VariationSlot`, an element ranked among its siblings with the shared object id ("1.4"), its variants beneath it, lettered only in the library form | C4-Q2. D19 recorded no rationale, and its slot could carry no rank. The LMA drafts number the position and letter the variants |
| D21: `agr:VariableValue` | `wrd:VariableValue` on an assembled wording, one per variable and per column for a table row's variable | C4-Q1, C4-Q3 |
| `stm:` templates and bound statements | stated meaning owned by a library element version, bound meaning owned by an instrument version | CC-D12 |
| an agreement as the subject of its own lifecycle state | a state occupancy for the instrument's persistent identity | ADR-A106 |

**Sectioned agreements (added 2026-09-30, revised by CC-D11).** A reviewed Lloyd's schedule defines
"the Coverholder", persons responsible, classes and locations per section. Upstream models a section
as a wording element of element type Section, placed by `ins:appliesWithin` and `ins:notWithin`,
each schedule column as an `ins:Definition` applying within its sections, and a case's section as
fixed by the section authority it was bound under. This is the design-spec §6.2 "agreement
segment" dimension, made first-class. Party identifiers such as the Coverholder PIN may move into
LATTICE Party (its CC-D9).

**Until LATTICE's slices C9 and C12 merge:** change `wim:`, `stm:` and `agr:` content only, not
their structure, so the migration maps a stable model.

