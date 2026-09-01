# Arcadia V2 — KubeJS Structure Guide

## Directory Tree

```
kubejs/
├── assets/arcadia/
│   ├── lang/
│   │   ├── en_us.json                              # English names & tooltips (keys, fusion chain, bridges, armor, discs)
│   │   ├── fr_fr.json                              # French translations
│   │   └── de_de/es_es/it_it/pt_br/ru_ru.json      # Other locales
│   ├── sounds.json                                 # 20 music disc SoundEvents
│   ├── sounds/                                     # Custom audio files
│   └── textures/
│       ├── item/                                   # Custom item textures
│       │   ├── music_disc_*.png       (20 x 64x64) # Vinyl discs with 3D shading + colored labels
│       │   ├── arcane_circuit.png     (32x32)      # Bridge: Create+TFMG+Mek+Ars
│       │   ├── ethereal_alloy.png     (32x32)      # Bridge: Ars+Mek+Occult+Create
│       │   ├── industrial_heart.png   (32x32)      # Bridge: Create+TFMG+Mek+IE
│       │   ├── rune_matrix.png        (32x32)      # Bridge: Ars+Occult+Create+Apotheosis
│       │   ├── fusion_*.png           (64x64)      # Fusion chain T0->Apex
│       │   ├── adept_*.png            (64x64)      # Purple cultist (armor + 10 unique)
│       │   ├── heretic_*.png          (64x64)      # Red rebel (armor + 10 unique)
│       │   ├── *_key.png              (64x64)      # 6 keys color-coded + casino token
│       │   ├── heart_of_arcadia.png   (64x64)
│       │   ├── _gen_all.py                         # Python generator for all 64x64 textures
│       │   └── _gen_discs.py                       # Python generator for 20 music discs
│       └── block/music_discs/                      # Same disc textures (for Amendments jukebox renderer)
│
├── client_scripts/
│   └── arcadia_item_tooltips.js                    # Per-key multi-line tooltips (keys + fusion chain + bridges)
│
├── data/
│   ├── apotheosis/
│   │   ├── rarities/{common,uncommon,rare,epic,mythic}.json    # Nerfed weight tables per world tier
│   │   ├── affixes/armor/attribute/winged.json     # Creative flight affix nerf (weight 3, mythic-only)
│   │   └── recipe/potion_charm.json                # Endgame charm: HDPE Sheet + Rune Matrix
│   ├── apothic_attributes/brewing_mixes/
│   │   ├── flying_from_levitation.json             # Gate: requires Dragon's Breath
│   │   ├── long_flying_from_flying.json            # Gate: Redstone Block
│   │   └── extra_long_flying_from_long_flying.json # Gate: Nether Star (Wither boss)
│   ├── apothic_spawners/tags/entity_type/
│   │   └── blacklisted_from_spawners.json          # 37 mobs banned (Animal Garden, turtles, bosses)
│   ├── arcadia/jukebox_song/                       # 20 jukebox song definitions
│   ├── createoreexcavation/recipe/                 # Custom Create Ore Excavation entries
│   ├── minecraft/tags/item/enchantable/
│   │   └── durability.json                         # 53 custom items removed from vanilla enchantable tag
│   └── parcool/advancement/
│       └── grant_parcool_guide.json                # Disables Parcool guide spam
│
├── server_scripts/
│   ├── tags/
│   │   └── item_entity_tags.js                     # c: convention item tags (consolidated)
│   │
│   ├── recipes/
│   │   ├── overhaul/                               # Recipe hardening — split by theme (was monolithic recipe_overhaul.js)
│   │   │   ├── 01_vanilla_tools_storage.js         # Vanilla 0-6: tools, armor, storage, workstations, decoration, redstone, combat
│   │   │   ├── 02_crossmod_general.js              # Cross-mod 7/10/11/12: storage, magic, tech, light touches, bridges
│   │   │   ├── 03_mekanism.js                      # Mekanism T1-T3 machine cross-Create gating
│   │   │   ├── 04_tfmg.js                          # TFMG industrial components
│   │   │   ├── 05_immersive_engineering.js         # IE multiblocks gated behind Create
│   │   │   ├── 06_create_addons.js                 # Addition, Nuclear, Diesel hardening
│   │   │   ├── 07_storage_peripherals_flux.js      # AdvancedPeripherals, RefinedStorage, FluxNetworks
│   │   │   ├── 08_magic_mods.js                    # Ars Nouveau/Creo/Technica, Iron's Spellbooks, Occultism
│   │   │   ├── 09_adventure_mods.js                # Apotheosis, Aether, Aquaculture
│   │   │   └── 10_steel_arbitrage.js               # Locks cross-mod steel laundering (TFMG/CN tag-keyed conversions)
│   │   ├── create/
│   │   │   ├── netherite_sequenced_assembly.js     # Netherite block decrafting via sequenced assembly
│   │   │   ├── precision_mechanism_fix.js          # Fix Create 6.0.10 bug #10203 (tag Either-codec)
│   │   │   ├── chromatic_chain.js                  # Reopens the chromatic chain (compound + shadow/radiant casings)
│   │   │   └── create_things_and_misc_fix.js       # Auto-rebuilds 39 recipes broken in 1.21 (legacy format)
│   │   ├── custom/
│   │   │   ├── misc_custom_crafts.js               # ATM recipe + iron_sheet hand-craft fallback (early-game unblock)
│   │   │   ├── armor_crafts.js                     # Adept/Heretic armor recipes
│   │   │   └── fusion_core_chain.js                # Fusion Core mega-chain (5 tiers, 9x9 final)
│   │
│   ├── items/
│   │   ├── banned/
│   │   │   ├── recipe_remover.js                   # 152 banned items — recipe removal
│   │   │   ├── inventory_scanner.js                # Strips banned items from inventories (given/picked)
│   │   │   └── strip_life_mending_gloves.js        # Strips Life Mending enchant on iron_gloves drops
│   │   └── loot/
│   │       └── loot_table_nerfs.js                 # Diamond/Netherite/Artifacts drop nerfs
│   │
│   ├── mobs/
│   │   ├── mob_stat_overrides.js                   # Vanilla+modded mob HP/damage/armor (bosses ×2.5-×8)
│   │   ├── mob_damage_nerfs.js                     # 5% equipment drop rate
│   │   └── merchant_trade_filter.js                # Filters banned items from merchant trades
│   │
│   └── fixes/
│       └── compat/
│           ├── blaze_burner_patch.js                       # Create blaze burner compat
│           ├── cannon_boat_crash_fix.js                    # Supplementaries cannon_boat crash fix
│           ├── claim_explosion_protection.js               # Hardens FTB claims vs custom mod explosions (Mutant Creeper etc.)
│           ├── creeper_lightning_charge_fix.js             # Lightning damage always charges creepers (vanilla + ISS spells)
│           ├── mowziesmobs_elokosa_paw_crashfix.js         # Mowzie's Mobs Elokosa paw crash fix
│           ├── occultengineering_pulverizer_dupe_fix.js    # Replaces broken upgrade_tier recipe (6 shapeless tier crafts)
│           ├── soul_gem_claim_protection.js                # Occultism Soul Gem: blocks mob capture inside foreign FTB claims
│           ├── tfmg_limestone_crushing_fix.js              # Drops TFMG-only limestone crushing recipe so CUF compat one wins
│           └── transmitter_claim_protection.js             # Create Ender Transmission: blocks config screen in foreign claims
│
├── startup_scripts/
│   ├── compat/
│   │   └── knightlib_enable_content.js             # Calls KnightLib.initialize(Usage.ALL) so grail/chalice recipes load
│   └── registry/
│       ├── item_registry.js                        # ALL custom items (keys, discs, fusion, bridges, armor, heart)
│       ├── block_registry.js                       # Custom blocks (ATM)
│       ├── sound_registry.js                       # 20 jukebox sound events
│       ├── armor_tiers.js                          # Adept + Heretic armor material tiers
│       └── item_stat_tweaks.js                     # Durability / attack speed modifications
│
├── startup_scripts/ui/
│   ├── arcadia_creative_tab.js                     # Arcadia creative tab contents
│   ├── hide_banned_from_creative.js                # Hides banned items from creative
│   └── player_welcome_message.js                   # Welcome message on join
│
├── modified_recipes.txt                            # Full staff reference (all recipe changes documented)
└── KUBEJS_GUIDE.md                                 # This file
```

