# Sending Us Feedback

We would love to get your feedback on Warp: bugs, feature requests, novel ideas, etc.

### Sending Warp feedback:

* Open a new issue or feature request in our [GitHub repository](https://github.com/warpdotdev/warp/issues/new/choose).
* Through the Mac Menu: Help > Send Feedback.
* Through in-app Menu: Warp Essentials:bulb: > Feedback
* Join our [Discord](https://www.warp.dev/discord?utm\_source=docs-sending\_us\_feedback) server. Send a message in `#bugs-and-feedback` for help with bugs and issues and `#questions` for general questions on how to do stuff in Warp.

<figure><img src="../.gitbook/assets/send-feedback-demo.gif" alt="sending feedback from the mac menu and warp essentials"><figcaption><p>Send Feedback</p></figcaption></figure>

### Sending WarpPreview feedback:

WarpPreview is an early access build given to Warp Ambassadors. You can join this insider program through our application. Learn more about the [Warp Ambassadors](https://warpdev.notion.site/Warp-Ambassadors-7aeacbc565694985a64710871470af67#68a28367517042a0aeaa472b2f29cea5) program.

* Join our [Discord](https://www.warp.dev/discord?utm\_source=docs-sending\_us\_feedback) server. Send a message in `#ambassador-forum` for help with WarpPreview.

## Gathering Warp Logs

In some cases, we may also ask for your Warp logs. You can retrieve them using your Terminal app or the Console – a utility for tracking diagnostic information. _Note:_ Warp’s logs do _not_ contain any console input or output. See more on how we handle [Crash Reports and Telemetry](../getting-started/privacy.md#what-telemetry-data-are-you-collecting-and-why).

### Exporting Logs from Console:

1. Launch Console, found in Mac’s `Applications > Utilities` folder
2. In the left pane, select Log Reports
   1. In the right pane, find the `warp` log
   2. Drag and drop the log into your GitHub issue comment, feedback email, or discord message.
3. In case of a Warp crash, select Crash Reports from the left pane
   1. Find the Warp crash report from within the right pane
   2. Drag and drop the crash report into your GitHub issue comment, feedback email, or discord message.

### Exporting Logs from Terminal:

1. Open Terminal, found in Mac’s Applications > Utilities folder
2. For a log report
   1. Run `find $HOME/Library/Logs -name "warp*log" -exec cp {} ~/Desktop/ \;`
   2. Drag and drop the log file from your Desktop into your GitHub issue comment, feedback email, or discord message.
3. In case of a Warp crash
   1. Run `find $HOME/Library/Logs -name "*dev*warp*" -exec cp {} ~/Desktop/ \;`
   2. Drag and drop the crash report into your GitHub issue comment, feedback email, or discord message.
