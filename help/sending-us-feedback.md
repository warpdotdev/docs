# Sending us Feedback

We would love to get your feedback on Warp: bugs, feature requests, novel ideas, etc.

### Sending Warp feedback:

* Open a new issue or feature request in our [GitHub repository](https://github.com/warpdotdev/warp/issues/new/choose).
* Join our [Discord](https://www.warp.dev/discord?utm_source=docs-sending_us_feedback) server. Send a message in `#bugs-and-questions` for help with issues and `#new-and-wild-ideas` for feature requests.
* Through our in-app feedback form: navigate to the Mac menu > Send Feedback > Open Feedback Form.

{% embed url="https://www.loom.com/share/a1a41940784e469b84cc2fe98b2fff3a?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %} Send Feedback {% endembed %}

### Sending WarpPreview feedback:

WarpPreview is an early access build given to Warp Ambassadors. You can join this insider program with 20 or more referrals or through our application. Learn more about our [Referral](../getting-started/refer-a-friend.md) and [Warp Ambassadors](https://warpdev.notion.site/Warp-Ambassadors-7aeacbc565694985a64710871470af67#68a28367517042a0aeaa472b2f29cea5) programs.

* Join our [Discord](https://www.warp.dev/discord?utm_source=docs-sending_us_feedback) server. Send a message in `#warp-preview-feedback` for help with WarpPreview.

## Gathering Warp Logs

In some cases, we may also ask for your Warp logs. You can retrieve them using your Terminal app or the Console – a utility for tracking diagnostic information. _Note:_ Warp’s logs do *not* contain any console input or output. See more on how we handle [Crash Reports and Telemetry](../getting-started/privacy.md#what-telemetry-data-are-you-collecting-and-why).

### Exporting Logs from Console:

1. Launch Console, found in Mac’s `Applications > Utilities` folder
1. In the left pane, select Log Reports
    1. In the right pane, find the `warp` log
    1. Drag and drop the log into your GitHub issue comment, feedback email, or discord message.
1. In case of a Warp crash, select Crash Reports from the left pane
    1. Find the Warp crash report from within the right pane
    1. Drag and drop the crash report into your GitHub issue comment, feedback email, or discord message.

### Exporting Logs from Terminal:

1. Open Terminal, found in Mac’s Applications > Utilities folder
1. For a log report
    1. Run `find $HOME/Library/Logs -name "warp*log" -exec cp {} ~/Desktop/ \;`
    1. Drag and drop the log file from your Desktop into your GitHub issue comment, feedback email, or discord message.
1.  In case of a Warp crash
    1. Run `find $HOME/Library/Logs -name "*dev*warp*" -exec cp {} ~/Desktop/ \;`
    1. Drag and drop the crash report into your GitHub issue comment, feedback email, or discord message.
