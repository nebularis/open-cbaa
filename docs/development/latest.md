**Decisions needing ratification:** D17 to D26 are in the design spec's decision log under "Proposed". The ones that change earlier recommendations:
- **D22:** only bound obligations are `ins:Obligation`s, because a template names roles, not the occupancies Instrument requires. This refines integration spec §5.5.
- **D23:** I6 is not adopted for now. Typing library wording as `ins:Provision` would fail LATTICE's `ins:ProvisionShape`, since library wording has obligations only as templates.
- **D20:** inclusion conditions are checked by posing the agreement's variable value as an eligibility question, because an evidence path can't pick out one variable's value. The cost is that design-time exclusivity checks over a variation slot will need a Surface step first.

**Upstream findings** (recorded in integration spec §8; LATTICE itself is unchanged):
- **L15:** `bhv:forSubject` only accepts a role occupancy, so an agreement can't be the subject of its own lifecycle state.
- **L16:** Quantification's vocab has no ontology header, so it can't be imported.
- **L17:** `qnt:OperationCapabilityMeetShape` uses `qnt:` without declaring it, so it breaks unless the data graph binds the prefix. The check tool binds it as a workaround.
- Integration spec §2 was wrong that importing Party brings in Quantification. Each LATTICE layer imports only Foundation, and the spec is corrected.

**Also updated:** the design spec (version 0.3), integration spec (version 0.5), plan status, walkthrough prefixes, POC notes, root and tools READMEs, and the copilot instructions (a checklist for changing an ontology). The catalog is regenerated.

**Not done:**
- The GWP allowance in the example.
- The lifecycles other than M12.
- The submodule, the gate run and compilation.
- Version checking of the `governance/` shapes: they don't sit beside a `spec/`, so LATTICE's check skips them.

No LATTICE release tags are needed.

To re-run the checks:
```bash
cd ../lattice && python ../open-dare/tools/ontology_check.py
```
```bash
cd ../lattice && python tools/ontology_version_check.py --root ../open-dare
```