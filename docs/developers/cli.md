---
description: Use Warp Agents from the terminal.
---

# Warp CLI

{% hint style="warning" %}
The Warp CLI under development and only supports some operations. We welcome [feedback](../support-and-billing/sending-us-feedback.md#sending-warp-feedback) on how you're building with the CLI and on any missing functionality!
{% endhint %}

## What is the Warp CLI?

A limited subset of Warp's features are available through the command-line interface. This CLI is for building integrations with Warp's agents, though it's available from any terminal (including Warp!).

## Installing the CLI

There are two ways to install the CLI:
1. Installing the CLI as part of Warp
2. Installing the CLI as a standalone package

### Bundled with Warp

The Warp CLI is automatically distributed with the Warp desktop app.

{% tabs %}
{% tab title="macOS" %}
To add the Warp CLI to your `PATH`, open the [Command Palette](../terminal/command-palette.md) and choose the `Install Warp CLI Command` action. This will ask for administrator permissions to install the CLI into `/usr/local/bin`.
{% endtab %}

{% tab title="Windows" %}
In the Warp installer, select `Add Warp to PATH`. If you are installing for all users, this will put the CLI on the system path. Otherwise, the CLI is only added to the path for your account.
{% endtab %}

{% tab title="Linux" %}
To run the Warp CLI on Linux, use the same command that you'd use to start Warp normally. If you installed Warp via a package manager, it should already be on the system `PATH`.
{% endtab %}
{% endtabs %}

### Standalone

On macOS and Linux, Warp provides standalone packages for the CLI, without the full Warp desktop application.

{% tabs %}
{% tab title="macOS" %}
On macOS, the recommended way to install and update the CLI is with [Homebrew], using the [`warpdotdev/warp` tap](https://github.com/warpdotdev/homebrew-warp).

```sh
$ brew tap warpdotdev/warp
$ brew update
$ brew install --cask warp-cli
```

To install Warp Preview, use `brew install --cask warp-cli@preview`.

You can also download the CLI directly from these URLs, though it will not auto-update:
* [Apple Silicon](https://app.warp.dev/download/cli?os=macos&package=tar&arch=aarch64)
* [Intel](https://app.warp.dev/download/cli?os=macos&package=tar&arch=x86_64)
* [Apple Silicon, Warp Preview](https://app.warp.dev/download/cli?os=macos&channel=preview&package=tar&arch=aarch64)
* [Intel, Warp Preview](https://app.warp.dev/download/cli?os=macos&channel=preview&package=tar&arch=x86_64)
{% endtab %}
{% tab title="Linux" %}
On Linux, the recommended way to install and update the CLI is through your distribution's package manager. See the [installation instructions](../getting-started/quickstart-guide/installation-and-setup.md) for how to add the distribution-specific Warp package repositories. We support `apt`, `yum`, and `pacman`.

Once the Warp package repository is added, you can install `warp-cli` or `warp-cli-preview` packages (for example, `apt install warp-cli`).

You can also download and install packages directly, which will automatically add the Warp repository:
* [x86-64 `.deb` package](https://app.warp.dev/download/cli?os=linux&package=deb&arch=x86_64)
* [x86-64 `.rpm` package](https://app.warp.dev/download/cli?os=linux&package=rpm&arch=x86_64)
* [x86-64 pacman package](https://app.warp.dev/download/cli?os=linux&package=pacman&arch=x86_64)
* [aarch64 `.deb` package](https://app.warp.dev/download/cli?os=linux&package=deb&arch=aarch64)
* [aarch64 `.rpm` package](https://app.warp.dev/download/cli?os=linux&package=rpm&arch=aarch64)
* [aarch64 pacman package](https://app.warp.dev/download/cli?os=linux&package=pacman&arch=aarch64)
{% endtab %}
{% endtabs %}

## Running the CLI

The command to run the Warp CLI depends on your OS, whether you installed the CLI as part of Warp or separately, and whether you're using the stable build or [Warp Preview](../community/warp-preview-and-alpha-program.md).

| OS      | Installation Method |    CLI Command |   CLI Command (Preview) |
|---------|---------------------|----------------|-------------------------|
| macOS   | Standalone          |         `warp` |          `warp-preview` |
| macOS   | Bundled             |         `warp` |          `warp-preview` |
| Linux   | Standalone          |     `warp-cli` |      `warp-cli-preview` |
| Linux   | Bundled             | `warp-terminal`| `warp-terminal-preview` |
| Windows | Standalone          |          N/A   |                     N/A |
| Windows | Bundled             |         `warp` |          `warp-preview` |

## Getting help

To get the most up-to-date information about the Warp CLI, use the built-in `help` command. For example, to learn about all MCP-related commands, run `warp help mcp`

```shell
$ warp help mcp
Manage MCP servers

Usage: warp-dev mcp <COMMAND>

Commands:
  list  List MCP servers
  help  Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

## Logging in

If you use the CLI on a host where you've already logged in to Warp, it will reuse your existing credentials.

To set up the CLI on a remote host, use the `warp login` command (replace `warp` with the appropriate command name for your installation method in the table above). This prints out a URL that you can open in a browser on another computer to sign in to Warp.

## Running agents

To start a Warp agent, use the `warp agent run` subcommand. You'll need to specify a prompt and, optionally, the [MCP servers](../knowledge-and-collaboration/mcp.md) and [agent profile](../agents/using-agents/agent-profiles-permissions.md) to use.

```shell
$ warp agent run --prompt "set up a new Rust crate named warp-cli"
I'll run a few terminal commands to:
- Detect the current Git branch to ensure we don't accidentally push to a protected branch later.
- Check if there's a root Cargo.toml (to determine if this repo uses a Cargo workspace).
- Create a new binary crate named warp-cli.
- If this is a workspace, I'll update the root Cargo.toml to include the new member.
Running `git rev-parse --abbrev-ref HEAD`
fatal: not a git repository (or any of the parent directories): .git

 (`git rev-parse --abbrev-ref HEAD` exited with code 128)
Finding files matching Cargo.toml in .
Running `test -d warp-cli && echo EXISTS || echo NOT_EXISTS`
NOT_EXISTS

 (`test -d warp-cli && echo EXISTS || echo NOT_EXISTS` exited with code 0)
Running `cargo new warp-cli --bin`
    Creating binary (application) `warp-cli` package
note: see more `Cargo.toml` keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

 (`cargo new warp-cli --bin` exited with code 0)
Reading warp-cli/src/main.rs, warp-cli/Cargo.toml
Done. I ran a few terminal commands to check your environment and scaffold the project, then created a new binary crate named warp-cli.
Next steps:
- Build/check: Want me to run cargo check or cargo build now to verify everything compiles?
- CLI framework: Want me to add clap and set up a basic command structure (e.g., subcommands, --version, --help)?
- Testing: If you’d like tests, we can set up cargo-nextest and add a first test.

Tell me which of the above you’d like me to do and I’ll proceed.
```

The agent will automatically carry out the task you gave it, printing out tool calls and responses as it works.

By default, the agent runs in your current working directory. To run from a different directory, use the `-C/--cwd` flag.

## Using saved prompts

Instead of typing out a prompt, you can reference [saved prompts](../knowledge-and-collaboration/warp-drive/prompts.md) using the `--saved-prompt` flag:

```sh
$ warp agent run --saved-prompt sgNpbUgDkmp2IImUVDc8kR
...
```

{% hint style="info" %}
The ID of a saved prompt will be the last part of its [URL](../knowledge-and-collaboration/warp-drive/README.md#sharing-a-drive-object-using-links).
For example, in the Warp Drive URL `https://staging.warp.dev/drive/prompt/Fix-compiler-error-sgNpbUgDkmp2IImUVDc8kR`, the ID is `sgNpbUgDkmp2IImUVDc8kR`.
{% endhint %}

## Referencing Warp Drive objects

This prompt can include [Warp Drive objects](../knowledge-and-collaboration/warp-drive/README.md) and [rules](../knowledge-and-collaboration/rules.md) as attached context, using the syntax `<workflow:id>`, `<notebook:id>`, or `<rule:id>`. To quickly create these references, use the [@ context menu](../agents/using-agents/agent-context/using-to-add-context.md) in Warp to construct a prompt, and then copy it into your CLI command.

```sh
$ warp agent run --prompt "Follow the instructions in <notebook:gq1CMAUWLtaL1CpEoTDQ3y>"
...
```

## Using agent profiles

The Warp CLI uses [agent profiles](../agents/using-agents/agent-profiles-permissions.md) to customize how the agent behaves. To use different models, autonomy behavior, or MCP servers, create a new profile. Agent profiles are automatically synced to each host that you have Warp installed on, so you can still use them remotely.

{% hint style="info" %}
Tip: create a dedicated profile for CLI usage. The CLI will fail if it tries to execute a prohibited action, so make sure your profile allows the directories, commands, and MCP servers that you'd like the agent to use.
{% endhint %}

To use an agent profile with the CLI, first get its ID using the `warp agent profile list` command:

```sh
$ warp agent profile list
+--------------+------------------------+
| Name         | ID                     |
+=======================================+
| Default      | AnTb02PZfrkVC9l4V15eH1 |
|--------------+------------------------|
| Coding       | CWhozDJPdPCsjJ1pSG0HCN |
|--------------+------------------------|
| Command Line | hV6n5dNm7ThQVlOiPF8DLS |
+--------------+------------------------+
```

Then, select that profile using the `--profile` flag:

```sh
$ warp agent run --profile CWhozDJPdPCsjJ1pSG0HCN --prompt "update my CI pipeline to use nextest"
...
```

## Using MCP servers

The CLI can use any [MCP server](../knowledge-and-collaboration/mcp.md) that you've configured. There are two ways to start MCP servers with the agent:

1. If the selected agent profile allows _specific_ MCP servers, they will start automatically.
2. If the selected agent profile allows _any_ MCP server, you must specify the ones to start using the `--mcp-server` flag.

Make sure that your agent profile includes the MCP servers that you want to use!

To start specific MCP servers, you'll need their ID. To get MCP server IDs, use `warp mcp list`:

```sh
$ warp mcp list
+--------------------------------------+--------+
| UUID                                 | Name   |
+===============================================+
| 1deb1b14-b6e5-4996-ae99-233b7555d2d0 | github |
|--------------------------------------+--------|
| 65450c32-9eb1-4c57-8804-0861737acbc4 | linear |
|--------------------------------------+--------|
| d94ade64-0e73-47a6-b3ee-14e5afec3d90 | Sentry |
+--------------------------------------+--------+
```

You can also copy the server ID from the MCP servers page:

<figure><img src="../.gitbook/assets/mcp-server-id.png" alt=""><figcaption><p>MCP servers page, showing a server with its UUID</p></figcaption></figure>

Then, run an agent like this:

```sh
$ warp agent run --mcp-server "1deb1b14-b6e5-4996-ae99-233b7555d2d0" --prompt "who last updated the README?"
...
```

{% hint style="warning" %}
While Warp syncs MCP server configuration between hosts, it **does not** sync environment variables. You'll have to set any required MCP environment variables when running the agent on a remote host.
{% endhint %}

```sh
export MY_MCP_SERVER_ACCESS_TOKEN="..."
$ warp agent run --mcp-server "904a8936-fa82-4571-b1d6-166c26197981" --prompt "use my MCP server to check for errors"
...
```

{% hint style="info" %}
Tip: consider using a password or secret manager CLI, such as [`op`](https://developer.1password.com/docs/cli/get-started/), [`pass`](https://www.passwordstore.org/), or [`gcloud secrets versions access`](https://cloud.google.com/secret-manager/docs/create-secret-quickstart#secretmanager-quickstart-gcloud) to fetch MCP secrets on remote hosts.
{% endhint %}
