# Vision and Proof of Value

Status: ideation, 2026-09-25. 

A vision for Open CBAA  and a demonstration that would show the market what the model makes possible.

## 1. Thesis

Today a binding authority agreement is a document. Every party that must act on it might potentially re-encode its rules, depending on how those parties are attempting to digitise their business today. The might include, for example, MGA oversight, coverholder binding platforms, bordereau validation rules, audit checklists, claims handler's authority matrices, and so on and so forth.

Each encoding risk drift from the wording and from the other encodings, making it extremely difficult to show which clause a given check came from. The CBAA makes the wording structured. Open CBAA makes it **mean** something: meaning is attached once to each library wording object (design-spec §3.4), bound per agreement from its variables, and compiled into every operational form from one intermediate representation (integration spec §6.2). 

> The agreement is the rulebook. Write it once, and every check, referral and report comes from
> it, and cites it.

## 2. Historical Mechanisms & Current Arts

Blueprint Two and the Core Data Record (CDR) are the reference points today.

| Current approach | Opportunity arising from an ontological foundation |
|---|---|
| The CDR standardises the **data exchanged**, what fields exist and their formats, not the **rules** that govern them. Participants still interpret and re-implement the rules | the rules themselves are data, derived from the contract |
| Validation checks structure (is the field present, well formed), not contract (is this risk within this binder) | contractual validation, with the clause that failed |
| The cost falls on the participants who capture the data, while the benefits accrue to central processing (tax, regulatory reporting, settlement) | value for the coverholder and the managing agent on day one |
| Built around open-market placement. Delegated authority stays on monthly bordereaux, where out-of-authority business is found weeks or months after binding | authority checked at the point of bind, and bordereaux as confirmation rather than discovery |

A demo must show semantics doing work that a data standard cannot.

## 3. Define or interact?

**Interact, with the definition visible behind it.**

- Authoring, meaning assembling a CBAA from the Wording Objects Library, is already the contract
  builders' ground (PPL, Whitespace, Ecliptic). An authoring demo competes with them and shows
  the least that is new.
- The pain in delegated authority is operational: referrals, out-of-authority discovery, bordereau
  quality, amendments, audits. That is where semantics pays.
- The moment that impresses is causal: **change a word in the agreement and watch operations
  change**, with every consequence traced back to the wording.

This positions Open CBAA as a meaning layer that contract builders and the WOL can consume, not
a competitor to them. Model A and Model B of the programme differ in where instances travel. Both need to know what an instance means.

## 4. Capabilities worth showing

Each is something the model already specifies. The last column says where.

| Pain point | Today | With the model | Where |
|---|---|---|---|
| Out-of-authority risks found late | bordereau review, weeks after binding | checked at bind against the agreement version in force | envelopes, modes A and Q (design-spec §6.3) |
| Binary pass/fail hides missing data | a missing field fails, or silently passes | three outcomes. `Undetermined` becomes a referral carrying its reason: missing value, a location only known at a level above an exclusion ("France", where Corsica is excluded), no limit in the case's currency | ADR-A87 decision table, `exe:Diagnostic` |
| Territory rules are nested and regulatory | include and exclude rows at every level, groupings such as "Europe A" that include French Guiana and Réunion | hierarchy-aware matching over a pinned, versioned territory scheme, with exclusions | design-spec §4, §6.2 |
| Is this endorsement a material change? | a person reads the endorsement | a reasoner proves whether the amended authority is contained in the old one. Expansion needs approval (M3 3.9.1), restriction does not | design-time classes (integration spec §5.6) |
| Overlapping arrangements | discovered in a dispute | segments whose scopes overlap, found before binding: two remuneration arrangements, two claims arrangements | overlap check, satisfiability of Env_g ⊓ Env_h |
| Limits in several currencies | ad hoc conversion, or none | each currency's limit read in its own unit, no silent conversion, `Undetermined` when a rate would be needed | ADR-A95 |
| Aggregate limits | tracked in spreadsheets | an accumulator per agreement, segment and period. The notification threshold (M5 SoUA row 47) is an event | design-spec §6.4 |
| "What did the binder allow on the day?" | reconstruct from document versions and emails | agreement versions and vocabulary editions are both time-scoped, so any past decision can be replayed exactly | design-spec §4.2, §8.5 |
| Why was this risk accepted? | audit sampling | every decision traces to its compiled artefact, the grant, the wording object version and the vocabulary edition, in PROV-O. The audit question becomes a query | design-spec §9, ADR-A92 |
| Deadlines scattered through the wording | diaries and reminders | obligations with triggers and deadlines, in business days where the wording says so, become a ledger of what is due, from whom, by when | statement kinds (§3.3), ADR-A94 |
| Every system re-implements the binder | N encodings that drift | one source, several compiled forms (bind-time table, bordereau shapes, design-time classes) that cannot disagree, because they share one intermediate representation | integration spec §6.2 |
| One wording across markets | separate wordings per market | market-scoped vocabulary bindings, so Lloyd's risk codes apply only in the Lloyd's scope, and the same agreement serves company, Lloyd's and mixed binders | ADR-A85, design-spec §4.2 |