## Script Types & Reload Behavior

| Type | Location | Runs when | Reloadable | Use case |
|------|----------|-----------|------------|----------|
| **Startup** | `startup_scripts/` | Game launch | **NO** (server restart) | Item/block registration, armor tiers, creative tabs |
| **Server** | `server_scripts/` | Server start + `/reload` | **YES** | Recipes, tags, events, loot, mob stats |
| **Client** | `client_scripts/` | Client join + F3+T | **YES** (client) | Tooltips, JEI, visuals |

## Datapack Overrides (`data/`)

Files in `kubejs/data/<namespace>/...` override vanilla/mod JSON files at the same path. Used for:

- **Apotheosis rarity tuning** — rebalanced weights per world tier (haven→pinnacle)
- **Apotheosis Winged affix** — weight 25→3, mythic-only
- **Apotheosis Potion Charm** — replaced with HDPE Sheet + Rune Matrix endgame recipe
- **Apothic Attributes flight** — Dragon's Breath + Nether Star gates
- **Apothic Spawners mob blacklist** — 37 entities via `entity_type` tag
- **Vanilla enchantable tag** — removes 53 custom Arcadia items from `minecraft:enchantable/durability` (NeoForge `remove` field)

## Custom Content Registry

### Keys & Currency (`registry/item_registry.js`)
7 web-ticket items + casino token. Each has multi-line tooltip (flavor + "Redeem on Arcadia website" + reward type) in EN + FR.

