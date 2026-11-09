# Workshop Site Review: Suggested Changes

This review reads the site in `site/content` as a learner would and checks each claim against the notebooks and the `workshop` package. Every item below was confirmed in the source unless it is marked **Needs check**. The in-progress rewrite of "The Goal", "The Final Objective" and "The Final Architecture" on the home page, and the new "A Unified Target Architecture" section on the Production Path page, are not treated as errors. Comments on how they fit the flow appear where relevant.

## Errors

### 1. The workshop challenge is never answered, and its booking cannot succeed

- **Where:** `site/content/index.en.md:33`.
- **What is wrong:** The home page sets the Chicago spa, pool, cancellation and four-guest booking question as the workshop challenge. No module asks an agent this question. The booking part cannot work for any Chicago hotel.
- **Evidence:** Only `hotel-cairo-001` and `hotel-cairo-002` are booking fixtures in `notebooks/workshop/hotel_ids.json` and `fixtures.py`. `reservation_command.py` returns `unknown_hotel` with "Hotel is not a prepared workshop fixture." for every other hotel. The Module 3 agent has two read tools and no write tool. Module 3 and Module 5 ask Cairo questions instead. Module 2 uses the Chicago question only as a filter example, where it finds Lakeview Horizon Suites.
- **Fit note:** The in-progress "Final Objective" at `index.en.md:76-96` repeats this promise in more detail. It says the agent "answers the challenge question end to end", including the booking. That rewrite will inherit the same gap.
- **Fix:** Pick one of two options. The first option reframes the challenge around the Cairo hero hotel, which every module already uses. The second option adds a Chicago booking fixture and a final notebook cell that runs the full question against the Module 5 agent.

### 2. "The hotel's guest limit" does not match the code

- **Where:** `site/content/neo4j-platform/index.en.md:33-34`. The in-progress `index.en.md:88` uses the same wording.
- **What is wrong:** Both pages say the reservation command checks "the hotel's guest limit". That implies each hotel has its own limit.
- **Evidence:** The code enforces one global `Rule` node. `contracts.py` sets `MAX_GUESTS_RULE_ID = "demo-06-maximum-guests"` and `MAX_GUESTS = 10`. `fixtures.py` writes that single rule. Module 5 at line 281 and Foundations at line 102 say "the guest limit", which is accurate.
- **Fix:** Change the wording to "the workshop's guest-limit rule" or "the guest limit".

### 3. Module 4 says Workshop Studio removes resources

- **Where:** `site/content/04-production-agent/index.en.md:538`.
- **What is wrong:** The page says "Workshop Studio removes them when the event ends." The hosted path is now Vocareum.
- **Evidence:** The Setup page lists only Vocareum and own-account paths. `.gitignore` marks the Workshop Studio files as retired. Module 5 at lines 187-188 already says the Vocareum lab account goes away.
- **Fix:** Replace "Workshop Studio" with "The Vocareum lab account".

### 4. Module 2 names a notebook cell that does not exist

- **Where:** `site/content/02-connected-context/index.en.md:341`.
- **What is wrong:** The page tells learners to look for a "**Verify the prepared graph**" cell.
- **Evidence:** The notebook `2.1_connected_context.ipynb` has the headings "Check that Module 1 finished" and "Check that the graph has the required data". No cell uses the name on the page.
- **Fix:** Use the notebook's actual heading, "Check that the graph has the required data".

### 5. The navigation order contradicts the page order

- **Where:** `site/nav.adoc:2-9`.
- **What is wrong:** The sidebar places Setup directly after Home. Every other signal places Setup after Foundations.
- **Evidence:** The page weights are platform 1, aws-services 2, neo4j-platform 3, foundations 5 and setup 10. The "Workshop Flow" table at `index.en.md:49-51` lists Platform overview, Foundations, then Setup. The Foundations page ends with "Head to [Setup](../setup/)." The slide order in `site/scripts/build-slides.mjs` pairs the Foundations deck before the Setup deck.
- **Fix:** Move the Setup block in `nav.adoc` below Foundations. The other option is to move Setup first everywhere else. Either way, the sidebar and the "Next" links should agree.

### 6. The Vocareum environment is named three different ways

- **Where:** `site/content/index.en.md:136`, `site/content/setup/index.en.md:22` and `site/content/setup/vocareum-access/index.en.md:10`.
- **What is wrong:** The home page says "Vocareum's JupyterLab environment". The Setup table says "Vocareum gives you JupyterLab". The Vocareum page tells learners to launch the "**Visual Studio Code**" environment.
- **Evidence:** The three lines quoted above.
- **Fix:** Confirm which environment the lab actually launches. Then use that name on all three pages.

### 7. Vocareum page says Module 6 creates AWS resources

- **Where:** `site/content/setup/vocareum-access/index.en.md:15`.
- **What is wrong:** The page says "Modules 4, 5, and 6 create AWS resources".
- **Evidence:** Module 6 writes memory into Neo4j and calls Titan embeddings. It creates no AWS resources. The own-account setup page says only Modules 4 and 5 create resources.
- **Fix:** Change the sentence to "Modules 4 and 5 create AWS resources".

