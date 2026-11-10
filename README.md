# Tinkerbox Beta

Tinkerbox – Your interface, unlocked. The World of Warcraft addon manager of the Video Game
Almanach family, first for *World of Warcraft: Forever*.

This repository carries Tinkerbox's releases only; the source is kept elsewhere.

## Install

**Windows** (PowerShell):

```
irm https://github.com/VivianVossNet/tinkerbox.pub/releases/latest/download/install.ps1 | iex
```

**macOS** (Terminal):

```
curl -fsSL https://github.com/VivianVossNet/tinkerbox.pub/releases/latest/download/install.sh | sh
```

The script finds the newest release, loads the setup for your system, checks its SHA-256 against
`SHA256SUMS` and starts it. The setup opens its own window and installs Tinkerbox Beta for you
alone, without administrator rights:

| System | Where | Found in |
|---|---|---|
| Windows x86_64 | `%LOCALAPPDATA%\Programs\Tinkerbox Beta` | the Start menu, the desktop if you choose, *Apps* to uninstall |
| macOS arm64 | `/Applications/Tinkerbox Beta.app` | Applications and Launchpad |

Linux follows.

Each release also carries the setups themselves, `tinkerbox-setup-windows-x86_64.exe` and
`tinkerbox-setup-macos-arm64`, for anyone who prefers to download and start one by hand.

## Beta

Tinkerbox is in beta: unsigned for now, so Windows may ask once whether to run it.

Licensed under the BSD-3-Clause. Copyright 2026 Vivian Voss.
