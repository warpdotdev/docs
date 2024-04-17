---
description: A step-by-step guide for setting up Warp on your machine.
---

# Installing & Onboarding

{% hint style="info" %}
**Platform support:** Warp is currently supported on Mac (both Intel and Mac Silicon) and Linux (x86\_64). We have plans to support Windows and the Web (WASM)!\
Subscribe to get notified when Warp is available for [Windows](https://warp.dev/windows-terminal). Please see our [Known Issues](../help/known-issues.md) for any issues running Warp or [contact us](../help/sending-us-feedback.md#sending-warp-feedback).
{% endhint %}

## Installing and Running Warp

{% hint style="warning" %}
**Visit** [**known issues**](../help/known-issues.md) **to get more details on setting up and troubleshooting Warp.**
{% endhint %}

{% tabs %}
{% tab title="macOS" %}
{% hint style="info" %}
**Requirements:** Minimum requirements are macOS 10.14 or above and hardware that supports [Metal](https://support.apple.com/en-us/HT205073).
{% endhint %}

There are two ways to get Warp onto your machine:

**Download Warp at the link below and Drag into your Application folder**

{% embed url="https://app.warp.dev/get_warp" %}
Link to Download Warp
{% endembed %}

**Install using Homebrew by running the command below**

```
brew install --cask warp
```

**Running Warp on Mac**

Find the Warp in your Applications folder and run it from there (or search for Warp in Spotlight/Raycast).
{% endtab %}

{% tab title="Linux" %}
{% hint style="info" %}
**Requirements:** Minimum requirement is a x86\_64 Linux distribution with glibc >= 2.31 (released Feb. 2020) and support for _either_ [OpenGL ES 3.0+ or Vulkan](https://github.com/gfx-rs/wgpu?tab=readme-ov-file#supported-platforms). We are tracking support requests for [ARM](https://github.com/warpdotdev/Warp/issues/4213) and [WSL](https://github.com/warpdotdev/Warp/issues/4240).

This includes (but is not limited to) the following:

* Ubuntu 20.04
* Debian 11 ("bullseye")
* Fedora 32
* Arch Linux
{% endhint %}

Visit the [Warp download page](https://app.warp.dev/get\_warp?auto\_download=false\&linux=true) for the full list of available installation options. All installation options support auto-update, ensuring you receive new features, bug fixes, and performance improvements.

**Debian- and Ubuntu-based distributions**

The easiest way to install Warp is to download and install the [.deb package](https://app.warp.dev/download?package=deb). After downloading, you can install the package with:

```
sudo apt install ./<file>.deb
```

Installing the .deb package will automatically set up the Warp apt repository and signing key needed to automatically update Warp and verify the integrity of the downloaded packages.

Alternatively, you can manually configure the Warp apt repository and install Warp by running the following commands:

```
sudo apt-get install wget gpg
wget -qO- https://releases.warp.dev/linux/keys/warp.asc | gpg --dearmor > warpdotdev.gpg
sudo install -D -o root -g root -m 644 warpdotdev.gpg /etc/apt/keyrings/warpdotdev.gpg
sudo sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/warpdotdev.gpg] https://releases.warp.dev/linux/deb stable main" > /etc/apt/sources.list.d/warpdotdev.list'
rm warpdotdev.gpg
sudo apt update && sudo apt install warp-terminal
```

**RHEL-, Fedora-, and CentOS-based distributions**

The easiest way to install Warp is to download and install the [.rpm package](https://app.warp.dev/download?package=rpm). After downloading, you can install the package with:

```
sudo dnf install ./<file>.rpm
```

Installing the .rpm package will automatically set up the Warp yum repository. On first update, `dnf` will retrieve the signing key needed to verify the integrity of the downloaded packages.

Alternatively, you can manually configure the Warp yum repository and install Warp by running the following commands:

```
sudo rpm --import https://releases.warp.dev/linux/keys/warp.asc
sudo sh -c 'echo -e "[warpdotdev]\nname=warpdotdev\nbaseurl=https://releases.warp.dev/linux/rpm/stable\nenabled=1\ngpgcheck=1\ngpgkey=https://releases.warp.dev/linux/keys/warp.asc" > /etc/yum.repos.d/warpdotdev.repo'
sudo dnf install warp-terminal
```

**Arch Linux-based distributions**

The easiest way to install Warp is to download and install the [.pkg.tar.zst package](https://app.warp.dev/download?package=pacman). After downloading, you can install the package with:

```
sudo pacman -U ./<file>.pkg.tar.zst
```

The first time you update Warp through the app, it will guide you through setting up the Warp pacman repository and signing key.

Alternatively, you can manually configure the Warp pacman repository and install Warp by running the following commands:

```
sudo sh -c "echo -e '\n[warpdotdev]\nServer = https://releases.warp.dev/linux/pacman/\$repo/\$arch' >> /etc/pacman.conf"
sudo pacman-key -r "linux-maintainers@warp.dev"
sudo pacman-key --lsign-key "linux-maintainers@warp.dev"
sudo pacman -Sy warp-terminal
```

**OpenSUSE- and SLE-based distributions**

The Warp yum repository also works for OpenSUSE- and SLE-based systems. Download and install the [.rpm package](https://app.warp.dev/download?package=rpm). After downloading, you can install the package with:

```
sudo zypper install ./<file>.rpm
```

Installing the .rpm package will automatically set up the Warp yum repository. On first update, `zypper` will retrieve the signing key needed to verify the integrity of the downloaded packages.

Alternatively, you can manually configure the Warp yum repository and install Warp by running the following commands:

```
sudo rpm --import https://releases.warp.dev/linux/keys/warp.asc
sudo sh -c 'echo -e "[warpdotdev]\nname=warpdotdev\ntype=rpm-md\nbaseurl=https://releases.warp.dev/linux/rpm/stable\nenabled=1\nautorefresh=1\ngpgcheck=1\ngpgkey=https://releases.warp.dev/linux/keys/warp.asc\nkeeppackages=0" > /etc/zypp/repos.d/warpdotdev.repo'
sudo zypper install warp-terminal
```

**AppImage**

We also provide an AppImage ([https://appimage.org](https://appimage.org)), a single-file executable version of Warp. Installing Warp via a package manager is recommended, however, as it will ensure your system has all necessary dependencies installed.

You can download the Warp AppImage with the following commands:

```
curl -L "https://app.warp.dev/download?package=appimage" -o Warp-x86_64.AppImage
chmod +x Warp-x86_64.AppImage
```

**Running Warp on Linux**

If you installed a package, find Warp in your desktop manager or run `warp-terminal` on your terminal.\
If you're using the AppImage, you can launch it by navigating to the directory where the AppImage is located and running `./Warp-x86_64.AppImage`.
{% endtab %}
{% endtabs %}

## Shell Compatibility

Locally, the terminal integrates with bash, zsh, or fish. Reference [using Warp with \[bash|zsh|fish\] ](using-warp-with-shells.md)for more details.

## Onboarding

### Logging into Warp (Required)

Unlike classic terminals, Warp requires you to [sign up](https://app.warp.dev/signup) and [log in](https://app.warp.dev/login) to get started with the app. Unique user identity is required to support Warp's collaborative features and it makes it easier for the Warp team to provide customer support, should you need to debug an issue.

{% hint style="info" %}
Issues with login? Check out the [login troubleshooting page](../help/troubleshooting-login-issues.md).
{% endhint %}

After installing Warp for the first time, you will be prompted to log in with GitHub, Google, SSO for Enterprise, or with an email link.

{% hint style="info" %}
If you log in with Google or GitHub, Warp only gets access to the associated email address. If you want to learn more, [read our approach to privacy](https://www.warp.dev/privacy).
{% endhint %}

Opening the app is the only time you need an active internet connection. Otherwise, Warp is a fully-native, local app that runs fine with no internet connection (although you will lose access to some [cooler features](../help/using-warp-offline.md)).

### Onboarding Survey (Optional)

Warp will ask a few questions within the app after you sign up.

The survey is optional. You can skip all questions if you’d like.

{% hint style="info" %}
Why do we ask these? Understanding how you use the terminal helps us improve the product and prioritize the right features to build.
{% endhint %}

### Customizing Warp

Warp has many [Appearance](../appearance/themes.md) settings you can configure, including themes, fonts, opacity, and input position. Navigate to `Settings > Appearance` to customize your setup.
