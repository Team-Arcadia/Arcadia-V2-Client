# Arcadia V2 - Complete Modpack Reference

Master reference of the Arcadia V2 "Echoes Of Power" instance. Everything is indexed here: directories, general configuration, content systems, and where to go for each kind of change.

## 1. Identity

| Field | Value |
|-------|-------|
| Name | Arcadia V2: Echoes Of Power |
| Minecraft | 1.21.1 |
| Loader | NeoForge 21.1.232 |
| Java | 21 (8+ GB RAM recommended) |
| Manifest | 455 CurseForge entries (442 mods + 13 shaderpacks) |
| Local jars | 445 active (incl. in-house mods and patched jars) |
| Target | Community server, 30-50 players, also fully solo-viable |
| Languages | Docs EN/FR, items in 7 locales, quests in 7 locales |
| License | Proprietary source-available (see `LICENSE`) |
| Team | See `CREDITS.md` |

## 2. Top-Level Layout

```
Arcadia V2/
├── manifest.json            CurseForge manifest, 455 entries resolved at import
├── minecraftinstance.json   CurseForge instance metadata (very large, grep only)
├── README.md                Bilingual repository documentation
├── CURSEFORGE_PAGE.md       HTML source of the CurseForge project page
├── CHANGELOG.md             Bilingual change history (dated entries)
├── CREDITS.md               Team, contributors and thanks (bilingual)
├── STRUCTURE.md             This file
├── RULES.md                 Project rules & AI/IDE instructions
├── ERROR_LOG.md             Error log with prevention rules
├── LICENSE                  Proprietary source-available license
│
├── mods/                    445 active .jar + in-house arcadia-* mods
├── config/                  ~1,156 files: modpack-shipped configuration
├── defaultconfigs/          Full mirror of config/ (new-world & server defaults)
├── kubejs/                  ~2,012 files: custom scripting ecosystem
├── datapacks/               Empty (all data lives in kubejs/data/)
├── resourcepacks/           ArcadiaLanguages (in-house localization) + hud.zip
├── shaderpacks/             13 curated shaders
│
├── saves/TEST/              Active QA test world
├── ESM/                     Historical snapshot archives (never modify)
├── logs/, debug/            Runtime logs (not tracked in git)
└── local/, downloads/, ...  Launcher/runtime caches (not tracked)
```

## 3. Where To Go For Each Change (Directions)

| You want to... | Go to |
|----------------|-------|
| Add a custom item/block/sound/armor | `kubejs/startup_scripts/registry/` |
| Add or change a recipe | `kubejs/server_scripts/recipes/{custom,create,overhaul}/` |
| Remove a recipe / ban an item | `kubejs/server_scripts/items/banned/recipe_remover.js` (+ 3 other ban layers, see §6) |
| Change mob HP/damage | `kubejs/server_scripts/mobs/mob_stat_overrides.js` |
| Change loot drops | `kubejs/server_scripts/items/loot/loot_table_nerfs.js` |
| Add an item tooltip | `kubejs/client_scripts/arcadia_item_tooltips.js` |
| Translate an item | `kubejs/assets/arcadia/lang/` (7 locales: de, en, es, fr, it, pt, ru) |
| Edit quests | `config/ftbquests/quests/chapters/` (34 chapters) |
| Translate quests | `config/ftbquests/quests/lang/` (7 locales) |
| Change the main menu / branding | `config/fancymenu/` (custom GUIs, panoramas, layouts) |
| Server progression / admin systems | `config/arcadia/` (production config, handle with care) |
| Change a mod's balance config | `config/<mod>.toml` then mirror to `defaultconfigs/` |
| Apotheosis rarities/affixes | `kubejs/data/apotheosis/` |
| Flight potion gating | `kubejs/data/apothic_attributes/brewing_mixes/` |
| Spawner mob blacklist | `kubejs/data/apothic_spawners/tags/entity_type/` |
| Custom music discs | `kubejs/data/arcadia/jukebox_song/` + `kubejs/startup_scripts/registry/sound_registry.js` |

Golden rules: always give recipes an explicit `.id('arcadia:xxx')`, always add lang keys in all 7 locales, always mirror `config/` changes into `defaultconfigs/`, never bump versions without an explicit request. Full conventions in `RULES.md` and `kubejs/KUBEJS_GUIDE.md`.

## 4. config/ - General Configuration

~1,156 files. Key areas:

| Path | Purpose |
|------|---------|
| `config/arcadia/` | In-house server systems: ArcadiaGuard (moderation), admin panel, auction house (ah), lootbox, pets, prestige, spawn/tablist |
| `config/fancymenu/` | Branded "Echoes Of Power" main menu, custom server-selection GUIs, panoramas, loading screens |
| `config/ftbquests/quests/` | 34 quest chapters, 3,000+ quests, 7-language lang files |
| `config/jei/` | Ingredient blacklist and curated sort order |
| `config/ars_nouveau/` | Magic balance tuning (intentionally nerfed) |
| `config/apotheosis/` | RPG loot/affix tuning |
| `config/ftbchunks-*`, `ftbessentials` | Claims and server utility commands |
| `config/voicechat/` | Simple Voice Chat client/server settings |
| `config/spark/` | Profiler output (runtime data, excluded from the defaultconfigs mirror) |

Performance stack: Sodium + Iris + ModernFix + FerriteCore + ImmediatelyFast + Entity Culling + FarSight (chunk cache capped at 32). Render-thread hotspots were tuned via spark profiling (see CHANGELOG 2026-07-20).

`defaultconfigs/` mirrors `config/` in full so every new world and server install starts from the curated defaults. Exclusions: `spark/` (runtime data) and `arcadia/arcadiaadminpanel/logins.json` (credentials, never distributed).

## 5. kubejs/ - Custom Scripting Ecosystem

```
kubejs/
├── KUBEJS_GUIDE.md          Staff guide: READ FIRST before touching any script
├── modified_recipes.txt     Recipe change log
│
├── startup_scripts/         9 scripts (full restart required)
│   ├── registry/            item_registry (70+ custom items), block_registry,
│   │                        sound_registry (20 jukebox songs), armor_tiers,
│   │                        item_stat_tweaks
│   ├── compat/              knightlib_enable_content (KnightLib recipe init)
│   └── ui/                  arcadia_creative_tab, hide_banned_from_creative,
│                            player_welcome_message
│
├── server_scripts/          33 scripts (/reload)
│   ├── recipes/overhaul/    01-10: vanilla tools, cross-mod, Mekanism, TFMG, IE,
│   │                        Create addons, storage/flux, magic, adventure,
│   │                        steel arbitrage lock
│   ├── recipes/create/      Netherite sequenced assembly, precision mechanism fix,
│   │                        create things & misc rebuilds
│   ├── recipes/custom/      Fusion Core chain (5 tiers, 9x9 final), Adept/Heretic
│   │                        armor, misc crafts
│   ├── items/banned/        recipe_remover (152 bans), inventory_scanner,
│   │                        strip_life_mending_gloves
│   ├── items/loot/          loot_table_nerfs (diamond 0.5%, netherite 0.01%)
│   ├── mobs/                mob_stat_overrides (boss HP x2.5-x8), damage nerfs,
│   │                        merchant_trade_filter
│   ├── fixes/compat/        9 cross-mod fixes: claim protections (explosions,
│   │                        soul gems, transmitters), TFMG limestone, blaze burner,
│   │                        cannon boat, creeper lightning, Mowzie paw, pulverizer dupe
│   └── tags/                c: convention item/entity tags
│
├── client_scripts/          arcadia_item_tooltips.js (bilingual tooltips)
├── data/                    ~1,465 JSON: apotheosis rarities/affixes, apothic
│                            brewing gates, spawner blacklist, jukebox songs,
│                            createoreexcavation, enchantable tag trims
├── assets/arcadia/          ~497 files: textures, models, sounds, 7 lang files
└── config/                  KubeJS client/common/web_server settings
```

## 6. Content & Balance Systems

**Custom content**: 4 cross-mod bridge items (Arcane Circuit, Ethereal Alloy, Industrial Heart, Rune Matrix), Fusion Core 5-tier chain ending in a 9x9 Mechanical Crafting recipe, Adept & Heretic armor sets (4 pieces + 10 companion items each), 20 custom music discs, Heart of Arcadia trophy.

**Ban system (4 layers, must stay in sync)**:
1. `recipe_remover.js` - removes crafting recipes (152 items)
2. `inventory_scanner.js` - strips banned items from inventories (Set-based, tick-batched)
3. `hide_banned_from_creative.js` - hides from creative/search tabs
4. `config/jei/blacklist.json` - hides from JEI

**Balance philosophy** (intentional, do not "fix"): loot drought (diamond 0.5%, netherite 0.01%), boss HP x2.5-x8, flight gated behind Dragon's Breath/Nether Star brewing, Winged affix mythic-only, artifacts craft-only, steel cross-mod arbitrage locked, merchant trades filtered.

