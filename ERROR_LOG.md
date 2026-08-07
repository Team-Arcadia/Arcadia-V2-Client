# Error Log — Arcadia V2

## [2026-07-20 16:39] — Client crash on Video Settings click (Reese's Sodium Options wrong MC version)

**Context:** Client crashed with a `mouseClicked event handler` crash when clicking a button in the Video Settings screen (opening the Sodium options GUI).
**Error:** `MixinApplyError: Mixin [reeses-sodium-options.mixins.json:sodium.MixinFlatButtonWidget from mod reeses_sodium_options] FAILED during APPLY` — caused by `InvalidMixinException: @Shadow field dim was not located in the target class net.caffeinemc.mods.sodium.client.gui.widgets.FlatButtonWidget`.
**Root cause:** `reeses-sodium-options-neoforge-1.8.3+mc1.21.4.jar` is built for Minecraft 1.21.4, while the pack runs MC 1.21.1 with `sodium-neoforge-0.8.12+mc1.21.1.jar`. The 1.21.4 build targets a newer Sodium (0.6+) whose `FlatButtonWidget` class layout differs, so the mixin fails to apply at class-load time — which only happens lazily when the Video Settings screen loads that widget class.
**Fix:** Replace the jar with the Reese's Sodium Options build for MC 1.21.1 / Sodium 0.8.x NeoForge (or remove the mod if no compatible build exists).
**Prevention:** When adding or updating client mods, verify the `+mcX.Y.Z` suffix in the jar name matches the pack's MC version (1.21.1). Wrong-version mods can load fine at startup and only crash when their mixin targets are first classloaded.

## [2026-07-20 17:00] — Startup incompatibility: RSO 2.x vs Sodium Options API

**Context:** After replacing Reese's Sodium Options 1.8.3 (wrong MC version) with 2.2.3+mc1.21.1, the game refused to start: `Mod reeses_sodium_options is incompatible with sodiumoptionsapi 0 or above`.
**Error:** FML loading error `fml.modloadingissue.incompatiblemod.noreason` — RSO 2.x declares a hard incompatibility with `sodiumoptionsapi` (any version), while `sodiumoptionsapi 1.0.10` itself declares a mandatory dependency on `reeses_sodium_options` — a circular dead-end.
**Root cause:** Sodium Options API (+ Sodium Options Mod Compat) targets the pre-0.6 Sodium options GUI and RSO 1.x hooks; the ecosystem was never updated for Sodium 0.8.x (latest sodiumoptionsapi release: 1.0.10, 2025-01). RSO 2.x rewrote the GUI integration and explicitly blocks the stale API to avoid broken hooks.
**Fix:** Scanned all 443 mod jars' mods.toml — nothing else depends on `sodiumoptionsapi` or `reeses_sodium_options`. Removed `sodiumoptionsapi-neoforge-1.0.10-1.21.1.jar` and `sodiumoptionsmodcompat-neoforge-1.0.0-1.21.1.jar`; kept RSO 2.2.3 which replaces their functionality.
**Prevention:** When bumping a mod across a major version, check its declared incompatibilities (mods.toml) against installed companion/addon mods, and check whether those companions are still maintained for the current Sodium/loader line before keeping them.

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

## [2026-07-20] — Apotheosis Create recipes invisible (two stacked format bugs)

**Context:** New mod apotheosis_create-1.1.0 showed nothing in JEI even after /reload and after re-shipping its recipes via kubejs/data.
**Error:** No log errors; recipes silently absent.
**Root cause:** Two issues stacked: (1) the mod ships recipes in data/<ns>/recipes/ (pre-1.21 plural folder) so 1.21.1 never reads them; (2) the recipe JSONs use the Create 5 schema (transitionalItem, results[].item) while the pack runs Create 6, whose codec expects transitional_item and results[].id and silently drops the old format.
**Fix:** Re-shipped the 8 recipes under kubejs/data/apotheosis_create/recipe/ and converted them to the Create 6 schema.
**Prevention:** When a compat mod's content is missing, check BOTH the datapack folder layout (recipe/ singular on 1.21+) and the recipe schema against the installed Create major version (compare with a recipe from the create jar itself).

## [2026-07-20] — Bug #213: kicked with "Network Protocol Error" when chatting while dying

**Context:** Player report: typing a chat message at the moment of death kicks the player instead of showing the respawn screen.
**Error:** Client disconnected with "Network Protocol Error" (server-side signed-chat validation failure).
**Root cause:** Since 1.19.3 every chat packet carries a signed-message acknowledgement; a message sent in the same instant as the death/respawn desyncs the acknowledgement chain and the server kicks. The pack ships No Chat Reports, but NCR-Client.json had defaultSigningMode=PROMPT, so any player who answered "sign" at first join kept sending signed messages and stayed exposed to the race.
**Fix:** defaultSigningMode set to NEVER (mirrored to defaultconfigs). Unsigned messages skip signature validation entirely; the server config already converts chat to system messages (convertToGameMessage=true).
**Prevention:** Never ship NCR in PROMPT mode on a curated pack; verify the dedicated server's own NCR-Common.json also has convertToGameMessage=true. Players who chose signing before this fix keep their per-server choice: they must click the NCR shield icon in the chat screen once and pick "unsigned", or delete their NCR-ServerPreferences.json.

