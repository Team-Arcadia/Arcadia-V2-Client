# Arcadia V2 — Echoes Of Power

A curated NeoForge 1.21.1 modpack designed for the **Arcadia** community server (30–50 players). Heavy cross-mod hardening, custom KubeJS content, bilingual EN/FR localization, and a complete FTB Quests progression.

## Features

- **Cross-mod recipe overhaul** — Iron/Gold/Diamond tools gated behind Create sheets, every tech mod (Mekanism, TFMG, Immersive Engineering, Refined Storage, Create addons) interlinked via bridge components
- **4 Custom bridge items** — Arcane Circuit, Ethereal Alloy, Industrial Heart, Rune Matrix progressively gate cross-mod progression
- **Fusion Core mega-chain** — 5-tier endgame crafting chain culminating in a 9×9 Mechanical Crafting recipe
- **Custom Adept & Heretic armor sets** — 4 pieces + 10 unique companion items each, full lore textures
- **20 custom music discs** — Original tracks with dedicated vinyl textures and jukebox-song integration
- **FTB Quests pack** — 7 languages (EN-US, EN-GB, FR, ES, PT-BR, RU, ZH-CN), 25 000+ translation entries
- **152 banned items** — 3-layer enforcement (recipe removal + inventory scan + JEI/creative hide)
- **Mob rebalance** — Boss HP ×2.5 to ×8, twilight/mowzie/iron-spellbook bosses individually tuned
- **Loot nerfs** — Diamond 0.5%, Netherite 0.01%, Artifacts craft-only, backpacks/twilight scaled
- **Apotheosis tuning** — Rarity weights, mythic-only Winged affix, gated flight potions (Dragon's Breath + Nether Star)
- **FancyMenu branding** — Localized main menu, server selection, loading screens
- **ArcadiaLanguages resource pack** — Forced load via ResourcePackOverrides, fixes EN-leak gaps from upstream mods

## Requirements

| Dependency | Version |
|------------|---------|
| Minecraft  | 1.21.1  |
| NeoForge   | 21.1.232+ |
| Java       | 21      |
| CurseForge or Prism Launcher | Required for manifest-based install |

## Installation

### Players (CurseForge)
1. Open CurseForge launcher
2. Import the `manifest.json` from this repository (or download the official pack from CurseForge)
3. Launcher resolves all 456 entries (443 mods + 13 shaders) automatically
4. Launch and join `arcadia.echoes-of-power.fr`

### Server admins
1. Clone this repository
2. Use the included `manifest.json` to fetch all mods via CurseForge Core / packwiz
3. Apply the `config/`, `defaultconfigs/`, `kubejs/`, `resourcepacks/ArcadiaLanguages/` overrides
4. Start your NeoForge 21.1.232+ server

## Repository Contents

This repo ships only what we author or maintain. Third-party mod jars are resolved via `manifest.json` on CurseForge import.

| Path | Purpose |
|------|---------|
| `manifest.json` | CurseForge modpack manifest (456 entries: 443 mods + 13 shaderpacks) |
| `STRUCTURE.md` | Full structural map of the instance (bilingual) |
| `CHANGELOG.md` | Change history by date (bilingual) |
| `CREDITS.md` | Team, contributors and thanks (bilingual) |
| `config/` | Modpack-shipped configurations (overrides upstream defaults) |
| `defaultconfigs/` | Canonical defaults distributed by DefaultOptions |
| `kubejs/` | Custom scripts, items, recipes, tags, lang files |
| `resourcepacks/ArcadiaLanguages/` | In-house localization pack |
| `LICENSE` | Proprietary source-available (private use only) + third-party/affiliation disclaimers |

## Credits

- **Author** — vyrriox
- **Organization** — Team Arcadia
- **Full team & thanks** — See `CREDITS.md`
- **License** — Proprietary source-available: contributions welcome, private copies/modifications allowed, redistribution and republication prohibited (see `LICENSE`)
- **Discord** — [discord.gg/xjF8Rtzyd4](https://discord.gg/xjF8Rtzyd4)
- **Website** — [arcadia-echoes-of-power.fr](https://arcadia-echoes-of-power.fr/)

---

# Arcadia V2 — Echoes Of Power (Version Francaise)

Un modpack NeoForge 1.21.1 curate, conu pour le serveur communautaire **Arcadia** (30 a 50 joueurs). Hardening cross-mod massif, contenu KubeJS custom, localisation bilingue EN/FR, et une progression FTB Quests complete.

## Caracteristiques

- **Refonte des recettes cross-mod** — Outils Fer/Or/Diamant gates derriere les plaques Create, chaque mod tech (Mekanism, TFMG, Immersive Engineering, Refined Storage, addons Create) interconnecte via des composants pont
- **4 items pont custom** — Circuit Arcane, Alliage Etheree, Coeur Industriel, Matrice de Runes pour gater progressivement la progression cross-mod
- **Mega-chaine Fusion Core** — 5 tiers de crafting endgame culminant en recette 9x9 Mechanical Crafting
- **Sets d armures Adept et Heretique** — 4 pieces + 10 items compagnons uniques chacun, textures completes
- **20 disques de musique customs** — Pistes originales avec textures vinyle dediees et integration jukebox-song
- **Pack FTB Quests** — 7 langues (EN-US, EN-GB, FR, ES, PT-BR, RU, ZH-CN), 25 000+ entrees de traduction
- **152 items bannis** — Application 3 couches (suppression de recette + scan d inventaire + masquage JEI/creatif)
- **Rebalance des mobs** — HP des boss x2.5 a x8, boss twilight/mowzie/iron-spellbook regles individuellement
- **Nerfs de loot** — Diamant 0.5%, Netherite 0.01%, Artifacts craft uniquement, sacs/twilight reduits
- **Tuning Apotheosis** — Poids des raretes, affixe Winged mythique uniquement, potions de vol gatees (Dragon Breath + Etoile Nether)
- **Branding FancyMenu** — Menu principal localise, selection de serveur, ecrans de chargement
- **Resource pack ArcadiaLanguages** — Chargement force via ResourcePackOverrides, corrige les fuites EN des mods upstream

## Prerequis

| Dependance | Version |
|------------|---------|
| Minecraft  | 1.21.1  |
| NeoForge   | 21.1.232+ |
| Java       | 21      |
| CurseForge ou Prism Launcher | Requis pour installation via manifest |

## Installation

### Joueurs (CurseForge)
1. Ouvrir le launcher CurseForge
2. Importer le `manifest.json` de ce depot (ou telecharger le pack officiel depuis CurseForge)
3. Le launcher resout les 456 entrees (443 mods + 13 shaders) automatiquement
4. Lancer et rejoindre `arcadia.echoes-of-power.fr`

### Admins serveur
1. Cloner ce depot
2. Utiliser le `manifest.json` fourni pour recuperer tous les mods via CurseForge Core / packwiz
3. Appliquer les overrides `config/`, `defaultconfigs/`, `kubejs/`, `resourcepacks/ArcadiaLanguages/`
4. Demarrer un serveur NeoForge 21.1.232+

## Contenu du depot

Ce depot ne contient que ce que nous avons ecrit ou maintenons. Les jars de mods tiers sont resolus via `manifest.json` lors de l import CurseForge.

| Chemin | Role |
|--------|------|
| `manifest.json` | Manifest CurseForge du modpack (456 entrees : 443 mods + 13 shaderpacks) |
| `STRUCTURE.md` | Carte structurelle complete de l instance (bilingue) |
| `CHANGELOG.md` | Historique des changements par date (bilingue) |
| `CREDITS.md` | Equipe, contributeurs et remerciements (bilingue) |
| `config/` | Configurations livrees par le modpack (override les defauts amont) |
| `defaultconfigs/` | Defauts canoniques distribues par DefaultOptions |
| `kubejs/` | Scripts, items, recettes, tags, fichiers lang customs |
| `resourcepacks/ArcadiaLanguages/` | Pack de localisation maison |
| `LICENSE` | Licence proprietaire source visible (usage prive uniquement) + clauses tiers/non-affiliation |

## Credits

- **Auteur** — vyrriox
- **Organisation** — Team Arcadia
- **Equipe complete & remerciements** — Voir `CREDITS.md`
- **Licence** — Proprietaire source visible : contributions bienvenues, copies/modifications privees autorisees, redistribution et republication interdites (voir `LICENSE`)
- **Discord** — [discord.gg/xjF8Rtzyd4](https://discord.gg/xjF8Rtzyd4)
- **Site web** — [arcadia-echoes-of-power.fr](https://arcadia-echoes-of-power.fr/)