### 8. Module 6 credits the hero hotel to Module 1

- **Where:** `site/content/06-neo4j-memory/index.en.md:68` and line 149.
- **What is wrong:** Line 68 says "the Hotel node Module 1 created". Line 149 says the nodes keep "the labels and properties Module 1 gave them".
- **Evidence:** Module 6 uses AnyCompany Cairo Nile View. That hotel comes from the restored dump. Module 1 extracts only the five held-out documents for Tokyo, Sydney, Rio de Janeiro, Cape Town and Prague, per `graph_config.HELD_OUT_DOCUMENTS`. The docstring in `held_out_documents.py` says the Cairo hotel was kept out on purpose.
- **Fix:** Replace "Module 1" with "the restored graph" on both lines.

### 9. Setup says agents start in Module 2

- **Where:** `site/content/setup/index.en.md:37`.
- **What is wrong:** The model table says Claude runs "every agent from Module 2 onward".
- **Evidence:** Module 2 has no agent. It uses Claude only for Text2Cypher. The first agent is built in Module 3.
- **Fix:** Change the cell to "Extraction in Module 1, Text2Cypher in Module 2, and every agent from Module 3 onward".

### 10. Module 2 has four different titles

- **Where:** `site/content/02-connected-context/index.en.md` title, `site/content/index.en.md:53`, `site/content/summary/index.en.md:17` and `site/nav.adoc:13`.
- **What is wrong:** The page title is "Compare GraphRAG Retrieval Paths". The home table and Summary say "From Vector Search to Graph-Enriched Retrieval". The sidebar says "Graph-Enriched Retrieval". The notebook says "Compare GraphRAG Read Paths".
- **Evidence:** The four sources listed above.
- **Fix:** Pick one title and use it in all four places.

### 11. The home page promises AgentCore content on Foundations

- **Where:** `site/content/index.en.md:50`.
- **What is wrong:** The table says Foundations covers "service responsibilities, and AgentCore capabilities".
- **Evidence:** The Foundations page has no AgentCore section. AgentCore capabilities are covered on the AWS GenAI Services page.
- **Fix:** Remove "and AgentCore capabilities" from the Foundations row. Mention AgentCore in the Platform overview row instead.

### 12. Needs check: Module 6 says the setup check expects the memory indexes

- **Where:** `site/content/06-neo4j-memory/index.en.md:305`.
- **What is wrong:** The page says "the workshop's setup check expects them".
- **Evidence:** `environment/verify.py` has no memory-index check. `cleanup_memory.py` says "the smoke test checks them", which may refer to a test outside the learner path.
- **Fix:** Confirm which check reads the memory indexes. If no learner-facing check does, drop the clause.

### 13. Aura setup says `verify.py` runs later for everyone

- **Where:** `site/content/setup/aura-free-setup/index.en.md:73`.
- **What is wrong:** The page says this is "the same check `environment/verify.py` runs later".
- **Evidence:** Only the own-account path runs `verify.py`. Vocareum learners run `1.0_verify_environment.ipynb`, which checks AWS and Bedrock only.
- **Fix:** Say "the own-account path runs the same check in `environment/verify.py`". Item 1 under Walkthrough Improvements covers the larger gap.

## Walkthrough Improvements

Ranked by impact on a learner.

1. **Give Vocareum learners a Neo4j check.** The notebook `1.0_verify_environment.ipynb` checks only AWS and Bedrock. A Vocareum learner with a wrong `NEO4J_URI` first finds out in Module 1 or Module 2. The Setup page at line 25 says "Both paths end at the same place", but only one path verifies Neo4j. The Setup troubleshooting also refers to "the script" and to `uv pip install`, which do not apply on Vocareum. Add the hero-hotel check from `verify.py` to the 1.0 notebook. The other option is to tell Vocareum learners to run `verify.py` from the terminal.

2. **Carry the challenge through the modules.** The challenge question appears on the home page and in the slides. No module returns to it. A short "Challenge checkpoint" at the end of Modules 2, 3 and 5 would show which part of the answer each module unlocks. This depends on the fix chosen for Error 1.

3. **Map the Module 2 page to the notebook.** The page has sections 1 through 8. The notebook has sections 1 through 5. Page sections 3 and 4 explain full-text search, but no notebook cell runs them on their own. A small table that maps page sections to notebook sections would remove the guesswork. The VectorCypher explanation at lines 105-145 also shows a core query, then says "the shipped query" uses a subquery. Showing the shipped query, or labeling the first one as simplified, would avoid that confusion.

4. **Tidy the Module 3 structure.** The section "Route Questions by Evidence Shape" shows a "Query 2" with no "Query 1". The instruction to open the notebook sits mid-page at line 125. Modules 2, 4 and 5 have a "Run It" section and a time estimate. Module 3 has neither. Adding both would make Module 3 match the others.

