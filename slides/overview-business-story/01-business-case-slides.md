---
marp: true
theme: default
paginate: true
---

<style>
section {
  --marp-auto-scaling-code: false;
}

li {
  opacity: 1 !important;
  animation: none !important;
  visibility: visible !important;
}

/* Disable all fragment animations */
.marp-fragment {
  opacity: 1 !important;
  visibility: visible !important;
}

ul > li,
ol > li {
  opacity: 1 !important;
}
</style>

# The Business Case for Grounded Agents

A guest asks for a Chicago hotel with a spa and a pool. The model answers with confidence. The graph answers with evidence.

<!--
This deck sets up the whole workshop. The argument runs in a fixed order:
what is at stake, why the model alone fails, why retrieval alone fails, what
a graph adds, third-party evidence, and then the hero question the rest of
the day answers. The deck closes on the demo, the six-module roadmap, the
request flow, and the control-ownership table.

Do not explain retrievers here. Deck 4 owns that. This deck only has to make
the room want the graph.
-->

---

## The Enterprise AI Paradox

Modern models already out-reason most people on general knowledge, recall, and synthesis. So why is the booking assistant still wrong?

- **High intelligence** plus **missing operational context** equals confident, useless answers
- The gap is not model capability. It is what the model was never told: how the facts of this business connect

<!--
Open here rather than with the technology. Everyone in the room has watched a
capable model produce a fluent answer about their own business that was simply
untrue. Name that experience, then spend the deck explaining why it happens.

The second bullet is the thesis. Nothing in this workshop makes the model
smarter. Everything in it changes what the model is allowed to see.
-->

---

## The Stakes

A hotel group is putting agents in front of guests. Three failures cost real money, and they are different failures:

- **A wrong answer:** the agent promises a spa the hotel does not have. The chain pays for a refund and absorbs a bad review
- **A wrong action:** the agent holds a room for fifteen guests in a suite that sleeps ten. Someone on the property has to unwind the reservation by hand
- **An unexplainable answer:** nobody can say which document the claim came from

Graph retrieval addresses the first. A controlled write path addresses the second. Graph provenance addresses the third.

<!--
This is where the hotel domain earns its place. The stakes are lower drama
than aviation and higher frequency, which is the honest framing. Every
attendee has a system that answers questions and a system that writes rows,
and most of them have wired an agent to both.

Land the split now, because it is the spine of Module 3. Grounding a read and
constraining a write are two different engineering problems, and most GraphRAG
talks only cover the first.
-->

---

## Why LLMs Alone Fall Short

- **Hallucination:** the model generates the statistically probable answer, not the verified one. It describes an amenity that does not exist as confidently as one that does
- **No access to your data:** the model has never seen this chain's hotels, rates, or policies. Retraining on a newer snapshot of the public web does not change that
- **Relationship blindness:** it cannot connect a policy to the property it governs, or find every hotel that shares one amenity

Plain retrieval narrows the first two gaps. Graph retrieval closes all three, with context that is verified, connected, and focused.

<!--
The closing line is the pivot the next two slides depend on. Say it slowly.

If someone pushes on hallucination as a solved problem, agree partly: plain
retrieval does reduce it. Then make the stronger claim. Graph retrieval does
better on all three gaps. The answer starts on a verified entity, follows
stored relationships, and carries only the facts the question needs. The
third bullet is the one no amount of chunk retrieval fixes.
-->

---

## The Problem Vectors Do Not Solve

Vector search finds text that is **similar**. It cannot **traverse relationships** or **guarantee a condition**.

Three questions this workshop asks of its own hotel documents:

- **"The hotel at postal code 60611"** loses the answer. An embedding of `60611` sits near every other five-digit number, so similarity ranks the right chunk below prose that reads more like the question
- **"Chicago hotels with both a spa and a pool"** returns hotels with one of them. Nothing ties two conditions to the same property
- **"What does this chunk's hotel actually offer"** cannot be answered from the passage. The name, the rating, and the amenity list live in the graph, not in the text

Similar text is not the same as a connected fact.

<!--
These three are not hypotheticals. Module 2 runs all three. The room watches
vector search miss the 60611 chunk before hybrid retrieval finds it, and then
sees the spa-and-pool question answered by reviewed Cypher rather than by
similarity at all.

Postal code 60611 is the demo that changes minds fastest. The fix is a
full-text index, and it lives in the same Neo4j database as the graph. The
exact-term match finds the chunk, and the traversal still attaches the hotel
behind it. Say plainly that an old idea beats the embedding here. That honesty
buys credibility for the spa-and-pool case, where only the graph can tie two
conditions to one hotel.
-->

