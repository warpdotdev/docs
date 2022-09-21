# Custom Themes

## What is it

You can add custom themes to Warp.

{% hint style="info" %}
A more thorough explanation of the theme format, together with examples and a collection of themes can be found in the [Warp themes repository](https://github.com/warpdotdev/themes).
{% endhint %}

## Warp's Custom Theme Repository

We have a [repository of themes hosted on GitHub.](https://github.com/warpdotdev/themes)

Each theme has a preview generated in the README.

The main difference between "standard" and "base16" themes is that "standard" themes follow the typical color setup, while "base16" themes follow the framework suggested by [@chriskempson](https://github.com/chriskempson/base16).

There are 2 ways to install a theme from this repo.

1. Download just a single file and follow the steps in the section below.
2. Clone the entire repo into `~/.warp/`

Here is a step-by-step Youtube video that goes through these 2 steps for an example theme.

{% embed url="https://www.youtube.com/watch?v=UTYgwD-cLbk" %}
Adding a Custom Theme to Warp
{% endembed %}

## How do I use a custom theme in Warp?

1. To start, create a config directory in your home directory:

```
mkdir -p ~/.warp/themes/
```

{% hint style="info" %}
Note that it may take several minutes for Warp to initially discover the new config directory. You can either wait or just restart the application. After that step, all future changes to `~/.warp/themes` directory will be reflected in Warp within seconds.
{% endhint %}

2\.  Add your new custom theme yaml theme file to this directory:

```
cp ~/Downloads/my_awesome_theme.yaml ~/.warp/themes/
```

Your new theme should now be visible on the list of available themes.

## How do I write my own custom theme?

Warp supports creating custom themes using .yaml files.&#x20;

The format itself might expand but we'll do our best to avoid breaking changes and maintain forward compatibility. We also plan on supporting sharing/creating custom themes directly within Warp.

A custom theme in Warp has the following .yaml structure:

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

Each color is represented in hex and must start with `#`.

* `accent`: Color used for highlights in Warp's UI
* `background`: Color of background
* `foreground`: Color of foreground
* `details`: Color used for detailing options
* `darker`: Color used for dark theme
* `lighter`: Color used for light-mode theme
* `terminal_theme`: Collection of normal & bright colors (16 total) known for other terminal themes (ansi colors)

## Background Images and Gradients

To add a background image you can use this attribute: `background_image:` with the name of the image you want to use as the background.&#x20;

{% hint style="info" %}
Note: Warp currently only supports images with the _.jpg_ file format:

* `.jpeg`
* `.jpg`
* `.JPEG`
{% endhint %}

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

## Contributing

Contributions to this repo are greatly appreciated!

1. Fork the project
2. Create your branch (`git checkout -b theme/AwesomeTheme`)
3. Regenerate thumbnails
4. Commit and open a pull request

Run this script to generate the thumbnails.

```
# assuming you're adding the theme to the `standard` directory:
python3 ./scripts/gen_theme_previews.py standard
```

{% hint style="info" %}
Note: We cannot accept pull requests that include custom background images because:

* Licensing restrictions
* Trying to keep the binary size of the repo as small as possible (just the yaml files)

If your theme has an intended custom background image, include a comment in the yaml with a link to where people should download it.
{% endhint %}

## Create your own theme with Warp-Themes.com

[Warp-Themes.com](https://warp-themes.com/) is a web app built entirely by community member [Torben Haack](https://twitter.com/torben_haack). The tool allows you to visually customize your own terminal theme with a few simple color selections, then download that theme file and have Warp load it into its theme picker. Please see more on how to use the app in our [Warp-Themes blog post](https://www.warp.dev/blog/create-custom-terminal-theme).

## Community

All other Warp-related things can be discussed in our [Warp official repo](https://github.com/warpdotdev/Warp/discussions?discussions\_q=label%3ARoadmap+sort%3Atop) or our [Discord server](https://discord.gg/warpdotdev).

## Open source dependencies

We'd like to call out a few of the open source themes and repositories that helped bootstrap the set of themes for Warp:

* [iTerm colors pencil](https://github.com/mattly/iterm-colors-pencil)
* [Alacritty-theme](https://github.com/eendroroy/alacritty-theme)
* [base16-Alacritty](https://github.com/aarowill/base16-alacritty)
* [base16](https://github.com/chriskempson/base16)
* [Solarized](https://ethanschoonover.com/solarized/)
* [Dracula](https://draculatheme.com/)
* [Gruvbox](https://github.com/morhetz/gruvbox)
