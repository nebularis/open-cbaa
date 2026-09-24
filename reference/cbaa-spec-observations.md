# CBAA Spec Observations (M1–M14)

Working notes supporting the design review in [ontology/README.md](../ontology/README.md#design-review-cbaa-modules-m1m14). Sources are the drafts in `.copilot/` (git-ignored), so this file paraphrases and cites clause numbers rather than quoting. Extract them with [tools/cbaa_extract.py](../tools/README.md).

## Coverage

| Module | Drafts available |
|---|---|
| M1 Introduction and General Principles | all variations, example |
| M2 Agreement Status | all variations, two examples |
| M3 Amendments | all variations |
| M4 Operational Responsibilities | all variations, Coverholder Responsibilities Table |
| M5 Scope of Underwriting Authority | all variations (docx), example, base and example tables |
| M6 Remuneration | all variations, two examples |
| M7 Evidence of Policies Bound | **not yet available** (referenced by M5, M9, M13, M14) |
| M8 Claims | all variations, variation and example sets |
| M9 Complaints | all variations, two examples, territory definitions and process table |
| M10 Reporting | all variations, Lineage example, Multiple Reporting Arrangements and DDM Roles tables |
| M11 Management of Monies | **not yet available** (referenced by M4, M6, M10, M12) |
| M12 Termination, Automatic Suspension and Non-Renewal | all variations, two examples |
| M13 Data Protection | all variations |
| M14 General Terms and Conditions | all variations |
| M15 Definitions | **not yet available** (named in cbaa.md) |

## Optionality and conditions

- Four inclusion modes: mandatory, variation (exactly one of A/B/C per slot), optional (Contract Creator's choice), conditional (included when a condition holds). Variations nest (M1 1.4A.2.2A/B inside 1.4A).
- Modes apply at every level: component groups (M9 CG09.1–CG09.3), components (M10 C10.3A/B), sub-components (M8 SC08.1.1/SC08.1.2, M9 SC09.1.1/SC09.1.2), clauses, and inline text (M12 title fragment "and Non-Renewal" is a variable whose options include empty).
- Conditions are propositions over agreement facts. Examples:
  - counts: number of Coverholder entities (M1 1.4A/B/C), more than one insurer (M1 1.19, M14 14.4), trading locations 1..n (M1 1.4A.2.2.x)
  - parties present: broker engaged (M1 1.20, M12 12.11.2)
  - capacity: Lloyd's, Lloyd's Europe (LIC), company market (M5 5.1.x.xA/B, M9 9.7.4, M14 14.48B.1)
  - territory and class: risk or policyholder location includes Texas and contract type includes insurance (M5 5.15.12)
  - territory groupings that are regulatory, not geographic: "Europe A" includes French Guiana and Réunion (M9 9.7.4 guidance), "any European country excluding UK" (M9 9.2.12), "Specific" vs "International" complaints territories (M9 C09.3)
  - agreement type: fixed term or continuous, period over 3 years (M2 2.2A/B, 2.9, M12 title)
  - party roles: Coverholder as data controller or processor (M13 13.2A/B)
  - lifecycle state: the amendment acceptance section appears only after a first amendment (M2 2.6–2.8)
- M5 comments write conditions against numbered governing variables: GOV 3 likely subscribing market, GOV 4 contract type, GOV 7/8 risk location country and sub-division, GOV 20/21 policyholder location, GOV 79–81 insurable interest.
- Slots depend on other slots: M10 10.4.1A–E determines the variants of 10.4.1.1–10.4.1.4 and 10.5.2.x.
- Some variations are auto-selected from facts (M4 4.3.36 A–D, M14 14.5A–C from Coverholder location). Others are user choice. Some governing facts come from questions put to the Contract Creator (M9 C1).
- Drafters flag conditions they cannot see how to digitise, e.g. the Coverholder's surplus lines licence status (M4 4.3.23–4.3.24 comments), and open questions about scope such as Coverholder location vs business written (M14 14.6.5, 14.6.6).

## Content keyed by governing variables

- M9 holds complaints wording as a matrix of territory × authority level (UK Full or Restricted, UK Restricted SRC, UK No, US, Canada, Australia, New Zealand, International, Europe, Italy, Spain). An instance includes only the cells for its authorised territories.
- Defined terms vary by jurisdiction: "Complaint", "Complainant" and "Redress" each have a UK, US, Australian and other definition (M9 table).

## Variables

- Stable ids scoped by module (`6.11` Producing Intermediary Name). One variable is displayed in several clauses, and some are populated from another module (M12 broker name from M1, M13 13.3 governing law from M14).
- Population methods seen: free entry, pick list (currencies are ISO codes, US states, Canadian provinces), lookup from a reference table (Coverholder details), auto-populated from the Insurer Capacity Table, pulled from the digital signature process (M2 acceptance dates), derived by rule (M5 5.1.2.1.1), defaulted from facts but overrideable within allowed values (M14 14.5).
- Constraints: minimum values (M10 10.3 retention at least 7 years, M13 13.2 breach notification at least 24 hours), maximum values (M3 3.9.1.1B at most 10%), cross-variable rules (M12 12.23.1 termination notice not less than the M5 advance binding period).
- Some variables hold the comparison operator ("equal to" vs "not exceeding", M6 6.1B), so a clause plus its variables is a parametric constraint.
- Value types: composite (addresses, amount with currency, duration with a business or calendar day basis), repeating (trading locations, tax types, sub-processors), multi-select (M10 10.2 data recipients), references to other clauses (M10 10.4.5A "10.4.1 and 10.4.2").

## Structure

- Explicit object ids: `CGnn` component group (nested groups `CGnn.X`), `Cnn.X` component, `SCnn.X.Y` sub-component (M5, M6, M8, M9, M10).
- Numbering in Word is for reference only. Instance numbering is dynamic.
- A numbered clause is a text object. Text objects group into components or sub-components and contain variables and references inline (cbaa.md).
- Two referenced object types: Table Objects (fully reportable) and Document Objects (annex or instructions, PDF, not digitised). References also point to modules and named components (M1 1.2.2, M3 3.4).
- Three Guidance Object types: Defined Terms, Technical Guidance, System Guidance (cbaa.md).

## Tables

- Base tables define every possible row, each marked Mandatory, Optional, Conditional or Mandatory Hidden, with a text fragment used to render the row as prose (M5 base tables, M10 Multiple Reporting Arrangements Table).
- Columns are Agreement Segments or reporting arrangements. A segment is the unit to which limits, remuneration (M6 6.1D), claims arrangements (M8) and reporting arrangements (M10) attach.
- An agreement can have several Territory and SoUA tables. Territory rows include and exclude at country, sub-division, county and city level.
- Reference lists: insurable interest hierarchy, perils, claims basis, sum insured basis (CDR values, known to need amending), pool schemes, policyholder classification, Coverholder level of authority, data transfer methods and frequencies (M10).
- GWP income limits apply across all policies bound, per table or per agreement, with a notification trigger percentage.
- Some tables are derived: the Full Policy Data Specification Table is generated from the authorised territories and insurable interests against the Lloyd's v5.2 data standard (M10 C9).

## Activities, authority and responsibility

- A recurring set of activities: quoting, binding, policy signing, policy administration, amending, extending, cancelling and replacing, renewing, servicing, FNOL handling, instructing claims professionals, claims determination and settlement, complaints handling, offering redress, reporting, data formatting, data transfer, management of monies, sub-delegation (M4 Coverholder Responsibilities Table, M8, M9, M10, M12, M14).
- Authority is granted per activity with a level and scope:
  - underwriting by segment, territory, insurable interest and limits (M5)
  - claims by activity and optionally segment (M8)
  - complaints by territory, with levels Full, Restricted (Prior Submit), Restricted (SRC), No, and a redress limit, optionally restricted to trading locations (M9 9.1)
  - sub-delegation by activity, with LIC party to contracts (M14 14.48)
  - use of capacity on co-insurance, line slips, other binders, consortia (M5 5.5–5.11)
- Responsibility per activity is assigned to named people (M4 Coverholder Responsibilities Table).

## Parties and roles

- Coverholder (one or more legal entities, trading names, locations), Insurers (Lead, Follow, platform Lloyd's / Lloyd's Europe / company market), Broker, Producing Intermediary, Regulatory Body, natural persons with named responsibilities.
- Insurer Capacity Table rows: placement role, shares and bases, amendment role, claims role, basis of claims agreement.
- Claims roles: FNOL Handling Party, Claims Determination & Settlement Party, Claims Agreement Parties, DCA, Loss Adjuster, Claims Assistance Company (M8).
- Reporting roles per segment and data stream: First Data Transfer Recipient, Data Formatter, Secondary Data Transfer Transferring Party, Error Communication Recipient (M10). DDM system roles per data stream: Contract Administrator, Submission, Transformation, Assignment, Approval.
- Data protection roles: Independent Data Controller, Data Controller, Data Processor, sub-processor (M13).
- Market bodies with specific roles: Lloyd's General Representative (Australia, Monaco, Germany), Attorney In Fact in Canada, LIC offices, Service Provider under an Outsourcing Agreement (M12 12.22.13).
- Lloyd's annual transfer: insurer parties change each year of account while the Agreement continues (M2 2.9).

## Lifecycle, amendment, identity

- Acceptance by insurers and coverholders is recorded per version (M2 2.3–2.8).
- Replacing a Coverholder legal entity or the Lead Insurer, or a change of broker number, is not an amendment. It requires a new Agreement (M3 3.2.1, 3.9.1.16 guidance, M12 12.17.1, 12.18.1).
- Required approvers depend on each insurer's amendment role (all, material only, capacity follow) and on whether the change touches objects designated material (M3 3.7, 3.9). Materiality thresholds are variables (M3 3.9.1.1B).
- Amendments carry agreed date, effective date (immediate, prospective or retrospective), and may need operational implementation before legal effect (M3 3.20–3.22).
- Exceptional amendments run outside the digital process and are re-incorporated later. The electronic version is the definitive record (M3 3.19.4).
- M12 specifies a state machine:
  - states: in effect, automatically suspended, termination notice period, non-renewal notice period, ended, run-off, with automatic extension when non-renewal notice is late (M12 12.37.2)
  - each state carries its own "NO authority to" and "authority to" lists over the activities above (M12 12.16, 12.24, 12.26, 12.39, 12.40)
  - transitions are automatic on events concerning any party (insolvency, loss of licence, 12.15), exercised powers (Right of Immediate Termination, 12.22), timers (breach not rectified within N business days, 12.22.2), or notices with a minimum period (12.23, 12.34)
  - run-off ends when every policy has expired or been transferred and every claim is resolved, capped at N years (12.X2, 12.28)
  - communications have deemed-receipt rules by channel (12.10)

## Obligations and events

- Deontic content throughout: must, must not, may, has the right, with bearer and counterparty. Rights to terminate are powers, distinct from permissions (M12 12.22).
- Deadlines tied to events: FNOL onward transfer within N business days (M8 8.1.2A), notify without undue delay (M1 1.11), personal data breach within 48 hours (M13 13.4.2), complaint files within 3 business days of request (M9 9.7.4.1), filings N days before first binding (M4 4.3.22).
- Recurring obligations: reporting monthly within N days after period end, with a no-activity notice (M10 10.4), annual resilience testing (M14 14.37.1), auto-renewal reports monthly until the Lead Insurer releases the obligation (M12 12.33.2).
- Survival: obligations outlive the Agreement until the last policy expires and the last claim is resolved (M14 14.49–14.50), or for a fixed period (M13 13.8).
- Registers with specified fields: complaints register (M9 9.8.2A/B).

## Provenance, regulation and external instruments

- Many M4 and M5 clauses derive from Lloyd's Crystal+, PBQA checks and market bulletins, and comments note mismatches between those sources.
- Clauses are to carry jurisdiction tags (US, Texas, New York State, South Africa) for later filtering.
- Several clauses originate in existing LMA wordings (LMA5032a, LMA5034A, LMA 5312B, LMA5210, LMA5546).
- External instruments are incorporated by reference with options selected: EU Standard Contractual Clauses Module 1 or 2, docking clause, sub-processor option 1, governing law option 1 (M13 13.7). Statutes are cited throughout (Contracts (Rights of Third Parties) Act 1999, Corporations Act s911A, Insurance Contracts Act s58).
- Precedence rules: the Agreement prevails over annexes (M1 1.2.1, M12 12.7.1), the more stringent law applies (M13 13.1.3B), the later incorporation supersedes an exceptional amendment (M3 3.19.5).
- Drafters flag conflicts between clauses (M14 14.19 vs 14.23.1) and duplicated provisions across modules (M1 1.19 vs M14 14.4, M4 4.3.6 vs 4.3.21).
