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

## Repair the linked reader journey

Read an entrance, its first-use procedure, and its next step together. A clear
definition doesn't help if the next page makes the reader assemble every
component before trying one task.

For example, an overview can offer "Review a PR" with its input, returned
findings, human merge decision, and editable review criteria. The quickstart
gets one small result; its next step changes one instruction and compares a
fresh trial. Keep file syntax in the reference, linked from configuration.

## Replace reassurance with an editable action

| Before | Better instruction |
| --- | --- |
| "You stay in control." | "Edit the review criteria, test them on a sample PR, and inspect the findings before widening the trigger." |
| "Rules enforce security practices." | "Write agent instructions in Rules; restrict access with permissions and enforce repository checks in CI." |
| "Generate a production-ready Docker setup." | "Containerize one named service, review image and secret choices, then build and check its application behavior." |
| "Every correction becomes an improvement." | "Read the correction in context, test a scoped change against the baseline and held-out cases, then review the proposal." |

Keep the scope and stop inside a copyable prompt. A warning outside the prompt
doesn't travel with it. Name required tools and access separately; instructions
don't install dependencies or grant permissions.

## Turn a recording into a lesson

Keep the demonstrated task, not transcript provenance or an application's full
generated Rules file. Explain what to supply, one useful edit, and how to check
the result. Label recorded counts as observations. If a request asks for 2,000
logs but the output summarizes 1,000, teach the reader to check the query and
coverage rather than presenting both as a successful result.

## Check the genre before judging the narrative

For an overview or tutorial, check whether the reader can identify the outcome,
the action they own, its limits, and the evidence needed to continue. For a
reference, judge lookup accuracy and usable examples; a field table doesn't
need an outcome story. Security detail can be necessary to a deployment
decision, and a terminal how-to doesn't need factory positioning.

For each narrative finding, record a quote or missing step, its reader impact,
and a concrete fix. Mark a dimension not applicable when the genre doesn't
need it. Keep factual, availability, and compliance checks as hard gates:
strong voice doesn't offset a wrong command or unsupported promise.

## Calibration follow-up

Use less-coached, real-page inputs alongside editing exercises. The copy-pass
manifest includes baseline quickstart, router, and terminal pages without
embedding the desired rewrite in their feedback. Reserve them from prompt
tuning; report any later exposure before calling them held-out.

For a separate journey check, use the overview → quickstart → tuning path and
the GitHub Actions series → factory quickstart path at a pinned revision.
Check whether each next link serves the reader's next decision and whether
the two orchestration paths remain distinct. A single-page concision score
can't establish that.

Keep baseline and candidate inputs identical, including verified source facts.
Assess context loading separately from writing quality. Fixtures without those
facts test copy consistency, not factual correctness. These checks don't
authorize a paid evaluation or live scorer activation.
