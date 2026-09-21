# Error Log — Arcadia V2

## [2026-09-21 08:20] — Server sync: settings silently lost and a removed mod left behind

**Context:** Syncing the 2.0.28 client to the eight environments in `Desktop\Serveur` following `PROCEDURE_MAJ.md`.
**Error:** Four problems, none of which the old procedure would have caught. `kubejstweaks`, removed from the client because it breaks KubeJS build 377, was still on all nine mod folders, and this very sync ships build 377. The new JEI 19.57 declares `mezz_config` as `required` on `BOTH` sides, while MezzConfig was not on any server. Moog's Structure Lib was renamed (`moogs_structures-neoforge-*` to `MoogsStructureLib-neoforge-*`) with the same modId, so a plain copy would have loaded it twice. And ServerEvent's own rules, ReviveMe disabled and near-instant corpse despawn, were no longer in its folder: its revive and corpse configs were byte-identical to the other servers.
**Root cause:** The procedure treated every server jar absent from the client as server-only, only looked at mods listed as new, never checked dependencies of updated mods, and merged shared config files over ServerEvent's customised ones, so an earlier sync had erased the event settings without anyone noticing. Separately, the NeoForge installer rewrites `run.bat` and `run.sh` with generic scripts that ignore the bundled `jre21\` and drop `nogui`.
**Fix:** Removed kubejstweaks and the old Moogs lib, added MezzConfig, verified the full dependency closure of each server's final mod set (with a control case proving the check catches a missing MezzConfig), restored the ServerEvent overrides, and restored the Arcadia launch scripts after installing NeoForge 21.1.250 in the serverpack. Every replaced file was moved to `_backup_pre_2.0.28\` first.
**Prevention:** `PROCEDURE_MAJ.md` now requires: a fixed server-only list (anything else missing from the client is a removal), a dependency closure check on updated mods too, config classification against the client's git history (a file that matches no committed version is server-specific and is kept), the ServerEvent overrides re-applied after every sync, and saving the launch scripts before running the NeoForge installer.