| Item | ID | Rarity | Color |
|------|-----|--------|-------|
| Basic Key | `arcadia:basic_key` | Common | Gray |
| Common Key | `arcadia:common_key` | Common | Green |
| Rare Key | `arcadia:rare_key` | Common | Blue |
| Legendary Key | `arcadia:legendary_key` | Common | Light Purple |
| Arcadia Key | `arcadia:arcadia_key` | **Epic** (glow) | Gold |
| Vote Key | `arcadia:vote_key` | Common | Aqua |
| Casino Token | `arcadia:token_casino` | Common | Gold |

### Music Discs (20) — `registry/item_registry.js` + `registry/sound_registry.js` + `data/arcadia/jukebox_song/`
Custom jukebox tracks. Each disc has:
- Own 64x64 vinyl texture (colored label per theme)
- Same texture duplicated in `textures/block/music_discs/` for Amendments jukebox renderer
- Registered jukebox song + sound event

### Cross-Mod Bridges (`registry/item_registry.js` + `recipes/overhaul/02_crossmod_general.js`)
4 custom items that bind multiple mods together. Progressive difficulty gate.

| Item | Tier | Mods | Recipe |
|------|------|------|--------|
| `arcadia:arcane_circuit` | MEDIUM | Create + TFMG + Mek + Ars | Create Mixing (heated) |
| `arcadia:ethereal_alloy` | HARD | Ars + Mek + Occult + Create | Create Mixing (heated) |
| `arcadia:industrial_heart` | HARD | Create + TFMG + Mek + IE | Sequenced Assembly 4 loops |
| `arcadia:rune_matrix` | ENDGAME | Ars + Occult + Create + Apotheosis | Mechanical Crafting 5x5 |

### Fusion Core Chain (`recipes/custom/fusion_core_chain.js`)
5-tier endgame chain. Total: ~100K Iron, ~50K Diamonds, ~20K Gold, ~10K Netherite. Final = 9x9 Mechanical Crafter.

| Tier | Items | Recipe Type |
|------|-------|-------------|
| **T0** | alloy_blend, diamond_matrix, infused_steel, nether_concentrate, energized_dust, wiring_bundle | Create Mixing (heated) |
| **T1** | refined_alloy_ingot, hardened_steel_compound, energized_crystal, treated_composite_plate | Mixing + MC 5x5 |
| **T2** | quantum_circuit, plasma_cell, reinforced_casing, thermal_conductor | MC 5x5 + Sequenced Assembly 8 loops |
| **T3** | fusion_matrix, containment_field_generator, neutron_reflector | MC 7x7 + Sequenced Assembly 10 loops |
| **Apex** | **fusion_core** | Mechanical Crafting 9x9 |

