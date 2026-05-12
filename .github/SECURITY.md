# Security Policy / Politique de securite

## Supported Versions / Versions supportees

| Version | Supported |
|---------|-----------|
| 2.0.x   | Yes / Oui |
| < 2.0   | No / Non  |

Only the current `2.0.X` release line receives security and bug fixes. Older release lines are not maintained.

Seule la ligne de version `2.0.X` actuelle recoit les correctifs de securite et de bugs. Les anciennes lignes ne sont pas maintenues.

## Scope / Portee

This security policy covers vulnerabilities in **Arcadia originals** only:
- Our KubeJS scripts (`kubejs/`)
- Our datapack overrides (`kubejs/data/`)
- Our config overlays (`config/arcadia*`)
- Our resource pack (`resourcepacks/ArcadiaLanguages/`)
- Our in-house mod jars (where we are the authors)
- Documentation and tooling in this repository

Vulnerabilities in **third-party mods** resolved by `manifest.json` are **not** in scope — please report those directly to their respective authors on CurseForge / Modrinth / the mod's own bug tracker.

Cette politique de securite couvre uniquement les vulnerabilites des **originaux Arcadia**. Les vulnerabilites des **mods tiers** resolus par `manifest.json` ne sont **pas** dans le perimetre — signalez-les directement aux auteurs respectifs sur CurseForge / Modrinth / le tracker du mod.

## What counts as a vulnerability / Ce qui compte comme vulnerabilite

- Server-crashing or hangs triggered by player input via our KubeJS scripts
- Inventory or recipe duplication caused by our custom recipes
- Privilege escalation or staff-command bypass via our scripts
- Exposure of player private data through our scripts or configs
- XSS / injection vectors in our website-facing JSON (if applicable)

What does NOT count:
- Cheats or exploits inherent to a third-party mod (report to the mod author)
- Imbalanced gameplay or design disagreements (use Discord or a regular issue)
- Performance regressions (use a regular issue)

## Reporting a Vulnerability / Signaler une vulnerabilite

**Do not** report security vulnerabilities through public GitHub issues, Discord channels, or in-game chat.

Instead, please report them via one of:
- **Private security advisory on GitHub** — preferred for repo-scope issues: [Open a draft advisory](https://github.com/Team-Arcadia/Arcadia-V2-Client/security/advisories/new)
- **Discord DM to vyrriox**: [Discord Server](https://discord.gg/xjF8Rtzyd4)

We aim to acknowledge reports within **48 hours** and to issue a fix or mitigation within **14 days** for confirmed high-impact issues.

---

**Ne signalez pas** les vulnerabilites via les issues GitHub publiques, les salons Discord ou le chat en jeu.

Signalez-les via l un de ces canaux :
- **Avis de securite prive sur GitHub** — recommande pour les problemes du depot : [Ouvrir un avis](https://github.com/Team-Arcadia/Arcadia-V2-Client/security/advisories/new)
- **Message prive Discord a vyrriox** : [Serveur Discord](https://discord.gg/xjF8Rtzyd4)

Nous visons un accuse de reception sous **48 heures** et un correctif ou une attenuation sous **14 jours** pour les problemes confirmes a fort impact.

## Responsible Disclosure / Divulgation responsable

We ask that reporters:
- Give us reasonable time to investigate and patch before any public disclosure
- Avoid exploiting the vulnerability on the production server beyond what is strictly necessary to demonstrate it
- Avoid accessing other players' data

Nous demandons aux personnes qui signalent :
- De nous laisser un delai raisonnable pour enqueter et corriger avant toute divulgation publique
- D eviter d exploiter la vulnerabilite sur le serveur de production au-dela du strict necessaire pour la demontrer
- D eviter d acceder aux donnees des autres joueurs
