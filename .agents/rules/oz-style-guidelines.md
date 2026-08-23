# Oz and Warp Positioning Briefing

This document provides comprehensive guidance for writing about Warp and Oz products in enterprise documentation, based on the Warp Positioning Bible and official messaging guidelines.

## Product Architecture

### What is Warp?
Warp is an AI development company with two core products:

1. **Warp terminal** - A modern terminal designed for agentic development where developers can run commands, collaborate with agents, and orchestrate autonomous work from the command line
2. **Oz** - A cloud-based orchestration platform for running, managing, and orchestrating coding agents at scale

Together, Warp and Oz form a complete **Agentic Development Environment** where local, cloud, interactive, and autonomous agents work together to help developers ship faster without losing control.

### Warp vs Warp terminal
- **"Warp"** can refer to either the company or the terminal product
- When discussing both the company and terminal product in the same context, use **"Warp"** for the company and **"Warp terminal"** for the product
- It's not necessary to always say "Warp terminal" - context determines usage

**Correct examples:**
- "Warp is a modern terminal built for coding with agents"
- "Warp is an AI development company"
- "Warp has two products, Warp terminal and Oz"

## Positioning Pillars

When writing about Warp products or features, tie back to at least one of these five positioning pillars:

1. **House of agents** - Warp is embedded in the ecosystem, supporting all the best models, CLI coding agents, and standards like Skills and AGENTS.md
2. **Integrated control plane** - Warp provides a unified set of tools to launch, orchestrate, and manage local, cloud, and autonomous agents
3. **Easy to start, but deeply configurable** - Warp works out of the box, but products are deeply customizable and programmable
4. **Collaborative by design** - Warp facilitates collaboration between developers, their teams, and their agents
5. **Developer in control** - Warp is designed to empower developers and keep them in control, not replace them

## Oz Terminology and Capitalization

### Core Terms

- **Oz** - Warp's programmable platform for running and coordinating agents at scale
- **Warp Agent** - Warp's built-in agent harness. Use "Warp Agent" when specifically referring to the built-in harness, especially when contrasting with third-party agents (Claude Code, Codex, etc.)
- **agent** - A combination of agent instructions (skill or prompt), trigger (cron, webhook, manual), environment (local, cloud), profile, and host. Can be local or cloud. Use lowercase "agent" in most contexts.
- **cloud agent** - An agent running in the cloud, from a trigger, schedule, or started from someone's local machine
- **subagent** - A child agent created by a parent agent to parallelize or delegate work
- **Oz run** - A single execution lifecycle of an agent, including actions, outputs, and logs. Always cloud-based
- **conversation** - An interactive execution lifecycle within Warp terminal, regardless of whether it's local or in the cloud
- **Environment** - The execution context for an agent, including repo access, dependencies, secrets, compute, and runtime configuration
- **Oz dashboard** - The app surface to manage all Oz runs, unified across the Warp app and web
- **Oz web app** - The web app for configuring agents and managing runs

### Capitalization Rules

**Cloud agents:**
- **Product** (capitalized): "Cloud Agent" or "Cloud Agents" when referring to Warp's specific product feature
  - "Cloud Agents send you session sharing links"
  - "Launch a Cloud Agent from the CLI"
- **Concept** (lowercase): "cloud agent" or "cloud agents" when referring to the general concept
  - "Running cloud agents lets you escape the limits of your local machine"
  - "The cloud agent architecture enables scalability"

**Other terms:**
- Use "agents" not "AI agents" (redundant)
- Use "agent" not "Oz agent" (deprecated); use "Warp Agent" only when referring to the built-in harness
- "Skills" not "skills" (capitalized)
- "AGENTS.md" not "agents.md" (all caps)

### Terms to Avoid

❌ **Don't use:**
- "Oz agent" / "Oz agents" → Use "agent" / "agents" (or "Warp Agent" / "Warp Agents" when referring to the built-in harness)
- "Oz cloud agent" → Use "cloud agent"
- "Oz subagent" → Use "subagent"
- "Oz conversation" → Use "conversation"
- "Ozzies" → Use "agents", "instances", or "subagents"
- "Deploying an Oz" → Use "Deploying an agent"
- "The Oz Agent" → Use "the agent" or "the Warp Agent"
- "Oz is running" → Use "An agent is running" or "A run is in progress"
- "AI agents" → Use "agents"
- "Warp's terminal" → Use "Warp" or "Warp terminal"

### Important Context About Oz

Oz is Warp's programmable platform for running and coordinating agents at scale, whether they are running in the cloud or running locally.

Oz exists to take agent workflows beyond a single prompt or a single laptop, making them scalable, autonomous, collaborative, and auditable.

## Target Audience: Professional Developers

Warp is for **professional developers and teams** building and maintaining production-grade software. Specific characteristics:

- Working across large, multi-repo systems
- Using the command line daily
- Not terminal nerds
- Full-stack developers, DevOps engineers, data scientists, ICs, tech leads

While students, designers, and product managers may use Warp, they are not our core audience.

## Messaging by Audience

