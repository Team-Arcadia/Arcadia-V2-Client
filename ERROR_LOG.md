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