## [2026-07-20 16:00] — Lootboxes not appearing in game (all 15 new boxes rejected)
**Context:** Reworked shop_* and event_* lootbox definitions for ArcadiaLootbox 1.2.6.
**Error:** New lootboxes absent from the in-game hub on the test server; no crash.
**Root cause:** LootboxManager.validate() requires every lootTable entry chance to be within [0,1]. The new files used integer weights 1..10 ("chance acts as weight" in guaranteed mode), so validate() returned false and every box was skipped at load.
**Fix:** Scaled all chance values by /10 (relative weights preserved), propagated to defaultconfigs and all server folders.
**Prevention:** For ArcadiaLootbox configs, always keep chance in [0,1] even in guaranteed/weight mode. Empty guaranteedItem only warns, it does not reject.

## [2026-07-20 17:30] — Voice chat broken on all servers after config sync
**Context:** Client-to-server config sync overwrote every config file that existed on both sides.
**Error:** Simple Voice Chat stopped working on the remote servers after the config upload.
**Root cause:** `config\voicechat\voicechat-server.properties` exists in the solo client too (generated by the integrated server) with default values (port=24454, empty voice_host). The sync overwrote the per-server UDP port / voice_host values with those defaults.
**Fix:** Removed `config\voicechat\` from all staging folders; original values must be restored from the hosting panel backup or re-entered per server (port + voice_host), then restart.
**Prevention:** `config\voicechat\` is now on the never-ship blacklist in PROCEDURE_MAJ.md. Generally: any *-server.properties/runtime file that also exists client-side must be excluded from config syncs.

## [2026-08-01] — Bug #224: Steam 'n' Rails couplers reported as uncraftable

**Context:** Player report claiming the Knuckle / Split Knuckle / Screwlink / Linkless Link'n Pin couplers, their headstock and copycat headstock variants and the Slashed Locometal have no recipe, "blocking 90% of the mod".
**Error:** No recipe shown in JEI for those items.
**Root cause:** Not a pack regression. Nothing in kubejs, config or the datapacks touches the railways namespace. Steam 'n' Rails ships exactly one craftable entry point per family (`railways:link_and_pin`, `railways:copycat_headstock_link_and_pin`, `railways:wooden_headstock_link_and_pin`); every other variant is reached with the mod's own radial cycle menu, driven by the `railways:deco_couplers`, `railways:copycat_headstocks` and `railways:wooden_headstocks` item tags. Slashed Locometal is craftable through the stonecutter (iron block -> riveted locometal -> slashed locometal, tag `railways:palettes/cycle_groups/base`). The mod does carry a hint tooltip (`block.railways.generic_radial.tooltip.summary`) but it sits behind the Create "hold Shift" detail panel, so players never see it.
**Fix:** Added always-visible bilingual tooltips on the 19 concerned items in `kubejs/client_scripts/arcadia_item_tooltips.js` pointing at the ALT cycle menu, with strings in the 7 arcadia lang files.
**Prevention:** Before treating a "no recipe" report as a pack bug, grep the mod namespace across kubejs/config/datapacks first, then check the mod jar for an in-jar recipe. Absence in both means the mod obtains the item another way (cycle menu, wrench, in-world interaction), not that the pack removed it.

## [2026-08-01] — Bug #228: Create trains not moving with wide / narrow / comically large bogeys

**Context:** Player report: only the "standard" bogey style drives a train; Wide, Narrow, Narrow Double Scotch Yoke and Comically Large produce a train that does not move properly.
**Error:** Train assembles but the affected bogeys do not drive it.
**Root cause:** Not a pack bug. Steam 'n' Rails splits track into four gauges (narrow, standard, wide, monorail) and each bogey style is bound to one gauge through `CRBogeyStyles.STYLES_FOR_GAUGES`. The four styles listed are narrow-gauge or wide-gauge only, so they need `railways:track_*_narrow` / `railways:track_*_wide` rails, not the standard `create:track`. Nothing in the pack touches the railways namespace (full grep: only two sound_physics entries). Aggravating factor: the French bogey menu names lose the gauge information, "Comically Large" becomes "Comiquement grand" with no gauge mention, and "Wide"/"Narrow" become "Large"/"Étroit" which read as a size, not a track gauge.
**Fix:** Added `kubejs/assets/railways/lang/fr_fr.json` overriding the 4 gauge-specific style names and the 6 gauge-specific bogey block names so the required gauge appears in the label (also fixed the "Bougie" typo on the large platform bogey).
**Prevention:** The in-game bogey menu already prints "Compatible avec :" plus the gauge; when a train report mentions a specific bogey style, check the gauge binding first. Narrow and wide tracks are crafted by sequenced assembly like standard tracks, from narrow/wide slabs variants.

## [2026-08-07 10:19] — Twilight Forest boss spawners never spawned their boss (ticket #226)

**Context:** No Twilight Forest boss would spawn. The boss spawner blocks were present in their structures but stayed in place indefinitely, in singleplayer on a fresh world as well as on every official server. Manually placed spawners behaved the same. `/summon twilightforest:naga` worked normally.
**Error:** No exception, no log output. Tracing `FinalizeSpawnEvent` and `EntityJoinLevelEvent` showed a single Naga spawner firing `finalizeMobSpawn` 2394 times with `reason=SPAWNER` while the entity never once reached `EntityJoinLevelEvent`.
**Root cause:** The tag-independent spawner safety-net in `kubejs/server_scripts/tags/item_entity_tags.js` cancelled `FinalizeSpawnEvent` for any entity in `ARCADIA_FARM_BLACKLIST` spawned with reason `SPAWNER`, and all ten Twilight Forest bosses are on that list. NeoForge has two paths into that event: a real spawner block goes through `EventHooks.finalizeMobSpawnSpawner`, which attaches the originating block entity, while blocks that implement their own spawning call plain `EventHooks.finalizeMobSpawn`, which attaches nothing. `BossSpawnerBlockEntity.spawnMyBoss` takes the second path yet still reports reason `SPAWNER`, so the safety-net could not tell a farmable spawner from a one-shot structure spawner. `TwilightForest` discards the return of `finalizeMobSpawn` and calls `addFreshEntity` regardless; that call returned false, so `spawnMyBoss` returned false, the spawner block was never destroyed and the whole sequence retried every tick.
**Fix:** Added `if (event.getSpawner().isWorldgen()) return;` before the blacklist check. `WrappedSpawner.isWorldgen()` is true exactly when neither a spawner block entity nor a spawner entity is attached to the event, which is the structure-spawner case. Real spawner blocks are still filtered, and placing a banned egg into a spawner is still blocked by the `apothic_spawners:blacklisted_from_spawners` tag.
**Prevention:** `MobSpawnType.SPAWNER` alone does not mean "came from a spawner block". Any gate keyed on that reason must also inspect `FinalizeSpawnEvent.getSpawner()`, otherwise it silently swallows every mod that hand-rolls its own spawning. Also note that cancelling `FinalizeSpawnEvent` does not by itself stop a spawn: `ServerLevel.addFreshEntity` never consults `Mob#isSpawnCancelled` (only `WorldGenRegion` and `EntityType.create(ServerLevel, Consumer, BlockPos, MobSpawnType, boolean, boolean)` do), so the effect depends entirely on whether the caller honours the result.

