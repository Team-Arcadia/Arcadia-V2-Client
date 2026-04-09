# Arcadia V2 — KubeJS Structure Guide

## Directory Tree

```
kubejs/
├── assets/arcadia/
│   ├── lang/
│   │   ├── en_us.json                              # English names & tooltips
│   │   └── fr_fr.json                              # French names & tooltips
│   └── textures/item/                              # Custom 16x16 item textures (PNG)
│
├── client_scripts/
│   └── arcadia_item_tooltips.js                    # All tooltip definitions (uses lang keys for FR/EN)
│
├── data/
│   ├── arcadia/                                    # Custom datapack entries
│   └── parcool/advancement/
│       └── grant_parcool_guide.json                # Disables Parcool guide book spam
│
├── server_scripts/
│   ├── tags/
│   │   └── item_entity_tags.js                     # Item tags (c: convention) + entity tags (spawner blacklist)
│   │
│   ├── recipes/
│   │   ├── recipe_overhaul.js                      # Main recipe hardening (1276 lines, vanilla + mods)
│   │   ├── create/
│   │   │   ├── netherite_sequenced_assembly.js     # Netherite block decrafting via sequenced assembly
│   │   │   └── basin_casting_fix.js                # Create basin/casting recipe compatibility fix
│   │   ├── custom/
│   │   │   ├── arcadia_custom_crafts.js            # Arcadia-specific recipes (keys, tokens)
│   │   │   └── fusion_core_chain.js                # Fusion Core mega-chain (5 tiers, 9x9 final)
│   │   └── mods/
│   │       ├── botanypots_modded_trees.js          # BOP + Twilight Forest + Ars Nouveau tree compat
│   │       └── tfmg_recipe_tweaks.js               # TFMG mod recipe adjustments
│   │
│   ├── items/
│   │   ├── banned/
│   │   │   ├── inventory_scanner.js                # Strips banned items from player inventories (instant + scan)
│   │   │   └── recipe_remover.js                   # Removes crafting recipes for banned items
│   │   └── loot/
│   │       └── loot_table_nerfs.js                 # Loot table drop rate modifications
│   │
│   ├── protection/
│   │   ├── spawn/
│   │   │   ├── spawn_core_protection.js            # Core arcadia:spawn dimension protection
│   │   │   ├── spawn_ability_blocker.js            # Blocks Simply Swords, Ars Nouveau, Iron's Spells at spawn
│   │   │   └── spawn_block_break_blocker.js        # Prevents ALL block breaking by survival in spawn
│   │   └── npc/
│   │       └── npc_interaction_guard.js            # NPC lead/rod blocking + harmful effect stripping
│   │
│   ├── mobs/
│   │   ├── mob_damage_nerfs.js                     # Mob damage output nerfs
│   │   ├── mob_stat_overrides.js                   # Custom mob HP/armor/speed overrides
│   │   └── merchant_trade_filter.js                # Filters banned items from merchant trades
│   │
│   └── fixes/
│       ├── compat/
│       │   ├── cannon_boat_crash_fix.js            # Supplementaries cannon boat server crash fix
│       │   └── blaze_burner_patch.js               # Create blaze burner recipe compatibility
│       └── exploits/
│           └── anti_book_dupe.js                   # Prevents enchanted book duplication
│
├── startup_scripts/
│   ├── registry/
│   │   ├── item_registry.js                        # All custom items (keys, discs, fusion chain, heart, armor)
│   │   ├── adept_armor_tier.js                     # Adept armor material tier definition
│   │   ├── block_registry.js                       # Custom blocks (ATM)
│   │   ├── sound_registry.js                       # Custom sound events
│   │   └── item_stat_tweaks.js                     # Durability/attack speed modifications
│   └── ui/
│       ├── arcadia_creative_tab.js                 # Arcadia creative tab contents
│       ├── hide_banned_from_creative.js            # Hides banned items from all creative tabs
│       └── player_welcome_message.js               # Welcome message on player join
│
├── config/
│   └── common.json                                 # KubeJS global config
│
└── KUBEJS_GUIDE.md                                 # This file
```

## Script Types

| Type | Location | Runs when | Reloadable | Use case |
|------|----------|-----------|------------|----------|
| **Startup** | `startup_scripts/` | Game launch | No (restart) | Item/block registration, creative tabs, armor tiers |
| **Server** | `server_scripts/` | Server start + `/reload` | Yes | Recipes, tags, events |
| **Client** | `client_scripts/` | Client join | Yes | Tooltips, JEI, visuals |

## Folder Organization

### `server_scripts/`
| Folder | Purpose |
|--------|---------|
| `tags/` | Item and entity tag definitions |
| `recipes/` | All recipe changes — `create/` for Create-specific, `custom/` for Arcadia originals, `mods/` for other mod compat |
| `items/banned/` | Banning system (recipe removal + inventory scanning) |
| `items/loot/` | Loot table modifications |
| `protection/spawn/` | Spawn dimension protections (abilities, block breaking) |
| `protection/npc/` | NPC-specific protections (interaction, effects) |
| `mobs/` | Mob stat changes and merchant filtering |
| `fixes/compat/` | Mod compatibility patches |
| `fixes/exploits/` | Anti-exploit scripts |

