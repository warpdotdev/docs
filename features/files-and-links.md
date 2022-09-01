# Files and Links

## What is it

Warp supports opening file, folder, and url links that are within Blocks. Multiple URL protocols are supported e.g. `https`, `ftp`, `file`, etc. Warp opens web links directly in your default browser.

## How to access it

1. After hovering over a link, open it directly by holding down `CMD` while clicking it. 
2. Clicking a link normally will open a clickable tooltip that says “Open File/Folder/Link”.
3. Right clicking a link will open a context menu that supports copying the absolute file path or url to the clipboard.

Note: Configure the default editor to open files with by navigating to `Settings > Features > Choose an editor to open file links`.

## How it works

Warp parses relative and absolute file paths. Warp also tries to capture line and column numbers attached to the file path, supported formats include:&#x20;

* `file_name:line_num`
* `file_name:line_num:column_num`
* `file_name[line_num, column_num]`
* `file_name(line_num, column_num)`
* `file_name, line: line_num, column: column_num`
* `file_name, line: line_num, in`