---

<style scoped>
/* 5% under the default theme's 29px. A percentage here would resolve against
   the root, not the theme's section size, and shrink far more than 5%. */
section { font-size: 27.55px; }
</style>

## The Shift to GraphRAG

A knowledge graph stores each hotel as a record and stores the links between records. This amenity belongs to that hotel. That policy governs this room. This fact came from that document.

- **Connected, verifiable facts:** the graph stores facts you can check, not pattern-matched chunks
- **Traversal on top of similarity:** a traversal reaches context that a vector search cannot
- **Traceable:** every answer walks back to the document behind it
- **Fewer tokens:** the graph returns the facts the answer needs, not everything that looked similar
- **Governed retrieval:** the application fixes the traversal, and the model does not choose it

The agent answers from evidence the graph can defend.

<!--
The last bullet is the one that separates this workshop from a generic
GraphRAG talk, and it comes back on slide 8. In most demos the model decides
what to fetch. Here the application decides, once, and the model never gets
that choice.
-->

---

<style scoped>
/* Five bullets, a lead-in, a closing line, and a source line at the theme's 29px. */
section { font-size: 24px; }
</style>

## The Evidence

The UK's National Innovation Centre for Data ran 510 complex questions. Some needed hundreds of steps. Neo4j sponsored the study. NICD ran it.

- **80% more truthful:** 63 against 35 on the study's truthfulness score, which penalizes hallucination
- **Over 2x precision and recall:** precision 0.38 against 0.18, recall 0.35 against 0.15
- **Half the refusals:** vector-only declined 71% of the questions, and GraphRAG declined 35%
- **Fewer tokens per correct answer:** the retriever fetches sections, not whole documents
- **No ontology project:** the graph was built from the titles, sections, and links the documents already carried

GraphRAG answered more than twice as many questions, and it answered them more truthfully.

