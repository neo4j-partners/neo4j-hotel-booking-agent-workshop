# Final Architecture: Proposal for the Site Index Page

> **Status:** Sections 3.1 to 3.3 are now live on the index page, `site/content/index.en.md`.

## 1. What Is on the Index Page Today

The index page goes from **Workshop Flow** straight to **Module 4 Tool
Architecture**. That section shows `03-agentcore-architecture.svg`.

- **Is it the Module 4 diagram?** Yes. Module 4 uses the same file,
  `site/content/04-production-agent/index.en.md:31`. The index page repeats it
  with a slightly shorter caption.
- **Why it reads wrong on the index:** The diagram sits where a reader expects
  the destination of the workshop. It shows only one of three deployment
  patterns. The two sentences under it then explain that Module 5 is different
  and Module 6 adds memory, so the reader has to assemble the real picture alone.
- **What the index never states:** The page never says what the reader will
  have running at the end, or which question the finished agent will answer.

## 2. What the Workshop Actually Builds

The workshop does not build one integrated system. It builds **one shared
core** and then runs it **three different ways**.

- **Shared core:** One Neo4j graph and one tool contract. The graph holds the
  hotel knowledge, the indexes, the reservation rule, and the memory. The tool
  contract defines `search_hotel_passages` and `query_hotel_records`, their
  descriptions, and their bounded result shape.
- **Pattern A, local agent (Module 3):** A Strands agent in the notebook calls
  both read tools as local Python functions. The reservation command runs
  locally against Neo4j.
- **Pattern B, remote tools (Module 4):** The agent stays in the notebook. The
  two read tools move to Lambda behind an IAM-authenticated AgentCore Gateway.
  This pattern has no write path.
- **Pattern C, hosted agent (Module 5):** The whole agent runs in an AgentCore
  Runtime container. It holds both read tools and `create_reservation`, and it
  connects to Neo4j directly. It does not use the Gateway.
- **Graph memory (Module 6):** The notebook writes and reads actor-scoped
  preferences in the same graph. The booking agent does not call memory in any
  pattern.

The site already says this in several places. Module 4 calls B and C "two
separate patterns, not two steps of one path." The Production Path page notes
that connecting Runtime to Gateway is a separate design choice. The wrap-up
diagram shows three side-by-side architectures. The index page is the one place
that does not.

## 3. Proposed Replacement for the "Module 4 Tool Architecture" Section

Replace that section with three short subsections: the goal, the final
objective, and the final architecture.

### 3.1 The Goal

> A booking agent should answer from evidence and act only within rules. This
> workshop builds that agent on one Neo4j graph. Amazon Bedrock reasons over
> the question. Neo4j supplies the facts, the source text behind each fact, and
> the rules a booking must satisfy. The agent then moves from a notebook onto
> managed AWS services without changing what it retrieves or how it is
> grounded.

### 3.2 The Final Objective

> The workshop challenge has two parts. The read part asks, "Which Chicago hotel
> has both a spa and a swimming pool, and what is its cancellation policy?" The
> graph answers it with retrieval and provenance. The write part asks, "Can a
> guest submit a booking request for four guests?" The reservation command
> answers it on the two Cairo fixture hotels.

The notebooks demonstrate four checkable parts:

- **The hotel:** A fixed Cypher query in Module 2 checks both amenities on each
  Chicago `Hotel` node. It returns Lakeview Horizon Suites and names the source
  document for each field.
- **The policy:** Hybrid search in Module 2 finds a Chicago cancellation policy
  by postal code. The policy comes back with the source `Chunk` and `Document`
  it was read from.
- **The booking:** The reservation command checks the workshop's 10-guest rule
  and writes the `ReservationRequest` in one transaction. A 15-guest request is
  rejected. A retry with the same `request_id` returns the first result instead
  of a second booking.
- **The gaps:** Questions the graph cannot answer, such as live room
  availability, come back as a stated missing fact instead of a guess.

As an optional exercise, ask the Module 3 agent the full Chicago read question.
Module 5 runs the same agent as a hosted service on AgentCore Runtime. A
separate exercise in Module 6 shows that a guest's stated preference can be
stored in the same graph, recalled in a later session, and traced to the
message it came from.

### 3.3 The Final Architecture

Proposed caption: *One graph and one tool contract, run three ways.*

