---
title: "GraphRAG with Neo4j on AWS: From Search to Grounded Agents"
weight: 0
---

This workshop shows how to build a booking agent that answers from a connected
graph. Semantic search finds relevant source text. Graph traversal then adds
properties, relationships, and provenance so the agent can identify the hotel
and show the source for its answer.

This workshop uses a hotel booking scenario. You will:

- **Compare retrieval:** Test GraphRAG retrieval paths for different question types.
- **Shape read tools:** Turn complementary passage and structured retrieval patterns into bounded interfaces.
- **Build an agent:** Let the model route between those tools and inspect its grounding evidence.
- **Deploy tools and the agent:** Use :link[Amazon Bedrock AgentCore]{href="https://aws.amazon.com/bedrock/agentcore/" external=true}.
- **Add memory:** Store agent memory as a graph in :link[Neo4j]{href="https://neo4j.com/" external=true}.

Start with [How Neo4j + AWS Work Together](./platform/). It leads through short
guides to [AWS GenAI Services](./aws-services/) and the
[Graph Intelligence Platform](./neo4j-platform/), then into the GraphRAG
concepts in [Foundations](./foundations/).

**Source code:** :link[Open the workshop repository on GitHub]{href="https://github.com/neo4j-partners/neo4j-hotel-booking-agent-workshop" external=true}.

## Why Grounding Matters

A booking agent needs evidence for its answers and controls for its actions.

- **Wrong answer:** The agent promises an amenity that the hotel does not offer.
- **Wrong action:** The agent accepts a reservation request for more guests than the booking rules allow.
- **Missing provenance:** The team cannot trace a claim to its source document.
- **Workshop challenge:** The challenge has a read part and a write part. The read part asks, "Which Chicago hotel has both a spa and a swimming pool, and what is its cancellation policy?" The write part asks, "Can a guest submit a booking request for four guests?" The reservation command demonstrates the 10-guest rule on a Cairo fixture hotel. A 10-guest request succeeds. A 15-guest request is rejected. Four guests fall within that rule.

You will connect each answer to its sources. A separate reservation command
will save each approved request. Neo4j enforces the guest limit inside the
write transaction, so an over-limit request creates no reservation node.

:::alert{type="info" header="Region"}
This workshop runs in **us-east-1**, the N. Virginia region. Your AWS account
arrives pre-configured. Setup guides you through creating a free Neo4j database.
:::

---

## Workshop Flow

| Module | What You Will Build |
|--------|---------------------|
| **Platform overview** | See how AWS and Neo4j work together, then learn the capabilities each platform contributes, including Amazon Bedrock AgentCore |
| **Foundations** | Learn the property graph, the GraphRAG retrieval flow, and service responsibilities |
| **Setup** | Create a Neo4j AuraDB Free database, restore the workshop graph, verify Neo4j and :link[Amazon Bedrock]{href="https://aws.amazon.com/bedrock/" external=true} access |
| **Module 1: Build the Graph** | Extract five held-out hotel documents into the graph, define the extraction schema, create both retrieval indexes |
| **Module 2: From Vector Search to Graph-Enriched Retrieval** | Semantic search, exact-term search, and graph-enriched retrieval |
| **Module 3: Build a Grounded Booking Agent with GraphRAG** | Turn two GraphRAG read paths into agent tools, check grounding verdicts, and protect reservation writes |
| **Module 4: Production Agent with AgentCore** | AgentCore Gateway, IAM-authenticated MCP, and a Strands agent over remote tools |
| **Module 5: Deploy to AgentCore Runtime** | Containerize the agent, launch it on Runtime, correlate one request end to end |
| **Module 6: Neo4j Graph Memory** | Cross-session graph memory, actor-scoped recall, full provenance, and a conceptual AgentCore comparison |
| **Summary, Production Path, and Wrap-up** | The argument end to end, the decision tables, the work required for production, and where to take it next |

Modules 3, 4, and 5 run the same tools in three alternative deployment
patterns, labeled Pattern A, B, and C in the architecture below. They are not
steps in one pipeline. Module 6 adds cross-session memory as a separate
exercise.

---

## The Goal

A booking agent should answer from evidence and act only within rules. This
workshop builds that agent on one Neo4j graph. Amazon Bedrock reasons over
the question. Neo4j supplies the facts, the source text behind each fact, and
the rules a booking must satisfy. The same agent can run in a notebook or on
managed AWS services without changing what it retrieves or how it is grounded.