5. **Reduce repetition in the opening pages.** The Platform, AWS GenAI Services, Graph Intelligence Platform and Foundations pages each carry a module-by-module table. Each one restates the two read tools. The property graph is explained on both the Graph Intelligence Platform page and Foundations. The image `01-graph-structure.svg` appears on four pages. The AgentCore Memory versus Neo4j table appears in Module 6, the Summary and the Production Path. A learner reads the same material four times before Module 1 starts. Keep one module table and one graph explanation, and link to them from the other pages.

6. **Say "alternatives" consistently for Modules 3 to 5.** Module 4 at line 509 and the AWS GenAI Services page explain that the three deployments are alternatives, not a pipeline. The home page at lines 60-61 says the sequence "moves the retrieval capabilities from local tools into production deployment patterns", which reads as a pipeline. Wrap-up line 6 says "from source documents through production deployment". The in-progress home page introduces Pattern A, B and C labels. Using those labels in the Module 3, 4 and 5 introductions would tie the pages together. This also fits the new "A Unified Target Architecture" section well.

7. **Collect cleanup in one place.** The home page cost alert at line 141 says "Follow the cleanup instructions at the end". The cleanup inventory is on the own-account setup page, not at the end. Wrap-up has no cleanup section. Module 6 cleanup is opt-in. Add a short cleanup section to Wrap-up that links to the inventory and to the Module 6 cleanup cell.

8. **Settle the terminology.** Module 6 defines "actor", while the Graph Intelligence Platform page says "User node" and other pages say "guest". The tools are called "read tools", "retrieval tools" and "Gateway tools" on different pages. "Pattern" means a GraphRAG retrieval pattern in Module 2 and a deployment pattern in the new home page. Pages also switch between "Module 3" and "Module 3.1". A short glossary on Foundations, plus one term per concept, would help.

9. **Name the eight keys in Module 4.** Module 4 at line 14 says the tool "returns the same eight keys". The keys are never listed on that page. Module 3 lists the five envelope keys instead, so the count does not match anything the learner has seen. List the eight `HotelContext` keys from `contracts.py`, or link to where they appear.

10. **Label the Module 4 handler as simplified.** The handler snippet at lines 104-125 differs from `lambda_function.py`. The real handler uses `_validated_query` and `INVALID_QUERY_MESSAGE`. A learner who opens the file will see different code. Add one sentence saying the snippet is simplified.

11. **Foreshadow the unified target architecture.** The new Production Path section fits well after the paragraph at lines 76-78. The Summary could point ahead to it in one sentence, so the learner expects one combined target after three separate patterns.

12. **Trim the repeated Aura step.** The Setup page tells learners to create the Aura database first. Step 3 of the Vocareum page repeats that step. The repetition is harmless, but Step 3 could become a single link back to the Aura page.

## Style Notes

These are low priority. The search for em-dashes in `site/content` found none.

- **Explanatory parentheses:** A rough search finds about 25 prose lines with parentheses. Some of them hold code and are fine. Examples are `02-connected-context/index.en.md:32` "(optional)", `02-connected-context/index.en.md:145` "(`contracts.MAX_AMENITIES`...)", `03-grounded-booking-agent/index.en.md:60` "(Reason plus Act)" and `setup/own-account-setup/index.en.md:58` "(or in `notebooks/`)".
- **Fragments after a bold label:** A rough search finds about 13 candidate bullets. Examples are `foundations/index.en.md:20-22`, where "**Node:** A thing, such as..." has no verb. `neo4j-platform/index.en.md:52-55` and `01-build-graph/index.en.md:30-34` follow the same pattern. Imperative bullets such as "**Compare retrieval:** Test..." on the home page are fine.
- **Semicolons joining two claims:** A search finds 7 prose lines with semicolons. Examples are `02-connected-context/index.en.md:34`, `03-grounded-booking-agent/index.en.md:135`, `06-neo4j-memory/index.en.md:73` and `foundations/index.en.md:111`.
- **Standalone bold labels used as headings:** Two instances. They are "**Brief overview**" at `02-connected-context/index.en.md:21` and "**Pattern reference**" at `03-grounded-booking-agent/index.en.md:12`. A real heading or plain sentence would read better.
- **Image naming:** Module 4 uses `03-agentcore-architecture.svg` and Module 6 uses `04-memory-comparison.svg`. The numbers do not match the module numbers. This does not break anything, but it confuses anyone maintaining the images.

## Suggested Priority

1. Resolve the challenge question and booking mismatch in Error 1. This also shapes the in-progress "Final Objective" text.
2. Add a Neo4j check for Vocareum learners, and fix the JupyterLab versus Visual Studio Code naming in Error 6.
3. Align the sidebar order with the page weights and "Next" links in Error 5.
4. Fix the Workshop Studio reference and the Module 6 resource claim in Errors 3 and 7.
5. Fix the missing notebook cell name in Error 4, and add the Module 2 page-to-notebook map.
6. Correct the guest-limit wording in Error 2 and the Module 1 attributions in Errors 8 and 9.
7. Settle the Module 2 title and the shared terminology.
8. Reduce the repetition in the opening pages and consolidate cleanup on Wrap-up.
9. Work through the style notes.
