# Arcadia V2 - Quest Book Economy

Reference figures for how much Numismatics currency the FTB Quests book can pay out in total.
Regenerate after any change to quest rewards. These numbers are the source of truth for balancing
the auction house, shop prices and any future money sink.

Measured on 2026-09-20, across 41 chapters and 3,841 quests.

## 1. Headline

| Scope | Before rebalance | After | Change |
|---|---:|---:|---:|
| Kill quests | 3,408,008 | 186,484 | -95% |
| Other quests | 59,184 | 59,184 | 0% |
| **Whole book** | **3,467,192** | **245,668** | **-93%** |

All values in **spurs**. 245,668 spurs = 480 crowns = 60.0 suns.

Coin values: spur 1, bevel 8, sprocket 16, cog 64, crown 512, sun 4096.

This is the ceiling a single player can mint by completing every quest once. It is new money
created from nothing, so it sets the inflation ceiling of the player-to-player economy.

## 2. Difficulty tiers used for kill quests

| Tier | Rate (spurs/kill) | Quests | Kills | Before | After |
|---|---:|---:|---:|---:|---:|
| T0 passive / critter | 0.01 | 691 | 317,050 | 909,520 | 3,085 |
| T1 common hostile | 0.08 | 196 | 105,985 | 310,912 | 8,402 |
| T2 dangerous | 0.15 | 1,110 | 523,318 | 1,535,104 | 76,078 |
| T3 elite / mini-boss | 0.35 | 253 | 103,920 | 300,256 | 35,728 |
| T4 boss | 3.0 | 67 | 21,593 | 352,216 | 63,191 |
| **Total** | | **2,317** | **1,071,866** | **3,408,008** | **186,484** |

Payout per quest = round(kill_count x tier_rate), rendered as the largest single coin that fits,
with a floor of one spur so a quest never pays nothing.

## 3. Money by chapter

| Chapter | Before | After |
|---|---:|---:|
| `the_nether_call` | 358,048 | 53,823 |
| `hunting_hostility` | 502,784 | 42,267 |
| `twilight_forest` | 522,912 | 35,229 |
| `occultism` | 396,544 | 26,656 |
| `arcadia` | 26,416 | 26,416 |
| `deep_and_darker` | 49,552 | 19,822 |
| `iron_spells_and_spellbooks` | 196,960 | 12,733 |
| `never_end` | 347,632 | 10,223 |
| `the_factory_must_grow` | 4,720 | 4,720 |
| `test` | 533,664 | 4,104 |
| `hunting_aquatic` | 298,224 | 3,636 |
| `hunting_protector` | 94,176 | 2,934 |
| `ars_nouveau` | 135,472 | 2,662 |
| `mowzies_mob` | 0 | 331 |
| `First Line of Code` | 48 | 48 |
| `A New Beginning` | 40 | 37 |
| `the_aether` | 0 | 12 |
| `mutan_monster` | 0 | 5 |
| `welcome_magic_food` | 0 | 4 |
| `all_create` | 0 | 3 |
| `artifacts` | 0 | 3 |

## 4. Top 20 paying mobs

| Mob | Tier | Quests | Kills | Spurs | Spurs/kill |
|---|---|---:|---:|---:|---:|
| `minecraft:wither` | T4 | 14 | 7,561 | 20,963 | 2.77 |
| `mowziesmobs:naga` | T4 | 16 | 5,650 | 17,104 | 3.03 |
| `minecraft:warden` | T4 | 14 | 5,586 | 16,931 | 3.03 |
| `minecraft:ender_dragon` | T4 | 13 | 2,786 | 8,163 | 2.93 |
| `minecraft:wither_skeleton` | T2 | 15 | 22,560 | 3,178 | 0.14 |
| `minecraft:zombified_piglin` | T1 | 15 | 22,560 | 1,965 | 0.09 |
| `irons_spellbooks:necromancer` | T3 | 14 | 5,595 | 1,920 | 0.34 |
| `irons_spellbooks:archevoker` | T3 | 14 | 5,586 | 1,917 | 0.34 |
| `irons_spellbooks:citadel_keeper` | T3 | 14 | 5,586 | 1,917 | 0.34 |
| `irons_spellbooks:priest` | T3 | 14 | 5,586 | 1,917 | 0.34 |
| `minecraft:elder_guardian` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `minecraft:ravager` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `knightquest:ratman` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `knightquest:eldknight` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `knightquest:swampman` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `minecraft:illusioner` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `minecraft:iron_golem` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `twilightforest:minotaur` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `twilightforest:death_tome` | T3 | 12 | 5,560 | 1,908 | 0.34 |
| `twilightforest:carminite_golem` | T3 | 12 | 5,560 | 1,908 | 0.34 |

