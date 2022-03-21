# Documentation

Test the documentation locally by installing honkit from npm.

[https://github.com/honkit/honkit#installation](https://github.com/honkit/honkit#installation)

The youtube embed in the introduction (getting_started) does not work with honkit. So comment that section out.

You can also rebase the honkit branch ontop of whatever changes you've made and then run honkit from there.

## Open Source Licenses

Note: The script is in python version 3.10.0. 
Python 3.10 is really nice, check out the [structural pattern matching (622)](https://www.python.org/dev/peps/pep-0622/)

### Installation

Install poetry (pip)

```sh
pip install poetry
```

Run poetry install to get all the dependencies

```sh
poetry install
```

### Running pipeline

Open up the settings.toml file to change the script configuration settings.

```shell
python3 ./src/main.py
```

### Data

Store the outputted .json files from running ScanCode and or Cargo License into the data folder.
This is where the script looks for the raw files to parse into markdown. The location and files to use can be changed in settings.toml.

The script picks up the file that matches the keywords passed into the filtering conditions variable in the settings.
toml.

### PRD

See [Open Source Licenses PRD](https://docs.google.com/document/d/1i9TMtcphwLSlpnb3P7We-RNkDiDQEWo6dq1gJrnKsyc/edit#)

## Scan Code

Download [scancode tool](https://scancode-toolkit.readthedocs.io/en/latest/getting-started/home.html)

Run the tool on our warp-internal codebase.
I recommend spinning up a VM in GCP, uploading a zip of warp-internal, and running it with an high compute instance with multiple cores.
See all the available [ScanCode flags](https://scancode-toolkit.readthedocs.io/en/latest/cli-reference/list-options.
html#cli-list-options).

When you do run the scan use this command:

```shell
scancode -clpeui -n <available-cores> --json-pp YYYY_MM_DD-scancode-raw.json warp-internal
```

### Analyzing results

Download Scancode workbench [https://github.com/nexB/scancode-workbench/releases](https://github.com/nexB/scancode-workbench/releases)

Import the json from your scan or the one that is in this repo into workbench.

Workbench [Wiki](https://github.com/nexB/scancode-workbench/wiki/)

## Cargo Licenses

Install cargo licenses

```shell
cargo install cargo-license
```

Run cargo licenses in warp-internal (it picks up Cargo.lock)

```shell
cargo license --all-features --json > YYYY_MM_dd-cargo.raw.json
```

Proceed to move the outputted json into the src > data folder in this repo (warpdotdev/license).
