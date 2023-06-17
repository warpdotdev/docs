# YAML-based Workflows

{% hint style="danger" %}
You can continue to use YAML-based workflows, but we recommend using new [workflows in Warp Drive](../warp-drive/workflows.md) instead for a better editing experience.
{% endhint %}

## What is it

Workflows are an easier way to execute and share commands within Warp. They are easily parameterized and searchable by name, description, or command arguments. [Common workflows](https://github.com/warpdotdev/workflows) sourced by the Warp team and community are readily available within the app. Additionally, you can create and scope workflows locally or to a git repository.

## How to use it

* Press `CTRL-SHIFT-R` to open the Workflow menu or through the Command Palette `CMD-P`.
* Once inside the menu, start typing in the search bar to filter the existing workflows or browse by category. (e.g. git, android, npm, etc.)
* When a Workflow is selected, you can use `SHIFT-TAB` to cycle thru the parameters.
* You can also expand the menu horizontally with the mouse by dragging it on the right edge.

## How it works

{% embed url="https://www.loom.com/share/27eccd9aa9b34884897e28a53642322b?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Workflows Demo
{% endembed %}

{% embed url="https://www.youtube.com/watch?v=9HGB7nxn_0I" %}
How to use Workflows
{% endembed %}

### How is this Different from Aliases?

Workflows solve some major pain points with aliases, specifically the:

1. need to context switch
   1. leave vim, source dotfiles, or reset shell
2. difficulty with attaching documentation
3. inability to easily search or share
4. inability to easily parameterize

## Creating Custom Workflows

### How to create a workflow with YAML

Workflows can easily be shared with your team by saving a workflow's YAML file to `~/.warp/workflows/` or `.warp/workflows/` in the top level of a repository. Local and Repository workflows can be accessed under the "My Workflows" and "Repository Workflows" tab of the Workflows menu, respectively.

See the existing workflows spec within the [Workflows repo](https://github.com/warpdotdev/Workflows/tree/main/specs) for examples. Additionally, we outline the file format below:

<details>

<summary><a href="https://github.com/warpdotdev/Workflows/blob/main/FORMAT.md">Workflow File Format</a></summary>

The workflow file format is a [yaml](https://yaml.org/) file and must have either a \`.yml \` or \`yaml\` extension. If you're new to YAML and want to learn more, see [Learn YAML in Y minutes](https://learnxinyminutes.com/docs/yaml/). _Compatibility Note_: Warp is still in Beta and this format is subject to change.

***

**`name`**

The name of the Workflow. Required.

**`command`**

The command that is executed when the Workflow is selected. Required.

**`tags`**

An array of tags that are useful to categorize the Workflow. Optional.

```yaml
tags: ["git", "GitHub"]
```

**`description`**

The description of the Workflow and what it does. Optional.

**`source_url`**

The URL from where the Workflow was originally generated from. This is surfaced in [commands.dev](https://www.commands.dev/) for attribution purposes. Optional.

**`author`**

The original author of the Workflow. For example, if this workflow was generated from StackOverflow, the `author` would be the `author` of the StackOverflow post. This is surfaced in [commands.dev](https://www.commands.dev/) for attribution purposes. Optional.

**`author_url`**

The URL of original author of the Workflow. For example, if this workflow was generated from StackOverflow, the `author_url` would be the StackOverflow author's profile page. This is surfaced in [commands.dev](https://www.commands.dev/) for attribution purposes. Optional.

**`shells`**

The list of shells where this Workflow is valid. If not specified, the Workflow is assumed to be valid in all shells. This must be one of `zsh`, `bash`, or `fish`.

**`arguments`**

A Workflow can have parameterized arguments to specify pieces of the Workflow that need to be filled in by the user.

You can specify which part of the Workflow command maps to an argument by surrounding it with two curly braces (`{{<argument>}}`).

For example the workflow command:

```bash
for {{variable}} in {{sequence}}; do
  {{command}}
done
```

Includes 3 arguments: `variable`, `sequence`, and `command`.

**`arguments.name`**

The name of the argument. The argument name is used within the command to specify the ranges of the argument. Required.

```yaml
name: Example workflow
command: echo {{string}}
arguments:
  - name: string
    description: The value to echo
```

**`arguments.description`**

The description of the argument. This is surfaced in both [commands.dev](https://www.commands.dev/) and Warp to help users fill in Workflow arguments. Optional

**`arguments.default_value`**

The default value for the argument. If specified, the `default_value` replaces the argument name within the command. Optional

***

</details>

### Where to save workflows

Local workflows are scoped to your machine. Repository workflows are scoped to a git repository and can be accessed by anyone who has cloned the repo. _Note:_ Repository workflows will not appear if you are ssh'd into a remote machine.

Local Workflow Path: `~/.warp/workflows`

Repository Workflow Path: `{{path_to_git_repo}}/.warp/workflows`

#### Adding a Local Workflow

To start, create a workflows subdirectory within your `.warp` folder

`mkdir -p ~/.warp/workflows`

Add your workflow’s `.yaml` file to this directory; if the file format is valid Warp should automatically load it into the Workflows menu.

`cp ~/path/to/my_awesome_workflow.yaml ~/.warp/workflows`

#### Adding a Repository Workflow

You can add a repository workflow similarly to how you added a local workflow. Create a workflows folder in a repository’s root directory and save your `.yaml` file like so:

```
cd {{repository_path}}
mkdir -p .warp/workflows/
cp ~/path/to/my_awesome_workflow.yaml .warp/workflows
```

#### Contributing to Global Workflows

You can contribute workflows that will be made available to other Warp users by forking the [Workflows repo](https://github.com/warpdotdev/workflows/tree/main/specs) and opening a pull request. See the [Contributing](https://github.com/warpdotdev/workflows#contributing) section for more details.
