---
title: "Neo4j Graph Intelligence Platform"
weight: 4
---

A grounded agent needs a knowledge layer that can retrieve source text and
follow the connections around it. Neo4j provides that layer. In this workshop,
one AuraDB database holds the hotel knowledge graph, retrieval indexes,
provenance, booking rules, reservation requests, and cross-session memory.

| Capability | What it contributes |
|---|---|
| **Native graph database** | Stores entities and relationships as the domain model the application queries |
| **Cypher** | Expresses connected patterns, structured filters, provenance paths, and transactional rules |
| **Vector and full-text indexes** | Combine semantic similarity with exact names, identifiers, and terms |
| **GraphRAG** | Expands a matched text chunk into connected hotel facts and their sources |
| **Agent memory** | Links actor-scoped preferences to conversations, messages, and real domain entities |
| **Drivers, connectors, and MCP** | Connect application code, data pipelines, and agents to the graph |

---

## AuraDB and the Property Graph

:link[Neo4j AuraDB]{href="https://neo4j.com/product/auradb/" external=true} is the
managed graph database used by every module. It stores the workshop data as a
property graph of hotels, rooms, amenities, policies, services, documents, and
chunks connected by named relationships.
[Foundations](../foundations/#the-property-graph-model) explains the property
graph model and the Cypher that queries it.

The reservation command is application-owned code. It checks the workshop's
10-guest rule and writes the request in one graph transaction. Model behavior
is not the final control.

---

## Enterprise Knowledge Layer

An Enterprise Knowledge Layer gives agents one shared place to find business
meaning, trusted data, and past experience. Agents query the layer while they
work. This keeps definitions, sources, rules, and memory consistent across
applications.

:image[The Enterprise Knowledge Layer serves applications, agents, and tools through three pillars: ontology, enterprise data, and agent memory]{src="../../images/enterprise-knowledge-layer.svg" width=800}

### Ontology

The ontology defines how the business works.

- **Business concepts** name the important people, products, events, and terms.
- **Relationships** describe the connections between those concepts.
- **Rules** set the policies and processes that guide access and action.
- **System mappings** link business terms to technical data sources.

### Enterprise Data

Enterprise data supplies the facts that ground the ontology.

- **Reference data** holds the approved values for concepts such as countries or account types.
- **Business records** hold the master and transaction data used to answer questions.
- **Data access** lets the layer query data in its source system or bring selected data into the graph.

### Agent Memory

Agent memory stores context, facts, and past decisions.

- **Short-term memory** holds the context from the current conversation.
- **Long-term memory** keeps facts and preferences across sessions.
- **Reasoning memory** records tool use, decisions, and outcomes from earlier work.
- A **decision trace** records the path that explains why the agent chose an action.

Ontology defines the meaning. Enterprise data supplies current facts. Agent
memory carries useful experience into the next request.

:link[Read Jesús Barrasa's article, The knowledge layer for enterprise AI]{href="https://neo4j.com/blog/agentic-ai/enterprise-knowledge-layer/" external=true}.

---

## One Graph, Multiple Retrieval Signals

The workshop keeps source text and structured domain facts in one connected
graph. Vector search, full-text search, graph expansion, and structured Cypher
are complementary entry paths over that same data. GraphRAG is the step that
combines retrieved text with the explicit entities and relationships around it.
[Foundations](../foundations/#from-rag-to-graphrag) explains each retrieval
signal and shows how the lexical graph connects to the domain graph.

---

## Provenance and Grounding

The graph does more than return an answer-shaped record. It keeps the path back
to the source document. The read tools return source filenames, source
chunks, graph fields, and a field-level provenance description in a bounded
result shape.

That evidence lets the agent distinguish three outcomes:

- **Supported:** The graph contains the facts required for the answer.
- **Missing fact:** The graph has related context but lacks a required fact.
- **No evidence:** The tool returned no usable evidence.

The prompt tells the model how to respond. The returned evidence and trace make
the behavior inspectable.

---

## Agent Memory in This Workshop

Module 6 extends the same graph with `User`, `Conversation`, `Message`, and
`Preference` nodes. A saved preference links to the message it came from and to
the real `Hotel` node it describes.

This structure makes memory:

- **Actor-scoped:** Recall starts from one selected `User` node. A production application must bind that identifier to the authenticated caller.
- **Auditable:** A preference retains its source message and session.
- **Correctable:** The application can update a specific graph record directly.
- **Connected:** Recalled information can traverse to current domain data.

Neo4j stores agent memory as connected data. AgentCore can host the agent. The
application can query and govern the memory in Neo4j.

---

## Where Neo4j Appears in the Workshop

The [module-by-module table](../platform/#module-by-module) on How Neo4j + AWS
Work Together shows which Neo4j capabilities each module uses.

## Learn More

- :link[Neo4j Graph Intelligence Platform]{href="https://neo4j.com/" external=true}
- :link[Neo4j Aura documentation]{href="https://neo4j.com/docs/aura/" external=true}
- :link[Neo4j GraphRAG for Python]{href="https://neo4j.com/docs/neo4j-graphrag-python/current/" external=true}
- :link[Neo4j connectors]{href="https://neo4j.com/docs/connectors/" external=true}

## Next

Continue to [Foundations](../foundations/) to learn the property graph and
GraphRAG concepts used in the labs.
