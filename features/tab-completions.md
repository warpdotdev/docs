# Tab Completions

Warp comes with **built-in tab completions** for some of the most common commands, which work regardless of the machine or directory you’re in (including when you’ve SSHed).  As with standard shell autocomplete, you activate completions by pressing `TAB`.

* Navigate to a local git directory
* Type `git checkout` and press `TAB`
* A menu will show all of your local branches. You can select one using your mouse or the up/down `↑`/`↓` arrow keys. A submenu shows the command's description.

![Tab completions in Warp](../.gitbook/assets/tab\_completions.png)

**NB**: to search for options, you first need to type `-` (dash).

Warp’s tab completions go beyond simply auto suggesting local file paths. We parse your input (without saving any state on our servers) to intelligently suggest arguments and options for commonly used commands.&#x20;

Discover what we can autocomplete by pressing `TAB`, or looking at the [supported completions section ](tab-completions.md#supported-completions)below.&#x20;

## Supported completions

`bigtable` `bundle` `cargo` `cat` `cd` `cdk` `cheat_sheet` `ch` `clear` `cloud_shell` `code` `command` `components` `config` `cp` `curl` `datastore` `dbt` `deployment_manager` `dig` `docker` `domains` `dotslash` `endpoints` `exa` `feedback` `firestore` `gcloud` `git` `github` `grep` `grex` `head` `help` `http_server` `info` `init` `jest` `knex` `less` `logging` `ls` `mkdir` `monitoring` `mv` `nano` `npm` `nuxt` `open` `organizations` `projects` `ps` `pushd` `pwd` `recommender` `resource_manager` `rm` `services` `source` `subl` `sudo` `survey` `tail` `tar` `test` `time` `top` `topic` `touch` `unzip` `vercel` `version` `vi` `whois` `wrk` `xcode_select` `zip`

Command missing autocomplete? [File a feature request](../help/sending-us-feedback.md).

