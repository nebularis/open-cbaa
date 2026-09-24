# CBAA Spec Observations (M1–M8)

Working notes supporting the design review in [ontology/README.md](../ontology/README.md#design-review-cbaa-modules-m1m8). Sources are the drafts in `.copilot/` (git-ignored), so this file paraphrases and cites clause numbers rather than quoting.

## Reading the source files

The XML files are Word packages (Flat OPC, one in WordML 2003). Semantics are carried by formatting, so extraction must keep it:

| Formatting | Meaning |
|---|---|
| red run | embedded variable |
| blue run | referenced object |
| highlighted letter after a clause number | variation (A/B/C) |
| grey text (`808080`) | optional or conditional clause |
| Word comment on a clause number | inclusion condition, guidance, drafting notes |
| endnote on a variable | variable id (e.g. `6.11`), name, population method |

The `.xlsx` table files use a namespace variant that `openpyxl` cannot load, so they need parsing from the raw sheet XML.

## Optionality and conditions

- Four inclusion modes: mandatory, variation (exactly one of A/B/C per slot), optional (Contract Creator's choice), conditional (included when a condition holds). Variations nest (M1 1.4A.2.2A/B inside 1.4A).
- Conditions are propositions over agreement facts. Examples:
  - counts: number of Coverholder entities (M1 1.4A/B/C), more than one insurer (M1 1.19), trading locations 1..n (M1 1.4A.2.2.x)
  - parties present: broker engaged (M1 1.20, M3 3.19.1.1)
  - capacity: Lloyd's, Lloyd's Europe (LIC), company market (M5 5.1.x.xA/B)
  - territory and class: risk or policyholder location includes Texas and contract type includes insurance (M5 5.15.12)
  - agreement type: fixed term or continuous, period over 3 years (M2 2.2A/B, 2.9)
  - lifecycle state: the amendment acceptance section appears only after a first amendment (M2 2.6–2.8)
- M5 comments write conditions against numbered governing variables: GOV 3 likely subscribing market, GOV 4 contract type, GOV 7/8 risk location country and sub-division, GOV 20/21 policyholder location, GOV 79–81 insurable interest.
- Some variations are auto-selected from facts (M4 4.3.36 A–D, US classification). Others are user choice.
- Drafters flag conditions they cannot see how to digitise, e.g. the Coverholder's surplus lines licence status (M4 4.3.23–4.3.24 comments).

## Variables

- Variables have stable ids scoped by module (`6.11` Producing Intermediary Name), and one variable is displayed in several clauses.
- Population methods seen: free entry, pick list (currencies are ISO codes), lookup from a reference table (Coverholder details), auto-populated from the Insurer Capacity Table, pulled from the digital signature process (M2 acceptance dates), derived by rule (M5 5.1.2.1.1).
- Some variables hold the comparison operator ("equal to" vs "not exceeding", M6 6.1B), so a clause plus its variables is a parametric constraint.
- Composite values (addresses) and repeating values (trading locations, tax types) occur.

## Structure

- Explicit object ids: `CGnn` component group, `Cnn.X` component, `SCnn.X.Y` sub-component (M5, M6, M8).
- Numbering in Word is for reference only. Instance numbering is dynamic.
- A numbered clause is a text object. Text objects group into components or sub-components and contain variables and references inline (cbaa.md).
- Two referenced object types: Table Objects (fully reportable) and Document Objects (annex or instructions, PDF, not digitised). References also point to modules and named components (M1 1.2.2, M3 3.4).
- Three Guidance Object types: Defined Terms, Technical Guidance, System Guidance (cbaa.md).

## Tables

- M5 base tables define every possible row, each marked Mandatory, Optional, Conditional or Mandatory Hidden, with a text fragment used to render the row as prose.
- Columns are Agreement Segments. A segment is the unit to which limits, remuneration (M6 6.1D) and claims arrangements (M8) attach.
- An agreement can have several Territory and SoUA tables. Territory rows include and exclude at country, sub-division, county and city level.
- Reference lists: insurable interest hierarchy (group, sub-group, type, grain), perils, claims basis, sum insured basis (CDR values, known to need amending), pool schemes, policyholder classification, Coverholder level of authority.
- GWP income limits apply across all policies bound, per table or per agreement, with a notification trigger percentage.

## Parties and roles

- Coverholder (one or more legal entities, trading names, locations), Insurers (Lead, Follow, platform Lloyd's / Lloyd's Europe / company market), Broker, Producing Intermediary, Regulatory Body.
- Insurer Capacity Table rows: placement role, shares and bases, amendment role, claims role, basis of claims agreement.
- Claims roles: FNOL Handling Party, Claims Determination & Settlement Party, Claims Agreement Parties, DCA, Loss Adjuster, Claims Assistance Company (M8).
- Lloyd's annual transfer: insurer parties change each year of account while the Agreement continues (M2 2.9).

## Lifecycle, amendment, identity

- Acceptance by insurers and coverholders is recorded per version (M2 2.3–2.8).
- Replacing a Coverholder legal entity or the Lead Insurer, or a change of broker number, is not an amendment. It requires a new Agreement (M3 3.2.1, 3.9.1.16 guidance).
- Required approvers depend on each insurer's amendment role (all, material only, capacity follow) and on whether the change touches objects designated material (M3 3.7, 3.9). Materiality thresholds are variables (M3 3.9.1.1B).
- Amendments carry agreed date, effective date (immediate, prospective or retrospective), and may need operational implementation before legal effect (M3 3.20–3.22).
- Exceptional amendments run outside the digital process and are re-incorporated later. The electronic version is the definitive record (M3 3.19.4).

## Obligations and events

- Deontic content throughout: must, must not, may, has the right, with bearer and counterparty.
- Deadlines tied to events: FNOL onward transfer within N business days (M8 8.1.2A), notify without undue delay (M1 1.11), filings N days before first binding (M4 4.3.22).

## Provenance and regulation

- Many M4 and M5 clauses derive from Lloyd's Crystal+, PBQA checks and market bulletins, and comments note mismatches between those sources.
- Clauses are to carry jurisdiction tags (US, Texas, New York State, South Africa) for later filtering.
- Several clauses originate in existing LMA wordings (LMA5032a, LMA5034A, LMA 5312B).
