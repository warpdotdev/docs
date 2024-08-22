---
description: >-
  Warp supports Custom Themes which can be created manually or downloaded from
  our repo.
---

# Custom Themes

{% hint style="info" %}
Examples and a collection of themes can be found in the [Warp themes repository](https://github.com/warpdotdev/themes).
{% endhint %}

## Warp's Custom Theme Repository

We have a [repository of themes hosted on GitHub.](https://github.com/warpdotdev/themes)

Each theme has a preview generated in the README.

The main difference between "standard" and "base16" themes is that "standard" themes follow the typical color setup, while "base16" themes follow the framework suggested by [@chriskempson](https://github.com/chriskempson/base16).

There are 2 ways to install a theme from this repo.

1. Download a single file and follow the steps in the section below.
2. Clone the entire repo into the appropriate location based on your OS below:

{% tabs %}
{% tab title="macOS" %}
```
mkdir -p ~/.warp
cd ~/.warp/
git clone https://github.com/warpdotdev/themes.git
```
{% endtab %}

{% tab title="Linux" %}
```
mkdir -p ${XDG_DATA_HOME:-$HOME/.local/share}/warp-terminal
cd ${XDG_DATA_HOME:-$HOME/.local/share}/warp-terminal/
git clone https://github.com/warpdotdev/themes.git
```
{% endtab %}
{% endtabs %}

Here is a step-by-step YouTube video that goes through these 2 steps for an example theme. Note the location for the files is based on macOS.

{% embed url="https://www.youtube.com/watch?v=UTYgwD-cLbk" %}
Adding a Custom Theme to Warp
{% endembed %}

## How do I use a custom theme in Warp?

1. To start, create the following directory:

{% tabs %}
{% tab title="macOS" %}
`mkdir -p ~/.warp/themes/`
{% endtab %}

{% tab title="Linux" %}
`mkdir -p ${XDG_DATA_HOME:-$HOME/.local/share}/warp-terminal/themes/`
{% endtab %}
{% endtabs %}

{% hint style="info" %}
It may take several minutes for Warp to initially discover the new themes directory. You can either wait or restart Warp. After that step, all future changes to the directory will be reflected within seconds.
{% endhint %}

2. Add your new custom theme yaml file to this directory:

```
cp ~/Downloads/my_awesome_theme.yaml {{path_to_your_themes_directory_from_step1}}
```

Your new theme should now be visible on the list of available themes.

## Create your custom theme, manually

Warp supports creating custom themes using .yaml files.

The format itself might expand, but we'll do our best to avoid breaking changes and maintain forward compatibility. We also plan on supporting sharing/creating custom themes directly within Warp.

A custom theme in Warp has the following `.yaml` structure:

```yaml
name: Custom Theme # Name for the theme
accent: '#268bd2' # Accent color for UI elements
background: '#002b36' # Terminal background color
foreground: '#839496' # The foreground color
cursor: '#d3a964' # The cursor color (optional; defaults to accent color if omitted)
details: darker # Whether the theme is lighter or darker
terminal_colors: # Ansi escape colors
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
{% hint style="info" %}
Each color is represented in hex and must start with `#`.
{% endhint %}

* `name`: Name for the theme, will show up in the Theme picker.
* `accent`: Color used for highlights in Warp's UI
* `background`: Color of background
* `foreground`: Color of foreground
* `cursor`: (Optional) color used for the cursor. Defaults to the `accent` color.
* `details`: Color used for detailing options
  * `darker`: Color used for dark theme
  * `lighter`: Color used for light-mode theme
* `terminal_colors`: Collection of normal & bright colors (16 total) known for other terminal themes (ANSI colors)

## Create your custom theme, automatically

Automatically create new themes based on a background image. Click the `+` button in the theme picker `Settings > Appearance > Current Theme` or search `Open Theme Picker` within the [Command Palette](../features/command-palette.md).

## Create your custom theme, with a tool

Use [Terminal-Themes](https://terminal-themes.com/) to create a custom theme and generate the appropriate RGB values for your custom theme. Once the YAML file is created, you can edit the file to add the background images or gradients.

## Background Images and Gradients

To add a background image you can use this attribute: `background_image:` with the name of the image you want to use as the background.

{% hint style="info" %}
Note: Warp currently only supports images with the _.jpg_ file format:

* `.jpeg`
* `.jpg`
* `.JPEG`
{% endhint %}

A `.yaml` config looks like this:

```yaml
name: Custom Theme
accent: '#268bd2'
background: '#002b36'
details: darker
foreground: '#839496'

############################################################### SEE BELOW
background_image:
  # the path is relative to ~/.warp/themes/
  # the full path to the picture is: ~/.warp/themes/warp.jpg
  path: warp.jpg
  # the opacity value is required and can range from 0-100
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

To set up a gradient, create a sublevel under accent with two key-value pairs:

* "left" and "right" or
* "top" and "bottom".

```yaml
accent:
  top: '#abcdef'
  bottom: '#fedcba'
```

```yaml
accent:
   left: '#abcdef'
   right: '#fedcba'
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

### Contributing

Contributions to this repo are greatly appreciated!

1. Fork the project
2. Create your branch with `git checkout -b theme/AwesomeTheme`
3. Regenerate thumbnails
4. Commit and open a pull request

Run this script to generate the thumbnails.

```
# Assuming you're adding the theme to the `standard` directory:
python3 ./scripts/gen_theme_previews.py standard
```

{% hint style="info" %}
Note: We cannot accept pull requests that include custom background images because:

* Licensing restrictions
* Trying to keep the binary size of the repo as small as possible (only the yaml files)

If your theme has an intended custom background image, include a comment in the yaml with a link to where people should download it.
{% endhint %}

## Community

All other Warp-related things can be discussed in our [Warp official repo](https://github.com/warpdotdev/Warp/discussions?discussions\_q=label%3ARoadmap+sort%3Atop) or our [Discord server](https://discord.gg/warpdotdev).

## Open source dependencies

We'd like to call out a few of the open-source themes and repositories that helped bootstrap the set of themes for Warp:

* [iTerm colors pencil](https://github.com/mattly/iterm-colors-pencil)
* [Alacritty-theme](https://github.com/eendroroy/alacritty-theme)
* [base16-Alacritty](https://github.com/aarowill/base16-alacritty)
* [base16](https://github.com/chriskempson/base16)
* [Solarized](https://ethanschoonover.com/solarized/)
* [Dracula](https://draculatheme.com/)
* [Gruvbox](https://github.com/morhetz/gruvbox)
