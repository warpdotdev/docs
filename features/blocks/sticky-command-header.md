# Sticky Command Header

## What is it

Sticky Command Header shows you the previous command run for a large Block that is scrolled partially off-screen. This helps you see the command that was previously run or currently running (if it’s long) and click on the header to jump to the top of the Block. _Note:_ For long-running commands that take up the full screen, the sticky header only shows after you start scrolling up. This is to prevent the header blocking the top part of the output for commands like ‘git log’ that simulate full screen apps.

## How to access it

* Sticky Command Header is enabled by default.
* Toggle Sticky Command Header by going to `Settings > Features` > toggle “Show sticky command header”. 
* Toggle by searching for “Sticky Command Header” within Command Palette `CMD-P`

## How to use it

* If a Block has a large output ( e.g. `seq 1 1000`), the header of the Block will show on the top of the active Window, Tab, or Pane.
* Access the Block context menu and bookmark the Block by clicking in the stick header
* Click on the Sticky Command Header to quickly jump to the top of the Block.

## How it works

{% embed url="https://www.loom.com/share/a86967c057e44ab4bee4860ba80538b9?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}Sticky Command Header Demo{% endembed %}
