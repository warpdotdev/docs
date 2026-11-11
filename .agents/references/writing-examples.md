# Reference writing examples

Use these examples alongside `AGENTS.md` and `.agents/rules/warp-positioning.md`.
They illustrate writing choices, not verified feature availability or approval
of every sentence on the source page. Reviewed November 10, 2026.

## Start with the reader's problem

Zach Lloyd's [Don't vibe code your software factory](https://www.warp.dev/blog/build-production-software-factory)
(November 4, 2026) starts with the limits of prompt-only factory setups, then
explains configuration, orchestration, and measurement through a Sentry workflow.
The mechanism answers a practical question before the component inventory.

For docs, write "Configure an automation to investigate new Sentry alerts,"
then name the trigger, receiving agent, and expected output. Do not start with
"Our orchestration layer offers a comprehensive set of capabilities."

## Explain ownership and a measurable decision

Zach Lloyd's [The Factory Stack](https://www.warp.dev/blog/the-factory-stack)
(September 5, 2026) connects definitions as code to versioning, testing, and
improvement. His [Tactics for rolling out software factories](https://www.warp.dev/blog/rolling-out-software-factories)
(October 15, 2026) makes shipped quality and customer impact the goal, rather
than automation or token consumption alone.

For docs, explain what a reader can configure and compare: "Compare two
configurations on the same tasks before changing the model used for that
workflow." Do not promise that changing a model will lower costs or raise quality.

## Show the mechanism with a bounded example

Ben Holmes's [Terraform for agents](https://www.warp.dev/blog/software-factory-as-code)
(September 30, 2026) explains what configuration files let people change before
walking through the files. His [7 core components for building a software factory](https://www.warp.dev/blog/7-ways-to-build-a-software-factory)
(October 29, 2026) ties shared configuration and benchmarks to the organization's
own work. These are Ben's articles, not examples of Zach's personal authorship.

For docs, define a resource in plain language, show one relevant example, then
link to its reference. Keep the default workflow a starting point rather than
the definition of every factory.

## Keep the infrastructure identity explicit

The [Factories landing page](https://www.warp.dev/factories) and
[Warp homepage](https://www.warp.dev/) lead with infrastructure, code-based
configuration, and measurement.

For docs, "Warp Factories provides infrastructure for building your own software
factory" establishes the relationship. "A factory is a team of cloud agents"
does not. "The foreman routes the request" is a precise description of a role,
not a reason to describe agents as employees or teammates.

## Adapt the writing to documentation

Borrow plain statements, explicit reasoning, concrete examples, and attention
to tradeoffs. Do not impersonate an author, invent customer conversations, or
copy first-person anecdotes, launch slogans, predictions, and calls to buy.
Procedures need actions and observable results; references need exact lookup
information, not a story.

Some source pages contain broad compatibility, data-location, automatic-scoring,
or savings claims, and some retain product or staffing metaphors. Those do not
override the positioning rule or prove technical behavior. Verify a factual
claim against its owning technical source and deployed scope, not a blog.

## Calibration follow-up

The current authoring fixtures explicitly provide the desired framing and are
editing exercises, not proof that writers loaded this guidance. During the
planned calibration, add a less-coached task that relies on the repository
rules without restating the expected answer. Keep baseline and candidate
inputs identical and assess context loading separately from writing quality.
This follow-up does not authorize a paid run or live scorer activation.
