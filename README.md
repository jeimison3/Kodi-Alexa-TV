# Kodi Alexa TV
[![Kodi version](https://img.shields.io/badge/kodi%20versions-18--19-blue)](https://kodi.tv/)
[![GitHub release](https://img.shields.io/github/release/jeimison3/Kodi-Alexa-TV.svg)](https://github.com/jeimison3/Kodi-Alexa-TV/releases)
[![Contributors](https://img.shields.io/github/contributors/jeimison3/Kodi-Alexa-TV.svg)](https://github.com/jeimison3/Kodi-Alexa-TV/graphs/contributors)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![](https://img.shields.io/badge/author-jeimison3-green.svg)](https://github.com/jeimison3)

Integration between Alexa Home Assistant and LibreELEC (Kodi 19 @ Raspberry Pi).

Bugs/suggestions on [Kodi Forum](https://forum.kodi.tv/showthread.php?tid=360265).

## Disclaimer

This plugin is not officially commissioned/supported by SinricPro.
It's a community plugin.

Some libraries ported in the final release are under other licenses, they are: Python Websockets, over BSD 3.

## Installing via .zip
Just download a release.

## Setup keys
After installed,
- Open your browser on `http://(KODI_IP):51494/alexatv`
- Fill each input with your keys
- Then press `Save and reboot` button. Kodi will restart.

Important: Create a `Device` on SinricPro Dashboard with type `TV`.

## Building:
```shell
git clone --recurse-submodules https://github.com/jeimison3/Kodi-Alexa-TV.git
```
To run on local tests, configure your `config/credentials.py` and run `python3 addon.py`.

### Build .zip with:
```sh
sh prepare.sh
```
