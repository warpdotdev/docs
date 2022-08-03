# Files and Links

Warp supports opening file and url links; after hovering over a link, open it directly by holding down \`CMD\` while clicking it. Clicking a link normally will open a clickable tooltip that says “Open link”.\
\
Right clicking a link will open a context menu that supports copying the absolute file path to the clipboard.

### File Path

Warp parses relative and absolute file paths. Warp also tries to capture line and column numbers attached to the file path, supported formats include:&#x20;

* `file_name:line_num`
* `file_name:line_num:column_num`
* `file_name[line_num, column_num]`
* `file_name(line_num, column_num)`
* `file_name, line: line_num, column: column_num`
* `file_name, line: line_num, in`

Configure the default editor to open files with by navigating to Settings > Features > Choose an editor to open file links

### URLs and Links

Multiple URL protocols are supported e.g. `https`, `ftp`, `file`, etc. Warp opens web links directly in your default browser.
