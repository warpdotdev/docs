---
description: Use Warp Agents from the terminal.
---

# Warp CLI

{% hint style="warning" %}
The Warp CLI under development, only available in [Warp Preview](../community/warp-preview-and-alpha-program.md#warp-preview), and only supports some operations. We welcome [feedback](../support-and-billing/sending-us-feedback.md#sending-warp-feedback) on how you're building with the CLI and on any missing functionality!
{% endhint %}

## What is the Warp CLI?

A limited subset of Warp's features are available through the command-line interface. This CLI is for building integrations with Warp's agents, though it's available from any terminal (including Warp!).

## Installing the CLI

The Warp CLI is automatically distributed with the Warp desktop app.

{% tabs %}
{% tab title="macOS" %}
To add the Warp CLI to your `PATH`, open the [Command Palette](../terminal/command-palette.md) and choose the `Install Warp CLI Command` action. This will ask for administrator permissions to install the CLI into `/usr/local/bin`.

You can then run the CLI using `warp` (if you've installed [Warp Preview](../community/warp-preview-and-alpha-program.md), use `warp-preview` rather than `warp`).
{% endtab %}

{% tab title="Windows" %}
In the Warp installer, select `Add Warp to PATH`. If you are installing for all users, this will put the CLI on the system path. Otherwise, the CLI is only added to the path for your account.

You can then run the CLI using `warp` (if you've installed [Warp Preview](../community/warp-preview-and-alpha-program.md), use `warp-preview` rather than `warp`).
{% endtab %}

{% tab title="Linux" %}
To run the Warp CLI on Linux, use the same command that you'd use to start Warp normally. If you installed Warp via a package manager, it should already be on the system `PATH`.

You can then run the CLI using `warp-terminal` (if you've installed [Warp Preview](../community/warp-preview-and-alpha-program.md), use `warp-terminal-preview` rather than `warp`).
{% endtab %}
{% endtabs %}

We are also working on a standalone distribution of the CLI for headless and resource-constrained systems.

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

The agent will automatically carry out the task you gave it, printing out tool calls and responses as it works. If you're using the CLI that's bundled with the Warp app, you can also follow along in the graphical interface with the `--gui` flag.

{% hint style="info" %}
Tip: create a dedicated Agent Profile for CLI usage. The CLI cannot ask you for approval, so use profiles to allow access to specific commands and directories.
{% endhint %}

## Using MCP servers

For robustness, the Warp CLI identifies MCP servers by auto-generated stable IDs. To get the ID of an MCP server, you can either:

* Use the `warp mcp list` command
* Copy the ID from the MCP server's settings page

To start an agent with an MCP server, add the `--mcp-server <server id>` flag. If you have Warp installed on multiple machines, MCP server configurations are automatically synced, but any necessary server programs must be installed on each one.

## Using agent profiles

1. Create an [agent profile](../agents/using-agents/agent-profiles-permissions.md) and use the `warp agent profile list` command to get its stable ID.
2. Use the `--profile <profile id>` flag to select the profile.

Agent profiles are automatically synced to each machine that you have Warp installed on.