## 5. How to regenerate

Walk every `config/ftbquests/quests/chapters/*.snbt`, iterate the `quests: []` array, and for each
quest sum the `rewards` entries of type `item` whose item id is a Numismatics coin, counting
`reward.count x item.count x coin_value`.

Two traps, both of which silently undercount:

- FTB Quests writes reward arrays in two forms, the expanded `rewards: [` and the compact
  `rewards: [{`. Handling only the expanded form loses about a third of the total.
- The reward object carries its own `count` on top of the item stack count. Ignoring it halves
  the result.

## 6. The market chapter (money sink)

`config/ftbquests/quests/chapters/market.snbt` is the counterpart to the payouts above: a
buy-only shop of repeatable quests that take coins and give items. It removes money from
circulation, so it is the only brake on the quest-book faucet. There is deliberately no sell
side: letting players turn items back into coins would mint money and undo the tiering.

| Metric | Value |
|---|---:|
| Shop entries | 183 |
| Distinct items on sale | 183 |
| Mod namespaces covered | 20 |
| Cheapest unit price | 0.50 spurs |
| Dearest unit price | 4,096 spurs |

Price bands, by number of entries:

| Band (spurs per unit) | Entries |
|---|---:|
| under 2 | 26 |
| 2 to 8 | 73 |
| 8 to 64 | 47 |
| 64 to 512 | 22 |
| 512 and up | 15 |

Coverage by namespace: `aether` 6, `apotheosis` 6, `aquaculture` 4, `ars_nouveau` 10, `create` 15, `createaddition` 4, `deeperdarker` 4, `farmersdelight` 7, `fluxnetworks` 1, `immersiveengineering` 8, `irons_spellbooks` 4, `knightquest` 2, `mekanism` 16, `minecraft` 63, `mowziesmobs` 1, `occultism` 8, `refinedstorage` 4, `supplementaries` 2, `tfmg` 8, `twilightforest` 10.

### Checking that an item exists

Validate shop item ids against **item models**, `assets/<namespace>/models/item/*.json`, harvested
from every mod jar plus the vanilla jar plus `kubejs/assets`. Do not use lang files: mods keep
translation keys for content they have removed, so a lang-derived registry reports items that the
game cannot resolve. After any change, load the pack once and grep the chapter for
`ftbquests:missing_item`, which is FTB Quests naming exactly what it failed to resolve.

### Pricing rule

A price must never let the quest book buy its way past a progression gate. The budget above
(245,668 spurs) is the yardstick: divide it by a unit price to get how many of that item a player
can buy with every quest completed. Anything that sits behind a long chain, a boss or a
multiblock belongs at 512 spurs per unit or more, which keeps it under 500 units for a full
clear. Common intermediates sit between 1 and 8, raw materials below 2.

Five entries were repriced on 2026-09-20 for breaking that rule: Precision Mechanism and
Diamond moved to 128 per unit, Refined Radiance, Shadow Steel and Atomic Alloy to 512. At their
old prices a full quest clear bought 15,354 Precision Mechanisms or 3,839 Refined Radiance,
which made the chromatic chain and the Create gating pointless.

---

# Arcadia V2 - Economie du livre de quetes

Chiffres de reference du montant total en monnaie Numismatics que le livre FTB Quests peut verser.
A regenerer apres toute modification des recompenses. Ces nombres font foi pour equilibrer
l'hotel des ventes, les prix boutique et tout futur puits monetaire.

| Perimetre | Avant | Apres | Variation |
|---|---:|---:|---:|
| Quetes de kill | 3,408,008 | 186,484 | -95% |
| Autres quetes | 59,184 | 59,184 | 0% |
| **Livre entier** | **3,467,192** | **245,668** | **-93%** |

Toutes les valeurs en **spurs**. 245,668 spurs = 480 couronnes = 60.0 soleils.

C'est le plafond qu'un joueur peut frapper en terminant chaque quete une fois. Cette monnaie est
creee ex nihilo : elle fixe donc le plafond d'inflation de l'economie entre joueurs.

Paliers de difficulte appliques aux quetes de kill : T0 passif 0.01 spur/kill, T1 hostile commun
0.08, T2 dangereux 0.15, T3 elite 0.35, T4 boss 3.0. Le versement vaut arrondi(kills x taux),
rendu dans la plus grosse piece possible, avec un minimum d'un spur.