**Quests**: 34 chapters in `config/ftbquests/quests/chapters/` covering every major mod (Create, Mekanism, TFMG, IE, Ars Nouveau, Iron's Spellbooks, Occultism, Apotheosis, Aether, Twilight Forest, Deeper & Darker, Farmer's Delight...), plus progression guide and bounty chapters.

## 7. In-House & Patched Mods

**In-house (Team Arcadia exclusives)**: `arcadia-lib`, `arcadia-admin-panel`, `arcadia-ah` (auction house), `arcadia-pets` (ELO PvP pet system), `arcadia-prestige`, `arcadia_spawn`, `arcadiaguard` (moderation), `arcadia-patch-create`, `ArcadiaLootbox`, `arcadiatweaks`.

**Patched third-party jars** (fixed by the team, shipped as `*-arcadia-fix.jar`): create-central-kitchen, deeperdarker, ecologics, tfmg, trailandtales_delight. These are NOT in the CurseForge manifest and ship via repository overrides.

## 8. Distribution & Workflow

- Git: single branch `2.0.X` on `github.com/Team-Arcadia/Arcadia-V2-Client`, auto-commit/push policy, English commits, no version bumps without explicit request.
- Players install via CurseForge (manifest resolves 455 entries); in-house content ships in `mods/` overrides + `kubejs/` + `config/`.
- Test world: `saves/TEST`. KubeJS server scripts reload with `/reload`; startup scripts need a full restart.
- Logs to watch: `logs/latest.log`, `logs/kubejs/{startup,server,client}.log`.

---

# Arcadia V2 - Référence Complète du Modpack (Version Française)

Référence maîtresse de l'instance Arcadia V2 « Echoes Of Power ». Tout est indexé ici : répertoires, configuration générale, systèmes de contenu, et où aller pour chaque type de modification.

## 1. Identité

| Champ | Valeur |
|-------|--------|
| Nom | Arcadia V2 : Echoes Of Power |
| Minecraft | 1.21.1 |
| Loader | NeoForge 21.1.232 |
| Java | 21 (8+ Go RAM recommandés) |
| Manifest | 455 entrées CurseForge (442 mods + 13 shaderpacks) |
| Jars locaux | 446 actifs (dont mods maison et jars patchés) |
| Cible | Serveur communautaire, 30-50 joueurs, jouable en solo |
| Langues | Docs EN/FR, items en 7 locales, quêtes en 7 locales |
| Licence | Propriétaire source visible (voir `LICENSE`) |
| Équipe | Voir `CREDITS.md` |

## 2. Arborescence Racine

```
Arcadia V2/
├── manifest.json            Manifest CurseForge, 455 entrées résolues à l'import
├── minecraftinstance.json   Métadonnées d'instance CurseForge (très volumineux)
├── README.md                Documentation bilingue du dépôt
├── CURSEFORGE_PAGE.md       Source HTML de la page CurseForge
├── CHANGELOG.md             Historique des changements bilingue (par date)
├── CREDITS.md               Équipe, contributeurs et remerciements (bilingue)
├── STRUCTURE.md             Ce fichier
├── RULES.md                 Règles projet & instructions AI/IDE
├── ERROR_LOG.md             Journal d'erreurs avec règles de prévention
├── LICENSE                  Licence propriétaire source visible
│
├── mods/                    445 .jar actifs + mods maison arcadia-*
├── config/                  ~1 156 fichiers : configuration livrée par le pack
├── defaultconfigs/          Miroir complet de config/ (défauts nouveaux mondes/serveur)
├── kubejs/                  ~2 012 fichiers : écosystème de scripts custom
├── datapacks/               Vide (toutes les données sont dans kubejs/data/)
├── resourcepacks/           ArcadiaLanguages (localisation maison) + hud.zip
├── shaderpacks/             13 shaders sélectionnés
│
├── saves/TEST/              Monde de test QA actif
├── ESM/                     Archives de snapshots historiques (ne jamais modifier)
├── logs/, debug/            Logs runtime (non suivis par git)
└── local/, downloads/, ...  Caches launcher/runtime (non suivis)
```

## 3. Où Aller Pour Chaque Modification (Directions)

