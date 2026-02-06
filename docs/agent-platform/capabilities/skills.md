---
description: >-
  Skills are reusable instruction sets that teach agents how to perform specific
  tasks. Create custom skills to standardize workflows and share expertise
  across your team.
---

# Skills

Skills allow you to create reusable, shareable instructions that Agents can invoke when performing tasks. Instead of repeating detailed prompts, you can encapsulate common workflows, coding patterns, or domain expertise into skill files that Agents automatically discover and use.

## Key features

* **Reusable instructions** - Define a task once and let Agents use it whenever relevant
* **Project and global scopes** - Create skills specific to a project or available across all projects
* **Automatic discovery** - Agents are aware of all available skills and invoke them when appropriate
* **Simple markdown format** - Skills are just markdown files with a small amount of metadata
* **Supporting files** - Include scripts, templates, or other resources alongside your skill instructions
* **Slash command invocation** - Invoke any skill directly with `/{skill-name}`

## How skills work

When you start an [Agent conversation](../local-agents/interacting-with-agents/README.md), the Agent receives a list of all available skills with their names and descriptions.

When the Agent determines that a skill would help accomplish your task, it loads the skill's full instructions and follows them to complete the task.

{% hint style="warning" %}
Skill discovery is based on your current working directory. For Git repositories, Warp includes all skills from your current directory up through the repository root. If you're working in project A, you won't have access to skills from project B.
{% endhint %}

{% hint style="info" %}
Skills complement Rules, which provide persistent guidelines that Agents always follow. Use Rules for constraints and preferences; use Skills for specific task workflows.
{% endhint %}

### Skill name conflicts

If you have skills with the same name in multiple directories, Warp handles the conflict differently depending on how the skill is invoked:

* **Natural language** - The Agent receives a list of all in-scope skills including their names, descriptions, and file paths. The Agent can see all available options and chooses the appropriate skill based on its path.
* **Slash commands** - When multiple skills share the same name, Warp displays all matching skills in the menu. You select which one to use based on the description.
* **Background resolution** - When Warp resolves skill names automatically (without direct user selection), it prioritizes home directory (global) skills first, then skills from higher directories (closer to the repository root).

### Example interactions

You can invoke skills in two ways:

**Using natural language** - Describe what you want to accomplish:

* "Use the deploy skill to push to staging"
* "Check the docs for broken links" (invokes a link-checking skill)
* "Create a DOCX file with my project's README content"
* "Draft documentation for the new API endpoint based on this PR"

**Using slash commands** - Invoke a skill directly with `/{skill-name}`:

* `/deploy` - Invokes the deploy skill
* `/add-feature-flag` - Invokes the add-feature-flag skill

The Agent recognizes when your request matches a skill's purpose, loads the skill instructions, and follows them to complete the task.

## Skill File Format

Skills are markdown files with YAML frontmatter. Each skill must have:

* **name** - A unique identifier for the skill (typically kebab-case)
* **description** - A brief explanation of what the skill does and when to use it

### Basic Structure

```markdown
---
name: your-skill-name
description: Brief description of what this skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for the agent.

## Examples
Show concrete examples of using this skill.
```

### Example Skill File

Here's a complete example of a skill that helps create feature flags:

```markdown
---
name: add-feature-flag
description: Add a new feature flag to the codebase with proper configuration and documentation
---

# Add Feature Flag

## Instructions
1. Ask the user for the feature flag name and default value
2. Add the flag definition to `config/feature_flags.yaml`
3. Create a helper function in `src/utils/flags.ts`
4. Update the feature flags documentation in `docs/FEATURE_FLAGS.md`

## Configuration Format
Feature flags should follow this format in the YAML file:

feature_name:
  default: false
  description: "What this flag controls"
  owner: "team-name"

## Examples
- "Add a feature flag for the new checkout flow"
- "Create a flag to enable dark mode for beta users"
```

## Skill locations

Skills can be stored at two levels: project-level (accessible only within that project) and user-level (accessible from any project).

### Project skills

Project skills live in your repository and are available when you're working in that project. We recommend storing them at your project root, but skills in subdirectories are also discovered when you're working within that subdirectory. This is useful for monorepos with separate `./frontend` and `./backend` directories.

Store them in any of these directories:

* **`.agents/skills/`** (recommended)
* **`.warp/skills/`**
* **`.claude/skills/`**
* **`.codex/skills/`**
* **`.cursor/skills/`**
* **`.gemini/skills/`**
* **`.copilot/skills/`**
* **`.factory/skills/`**
* **`.github/skills/`**
* **`.opencode/skills/`**

Each skill must be in its own subdirectory with a `SKILL.md` file. Any supporting files (scripts, templates, configs) should be referenced in `SKILL.md` so the Agent knows they exist:

