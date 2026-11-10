---
title: "AWS GenAI Services"
weight: 3
---

AWS provides the model and application infrastructure around the Neo4j graph.
The workshop starts with models on Amazon Bedrock, builds an agent with Strands,
then uses Amazon Bedrock AgentCore to expose tools and host the agent. Lambda,
Secrets Manager, IAM, ECR, and CloudWatch support the production path.

| Capability | Service or component | Workshop use |
|---|---|---|
| **Reasoning and extraction** | Claude on Amazon Bedrock | Extract graph structure, select tools, and generate grounded answers |
| **Embeddings** | Amazon Nova 2 Multimodal Embeddings and Amazon Titan Text Embeddings V2 | Index hotel text for retrieval and encode graph memory |
| **Agent loop** | Strands Agents SDK | Give the model typed tools and execute its tool calls |
| **Remote tools** | AgentCore Gateway and AWS Lambda | Publish the two read tools as Lambda functions through IAM-authenticated MCP |
| **Agent hosting** | AgentCore Runtime | Run the packaged booking agent as an invocable service |
| **Security and operations** | IAM, SigV4, Secrets Manager, ECR, and CloudWatch | Authorize calls, protect Neo4j settings, store the image, and observe the deployed path |

---

## Amazon Bedrock

Amazon Bedrock gives application code managed API access to foundation models.
The workshop uses model calls for three different jobs:

- **Extraction:** A model maps hotel documents into a fixed graph schema.
- **Reasoning:** A model reads the agent's tool specifications, chooses a tool, and writes an answer from the returned evidence.
- **Embeddings:** Embedding models turn text into vectors that Neo4j indexes for semantic retrieval and memory recall.

Model output is not treated as the system of record. Neo4j stores the graph,
and application or database controls own the rules that must be enforced.

---

## Strands Agents

Strands is the agent SDK used in the notebooks and in the deployed Runtime
container. It combines a Bedrock-backed model, a system prompt, and a list of
tools. For each request, the model can answer, call one of those tools, inspect
the result, and continue until it has a final response.

The workshop deliberately keeps its two read tools narrow:

- `search_hotel_passages` returns source text plus connected hotel context.
- `query_hotel_records` returns structured records from planner-checked Cypher.

The same model-facing interfaces work as local Python tools and as remote MCP
tools behind AgentCore Gateway.

---

## Amazon Bedrock AgentCore

Three AgentCore capabilities matter to this architecture:

- **Gateway:** Gateway presents Lambda functions as MCP tools and authenticates requests with IAM. Module 4 uses this path.
- **Runtime:** Runtime hosts the packaged Strands agent and exposes it through `InvokeAgentRuntime`. Module 5 uses this path.
- **Memory:** AgentCore Memory provides the managed memory alternative discussed in Module 6. The hands-on lab implements graph memory in Neo4j instead.

Gateway and Runtime belong to separate deployment patterns in this workshop.
In Pattern B, the Module 4 agent runs in the notebook and calls remote tools
through Gateway. In Pattern C, the Module 5 agent runs on Runtime and connects
to Neo4j directly.

---

## Supporting AWS Services

- **AWS Lambda:** Lambda runs the two read tools behind Gateway.
- **AWS Secrets Manager:** Secrets Manager stores the Neo4j connection settings used by those functions.
- **AWS IAM and SigV4:** IAM policies and SigV4 request signing authorize access to Bedrock, Gateway, Runtime, Lambda, secrets, and container resources.
- **Amazon ECR:** ECR stores the Module 5 container image.
- **Amazon CloudWatch:** CloudWatch captures the logs used to correlate a deployed request.

These services operate the agent path. They do not replace the graph's data
model, indexes, relationships, or provenance.

---

## Where AWS Appears in the Workshop

The [module-by-module table](../platform/#module-by-module) on How Neo4j + AWS
Work Together shows which AWS services each module uses.

## Learn More

- :link[Amazon Bedrock]{href="https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html" external=true}
- :link[Amazon Bedrock AgentCore]{href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html" external=true}
- :link[Strands Agents]{href="https://strandsagents.com/" external=true}

## Next

Continue to [Neo4j Graph Intelligence Platform](../neo4j-platform/) for the
connected knowledge and retrieval side of the stack.
