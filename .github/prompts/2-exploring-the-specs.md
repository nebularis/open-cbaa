# Exploring the specs

The specs (currently up to M8) are now available to you in the `.copilot/` directory, along with an overview file. The specifications of the wording, examples, and embedded tabular data, have all been converted to XML format for your convenience.

## Thinking About The Models

Thinking about the ways in which different types of components are inter-connected in the models - tabular data embedded alongside references to internal and external clauses - please review our ontological layers `ontology/*.ttl` to ensure alignment.

Things to consider:

- are we making the most of the expressiveness of the DL fragment we've chosen?
- to what extent have we enabled (or prevented) useful reasoning over the ontologies with our design? 

## Thinking About Implementors

If you were implementing a system on this semantic foundation, would the abstractions that you've chosen enable the kind of behaviour that a market-wide DA platform really needs to exhibit?

### Ontological Layering

As you contemplate layering your ontologies, I want you to think carefully about a few more things...

**Principle #1** ANY model should be designed according to its intended use. What is the intended use here? What _behaviour_ do we want to get out of a model of these contracts?

## Architectural vs. Operational Semantics

The semantics we want for a data architecture - acting as a conceptual model and a terminological reference around which the industry can align - are, perhaps, different to the semantics we want for operational systems. Think about:

- what governance and provenance mean in the ontological layers of these kinds of governing contracts/instruments
- how different would the model be if its primary aim was to enable a compiler tool-chain that could read the text and generate code (text or intermediate forms, e.g., bytecode), or that could be used to generate implementation models for condition-checking, workflow, contract validation, etc etc
- yet again how different might the abstractions be, if our goal was to populate the A-Box (e.g., a graph database at runtime) with individuals (i.e., nodes whose `rdf:type` relates to the concepts in the T-Box) with the intention of processing said data within the broader architectural quanta of an operational system? 

## Ontological & Functional Strata 

What belongs in the T-box, versus where could A-box expressiveness be leveraged, is meaningfully challenged by the need to process data in a real system. Equally, the right data granularity for one task, might not suit another. 

Do we need the ability to layer ontologies in order to "mix-in" functionality/behaviour? When we talk about behaviour, do we want to model state in the A-Box, or just use the T-Box as a "ground truth" for creating a state-machine implementation for runtime use? _How 'executable' do these kinds of contracts need to be?_ - Here YOU MUST think about the broader market and operational considerations for Delegated Authority at Lloyd's, and what computable contracts potentially offer from an aligned business/technology strategy perspective.

## Inspiration

You may now cross-reference [Lattice](https://github.com/nebularis/lattice), however DO NOT implement your models on top of this framework yet. It is too unstable being under active development. For now, just look for inspiration.

## Reminder

Please don't forget that the `ontology/README.md` needs to be kept up to date with your design thinking and decisions!
