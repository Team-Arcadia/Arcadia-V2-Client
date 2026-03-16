# Journal des modifications

## [Non publié] - 2026-03-16
### Added / Ajouté
- **Blaze Burner Exploit Patch**: Reinforced `patch_blaze_burner.js` to block Cart Assembler retrieval using `CreateEvents.canMoveBlock` and relocation tags.
- **FTB Chunks Config**: Updated `ftbchunks-world.snbt` to limit claims to 500 and force-loading to 1 chunk.
- **ReviveMe Bug Fix**: Fixed residual "slowness" (snoless) bug by adding a cleanup logic in `reviveme_feeding_fix.js`.
- **Patch Exploit Blaze Burner** : Renforcement de `patch_blaze_burner.js` pour bloquer le Cart Assembler via `CreateEvents.canMoveBlock` et des tags de relocalisation.
- **Correction Bug ReviveMe** : Correction du bug de lenteur résiduelle ("snoless") via une logique de nettoyage dans `reviveme_feeding_fix.js`.
- **NPC Protection Reinforcement**: Improved `npc_protection.js` to block vanilla leads, fishing rods, knockback, and vehicle mounting for Easy NPCs at spawn.
- **NPC Total Lockdown**: Reinforced `spawn_movement_block.js` and `npc_protection.js` to block Ars Nouveau spells, Simply Swords abilities, and added a dynamic anchoring system to keep NPCs immobile at spawn.
- **KubeJS Script Fix**: Resolved event name errors and constant redeclaration issues using an IIFE in `npc_protection.js`.
- **Isolation des Scripts KubeJS** : Utilisation d'un IIFE dans `npc_protection.js` pour éviter les erreurs de redéclaration de constantes lors des rechargements.
- [UPDATE] Libres de Bienvenue : Désactivation des guides MIMI, Parcool et Advanced Peripherals.
- [FIX] Schematicannon (Create) : Autorisation des fake players dans FTB Chunks pour le fonctionnement hors-ligne.
- [FIX] Script `npc_protection.js` : Refonte complète du système (migration vers `EntityEvents.tick`) pour corriger les lags massifs du serveur.
- [FIX] Script `npc_protection.js` : Suppression de l'invincibilité (Résistance 255) des NPCs comme demandé.
- [FIX] Script `npc_protection.js` : Correction d'une erreur de type (remplacement de `has` par `isActive` pour les effets de potion).
- [FIX] Script `remove_from_creative.js` : Retrait de l'ID inexistant `occultism:lighted_air`.
- [FIX] Script `npc_protection.js` : Verrouillage total des NPCs avec Résistance 255 et Ancrage Dynamique.
- [UPDATE] FTB Chunks : Claims limités à 500, Forceload à 1.
- [UPDATE] FTB Chunks : Claims restreints à l'Overworld et JAVD uniquement.
- [UPDATE] FTB Chunks : PvP en zone claim réglé sur `per_team`.
- [BAN] ComputerCraft : Toutes les Turtles sont bannies et supprimées.
- [BAN] Better Copper : Les Copper Hearts sont bannis.
- [UNBAN] Mekanism : HDPE Sheets et Rods réactivés.
- **Protection PNJ Totale** : Renforcement de `spawn_movement_block.js` et `npc_protection.js` pour bloquer les sorts Ars Nouveau, les capacités Simply Swords et ajout d'un système d'ancrage dynamique pour figer les PNJ au spawn.
- **Renforcement Protection PNJ** : Amélioration de `npc_protection.js` pour bloquer les laisses, les cannes à pêche, le recul et l'utilisation de véhicules sur les PNJ au spawn.
- **Config FTB Chunks** : Mise à jour de `ftbchunks-world.snbt` pour limiter à 500 claims et 1 seul chunk loadé.

## [Non publié] - 2026-03-14
### Added / Ajouté
- **ReviveMe Fixes**: Blocked `/home`, `/spawn`, `/tpa`, and `/tpahere` while in downed state in `reviveme-common.toml`.
- **Feeding Upgrade Fix**: Added `reviveme_feeding_fix.js` to prevent Sophisticated Backpacks from infinitely consuming food when a player is downed.
- **ReviveMe Fixes** : Blocage des commandes `/home`, `/spawn`, `/tpa`, et `/tpahere` lors de l'état "à terre" dans `reviveme-common.toml`.
- **Correctif Feeding Upgrade** : Ajout de `reviveme_feeding_fix.js` pour empêcher le Feeding Upgrade de consommer de la nourriture à l'infini quand le joueur est à terre.

## [Non publié] - 2026-03-10
### Ajouté
- Limite globale de PV (10 000) pour tous les mobs dans `mob_stats.js`.
- Limite globale de dégâts (50) pour les mobs attaquant les joueurs dans `mob_stats.js`.
- **Système de Protection Ultime** : Implémentation d'un verrouillage idempotent à plusieurs couches pour empêcher le cumul des stats.
- **Protection des PNJ** : Blocage des Laisses de l'Ender (toutes variantes) sur les entités Easy NPC dans `npc_protection.js`.
- **Décumul de Netherite** : Ajout d'une recette complexe d'Assemblage Séquentiel (Create) pour décrafter les Blocs de Netherite en 9 Lingots dans `decraft_netherite.js`.
