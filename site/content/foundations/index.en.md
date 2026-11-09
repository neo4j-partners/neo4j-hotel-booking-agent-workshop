---
title: "Foundations: Property Graphs and GraphRAG"
weight: 5
---

The platform overview assigned clear roles to AWS and Neo4j. This page explains
the technical ideas that connect them: property graphs, GraphRAG retrieval,
grounded agent requests, and control ownership.

Use [AWS GenAI Services](../aws-services/) and the
[Neo4j Graph Intelligence Platform](../neo4j-platform/) as references for the
individual services and capabilities.

---

## The Property Graph Model

A property graph stores data with three parts:

- A **node** represents a thing, such as a hotel, room, amenity, document, or text chunk.
- A **relationship** is a named connection between nodes, such as `OFFERS_AMENITY`.
- A **property** is a named value, such as a hotel name or guest rating.

:image[Property graph anatomy showing hotel, amenity, policy, and source chunk nodes connected by named relationships]{src="../../images/property-graph-anatomy.svg" width=800}

The pattern below says that a hotel offers an amenity:

:::code{language=cypher}
(:Hotel {name: "AnyCompany Cairo Nile View"})
    -[:OFFERS_AMENITY]->
(:Amenity {name: "Full-Service Spa"})
:::

Cypher is Neo4j's graph query language. Its pattern syntax follows the same
shape as the graph:

:::code{language=cypher showCopyAction=true}
CYPHER 25
MATCH (h:Hotel)-[:OFFERS_AMENITY]->(a:Amenity)
WHERE h.name = $hotel_name
RETURN h.name AS hotel, collect(a.name) AS amenities
:::

- **`MATCH`** selects a graph pattern.
- **Parentheses** describe nodes.
- **Square brackets** describe relationships.
- **Arrows** describe relationship direction.
- **`WHERE`** filters the result.
- **`RETURN`** selects the fields sent to the application.

Neo4j stores facts and their connections. Cypher retrieves the required path
through those facts.

---

## Same Hotel Business, Two Question Shapes

| Question | Best fit | Why |
|---|---|---|
| What is the average nightly rate next month? | Relational database, SQL aggregation | Group and average many rate rows |
| Which rooms are available for four guests tonight? | Relational database, SQL filter | Check dates, inventory, and room capacity |
| How many reservation requests were accepted this week? | Relational database, SQL aggregation | Count time-stamped transaction rows |
| Which Chicago hotel has both a spa and a pool? | Neo4j, Cypher pattern | Both amenities must connect to the same hotel |
| What cancellation policy applies to that hotel? | Neo4j, Cypher traversal | Follow the hotel to its policy |
| Which source document supports the answer? | Neo4j, GraphRAG | Follow the hotel to its chunk and document |

**Together:** SQL answers availability and transaction questions. Neo4j answers how hotel facts connect and where they came from.

---

## From RAG to GraphRAG

Retrieval-augmented generation sends selected source material to a model before
it answers. GraphRAG adds graph facts and connections to that source material.

- **Vector search** finds chunks whose meaning resembles a question.
- **Full-text search** finds exact hotel names, postal codes, identifiers, and terms.
- **Graph expansion** follows a matched chunk to its hotel, amenities, policy, service, room, and source document. It adds their properties and provenance to the result.
- **Structured Cypher** filters and aggregates known graph fields.

The workshop graph keeps a lexical graph and a domain graph, connected to each other:

:image[Two connected layers: the source file becomes a Document and Chunk in the lexical graph, and a Hotel node with typed Room, Amenity, Policy, and Service relationships in the domain graph]{src="../../images/01-graph-structure.svg" width=800}

- **Search** finds a `Chunk` in the lexical graph.
- **Expansion** follows typed relationships from that chunk into the domain graph.
- **Provenance** links each extracted fact to its source.

---

## One Grounded Request

Module 3 turns two retrieval patterns into model-selectable read tools:

:image[A hotel question reaches a plain Strands agent, which reads two tool specifications and chooses passage search using hybrid indexes and a reviewed traversal, or a structured record query using model-generated Cypher and an EXPLAIN read-plan check; Neo4j returns bounded evidence and a shared verdict that the trace records before the model writes its response]{src="../../images/foundations-grounded-request-flow.svg" width=800}

- **Tool selection:** The model reads each tool's name, description, and input
  schema. Nothing forces a call, so the lab observes routing with a trace.
- **Answer flow:** The prompt directs the model to answer from returned evidence
  or state what is missing.
- **Reservation command:** A separate command validates the request and writes it.
- **Rule enforcement:** Neo4j checks the workshop's 10-guest rule in the write transaction.

---

## Control Ownership

Each control belongs to a layer that can enforce it:

- **Read-tool choice:** The model chooses between two application-defined tool specifications.
- **Answer policy:** The prompt directs the model to use returned evidence. The trace and the grounding verdict make each lab turn inspectable.
- **Passage query:** A fixed `retrieval_query` defines the reviewed traversal.
- **Structured query:** Text2Cypher generates Cypher. The `EXPLAIN` guard allows only read plans.
- **Database write:** Neo4j rejects invalid and duplicate requests.
- **AWS access:** IAM controls deployment and service calls.
- **Memory access:** Actor-scoped Cypher limits recall to one actor.

You can reuse this separation of layers with a different graph schema and domain.

Slides for this module\: [Knowledge Graphs and AuraDB](../slides/overview-knowledge-graph/)

---

## Glossary

- **Guest:** A guest is the person in the hotel scenario who asks questions and requests bookings.
- **Actor:** Module 6 uses actor for the person a memory belongs to, stored in the graph as a `User` node.
- **Read tools:** The two read tools, `search_hotel_passages` and `query_hotel_records`, return hotel evidence from Neo4j without writing to it.
- **Reservation command:** The reservation command is application code that checks the 10-guest rule and writes a booking request for a Cairo fixture hotel in one Neo4j transaction.
- **Retrieval pattern:** A retrieval pattern is one of the four ways Module 2 reads the graph: Vector, Hybrid, VectorCypher, or Text2Cypher.
- **Deployment pattern:** A deployment pattern is one of three alternative places to run the agent and its tools.
- **Pattern A:** The agent and its read tools run locally in Module 3.
- **Pattern B:** The agent runs in the notebook and calls the read tools through AgentCore Gateway in Module 4.
- **Pattern C:** The agent runs on AgentCore Runtime in Module 5 and exposes the reservation command as the `create_reservation` tool.
- **Gateway tool:** A Gateway tool is a read tool that AgentCore Gateway exposes as a Lambda-backed MCP tool.
- **Provenance:** Provenance is the graph path that links each fact back to the source chunk and document it came from.
- **Grounding verdict:** The grounding verdict is the `grounding_result` that each read tool returns to say whether Neo4j holds enough evidence and which fact is missing.
- **Module and notebook numbers:** Module 3 is a workshop section, and notebook 3.1 is the `3.1_grounded_booking_agent.ipynb` file you run inside it.

## Next

Head to [Setup](../setup/).
