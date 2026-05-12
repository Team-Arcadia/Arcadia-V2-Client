# Contributing to Arcadia V2 / Contribuer

Thank you for your interest in contributing! | Merci de votre interet !

Arcadia V2 is a curated Minecraft modpack. Contributions cover **our originals only** — the third-party mod jars resolved by `manifest.json` are not part of this repo and are not under our control (see `LICENSE`).

Arcadia V2 est un modpack Minecraft curate. Les contributions concernent **uniquement nos originaux** — les jars de mods tiers resolus par `manifest.json` ne font pas partie de ce depot et ne sont pas sous notre controle (voir `LICENSE`).

## What can I contribute? / Que puis-je contribuer ?

- **KubeJS scripts** — `kubejs/server_scripts/`, `kubejs/startup_scripts/`, `kubejs/client_scripts/` — recipes, custom items, tags, mob tweaks, fixes
- **Custom assets** — Textures, sounds, lang files in `kubejs/assets/arcadia/` and the `arcadia_*` namespaces
- **Config overlays** — Modpack-shipped configurations under `config/` and `defaultconfigs/`
- **FTB Quests** — Quest content under `config/ftbquests/quests/` (chapters, lang files, structure)
- **ArcadiaLanguages resource pack** — Localization keys under `resourcepacks/ArcadiaLanguages/`
- **Documentation** — `README.md`, `kubejs/KUBEJS_GUIDE.md`, `RULES.md`, this file

## Prerequisites / Prerequis

- Java 21 (Temurin recommended)
- CurseForge or Prism Launcher (to install the pack locally for testing)
- A local NeoForge 1.21.1 server for testing server-side changes
- Familiarity with KubeJS 7.x for script contributions
- Python 3.11+ (for translation / pipeline tooling, optional)

## Setup / Installation

```bash
git clone https://github.com/Team-Arcadia/Arcadia-V2-Client.git
cd Arcadia-V2-Client
```

To run the modpack locally:
1. Install Arcadia V2 in CurseForge using `manifest.json` (or download the published pack)
2. Replace the launcher's instance overrides with this clone (or symlink)
3. Launch the game and verify your changes

Pour lancer le modpack localement : installer Arcadia V2 dans CurseForge avec `manifest.json` (ou telecharger le pack publie), remplacer les overrides de l instance du launcher par ce clone (ou symlink), lancer le jeu et verifier les changements.

## Code Conventions

- **Code, variables, logs**: English only
- **Naming**:
  - KubeJS files: `snake_case.js` — name describes the function, not the mod
  - Custom item / block IDs: `arcadia:snake_case`
  - Recipe IDs: every custom recipe MUST have an explicit `.id('arcadia:recipe_name')`
- **KubeJS priority directive**: `// Priority: N` at top of file (higher loads first)
- **No accents** in filenames or identifiers — ASCII only
- **Translations**: ALWAYS add entries to both `en_us.json` and `fr_fr.json` for new items, blocks, or messages
- **Tooltips**: use `Text.translate()` with lang keys, never hardcoded strings
- **SNBT files**: validate bracket balance and key format before committing — corrupted lang files silently break FTB Quests (see `ERROR_LOG.md`)

## Commit Messages

```
feat: add new feature
fix: resolve bug
refactor: restructure code
docs: update documentation
perf: improve performance
chore: tooling / repo housekeeping
```

## Branch Strategy

| Branch | Purpose | Merges into |
|--------|---------|-------------|
| `2.0.X`  | Stable releases (default branch) | - |
| `staging` | Pre-release testing | `2.0.X` |
| `develop` | Active development | `staging` |
| `feat/*` | New features | `develop` |
| `fix/*` | Bug fixes | `develop` |
| `hotfix/*` | Critical patches | `2.0.X` + `develop` |

## Pull Requests

- Target the appropriate branch per the table above
- Describe what was changed and why
- For KubeJS changes: confirm you tested with `/reload` (server scripts) or a server restart (startup scripts)
- For SNBT / lang changes: confirm structural integrity (brackets balanced, no malformed keys)
- Reference any related issue or in-game incident
- Keep the PR focused — one logical change per PR

## What NOT to contribute

- **Third-party mod jars** — they live on CurseForge, not in this repo
- **World saves** — `saves/` is git-ignored
- **Personal screenshots, server-list state, user-prefs** — git-ignored
- **Re-introducing files listed in `.gitignore`** — there is a reason each one is excluded

## Community / Communaute

- [Discord](https://discord.gg/xjF8Rtzyd4)
- [Website](https://arcadia-echoes-of-power.fr/)

By contributing, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) and license your originals under the project's MIT terms (see `LICENSE`).

En contribuant, vous acceptez de respecter notre [Code de conduite](CODE_OF_CONDUCT.md) et de placer vos originaux sous les termes MIT du projet (voir `LICENSE`).