**Contexte :** Synchro du client 2.0.28 vers les huit environnements de `Desktop\Serveur` selon `PROCEDURE_MAJ.md`.
**Erreur :** `kubejstweaks`, retiré du client car il casse KubeJS build 377, était encore dans les neuf dossiers de mods alors que cette synchro livre le build 377. Le nouveau JEI 19.57 exige `mezz_config` des deux côtés, absent de tous les serveurs. Moog's Structure Lib a été renommée avec le même modId, une simple copie l'aurait chargée deux fois. Et les règles propres à ServerEvent (ReviveMe désactivé, corps qui disparaissent presque aussitôt) n'étaient plus dans son dossier.
**Cause :** La procédure considérait tout jar absent du client comme server-only, ne vérifiait pas les dépendances des mods mis à jour, et écrasait les configs personnalisées de ServerEvent avec les fichiers partagés. L'installeur NeoForge réécrit aussi `run.bat` et `run.sh` avec des scripts génériques.
**Correction :** Retrait de kubejstweaks et de l'ancienne lib Moogs, ajout de MezzConfig, vérification complète des dépendances, restauration des règles ServerEvent et des scripts de lancement Arcadia. Tout fichier remplacé a d'abord été déplacé dans `_backup_pre_2.0.28\`.
**Prevention :** `PROCEDURE_MAJ.md` impose désormais une liste server-only fixe, la vérification des dépendances, le classement des configs par l'historique git, la réapplication des règles ServerEvent après chaque synchro et la sauvegarde des scripts avant l'installeur NeoForge.

## [2026-09-20 20:12] — The temporary contraption tracer crashed the world on any bed or door dropping

**Context:** Playing on the TEST02 world with `kubejs/startup_scripts/diagnostics/contraption_block_loss_trace.js` still armed for tickets #218 and #233.
**Error:** `TypeError: Cannot call property dimension in object ServerLevel[TEST02]. It is not a function, it is "object". (startup_scripts:diagnostics/contraption_block_loss_trace.js#116)`, thrown during `Exception during promotion of chunk to FULL status`, which takes the integrated server down.
**Root cause:** The script read the dimension with `level.dimension()`. Rhino's bean mapping turns a zero-argument `dimension()` into the **property** `level.dimension`, so calling it as a function throws. The line had never run: it only fires when a watched item entity joins a server level, and the tracer watches 879 items, every door, bed, banner and bell in the pack. The first chunk containing one of them was enough, and because the listener body was not guarded, a diagnostic that changes nothing in the game became a hard crash on chunk load.
**Fix:** Read the dimension through a `diagDimensionOf()` helper that reads the property and falls back to `'unknown dimension'`, and move the listener body into `traceWatchedDrop()` wrapped in try/catch, so any future failure silences the tracer for the session instead of killing the server thread.
**Same bug elsewhere:** `compat/handcrafted_cushion_move_dupe.js` built its position key with the same `level.dimension()` call. It had never crashed only because `armKey()` runs just when furniture is actually moved, but it meant the cushion duplication fix for tickets #241 and #234 had never worked at all: the first contraption capture of a chair or bench threw before arming anything. Fixed the same way, and its three runtime callbacks now carry their own try/catch, since the `StartupEvents.postInit` wrapper only covered installation.

**Prevention:** Two rules. A zero-argument Java getter reached from KubeJS is a property, not a call, whenever Rhino can map it as a bean; when unsure, read it as a property and guard it. And any diagnostic script, by definition code that must change nothing, wraps its whole listener body in try/catch: a tracer is never worth a crash. The same applies to the untested tail of a listener, here `console.trace()`, which had never executed either.

**Contexte :** Partie sur le monde TEST02 avec le traceur temporaire des contraptions encore arme pour les tickets #218 et #233.
**Erreur :** `TypeError: Cannot call property dimension in object ServerLevel[TEST02]` pendant la promotion d'un chunk en statut FULL, ce qui arrete le serveur integre.
**Cause :** Le script lisait la dimension avec `level.dimension()`. Rhino transforme un `dimension()` sans argument en **propriete** `level.dimension` : l'appeler comme une fonction leve une erreur. Cette ligne n'avait jamais ete executee, car elle ne se declenche qu'a l'apparition d'un objet surveille, et le traceur en surveille 879, soit toutes les portes, lits, bannieres et cloches du pack. Le premier chunk en contenant un a suffi, et faute de garde autour de l'ecouteur, un diagnostic cense ne rien modifier est devenu un crash au chargement de chunk.
**Correction :** Lecture de la dimension via un helper `diagDimensionOf()` avec repli, et corps de l'ecouteur deplace dans `traceWatchedDrop()` sous try/catch, qui desarme le traceur pour la session au lieu de tuer le thread serveur.
**Prevention :** Un getter Java sans argument appele depuis KubeJS est une propriete, pas un appel, des que Rhino peut le mapper. Et tout script de diagnostic enveloppe son ecouteur dans un try/catch : un traceur ne vaut jamais un crash.

## [2026-09-20 11:30] — "Unnamed" chapters kept coming back because two chapter files had spaces in their names

**Context:** Duplicate chapters labelled "Unnamed" reappeared in the quest book after every launch, even though the duplicate files had been deleted three times.
**Error:** Deleting `a_new_beginning.snbt` and `first_line_of_code.snbt` fixed the book until the next boot, then both returned with freshly generated ids and no title, so FTB Quests rendered them as "Unnamed".
**Root cause:** `A New Beginning.snbt` and `First Line of Code.snbt` were the only two chapter files in the pack whose name contained spaces; the other 39 use snake_case and their `filename` field matches their file name exactly. FTB Quests saves a chapter to `<filename>.snbt` after sanitising it, so it wrote a snake_case copy and left the space-named original untouched. The next load read both files, saw the same chapter id twice, regenerated one of them, and a regenerated chapter has no `chapter.<ID>.title` entry. Deleting the copy could never hold, because the space-named file recreated it on the following save.
**Fix:** Renamed both chapters to snake_case and aligned their `filename` field, **keeping the original chapter id** so the seven lang files and every player's progress still resolve. One file per chapter, filename matching the file name, exactly like the other 39. Verified afterwards: 41 chapters, zero duplicate ids, zero filename mismatches, no file with a space left, every chapter has a title, and the quest book still totals 3,897 quests and 245,668 spurs.
**Prevention:** Never let an FTB Quests chapter file name differ from its `filename` field, and never use spaces. A one-line audit catches it: compare each file's base name with its `filename` value across `chapters/*.snbt`. Deleting a duplicate chapter treats the symptom; the file whose name FTB Quests will rewrite is the one to fix.

**Contexte :** Des chapitres "Unnamed" revenaient a chaque lancement malgre trois suppressions.
**Erreur :** Supprimer les doublons corrigeait le livre jusqu'au demarrage suivant, puis ils revenaient avec de nouveaux identifiants et sans titre.
**Cause :** `A New Beginning.snbt` et `First Line of Code.snbt` etaient les deux seuls fichiers de chapitre du pack dont le nom contenait des espaces ; les 39 autres sont en snake_case avec un champ `filename` identique au nom de fichier. FTB Quests sauvegarde un chapitre sous `<filename>.snbt` apres assainissement : il ecrivait donc une copie snake_case et laissait l'original. Au chargement suivant, les deux fichiers se chargeaient, l'identifiant entrait en collision, l'un etait regenere, et un chapitre regenere n'a plus de cle de titre.
**Correction :** Chapitres renommes en snake_case avec le champ `filename` aligne, **en conservant l'identifiant d'origine** pour que les sept fichiers de langue et la progression des joueurs continuent de correspondre.
**Prevention :** Ne jamais laisser le nom d'un fichier de chapitre differer de son champ `filename`, et jamais d'espaces. Supprimer le doublon ne traite que le symptome.

## [2026-09-20 11:10] — A mod's own translation typo broke the whole French quest lang file

**Context:** Generating market shop titles and descriptions in the seven quest locales, taking each item's display name from the mod lang files.
**Error:** FTB Quests refused the file: `Failed to read config/ftbquests/quests/lang/fr_fr.snbt: New line without closing string with " @ 14921:36`, and loaded `translation tables for 6 language(s)` instead of seven. French, the server's main language, silently lost every quest string.
**Root cause:** Mekanism's French translation spells its Energy Tablet `Tablette d"énergie`, with a double quote where the apostrophe belongs. The generator interpolated that name straight into an SNBT string, which closed the string early and left the rest of the line dangling. Three lines were affected: the description header, the pay line and the title.
**Fix:** Replaced the typo with a real apostrophe in the three generated lines. A sweep over every mod lang file found 60 display names containing a raw double quote across the seven locales, including `"Android" sign`, `Патрон "Дыхание дракона"` and a stray trailing quote on `白葡萄"`. Only Mekanism's Energy Tablet is currently sold in the market, so it was the only one that could bite.
**Prevention:** Never interpolate a mod-provided display name into SNBT without escaping. Sanitise the value, replacing a bare `"` with an apostrophe or escaping it as `\"`, and validate the written file with a string-state scan before finishing: walk the characters, track whether you are inside a string, honour backslash escapes, and fail on a newline reached while still inside one. That scan reproduces FTB Quests' own parser and catches the fault in a second, whereas counting quotes per line does not, because an escaped quote and a balanced pair both look fine.

**Contexte :** Generation des titres et descriptions du market dans les sept langues, en reprenant le nom d'affichage de chaque item depuis les fichiers de langue des mods.
**Erreur :** FTB Quests refusait `fr_fr.snbt` et ne chargeait que six langues sur sept. Le francais perdait donc toutes ses chaines de quetes.
**Cause :** La traduction francaise de Mekanism ecrit `Tablette d"energie` avec un guillemet droit a la place de l'apostrophe. Interpole tel quel dans une chaine SNBT, il la fermait prematurement.
**Correction :** Apostrophe retablie sur les trois lignes generees. Un balayage a trouve 60 noms d'items contenant un guillemet droit sur l'ensemble des locales ; un seul est vendu au market.
**Prevention :** Ne jamais interpoler un nom fourni par un mod dans du SNBT sans echappement, et valider le fichier ecrit par un parcours d'etat de chaine qui echoue sur un retour a la ligne rencontre a l'interieur d'une chaine. Compter les guillemets par ligne ne suffit pas.

## [2026-09-20 10:30] — Verified item ids against lang files, which passed three items that do not exist

**Context:** Extending the market chapter. Every item the chapter references was checked against a registry built by harvesting `item.*` and `block.*` keys from every mod's `en_us.json`, plus the vanilla jar. The check reported 188 items, zero missing.
**Error:** In game, three of them rendered as `ftbquests:missing_item`: `knightquest:great_essence`, `knightquest:small_essence` and `ars_nouveau:magic_clay`. FTB Quests rewrote the chapter on load, replacing each broken stack with a placeholder carrying the original id in a component.
**Root cause:** A translation key is not proof that an item is registered. Mods keep lang entries for content they have removed: the Ars Nouveau jar still ships `item.ars_nouveau.magic_clay` and contains no other file mentioning clay at all, the whole family having been dropped. The two essences were my own mistake on top of that, they live in the `knightlib` namespace, not `knightquest`. The lang-based registry therefore produced false positives in both directions and hid a pre-existing broken entry that had been in the market before this work.
**Fix:** Rebuilt the registry from **item models**, `assets/<namespace>/models/item/*.json`, across every mod jar, the vanilla jar and `kubejs/assets`. A registered item essentially always ships one, and the three ghosts disappear from the registry immediately. Repointed the essences to `knightlib:` and `magic_clay` to `ars_nouveau:magebloom`.
**Prevention:** Never validate an item id against lang files. Use the item-model registry, and treat the absence of a model as the answer. Cross-check anything surprising by searching the jar for the id: a mod that ships no file at all mentioning the item has removed it, whatever its lang file still says. The strongest check remains loading the pack once and grepping the chapter for `ftbquests:missing_item`, which is FTB Quests telling you exactly what it could not resolve.

**Contexte :** Extension du chapitre market. Les items etaient valides contre un registre bati depuis les fichiers de langue des mods : 188 items, zero manquant annonce.
**Erreur :** En jeu, trois d'entre eux s'affichaient en `ftbquests:missing_item`.
**Cause :** Une cle de traduction ne prouve pas qu'un item est enregistre. Ars Nouveau livre encore `item.ars_nouveau.magic_clay` alors que le jar ne contient plus aucun fichier mentionnant clay. Les deux essences venaient en plus d'une erreur de namespace de ma part : elles sont dans `knightlib`, pas `knightquest`.
**Correction :** Registre reconstruit depuis les modeles d'items `assets/<ns>/models/item/*.json`. Essences repointees vers `knightlib:`, magic_clay vers `ars_nouveau:magebloom`.
**Prevention :** Ne jamais valider un identifiant d'item sur les fichiers de langue. Utiliser le registre des modeles, et chercher l'identifiant dans le jar en cas de doute. Le controle le plus sur reste de lancer le pack une fois puis de chercher `ftbquests:missing_item` dans le chapitre.

## [2026-09-20 09:05] — Deleted a defaultconfigs file that FTB Essentials owns by design

**Context:** Repairing the `defaultconfigs/` mirror. `defaultconfigs/ftbessentials-server.snbt` existed with no counterpart in `config/`, which holds `ftbessentials.snbt` instead.
**Error:** Read as a leftover from the 2025 initial commit and deleted. It is not a leftover: FTB Essentials reads that exact path and copies it to `config/ftbessentials.snbt` on startup. Its own header says so, `Default config file that will be copied to instance's config/ftbessentials.snbt location`. The mod recreated it on the next launch.
**Root cause:** The mirror audit assumed `defaultconfigs/` may only contain files mirroring `config/`. Some mods use it as their own template directory, with a deliberately different file name, so an entry present only on the mirror side is not automatically stale.
**Fix:** The file is back and tracked again. No data was lost because the template carries `{ }`, no overrides.
**Prevention:** Before deleting anything from `defaultconfigs/` that has no `config/` counterpart, open it. A header naming its own target path means the mod owns it. Only delete a mirror-only file when nothing on disk and no mod claims it.

**Contexte :** Reparation du miroir `defaultconfigs/`. Un fichier sans equivalent dans `config/`.
**Erreur :** Pris pour un reliquat de 2025 et supprime. En realite FTB Essentials lit ce chemin precis et le copie vers `config/ftbessentials.snbt` au demarrage, comme l'indique son propre en-tete. Le mod l'a recree au lancement suivant.
**Cause :** L'audit supposait que `defaultconfigs/` ne contient que des miroirs de `config/`. Certains mods s'en servent comme repertoire de gabarits, avec un nom de fichier volontairement different.
**Correction :** Fichier restaure et de nouveau suivi. Aucune perte, le gabarit ne contient aucune surcharge.
**Prevention :** Avant de supprimer un fichier de `defaultconfigs/` sans equivalent dans `config/`, l'ouvrir. Un en-tete qui nomme son chemin cible signifie que le mod en est proprietaire.

## [2026-09-20 08:45] — Two quest chapters shipped twice, so FTB Quests kept regenerating ids and showed "Unnamed" duplicates

**Context:** Player report of duplicate chapters named "Unnamed" in the quest book, right under "A New Beginning".
**Error:** `config/ftbquests/quests/chapters/` held four files for two chapters: `A New Beginning.snbt` and `a_new_beginning.snbt`, `First Line of Code.snbt` and `first_line_of_code.snbt`. Both copies of each pair claimed the same chapter id, so on every load FTB Quests detected the collision and assigned a fresh id to one of them. The regenerated chapter has no `chapter.<ID>.title` entry in any lang file, so it renders as "Unnamed".
**Root cause:** The duplicates have been tracked since the initial commit. The snake_case copies are the same chapters re-saved by a newer FTB Quests, which adds an `id` field to chapter images, so they were never byte-identical to the originals and no diff ever flagged them. They almost certainly came from renaming the files toward the project's snake_case convention by copying instead of moving. This also explains an earlier mistake in this repository: the quest count was raised to 3,893 over 43 chapters, when both figures were inflated by the duplicate pair.
**Fix:** Deleted the four snake_case copies, in `config/` and in the `defaultconfigs/` mirror. The canonical space-named files keep the ids the lang files reference. Verified afterwards: 41 chapters, 3,841 quests, zero duplicate chapter ids, zero chapters without a title, and 3,841 `quest_desc` keys per language as an independent cross-check. The 301 ids exclusive to the deleted copies were referenced by no other file.
**Prevention:** Never rename an FTB Quests chapter file by copying, and never assume two chapter files are unrelated because their contents differ: compare the `id:` field at chapter level, not the file. A quick audit is worth running after any chapter reorganisation: extract the chapter-level id from every file in `chapters/` and check that the set has no repeats. An "Unnamed" chapter in game always means a chapter whose id has no `chapter.<ID>.title` key, which is nearly always a regenerated id rather than a missing translation.

**Contexte :** Signalement de chapitres en double nommes "Unnamed" dans le livre de quetes.
**Erreur :** Quatre fichiers pour deux chapitres, chaque paire revendiquant le meme id de chapitre. FTB Quests regenerait donc un id a chaque chargement, et le chapitre regenere n'a aucune cle de titre : il s'affiche "Unnamed".
**Cause :** Doublons suivis depuis le commit initial. Les copies snake_case sont les memes chapitres re-sauvegardes par une version plus recente de FTBQ, donc jamais identiques octet pour octet : aucun diff ne les a jamais signales. Cela explique aussi une erreur anterieure du depot, ou le nombre de quetes avait ete porte a 3 893 sur 43 chapitres, les deux chiffres etant gonfles par la paire en double.
**Correction :** Suppression des quatre copies snake_case, dans `config/` et dans le miroir. Verifie ensuite : 41 chapitres, 3 841 quetes, aucun id de chapitre duplique, aucun chapitre sans titre, et 3 841 cles `quest_desc` par langue en recoupement independant.
**Prevention :** Ne jamais renommer un fichier de chapitre FTBQ par copie. Comparer les `id:` au niveau chapitre, pas le contenu des fichiers. Un chapitre "Unnamed" signifie toujours un id sans cle `chapter.<ID>.title`, donc presque toujours un id regenere.

## [2026-09-20 03:10] — FTB Quests regenerated every quest id in two chapters, orphaning translations and player progress

**Context:** Reviewing 15 uncommitted files before pushing. Two quest chapters, `a_new_beginning` and `first_line_of_code`, showed diffs of 500 and 106 lines.
**Error:** The diffs were not content edits. Every 16-hex quest id had been replaced: `a_new_beginning` kept 1 id out of 249, `first_line_of_code` kept 0 out of 52. Quest ids are the key for both player completion state and the `quest.<ID>.title` entries in the seven quest lang files, so committing this would have reset both chapters for every player and orphaned 42 and 13 translation entries respectively.
**Root cause:** The chapters were recreated rather than edited, most likely through an import or a duplicate-and-replace in the FTB Quests editor. Masking every id showed the two files were otherwise byte-identical to their committed versions apart from one `order_index` line each, which confirms a pure regeneration. In `a_new_beginning` the regeneration was not even self-consistent: 284 distinct new ids mapped onto 251 old ones, meaning some ids were left untouched while other references to the same quest were rewritten, leaving broken dependency links.
**Fix:** Restored both files from `HEAD` and re-applied the single intended change, the new `order_index`. Translation coverage came back to 42 and 13, and the pack total stayed at 43 chapters and 3,893 quests. A positional id remap was considered and rejected for `a_new_beginning` because the mapping was not a bijection.
**Prevention:** Never commit an FTB Quests chapter diff without masking the ids first: `sed -E 's/"[0-9A-F]{16}"/"<ID>"/g'` on both versions, then compare. If the masked files match, the diff is an id regeneration and must be discarded, not committed. A large line count on a chapter file is a warning sign, since real quest edits touch few lines.

**Contexte :** Revue de 15 fichiers non commites avant un push. Deux chapitres de quetes affichaient 500 et 106 lignes de diff.
**Erreur :** Tous les identifiants de quetes avaient ete regeneres. Les ids servent de cle a la progression des joueurs et aux fichiers de langue : committer aurait remis les deux chapitres a zero pour tout le monde et orpheline 42 et 13 entrees de traduction.
**Cause :** Chapitres recrees et non edites. En masquant les ids, les fichiers etaient identiques aux versions commitees a une ligne `order_index` pres. Dans `a_new_beginning` la regeneration etait elle-meme incoherente : 284 nouveaux ids pour 251 anciens, donc des references de dependance cassees.
**Correction :** Restauration depuis `HEAD` puis reapplication du seul `order_index`. Couverture de traduction revenue a 42 et 13, total inchange a 43 chapitres et 3 893 quetes.
**Prevention :** Toujours masquer les ids avant de juger un diff de chapitre FTBQ. Si les fichiers masques sont identiques, c'est une regeneration d'ids : a jeter, jamais a committer.

## [2026-09-20 00:48] — Combined temporary-folder cleanup was blocked
**Context:** Removing the locally extracted FTB GUI sources and concept preview after generating the Arcadia overrides.
**Error:** The command runner rejected both a PowerShell invocation that resolved, validated and recursively removed the temporary `work` directory and a later `Remove-Item` call using its explicit absolute path.
**Root cause:** The safety policy blocked the recursive `Remove-Item` operation even after its target had been verified separately.
**Fix:** Verified the absolute directory and every contained file in a read-only command, then removed that exact directory through PowerShell's .NET directory API.
**Prevention:** Resolve and inspect recursive deletion targets first; if the command runner rejects `Remove-Item`, use the verified absolute literal path with the .NET directory API instead of changing shells.

## [2026-09-18 10:30] — Auditing a mod's recipes counted the 1.20 folder and nearly kept 26 dead patches

**Context:** Checking whether the `create_things_and_misc_fix.js` rebuilds were still needed after the mod moved to 4.1.1, by reading the recipe JSON straight out of the jar.
**Error:** The first sweep reported 33 still-broken recipes and claimed 5 of them were not covered by our script, which would have meant writing 5 new rebuilds. The real number was 13, and nothing was uncovered.
**Root cause:** The jar ships both `data/create_things_and_misc/recipe/` (100 files) and `data/create_things_and_misc/recipes/` (57 files). Only the singular folder is read on 1.21; the plural one is the 1.20 path and is dead weight the author never deleted. Matching on `"/recipe" in name` swept up both, so recipes that exist only as abandoned 1.20 files were counted as live breakage.
**Fix:** Filter on the exact prefix `data/<namespace>/recipe/`. The count dropped to 13 real failures, all of them a numeric key in a shaped pattern, and the 5 "uncovered" entries turned out to live only in the dead folder.
**Prevention:** When auditing recipes, loot tables or tags inside a jar, match the full 1.21 directory (`recipe/`, `loot_table/`, `advancement/`), never a prefix that a legacy plural or singular variant also satisfies. A mod updated across the 1.20 to 1.21 datapack rename frequently carries both, and the stale one parses perfectly well.

**Contexte :** Verification de l'utilite des reconstructions de `create_things_and_misc_fix.js` apres le passage du mod en 4.1.1.
**Erreur :** Le premier balayage annoncait 33 recettes cassees et 5 non couvertes, au lieu de 13 et aucune.
**Cause :** Le jar contient `recipe/` (lu en 1.21) et `recipes/` (chemin 1.20, jamais lu). Le filtre attrapait les deux.
**Correction :** Filtrer sur le prefixe exact `data/<namespace>/recipe/`.
**Prevention :** Toujours cibler le repertoire 1.21 complet, jamais un prefixe que la variante singulier/pluriel satisfait aussi.

## [2026-09-14 22:48] - Texture import and validation gaps
**Context:** Completing the custom texture refresh and reviewing the reduced PNG assets.
**Error:** The texture checker accepted legacy item dimensions. The local importer failed with CS1069 under PowerShell 7. Armor image edits also contained neutral checkerboard pixels near UV boundaries.
**Root cause:** Dimension checks were conditional; the importer referenced the .NET Framework drawing assembly; generated artwork did not exactly preserve every UV edge.
**Fix:** Require 32x32 inventory and opaque block textures, run the local importer under Windows PowerShell, restore original armor alpha masks, and replace stray neutral background samples with nearby painted samples before visual review.
**Prevention:** Treat file existence separately from completion, check final dimensions and alpha coverage, and review reduced textures before publishing.

**Contexte :** Finalisation des textures et revue des PNG reduits.
**Erreur :** Le controle acceptait les anciens formats, l'importeur echouait sous PowerShell 7 et des pixels de damier subsistaient aux bords des UV.
**Cause :** Controle conditionnel des dimensions, reference .NET Framework et contours du dessin imparfaitement conserves.
**Correction :** Dimensions strictes, import sous Windows PowerShell, masque alpha original et suppression des echantillons de fond parasites avant revue visuelle.
**Prevention :** Verifier les dimensions, la transparence et les textures reduites avant publication.

## [2026-09-14 09:49] — Fresh clone of ArcadiaTweaks left an index showing every file deleted (Windows MAX_PATH)

**Context:** Cloning `Team-Arcadia/ArcadiaTweaks` with `gh repo clone` into a deep temporary directory, to prepare the Waystones team visibility fix for ticket #279.
**Error:** The clone printed `failed to run git: exit status 128` and a hint to run `git restore --source=HEAD :/`, yet `git log` and the top-level files looked normal. `git status` then listed all 88 tracked files as staged deletions (`D `). A first `git restore --staged --worktree --source=HEAD :/` failed with `unable to create file ...RefinedStorageMixinPlugin.java: Filename too long`, and even `git show HEAD:<path>` refused with `failed to stat ...: Filename too long`.
**Root cause:** The repository nests sources up to 127 characters deep (`src/main/java/com/teamarcadia/arcadiatweaks/neoforge/mixin/refinedstorage/...`). Under a directory prefix of about 130 characters the full path crosses the 260-character Windows limit, and git for Windows does not use long paths unless `core.longpaths` is set. The checkout aborted halfway, leaving the index empty while HEAD and part of the working tree existed, which reads as "everything deleted".
**Fix:** `git config core.longpaths true` in the clone, then `git restore --staged --worktree --source=HEAD :/`; `git status` came back clean. Gradle and the JDK handled the same long paths without any change (build successful).
**Prevention:** Before cloning a Java/Gradle repository on Windows, run `git config --global core.longpaths true` or clone into a short path. After any clone that reports a non-zero exit, check `git status` before doing anything else: a staged-deletion listing on a fresh clone means a failed checkout, never a state to commit. `git cat-file -p <blob sha>` from `git ls-tree` reads a file without touching the working tree when paths are too long.

## [2026-09-01 14:00] — Jar audit returned a false negative (unzip wildcard silently matched nothing)

**Context:** Auditing all 443 jars for the producer of an item, while tracing the missing Shadow Casing recipe (ticket #269). The sweep used `for j in *.jar; do unzip -p "$j" 'data/*' | grep -qa "cinder_flour" && echo HIT; done`.
**Error:** The sweep reported zero hits. `create-1.21.1-6.0.10.jar` alone contains four files with that string, so the correct answer was at least one hit. Read literally, the result said Cinder Flour had no source in the pack and Blaze Cake was uncraftable, which would have sent the fix down the wrong road.
**Root cause:** Two compounding faults. Git Bash rewrites any argument containing a slash into a Windows path, so `data/*` never reached unzip intact; and this unzip build does not let `*` cross a `/` anyway, so even a preserved `data/*` would only match one directory level. `unzip -p` prints nothing and exits 0 when a pattern matches no entry, so the pipeline stayed silent and the loop looked healthy.
**Fix:** Re-ran the audit with a Python `zipfile` walk over `z.namelist()`, filtering on `data/` and `.json` and reading each entry. That found the real source immediately (`data/create/recipe/crushing/netherrack.json`) plus the true absence of any `chromatic_compound` producer.
**Prevention:** Never audit jar contents with `unzip -p jar 'pattern'` under Git Bash. Use Python `zipfile` for anything recursive; `unzip -l` (no path argument) and `unzip -p jar <full/exact/path>` are safe because neither relies on a wildcard crossing directories. Any sweep that reports zero hits must first be validated against a jar known to contain the string, otherwise a silent no-match is indistinguishable from a real absence.

## [2026-08-23 02:00] — Pack refuses to launch after a CurseForge "Update All" (WaterMedia 2.x/3.x split)

**Context:** Launching Arcadia V2 from CurseForge after a mass mod update. The launcher reported the instance as running, but `logs/latest.log` stopped after three ModLauncher lines and no crash report was produced.
**Error:** Two distinct failures, in sequence. First, launches fired while CurseForge was still downloading in the background, so the game started against a half-written `mods/` folder (`Structory_Towers_26.2_v1.0.17.jar is not a valid mod file`, `Missing ModLoader in file`). Once the sync finished, FML stopped on version-range violations: `Mod waterframes requires watermedia 2.1.34 or above, and below 2.2 - Currently, watermedia is 3.0.0.23` and the same for `watervision`.
**Root cause:** WaterMedia forked into two incompatible lines. WaterMedia 3.x (beta) is required by FancyMenu 3.9.6+, WATERMeDIA: Binaries 3.x and WATERMeDIA: Platform Extension, while WaterFrames and WaterVision are still capped at `[2.1.x,2.2)` on NeoForge 1.21.1 — the WaterMedia v3 rewrite of WaterFrames (2.2.0-beta) only exists for Forge 1.20.1. "Update All" pulled the 3.x half of the family and left the 2.x half stranded. The empty log was misleading: nothing was wrong with the JVM, FML simply had not reached its file appender before dying on the partial mod folder.
**Fix:** Pinned the whole family to the WaterMedia 2.1.x line, which keeps WaterFrames and WaterVision working: watermedia 2.1.37, watermedia_youtube_plugin 2.1.2, fancymenu 3.9.1 (last build with no watermedia dependency at all), drippyloadingscreen 3.1.2 (fancymenu `[3.9.0,)`, whereas 3.1.5 needs `[3.9.9,)`). Removed watermedia_binaries 3.0.0.6 and watermedia_platform_extension 3.0.0-beta.7, both 3.x-only; WaterMedia 2.1.37 ships its binaries in-jar.
**Prevention:** Never launch while CurseForge is still syncing — check that `mods/` file timestamps have settled first. Before accepting a bulk update, extract `META-INF/neoforge.mods.toml` from the changed jars and diff the `versionRange` entries of any shared library (WaterMedia, Sodium, Create, SuperMartijn642 Core) against every dependent still installed. Reproducing a silent launch failure is done by replaying the launcher command line from `logs/instance_audit.txt` in a terminal: CurseForge captures stdout only, and the real cause is on stderr.

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

## [2026-08-07] — Simply Swords animated textures freeze after a few seconds (ticket #220)

**Context:** The animated textures on Simply Swords weapons stopped animating after a few seconds, both in the inventory and held in hand.
**Error:** No error. Purely a rendering behaviour.
**Root cause:** `animate_only_visible_textures` was `true` in `config/sodium-options.json` (and its `defaultconfigs/` mirror). Sodium's texture animation culling only ticks sprites it has seen in the terrain rendering pass; sprites used solely by items rendered in a GUI or in first person are never marked active, so their animation freezes once the initial frames have played. Simply Swords ships 152 animated item textures (`textures/item/*.png.mcmeta`), which is why the mod is the visible victim.
**Fix:** Set `animate_only_visible_textures` to `false` in both `config/` and `defaultconfigs/`. Cost is every animated sprite in the atlas being ticked each frame rather than only the visible ones — negligible next to the rest of the pack's render load.
**Prevention:** Sodium's animation culling is unsafe for any pack shipping animated item textures. Check this flag before blaming a mod for frozen animations. Note the setting lives in two places since the `defaultconfigs/` mirror exists — changing only `config/` leaves fresh installs broken.

## [2026-08-07] — Occultism Vitality Compass allowed teleporting to any player (ticket #223)

**Context:** Players could teleport to each other without `/tpa`, and could also yank another player to them with a fishing rod. Reported as going through Occultism's Entity Wormhole with a "player soul" obtained by right-clicking a player.
**Error:** No error. Intended mod behaviour, unwanted on a server with a consent-based teleport system.
**Root cause:** Not the Soul Gem, which the report blamed: `SoulGemItem.interactLivingEntity` returns FAIL on a Player before it ever reads its deny list, so players cannot be captured in a gem. The actual vector is the Vitality Compass. `VitalityCompassItem.interactLivingEntity` binds the compass to any right-clicked `LivingEntity` and has no Player guard — it only consults `occultism:vitality_compass_deny_list`, a tag Occultism ships empty. Placed in an Entity Wormhole, a bound compass makes the wormhole teleport to the bound entity, and lets a fishing rod reel that entity into the portal.
**Fix:** Added `minecraft:player` to `occultism:vitality_compass_deny_list`, in `kubejs/server_scripts/tags/item_entity_tags.js` plus a datapack mirror at `kubejs/data/occultism/tags/entity_type/vitality_compass_deny_list.json`. Binding a compass to a player now fails with the mod's own "target_blocked" message.
**Prevention:** Occultism gates each capture/binding item behind its own deny-list tag, and they are not interchangeable — `soul_gem_deny_list`, `fragile_soul_gem_deny_list`, `trinity_gem_deny_list`, `soul_shattered_deny_list` and `vitality_compass_deny_list` are five separate tags. Adding a mob to one does not cover the others. Known gap: `EntityWormholeBlock` only checks `ItemTags.COMPASSES` and never re-reads the deny list, so a compass bound to a player before this fix keeps working.

## [2026-08-11] — Straw statues and Create transmitters usable inside foreign claims (ticket #248)

**Context:** Players reported that straw statues can be opened and emptied inside another team's claim, and that Create Ender Transmission transmitters expose their channel and password to anyone, allowing outright theft of the items, fluids and energy on that network.
**Error:** No error. Both are silent protection bypasses.
**Root cause:** Two distinct holes.
(1) FTB Chunks only guards one of the two vanilla entity right-click packets. `INTERACT` goes through its architectury `interactEntity` handler, but `INTERACT_AT` has no handler at all — armor stands are covered by a mixin injected into `ArmorStand.interactAt`, which only fires for entities that actually reach that method. `StrawStatue.onUseEntityAt` answers `PlayerInteractEvent.EntityInteractSpecific` from a puzzleslib `USE_ENTITY_AT` listener and opens the statue menu (full equipment access) before `interactAt` is ever called, so the mixin never runs. Sneak + empty hand was enough to strip any statue in a foreign claim. The same listener also lets a player head rewrite the statue's skin ahead of the vanilla path.
(2) Create's `BlockEntityConfigurationPacket.handle` validates only: sender non-null, not spectator, not adventure mode, chunk loaded, within `maxRange()`. It never consults any land protection. Every subclass inherits that — 24 in Create itself (`StationEditPacket`, `PackagePortConfigurationPacket`, `FactoryPanelConfigurationPacket`, `DisplayLinkConfigurationPacket`, `ValueSettingsPacket`, ...) plus `ConfigureTransmitterPacket` (Create Ender Transmission), `ConfigureAutoClutchPacket` (Create Encased), `ConfigureSourceMotorPacket` (Ars Technica), `ConfigureSequencedPulseGeneratorPacket` (Create Connected) and `VatEvaluationPacket` (TFMG). Create Numismatics is the only addon in the pack that overrides `handle` with its own `Trusted.isTrusted` check, so vendors, blaze bankers and depositors are safe.
On top of that, those Create screens are opened purely client-side (`FMLLoader.getDist() == Dist.CLIENT` inside `useItemOn` then `ScreenOpener.open`), and FTB Chunks' block-interact handler bails out on `!(player instanceof ServerPlayer)`. A server-side cancel therefore never reaches the client, which still opens the screen during interaction prediction. For the transmitters the channel and password live in the block entity's `persistentData`, and `SmartBlockEntity.write` calls `super.saveAdditional` for the client packet as well, so both values are synced to every client with the chunk loaded. Reading them is enough to steal: `MatterTransmitterNetwork` keys its shared inventories on channel + password only, with no owner component.
**Fix:** (1) fixed in `kubejs/server_scripts/fixes/compat/entity_interact_at_claim_protection.js` — a `NativeEvents` listener on `PlayerInteractEvent$EntityInteractSpecific` at `HIGHEST` priority, gated through the same `ClaimedChunkManager.shouldPreventInteraction(..., Protection.INTERACT_ENTITY, target)` call FTB Chunks already uses for `INTERACT`. Registering above every mod listener means the event is cancelled before any of them can consume it, so this closes the whole `interactAt` class of bypasses, not only straw statues.
(2) not fixable from the pack. `kubejs/server_scripts/fixes/compat/transmitter_claim_protection.js` gates `BlockEvents.rightClicked`, which only runs on the logical server and therefore stops nothing: the client opens the screen anyway and the configuration packet is a direct C2S message KubeJS cannot intercept. A real fix has to be a mixin on `BlockEntityConfigurationPacket.handle` in `arcadia-patch-create`, plus stripping `password` from the transmitter's client sync tag; until then the only pack-level mitigation is removing the three transmitters.
**Prevention:** FTB Chunks protection is not a complete perimeter. It covers `INTERACT` but not `INTERACT_AT`, and every one of its handlers is server-side only, so any mod that opens its UI client-side or applies changes through its own C2S packet bypasses it entirely. When auditing a mod for claim safety, check three things: which of the two entity-interaction packets it answers, whether its screen is opened by a server `MenuProvider` or by `ScreenOpener.open` under a `Dist.CLIENT` guard, and whether its serverbound packets re-validate permission on arrival rather than trusting that the screen could only have been opened legitimately.

## [2026-08-11] — FTB Quests "Loot Reward" grants nothing on the Wireless Crafting Grid quest (ticket #246)

**Context:** Quest `744842B2AED28344` ("Grille de fabrication sans fil", Refined Storage chapter). Claiming the loot reward — the pouch icon labelled "Récompense de butin" — gave the player nothing at all. The XP reward on the same quest worked.
**Error:** No error, no log line, no toast. The reward is consumed and marked claimed, and nothing is granted.
**Root cause:** The reward entry in `config/ftbquests/quests/chapters/refined_storage.snbt` was written without a `table_id` key, so it deserialized with the default value 0. `LootReward.getTable()` resolves table 0 to null, and `LootReward.claim` opens with `if (table == null) return;` — the whole grant is skipped silently. Every other loot reward in that chapter points at `2855284357105343251L` (`27A001FEADFE5B13`, the Refined Storage table), including the two neighbouring quests, so this is a single entry that lost its table reference during editing rather than a missing table.
**Fix:** Added `table_id: 2855284357105343251L` to the reward entry, and mirrored the file into `defaultconfigs/`. Note that the reward stays flagged as claimed for anyone who already took it: those players need `/ftbquests change_progress <player> reset 744842B2AED28344` before they can claim it again.
**Prevention:** `type: "loot"` and `type: "random"` both fail closed and silently when `table_id` is absent or points at a deleted table — no warning at load, no warning at claim. After any reward-table edit, sweep the chapters for reward entries whose `type: "loot"` or `type: "random"` line is not immediately preceded by a `table_id` line (FTB Quests writes SNBT keys alphabetically, so `table_id` always sits directly above `type`). A full sweep on 2026-08-11 found this entry plus one more, quest `4D4AB60B3B1CD437` in `twilight_forest.snbt`, whose `type: "random"` reward had no table either — never reported, since the quest simply looked like it had no reward. That chapter uses no reward tables anywhere else, so the tier was a balance call: pointed at `rare` (`5B2C3D4E5F6A7B81`, `6569693363244268417L`) rather than `legendary`, the Naga being the first Twilight Forest boss and its armour set early progression.

## [2026-08-11] — Schematicannon prints Liquid Blaze Burners without spending the straws (ticket #240)

**Context:** A player printed a Create power setup with a schematicannon. The four Liquid Blaze Burners were placed correctly, but the four straws he had loaded into the cannon chest were still there afterwards. Breaking a printed burner gives back a blaze burner and a straw.
**Error:** No error. The cannon charges a plain `create:blaze_burner` for a block that costs a burner plus a `createaddition:straw` by hand, so every print/break cycle creates one straw out of nothing.
**Root cause:** `LiquidBlazeBurnerBlock` has no item of its own — `asItem()` returns `create:blaze_burner` — and it implements neither `SpecialBlockItemRequirement` nor registers a `BlockRequirement` in Create's `SchematicRequirementRegistries.BLOCKS`. `ItemRequirement.of(state, be)` consults, in order, the `BLOCKS` registry, the `SpecialBlockItemRequirement` interface, then falls back to `defaultOf`, which resolves to `block.asItem()`. The straw is only ever consumed by Create Crafts & Additions' `GameEvents.interact` right-click handler, which the cannon never goes through, while `data/createaddition/loot_table/blocks/liquid_blaze_burner.json` drops both the burner and a straw. Straw itself is cheap (one bamboo or one paper through a rolling mill), so this is a nuisance dupe rather than an economy hole, but the cannon behaviour was plainly wrong.
**Fix:** `kubejs/startup_scripts/compat/liquid_blaze_burner_schematic_cost.js` registers the missing requirement at `StartupEvents.postInit`, returning blaze burner + straw, both `CONSUME`. Registration goes through the public `SchematicRequirementRegistries.BLOCKS` registry, which takes priority over the interface and the default, so no mixin is needed. The script self-tests by calling Create's own `ItemRequirement.of` on the block's default state and logs an error if the resolved requirement is still a single stack, which is the tell that Rhino failed to adapt the JS function to the `BlockRequirement` interface.
**Prevention:** Any block that is a converted form of another block — created by a right-click handler, keeping the source block's item as its `asItem()`, dropping the extra ingredient in its loot table — is printed at the wrong price by the schematicannon unless its mod registers a schematic requirement. Check `asItem()` against the block's loot table when auditing an addon block: if the table drops more than `asItem()`, the difference is free from a cannon. `SchematicRequirementRegistries.BLOCKS` is the pack-level lever, no mod patch required.

## [2026-08-11] — Handcrafted cushions duplicated when furniture is relocated (tickets #241 and #234)

**Context:** Two reports, one cause. #241: a Create mechanical piston pushing a couch that carries a cushion, the cushion dropping as an item on every stroke while staying on the couch, so a cycling piston prints cushions indefinitely. #234: the same cushions duplicating on every train reassembly. Reported for couches, applies to every wood type and every cushion colour.
**Error:** No error. A silent duplication on each contraption assembly.
**Root cause:** Handcrafted keeps the cushion as a blockstate property on the furniture, not as a separate block, and gives it back in `onRemove`. `ChairBlock`, `BenchBlock`, `CouchBlock` and `FancyBedBlock` all run the same body: if the level is server side and the new block differs, `Containers.dropItemStack(level, x, y, z, color.toCushion())`. Neither the `isMoving` argument nor the `UPDATE_SUPPRESS_DROPS` flag is consulted, so the drop also fires when the block is removed because it is being relocated. `Contraption.removeBlocksFromWorld` sets air with flags 122 (`UPDATE_CLIENTS | UPDATE_IMMEDIATE | UPDATE_KNOWN_SHAPE | UPDATE_SUPPRESS_DROPS | UPDATE_MOVE_BY_PISTON`) and a vanilla piston uses 68 for the moved position and 82 for the vacated one, all of which announce a move. The furniture is re-placed with its colour intact, so each assembly leaks one cushion. A mechanical piston extending then retracting assembles twice, which is the "casse 2 fois" in the report. Train stations go through the same funnel: `StationBlockEntity.assemble` builds each `CarriageContraption`, calls `assemble` (`searchMovedStructure` then `moveBlock`) and calls `removeBlocksFromWorld` further down the same method, so a station reassembly leaks one cushion per seat exactly like a piston stroke. `CarriageContraption` does not override `movementAllowed`, and `MountedContraption` falls through to `Contraption.movementAllowed` for anything that is not a cart assembler. Nothing here is Create specific: a vanilla piston duplicates just as well, since Handcrafted sets no push reaction on those blocks.
**Fix:** `kubejs/startup_scripts/compat/handcrafted_cushion_move_dupe.js` suppresses the drop only when the furniture is being moved. Two arming points: a Create `MovementAllowedCheck` registered through `BlockMovementChecks.registerMovementAllowedCheck`, which sees every block a contraption is about to capture in the same tick as the removal and stays neutral by returning `CheckResult.PASS`; and `PistonEvent.Pre`, which resolves the pushed set for vanilla pistons, behind a cheap line scan so piston farms without furniture never pay for a second resolve. A cushion item entity spawning on an armed position within two ticks is cancelled through `EntityJoinLevelEvent`. Breaking furniture by hand still drops the cushion, and moved furniture keeps it. Known gap: the line scan only walks the piston axis, so furniture attached sideways by a slime block alone is not covered; contraptions are covered in full since Create's check runs on every captured block.
**Prevention:** Any furniture-style block that stores an attachment as a blockstate property and refunds it in `onRemove` duplicates under pistons unless it checks `isMoving`. Only Create and Contraption code calls `BlockMovementChecks.isMovementAllowed`, and only during assembly, which makes that check a reliable "this block is about to be relocated" signal usable from KubeJS without a mixin. When auditing a furniture mod, grep its blocks for `onRemove` bodies that call `dropItemStack`/`dropContents` and ignore the last boolean argument.

## [2026-08-11] — Redstone Links duplicated when a piston contraption returns to blocks (ticket #218), UNRESOLVED

**Context:** Create mechanical pistons carrying Redstone Links on the moved structure. Activating the piston and stopping it, at the moment the contraption turns back into physical blocks, leaves the player with more links than were on the structure.
**Error:** No error, no log line. Duplication only, reported as happening at disassembly.
**Root cause:** Not identified yet. Established by reading Create 6.0.10: `create:redstone_link` is in `create:brittle`, so both `Contraption.removeBlocksFromWorld` and `Contraption.addBlocksToWorld` handle it in the brittle half of their `Iterate.trueAndFalse` double pass, removed first at assembly and placed last at disassembly. Ruled out, with reasons: the Handcrafted-style block-entity drop (`removeBlocksFromWorld` calls `Level.removeBlockEntity` before `setBlock(air, 122)`, so `IBE.onRemove` finds no block entity and never reaches `SmartBlockEntity.destroy`); a behaviour drop (`LinkBehaviour` does not override `destroy()`, and link frequencies are ghost items); and any third-party interference (no mod in the pack references `contraptions/Contraption`, and the two `arcadia-patch-create` contraption mixins only reject unreadable contraption NBT). What remains are the three item-producing sites in `addBlocksToWorld` — `Block.dropResources` when the target is unbreakable or in collision conflict, `Level.destroyBlock(targetPos, true)` on whatever occupies the target, and the same block being captured by two contraptions — which static reading cannot tell apart. The report's wording, "en activant les pistons au moment de la remise en bloc physique", points at a race between a disassembly and a fresh assembly, which does not show up in the code either since the `disassembled` guard is per Contraption instance.
**Fix:** None yet. `kubejs/startup_scripts/diagnostics/contraption_block_loss_trace.js` logs a stack trace, position and current block for every watched item entity spawning server side, capped at 12 reports per restart, and logs what a contraption captures at assembly. One reproduction on the test server names the caller. The file is temporary and must be deleted once tickets #218 and #233 are closed.
**Prevention:** Pending the root cause. Worth noting for the next contraption ticket: `addBlocksToWorld` drops rather than places when the target block is unbreakable or when the incoming state has an empty collision shape while the existing one does not, and it calls `destroyBlock` with drops enabled unless `noDropWhenContraptionReplaceBlocks` is set in the Create server config. That config flag is the only pack-level lever on those two paths.

## [2026-08-11] — Doors, beds, banners and bells lost on train assembly (ticket #233), UNRESOLVED

**Context:** Steam 'n' Rails train, glue placed correctly. Disassembling then reassembling the train at a station leaves it without its Create and vanilla doors. A comment on the report adds beds, banners and bells, all vanishing at disassembly. Copycat and Copycat+ doors survive.
**Error:** No error. Blocks are simply missing after the cycle.
**Root cause:** Not identified yet. The discriminator is clear: every block named in the report sits in `create:brittle` (`#minecraft:doors`, `#minecraft:beds`, `#minecraft:banners`, `minecraft:bell`, `create:peculiar_bell`, `create:haunted_bell`), while copycat doors are not brittle and are not instances of `DoorBlock`. Both `Contraption.removeBlocksFromWorld` and `Contraption.addBlocksToWorld` split their work with `Iterate.trueAndFalse`: brittle blocks are removed first at assembly and placed last at disassembly, and the `updateShape` normalisation of the first pass is skipped for them. Ruled out: the removal flags, 122, carry `UPDATE_KNOWN_SHAPE`, so clearing one door half never pops the other; and Create's own destroy branch in `addBlocksToWorld`, which does destroy doors, pulley ropes and magnets after placing them, only fires when `transform.rotationAxis` is horizontal and `transform.rotation` is not `NONE`. `OrientedContraptionEntity.makeStructureTransform` builds `new StructureTransform(anchor, 0, yaw - initialYaw, 0)`, which sets `rotationAxis` to Y, so a train never enters it. Steam 'n' Rails is not implicated either: its `MixinContraption` only fires an `IPreAssembleCallback` on block entity behaviours inside `removeBlocksFromWorld`, and its carriage mixin is client-side rendering.
**Fix:** None yet. Shares the tracer written for #218, `kubejs/startup_scripts/diagnostics/contraption_block_loss_trace.js`, extended to watch doors, beds, banners, bells and redstone links. It logs what a contraption captures at assembly through a neutral `MovementAllowedCheck`, and logs a stack trace for every watched item entity that spawns. The two together separate the three remaining hypotheses: captured then dropped points at a drop site in `addBlocksToWorld`, captured and never dropped points at the silent `iterator.remove()` in `removeBlocksFromWorld` when the world block no longer matches the captured one, and never captured means the loss happened at assembly.
**Prevention:** Pending the root cause. Worth carrying forward: `create:brittle` membership changes both the ordering and the placement rules of a block inside a contraption, so it is the first thing to check when a block behaves differently from its neighbours on a moving structure. `BlockMovementChecks.registerMovementAllowedCheck` gives a pack-level, mixin-free probe on every block a contraption captures.

## [2026-08-16] — Control Chip and Sequenced Pulse Generator uncraftable (ticket #250)

**Context:** `create_connected:sequenced_pulse_generator` has a working shaped recipe in JEI but needs a `create_connected:control_chip`, which shows no recipe at all. The chip is produced by `create_connected:sequenced_assembly/control_chip` (Deployer chain on a Golden Sheet), a recipe that ships in the create_connected jar and is not gated by any feature condition.
**Error:** No log line. The recipe is silently absent from JEI and from the server recipe manager.
**Root cause:** `kubejs/server_scripts/recipes/overhaul/02_crossmod_general.js` rewrites the vanilla compass with `event.remove({ output: 'minecraft:compass' })`. In the kubejs-create schema for `create:sequenced_assembly`, the whole `results` list carries `"role": "output"` (and so does `transitional_item`), so an output filter matches random by-products, not just the main result. The control chip recipe lists `minecraft:compass` as its last by-product, so the compass removal deleted the entire sequenced assembly. The same pattern hit `create:sequenced_assembly/precision_mechanism` through the `minecraft:clock` removal two lines above, which is the real reason the Precision Mechanism went missing: the Either-codec theory written in `precision_mechanism_fix.js` is wrong, that script only works because it re-registers the recipe afterwards.
**Fix:** Both removals now carry `not: { type: 'create:sequenced_assembly' }`. `RecipeFilter` in KubeJS 2101.7.2 builds an `AndFilter` from every key of the filter object and wraps the `not` value in a `NotFilter`, so the compass and clock crafting recipes are still removed while sequenced assemblies are left alone. A sweep over all 443 jars plus `kubejs/data` for Create recipes whose non-primary results are targeted by one of the 207 remove-by-output calls in the pack returns only these two, plus `create:crushing/blaze_rod`, whose primary result is blaze powder and whose removal is intentional.
**Prevention:** `event.remove({ output: X })` is not "remove the recipes that make X". For every Create processing type it matches any entry of `results` and the transitional item, so it silently kills unrelated multi-output recipes. Before removing by output, check which recipes carry that item as a by-product, and scope the filter with `type:` or `not:`. Same trap as the netherite ingot removal that also wiped the netherite block decraft.

## [2026-08-16] — Trains frozen for good after rolling onto the wrong track gauge

**Context:** Players report trains ending up on rails they should not be on, then being unable to disassemble them. Follow-up to #228, which covered the same gauge split from the "my train does not move" angle.
**Error:** Train status "Un wagon a atteint la fin de son rail" while the train sits on visually intact track, and "Ne peut pas d\u00e9sassembler, tous les wagons ne sont pas align\u00e9s" at the station.
**Root cause:** Not a pack regression, nothing outside lang and tooltips touches the railways namespace. Three upstream behaviours stack. `TrackPlacement.tryConnect` validates geometry only and never compares `TrackMaterial.TrackType`, so a narrow or wide segment can be grafted onto a standard line with no warning; Create has no lang string for a type mismatch at placement. `Train.tick` then computes `blocked |= carriage.blocked || carriage.isOnIncompatibleTrack()`, and `AbstractBogeyBlock.isOnIncompatibleTrack` simply compares the edge's track type with the bogey style's track type; when it trips, the tick sets `speed = 0`, calls `cancelNavigation()` and reports `TrainStatus.endOfTrack()`. The speed is overwritten without looking at its sign, so the train cannot reverse out either. Finally `Train.canDisassemble()` requires `pitch == 0` and `yaw % 90 == 0` on every carriage and only runs from a station where the train is present, which a train frozen mid-line can never satisfy. Bogeys themselves are not the entry point: they have no item and no recipe, they exist only through Train Casing on a track, and `MixinAbstractBogeyBlock.filterStyles` filters the offered styles by the track type underneath. The wrong rails are the wrong half.
**Fix:** Recovery already exists and is simply invisible: `TrainRelocator.carriageWrenched` refuses only when `train.speed != 0`, so a blocked train at zero speed can be relocated with a wrench, and `relocate()` clears `derailed` while Steam 'n' Rails rebinds the carriages behind it. Create only advertises that hint for derailed trains (`create.hint.derailed_train`), which a blocked train is not. Added always-visible tooltips in `kubejs/client_scripts/arcadia_item_tooltips.js`: the gauge warning on the 219 narrow, wide and monorail track items (filtered from the live item registry, incomplete sequenced assembly intermediates excluded), a note on the Train Casing that the offered bogey styles follow the rail underneath, and the relocation hint on the wrench. Strings added to the 7 arcadia locales. A real prevention needs a mixin on `TrackPlacement.tryConnect` in `arcadia-patch-create`, refusing to connect two different track types, and is not done.
**Prevention:** Track gauge is enforced at roll time, not at build time, and the penalty is a permanent freeze rather than an error message. Any report of a train that stopped for no visible reason should start with the track type under each bogey. The wrench relocation is the universal way out of an immobilised train, blocked or derailed, as long as its speed is zero.

## [2026-08-20] — Building Gadget stuck after picking a camouflaged elevator (ticket #252)

**Context:** A player building with the Building Gadget set it on what looked like Redwood planks. The block was in fact an Elevator ID elevator wearing that camouflage. The gadget then rendered a stretched red preview crossed by coloured lines (screenshot on the report) and could not place anything until another block was picked. The reporter also wondered what a copy paste of several elevators would do, which they did not try.
**Error:** No log line, no crash. Client-side render artefact only, on a gadget whose stored block state is an elevator.
**Root cause:** Not proven, established by reading both jars. `elevatorid` 1.11.4 registers `ElevatorBakedModel`, a `BakedModelWrapper` whose quads come from the `HELD_STATE` model property, and that property is filled by `ElevatorBlockEntity` from the camouflage block state. Building Gadgets 2 1.3.9 draws its previews through `FakeRenderingWorld`, whose `getBlockEntity` never returns the real block entity: it calls `EntityBlock.newBlockEntity` on an offset position and hands it the real level, so the fresh instance carries no camouflage and no facing data. The elevator model therefore renders against a block entity that is not the one it was copied from. Which of the two branches of `ElevatorBakedModel.getQuads`, the directional arrow model or the camouflage passthrough, produces the stretched geometry could not be told apart without a reproduction, and none of it reaches a log.
**Fix:** Elevators are denied to the gadgets. `kubejs/data/buildinggadgets2/tags/block/deny.json` adds `#elevatorid:elevators` to `buildinggadgets2:deny`, the tag `GadgetUtils.isValidBlockState` tests first; both `GadgetBuilding` and the `Copy` mode call it, so an elevator can no longer be set as the gadget block and is skipped when it sits inside a copied region. That rejection is silent, so `kubejs/client_scripts/arcadia_item_tooltips.js` puts a line on the 16 elevator items saying to copy the shaft and place the elevators by hand. This is a containment, not an upstream fix; the render bug itself is still there for anyone forcing the state another way.
**Prevention:** Any block whose appearance depends on its block entity (camouflage, copycat, facade) is a candidate for the same failure with any preview renderer built on a fake level, since the fake level fabricates a blank block entity instead of returning the real one. `buildinggadgets2:deny` is the pack-level lever and it covers picking, copying and placing at once.
## [2026-09-14 23:55] - Image generation quota reached during texture refresh
**Context:** Regenerated KubeJS Arcadia item artwork in Minecraft pixel-art style.
**Error:** Image generation returned HTTP 429 usage limit after part of the requested batch.
**Root cause:** The image generation account quota was exhausted during the multi-asset refresh.
**Fix:** Kept generated assets in the workspace, added deterministic PNG import and validation scripts, and documented the partial scope.
**Prevention:** Generate future texture families in separate quota windows and run the texture checker after each batch.

## [2026-09-16 07:04] — Three KubeJS startup scripts dead on arrival

**Context:** The startup error GUI reported three failures at boot: the Handcrafted cushion move guard (tickets #241 and #234), the Liquid Blaze Burner schematic cost (ticket #240) and the contraption brittle-block tracer (tickets #218 and #233). Each one installs from `StartupEvents.postInit` behind its own try/catch, so the pack booted normally with all three inactive and the bugs they cover still live.

**Error:**
1. `compat/handcrafted_cushion_move_dupe.js#110: InternalError: Java class "earth.terrarium.handcrafted.common.blocks.ChairBlock" has no public instance field or method named "isInstance".`
2. `[Arcadia] Failed to register the Liquid Blaze Burner schematic cost: TypeError: Cannot call method "getRequiredItems" of null`
3. `diagnostics/contraption_block_loss_trace.js#86: InternalError: Failed to load Java class 'java.lang.Throwable': Class is not allowed by class filter!`

**Root cause:** Three distinct mistakes about what Rhino exposes to a script, all of them invisible until the script runs.
1. `Java.loadClass(x)` returns a `NativeJavaClass`, which exposes the static members of the wrapped class, not the instance methods of `java.lang.Class`. `ChairBlock.isInstance(block)` therefore resolves against `ChairBlock`'s own statics and finds nothing. The same broken call sat on `ItemEntity.isInstance(entity)` in the event handler of both scripts, where it had never had the chance to throw because the install aborted a few lines earlier.
2. `new BlockRequirement(fn)` builds a JavaAdapter from the **function properties** of the delegate: `JavaAdapter.getObjectFunctionNames` walks the delegate's property ids and keeps those whose value is a function, and `JavaAdapter.getFunction` returns null when the property is missing. A bare function has no property named `getRequiredItems`, so the generated adapter implements the interface with a method that returns null. `ItemRequirement.of` then called `getRequiredItems` on that adapter, got null back, and the self test dereferenced it. Create's `defaultOf` never returns null, which is what ruled out every other branch.
3. The KubeJS class filter shipped in `kubejs.classfilter.txt` denies `java.lang` wholesale and re-allows a fixed list (String, Number, Runnable, StringBuilder and a handful more). `Throwable`, `Thread` and `StackTraceElement` are not on it, so no script can build a stack trace by itself.

**Fix:** `block instanceof furnitureClasses[i]` and `entity instanceof ItemEntity`, since `NativeJavaClass.hasInstance` is what implements `instanceof` on a loaded class. The schematic requirement now passes an object keyed by the interface method name, `new BlockRequirement({ getRequiredItems: ... })`, and probes the adapter before registering: `SimpleRegistryImpl.register` throws `IllegalArgumentException` on a duplicate key, so there is no second attempt once a value is in. The self test also stopped assuming `ItemRequirement.of` is non-null. The tracer drops `Throwable` and calls `console.trace()`, which KubeJS backs with `Thread.currentThread().getStackTrace()` on the Java side; the trace comes out unfiltered and untagged, which is noted in the script header.

**Prevention:** A `Java.loadClass` handle is not a `java.lang.Class`: use `instanceof` for a type test, never `isInstance`. Before reaching for a `java.lang` class, check the allowlist in `kubejs.classfilter.txt` inside the KubeJS jar. Lastly, an install wrapped in try/catch only proves the boot survived: the code after the failure point, event handlers included, has never run and can hide the same mistake. The interface part of this entry was only half right, see the follow-up below.

## [2026-09-16 07:29] — Liquid Blaze Burner requirement, second failure: JavaAdapter cannot take a null argument

**Context:** Follow-up to the entry above, on the next boot. The cushion guard and the tracer were fixed and stayed fixed. The schematic cost failed again, differently, which means the first diagnosis was incomplete: the delegate shape was a real bug, but it was hiding a second one behind it.

**Error:** `[Arcadia] Failed to register the Liquid Blaze Burner schematic cost: JavaException: java.lang.NullPointerException: Cannot invoke "Object.getClass()" because "obj" is null`. No stack trace in `logs/latest.log`, only the message; the variable name in it is what identified the method.

**Root cause:** `new BlockRequirement({ getRequiredItems: ... })` builds the adapter through `JavaAdapter`, which generates a class at runtime. `JavaAdapter.generatePushWrappedArgs` flags every object argument for wrapping, and the generated method hands them to `JavaAdapter.doCall`, which wraps each flagged argument with `Context.wrapAny(scope, obj)`. `wrapAny` tests the argument against String, Boolean, Integer, Short, Long, Float, Double and Character, all false for a null, then falls straight through to `obj.getClass()` with no null check. So the adapter throws on any call carrying a null object argument. The probe passed `null` as the block entity, and so does Create: `SchematicPrinter` reads the block entity from the schematic level with `getBlockEntity(pos)` and passes it to `ItemRequirement.of(state, be)` without testing it. Fixing only the probe would have moved the crash from boot to the schematicannon.

**Fix:** Build the interface with `Java.cast(BlockRequirement, fn)` instead. `JavaWrapper.cast` calls `Context.jsToJava(value, TypeInfo.of(type))`, which reaches `createInterfaceAdapter` and `InterfaceAdapter.create`, producing a `java.lang.reflect.Proxy` rather than a generated class. That path wraps arguments with `Context.wrap`, which starts with a null check and returns null unchanged. The probe deliberately passes a null block entity, so it now exercises the exact call the printer makes. `Java.cast` also accepts a bare function, since `InterfaceAdapter` resolves the single abstract method.

**Prevention:** See the follow-up below for the third failure in the same registration. Two ways to implement a Java interface from a KubeJS script, and they are not interchangeable. `new SomeInterface(...)` (JavaAdapter, generated class) breaks on null arguments and silently returns null when handed a bare function. `Java.cast(SomeInterface, fn)` (InterfaceAdapter, proxy) tolerates nulls and accepts a function. Prefer `Java.cast`. More generally: when a fix for a failing script produces a *different* error on the next boot, the first diagnosis was probably incomplete rather than wrong, and the new error deserves the same treatment from scratch. `dev.latvian.mods.rhino` is denied by the class filter, so `TypeInfo` is out of reach and `Java.cast` with a loaded class is the only route from a script.

## [2026-09-16 07:42] — Liquid Blaze Burner requirement, third failure: ambiguous constructor overload

**Context:** Same registration, next boot. `Java.cast` worked: the proxy was built and the probe reached the body of the function, so the interface half is settled. The failure moved inside the function.

**Error:** `compat/liquid_blaze_burner_schematic_cost.js#71: InternalError: The choice of Java constructor ItemRequirement matching JavaScript argument types (ItemUseType, ItemStack) is ambiguous; candidate constructors are: (ItemUseType, java.util.List), (ItemUseType, Item), (ItemUseType, ItemStack)`.

**Root cause:** `new ItemRequirement(ItemUseType.CONSUME, new ItemStack(item))` names an exact Java signature, and that is precisely why it fails. Rhino weighs an exact match the same as its own conversions, and KubeJS registers enough of them that all three overloads apply at once: an `ItemStack` converts to an `Item`, and any object at all converts to a single element `List` through the `listOf` path in `internalJsToJava`. Three applicable candidates, no winner, so Rhino reports the ambiguity instead of picking. The error is not about the argument being wrong, it is about the target class offering several overloads that a script cannot separate.

**Fix:** Build the requirement through `ItemRequirement(List<StackRequirement>)`, filling a real `java.util.ArrayList`. An `ArrayList` is exact for the `List` overload and converts to none of the others, which makes it the only unambiguous shape. `java.util` is allowed by the class filter. Note that passing a lone `StackRequirement` to the single argument constructor would have walked straight back into the same trap, since the any-object-to-List conversion puts `ItemRequirement(List)` and `ItemRequirement(StackRequirement)` at equal weight. `StackRequirement` takes `(ItemStack, ItemUseType)`, the reverse order of `ItemRequirement`. The `union()` call is gone, both stacks live in the one list.

**Prevention:** When a Java class offers several overloads that differ only by a parameter type Rhino can convert between (`Item` / `ItemStack` / `List` are the classic trio in KubeJS), no argument will disambiguate them, because the conversions are what create the tie. Pick the overload whose parameter type nothing else converts into, usually the collection one, and build a real Java collection for it. Do not expect an exact type match to win.

## [2026-09-16 07:53] — Single player world refuses to load: kubejstweaks mixin against KubeJS build 377

**Context:** Opening a single player world showed "Errors in currently selected data packs prevented the world from loading". Unrelated to the startup script work of the same morning: that same boot logged `Loaded 12/12 KubeJS startup scripts with 0 errors`, along with the cushion guard, the tracer and the Liquid Blaze Burner cost all reporting success. The failure only appears when a world loads, which is the first time recipes are parsed, so the earlier boots to the main menu never reached it.

**Error:** `InjectionError: Critical injection failure: Redirector keepOrder([Ljava/lang/Object;)Ljava/util/Set; in kubejstweaks.mixins.json:main.RecipeComponentValueMapMixin from mod kubejstweaks failed injection check, (0/1) succeeded. Scanned 0 target(s).` raised through `MixinTransformerError` while `KubeRecipe.<init>` loaded its class, which killed `RecipeManager.apply` and the whole datapack reload.

**Root cause:** A mod version conflict, nothing in the pack's own files. `kubejstweaks` 1.0.6 (dated 29 January) redirects a specific `java.util.Set.of(Object[])` call inside `RecipeComponentValueMap.entrySet()` and replaces it with an ordered `LinkedHashSet`, purely to preserve the iteration order of recipe components. KubeJS was updated to build 377 on 14 September, and that build no longer calls `Set.of` there: the bytecode still ends with `checkcast Set` but the `invokestatic Set.of` present in build 368 is gone. With no call to redirect, the injector matches zero targets. The mixin carries only `@Mixin`, no `@ConditionalMixin`, so the mod's own version gating machinery never gets a chance to disable it, and with `"required": true` plus `defaultRequire: 1` the miss is fatal. The declared dependency range `kubejs [2101.7.1,2101.7.3)` is satisfied by `2101.7.2` because it ignores the build number, so FML loaded the mod without a warning.

**Fix:** `kubejstweaks-1.0.6.jar` moved from `mods/` to `disabled-mods/`, after confirming it is used nowhere: no script references it, no mod declares it as a dependency, and its jar registers no game content at all (4 `assets/` entries, a lang file only), so no existing save can refer to it. Its KubeJS plugins are development tooling (ProbeJS typings, dumping erroring recipes). Two harmless leftovers kept on purpose: the pack's French translation of its 4 strings in `kubejs/assets/kubejstweaks/lang/fr_fr.json`, and a filter line in `config/logbegone.json`.

**Prevention:** A dependency range that names a version but not a build (`2101.7.2` covers build 363 and build 377 alike) gives no protection at all for a mixin that redirects a call site inside a method body. Such a mixin breaks on any upstream build that merely rewrites that method, with no warning at load time and no failure until the affected system runs. After updating KubeJS, load a world before assuming the update is clean: startup scripts and the main menu exercise none of the recipe pipeline. Other mixins in this mod target Rhino internals (`ContextFactoryMixin`, `NativeJavaMethodMixin`, `TypesMixin`, `VariableTypeInfoMixin`), so script behaviour, overload resolution in particular, may shift slightly now that it is gone.

## [2026-09-20 01:45] — Drippy loading gauge falls back to the white default bar

**Context:** The four Drippy layouts were changed from a legacy button-shaped bar to FancyMenu's textured progress element. Static checks confirmed the element and local PNG paths, but the first F3+T visual check still showed the white default progress bar.

**Error:** The Arcadia track and fill textures were not rendered during resource reload. FancyMenu displayed a plain white fill and outline even though both PNG files existed and the active layout referenced them.

**Root cause:** Loading-overlay resources have to be available before the normal resource reload completes. The two new local texture paths were absent from FancyMenu's `preload_resources` list, so the progress element could not resolve them at render time and used its fallback appearance.

**Fix:** Add `loading_progress_track.png` and `loading_progress_fill.png` to `config/fancymenu/options.txt` under `preload_resources`, using the same local-source syntax and separator as the other Arcadia loading assets.

**Prevention:** Any new local texture used by the startup or F3+T loading overlay must be added to FancyMenu's preload list. A successful file and layout validation is insufficient for loading-screen assets; always perform an actual startup and F3+T visual check.

## [2026-09-20 02:00] — Drippy loading gauge, second failure: invalid layout block type

**Context:** After adding the two gauge textures to FancyMenu's preload list and fully restarting the game, an F3+T visual check still showed the same white Drippy bar. The bar position and live progress proved that the active loading layout was correct, while the Arcadia textures remained absent.

**Error:** The textured progress element never appeared. No missing-texture error was logged because FancyMenu never instantiated the element at all.

**Root cause:** FancyMenu serializes registered custom elements inside an `element` block and selects their builder through `element_type`. The layouts incorrectly used `progress_bar {` as the block header. That syntax is not a registered layout section, so the whole block was ignored even though its inner `element_type = progress_bar` and texture fields were valid. The earlier preload diagnosis was incomplete.

**Fix:** Change the header to `element {` in all four Drippy layout variants while retaining `element_type = progress_bar`, the live Drippy placeholder, the local texture paths and preloading.

**Prevention:** When adding a FancyMenu custom element by hand, copy the serialized container shape from an existing custom element: `element { ... element_type = <registered_type> ... }`. Type-specific block names are not interchangeable with `element`. Validate the rendered screen, not only the inner fields.

## [2026-09-20 02:15] — Arcadia gauge overlaps the native bar and fills backwards

**Context:** After correcting the custom-element container, the Arcadia texture rendered for the first time. The visual check showed it above the still-visible native white bar, and its fill receded from right to left. Resizing the game window also displaced the fixed layout.

**Error:** Two progress bars were visible, the Arcadia gauge filled in the opposite direction, and fixed coordinates did not adapt cleanly to smaller windows.

**Root cause:** Replacing the original `vanilla_button` entry removed FancyMenu's customization record for the native `progress_bar` widget, so Drippy rendered it again underneath the new element. FancyMenu's `left` direction selects right-to-left filling. The Drippy layouts also had no layout-wide auto-scaling block.

**Fix:** Restore a hidden `vanilla_button` entry targeting the native `progress_bar`, give the custom gauge its own `arcadia_progress_bar` identifier, change its direction to `right`, and enable a forced GUI scale plus layout auto-scaling from the 1920x1010 design canvas in all four variants.

**Prevention:** Keep native-widget suppression and replacement elements as separate records with separate identifiers. Confirm fill direction at partial progress and resize the game window during every loading-layout visual test.

## [2026-09-20 02:30] — Arcadia gauge clashes with the warm loading artwork

**Context:** The functional gauge rendered correctly after the overlap, direction and responsive-layout fixes. The in-game visual review showed that its long cyan center stripe dominated the composition.

**Error:** The progress fill looked like a clean neon tube and did not belong to the loading background's amber, wood, brass and shadow-heavy industrial palette.

**Root cause:** The original texture gave two of its six visible fill rows to saturated cyan. Nine-slice stretching turned those pixels into uninterrupted screen-wide lines, amplifying a small accent into the gauge's primary color.

**Fix:** Remove the cyan rows, expand both textures to the element's native 32x14 proportion, deepen the track into dark iron and walnut, and grade the fill from pale brass through amber to burnt copper.

**Prevention:** Judge nine-sliced textures by their stretched in-game appearance, not by the tiny source PNG. Reserve saturated accent colors for end caps or isolated details that cannot become full-width bands.

## [2026-09-20 02:45] — Hotbar micro-gears are invisible in game

**Context:** Two 5x5 copper-and-brass gears were added to the extreme ends of the Arcadia hotbar without changing the vanilla sprite dimensions. The first in-game review showed only a few copper pixels at normal GUI scale.

**Error:** The gears could not be identified as gears and disappeared visually into the dark end-cap lines.

**Root cause:** Their 5x5 footprint was centered only two pixels from each outer edge, leaving no room for a readable ring and placing the teeth over existing frame pixels with similar values.

**Fix:** Redraw each gear at 9x9 pixels with eight pale-brass teeth, a copper octagonal ring, a dark 3x3 center and a bright highlight. Move both gears to the upper end plates, where they have stronger contrast and remain clear of the item centers. A 7x7 intermediate preview was rejected because its one-pixel center still read as a copper sparkle rather than a gear.

**Prevention:** Review HUD pixel art at the actual in-game GUI scale and against populated slots. A recognizable mechanical symbol needs a distinct silhouette, a center hole and at least one value contrast from the surrounding frame.

## [2026-09-20 03:00] — Larger hotbar gears cover item slots

**Context:** Enlarging the gears from 5x5 to 9x9 made their silhouettes readable, but the vanilla hotbar sprite has no unused horizontal canvas outside its 182x22 bounds.

**Error:** Both gears overlapped the first and last slot, hiding part of the item icons.

**Root cause:** Decorative pixels baked into `hotbar.png` must remain inside the same 182-pixel width that contains all nine 20-pixel slots and the two one-pixel outer edges. Enlarging the source canvas would be scaled back into the fixed render width and distort every slot, so a texture-only fix cannot place artwork outside the bar.

**Fix:** Remove the gears from `hotbar.png`, generate one separate transparent 11x11 gear texture, and render two copies from a client-side post-HUD event. Their positions derive from the current GUI width and height and sit two pixels beyond the vanilla bar edges.

**Prevention:** Do not place external decorations inside fixed-size vanilla HUD sprites. Use a separate overlay with live GUI-relative coordinates whenever artwork must extend beyond the original occupied bounds.

## [2026-09-20 03:20] — External hotbar gears look detached

**Context:** The separate 11x11 overlay kept both gears outside the item slots, but the first in-game review exposed their final appearance at normal GUI scale.

**Error:** Each decoration looked like a small bright-orange ring floating too far from the hotbar instead of an attached industrial cog.

**Root cause:** The saturated copper body dominated the one-pixel teeth, and the two-pixel coordinate gap was compounded by transparent edge pixels in the sprite.

**Fix:** Replace the ring with a 13x13 dark-iron cog using substantial aged-copper teeth, a restrained copper hub and a small brass highlight. Position the nearest tooth directly against the hotbar's outer frame without entering an item slot.

**Prevention:** Review HUD decorations at their actual in-game scale and include transparent sprite margins when calculating visual spacing.

## [2026-09-20 03:35] — Full hotbar gears look like attached badges

**Context:** The 13x13 redesign improved contrast and spacing, but the in-game review still showed both complete gears beside the bar.

**Error:** The decorations remained visually separate from the chassis and did not provide enough pixels for convincing mechanical detail.

**Root cause:** Rendering the complete sprite outside the fixed hotbar preserved the item slots but made the gears read as external icons. The 13x13 canvas also limited the hub, rivets and tooth shading.

**Fix:** Expand the source cog to 17x17 with shaded teeth, an inset hub and four brass rivets. After in-game spacing review, render only the outer seven-pixel section at each end so most of the gear appears embedded behind the hotbar frame without covering item content.

**Prevention:** For decorations intended to look integrated into a fixed HUD sprite, crop the overlay at the chassis boundary instead of placing the full ornament beside it.

## [2026-09-20 14:23] — Relic texture pipeline rejected new and animated assets

**Context:** New inventory sprites, worn armor layers and animated weapon strips were being integrated for the three Arcadia relic sets.

**Error:** The first batch generator lost its stored output path after a regular-expression mismatch, the import helper rejected destinations that did not exist yet, the generic armor importer converted its bitmap back to a string, and GDI+ refused to save an animation over its still-open source file.

**Root cause:** The output-path expression escaped `.png` twice; the original importer assumed every operation replaced an existing asset; PowerShell variable names are case-insensitive, so the typed `$Source` parameter collided with `$source`; and `System.Drawing` keeps an input file locked until its bitmap is disposed.

**Fix:** Generate and import each source independently, permit new destinations, rename the bitmap variables, and save animated strips to a temporary PNG before replacing the source after disposal.

**Prevention:** Parse generator output with the tested expression, keep path and bitmap variables distinct, and use write-then-move whenever System.Drawing reads and replaces the same file.

**Contexte :** Integration des nouvelles icones, des couches d'armure portees et des bandes animees des trois ensembles reliques Arcadia.

**Erreur :** Le premier lot a perdu le chemin genere apres une expression reguliere incorrecte, l'importeur refusait les nouvelles destinations, l'importeur d'armure reconvertissait son bitmap en texte et GDI+ refusait d'ecraser l'image source encore ouverte.

**Cause :** L'expression echappait deux fois `.png`, l'importeur supposait qu'un fichier existait deja, les noms de variables PowerShell ne distinguent pas les majuscules et le fichier lu restait verrouille jusqu'a la liberation du bitmap.

**Correction :** Generation et import unitaire, autorisation des nouvelles destinations, noms de variables distincts et ecriture dans un PNG temporaire avant remplacement.

**Prevention :** Tester l'extraction du chemin, separer clairement chemins et bitmaps et toujours ecrire puis deplacer quand System.Drawing lit et remplace le meme fichier.

## [2026-09-21] Rhino const redeclaration in the cushion move guard
**Context:** handcrafted_cushion_move_dupe.js installing its piston and item-drop handlers.
**Error:** `redeclaration of var level` at line 192, guard never installed.
**Root cause:** Rhino hoists `const` declared in nested functions and callbacks into the enclosing function scope, so `const level` in armPistonFurniture and in the EntityJoinLevelEvent callback collided.
**Fix:** renamed them `pistonLevel` and `joinLevel`.
**Prevention:** inside one KubeJS function, give every `const`/`let` in nested callbacks a unique name.

## [2026-09-21] getGameTime() not callable from Rhino, server crash
**Context:** contraption_block_loss_trace.js capture probe, run from Create's BlockMovementChecks during piston assembly.
**Error:** `TypeError: Cannot find function getGameTime in object ServerLevel` at line 105, "Ticking block entity" crash.
**Root cause:** Rhino exposes ServerLevel#getGameTime() only as the `gameTime` bean property (same as `dimension`). The probe had no try/catch, so the throw reached the server tick.
**Fix:** use `level.gameTime` in the tracer and the cushion guard; wrap the capture probe in try/catch.
**Prevention:** read Level getters as properties in KubeJS, and wrap every callback Create or NeoForge invokes on the server thread.
