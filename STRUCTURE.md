# Arcadia V2 — Modpack Structure

Complete structural map of the Arcadia V2 "Echoes Of Power" instance (Minecraft 1.21.1 · NeoForge 21.1.221 · v2.0.10).

## Top-Level Layout

```
Arcadia V2/
├── manifest.json            CurseForge manifest — 450 mods resolved at import
├── minecraftinstance.json   CurseForge instance metadata (very large — grep, don't read whole)
├── README.md                Bilingual EN/FR repository documentation
├── CURSEFORGE_PAGE.md       HTML source of the CurseForge project page
├── CHANGELOG.md             Bilingual version history
├── STRUCTURE.md             This file
├── RULES.md                 Project rules & AI/IDE instructions
├── ERROR_LOG.md             Session error log with prevention rules
├── LICENSE                  MIT (our originals) + third-party scope disclaimers
│
├── mods/                    446 active .jar (incl. 8 in-house arcadia-* mods) + 1 disabled
├── config/                  ~1,156 files — modpack-shipped configuration overrides
├── defaultconfigs/          ~1,170 files — full mirror of config/ (new-world defaults)
├── kubejs/                  ~2,012 files — custom scripting ecosystem (see below)
├── datapacks/               Empty — all data lives in kubejs/data/
├── resourcepacks/           ArcadiaLanguages (in-house localization) + hud.zip
├── shaderpacks/             13 curated shaders (BSL, Bliss, Complementary, ...)
│
├── saves/TEST/              Active QA test world
├── ESM/                     Historical snapshot archives — never modify
├── logs/, debug/            Runtime logs (not tracked in git)
└── local/, downloads/, ...  Launcher/runtime caches (not tracked)
```

## config/ — Key Areas

| Path | Purpose |
|------|---------|
| `config/arcadia/` | In-house server-side progression & admin config (production — handle with care) |
| `config/fancymenu/` | Branded "Echoes Of Power" main menu, server selection, loading screens |
| `config/ftbquests/quests/` | 31 quest chapters, 3,000+ quests, 7-language lang files |
| `config/jei/` | Ingredient blacklist & curated sort order |
| `config/ars_nouveau/` | Magic balance tuning (intentionally nerfed) |
| `config/spark/` | Profiler output (runtime data, excluded from defaultconfigs) |

`defaultconfigs/` mirrors `config/` in full so every new world and server install starts from the curated defaults. Exclusions: `spark/` (runtime profiling data) and `arcadia/arcadiaadminpanel/logins.json` (credentials — never distributed).

## kubejs/ — Custom Scripting Ecosystem

```
kubejs/
├── KUBEJS_GUIDE.md          Staff guide — READ FIRST before touching any script
├── modified_recipes.txt     Recipe change log
│
├── startup_scripts/         9 scripts — registries & UI (need full restart)
│   ├── registry/            armor_tiers, block_registry, item_registry,
│   │                        item_stat_tweaks, sound_registry
│   ├── compat/              Cross-mod startup compatibility patches
│   └── ui/                  Custom UI registration
│
├── server_scripts/          33 scripts — recipes, mobs, items, fixes (/reload)
│   ├── recipes/create/      Create & addon recipe overhauls
│   ├── recipes/custom/      Arcadia custom items (bridges, Fusion Core chain)
│   ├── recipes/overhaul/    Cross-mod gating (tools behind Create sheets, ...)
│   ├── items/banned/        152-item ban enforcement (recipe removal + inventory scan)
│   ├── items/loot/          Loot table nerfs (diamond 0.5%, netherite 0.01%)
│   ├── mobs/                Boss HP ×2.5–×8, damage nerfs, merchant trade filter
│   ├── fixes/compat/        Cross-mod bug fixes (steel arbitrage lock, ...)
│   └── tags/                Tag adjustments
│
├── client_scripts/          1 script — bilingual item tooltips
├── data/                    1,465 JSON — recipes/tags/loot for apotheosis, apothic,
│                            arcadia jukebox, createoreexcavation, ...
├── assets/arcadia/          497 files — textures, models, 7 lang files, sounds
└── config/                  KubeJS client/common/web_server settings
```

## In-House Arcadia Mods (8)

`arcadia-lib`, `arcadia-admin-panel`, `arcadia-ah`, `arcadia-patch-create`, `arcadia-pets`, `arcadia-prestige`, `arcadia_spawn`, `arcadiaguard`

---

# Arcadia V2 — Structure du Modpack (Version Française)

Carte structurelle complète de l'instance Arcadia V2 « Echoes Of Power » (Minecraft 1.21.1 · NeoForge 21.1.221 · v2.0.10).

