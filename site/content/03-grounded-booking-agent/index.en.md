---
title: "Module 3: Build a Grounded Booking Agent with Strands and GraphRAG"
weight: 40
---

Module 2 compares GraphRAG ways to read hotel information from Neo4j. Module 3
turns two of those read paths into tools for one local hotel assistant. A plain
Strands agent chooses a read tool, uses its returned evidence to answer, and
says when the graph does not have a needed fact. A separate reservation command
writes an approved request to Neo4j. Neo4j enforces the guest limit inside the
write transaction, so an over-limit request creates no reservation node.

This module is deployment Pattern A, the local agent. Modules 4 and 5 show
Patterns B and C as alternatives to it, not as later steps.

The module demonstrates five behaviors:

* **Automatic tool selection:** The model reads two tool specifications and
  chooses passage search, a structured graph query, both, or no tool when the
  turn needs no hotel fact.
* **Observable grounding:** The system prompt directs the model to use tool
  evidence before stating hotel facts. A trace records each tool call, and both
  read tools return the same structured answerability verdict.
* **An explicit limit:** Live room inventory is absent from the graph. The
  returned verdict marks that fact as missing instead of relying on a phrase in
  the model's answer.
* **A separate write path:** A reservation command, not the model, validates a
  reservation request and writes it to Neo4j in one transaction.
* **Safe retries:** A caller-supplied `request_id` lets a retried request
  return the original result instead of creating a second `ReservationRequest`
  node.

:image[Grounded agent architecture: the model chooses passage search or a structured record query for reads, while a separate application command writes reservations]{src="../../images/03-grounded-agent-overview.svg" width=800}

The agent has two ways to read the graph and no registered write tool. A
separate command handles the notebook's reservation examples.

* **Strands agent:** The agent runs Claude on Amazon Bedrock. It reads the
  question and picks the tool to call.
* **`search_hotel_passages`:** This read tool runs the Module 2 hybrid search and
  returns up to five source passages with linked hotel facts. It fits amenities,
  rooms, policies, services, and location details.
* **`query_hotel_records`:** This read tool uses `Text2CypherRetriever` for
  counts, averages, rankings, filters, and relationship questions. It returns
  the generated Cypher beside the database records.
* **Neo4j:** Neo4j stores the hotel graph, both search indexes, and the
  maximum-guests rule.
* **Grounded response policy:** The model is instructed to answer from returned
  facts and state what is missing when the evidence does not support an answer.
* **Reservation command:** The reservation command is plain Python code. It
  checks the rule and writes the request in one transaction, so the model never
  writes to the graph.

## Strands Agent Basics

The :link[Strands Agents SDK]{href="https://strandsagents.com/" external=true}
is an open-source Python library for building agents where the model decides
what happens next, not the developer.

* **Model-driven:** You do not write code that says "call the retrieval
  function, then call the answer function." You write a system prompt and
  register tools. The model reads the question, the tools' docstrings, and the
  conversation so far, then decides which tool to call and when it has enough
  information to answer.
* **The agent loop:** Strands runs a loop similar to the common "ReAct"
  pattern used by most agent frameworks. ReAct stands for Reason plus Act. The model reasons
  about what it needs, acts by calling a tool, observes the tool's result, and
  repeats until it can answer. Each turn of the loop is one round trip to the
  model.
* **Why this workshop uses it:** Strands makes the model's routing decision
  visible without a custom orchestration loop. The notebook can inspect the
  selected tools and their structured results directly.

The notebook uses these parts:

* **`Agent`:** This class runs the loop above. It sends messages to the model
  and calls whichever tool the model selects.
* **`BedrockModel`:** This class connects the agent to the Amazon Bedrock model
  named by the model ID.
* **`@tool`:** This decorator turns a Python function into a tool specification
  the model can select. The specification contains a name, a description
  derived mostly from the docstring, and an input schema.
* **`ToolTraceHook`:** This hook prints each tool call and records its complete
  bounded result for the notebook checks.
* **System prompt:** The system prompt defines which facts the model may use and
  when it must say that the graph lacks an answer.

The notebook prints the final specification for both read tools before it
creates an agent. This is the interface the model actually receives. The
descriptions explain the routing boundary between passage questions and
structured questions, and both schemas require one natural-language `query`.

Module 3 uses `BedrockModel` directly. Nothing forces a tool call. The system
prompt says to use a tool before stating a hotel fact, but a greeting or thank
you can receive a direct answer. Routing is a model decision, so the notebook
uses fresh agents and traces to make variation visible.

## How the Grounded Agent Works

For a hotel question, the normal agent loop is:

1. The model reads each tool's name, description, and input schema.
2. It chooses `search_hotel_passages`, `query_hotel_records`, or both and sends
   the guest's question as `query`.
