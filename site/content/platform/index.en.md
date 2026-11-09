---
title: "How Neo4j + AWS Work Together"
weight: 1
---

AWS and Neo4j provide complementary parts of a grounded AI system. AWS supplies
foundation models, agent infrastructure, identity, serverless compute, and
operations. Neo4j supplies the connected knowledge layer that those agents
query: facts, source text, relationships, retrieval indexes, business rules,
provenance, and memory.

This workshop connects the two platforms around one booking agent. The agent
uses models on Amazon Bedrock to reason, uses Strands to select tools, and uses
Neo4j to retrieve evidence and enforce graph-backed rules. AgentCore then moves
those tools and the agent from a notebook into managed AWS endpoints.

| Component | Primary job in this workshop |
|---|---|
| **AWS** | Run reasoning and embedding models, authenticate callers, expose remote tools, host the deployed agent, execute Lambda functions, and operate the system |
| **Neo4j** | Store the hotel knowledge graph, combine semantic and exact retrieval with graph traversal, return provenance, run transactional booking checks, and store auditable memory |
| **Strands Agents** | Present application-defined tools to the model and run the tool-selection loop across the two platforms |

AWS provides the models and application infrastructure that interpret requests,
run tools, secure access, and host the agent. Neo4j stores and retrieves the
authoritative hotel facts, relationships, provenance, booking rules, and memory.

---

## One Grounded Request Across Both Platforms

:image[A grounded request moves through an AWS-hosted agent and tools to Neo4j, then returns connected evidence and provenance]{src="../../images/neo4j-aws-together.svg" width=800}

1. **A guest asks a question.** The request reaches a Strands agent locally or on AgentCore Runtime.
2. **Amazon Bedrock reasons over the request.** The model chooses between bounded tools rather than querying infrastructure directly.
3. **The tool reaches Neo4j.** It can connect directly with a Neo4j driver or run through AgentCore Gateway and Lambda.
4. **Neo4j returns connected evidence.** Vector and full-text indexes find source text, while Cypher adds hotel facts, relationships, and provenance.
5. **The model writes the answer.** The prompt requires the answer to use the returned evidence or state what is missing.
6. **Application commands and memory remain explicit.** The reservation command checks its rules inside a Neo4j transaction. Agent memory stores actor-scoped preferences with links to their source.

---

## Module by Module

The division of labor stays consistent as the workshop progresses. What changes
is where the agent and tools run.

| Module | AWS role | Neo4j role |
|---|---|---|
| **Setup** | Verify AWS credentials, region, and Bedrock model access | Create AuraDB, restore the workshop graph, and verify connectivity |
| **1. Build the Graph** | Bedrock models extract structure into a fixed schema and create embeddings | AuraDB stores documents, chunks, entities, relationships, constraints, vector and full-text indexes, and provenance |
| **2. From Vector Search to Graph-Enriched Retrieval** | Nova creates query embeddings. Claude writes Cypher for the optional Text2Cypher path | Vector, Hybrid, VectorCypher, and Text2Cypher retrieval patterns return bounded evidence with provenance |
| **3. Build a Grounded Booking Agent with GraphRAG** | Bedrock reasons through a local Strands agent that selects a read tool | The read tools return connected evidence. The reservation command checks the 10-guest rule and writes the request in one transaction |
| **4. Production Agent with AgentCore** | AgentCore Gateway authenticates MCP calls with IAM SigV4 and invokes Lambda. Secrets Manager stores the Neo4j settings | Lambda tools query the same graph through the Neo4j driver |
| **5. Deploy to AgentCore Runtime** | ECR stores the container image. AgentCore Runtime hosts the packaged Strands agent. CloudWatch captures its logs | The deployed agent connects directly to AuraDB as its knowledge service |
| **6. Neo4j Graph Memory** | Titan creates the memory embedding. IAM controls access to the model. AgentCore Memory serves as the managed comparison | Neo4j stores actor-scoped preferences with their source messages and domain links. The application can correct a stored preference |

---

## AWS Connection Patterns for Neo4j

The connection pattern is a top-level architecture choice. Choose it based on
how data moves and who needs to use the graph.

| Connection pattern | Use it when | Data or request path |
|---|---|---|
| **Neo4j drivers in AWS applications** | Application code running in AWS Lambda, Amazon ECS, Amazon EKS, Amazon EC2, notebooks, or AgentCore needs transactional Cypher access | Application ↔ Neo4j |
| **MCP tools for agents** | An MCP-compatible agent needs discoverable graph tools behind a standard tool protocol | Agent → graph tools → Neo4j |
| **Neo4j Connector for AWS Glue** | A managed ETL job needs to move data from Amazon S3, Amazon RDS, Amazon Redshift, Amazon DynamoDB, or another Glue source into a graph pipeline | AWS data sources → Neo4j |
| **Spark Connector on Amazon EMR** | Large Spark DataFrames need bulk reads or writes | Spark ↔ Neo4j |
| **Kafka Connector on Amazon MSK** | Event streams need continuous graph updates or Neo4j changes need to reach Kafka topics | Kafka ↔ Neo4j |

This workshop implements two of these connection patterns directly:

- **Direct driver:** Modules 1 through 3 and Modules 5 through 6 connect Python application code to Neo4j.
- **MCP and Lambda:** Module 4 exposes the two read tools as Lambda-backed tools through an IAM-authenticated AgentCore Gateway.

The data-pipeline connectors solve a different problem from the agent path.
Glue, Spark, and Kafka move or synchronize data. Drivers and MCP serve live
application and agent requests. A production architecture can use both.

Read the Neo4j documentation for :link[data connectors]{href="https://neo4j.com/docs/connectors/" external=true}, the :link[Spark Connector]{href="https://neo4j.com/docs/spark/current/" external=true}, the :link[Kafka Connector]{href="https://neo4j.com/docs/kafka/current/" external=true}, and :link[MCP]{href="https://neo4j.com/developer/genai-ecosystem/model-context-protocol-mcp/" external=true}.

## Next

Continue to [AWS GenAI Services](../aws-services/) for the AWS side of the stack.