```
                              Amazon Bedrock
        Claude: reasoning, Text2Cypher   Nova: chunk embeddings   Titan V2: memory embeddings
                     ^                          ^                         ^
                     |                          |                         |
=====================|==========================|=========================|==================
 HOW THE AGENT RUNS: one pattern per deployment

 [A] Local agent            [B] Remote tools               [C] Hosted agent
     Module 3                   Module 4                       Module 5

  Notebook                  Notebook                       Authorized AWS client
  Strands agent             Strands agent                          |
   |                          |                                    | InvokeAgentRuntime (IAM)
   |- search_hotel_passages   | MCP over HTTPS, SigV4              v
   |- query_hotel_records     v                            +-----------------------------+
   '- reservation command  +-------------------------+     | AgentCore Runtime container |
      (called directly)    | AgentCore Gateway       |     | booking_agent.py            |
   |                       | IAM authorizer          |     |  |- search_hotel_passages   |
   |                       +-------------------------+     |  |- query_hotel_records     |
   |                          | invoke                     |  '- create_reservation      |
   |                          v                            +-----------------------------+
   |                       +-------------------------+                 |
   |                       | Lambda x2, read only    |<- Secrets       |
   |                       |  search_hotel_passages  |   Manager       |
   |                       |  query_hotel_records    |                 |
   |                       +-------------------------+                 |
   |                          |                                        |
===|==========================|========================================|====================
   v                          v                                        v
+------------------------------------------------------------------------------------------+
|                          Neo4j AuraDB: one graph for every pattern                       |
|                                                                                          |
|  Lexical layer   Document -> Chunk, vector index + full-text index        (Module 1)     |
|  Domain layer    Hotel -> Room, Amenity, Policy, Service, with provenance (Module 1)     |
|  Commands        ReservationRequest -> Hotel, guest-limit rule, request_id (Module 3)    |
|  Memory          User -> Preference -> Message -> Hotel, actor-scoped      (Module 6)    |
+------------------------------------------------------------------------------------------+
           ^
           |  Module 6 notebook writes and reads memory directly.
           |  No agent pattern calls memory.
```

Suggested text under the diagram:

- **Bottom layer, Neo4j:** Every pattern reads and writes the same graph. Module
  1 builds the lexical and domain layers. Module 3 adds the reservation command.
  Module 6 adds memory.
- **Middle layer, three patterns:** Pattern A is where you learn routing and
  grounding. Pattern B moves the read tools behind a managed MCP endpoint.
  Pattern C hosts the full agent, including the write. The tool names,
  descriptions, and result shapes stay the same in all three.
- **Top layer, Bedrock:** Claude chooses tools and writes the answer. It also
  generates Cypher inside `query_hotel_records`. Nova embeds hotel chunks.
  Titan V2 embeds memory records. The two embedding spaces use separate
  indexes.
- **What stays fixed:** The graph schema, the tool contract, the grounding
  verdict, and the transactional write. Only the place where the agent and
  tools run changes.

Then keep the existing two role bullets for Neo4j and Bedrock, or fold them
into the layer bullets above.

## 4. Additional Details Worth Adding

These are optional. Each is one or two lines on the index page.

- **A request walkthrough:** Trace the challenge question through Pattern C in
  five steps: invoke, passage search, policy with provenance, reservation
  transaction, response with tool results. This ties the objective to the
  diagram.
- **A "what you will have at the end" list:** A graph you built, two read tools
  with a shared verdict, a protected write, a Gateway with two Lambda tools, a
  Runtime deployment, and a memory record with provenance.
- **A one-line note on scope:** The patterns are alternatives, not a pipeline.
  The Production Path page covers combining them.
- **A link to the wrap-up diagram:** `wrap-up-architectures.svg` already shows
  B, C, and memory side by side. The index diagram above is the same idea with
  the shared graph made explicit.

## 5. Optional: A Unified Target Architecture

The workshop does **not** build this. It is the production design the modules
point toward, and it fits the Production Path page better than the index page.
It is included here only if you want to show the reader where the patterns
lead.

```
  Guest app
     |  OAuth bearer token
     v
+-------------------------------+        +------------------------------+
| AgentCore Runtime             |------->| Amazon Bedrock               |
| Strands booking agent         |        | Claude, Nova, Titan V2       |
| per-request Agent, session ID |        +------------------------------+
+-------------------------------+
     |  MCP, SigV4
     v
+-------------------------------+
| AgentCore Gateway             |
| tool policy per call          |
+-------------------------------+
     |              |                    |
     v              v                    v
+-----------+  +----------------+  +------------------+
| Read tools|  | Reservation    |  | Memory tools     |
| Lambda x2 |  | command Lambda |  | recall / promote |
+-----------+  +----------------+  +------------------+
     |              |                    |
     | read-only    | write user,        | actor-scoped
     | Neo4j user   | one transaction    | queries
     v              v                    v
+-----------------------------------------------------------+
| Neo4j AuraDB: hotel graph, reservations, graph memory     |
+-----------------------------------------------------------+

 Cross-cutting: Secrets Manager for every Neo4j credential,
 CloudWatch traces with one request ID across all hops.
```

What differs from the workshop:

- **Runtime calls Gateway:** In the workshop, Pattern C reaches Neo4j directly.
- **The write is a Gateway tool:** In the workshop, the reservation command never
  sits behind Gateway.
- **Memory is in the agent loop:** In the workshop, only the Module 6 notebook
  touches memory.
- **Separate Neo4j identities:** The workshop uses one shared credential.

## 6. Decisions Needed Before Editing the Site

1. **Which diagram goes on the index?** The recommendation is the three-pattern
   diagram in section 3.3, because it matches what the notebooks build.
   Section 5 would overstate the workshop if it appeared on the index.

three-pattern diagram in section 3.3
 
2. **New SVG or ASCII?** The index uses SVG diagrams. Section 3.3 would need a
   new SVG, likely a revision of `wrap-up-architectures.svg` with the shared
   Neo4j layer at the bottom and Pattern A added.

have a background agent draw an svg

3. **Keep the Module 4 diagram on the index at all?** The recommendation is to
   remove it there and keep it in Module 4, where it already appears.

remove it 

4. **Where does section 5 go, if anywhere?** The Production Path page is the
   natural home.

Production Path Page 