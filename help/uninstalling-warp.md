# Uninstalling Warp

Removing Warp from your computer involves uninstalling Warp and then removing any files or data.

### Uninstalling Warp installed via dmg

* Remove Warp with `sudo rm -r /Applications/Warp.app`

### Uninstalling Warp installed via Brew

* Remove Warp with `brew uninstall warp`
* Clean up old versions of Warp formulae and small kegs of data with `brew cleanup warp`

## Removing Warp logins, files, logs, and database

* Remove Warp user login with `sudo security delete-generic-password -l "dev.warp.Warp-Stable" $HOME/Library/Keychains/login.keychain`
* Remove Warp user files and logs with `sudo rm -r $HOME/.warp/ $HOME/Library/Logs/warp.log`
R* emove Warp database with `sudo rm -r "$HOME/Library/Application Support/dev.warp.Warp-Stable"`
