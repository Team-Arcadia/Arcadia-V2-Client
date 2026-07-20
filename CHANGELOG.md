# Changelog

All notable changes to Arcadia V2 - Echoes Of Power are documented here, by date.

---

## 2026-07-20

### Added

- **Proprietary license** — Replaced the MIT license with the Arcadia V2 Proprietary License (source-available): viewing, private copies, private modifications, and contributions are allowed; redistribution, republication, derivative packs, and monetization are prohibited. Third-party and no-affiliation clauses retained, bilingual EN/FR.
- **CREDITS.md** — New bilingual credits file: founders, staff, development and content contributors, special thanks.
- **STRUCTURE.md** — New bilingual structural map of the whole instance: top-level layout, config/ key areas, full kubejs/ ecosystem breakdown, in-house mod list.
- **CHANGELOG.md** — This file; version history now tracked in the repository.
- **defaultconfigs full mirror** — `defaultconfigs/` now mirrors `config/` in full (~1,170 files) so new worlds and fresh server installs start from the curated defaults. `config/spark/` (runtime profiling data) and the admin panel credentials file are excluded from the mirror.

### Changed

- **manifest.json regenerated from the live instance** — Now 456 entries (443 mods + 13 shaderpacks): 6 new projects added (Create O' Plenty, Create: Ice & Creams, Create Heat JS, Steam 'n' Rails, WATERMeDIA: Binaries, Create: Apotheosis Automation), 100 file IDs bumped to the installed versions, mod loader raised to NeoForge 21.1.232.
- **README.md refreshed** — Mod counts aligned with the real manifest (450 manifest entries, 446 active jars), repository contents table updated with the new documentation files.
- **RULES.md structure section updated** — File counts and kubejs/ tree brought in line with the current state of the instance.

### Fixed

- **Repository cleanup** — Removed 21 stale `.toml.bak` backup files from `config/`, ~170 archived rotated logs (`logs/*.log.gz`), old client disconnect reports in `debug/`, two 500+ MB spark heap dumps (`config/spark/heap-*.hprof`), the empty `rapport_test/` folder, and the obsolete 99 MB `translation_workspace/` (translation tooling no longer in use).

### Performance

- **Render-thread hotspots** — Config-level mitigations for render-thread hotspots identified via spark profiling (carried from the previous commit series, documented here).

### Ajouts

- **Licence propriétaire** — La licence MIT est remplacée par la Licence Propriétaire Arcadia V2 (source visible) : consultation, copies privées, modifications privées et contributions autorisées ; redistribution, republication, packs dérivés et monétisation interdits. Clauses tiers et non-affiliation conservées, bilingue EN/FR.
- **CREDITS.md** — Nouveau fichier de crédits bilingue : fondateurs, staff, contributeurs développement et contenu, remerciements spéciaux.
- **STRUCTURE.md** — Nouvelle carte structurelle bilingue de l'instance : arborescence racine, zones clés de config/, détail complet de l'écosystème kubejs/, liste des mods maison.
- **CHANGELOG.md** — Ce fichier ; l'historique des versions est désormais suivi dans le dépôt.
- **Miroir complet defaultconfigs** — `defaultconfigs/` reflète désormais intégralement `config/` (~1 170 fichiers) afin que les nouveaux mondes et installations serveur partent des défauts organisés. `config/spark/` (données de profiling runtime) et le fichier d'identifiants du panneau admin sont exclus du miroir.

### Modifications

- **manifest.json régénéré depuis l'instance** — Désormais 456 entrées (443 mods + 13 shaderpacks) : 6 nouveaux projets ajoutés (Create O' Plenty, Create: Ice & Creams, Create Heat JS, Steam 'n' Rails, WATERMeDIA: Binaries, Create: Apotheosis Automation), 100 IDs de fichiers alignés sur les versions installées, mod loader monté à NeoForge 21.1.232.
- **README.md rafraîchi** — Compteurs de mods alignés sur le manifest réel (450 entrées manifest, 446 jars actifs), table du contenu du dépôt mise à jour avec les nouveaux fichiers de documentation.
- **Section structure de RULES.md mise à jour** — Compteurs de fichiers et arborescence kubejs/ alignés sur l'état actuel de l'instance.

### Correctifs

- **Nettoyage du dépôt** — Suppression de 21 fichiers de sauvegarde `.toml.bak` obsolètes dans `config/`, ~170 logs archivés (`logs/*.log.gz`), anciens rapports de déconnexion dans `debug/`, deux heap dumps spark de 500+ Mo (`config/spark/heap-*.hprof`), le dossier vide `rapport_test/`, et l'obsolète `translation_workspace/` de 99 Mo (outillage de traduction plus utilisé).

### Performance

- **Hotspots du thread de rendu** — Mitigations au niveau config des hotspots du thread de rendu identifiés via profiling spark (héritées de la série de commits précédente, documentées ici).

---
