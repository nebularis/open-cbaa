# SPDX-License-Identifier: MPL-2.0
"""Checks the Open CBAA ontologies with LATTICE's tooling: HermiT consistency and class
satisfiability, SHACL conformance of the worked examples, and probes that each OWL axiom
and SHACL shape still rejects what it should.

Imports resolve through ontology/catalog-v001.xml. It needs a LATTICE checkout (its
catalog closure, its reasoning testkit jar and its layer shapes) and LATTICE's Python and
Java, so run it from the LATTICE directory::

    cd ../lattice && python ../open-dare/tools/ontology_check.py [--lattice .]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology"
UMBRELLA = "https://nebularis.github.io/open-cbaa/ontology/open-cbaa/0.2.0"
EXAMPLE = ONTOLOGY / "examples/ba-2026-001.ttl"
LAYERS = ["foundation", "vocabulary", "quantification", "party", "eligibility", "instrument", "behaviour"]
QNT = "https://www.nebularis.org/neuro-semantic/lattice/quantification#"

PREFIXES = """
@prefix ex:   <https://nebularis.github.io/open-cbaa/ontology/examples/ba-2026-001#> .
@prefix wim:  <https://nebularis.github.io/open-cbaa/ontology/wim#> .
@prefix stm:  <https://nebularis.github.io/open-cbaa/ontology/statement#> .
@prefix agr:  <https://nebularis.github.io/open-cbaa/ontology/agreement#> .
@prefix rsk:  <https://nebularis.github.io/open-cbaa/ontology/risk#> .
@prefix fnd:  <https://www.nebularis.org/neuro-semantic/lattice/foundation#> .
@prefix qnt:  <https://www.nebularis.org/neuro-semantic/lattice/quantification#> .
@prefix ins:  <https://www.nebularis.org/neuro-semantic/lattice/instrument#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
"""

# (claim, triples added to the example, consistent afterwards?)
OWL_PROBES = [
    ("a bound obligation is an ins:Obligation", "ex:fnol-transfer a [ owl:complementOf ins:Obligation ] .", False),
    ("an obligation template is not", "ex:FNOLTransfer a [ owl:complementOf ins:Obligation ] .", True),
    ("an agreement version is a wording object", "ex:BA-2026-001-v1 a [ owl:complementOf wim:WordingObject ] .", False),
    ("an agreement version is an ins:Element", "ex:BA-2026-001-v1 a [ owl:complementOf ins:Element ] .", False),
    ("wim:comprises is transitive",
     "ex:M5 a [ a owl:Restriction ; owl:onProperty wim:comprises ; owl:allValuesFrom [ owl:complementOf wim:Text ] ] .", False),
    ("a data element comprises nothing", "ex:C05-2-text wim:directlyComprises ex:C05-2-limit .", False),
    ("direct part-whole is asymmetric", "ex:C05-2 wim:isDirectlyComprisedBy ex:C05-2-text .", False),
    ("a template names no occupancy", "ex:FNOLTransfer stm:bearerOccupancy ex:Coverholder-occ .", False),
    ("a bound statement names no role", "ex:fnol-transfer stm:bearer ex:SomeRole .", False),
    ("a bound grant has one scope", "ex:grant-uw stm:scope ex:scope-uw-v2 . ex:scope-uw owl:differentFrom ex:scope-uw-v2 .", False),
    ("wording is not meaning", "ex:C05-2 a stm:Statement .", False),
]

# (claim, triples removed, triples added, text the report must contain)
SHACL_PROBES = [
    ("one variant per slot", "", "ex:BA-2026-001-v1 agr:includes ex:C01-4B .", "exactly one of the slot's variants"),
    ("mandatory children included", "ex:BA-2026-001-v1 agr:includes ex:C05-2-text .", "", "mandatory children"),
    ("values come from the bound scheme", "ex:risk-ajaccio rsk:riskLocation ex:Ajaccio .",
     "ex:risk-ajaccio rsk:riskLocation ex:Paris .", "not in the contract's bound scheme"),
    ("segment indices have no gaps", "",
     'ex:C05-2-text wim:hasSegment [ a wim:Segment ; wim:segmentIndex "10"^^xsd:nonNegativeInteger ; wim:segmentText "x" ] .',
     "run 0..n-1"),
    ("bound while the version is valid", 'ex:Policy-0001 rsk:boundAt "2026-03-02T09:30:00Z"^^xsd:dateTime .',
     'ex:Policy-0001 rsk:boundAt "2025-03-02T09:30:00Z"^^xsd:dateTime .', "valid at the time of binding"),
    ("a bound statement names occupancies", "", "ex:grant-uw stm:bearer agr:Coverholder .", "occupancies, not roles"),
    ("a bound obligation names its obligee", "ex:fnol-transfer ins:obligee ex:Lead-occ .", "", "ins:obligor and ins:obligee"),
    ("a UMR is unique per market", "",
     'ex:other a agr:AgreementVersion ; fnd:hasIdentity ex:OTHER ; fnd:hasGovernanceState fnd:Active ; '
     'agr:umr "B1234ACME2026001" ; agr:inMarket agr:LloydsMarket .', "claimed per market"),
    ("an amendment keeps the identity", "ex:BA-2026-001-v2 fnd:hasIdentity ex:BA-2026-001 .", "ex:BA-2026-001-v2 fnd:hasIdentity ex:BA-2026-002 .",
     "same agreement"),
    ("alternative bounds differ in unit", "",
     "ex:v1-limit-gbp qnt:alternativeBound ex:x . ex:x a qnt:Bound ; qnt:onSpace stm:MoneySpace ; qnt:boundSense qnt:Upper ; "
     "qnt:boundClosure qnt:Closed ; qnt:boundValue [ a qnt:Quantity ; qnt:onSpace stm:MoneySpace ; qnt:numericValue 1.0 ; qnt:inUnit ex:GBP ] .",
     "different units"),
    ("a bound statement has its template's kind", "ex:grant-uw a stm:AuthorityGrant .", "ex:grant-uw a stm:Permission .",
     "kind of the template"),
    ("inclusion conditions read governing variables", "ex:IsLineSlip wim:readsVariable ex:M1-GOV1 .",
     "ex:IsLineSlip wim:readsVariable ex:C05-2-classes .", "governing variable"),
    ("a risk has one location", "", "ex:risk-ajaccio rsk:riskLocation ex:Lyon .", "one deemed location"),
    ("a scope parameter names its path", "ex:SoUAGrant-territories stm:scopeStep ex:RiskLocationStep .", "", "stm:scopeStep"),
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lattice", type=Path, default=Path.cwd(), help="LATTICE checkout (default: current directory)")
    args = parser.parse_args(argv)
    lattice = args.lattice.resolve()
    sys.path[:0] = [str(lattice / "tools"), str(lattice / "tools/mork_compilers/src")]

    from mork_compilers import reasoning
    from ontology_catalog import Catalog, closure
    from pyshacl import validate
    from rdflib import Graph, URIRef
    from rdflib.namespace import OWL, RDF

    catalog = Catalog(ONTOLOGY / "catalog-v001.xml")
    shapes = Graph()
    for path in sorted(ONTOLOGY.glob("*/shapes/*.ttl")) + [ONTOLOGY / "governance/scheme-contracts.ttl"]:
        shapes.parse(path)
    for layer in LAYERS:
        for kind in ("structural", "constraints"):
            if (path := lattice / "ontology" / layer / "shapes" / f"{kind}.ttl").exists():
                shapes.parse(path)

    failures = 0

    def report(ok: bool, claim: str, detail: str = "") -> None:
        nonlocal failures
        failures += not ok
        print(("ok    " if ok else "FAIL  ") + claim + ("" if ok else f"\n{detail}"))

    def conforms(data: Graph) -> tuple[bool, str]:
        # LATTICE's qnt:OperationCapabilityMeetShape query uses qnt: without declaring it.
        data.bind("qnt", QNT)
        ok, _, text = validate(data, shacl_graph=shapes, inference="rdfs", allow_warnings=True)
        return ok, text

    ontology = closure(catalog, UMBRELLA, include_external=True)
    report(reasoning.run("consistent", graphs=[ontology]), "the ontologies are consistent")
    classes = sorted({c for c in ontology.subjects(RDF.type, OWL.Class) if "open-cbaa" in str(c)})
    probe = Graph()
    for i, c in enumerate(classes):
        probe.add((URIRef(f"urn:probe:{i}"), RDF.type, c))
    report(reasoning.run("consistent", graphs=[ontology, probe]), f"all {len(classes)} Open CBAA classes are satisfiable together")

    version = re.search(r"owl:versionIRI\s+<([^>]+)>", EXAMPLE.read_text()).group(1)
    example = closure(catalog, version, include_external=True)
    report(reasoning.run("consistent", graphs=[example]), f"{EXAMPLE.name} is consistent")
    ok, text = conforms(Graph() + example)
    report(ok, f"{EXAMPLE.name} conforms to the shapes", text)

    for claim, added, consistent in OWL_PROBES:
        extra = Graph().parse(data=PREFIXES + added, format="turtle")
        report(reasoning.run("consistent", graphs=[example, extra]) == consistent, f"owl: {claim}")

    for claim, removed, added, expected in SHACL_PROBES:
        data = Graph() + example
        data -= Graph().parse(data=PREFIXES + removed, format="turtle")
        data.parse(data=PREFIXES + added, format="turtle")
        ok, text = conforms(data)
        report(not ok and expected in text, f"shacl: {claim}", text[:1500])

    print(f"{failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
