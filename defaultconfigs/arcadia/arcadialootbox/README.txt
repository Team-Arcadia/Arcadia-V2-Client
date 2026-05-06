================================================================
          ARCADIA LOOTBOX v1.2.0 - CONFIG GUIDE
================================================================

TWO LOOTBOX TYPES:
===================
1. "weighted" (default): Each item rolls independently.
   Every item has its own chance %. Multiple items can drop.

2. "guaranteed": ONE item is picked from the pool (weighted),
   PLUS a guaranteed item always drops. Set fields:
   - "type": "guaranteed"
   - "guaranteedItem": "minecraft:bread"
   - "guaranteedMinCount": 1
   - "guaranteedMaxCount": 3
   In the lootTable, "chance" acts as WEIGHT (higher = more likely).

KEY ITEMS:
==========
The mod registers 50 key items. Use their IDs in "keyItem":
- arcadialootbox:dungeon_key_<tier>
- arcadialootbox:shop_key_<tier>
- arcadialootbox:vote_key_<tier>
- arcadialootbox:lootable_key_<tier>
- arcadialootbox:event_key_<tier>
- arcadialootbox:boss_key_<tier>

Standard tiers: common, uncommon, rare, superior, epic,
               legendary, mythic, divine, celestial, transcendent
Event tiers: bronze, silver, gold, platinum, diamond
Boss tiers: minor, major, elite, supreme, overlord

COMMANDS:
=========
/arcadia_lootbox give <player> <id> [amount]
/arcadia_lootbox giveall <id> [amount]
/arcadia_lootbox givekey <player> <key_id> [amount]
/arcadia_lootbox reload
/arcadia_lootbox list
/arcadia_lootbox listkeys
/arcadia_lootbox info <id>
/arcadia_lootbox preview <player> <id>
/arcadia_lootbox history <player>
/arcadia_lootbox clearhistory <player>
/arcadia_lootbox create <id> <displayName>
/arcadia_lootbox delete <id>
/arcadia_lootbox setuses <pos> <uses>
/arcadia_lootbox resetcooldown <player>
/arcadia_lootbox stats
/arcadia_lootbox hub