---

## The Final Objective

The workshop challenge has two parts. The read part asks, "Which Chicago hotel
has both a spa and a swimming pool, and what is its cancellation policy?"
Module 2 demonstrates the retrieval each part of that question needs. The
write part asks, "Can a guest submit a booking request for four guests?" The
reservation command demonstrates the 10-guest rule on a Cairo fixture hotel.
A 10-guest request succeeds. A 15-guest request is rejected. Four guests fall
within that rule.

The notebooks demonstrate four checkable parts:

- **The hotel:** A fixed Cypher query in Module 2 checks both amenities on each
  Chicago `Hotel` node. It returns Lakeview Horizon Suites. The result names
  the hotel's source document and the graph path behind each field.
- **The policy:** Hybrid search in Module 2 finds a cancellation policy by
  postal code. It returns the policy of Windward Mile Tower, the Chicago hotel
  that the spa-and-pool filter excludes. This result demonstrates exact-term
  retrieval with provenance. The policy comes back with the source `Chunk` and
  `Document` it was read from.
- **The booking:** The reservation command checks the workshop's 10-guest rule
  and writes the `ReservationRequest` in one transaction. A 15-guest request is
  rejected. A retry with the same `request_id` returns the first result instead
  of a second booking.
- **The gaps:** Questions the graph cannot answer, such as live room
  availability, come back as a stated missing fact instead of a guess.

As an optional exercise, retrieve the cancellation policy of Lakeview Horizon
Suites, or ask the Module 3 agent the full Chicago read question.
Module 5 runs the same agent as a hosted service on AgentCore Runtime. A
separate exercise in Module 6 shows that a guest's stated preference can be
stored in the same graph, recalled in a later session, and traced to the
message it came from.

---

## The Final Architecture

:image[Final architecture: Amazon Bedrock models on top, three agent patterns in the middle, and one Neo4j AuraDB graph at the bottom. Pattern A runs a local notebook agent. Pattern B calls read-only Lambda tools through AgentCore Gateway. Pattern C hosts the agent on AgentCore Runtime.]{src="../images/final-architecture.svg" width=800}

- **Bottom layer, Neo4j:** Every pattern uses the same graph. Setup restores
  the lexical and domain layers. Module 1 extends them with held-out documents
  and creates the indexes. Module 3 adds the reservation command. Module 6 adds
  memory.
- **Middle layer, three deployment patterns:** Pattern A is where you learn routing and
  grounding. Pattern B moves the read tools behind a managed MCP endpoint.
  Pattern C hosts the full agent, including the write. The read tools keep the
  same base names, descriptions, and result shapes in all three.
- **Top layer, Bedrock:** Claude chooses tools and writes the answer. It also
  generates Cypher inside `query_hotel_records`. Nova embeds hotel chunks.
  Titan V2 embeds memory records. The two embedding spaces use separate
  indexes.
- **What stays fixed:** The graph schema, the read-tool contract, and the
  grounding verdict stay the same in every pattern. Patterns A and C use the
  same transactional reservation command. Only the place where the agent and
  tools run changes.

---

## What You Will Learn

- **Graph construction:** Use a fixed extraction schema and provenance to build a queryable graph.
- **Retrieval:** Choose Vector, Hybrid, VectorCypher, or Text2Cypher for each query need.
- **Grounding:** Inspect tool selection and structured evidence, state missing facts, and enforce write rules in one transaction.
- **Remote tools:** Deploy tools to AgentCore Gateway and call them through IAM-authenticated MCP.
- **Memory:** Store auditable, correctable graph memory.
- **Architecture:** Assign clear roles to Neo4j, Bedrock, Strands, Gateway, Runtime, Lambda, and IAM.

---

## Prerequisites

- **Skills:** Use basic Python and AWS CLI commands.
- **Neo4j Aura:** Create a free account during the first Setup step.
- **Hosted environment:** Run the notebooks in Vocareum's Visual Studio Code environment.

Presenter slides for the opening\: [The Business Case for Grounded Agents](./slides/overview-business-story/)

:::alert{type="warning" header="Cost"}
This workshop creates AWS resources that incur charges. Follow the [Clean Up](./wrap-up/#clean-up) steps on the Wrap-up page. Estimated cost\: under $2.
:::

::children{depth=2 variant=list}
