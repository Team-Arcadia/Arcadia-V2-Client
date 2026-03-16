# Arcadia V2 - KubeJS Scripts

Custom scripts for the Arcadia V2 modpack to balance gameplay.

## Features
- **Mob Stats Balancing**: Adjusts health, damage, and armor for various bosses and mobs.
- **Stat Caps**: 
  - Maximum Health: 10,000 HP
  - Maximum Damage: 50 (25 Hearts)
- **Stacking Fix**: Prevents mob stats from increasing every time chunks are loaded.
- **Loot Balancing**: Reduces equipment drop rates to 5%.
- **Netherite Decrafting**: Added a complex Create Sequenced Assembly recipe to decraft Netherite Blocks into 9 Ingots in `decraft_netherite.js`.
- **Blaze Burner Exploit Patch**: Prevents Blaze Burners from being moved by contraptions (including Cart Assemblers) using tags and Create events in `patch_blaze_burner.js`.
- **NPC Protection Reinforcement**: Blocks leads, fishing rods, vehicles, and knockback for Easy NPCs in the spawn area via `npc_protection.js`. (Block protection managed by Yawp).
- **FTB Chunks Limits**: Configured maximum claimed chunks to 500 and force-loaded chunks to 1 in `ftbchunks-world.snbt`.

## Authors
- vyrriox

---

# Arcadia V2 - Scripts KubeJS

Scripts personnalisés pour le modpack Arcadia V2 afin d'équilibrer le gameplay.

## Fonctionnalités
- **Équilibrage des Stats des Mobs** : Ajuste la vie, les dégâts et l'armure de divers boss et mobs.
- **Limites de Stats** : 
  - Santé Maximum : 10 000 PV
  - Dégâts Maximum : 50 (25 Cœurs)
  - Armure Maximum : 50
- **Protection Ultime** : Système de protection à plusieurs couches pour empêcher le cumul des stats lors du chargement des chunks ou des conflits entre mods.
- **Équilibrage du Loot** : Réduit le taux de drop d'équipement à 5 %.
- **Décumul de Netherite** : Ajout d'une recette complexe d'Assemblage Séquentiel (Create) pour décrafter les Blocs de Netherite en 9 Lingots dans `decraft_netherite.js`.
- **Patch Exploit Blaze Burner** : Empêche tout mouvement des Blaze Burners par Create (y compris via Cart Assembler) et bloque leur récupération via `patch_blaze_burner.js`.
- **Protection PNJ Renforcée** : Bloque les laisses, cannes à pêche, véhicules et le recul pour les NPC au spawn via `npc_protection.js`. (Protection des blocs gérée par Yawp).
- **Limites FTB Chunks** : Limitation à 500 claims et 1 chunk load forcé dans `ftbchunks-world.snbt`.

## Auteurs
- vyrriox
