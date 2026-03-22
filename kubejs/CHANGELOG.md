# Journal des modifications

## [Unreleased] - 2026-03-22
### Added / Ajouté
- **Music Disc Creative Tab Fix**: Added missing `arcadia:music_disc_au_pactole` to the Arcadia creative tab.
- **Correction Menu Créatif** : Ajout du disque `arcadia:music_disc_au_pactole` manquant dans l'onglet créatif Arcadia.
- **Global Tags Addition**: Created `global_tags.js` to add organizational tags (`c:` and `arcadia:is_item`) to various vanilla and modded items for easier sorting.
- **Ajout de Tags Globaux** : Création de `global_tags.js` pour ajouter des tags d'organisation (`c:` et `arcadia:is_item`) à divers objets vanilla et moddés pour faciliter le tri.

## [Unreleased] - 2026-03-17
### Optimized / Optimisé
- **Mob Stats Optimization**: Completely refactored `mob_stats.js` for KubeJS 1.21.1.
    - Replaced O(N) array lookups with O(1) object lookups for boss data.
    - Updated attribute handling to use `entity.type.id` and modern KJS attribute methods.
    - Consolidated health, damage, and armor boosting/clamping into a single-pass logic.
    - Added detailed console logging for transparency on entity stat adjustments.
- **Optimisation Mob Stats** : Refonte complète de `mob_stats.js` pour KubeJS 1.21.1.
    - Remplacement des recherches O(N) dans des tableaux par des recherches O(1) via un objet de données.
    - Mise à jour de la gestion des attributs pour utiliser `entity.type.id` et les méthodes KJS modernes.
    - Consolidation du boost et du bridage (HP, Dégâts, Armure) dans une logique à passage unique.
    - Ajout de logs console détaillés pour le suivi des ajustements de stats.

## [Non publié] - 2026-03-16
### Added / Ajouté
- [REMOVE] Script `spawn_protection.js` : Suppression de la protection anti-pose de blocs (le serveur utilise Yawp pour la gestion des zones).
- **Blaze Burner Exploit Patch**: Reinforced `patch_blaze_burner.js` to block Cart Assembler retrieval using `CreateEvents.canMoveBlock` and relocation tags.
- **FTB Chunks Config**: Updated `ftbchunks-world.snbt` to limit claims to 500 and force-loading to 1 chunk.
- **ReviveMe Bug Fix**: Fixed residual "slowness" (snoless) bug by adding a cleanup logic in `reviveme_feeding_fix.js`.
- **Patch Exploit Blaze Burner** : Renforcement de `patch_blaze_burner.js` pour bloquer le Cart Assembler via `CreateEvents.canMoveBlock` et des tags de relocalisation.
- **Correction Bug ReviveMe** : Correction du bug de lenteur résiduelle ("snoless") via une logique de nettoyage dans `reviveme_feeding_fix.js`.
- **NPC Protection Reinforcement**: Improved `npc_protection.js` to block vanilla leads, fishing rods, knockback, and vehicle mounting for Easy NPCs at spawn.
- **NPC Total Lockdown**: Reinforced `spawn_movement_block.js` and `npc_protection.js` to block Ars Nouveau spells, Simply Swords abilities, and added a dynamic anchoring system to keep NPCs immobile at spawn.
- **KubeJS Script Fix**: Resolved event name errors and constant redeclaration issues using an IIFE in `npc_protection.js`.
- [FIX] Script `npc_protection.js` : Correction de l'erreur `setDeltaMovement` (signature Java non reconnue) en utilisant `Utils.vec3`.
- **Isolation des Scripts KubeJS** : Utilisation d'un IIFE dans `npc_protection.js` pour éviter les erreurs de redéclaration de constantes lors des rechargements.
- [UPDATE] Libres de Bienvenue : Désactivation des guides MIMI, Parcool et Advanced Peripherals.
- [FIX] Schematicannon (Create) : Autorisation des fake players dans FTB Chunks pour le fonctionnement hors-ligne.
- [FIX] Script `npc_protection.js` : Correction de l'erreur `Unknown event` et optimisation finale (tick bridé à 20t et protection knockback directe).
- [FIX] Script `npc_protection.js` : Refonte complète du système pour corriger les lags massifs du serveur.
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
