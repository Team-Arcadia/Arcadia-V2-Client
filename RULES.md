# Project Rules & AI/IDE Instructions

## 1. Project Identity

| Field         | Value                                                          |
|---------------|----------------------------------------------------------------|
| Project name  | Arcadia V2 (branded "Arcadia: Echoes Of Power")                |
| Type          | Minecraft modpack (curated multiplayer, 30–50 players)         |
| Tech stack    | Minecraft 1.21.1 · NeoForge 21.1.232 · Java 21 · KubeJS        |
| Mod count     | 443 active JARs (+ 2 disabled)                                 |
| Config files  | ~1,174                                                         |
| Disk size     | 12–15 GB                                                       |
| Languages     | Code & UI: English · Docs: bilingual FR/EN · Items: 7 locales  |
| Author        | vyrriox                                                        |
| License       | See `LICENSE`                                                  |
| Namespace     | `arcadia:` (custom content)                                    |

**Custom Arcadia mods** (in-house, exclusive):
- `arcadia-lib`, `arcadia-admin-panel`, `arcadia-ah`, `arcadia-patch-create`, `arcadia-pets`, `arcadia-prestige`, `arcadia_spawn`, `arcadiaguard`

## 2. Git Workflow

- **Branch model**: single `main` branch (no staging/develop). Feature work committed directly to `main`.
- **Remote**: `origin/main`
- **Auto-push policy**: Every modification is immediately `git add . && git commit -m "..." && git push` per CLAUDE.md §3 — no confirmation required.
- **Commit convention** (enforced):
  - Format: `type: short description`
  - Types observed: `feat`, `chore`, `fix`, `refactor`, `docs`
  - Imperative mood, English, ≤ 72 chars subject
  - **NO AI attribution** — never add Co-Authored-By Claude, never mention Claude/AI/LLM in commits or code
- **Tracked**: `mods/`, `config/`, `kubejs/`, `saves/`, `defaultconfigs/`, `datapacks/`, `resourcepacks/`, `shaderpacks/`, `README.md`, `CHANGELOG.md` (if present)
- **Ignored**: `.claude/`, `CLAUDE.md`, `logs/`, `crash-reports/`, `local/`, `command_history.txt`. `.toml.bak` backup files are NOT kept — delete them on sight (repo cleaned 2026-07-20).
- **Version lock**: never bump the modpack version or mod versions unless the user explicitly requests it.
- **Release flow**: when user requests a version bump → update `minecraftinstance.json`, `README.md`, `CHANGELOG.md`, generate `TEST_PROCEDURE_vX.Y.Z.html`.

## 3. Code Conventions

- **Language policy**: all code, comments, identifiers, JEI search terms, log messages → **English only**. User-facing lang files → 7 locales (EN, FR, DE, ES, IT, PT, RU).
- **KubeJS scripts**:
  - `snake_case` for script filenames and recipe IDs
  - `camelCase` for JavaScript variables/functions
  - Every recipe MUST have an explicit `.id('arcadia:xxx')` — prevents duplicate IDs
  - Namespace all custom content as `arcadia:xxx`
  - Group server scripts under `server_scripts/{recipes,items,mobs,fixes}/...` subdirs
- **Datapack JSON**: use NeoForge 1.21.1 syntax — `remove` field for tags (NOT forge `replace`).
- **Config files**: prefer editing existing `.toml`/`.json`/`.properties` in place; do not create `.bak` copies (git is the backup). After any `config/` change, mirror it into `defaultconfigs/` (full mirror policy, excluding `spark/` and `arcadia/arcadiaadminpanel/logins.json`).
- **Architecture rules**:
  - Custom content → `kubejs/` (never patch mod JARs)
  - Balance/nerf changes → KubeJS server scripts, NOT mod configs (when possible)
  - Branding/menu → `config/fancymenu/`
  - Server-side progression → `config/arcadia/`
  - Quests → `config/ftbquests/quests/`