<small>Source: [Independent study: GraphRAG makes AI agents 80% more truthful](https://neo4j.com/blog/agentic-ai/study-graphrag-ai-agents-80-percent-more-truthful/), Neo4j</small>

<!--
Full NICD report: neo4j.com/whitepapers/nicd-reducing-hallucinations-graphrag/

Two points to land in the room:

The refusal number is the one that changes minds. Vector-only RAG mostly fails
by declining, not by lying, so teams who have only measured hallucination rate
think their system is fine. Ask how useful an assistant is that shrugs at two
out of three real questions.

The last bullet answers the objection that always comes: a graph means a
six-month data modeling project. NICD hand-engineered nothing, and Module 1
does the same thing to the hotel documents with a pinned schema.
-->

---

## Grounding Is More Than Retrieval

Graph retrieval decides what the model sees. Grounding decides what it is allowed to do with it.

- **Two bounded read tools:** both tools read only from the graph. The model routes by tool name, description, and input schema
- **Answer from graph evidence:** the prompt limits hotel answers to facts a read tool returned from the graph
- **Expose missing facts:** both read tools return the same structured verdict, which names any fact the graph does not hold
- **Application-owned writes:** the model proposes an action. Application code validates it, and Neo4j enforces the rule inside the write transaction

<!--
This slide has no equivalent in most GraphRAG decks, and it is the one that
distinguishes this workshop. Everything after it is an implementation of these
four rules.

Point out which statements are policy and which are mechanisms. The prompt
directs answer behavior. Tool input validation, the Text2Cypher read-plan guard,
and the reservation transaction are enforced in code or the database.

Module 3 demonstrates all four in one notebook: automatic tool selection with a
trace, structured evidence and verdicts, an unsupported availability case, and
a rejected fifteen-guest reservation. A plain BedrockModel chooses from the
registered tool specifications.
-->

---

## The Hero Question

> Which Chicago hotel has both a spa and a swimming pool, what is its cancellation policy, and can I submit a booking request for four guests?

One sentence, three different mechanisms:

- **The spa and the pool:** a Cypher template tests both conditions on the same hotel. Similarity cannot guarantee it
- **The cancellation policy:** hybrid retrieval finds the passage, a graph traversal attaches the hotel and its source document
- **The hold for four guests:** a reservation command validates the guest count, and Neo4j enforces the limit in the write transaction

Add a fourth question, "is a room free tonight," and the graph shows it holds no availability data. The agent declines instead of guessing.

<!--
This question runs through decks 4, 5, 6, and 7 word for word. Do not
paraphrase it later. The repetition is what makes the arc legible.

The fourth line matters as much as the first three. Every attendee has been
asked to build an agent that answers everything, and the useful discipline is
knowing which questions the data cannot support. Module 3 makes the agent
refuse this one on purpose.
-->

---

## Opening Demo

See the finished build answer the hero question live.

Then we look at the six modules that build it, and who owns each control.

<!--
Instructor run instructions:

Run the hero question against the pre-deployed Module 5 AgentCore Runtime
agent, deployed before the event against the instructor's own Aura instance:

"Which Chicago hotel has both a spa and a swimming pool, what is its
cancellation policy, and can I submit a booking request for four guests?"

Show the tool calls, not just the answer, so the room sees the retrieval
happen. Then ask the availability question and let it refuse. The refusal
gets more comment than the answer, every time.

Keep the runtime live all day so attendees can invoke it during breaks. Point
back to this demo from each module: Module 1 builds the graph behind it,
Module 2 chooses its retriever, Module 3 grounds it, Modules 4 and 5 deploy
it, Module 6 gives it memory.
-->

---

<style scoped>
/* A numbered list of six plus one closing line. */
section { font-size: 24px; }
</style>

## What You Will Build

Six modules, six verbs:

1. **Build** a knowledge graph from hotel documents into your own Aura instance
2. **Compare** eight retrieval patterns and identify complementary question shapes
3. **Ground** an agent in two bounded read tools, and keep its write path separate
4. **Publish** the retrieval tools through AgentCore Gateway, on the Model Context Protocol
5. **Deploy** the whole agent to AgentCore Runtime as a container
6. **Remember** guest preferences in the same graph, with provenance

Modules 3, 4, and 5 reuse the same boundaries while packaging their tools differently.

<!--
This deck's thesis, restated: the model does not get smarter across these six
steps. What changes is what it can see and what it is allowed to do.

Say the grouping out loud, because it saves questions later. Modules 1 and 2
are where the day's understanding gets built. Modules 3, 4, and 5 are the same
design deployed three ways, so nobody should spend Module 5 wondering why the
Gateway disappeared. If you fall behind, 4 and 5 are the ones to demonstrate
rather than have everyone run.
-->

---

![bg contain](../images/foundations-grounded-request-flow.svg)

<!--
Walk this end to end, once, slowly. It is the only time today the whole path
is on one slide.

A question arrives at the Strands agent running a model on Bedrock. The model
reads two tool specifications. It can choose passage search, which uses Nova,
the vector and full-text indexes, and a reviewed traversal, or a structured
record query, which adds a model call to generate Cypher and an `EXPLAIN`
read-plan check. Bounded evidence and a shared verdict come back to the model.

The reservation write is not on this path at all. It runs beside the agent,
and the next slide is where you say who owns it.

The packaging changes across later modules. Module 3's key lesson is the
model-driven choice between two local read tools.
-->

---

<style scoped>
/* Six rows of three-column prose. */
section { font-size: 21px; }
</style>

## The Model Chooses Inside Guarded Boundaries

| Decision or constraint | Owner |
|---|---|
| Which read tool fits the question | The model, from two tool specifications |
| Passage-search configuration and traversal | Application code, fixed inside `search_hotel_passages` |
| Whether generated Cypher has a read plan | The `EXPLAIN` guard, backed by a read-only database identity in production |
| Whether live availability is supported | The shared tool verdict, computed from the question and graph boundary |
| Rejecting an invalid or duplicate write | Neo4j, inside the reservation transaction |
| Who can call AWS services | IAM, on the execution role |

The model routes and writes prose. Code and the database own the hard constraints.

<!--
This is the control-ownership correction to emphasize. Module 3 deliberately
returns one decision to the model: which evidence shape fits the question.

The passage tool still owns a fixed retrieval configuration. The structured
tool does allow a model to generate Cypher, but the query is returned for
inspection and Neo4j runs it only after the planner reports a read plan. A
valid read query can still have the wrong meaning. The plan check is a safety
boundary. Semantic validation remains a separate responsibility.

The availability verdict is deterministic data from the tool. The final prose
and whether the agent follows its prompt remain model behavior, which the lab
observes through traces rather than claiming to enforce.

This table reuses cleanly with a different schema and a different domain, which
is the takeaway to name out loud.

Next is what a knowledge graph actually is. Setup follows that deck.
-->