```
your-project/
├── .agents/
│   └── skills/
│       ├── add-feature-flag/
│       │   └── SKILL.md
│       └── run-migrations/
│           └── SKILL.md
├── .claude/
│   └── skills/
│       └── review-code/
│           └── SKILL.md
└── .github/
    └── skills/
        └── create-release/
            └── SKILL.md
```

{% hint style="info" %}
Warp scans all supported skill directory names in your project root, allowing you to maintain skills compatible with multiple AI coding tools in the same repository.
{% endhint %}

### Root directory skills (global)

Root directory skills are stored in your home directory and are available across all projects on your machine. These are useful for personal workflows, coding patterns, or procedures you use regardless of the specific project.

Store global skills in any of these directories in your home folder:

* **`~/.agents/skills/`** (recommended)
* **`~/.warp/skills/`**
* **`~/.claude/skills/`**
* **`~/.codex/skills/`**
* **`~/.cursor/skills/`**
* **`~/.gemini/skills/`**
* **`~/.copilot/skills/`**
* **`~/.factory/skills/`**
* **`~/.github/skills/`**
* **`~/.opencode/skills/`**

The directory structure is the same as project skills:

```
~/.agents/
└── skills/
    ├── git-workflow/
    │   └── SKILL.md
    └── code-review/
        └── SKILL.md
```

### Project vs Root directory skills

Understanding when to use each level:

**Project skills** are best for:

* Project-specific workflows (deployment, testing, migrations)
* Team-shared procedures and standards
* Repository-specific automation and tooling
* Domain-specific patterns for that codebase

**Root directory skills** are best for:

* Personal coding preferences and patterns
* General-purpose workflows used across all projects
* Cross-project automation (git workflows, documentation templates)
* Professional standards you apply everywhere

## Creating skills

### Step 1: Choose a location

Decide whether your skill should be:

* **Project-specific** - Place it in one of your project's skill directories (`.agents/skills/`, `.warp/skills/`, `.claude/skills/`, etc.)
* **Global** - Place it in one of your home directory's skill folders (`~/.agents/skills/`, `~/.warp/skills/`, `~/.claude/skills/`, etc.)

### Step 2: Create the directory structure

Create a subdirectory for your skill with a descriptive name:

```bash
mkdir -p .agents/skills/my-new-skill
```

### Step 3: Write the skill file

Create `SKILL.md` in your skill directory:

```bash
touch .agents/skills/my-new-skill/SKILL.md
```

### Step 4: Add content

Write your skill with clear instructions:

```markdown
---
name: my-new-skill
description: One-line description of what this skill does
---

# My New Skill

## When to use
Explain the scenarios where this skill is helpful.

## Instructions
1. First step the Agent should take
2. Second step with specific details
3. Continue with clear, actionable steps

## Important notes
- Any constraints or requirements
- Common pitfalls to avoid
```

## Skills with supporting files

Skills can include supporting files like scripts, templates, or configuration files. Place these files in the same directory as your `SKILL.md`:

```
.agents/skills/
└── check-broken-links/
    ├── SKILL.md
    ├── check_links.py      # Supporting script
    └── config.yaml         # Configuration file
```

In your skill instructions, reference these files using relative paths. For example, in your `SKILL.md`:

```
## Running the check

From the project root:

python3 .agents/skills/check-broken-links/check_links.py --internal-only
```

This pattern is useful for:

* **Automation scripts** - Python, shell, or Node scripts that perform complex tasks
* **Templates** - Boilerplate files the Agent can copy and customize
* **Configuration** - Default settings or schemas the skill references

## Managing skills

### Viewing available skills

Ask the Agent what skills are available:

```
What skills do I have?
```

The Agent lists all discovered skills with their names and descriptions. This includes skills from all supported directories in both your current project and your home directory.

### Editing skills

Use the [`/open-skill`](slash-commands.md) slash command to modify existing skills:

```
/open-skill
```

This opens an interactive menu where you can:

* Browse project and root directory skills
* See which directory each skill is located in
* Open the skill file in your editor

### Best practices

* **Write clear descriptions** - The description is how Agents decide whether to use your skill
* **Be specific in instructions** - Include exact file paths, command syntax, and expected formats
* **Include examples** - Show concrete use cases to help Agents understand intent
* **Keep skills focused** - Each skill should do one thing well
* **Use consistent naming** - Follow a naming convention like `verb-noun` (e.g., `add-feature-flag`, `run-migrations`)
* **Version control your skills** - Commit project skills to your repo so the whole team benefits

## Related features

* **Rules** - Set persistent guidelines and constraints for Agent behavior
* **MCP Servers** - Expose external data sources and tools to Agents
* [**Cloud Agents**](../cloud-agents/cloud-agents-overview.md) - Run Agents in the cloud on schedules or triggers
* [**Agent Profiles**](agent-profiles-permissions.md) - Control Agent permissions and autonomy
