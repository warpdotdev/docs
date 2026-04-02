---
description: >-
  See how Warp's design team used Warp itself to locate, edit, and test changes
  to the universal input.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/how-warp-uses-warp/building-warps-input-with-warp
---

# Building Warp's Input - With Warp

_Speaker: Dave, Product Design Lead at Warp_

{% embed url="https://youtu.be/ySzUj7kMZ64?si=MBhB4s_6lMDWHeS6" %}

### The Challenge

Redesigning the input was tricky because it’s the primary interface developers use all day, every day.\
Everyone had opinions — and expectations — about how it should look and behave.

So, Peter (a product designer on my team) and I iterated on multiple designs using Figma.

Once we landed on a version we liked, we shared it internally.\
Most people were excited, but engineering resources were stretched thin — focused on improving agent-mode quality and prepping the Agentic Development Environment.

So I thought: _“What if I just Warp it?”_

#### Step 1. Locating the Git Diff Chip Code

Inside the universal input, there’s a small Git Diff chip — it shows your current branch and open changes. It was one pixel too tall. That tiny visual bug drove me nuts, so I used Warp to find where it lived.

Warp searched across the entire codebase and found references inside:

* `displaychip.rs`
* Related render and configuration files

It used a combination of semantic search, code indexing, and traditional grep to pinpoint the exact implementation.

***

#### Step 2. Modifying the Font Size

Once Warp located the implementation, I asked it to reduce the font size by 1 pixel.

Warp automatically edited the relevant lines:

* Found the current setting (`system_font_size - 1`)
* Adjusted it to (`system_font_size - 2`)

I reviewed the diffs to confirm everything looked good.

***

#### Step 3. Building and Testing the Change

Next, I rebuilt the app using:

```bash
cargo run
```
