# AWS Agentic AI Conference: Neo4j + AWS

Plain-English conversion of the source deck (`AWS Agentic AI Conference - Neo4j + AWS.pdf`), slide by slide. Images are not reproduced. Each image slide gets a short bullet summary instead.

---

## Slide 1: Neo4j + Databricks + AWS

Title slide. Tagline: "Data Intelligence Meets Graph Intelligence."

- **Image:** Neo4j and Databricks logos on a dark blue background with green and orange accent shapes.

---

## Slide 2: Neo4j Graph Intelligence Platform

Section title slide that introduces the Neo4j product overview section.

- **Image:** Neo4j logo on the same dark blue background style as Slide 1.

---

## Slide 3: The Power of the Label Property Graph

Neo4j stores data as nodes and relationships, and both can carry properties.

- **Nodes:** hold real-world objects, such as a Person, an Account, or a Transaction. Nodes can have properties, such as a name or a date of birth.
- **Relationships:** connect two nodes and describe an action between them, such as `:HAS_ACCOUNT` or `:HAS_TRANSACTIONS`. Relationships can have their own properties, such as the date an account was opened.
- **Direction:** every relationship points from one node to another. This shows which node acted on which.
- **Image:** a diagram showing Person connected to Account through `:HAS_ACCOUNT`, and Account connected to Transaction through `:HAS_TRANSACTIONS`, with example property values on each node and relationship.

---

## Slide 4: From Silos to Connected Context

Separate systems each hold one piece of the picture. A graph connects them so hidden context becomes visible.

- **Employees:** talent development, career management, and understanding who is who in the organization.
- **Network & Security:** identity and access management, identity resolution, reputation scoring, threat detection, and zero trust.
- **Suppliers:** route planning, real-time supply chain visibility, inventory planning, and risk analysis.
- **Process:** finding bottlenecks, improving processes, and automating and monitoring them.
- **Product:** product recommendations, new product introductions, customization, inventory, and pricing.
- **Transactions:** anti-money laundering, digital payment scam detection, credit risk assessment, and fraud detection.
- **Customers:** recommendations, loyalty programs, churn prevention, customer offers, dynamic pricing, and intelligent ads.
- **Image:** a network diagram with these seven areas as connected hubs, showing how they link into one shared graph.

---

## Slide 5: Graph Makes It Easy to Explore Hidden Patterns

A graph lets you ask three kinds of questions directly against connected data.

- **What's important:** find the most central or influential node in a network, such as the most connected person.
- **What's unusual:** spot outliers, such as one person linked to multiple emails and SSNs that other people do not share.
- **What's next:** predict a likely new connection, such as recommending a sports team based on a person's existing interests.
- **Image:** three small example graphs, one for each question, each showing people, attributes, and their connections.

---

## Slide 6: AWS + Neo4j

Section title slide. Tagline: "From Models to Knowledge."

- **Image:** Neo4j logo on the same dark blue background style as Slides 1 and 2.

---

## Slide 7: Select Neo4j and AWS Customers

A logo wall of companies that use Neo4j and AWS together.

- **Companies shown:** Adobe, Financial Times, Meredith, AstraZeneca, Novo Nordisk, Volvo, Lyft, Verizon, Novartis, LendingClub, Lockheed Martin, Comcast, Cisco, Airbus, DB (Deutsche Bahn), Levi Strauss & Co., Caterpillar, and TAG IMF.
- **Image:** a grid of company logos, no additional data.

---

## Slide 8: Five Ways AWS Connects to Neo4j

Choose the connection pattern based on how the data moves and who needs it.

- **Spark Connector on Amazon EMR:** moves large Spark DataFrames into Neo4j, and reads graph data back into Spark.
- **AWS Glue Connector:** builds managed ETL jobs that pull from S3, RDS, Redshift, DynamoDB, and other Glue sources.
- **Kafka Connector on Amazon MSK:** streams events into Neo4j, and publishes changes back out to Kafka.
- **Neo4j Drivers in AWS Apps:** let Lambda, ECS, EKS, and EC2 services run Cypher queries directly.
- **MCP for AWS Agents:** lets Bedrock and AgentCore call graph tools directly.

---

## Slide 9: Neo4j in the AWS Ecosystem

Neo4j Aura sits at the center of the AWS cloud, with data flowing in and out through several AWS services.

- **Graph Analytics, Graph Database, Explore:** the three connected parts of Neo4j Aura shown in the diagram.
- **Data in:** Amazon Managed Streaming for Apache Kafka, Amazon S3, JDBC Driver, AWS Lambda, and Amazon EMR through the Spark connector feed data into Neo4j.
- **Data out:** AWS Glue, Amazon Bedrock AgentCore, and Amazon Bedrock read from Neo4j Aura.
- **Other paths:** Amazon Redshift connects through the Spark connector, and a general database driver connects Neo4j to other AWS services.
- **Image:** a boxed AWS Cloud diagram with Neo4j Aura in the middle and arrows to each connected AWS service.

---

## Slide 10: AWS & Neo4j - Connecting Enterprise Agents to Context-Enriched Data

Three goals for the AWS and Neo4j partnership.

- **Bi-directional, scalable data pipelines:** data can move both into and out of Neo4j at scale.
- **Effortless AWS AgentCore + Neo4j integration:** AWS agents can reach graph data with little setup.
- **Accelerate innovation with GraphRAG:** graph-enriched retrieval helps AI agents give better answers faster.

---

## Slide 11: Neo4j + Amazon Quick

Section title slide that introduces the Amazon Quick integration.

- **Image:** Neo4j logo on the same dark blue background style as the other section title slides.

---

## Slide 12: GraphRAG: Graph-Enriched Retrieval

GraphRAG improves standard AI retrieval by adding graph traversal on top of search.

- **Search finds the starting points:** the system first finds the text chunks that are closest in meaning to the question.
- **Graph traversal enriches:** the system then follows entities and relationships that connect to those chunks.
- **Agents receive richer context than text search alone:** the combined result gives the AI agent more complete and accurate information.

---

## Slide 13: GraphRAG Patterns

Five patterns for building GraphRAG, arranged around a central hub.

- **Vector & Hybrid Search:** basic vector or full-text search, enhanced with graph and metadata filtering.
- **Query Templates (Deterministic):** fixed Cypher templates that match a known question shape.
- **Query Generation:** the system writes Cypher queries dynamically, also called text-to-Cypher.
- **Graph Enrichment:** adds community summaries, graph embeddings, and PageRank scores to improve results.
- **Query Optimized Graphs:** graphs built for direct querying, using hypothetical Q&A pairs and a parent-child retriever structure.
