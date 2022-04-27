# Themes

Warp supports setting custom themes.
In your `.warp` folder, located in your home directory (`~/.warp`), create a themes folder, `~/.warp/themes/`.
Warp will source any themes stored in this directory.
See the custom themes section below for more information.

The Theme Changer can be accessed through the [Command Palette](https://docs.warp.dev/features/command_palette) or by:

1. navigating to the top-right section of the Warp window
2. clicking the kebab-menu to open the drop down menu
3. clicking on “Settings”
4. clicking appearance in the left sidebar of the settings dialog
5. clicking the custom themes (shaded) box

Upon selecting a theme, Warp's appearance will update accordingly.
Press the checkmark to save the selection, or the X to revert.

This setting persists i.e. Warp will open with the same settings in the next session.

![Themes](../.gitbook/assets/themes.gif)

## OS Theme Sync

Warp supports synchronizing your theme with the OS’s light or dark appearance.
To enable this open the settings dialog and click the toggle "Sync with OS".
You will then be able to select a specific theme for when the OS is in light mode and dark mode.

## Default Themes

By default, Warp ships with these themes:

* Warp Dark
* Warp Light
* Dracula
* Solarized Dark
* Solarized Light
* Gruvbox Dark
* Gruvbox Light
* Jellyfish (custom background)
* Koi (custom background)
* Leafy (custom background)
* Marble (custom background)
* Pink City (custom background)
* Snowy (custom background)
* Dark City (custom background)
* Red Rock (custom background)
* Cyber Wave (custom background)
* Willow Dream (gradient)
* Fancy Dracula (gradient)

## Custom themes

Custom themes can be added to your Warp config directory: `~/.warp/themes/`.
Once the themes are added to the config directory, they're available through the theme picker described above.

A more thorough explanation about the theme format, together with examples and a collection of themes can be found in the [Warp themes repository](https://github.com/warpdotdev/themes).

### 1. How do I use a custom theme in Warp?

To start, create a config directory in your home directory:

```sh
mkdir -p ~/.warp/themes/
```

Note that it may take several minutes for Warp to initially discover the new config directory.
You can either wait, or just restart the application.
After that step, all future changes to `~/.warp/themes` directory will be reflected in Warp within seconds.

Add your new custom theme yaml theme file to this directory:

```sh
cp ~/Downloads/my_awesome_theme.yaml ~/.warp/themes/
```

Your new theme should now be visible on the list of available themes.

### 2. Custom Theme Repository

We have a [repository of themes hosted on GitHub.](https://github.com/warpdotdev/themes)

Each theme has a preview generated in the README.

The main difference between "standard" and "base16" themes is that "standard" themes follow the typical color setup, while "base16" themes follow the framework suggested by [@chriskempson](https://github.com/chriskempson/base16).

To install a theme from this repo you can:

* download just a single file and follow the steps from (1)
* clone the entire repo into `~/.warp/`

### 3. How do I write my own custom theme?

Warp supports creating custom themes using yaml files.
The format itself might expand but we'll do our best to avoid breaking changes and maintain forward compatibility.
We also plan on supporting sharing/creating custom themes directly within Warp.

A custom theme in Warp has the following yml structure:

```yaml
accent: '#268bd2' # Accent color for UI elements
background: '#002b36' # Terminal background color
details: darker # Whether the theme is lighter or darker.
foreground: '#839496' # The foreground color.
terminal_colors: # Ansi escape colors.
  bright:
    black: '#002b36'
    blue: '#839496'
    cyan: '#93a1a1'
    green: '#586e75'
    magenta: '#6c71c4'
    red: '#cb4b16'
    white: '#fdf6e3'
    yellow: '#657b83'
  normal:
    black: '#073642'
    blue: '#268bd2'
    cyan: '#2aa198'
    green: '#859900'
    magenta: '#d33682'
    red: '#dc322f'
    white: '#eee8d5'
    yellow: '#b58900'
```

Each color is represented in hex and must start with with `#`.

`background`, `foreground`, `accent` and `details` are Warp-specific.
The accent color is the one used for highlights in Warp's UI, while `details` describe what detailing options in our UI should we pick for the given theme.
The options are `darker` (typically used for dark themes) or `lighter` (typically used for light-mode themes).
`terminal_theme` represents the collection of normal & bright colors (16 total) known from other terminal themes (ansi colors).

### 4. Background Images and Gradients

To add a background image you can use this attribute: "background_image:" with the name of the image you want to use as the background.
Note: Warp currently only supports images with the *.jpg* file format:

* `.jpeg`
* `.jpg`
* `.JPEG`

Here is what a `.yaml` config looks like:

```yaml
accent: '#268bd2'
background: '#002b36'
details: darker
foreground: '#839496'

############################################################### SEE BELOW
background_image:
  # the path is relative to ~/.warp/themes/
  # the full path to the picture is: ~/.warp/themes/warp.jpg
  path: warp.jpg

  opacity: 60
############################################################### SEE ABOVE

terminal_colors:
  bright:
    black: '#002b36'
    blue: '#839496'
    cyan: '#93a1a1'
    green: '#586e75'
    magenta: '#6c71c4'
    red: '#cb4b16'
    white: '#fdf6e3'
    yellow: '#657b83'
  normal:
    black: '#073642'
    blue: '#268bd2'
    cyan: '#2aa198'
    green: '#859900'
    magenta: '#d33682'
    red: '#dc322f'
    white: '#eee8d5'
    yellow: '#b58900'
```

To set up a gradient, create a sub-level under accent with two key-value pairs:

* "left" and "right" or
* "top" and "bottom".

```yaml
accent:
  top: #abcdef
  bottom: #fedcba
```

```yaml
accent:
   left: #abcdef
   right: #fedcba
```

Warp also supports setting a gradient for the background.

```yaml
# accent has a gradient
accent:
  left: '#474747'
  right: '#ffffff'
# background has a gradient
background:
  top: '#474747'
  bottom: '#ffffff'
```

## 5. Contributing

Contributions to this repo are greatly appreciated!

1. Fork the project
2. Create your branch (`git checkout -b theme/AwesomeTheme`)
3. Regenerate thumbnails
4. Commit and open a pull request.

Run this script to generate the thumbnails.

```sh
# assuming you're adding the theme to `standard` directory:
python3 ./scripts/gen_theme_previews.py standard
```

Note: We cannot accept pull request that include custom background images because:

* of licensing restrictions
* we are trying to keep the binary size of the repo as small as possible (just the yaml files)

If your theme has an intended custom background image, include a comment in the yaml with a link to where people should download it.

## 5. Community

All other Warp-related things can be discussed in our [Warp official repo](https://github.com/warpdotdev/Warp/discussions?discussions_q=label%3ARoadmap+sort%3Atop) or our [Discord server](https://discord.gg/warpdotdev).

## 6. Open source dependencies

We'd like to call out a few of the open source themes and repositories that helped bootstrap the set of themes for Warp:

* [iTerm colors pencil](https://github.com/mattly/iterm-colors-pencil)
* [Alacritty-theme](https://github.com/eendroroy/alacritty-theme)
* [base16-Alacritty](https://github.com/aarowill/base16-alacritty)
* [base16](https://github.com/chriskempson/base16)
* [Solarized](https://ethanschoonover.com/solarized/)
* [Dracula](https://draculatheme.com/)
* [Gruvbox](https://github.com/morhetz/gruvbox)
