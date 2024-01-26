# Network Log

## What is it

Warp’s network log contains logs for all network traffic (both requests and responses) originating from the current terminal session. You can use Warp’s network log to help debug issues or simply use it to understand when information is sent or received over the network over the course of a Warp terminal session.

Each log item is a timestamped Debug format string for either a request or response object handled by Warp. Messages are logged via pre-request and post-response hooks in Warp’s internal HTTP client.

## How to use it

1. There are 2 main ways to access the network panel.
   1. Option 1: CMD-P > Type in “Show Warp Network Log”
   2. Option 2: Press CMD-R > Type in “Tail Warp Network Log”
2. Both options insert a workflow into your input editor - it should look something like this: `tail -f "some/path/to/warp_network.log"`.
3. Press Enter to run this workflow.
4. Press CMD-D to open up a split pane on the right, then run AI Command Search or share a block to see the network log activity.
   1. Example #1: Press CTRL-\` to open up A.I. Command Search > Type in “print hello world”
   2. Example #2: Run `echo “hello world”` > Right click on the block > Click “Create permalink” > Click “Create and Copy Link”
5. Once you run one of these examples, you’ll see the corresponding requests and responses logged in the left pane.

## How it Works

{% embed url="https://www.loom.com/share/0d9eaeb8715846f3a96d557abe23e7ac?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Network Log Demo
{% endembed %}

## Known Issues

At the moment, network traffic originating from crash reports and error messages are not captured in the network log. This is due to our use of the Sentry SDK, which encapsulates all network logic and doesn’t currently expose a hook for handling requests and responses directly. The team is actively investigating a solution to include such traffic in the log in a future release. You may also disable Crash Reporting entirely in Warp’s `Settings > Privacy` tab.