### Adept Armor (`registry/armor_tiers.js` + `recipes/custom/armor_crafts.js`)
Purple cultist armor. 4 pieces + 10 unique items (grimoire, pendant, candle, incense, staff, seal, chalice, orb, scroll, relic).

### Heretic Armor (`registry/armor_tiers.js` + `recipes/custom/armor_crafts.js`)
Red/bone rebel armor. 4 pieces + 10 unique items (tome, blood_vial, dagger, chain, skull_totem, icon, crystal, bone_charm, poison_flask, mark).

**Armor stats (both sets):**
| Stat | Value |
|------|-------|
| Protection | 2/5/6/2 (15 total = iron-equivalent) |
| Durability multiplier | 20 (between iron 15 and diamond 33) |
| Toughness | 1.0 |
| Knockback resistance | 0.05 |
| Enchantability | 15 (high — mystical) |
| Repair ingredient | Amethyst Shard |

### Heart of Arcadia (`registry/item_registry.js`)
**Uncraftable** legendary item. Reserved for future content. Earned, not crafted.

## Key Systems

### Item Banning (4-layer)
1. **`recipe_remover.js`** — removes the craft recipe at server load (152 items banned)
2. **`inventory_scanner.js`** — strips banned items from inventories on pickup + periodic scan
3. **`config/jei/blacklist.json`** — hides from JEI completely
4. **`ui/hide_banned_from_creative.js`** — hides from all creative tabs

### Enchantment Stripping
- **`strip_life_mending_gloves.js`** — strips the Life Mending enchant from any Aether iron_gloves drop (prevents an exploit combo with the modded gloves slot).

### Apotheosis Tuning (datapack)
- **Rarity weights** rebalanced per world tier → less epic/mythic spam
- **Winged affix** (creative flight) → mythic-only, weight 3 (was 25)
- **Potion Charm** → Endgame recipe with HDPE Sheet + Rune Matrix
- **`Restrict Charms to Curios`** → `true` (must equip in Curios slot)
- **Upgrade/Reroll costs** doubled+ in `apotheosis.cfg`

