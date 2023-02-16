# Smart-Select

## What is it

Smart-select is an alternative to traditional double-click selection, i.e. semantic selection.
Normally, semantic selection selects a "word".
This isn't necessarily a dictionary word, but a string of contiguous letter characters unbroken by whitespace or punctuation.
Since terminals often show patterns like URLs or file paths, it makes sense to have double-clicks automatically select these commonly-encountered patterns.
In Warp, double-clicking certain patterns will select them without dragging the mouse.

## How to access it

Double-click on some text in the app.
The following patterns are recognized:

1. URLs
1. File paths
1. Email addresses
1. IP addresses
1. Floating point numbers, including scientific notation.

You can enable and disable this feature in the `Settings > Features` page.

If disabled, you can instead manually select specfic punctuation characters to be included within word boundaries.