Three of these carry the demo, because no data standard can do them:

1. **Materiality by proof.** "Is this amendment an expansion of authority?" answered by a
   reasoner, with the dimension that grew.
2. **Undetermined with a reason.** Referrals that say exactly what is missing and which clause
   needs it.
3. **The golden thread.** From any decision back to the words that caused it, at the version
   and on the date that applied.

## 5. The demo: a binder's year in fifteen minutes

One agreement, using the published M5 examples (the SoUA and territory example tables) with
two insurers and a broker.

| Act | Time | What happens | What it proves |
|---|---|---|---|
| 1. Assemble | 2 min | Set a few governing variables: subscribing market, contract type, risk locations. Clauses appear or drop out (surplus lines wording appears once US risks are authorised). Open one SoUA row and show the authority grant attached to it | the contract is assembled from meaning-bearing objects, and the rules come with it |
| 2. Bind | 4 min | The coverholder quotes three risks: one inside authority, one in Corsica, one located only as "France". Then one priced in a currency with no stated limit | `Permitted`, `Denied` citing the exclusion row, `Undetermined` with a referral reason, `Undetermined` for no limit in that currency |
| 3. Report | 3 min | Load a month's bordereau spreadsheet. Rows are validated against the compiled shapes. The accumulator moves towards the GWP limit and crosses the notification threshold | contractual validation of bordereaux, with clause citations, and aggregate limits as live state |
| 4. Amend | 3 min | Draft an endorsement: add Belgium, lower one limit, remove one peril. The reasoner reports an expansion (Belgium), so managing agent approval is required. Downstream artefacts regenerate. Risks bound before the effective date are still judged by the version in force when they were bound | materiality by proof, and no retrospective surprises |
| 5. Audit | 2 min | Pick one bound risk and ask why it was accepted | the provenance chain, from decision to wording object version, vocabulary edition and scheme binding |
| 6. Obligations (optional) | 2 min | The agreement's obligations as a ledger: FNOL onward transfer within one business day (M8), monthly reporting within 15 days of period end (M10) | the contract as a schedule of duties, not only a scope |

The strongest single moment is act 4. Rehearse it first.

### Minimum slice

Acts 2, 4 and 5 over M5 alone make a complete proof. They need:

- plan steps 2 to 5 (integration spec §9), restricted to M5: the LATTICE imports, the reclassified
  territory, insurable interest and peril schemes, `AuthorityGrant` statements on the SoUA
  wording, and the compilation module
- I7 settled: the case is the risk, whose deemed location is single-valued
- I9 settled for the territory scheme, so sibling territories can be declared disjoint where the
  scheme is a tree

Act 1 needs inclusion conditions (design-spec §3.6) and I8. Act 3 needs accumulators. Act 6 needs
the Behaviour lifecycles (plan step 6).

## 6. Measures of value

A proof of value should report numbers, not impressions. Candidates:

- time from binding to discovery of an out-of-authority risk: at bind, against weeks today
- share of referrals that carry a machine-readable reason
- number of independent encodings of the binder's rules: one, against one per system
- amendment review: which changes needed a human reading, against which were proved
- audit: sample questions answered by query, with the provenance returned

## 7. Tensions and open questions

| # | Question | Notes |
|---|---|---|
| V1 | AP1 says no reference implementation before the ontological design is complete. A demo is executable | options: build the demo only from D6-permitted tools (compilers, validators, queries in a notebook), or record an AP1 exception scoped to a demo outside `ontology/` |
| V2 | Audience first: managing agents' oversight teams, coverholders, the LMA's CBAA Steer, or the contract builders | the acts are the same, the emphasis differs. Oversight teams care about acts 3 to 5, coverholders about act 2, the LMA about the whole thread |
| V3 | Use of LMA material | the drafts are shared for education. A public demo may need the LMA's agreement or synthetic wording |
| V4 | The Blueprint Two and CDR comparison | verify §2 against current market sources before stating it to a market audience |
| V5 | Bordereau format | Lloyd's coverholder reporting standards define the rows. The demo needs a mapping from one real layout, which is where MORK's validated mappings apply |

## 8. Suggested next step

Settle V1 and V2, then treat the minimum slice (§5) as the acceptance test for plan steps 2 to 5:
each step is done when it moves the M5 slice one act closer to running.
