# Journal des modifications

## [Non publié] - 2026-03-16
### Added / Ajouté
- **Blaze Burner Exploit Patch**: Added `patch_blaze_burner.js` to prevent infinite Blaze Burner spawning exploit via Create contraptions and restricted interactions in the Nether.
- **FTB Chunks Config**: Updated `ftbchunks-world.snbt` to limit claims to 500 and force-loading to 1 chunk.
- **Patch Exploit Blaze Burner** : Ajout de `patch_blaze_burner.js` pour empêcher l'exploit de spawn infini de Blaze Burners via les contraptions Create et restriction des interactions dans le Nether.
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