3. Strands runs the selected tool and returns its JSON evidence to the model.
4. The model writes a response. The trace shows which path ran and what came
   back.

* **Why the tool owns the driver session:** The model receives data, not
  database credentials. It cannot run its own Cypher.
* **Passage result:** The passage tool returns `ok`, up to five `passages`,
  `hotel_ids`, `top_result`, and `grounding_result`. Each passage keeps at most
  8,000 characters of source text and 12 amenities.
* **Record result:** The record tool returns `ok`, the generated `cypher`, at
  most 25 list `records`, `row_count`, and `grounding_result`. An aggregate can
  still cover every matching graph record.
* **Shared verdict:** On a successful read, `grounding_result` contains exactly
  `answerable` and `missing_fact`. Empty records and a failed query remain
  distinct outcomes.

### The Nested Model Call in `query_hotel_records`

The structured path reaches a model twice. First, the agent model chooses the
tool. Inside the tool, `Text2CypherRetriever` asks a model to generate Cypher
from the pinned graph schema. Neo4j plans the statement with `EXPLAIN` and runs
it only when the plan is read-only. The tool returns the generated Cypher for
inspection because a query can run successfully and still express the wrong
meaning.

### Route Questions by Evidence Shape

> **"What amenities and guest rating does AnyCompany Cairo Nile View have?"**

This named-hotel question should reach `search_hotel_passages`. The notebook
also routes an average rating and a hotel count to `query_hotel_records`, then
routes a request for recorded cancellation-policy wording back to
`search_hotel_passages`. Each case gets a fresh agent. A mismatch produces a
warning because automatic model routing can vary. The warning does not make the
notebook fail.

### A Question the Graph Cannot Answer

> **"Does AnyCompany Cairo Nile View guarantee room availability next weekend?"**

* **What it tests:** The check confirms that a read tool ran and returned the
  explicit missing fact. It does not grade the model's wording.
* **Why the evidence is insufficient:** Neo4j stores descriptive hotel facts,
  policies, and total room capacity, not live room inventory. Either read tool
  can return real hotel evidence, but its verdict reports
  `missing_fact: live_room_availability`.

The next example sends `thanks, that is all`. Because it needs no hotel fact,
the expected behavior is a direct reply with no tool call. Together, these
checks demonstrate the intended policy and expose deviations during the lab.
Production systems still need routing and answer-quality monitoring.

## The Reservation Command

Reservation requests use a separate command because retrieval and writes need
different controls. The model never writes Cypher. Instead, the command accepts
five defined inputs and runs application-owned queries.

* **`request_id`:** This caller-created UUID stays the same when the caller
  retries a request.
* **`hotel_id`:** This stable hotel identifier selects the hotel. In an
  application, retrieval supplies this ID. This notebook's write example uses
  the matching ID from the local fixture manifest.
* **`check_in` and `check_out`:** The command validates these ISO dates before
  it opens the write transaction.
* **`guests`:** The command checks this positive integer against the enabled
  Neo4j rule.

Inside one write transaction, the command checks for an existing `request_id`,
reads the enabled maximum-guests rule, verifies the hotel, and creates the
request only when every check passes. Keeping the rule check and write in one
transaction prevents another request from changing the relevant graph state
between those operations.

### Reject a 15-Guest Reservation

Submit a reservation for 15 guests to test the maximum-guests rule. Neo4j
stores a limit of 10 guests, so the command returns this result:

:::code{language=json}
{
  "status": "rejected",
  "reason_code": "max_guests_exceeded",
  "max_guests": 10
}
:::

The transaction returns the rejection before the create query runs. Neo4j
therefore creates no `ReservationRequest` node for this request.

### Safely Retry a Valid Request

Submit the same valid request twice with one `request_id`. The first call
creates a `ReservationRequest` node and links it to the hotel with `FOR_HOTEL`.
The second call finds that node and returns `duplicate: true` with the original
`created_at` value.

A uniqueness constraint also covers concurrent retries. If two transactions
try to create the same `request_id`, Neo4j accepts one node and rolls back the
other transaction. The command then reads the accepted node and returns it as
the duplicate result.

## Run It

Open `notebooks/03-grounded-booking-agent/3.1_grounded_booking_agent.ipynb` and
run the cells in order. Expect about five minutes for the full notebook. Most
of that time goes to the agent's Amazon Bedrock calls.

## Challenge Checkpoint

The routing check shows whether the agent sends each read question to the read
tool that fits its evidence shape. The reservation command covers the write
part of the challenge. It enforces the workshop's 10-guest rule on a Cairo
fixture hotel and returns the first result when a request is retried with the
same `request_id`. As an optional exercise, ask a fresh agent the Chicago
spa-and-pool question and check the trace to see which read tool it chooses.

Slides for this module\: [The Grounded Booking Agent](../slides/overview-agent/)

## Next

Head to [Module 4](../04-production-agent/).