### For End Users (PLG)
Emphasize:
- Parallel agent workflows
- Automating tasks they don't want to do
- Building apps on top of agents
- Scaling beyond what their laptop can support
- Focusing more on work they enjoy
- Continuing tasks on the go (not team collaboration)

### For Enterprise Buyers
Emphasize:
- Embedding agents through the SDLC
- Programming agents
- All the scaffolding built in
- Flexibility and safe agent execution
- Collaboration across teams
- Connect features to specific values: engineering productivity, safe agent execution, shorter product backlogs

## Key Messaging Points

### Warp's Unique Advantages

**Warp terminal:**
- Modern terminal UI with block-based navigation and command completions
- Code editing features that give developers full visibility and control
- House of agents - integrated with all major CLI coding agents (Oz, Claude Code, Codex, Copilot)
- Unified local <> cloud agents for seamless workflows
- Built-in knowledge store for collaboration

**Oz:**
- No vendor lock-in - works with any model, with or without Warp
- Real codebases at enterprise scale - multi-repo environments
- Easy to start, deeply programmable
- Integrated local <> cloud agents
- Auto-tracking with full visibility and auditing
- Collaboration baked in with access control

### What We Are NOT

Avoid framing Warp as:
- An IDE replacement (we bring in select IDE features but aren't building an IDE)
- An AI "engineer"
- A cheap agent wrapper

**Note:** We don't care about the traditional terminal vs IDE distinction. Building the best place for agent-first workflows requires bringing in the best of both tools.

## Voice and Style

The authoritative tone rules live in the "Voice & tone" section of the docs style guide (`AGENTS.md`), including the lists of AI-generated-sounding words and structural patterns to avoid. The points below cover positioning-specific guidance.

### Do's:
- **Talk about outcomes, not hype** - Show what changes when agents are reliable and orchestrated
- **Emphasize control and trust** - Warp augments developers, doesn't replace them
- **Anchor on production** - Real software, real workflows, real scale
- **Lean into the ecosystem** - We're neutral and support all top models and agents
- **Show impact** - Use numbers, stories, and real-world use cases
- **Make it applicable** - Give developers something useful to take away
- **Champion the developer** - Speak like a developer, respect their knowledge and time
- **Keep it practical** - Skip fluff, provide clear actionable insights

### Don'ts:
- Avoid overly-strong marketing language
- Don't use corporate or disconnected language
- Skip theoretical posts without practical value
- Don't list features without context or problem-solving
- Don't use AI-slop buzzwords ("seamless," "powerful," "robust," "leverage," "streamline"): name the specific capability instead
- Don't open pages with meta-text ("This page covers...") or narrate the page's structure
- Don't document internal architecture (orchestrators, control planes, lifecycle states): describe the user-visible model the reader acts on
- Don't stack an em dash and a colon in the same sentence: pick one, or split into two direct sentences

## Writing Guidelines

### Headers
- Use sentence case (not title case)
- Capitalize only proper nouns

### Lists
- List items end in periods when the item is a full sentence
- Otherwise, list items don't end with periods
- Descriptive text and captions end in periods

### Preferred Phrases
- ✅ "Ask the agent to..."
- ✅ "Run an agent on the Automation Platform"
- ✅ "The Automation Platform can run this on a schedule"
- ❌ "Ask Oz to..." (stale: Oz was renamed to the Automation Platform on 2026-08-18)
- ❌ "Ask the Automation Platform to..." (you ask an agent, not a platform)

## Problem Framing

### What Developers Struggle With

**Multi-agent workflows:**
- Running more than 3-4 agents before losing track
- Balancing autonomy with safety

**Agents get tasks 80% right:**
- Hard to see exactly what agents have done
- Difficult to continue tasks locally
- Forced to switch between terminals and IDEs

**Staying current:**
- Trying new models and tools daily
- Too much switching and comprehension overhead

**Breaking of flow:**
- Context-switching between tools
- Constant babysitting and supervision of AI
- Resource-heavy and slow tools

### What Teams Struggle With

- Embedding AI tooling across whole teams
- AI adoption doesn't compound across teams
- Running agents safely at scale
- Avoiding vendor lock-in
- Keeping control of agent infrastructure

## Warp's Point of View

**The command line is the best place to do agentic development, but the terminal needs to be modernized.**

The terminal is the natural home for agentic development because:
- It orchestrates systems, processes, and environments
- It spans local and remote work
- It spans the entire SDLC

Modernizing the terminal unlocks a fundamentally better way to build software with:
- Audit trails and visibility
- Modern UI around commands, code editing, and agent prompting
- Collaboration features that mirror real-world workflows

## Enterprise Value Proposition

Organizations adopt Warp Enterprise to:
- **Accelerate development velocity** - AI agents automate tedious tasks across the SDLC
- **Maintain security and control** - Deploy on your infrastructure, route AI inference through your cloud accounts, enforce team-wide guardrails
- **Scale best practices** - Share team knowledge, coding standards, and operational runbooks
- **Reduce context switching** - Keep developers in the terminal with integrated AI, code editing, and tool integrations