- **Do NOT**:
  - Bump mod versions without explicit request
  - Revert Ars Nouveau / Create / Revive-Me balance values to defaults
  - Add items to creative tabs without checking the ban list (`hide_banned_from_creative.js`)
  - Remove the 4-layer banned item defense (recipe/inventory/JEI/creative)
  - Commit `.claude/`, `CLAUDE.md`, `logs/`, `local/`

## 4. Project Structure

```
Arcadia V2/
├── mods/                    (446 .jar files — includes 8 arcadia-* custom mods)
├── config/                  (~1,156 files, 50+ subfolders)
│   ├── arcadia/             (custom server-side progression datapack)
│   ├── fancymenu/           (branded main menu "Echoes Of Power")
│   ├── ftbquests/quests/    (progression chapters)
│   ├── jei/                 (blacklist.json, sort order)
│   ├── ars_nouveau/         (nerfed: lectern 10, mana tuned)
│   ├── dndesires-server.toml (Create: Desires balance)
│   └── ... (many more mod configs)
├── kubejs/                  (custom scripting ecosystem)
│   ├── KUBEJS_GUIDE.md      (staff guide — READ FIRST)
│   ├── modified_recipes.txt (recipe change log)
│   ├── startup_scripts/     (9 files: registry + compat + UI)
│   ├── server_scripts/      (33 files: recipes, mobs, items, fixes, tags)
│   ├── client_scripts/      (1 file: bilingual tooltips)
│   ├── data/                (~1,465 JSON: apotheosis, apothic, arcadia jukebox, createoreexcavation, ...)
│   ├── assets/arcadia/      (~497 files: textures, 7 lang, sounds)
│   └── config/              (client/common/web_server JSON)
├── saves/TEST/              (active test world)
├── ESM/                     (snapshot archives — historical, never modify)
├── resourcepacks/           (hud.zip, ArcadiaLanguages)
├── shaderpacks/             (13 shaders)
├── defaultconfigs/          (full mirror of config/ — new-world & server defaults)
├── datapacks/               (empty — all data in kubejs/data/)
├── README.md                (bilingual FR/EN)
├── STRUCTURE.md             (full structural map, bilingual)
├── CHANGELOG.md             (dated bilingual change history)
├── minecraftinstance.json   (CurseForge metadata, 1.2M tokens — grep, don't read whole)
└── RULES.md                 (this file)
```

## 5. Adding a New Feature (Step by Step)

1. **Read `kubejs/KUBEJS_GUIDE.md`** and this `RULES.md` completely.
2. **Check the ban list**: does the new feature conflict with banned items (152 banned) or the Fusion Core chain gating? If yes → stop and discuss with user.
3. **Identify the layer**:
   - New item/block/sound/armor → `kubejs/startup_scripts/registry/`
   - New recipe → `kubejs/server_scripts/recipes/{custom,mods,create}/`
   - Recipe removal → `kubejs/server_scripts/items/banned/recipe_remover.js`
   - Mob stat change → `kubejs/server_scripts/mobs/`
   - Loot table → `kubejs/server_scripts/items/loot/loot_table_nerfs.js`
   - Tooltip → `kubejs/client_scripts/arcadia_item_tooltips.js`
   - Progression/admin → `config/arcadia/`
   - Quest → `config/ftbquests/quests/`
   - Branding → `config/fancymenu/`
4. **Implement** with `arcadia:` namespace, explicit `.id()`, `snake_case` filenames.
5. **Add lang keys** in all 7 locales under `kubejs/assets/arcadia/lang/`.
6. **Update** `kubejs/modified_recipes.txt` (recipe-level changes) and `kubejs/KUBEJS_GUIDE.md` (architectural changes).
7. **Test**: launch client, load TEST world, `/reload` for server scripts or full restart for startup scripts. Validate via JEI/EMI search + craft.
8. **Document**: bilingual entry in `README.md` if user-facing; log any errors in `ERROR_LOG.md`.
9. **Commit & push**: `git add . && git commit -m "feat: ..." && git push` (CLAUDE.md §3 — no confirmation).

