---
description: >-
  Secret Redaction attempts to automatically redact secrets and sensitive
  information in your terminal output, including passwords, IP addresses, API
  keys, and PII.
---

# Secret Redaction

## How to access it

Disabled by default, to enable Secret Redaction open `Settings > Privacy > Secret Redaction` or type in "Secret Redaction" to toggle it in the [Command Palette](command-palette.md).

## How it works

Secret Redaction attempts to detect sensitive data (including secrets, passwords, API keys, and PII) using a list of default regex patterns and then masks it with asterisks. Clicking on a secret will display a tooltip that lets you reveal the secret or copy the secret's contents. When trying to copy terminal output containing secrets, it will be copied as asterisks (e.g. `echo password` becomes `echo ********`) unless revealed or copied from the tooltip. Secret redaction is not applied in shared sessions.

You can add additional custom regex for secrets you want to include in `Settings > Privacy > Secret Redaction > Custom Secret Redaction`.

Secret redaction **always** applies to AI interactions, regardless of this setting. Your secrets will never be sent to AI.

## Secret Regex List

Here is a list of the default regular expressions that Warp uses to identify secrets.

| Secret Type                               | Regex Pattern                                                                             |
| ----------------------------------------- | ----------------------------------------------------------------------------------------- |
| IP V4 Address                             | `\b((25[0-5]\|(2[0-4]\|1\d\|[1-9]\|)\d)\.?\b){4}\b`                                       |
| IP V6 Address                             | `\b((([0-9A-Fa-f]{1,4}:){1,6}:)\|(([0-9A-Fa-f]{1,4}:){7}))([0-9A-Fa-f]{1,4})\b`           |
| Slack App Token                           | `\bxapp-[0-9]+-[A-Za-z0-9_]+-[0-9]+-[a-f0-9]+\b`                                          |
| Phone Number                              | `\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b`                                     |
| AWS Access ID                             | `\b(AKIA\|A3T\|AGPA\|AIDA\|AROA\|AIPA\|ANPA\|ANVA\|ASIA)[A-Z0-9]{12,}\b`                  |
| MAC Address                               | `\b((([a-zA-z0-9]{2}[-:]){5}([a-zA-z0-9]{2}))\|(([a-zA-z0-9]{2}:){5}([a-zA-z0-9]{2})))\b` |
| Google API Key                            | `\bAIza[0-9A-Za-z-_]{35}\b`                                                               |
| Google OAuth ID                           | `\b[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com\b`                               |
| Github Classic Personal Access Token      | `\bghp_[A-Za-z0-9_]{36}\b`                                                                |
| Github Fine Grained Personal Access Token | `\bgithub_pat_[A-Za-z0-9_]{82}\b`                                                         |
| Github OAuth Access Token                 | `\bgho_[A-Za-z0-9_]{36}\b`                                                                |
| Github User to Server Token               | `\bghu_[A-Za-z0-9_]{36}\b`                                                                |
| Github Server to Server Token             | `\bghs_[A-Za-z0-9_]{36}\b`                                                                |
| Heroku API Key                            | `\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b`         |
| Stripe Key                                | `\b(?:r\|s)k_(test\|live)_[0-9a-zA-Z]{24}\b`                                              |
| Firebase Auth Domain                      | `\b([a-z0-9-]){1,30}(\.firebaseapp\.com)\b`                                               |
| JSON web token                            | `\b(ey[a-zA-z0-9_\-=]{10,}\.){2}[a-zA-z0-9_\-=]{10,}\b`                               |
| OpenAI API Key                            | `\bsk-[a-zA-Z0-9]{48}\b`                               |
| Anthropic API Key                         | `\bsk-ant-api\d{0,2}-[a-zA-Z0-9\-]{80,120}\b`                               |
| Fireworks API Key                         | `\bfw_[a-zA-Z0-9]{24}\b`                               |
