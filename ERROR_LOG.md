# Error Log — Arcadia V2

## [2026-06-13] — git add aborted by deleted-file pathspec, partial commit pushed

**Context:** Committing Apotheosis loot nerfs together with the removal of `equipment_drop_cap.js` (already staged via `git rm`).
**Error:** `fatal: pathspec 'kubejs/server_scripts/mobs/equipment_drop_cap.js' did not match any files` — the `git add` listing that path aborted entirely, then `git commit` shipped only the previously staged deletion. The new data files were silently left out of the pushed commit.
**Root cause:** A `git rm`'d file no longer exists in the working tree, so passing it to `git add` is a fatal pathspec error; `git add` is all-or-nothing across its arguments.
**Fix:** Re-ran `git add` without the deleted path, verified with `git status -s`, committed and pushed the missing files in a follow-up commit.
**Prevention:** Never pass `git rm`'d paths to a later `git add`. After any failed `git add`, check `git status -s` BEFORE committing; verify the commit summary line (files changed count) matches expectations before pushing.

## [2026-05-11 — FTB Quests lang files corruption (Unnamed Group / Sans nom)

**Context:** Mass translation work across 7 FTB Quests lang files (en_us, en_gb, fr_fr, es_es, pt_br, ru_ru, zh_cn). Player reported all quests and chapter groups displaying as "Unnamed Group" / "Sans nom" in-game.

**Error:** All 7 lang files structurally corrupt:
- 255–516 malformed keys using item IDs (`quest.minecraft:flint_and_steel.quest_desc`) instead of quest hex IDs (`quest.787A04639A74D85A.quest_desc`).
- 275 unclosed `[` brackets in fr_fr/es_es/pt_br/ru_ru/zh_cn/en_gb.
- FTB Quests parser silently fails on the file and falls back to "Unnamed" for every quest and group title.

**Root cause:** The phase-2 merge script (`merge_phase2.py`) used the item ID extracted from a quest's task list as the key prefix instead of the quest's hex UUID. Phase 3 `fill_orphans.py` propagated and amplified the corruption. The custom audit tool (`audit_5_final.py`) only checked key count and identical-EN comparison, NOT structural SNBT validity — so the corruption passed all 5 audits silently.

**Fix:** Restored all 7 lang files from `translation_workspace/ftbq_audit/<lang>_original_backup.snbt` (en_us restored from `git show HEAD~1`). All translation work since the initial state is discarded. Files re-synced to `defaultconfigs/ftbquests/quests/lang/`.

**Prevention:**
1. Any future SNBT generation script MUST validate bracket balance and key format (`^[a-z_]+\.[A-F0-9]{16}\.[a-z_]+$` for quest/task/chapter entries) BEFORE writing output.
2. Audit tools MUST include a real SNBT parse step (not just key counting). Treat parse failure as a critical audit failure that blocks downstream work.
3. Never trust the phase-2 backups again — they were already corrupt at creation. Always keep `_original_backup` as the only safe rollback target.
4. Bulk translation should write to a sandbox file, then run a full SNBT round-trip parse (load → re-serialize → diff) before replacing the live lang file.

## [2026-07-20] — Phantom dndecor bolt IDs crash creative-tab hide at startup

**Context:** Full-pack audit; reviewing `logs/kubejs/startup.log` for script errors.
**Error:** `Error in 'StartupEvents.modifyCreativeTab': Failed to read ingredient from dndecor:lead_cross_bolt: Item with ID dndecor:lead_cross_bolt does not exist!` — the only ERROR-level line in KubeJS logs.
**Root cause:** The three ban lists drifted apart. `inventory_scanner.js` and `loot_table_nerfs.js` were updated to the real Design n' Decor bolt IDs (andesite/brass/copper/gold/industrial/iron/netherite/zinc), but `hide_banned_from_creative.js` (both lists) and `recipe_remover.js` kept the obsolete lead/tin/uranium/aluminum/nickel/steel/bronze/cast_iron set.
**Fix:** Replaced all three stale lists with the corrected mineral set already used in `inventory_scanner.js`.
**Prevention:** The 4 ban lists (creative hide ×2, recipe remover, inventory scanner, loot nerfs) must be updated together — grep all of `kubejs/` for the old ID before renaming any banned item.

## [2026-07-20] — Wrong CC: Tweaked kept when resolving the duplicate

**Context:** Full-pack audit found two CurseForge projects both shipping the computercraft mod id (official CC: Tweaked 1.113.1 and unofficial port 1.117.1). One had to go.
**Error:** Kept the official 1.113.1 based on install date; on next launch, `advancedperipherals` and `fncct` failed dependency checks: "requires computercraft 1.116.2 or above. Currently 1.113.1".
**Root cause:** Chose which duplicate to keep by project officiality/install date instead of checking the version constraints of DEPENDENT mods. The unofficial 1.117.1 port existed precisely because the official project lags behind on 1.21.1.
**Fix:** Re-downloaded cc-tweaked-1.21.1-forge-1.117.1.jar (project 1527866, file 8005487) from the CurseForge CDN, deleted the 1.113.1 jar, swapped the manifest entry back.
**Prevention:** Before removing one of two duplicate mods, grep the other jars' dependency ranges (or launch once) to see which version the pack's dependents require. Newest version wins by default, not "most official".

## [2026-07-20] — Sodium Leaf Culling crashes on world join after Sodium 0.8.12 update

**Context:** Game crashed when joining a world (ClientboundLoginPacket -> SodiumWorldRenderer init).
**Error:** MixinPreProcessorException in mixins.sodiumleafculling.json:BlockRendererMixin — ClassNotFoundException: net.caffeinemc.mods.sodium.client.gui.SodiumGameOptions.
**Root cause:** Sodium was updated to 0.8.12 during the manifest resync; SodiumGameOptions moved in Sodium 0.8.x. Sodium Leaf Culling 1.0.1 (latest available for NeoForge 1.21.1, April 2025) targets the old class and has no compatible release.
**Fix:** Removed the sodiumleafculling jar and its manifest entry (project 1089479). Sodium 0.8 handles leaf quality natively.
**Prevention:** After bulk mod updates, check small Sodium-addon mods (leafculling-style tweaks) against the new Sodium version — they break on internal class moves and are often abandoned.
