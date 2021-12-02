# The Input Editor

Unlike other terminals, Warp’s input area is designed to look and work as an out-of-the-box text editor like you’re used to in an IDE. **This remains true even when you’ve** [**SSHed into another machine**](ssh.md). Written in Rust, without any web tech or Electron, Warp’s input editor is built for both speed and utility.

Our editor supports all of your favorite keyboard and mouse bindings, including multiple cursors and selections. Point and click into the text. Click and drag to select. The mouse works the same way it works in any editor. We also strive to be backwards-compatible with the normal terminal (emacs) keyboard bindings like `ctrl-a` and `ctrl-e` to move to the start and end of a line.

* In the editor, type in a multi-line command using `shift-enter` or `opt-enter` to insert newlines.
* Click into a word on the first line
* Holding the `cmd` key down, click into anywhere else in the text. You’ll notice multiple cursors show up.
* Use `shift-left/right-arrow` to make multiple selections.

![Multiple cursors in Warp's input editor](../.gitbook/assets/4\_multiple\_cursors.png)



To see all the functionality that our input editor unlocks, head to [Keyboard Shortcuts](keyboard-shortcuts.md).