## 6. Testing Checklist

Before reporting any task complete:

- [ ] **Syntax check**: KubeJS scripts parse (no red in `logs/kubejs/startup.log`, `server.log`, `client.log`)
- [ ] **Recipe presence**: new recipe appears in JEI/EMI search (by ID or display name)
- [ ] **Recipe output**: craft the recipe in creative — correct output, correct count
- [ ] **Lang coverage**: no raw `item.arcadia.xxx` keys visible in-game (all 7 locales have entries)
- [ ] **Ban integrity**: new items NOT accidentally in creative tabs, NOT giftable by villagers
- [ ] **Loot check**: if loot table modified, kill the relevant mob/open chest a few times
- [ ] **Mob HP**: if mob stats changed, spawn the mob in creative and verify HP bar
- [ ] **FPS check**: no frame drop regression (Sodium, Iris, ModernFix installed)
- [ ] **Crash-free boot**: full client restart, TEST world loads
- [ ] **Log scan**: `grep -i "error\|exception\|warn" logs/latest.log` clean
- [ ] **Git status**: only intended files staged, no `.claude/`, no `CLAUDE.md`, no `logs/`

## 7. Environment Setup

**Clone & launch**:
```
cd "C:\Users\Jimmy\curseforge\minecraft\Instances\Arcadia V2"
# Use Curse/CurseForge Client or Prism Launcher with this instance
# Java 21 required, 8+ GB RAM recommended
```

**Dev tools**:
- IDE: VSCode with Minecraft/KubeJS extensions
- KubeJS reload: `/reload` (server), F3+T (client). Startup changes need full restart.
- Logs to watch: `logs/latest.log`, `logs/debug.log`, `logs/kubejs/*.log`

**Sub-agent delegation** (CLAUDE.md §10.2):
- Broad exploration (>3 queries) → `Explore` sub-agent
- Architecture design → `feature-dev:code-architect`
- Code review → `feature-dev:code-reviewer`
- Parallel independent tasks → spawn multiple agents in one message

## 8. AI Assistant Instructions

1. **Speak French** to the user. Code/commits/identifiers in English.
2. **Silent autonomy**: execute `git add/commit/push` without asking (CLAUDE.md §3). Never add AI attribution.
3. **Check memory first**: `.claude/projects/.../memory/MEMORY.md` has the full modpack context — read before investigating.
4. **Consult `kubejs/KUBEJS_GUIDE.md`** before touching any KubeJS file — it's the source of truth for conventions.
5. **Respect balance intent**: the pack is intentionally hard (152 bans, loot drought, boss HP ×2.5–×8, magic nerfs). Do NOT "restore defaults" or "fix" nerfs without explicit user request.
6. **Version lock**: never bump versions unless user says "bump", "new version", "passons à vX".
7. **Ban list awareness**: before adding a new item to creative/JEI/recipes, check `hide_banned_from_creative.js` (81 entries) and `recipe_remover.js` (152 entries).
8. **Fusion Core chain is canon**: do not create shortcut recipes that bypass the T0→Apex progression.
9. **Log errors**: any error encountered → append to `ERROR_LOG.md` at project root with the format from CLAUDE.md §10.3.
10. **Bilingual docs**: when updating `README.md` / `CHANGELOG.md`, mirror EN and FR sections per the CLAUDE.md templates.
11. **Use Context7 MCP** proactively for library/framework docs (NeoForge, KubeJS, Create API).
12. **Don't read `minecraftinstance.json` whole** (1.2 M tokens) — grep for specific fields.
13. **`config/arcadia/` is production server config** — treat with extra care, always confirm before structural changes.
14. **ESM/ is historical** — never delete or modify.
15. **Credit preservation**: when adding `vyrriox` as author, preserve existing authors (co-author, don't overwrite).