## [2026-08-07] — Menu serveurs: raw translation keys shown instead of text (ticket #232)

**Context:** Launching the pack from the launcher, the multiplayer hub and official-servers screens displayed raw keys (`arcadia.servers.menu.title`, `arcadia.servers.official`, `arcadia.servers.section.eu`, `arcadia.servers.back`...) instead of localized text. Hardcoded button labels ("Serveur 1", "Serveur Event") rendered fine, which is what made it look like a partial visual glitch rather than a localization failure.
**Error:** No error or warning. FancyMenu resolves those strings through `{"placeholder":"local","values":{"key":"..."}}` and falls back to printing the key verbatim when the key is absent from the loaded language.
**Root cause:** The 34 menu and server-screen strings existed only in `resourcepacks/ArcadiaLanguages`, a resource pack the player has to enable. `config/defaultoptions/options.txt` — the Default Options template applied on a fresh install — does not list `file/ArcadiaLanguages` in `resourcePacks`, so on a clean launcher install the pack is never enabled and none of those keys resolve. A resource pack cannot enable itself; `pack.mcmeta` has no such mechanism.
**Fix:** Merged the 34 keys into `kubejs/assets/arcadia/lang/{en_us,fr_fr}.json`. The KubeJS virtual resource pack is always loaded and cannot be toggled off by the player, so the strings no longer depend on any user action. Verified beforehand that a JSON round-trip reproduced the existing files byte for byte (no reformatting churn) and that no key collided with a different value. The other five languages (de, es, it, pt, ru) never had these strings even in the resource pack; they fall back to en_us, which is now always present.
**Prevention:** Never put UI strings in a resource pack the player must enable. Anything the menus render belongs in `kubejs/assets/<namespace>/lang/`, which ships loaded. `resourcepacks/ArcadiaLanguages` is now fully redundant (all of its keys, and its `rbf_quest.png`, also live under `kubejs/assets/arcadia/`) and can be dropped from the export.
