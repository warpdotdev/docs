# Positioning for Warp documentation

Use this as the canonical positioning source for Warp documentation and related explanatory copy. Names live in `.agents/references/terminology.md`; voice and content-type rules live in `AGENTS.md`. Read `.agents/references/writing-examples.md` for annotated examples, not additional product promises.

Reviewed direction: November 10, 2026. This guidance applies the Warp Positioning direction and the approved requirement to avoid anthropomorphizing agents while preserving shipped role names. Changes to that direction require human approval; examples and existing docs do not override it.

## Infrastructure framing

Warp Factories is open, flexible infrastructure on which teams build, run, measure, and improve their own software factories. A software factory is a configurable system of development workflows, not a team to hire or a fixed pipeline to adopt.

Warp's terminal and coding surface supports interactive work. The Automation Platform supplies shared execution and APIs for factories and standalone cloud agents; it is not an agent harness. The Warp Agent is the built-in harness. Explain the surface relevant to the reader's task rather than presenting every task as a factory workflow.

**Positioning rule P1:** Describe Warp Factories as infrastructure or an infrastructure platform, not as a product, an AI software engineer, or a team of agents. This applies to all explanatory definitions, including a customer's factory. Avoid equivalent staffing metaphors such as an AI teammate, workforce, or fleet of teammates. Describe configuration, routing, execution, and outputs instead.

Retain shipped role names such as foreman, triage, spec, implement, and review agents, and exact UI strings, handles, commands, and configuration keys. For example, "The foreman routes the request to the review agent" explains behavior without assigning agents personalities or employment roles.

* **Open** - Explain the supported choices that preserve customer control over models, harnesses, hosting, and data. This is not a claim that every component is open source or every configuration is supported.
* **Flexible** - Show how teams adapt workflows and select primitives for their existing tools and development process, rather than replace their systems with a fixed pipeline.
* **Infrastructure** - Teams own the workflow's behavior and continue building on Warp. The opinionated quickstart and default agents are starting points, not the definition or required scope of every factory.

Direct teams building standing development workflows to factory setup. Keep standalone tasks and supported legacy interfaces distinct. A factory can start with one bounded workflow; it need not automate every development stage. Verify workflow equivalents before moving instructions from the legacy web app or CLI.

## Reader needs and supported positioning

Overviews orient the reader with relevant capabilities and a concrete example. Procedures and quickstarts explain choices, consequences, and success. Do not require a pillar mention in every article.

* **Choice of models and harnesses** - Help developers select a supported model, harness, and tools. Link compatibility and plan constraints rather than promising any combination.
* **Visibility and intervention** - Explain how to inspect runs, steer work, and take it over locally. Describe the controls the reader uses, not the architecture behind them.
* **Incremental adoption and configuration** - Start with a bounded request and verification command, then link definitions as code and advanced configuration. Do not derive completion times from marketing claims.
* **Team workflows** - Explain how work enters from existing tools, where results return, and who needs access. Developers building the workflow need setup detail; engineering leaders need ownership and measurement context.
* **Developer control** - Distinguish editable workflow instructions from enforced permissions. Identify human review and merge ownership, rather than promising safety or autonomy without constraints.
* **Measurement and improvement** - Connect measurement to a reviewable improvement loop: evaluate work, compare a candidate, review a change, and monitor the result. Explain the available controls for quality, cost, and governance, not guaranteed ROI, savings, or proof that every run is scored.

For example, replace “Configure once and every trigger uses it” with the verified configuration scope and a link to its owning reference. Replace “seamless local-to-cloud workflows” with the specific handoff action and what state it preserves.

## Evidence boundaries

**Evidence rule P2:** Positioning sources establish framing, not shipped behavior, availability, deployment, migration guarantees, or typical customer outcomes. Verify model and harness compatibility, hosting and data controls, and feature availability against the owning technical sources. Do not turn strategic choice language into universal model or harness support, or use positioning as evidence for competitor claims. Keep dated customer results tied to their source and scope; forecasts, sample dashboard values, and launch targets are not current facts.

Correct an unsupported promise narrowly. Retain a transition page's explanation and valid legacy commands; removing a page or changing its purpose requires human approval. No replacement deadline, automatic-transfer policy, or blanket compatibility guarantee is established by this guidance.