## Arborescence Racine

```
Arcadia V2/
├── manifest.json            Manifest CurseForge — 450 mods résolus à l'import
├── minecraftinstance.json   Métadonnées d'instance CurseForge (très volumineux)
├── README.md                Documentation bilingue EN/FR du dépôt
├── CURSEFORGE_PAGE.md       Source HTML de la page CurseForge
├── CHANGELOG.md             Historique des versions bilingue
├── STRUCTURE.md             Ce fichier
├── RULES.md                 Règles projet & instructions AI/IDE
├── ERROR_LOG.md             Journal d'erreurs avec règles de prévention
├── LICENSE                  MIT (nos originaux) + clauses de contenu tiers
│
├── mods/                    446 .jar actifs (dont 8 mods maison arcadia-*) + 1 désactivé
├── config/                  ~1 156 fichiers — configurations livrées par le modpack
├── defaultconfigs/          ~1 170 fichiers — miroir complet de config/ (défauts nouveaux mondes)
├── kubejs/                  ~2 012 fichiers — écosystème de scripts custom (voir plus bas)
├── datapacks/               Vide — toutes les données sont dans kubejs/data/
├── resourcepacks/           ArcadiaLanguages (localisation maison) + hud.zip
├── shaderpacks/             13 shaders sélectionnés (BSL, Bliss, Complementary, ...)
│
├── saves/TEST/              Monde de test QA actif
├── ESM/                     Archives de snapshots historiques — ne jamais modifier
├── logs/, debug/            Logs runtime (non suivis par git)
└── local/, downloads/, ...  Caches launcher/runtime (non suivis)
```

## config/ — Zones Clés

| Chemin | Rôle |
|--------|------|
| `config/arcadia/` | Config maison de progression & admin côté serveur (production — prudence) |
| `config/fancymenu/` | Menu principal « Echoes Of Power », sélection de serveur, écrans de chargement |
| `config/ftbquests/quests/` | 31 chapitres, 3 000+ quêtes, fichiers lang en 7 langues |
| `config/jei/` | Blacklist d'ingrédients & ordre de tri organisé |
| `config/ars_nouveau/` | Équilibrage magie (nerfs intentionnels) |
| `config/spark/` | Sorties du profiler (données runtime, exclues de defaultconfigs) |

`defaultconfigs/` reflète intégralement `config/` afin que chaque nouveau monde et chaque installation serveur parte des défauts organisés. Exclusions : `spark/` (données de profiling runtime) et `arcadia/arcadiaadminpanel/logins.json` (identifiants — jamais distribués).

## kubejs/ — Écosystème de Scripts Custom

```
kubejs/
├── KUBEJS_GUIDE.md          Guide staff — À LIRE AVANT de toucher un script
├── modified_recipes.txt     Journal des modifications de recettes
│
├── startup_scripts/         9 scripts — registres & UI (redémarrage complet requis)
│   ├── registry/            armor_tiers, block_registry, item_registry,
│   │                        item_stat_tweaks, sound_registry
│   ├── compat/              Patchs de compatibilité cross-mod au démarrage
│   └── ui/                  Enregistrement des UI custom
│
├── server_scripts/          33 scripts — recettes, mobs, items, fixes (/reload)
│   ├── recipes/create/      Refontes de recettes Create & addons
│   ├── recipes/custom/      Items custom Arcadia (ponts, chaîne Fusion Core)
│   ├── recipes/overhaul/    Gating cross-mod (outils derrière les plaques Create, ...)
│   ├── items/banned/        Application des 152 bans (suppression recettes + scan inventaire)
│   ├── items/loot/          Nerfs de loot (diamant 0.5%, netherite 0.01%)
│   ├── mobs/                HP boss ×2.5–×8, nerfs de dégâts, filtre de trades marchands
│   ├── fixes/compat/        Correctifs cross-mod (verrou arbitrage acier, ...)
│   └── tags/                Ajustements de tags
│
├── client_scripts/          1 script — tooltips d'items bilingues
├── data/                    1 465 JSON — recettes/tags/loot pour apotheosis, apothic,
│                            jukebox arcadia, createoreexcavation, ...
├── assets/arcadia/          497 fichiers — textures, modèles, 7 fichiers lang, sons
└── config/                  Réglages KubeJS client/common/web_server
```

## Mods Maison Arcadia (8)

`arcadia-lib`, `arcadia-admin-panel`, `arcadia-ah`, `arcadia-patch-create`, `arcadia-pets`, `arcadia-prestige`, `arcadia_spawn`, `arcadiaguard`