| Vous voulez... | Allez dans |
|----------------|------------|
| Ajouter un item/bloc/son/armure custom | `kubejs/startup_scripts/registry/` |
| Ajouter ou modifier une recette | `kubejs/server_scripts/recipes/{custom,create,overhaul}/` |
| Supprimer une recette / bannir un item | `kubejs/server_scripts/items/banned/recipe_remover.js` (+ 3 autres couches, voir §6) |
| Changer les HP/dégâts d'un mob | `kubejs/server_scripts/mobs/mob_stat_overrides.js` |
| Changer les drops de loot | `kubejs/server_scripts/items/loot/loot_table_nerfs.js` |
| Ajouter un tooltip d'item | `kubejs/client_scripts/arcadia_item_tooltips.js` |
| Traduire un item | `kubejs/assets/arcadia/lang/` (7 locales : de, en, es, fr, it, pt, ru) |
| Éditer les quêtes | `config/ftbquests/quests/chapters/` (34 chapitres) |
| Traduire les quêtes | `config/ftbquests/quests/lang/` (7 locales) |
| Changer le menu principal / branding | `config/fancymenu/` (GUIs custom, panoramas, layouts) |
| Progression serveur / systèmes admin | `config/arcadia/` (config de production, prudence) |
| Modifier la config d'équilibrage d'un mod | `config/<mod>.toml` puis miroir vers `defaultconfigs/` |
| Raretés/affixes Apotheosis | `kubejs/data/apotheosis/` |
| Gating des potions de vol | `kubejs/data/apothic_attributes/brewing_mixes/` |
| Blacklist de mobs des spawners | `kubejs/data/apothic_spawners/tags/entity_type/` |
| Disques de musique customs | `kubejs/data/arcadia/jukebox_song/` + `kubejs/startup_scripts/registry/sound_registry.js` |

Règles d'or : toujours un `.id('arcadia:xxx')` explicite sur les recettes, toujours les clés lang dans les 7 locales, toujours répercuter les changements `config/` dans `defaultconfigs/`, jamais de bump de version sans demande explicite. Conventions complètes dans `RULES.md` et `kubejs/KUBEJS_GUIDE.md`.

## 4. config/ - Configuration Générale

~1 156 fichiers. Zones clés :

| Chemin | Rôle |
|--------|------|
| `config/arcadia/` | Systèmes serveur maison : ArcadiaGuard (modération), panneau admin, hôtel des ventes (ah), lootbox, pets, prestige, spawn/tablist |
| `config/fancymenu/` | Menu principal « Echoes Of Power », GUIs de sélection de serveur, panoramas, écrans de chargement |
| `config/ftbquests/quests/` | 34 chapitres, 3 000+ quêtes, fichiers lang en 7 langues |
| `config/jei/` | Blacklist d'ingrédients et ordre de tri |
| `config/ars_nouveau/` | Équilibrage magie (nerfs intentionnels) |
| `config/apotheosis/` | Réglages loot/affixes RPG |
| `config/ftbchunks-*`, `ftbessentials` | Claims et commandes serveur |
| `config/voicechat/` | Réglages Simple Voice Chat client/serveur |
| `config/spark/` | Sorties du profiler (données runtime, exclues du miroir defaultconfigs) |

Stack performance : Sodium + Iris + ModernFix + FerriteCore + ImmediatelyFast + Entity Culling + FarSight (cache de chunks limité à 32). Les hotspots du thread de rendu ont été réglés via profiling spark (voir CHANGELOG 2026-07-20).

`defaultconfigs/` reflète intégralement `config/` afin que chaque nouveau monde et installation serveur parte des défauts organisés. Exclusions : `spark/` (données runtime) et `arcadia/arcadiaadminpanel/logins.json` (identifiants, jamais distribués).

## 5. kubejs/ - Écosystème de Scripts Custom