### Flight Potion Gate (`data/apothic_attributes/brewing_mixes/`)
Creative flight now requires Ender Dragon kill (Dragon's Breath) + Wither kill (Nether Star) for extra long.

### Mob Stats (`mobs/mob_stat_overrides.js`)
- Global caps: HP 10k / Damage 50 / Armor 50
- Boss overrides: Wither 500 HP, Ender Dragon 2000 HP, Warden 1000 HP
- Twilight Forest bosses ×2.5
- Mowzie's bosses ×4.0
- Castle Keeper (Twilight final boss) ×8.0
- Iron's Spellbooks bosses ×1.9

### Loot Nerfs (`items/loot/loot_table_nerfs.js`)
- Diamond drops: 0.5%
- Netherite: 0.01% (except smithing template → normal)
- Artifacts: 0% (craft only)
- Sophisticated Backpacks: 15%
- Twilight Forest: 20%

### Localization
- All custom items have EN + FR names
- Per-item multi-line tooltips (3 colored lines)
- FTB Quests: 6 languages, fallback to `en_us` (not French — UK/US fix)
- Starterkit: 10 kits bilingues (5 FR + 5 EN)

## Recipe Fixes (bugfixes for mods)

Several broken recipes from mod authors fixed via KubeJS:

| Fix | File | Reason |
|-----|------|--------|
| **Create Precision Mechanism** | `recipes/create/precision_mechanism_fix.js` | Create 6.0.10 bug #10203 (tag Either-codec) |
| **create_things_and_misc** (39 recipes) | `recipes/create/create_things_and_misc_fix.js` | Legacy 1.20 format (`result.item` → `result.id`) + numeric pattern keys + `forge:` tags |
| **Netherite decrafting** | `recipes/create/netherite_sequenced_assembly.js` | Allows turning Netherite Block back into 9 ingots (4 loops) |
| **Chromatic chain** | `recipes/create/chromatic_chain.js` | Create 6.0.10 registers Chromatic Compound / Shadow / Radiant casings but ships no recipe for them, leaving 44 Create Encased blocks unobtainable (ticket #269) |
| **Occult Engineering Pulverizer dupe** | `fixes/compat/occultengineering_pulverizer_dupe_fix.js` | Removes broken `upgrade_tier` recipe (shift-craft duped output), replaces with 6 explicit shapeless tier transitions |
| **Creeper lightning charge** | `fixes/compat/creeper_lightning_charge_fix.js` | Safety net: any lightning-typed damage (`msgId` contains "lightning") forces `powered=true` on surviving creepers — covers vanilla bolts + ISS lightning spells |
| **Iron sheet hand-craft fallback** | `recipes/custom/misc_custom_crafts.js` | Adds 3 iron_ingot → 1 iron_sheet vanilla craft so solo players are not gated by the Mechanical Press for their first iron tools |

## Recipe Overhaul Split (`recipes/overhaul/`)

The original `recipe_overhaul.js` (2793 lines) was split into 9 themed files for maintainability. All run at `// Priority: 100` and each declares its own shared constants inside its own `ServerEvents.recipes` callback, so files are fully self-contained — order between them does not matter for correctness, only the numeric prefix preserves the original section reading order.

| File | Original sections | Scope |
|------|-------------------|-------|
| `01_vanilla_tools_storage.js` | 0–6 | Wood/sticks, tools/armor, storage, workstations, decoration, redstone, combat |
| `02_crossmod_general.js` | 7, 10, 11, 12 | General mod compat + cross-mod hardening + bridge components |
| `03_mekanism.js` | 13 | Mekanism T1/T2/T3 machines gated behind Create |
| `04_tfmg.js` | 14 | TFMG industrial components |
| `05_immersive_engineering.js` | 15 | IE multiblocks |
| `06_create_addons.js` | 16, 17, 18 | Create Addition, Nuclear, Diesel |
| `07_storage_peripherals_flux.js` | 19, 20, 21 | AdvancedPeripherals, RefinedStorage, FluxNetworks |
| `08_magic_mods.js` | 22, 23, 24, 25 | Ars Nouveau, Ars Creo/Technica, Iron's Spellbooks, Occultism |
| `09_adventure_mods.js` | 26, 27, 28 | Apotheosis, Aether, Aquaculture |

**Adding a new recipe override:** pick the file whose theme matches (or create a new one in the same folder); the priority and constant set are already in place.

## Naming Conventions

- **Files**: `snake_case.js` — name describes the function, not the mod
- **Namespace**: All custom content uses `arcadia:` prefix
- **Recipe IDs**: `arcadia:recipe_name` — every custom recipe has explicit `.id()`
- **Priority**: `// Priority: N` header at top (higher = loads first)
- **No accents** in filenames — ASCII only
- **Translations**: ALWAYS add both `en_us.json` and `fr_fr.json` entries for new items
- **Tooltips**: Use `Text.translate()` with lang keys, never hardcoded strings

## Reload Cheatsheet

| Modification | Command |
|--------------|---------|
| `server_scripts/*` changed | `/reload` |
| `data/*` changed (tags, rarity, recipes) | `/reload` |
| `client_scripts/*` or `assets/*` changed | F3+T on client |
| `startup_scripts/*` changed | **Full server restart required** |
| `config/*.cfg` or `.toml` changed | **Full server restart required** |

## Troubleshooting

- **Item has no recipe in JEI** → check `recipe_remover.js` banned list + `config/jei/blacklist.json` + run `/recipe give` to test server-side
- **Script throws "does not exist"** → item/mod missing — wrap in try/catch or check mod IDs
- **Create sequenced_assembly not loading** → check for tag-based `ingredient` bug in Create 6.0.10 (see `precision_mechanism_fix.js`)
- **Recipe format `item: {id: ...}` fails** → legacy 1.20 format, rebuild via KubeJS using `id: ...`
- **Client sees wrong language** → check FTB Quests `data.snbt` `fallback_locale` is `"en_us"`

See [`modified_recipes.txt`](modified_recipes.txt) for the complete staff-facing reference of every recipe change + banned item + mob blacklist.