### `startup_scripts/`
| Folder | Purpose |
|--------|---------|
| `registry/` | Item, block, sound, armor tier registration + stat modifications |
| `ui/` | Creative tabs, banned item hiding, welcome messages |

## Custom Content Registry

### Custom Items (`registry/item_registry.js`)
| Item | Namespace ID | Rarity | Description |
|------|-------------|--------|-------------|
| Basic Key | `arcadia:basic_key` | Common | Loot box key |
| Common Key | `arcadia:common_key` | Common | Loot box key |
| Rare Key | `arcadia:rare_key` | Common | Loot box key |
| Legendary Key | `arcadia:legendary_key` | Common | Loot box key |
| Arcadia Key | `arcadia:arcadia_key` | Epic | Glowing loot box key |
| Vote Key | `arcadia:vote_key` | Common | Vote reward key |
| Casino Token | `arcadia:token_casino` | Common | Casino currency |
| Music Discs | `arcadia:music_disc_*` (x20) | Rare | Custom jukebox tracks |
| Heart of Arcadia | `arcadia:heart_of_arcadia` | Epic | Uncraftable future component |

### Fusion Core Chain (`registry/item_registry.js` + `recipes/custom/fusion_core_chain.js`)
5-tier crafting chain requiring Create, Mekanism, TFMG, and Immersive Engineering.
Total cost: ~100K iron, ~50K diamonds, ~20K gold, ~10K netherite. Final assembly is a 9x9 mechanical crafter.

| Tier | Items | Recipe Type |
|------|-------|-------------|
| **Tier 0** | Alloy Blend, Diamond Matrix, Infused Steel, Nether Concentrate, Energized Dust, Wiring Bundle | Create Mixing (heated) + Mechanical Crafting |
| **Tier 1** | Refined Alloy Ingot, Hardened Steel Compound, Energized Crystal, Treated Composite Plate | Create Mixing + Mechanical Crafting 5x5 |
| **Tier 2** | Quantum Circuit, Plasma Cell, Reinforced Casing, Thermal Conductor | Mechanical Crafting 5x5 + Sequenced Assembly (8 loops) |
| **Tier 3** | Fusion Matrix, Containment Field Generator, Neutron Reflector | Mechanical Crafting 7x7 + Sequenced Assembly (10 loops) |
| **Final** | **Fusion Core** | Mechanical Crafting 9x9 |

### Adept Armor Set (`registry/item_registry.js` + `registry/adept_armor_tier.js`)
Dark cultist/sect roleplay armor set. Medium tier (between iron and diamond).

| Piece | EN Name | FR Name | Namespace ID |
|-------|---------|---------|-------------|
| Helmet | Adept's Hood | Capuche de l'Adepte | `arcadia:adept_helmet` |
| Chestplate | Adept's Robe | Robe de l'Adepte | `arcadia:adept_chestplate` |
| Leggings | Adept's Vestments | Vetements de l'Adepte | `arcadia:adept_leggings` |
| Boots | Adept's Wrappings | Bandelettes de l'Adepte | `arcadia:adept_boots` |

**Armor Stats:**
| Stat | Value | Comparison |
|------|-------|-----------|
| Protection | 2/5/6/2 (15 total) | Same as iron |
| Durability multiplier | 20 | Iron=15, Diamond=33 |
| Toughness | 1.0 | Iron=0, Diamond=2 |
| Knockback resistance | 0.05 | Slight |
| Enchantability | 15 | High (mystical) |
| Repair ingredient | Amethyst Shard | — |
| Equip sound | Leather | Robe/cloth feel |

### Custom Blocks (`registry/block_registry.js`)
| Block | Namespace ID | Description |
|-------|-------------|-------------|
| ATM | `arcadia:atm` | Automated Teller Machine |

## Key Systems

### Item Banning (`items/banned/` + `ui/hide_banned_from_creative.js`)
Three-layer system: recipes removed, items stripped from inventory on pickup + periodic scan, hidden from JEI and creative tabs.

### Spawn Protection (`protection/`)
Multi-layer protection for `arcadia:spawn` dimension: block breaking disabled, Simply Swords abilities blocked, movement spells blocked, NPC interaction restricted, harmful effects stripped from NPCs.

### Localization (`assets/arcadia/lang/`)
All custom items have English (en_us) and French (fr_fr) names and tooltips. Tooltips use `Text.translate()` keys for automatic language switching.

### Custom Textures (`assets/arcadia/textures/item/`)
All Fusion Core chain items, Heart of Arcadia, and Adept Armor pieces have custom 16x16 pixel art textures generated with unique color palettes per tier.

## Naming Conventions

- **Files**: `snake_case.js` — name describes the function, not the mod
- **Namespace**: All custom content uses `arcadia:` prefix
- **Recipe IDs**: `arcadia:recipe_name`
- **Priority**: `// Priority: N` header (higher = loads first)
- **No accents** in filenames — ASCII only
- **Translations**: Always add both `en_us.json` and `fr_fr.json` entries for new items
- **Tooltips**: Use `Text.translate()` with lang keys, never hardcoded strings