```
kubejs/
├── KUBEJS_GUIDE.md          Guide staff : À LIRE AVANT de toucher un script
├── modified_recipes.txt     Journal des modifications de recettes
│
├── startup_scripts/         9 scripts (redémarrage complet requis)
│   ├── registry/            item_registry (70+ items customs), block_registry,
│   │                        sound_registry (20 musiques), armor_tiers,
│   │                        item_stat_tweaks
│   ├── compat/              knightlib_enable_content (init recettes KnightLib)
│   └── ui/                  arcadia_creative_tab, hide_banned_from_creative,
│                            player_welcome_message
│
├── server_scripts/          33 scripts (/reload)
│   ├── recipes/overhaul/    01-10 : outils vanilla, cross-mod, Mekanism, TFMG, IE,
│   │                        addons Create, stockage/flux, magie, aventure,
│   │                        verrou arbitrage acier
│   ├── recipes/create/      Assemblage séquencé netherite, fix precision mechanism,
│   │                        reconstructions create things & misc
│   ├── recipes/custom/      Chaîne Fusion Core (5 tiers, 9x9 final), armures
│   │                        Adept/Heretic, crafts divers
│   ├── items/banned/        recipe_remover (152 bans), inventory_scanner,
│   │                        strip_life_mending_gloves
│   ├── items/loot/          loot_table_nerfs (diamant 0.5%, netherite 0.01%)
│   ├── mobs/                mob_stat_overrides (HP boss x2.5-x8), nerfs de dégâts,
│   │                        merchant_trade_filter
│   ├── fixes/compat/        9 correctifs cross-mod : protections de claims
│   │                        (explosions, soul gems, transmitters), TFMG limestone,
│   │                        blaze burner, bateau-canon, creeper foudre, patte Mowzie,
│   │                        dupe pulverizer
│   └── tags/                Tags d'items/entités convention c:
│
├── client_scripts/          arcadia_item_tooltips.js (tooltips bilingues)
├── data/                    ~1 465 JSON : raretés/affixes Apotheosis, gates de
│                            brassage apothic, blacklist spawners, musiques jukebox,
│                            createoreexcavation, retraits du tag enchantable
├── assets/arcadia/          ~497 fichiers : textures, modèles, sons, 7 fichiers lang
└── config/                  Réglages KubeJS client/common/web_server
```

## 6. Systèmes de Contenu & Équilibrage

**Contenu custom** : 4 items pont cross-mod (Circuit Arcane, Alliage Éthéré, Cœur Industriel, Matrice de Runes), chaîne Fusion Core en 5 tiers finissant en recette 9x9 Mechanical Crafting, sets d'armures Adept & Heretic (4 pièces + 10 items compagnons chacun), 20 disques de musique customs, trophée Heart of Arcadia.

**Système de ban (4 couches, à garder synchronisées)** :
1. `recipe_remover.js` - supprime les recettes (152 items)
2. `inventory_scanner.js` - retire les items bannis des inventaires (Set, batché par tick)
3. `hide_banned_from_creative.js` - masque du créatif/recherche
4. `config/jei/blacklist.json` - masque de JEI

**Philosophie d'équilibrage** (intentionnelle, ne pas « corriger ») : disette de loot (diamant 0.5%, netherite 0.01%), HP des boss x2.5-x8, vol gaté derrière Dragon's Breath/Étoile du Nether, affixe Winged mythique uniquement, artifacts craft uniquement, arbitrage d'acier cross-mod verrouillé, trades des marchands filtrés.

**Quêtes** : 34 chapitres dans `config/ftbquests/quests/chapters/` couvrant chaque mod majeur (Create, Mekanism, TFMG, IE, Ars Nouveau, Iron's Spellbooks, Occultism, Apotheosis, Aether, Twilight Forest, Deeper & Darker, Farmer's Delight...), plus les chapitres guide de progression et bounties.

## 7. Mods Maison & Jars Patchés

**Maison (exclusivités Team Arcadia)** : `arcadia-lib`, `arcadia-admin-panel`, `arcadia-ah` (hôtel des ventes), `arcadia-pets` (système de pets PvP ELO), `arcadia-prestige`, `arcadia_spawn`, `arcadiaguard` (modération), `arcadia-patch-create`, `ArcadiaLootbox`, `arcadiatweaks`.

**Jars tiers patchés** (corrigés par l'équipe, livrés en `*-arcadia-fix.jar`) : create-central-kitchen, deeperdarker, ecologics, tfmg, trailandtales_delight. Ils ne sont PAS dans le manifest CurseForge et sont livrés via les overrides du dépôt.

## 8. Distribution & Workflow

- Git : branche unique `2.0.X` sur `github.com/Team-Arcadia/Arcadia-V2-Client`, politique d'auto-commit/push, commits en anglais, pas de bump de version sans demande explicite.
- Les joueurs installent via CurseForge (le manifest résout 455 entrées) ; le contenu maison est livré via les overrides `mods/` + `kubejs/` + `config/`.
- Monde de test : `saves/TEST`. Scripts serveur KubeJS rechargés avec `/reload` ; scripts startup : redémarrage complet.
- Logs à surveiller : `logs/latest.log`, `logs/kubejs/{startup,server,client}.log`.
