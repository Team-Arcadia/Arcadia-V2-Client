# Changelog

All notable changes to Arcadia V2 - Echoes Of Power are documented here, by date.

---

## 2026-09-20

### Changed

- **The loading progress bar is now a real Arcadia gauge** — All four Drippy loading-screen variants hide the native white bar and replace it with FancyMenu's native textured progress element. A dark iron and walnut housing with aged-brass edges frames a warm molten-copper fill, matching the amber industrial loading artwork without a dominant neon accent. Drippy drives it from left to right through `game_loading_progress`; both textures are preloaded, and layout-wide auto-scaling keeps the gauge aligned when the game window changes size.

- **The vanilla hotbar now matches Arcadia** — KubeJS overrides the four Minecraft 1.21.1 HUD sprites for the nine-slot bar, active-slot selection and both offhand orientations. The bar uses dark iron and restrained copper separators; two separate 13x13 dark-iron cogs with aged copper teeth touch its outer frame without covering an item. Their coordinates follow the current GUI dimensions automatically. The selected slot uses luminous copper and brass with small arcane-cyan corner accents, while every vanilla sprite keeps its original dimensions.

- **FTB Quests now carries the Arcadia visual identity** — KubeJS overrides the five shared FTB Library surfaces and all 27 FTB Quests GUI textures shipped by version 2101.1.36. The new skin uses restrained dark iron, walnut, aged brass and arcane-cyan accents, preserves every upstream texture dimension and icon silhouette, and includes a deterministic generator for future maintenance. In-game reviews replaced the dense 16-pixel editor grid with a continuous warm charcoal surface and quiet broken grain, then changed dependency arrows from muted cyan to luminous copper-gold that remains visible after FTB applies its state tint. Reload client resources with F3+T to apply it. Final in-game confirmation is still required.

### Modifications

- **La barre de chargement devient une vraie jauge Arcadia** — Les quatre variantes de l'ecran Drippy masquent l'ancienne barre blanche et la remplacent par l'element de progression texture natif de FancyMenu. Un chassis en fer sombre et noyer borde de laiton vieilli encadre un remplissage chaud en cuivre en fusion, assorti au decor industriel ambre sans accent neon dominant. Drippy le pilote de gauche a droite par `game_loading_progress` ; les textures sont prechargees et la mise a l'echelle automatique garde la jauge alignee quand la fenetre change de taille.

- **La barre rapide vanilla adopte le style Arcadia** — KubeJS surcharge les quatre sprites HUD de Minecraft 1.21.1 pour la barre de neuf cases, la selection active et les deux orientations de main secondaire. La barre emploie du fer sombre et des separateurs cuivre discrets ; deux engrenages distincts de 13x13 pixels, en fer sombre avec des dents en cuivre vieilli, touchent son cadre exterieur sans masquer un objet. Leurs coordonnees suivent automatiquement les dimensions actuelles de l'interface. La case choisie conserve ses accents cuivre, laiton et cyan, tandis que tous les sprites vanilla gardent leurs dimensions d'origine.

- **FTB Quests porte desormais l'identite visuelle Arcadia** — KubeJS surcharge les cinq surfaces partagees de FTB Library et les 27 textures d'interface livrees par FTB Quests 2101.1.36. Le nouveau skin emploie sobrement fer sombre, noyer, laiton vieilli et accents cyan arcaniques, conserve toutes les dimensions et silhouettes amont, et fournit un generateur deterministe pour la maintenance. Les verifications en jeu ont remplace la grille dense de 16 pixels par une surface anthracite chaude et continue au grain discret, puis transforme les fleches de dependance cyan ternes en cuivre dore lumineux qui reste visible apres la teinte d'etat appliquee par FTB. Recharger les ressources client avec F3+T pour l'appliquer. La confirmation finale en jeu reste necessaire.

---

## 2026-09-18

### Fixed

- **The CurseForge manifest no longer matched the pack** — The manifest is what a player's launcher reads to download the mods, and it had drifted badly: 134 of its entries pointed at files that are no longer installed, while 145 projects the pack actually runs were missing from it. Anyone importing the pack got a different set of mods from the one the `config/` and `kubejs/` overrides are written against. It is now generated from the installed instance and lists 466 entries, 440 mod jars and the 26 shaderpacks. The two patched jars CurseForge still tracks are deliberately left out, because the launcher would otherwise download the upstream file over our fix.

### Changed

- **The store page and the docs now carry measured figures** — Every advertised number was recounted against the pack instead of being carried over. The mod count goes from 441 to 446, the quest count from "3000+" to 3,893 across 43 chapters (the page claimed 41 chapters in English and 31 in French), and the translation figure from "25 000+" to 85 000+, which was a large understatement: the quest lang files alone hold 83,284 keys across the seven languages. The banned item list is 154, not 152. Server capacity is no longer given as a 30-50 range but as the real peak, 88 simultaneous players.

- **The advertised NeoForge version was two hundred builds behind** — The page, the README, the structure map and the project rules all said 21.1.232 while the instance runs 21.1.250. More importantly the manifest declared the same stale build, so a CurseForge import installed a loader the pack is not tested on. All five are corrected; the changelog entries that describe the older state are left alone.

- **Two mod bugs we were patching have been fixed upstream** — Create: Apotheosis Automation 1.1.1 now ships three of the recipes we were overriding in exactly the form we had written, so those overrides were removed. The five remaining ones stay: the mod still declares its fluid ingredients with a type that does not exist on 1.21.1. In the same pass, create_things_and_misc 4.1.1 corrected the recipe format on its own side, so 26 of our 39 rebuilt recipes were replacing the mod's recipes with an identical copy and are gone. Thirteen rebuilds remain, covering the recipes the mod still ships with a pattern key the 1.21 recipe reader rejects.

### Correctifs

- **Le manifest CurseForge ne correspondait plus au pack** — Le manifest est ce que le launcher d'un joueur lit pour telecharger les mods, et il avait fortement derive : 134 de ses entrees pointaient vers des fichiers qui ne sont plus installes, tandis que 145 projets reellement utilises par le pack n'y figuraient pas. Toute personne important le pack obtenait donc un ensemble de mods different de celui pour lequel les overrides `config/` et `kubejs/` sont ecrits. Il est desormais genere depuis l'instance installee et compte 466 entrees, 440 jars de mods et les 26 shaderpacks. Les deux jars patches encore suivis par CurseForge en sont volontairement exclus, sans quoi le launcher telechargerait le fichier amont par-dessus notre correctif.

### Modifications

- **La page boutique et les docs portent desormais des chiffres mesures** — Chaque nombre annonce a ete recompte sur le pack au lieu d'etre recopie. Le nombre de mods passe de 441 a 446, celui des quetes de « 3000+ » a 3 893 reparties sur 43 chapitres (la page annoncait 41 chapitres en anglais et 31 en francais), et celui des traductions de « 25 000+ » a 85 000+, ce qui etait une large sous-estimation : les fichiers de langue des quetes contiennent a eux seuls 83 284 cles sur les sept langues. La liste d'items bannis en compte 154, pas 152. La capacite serveur n'est plus donnee comme une fourchette 30-50 mais comme le vrai pic atteint, 88 joueurs simultanes.

- **La version NeoForge annoncee avait deux cents builds de retard** — La page, le README, la carte de structure et les regles du projet indiquaient tous 21.1.232 alors que l'instance tourne en 21.1.250. Plus genant, le manifest declarait le meme build perime : un import CurseForge installait donc un loader sur lequel le pack n'est pas teste. Les cinq sont corriges ; les entrees de changelog qui decrivent l'etat anterieur sont laissees telles quelles.

- **Deux bugs de mods que nous corrigions l'ont ete en amont** — Create: Apotheosis Automation 1.1.1 livre desormais trois des recettes que nous surchargions, dans exactement la forme que nous avions ecrite : ces surcharges ont ete retirees. Les cinq autres restent, le mod declarant toujours ses ingredients fluides avec un type qui n'existe pas en 1.21.1. Dans la meme passe, create_things_and_misc 4.1.1 a corrige le format de ses recettes, si bien que 26 de nos 39 recettes reconstruites remplacaient celles du mod par une copie identique : elles ont ete supprimees. Treize reconstructions subsistent, pour les recettes que le mod livre encore avec une cle de motif que le lecteur de recettes 1.21 refuse.

---

## 2026-09-16

### Fixed

- **Single player worlds refused to load** — Opening a world failed with "Errors in currently selected data packs prevented the world from loading". KubeJS Tweaks patches a specific call inside KubeJS to keep the ordering of recipe components, and the KubeJS update of 14 September rewrote that method, so the patch no longer found what it was meant to replace. The mod declares no guard against this, and the miss was fatal: it broke the class that parses recipes, which brought down the whole datapack reload. KubeJS Tweaks is a development tool with no in-game content, no script in the pack uses it and no mod depends on it, so it has been taken out of the pack rather than holding KubeJS back.

- **The cushion duplication guard had never run** — The fix meant to stop Handcrafted chairs, benches, couches and fancy beds from printing a free cushion every time a Create contraption or a piston moved them failed to install at every boot, so the duplication was still live. The script tested block types with a call that KubeJS does not expose on a loaded Java class, which aborted the install before a single guard was armed. The same faulty call sat in the handler that cancels the duplicated cushion and would have failed on the first dropped item. Both are corrected, so the guard now arms.

- **The Liquid Blaze Burner still printed for free** — A schematicannon printed a Liquid Blaze Burner at the price of a plain Blaze Burner, without ever taking the Straw out of the chest, while breaking it gave back a burner and a straw: print, break and repeat yielded one free straw per cycle. The script registering the missing cost built its cost provider in a shape Rhino turns into a stub that answers nothing, so Create fell back to the default price and the registration crashed on its own self test. The provider is now built correctly and checked before being registered, so a printed Liquid Blaze Burner costs a Blaze Burner plus a Straw, as the material checklist now shows.

- **The contraption block-loss tracer could not start** — The temporary diagnostic collecting evidence on Redstone Links duplicating and on doors, beds, banners and bells vanishing when a train is reassembled could not load, because it asked for a Java class the KubeJS security filter denies. It now uses the stack trace facility KubeJS provides, so the next reproduction of either report will be recorded.

### Correctifs

- **Les mondes solo refusaient de charger** — L'ouverture d'un monde echouait avec "Errors in currently selected data packs prevented the world from loading". KubeJS Tweaks modifie un appel precis a l'interieur de KubeJS pour conserver l'ordre des composants de recette, et la mise a jour de KubeJS du 14 septembre a reecrit cette methode : la modification ne trouvait donc plus ce qu'elle devait remplacer. Le mod ne prevoit aucun garde-fou pour ce cas, et l'echec etait fatal puisqu'il cassait la classe qui lit les recettes, entrainant tout le rechargement des datapacks. KubeJS Tweaks est un outil de developpement sans contenu en jeu, aucun script du pack ne l'utilise et aucun mod n'en depend : il a donc ete retire plutot que de bloquer KubeJS sur une ancienne version.

- **Le correctif de duplication des coussins n'avait jamais tourne** — Le correctif cense empecher les chaises, bancs, canapes et lits raffines de Handcrafted de produire un coussin gratuit a chaque deplacement par une contraption Create ou un piston echouait a s'installer a chaque demarrage, et la duplication restait donc active. Le script testait le type des blocs avec un appel que KubeJS n'expose pas sur une classe Java chargee, ce qui interrompait l'installation avant l'armement du moindre garde. Le meme appel fautif se trouvait dans le gestionnaire qui annule le coussin duplique et aurait echoue au premier objet tombe. Les deux sont corriges, le garde s'arme desormais.

- **Le Liquid Blaze Burner s'imprimait toujours gratuitement** — Un schematicannon imprimait un Liquid Blaze Burner au prix d'un simple Blaze Burner, sans jamais prendre la Paille dans le coffre, alors que le casser rendait un brasier et une paille : imprimer, casser et recommencer donnait une paille gratuite par cycle. Le script qui enregistrait le cout manquant construisait son fournisseur de cout dans une forme que Rhino transforme en coquille vide, si bien que Create revenait au prix par defaut et que l'enregistrement plantait sur son propre test. Le fournisseur est desormais construit correctement et verifie avant enregistrement : un Liquid Blaze Burner imprime coute un Blaze Burner et une Paille, ce que la liste de materiaux affiche maintenant.

- **Le traceur de pertes de blocs en contraption ne demarrait pas** — Le diagnostic temporaire qui recolte des preuves sur la duplication des Redstone Links et sur la disparition des portes, lits, bannieres et cloches au reassemblage d'un train ne pouvait pas se charger, car il demandait une classe Java refusee par le filtre de securite de KubeJS. Il utilise desormais le mecanisme de trace fourni par KubeJS, la prochaine reproduction de l'un ou l'autre rapport sera donc enregistree.

---

## 2026-09-14

### Changed

- **Texture completion**: refreshed all 21 disc icons and their 42 placed-disc copies, both machine faces, and six worn-armor texture files. The finished reinforced casing now has closed panels. Texture validation rejects legacy item sizes and transparent block pixels; armor UV coverage is preserved. In-game rendering still requires visual confirmation.

- **Arcadia texture refresh**: replaced the custom inventory artwork with 32x32 pixel art, including industrial components, incomplete assemblies, keys, magic items, armor icons and music discs. Machine blocks use matching pixel textures. Placed-disc copies stay synchronized with their inventory icons. Texture checks are available through `kubejs/tools/check_textures.ps1`.

### Fixed

- **Palm and avocado saplings could not go into Botany Pots** — The Crabber's Delight palm sapling and the Cultural Delights avocado sapling had no Botany Pots recipe, because Botany Trees ships none for either mod, so the pots refused them. Both now grow in pots in 2400 ticks like every other Botany Trees tree: logs, a 5% sapling, leaves when shears sit in the harvest slot, and their fruit (45% coconut, 15% avocado). The palm accepts dirt or sand, the avocado dirt. Contributed through pull request #1.

- **Storage disks from lootboxes did not work** — Every Refined Storage and ExtraDisks disk offered by the shop lootboxes and the Diamond event box, from the 1k disk up to the infinite item, fluid and chemical disks, was defined with a fixed `refinedstorage:storage_reference` UUID, most likely copied from an existing disk when the boxes were reworked in July. A disk only points at its storage through that UUID, and Refined Storage only creates a storage for a disk that has none, so every winner received a disk pointing at a storage that never existed: it stayed inert and did not show on the Disk Drive. The 13 affected rewards (12 item rewards and one give command) now hand out a blank disk that gets its own storage on first use. Winners never shared contents, since a disk carrying a UUID never creates storage. Disks already given out stay broken until replaced or cleared of the component.

- **Elokosa Paws still crashed the server** — Using a Paw of the New Moon, or any other moon phase paw, crashed the server: `ItemElokosaPaw.use()` loads client-only particle classes that do not exist on a dedicated server. A KubeJS patch meant to block it had been in place since May, but it listened for `mowziesmobs:elokosa_paw`, an id Mowzie's Mobs 1.8.2 never registers; the mod ships one item per phase instead, so the patch never fired. It now covers the five real ids (full, gibbous, half, crescent, new) and still cancels the use with a message. Using a paw on another player goes through the same method, so that case is covered too.

- **Small dripleaf and nether sprouts grew empty in Botany Pots** — The crops grew normally but every harvest came back empty. Botany Pots harvests these through the vanilla block loot table, which only drops the plant when broken with shears, and the pot's harvest slot holds no tool by default. Botany Pots already ships a tool-free table for ferns, grass, seagrass, glow lichen, corals and sculk, but not for these two. Both recipes are now overridden with a table that yields one plant per harvest; the nether sprouts soil rules are unchanged. Twisting and weeping vines keep their vanilla one-in-three chance without a tool.

### Modifications

- **Finalisation des textures** : refonte des 21 icones de disques et de leurs 42 copies posees, des deux faces de machines et des six fichiers d'armures portees. Le boitier renforce termine possede des panneaux fermes. Le controle refuse les anciens formats d'objets et les pixels transparents des blocs ; les zones UV des armures sont conservees. Le rendu en jeu reste a confirmer visuellement.

- **Refonte des textures Arcadia** : nouvelles textures d'inventaire en pixel art 32x32 pour les composants industriels, assemblages incomplets, cles, objets magiques, icones d'armure et disques. Les blocs de machines utilisent des textures assorties. Les copies des disques poses restent synchronisees avec leurs icones. Le controle des textures est disponible dans `kubejs/tools/check_textures.ps1`.

### Correctifs

- **Les pousses de palmier et d'avocatier n'entraient pas dans les Botany Pots** — La pousse de palmier de Crabber's Delight et la pousse d'avocatier de Cultural Delights n'avaient aucune recette Botany Pots, Botany Trees n'en fournissant pour aucun de ces deux mods, et les pots les refusaient. Les deux poussent desormais en pot en 2400 ticks comme les autres arbres Botany Trees : buches, 5 % de pousse, feuilles avec des cisailles dans l'emplacement de recolte, et leur fruit (45 % de noix de coco, 15 % d'avocat). Le palmier accepte la terre ou le sable, l'avocatier la terre. Contribution via la pull request #1.

- **Les disques de stockage des lootbox ne fonctionnaient pas** — Tous les disques Refined Storage et ExtraDisks proposes par les lootbox de boutique et la box d'event Diamant, du disque 1k jusqu'aux disques infinis d'items, de fluides et de chimiques, etaient definis avec un UUID `refinedstorage:storage_reference` fige, tres probablement recopie depuis un disque existant lors de la refonte des box en juillet. Un disque ne pointe vers son stockage que par cet UUID, et Refined Storage ne cree un stockage que pour un disque qui n'en a pas : chaque gagnant recevait donc un disque pointant vers un stockage qui n'a jamais existe, inerte et invisible sur le Disk Drive. Les 13 recompenses concernees (12 items et une commande give) donnent desormais un disque vierge qui recoit son propre stockage a la premiere utilisation. Les gagnants n'ont jamais partage de contenu, un disque portant un UUID ne creant jamais de stockage. Les disques deja distribues restent inutilisables tant qu'ils ne sont pas remplaces ou purges du composant.

- **Les pattes d'Elokosa faisaient encore crasher le serveur** — Utiliser une Patte de la Nouvelle Lune, ou n'importe quelle autre phase, faisait crasher le serveur : `ItemElokosaPaw.use()` charge des classes de particules reservees au client, absentes d'un serveur dedie. Un correctif KubeJS etait en place depuis mai, mais il ecoutait `mowziesmobs:elokosa_paw`, un identifiant que Mowzie's Mobs 1.8.2 n'enregistre pas ; le mod declare un item par phase, donc le correctif ne se declenchait jamais. Il couvre desormais les cinq vrais identifiants (pleine, gibbeuse, demi, croissant, nouvelle) et annule toujours l'utilisation avec un message. Utiliser une patte sur un autre joueur passe par la meme methode et est donc couvert aussi.

- **Le small dripleaf et les nether sprouts poussaient a vide dans les Botany Pots** — Les plantes poussaient normalement mais chaque recolte etait vide. Botany Pots recolte ces crops via la loot table vanilla du bloc, qui ne rend la plante qu'avec des cisailles, et l'emplacement de recolte du pot est vide par defaut. Botany Pots fournit deja une table sans outil pour les fougeres, les herbes, la seagrass, le glow lichen, les coraux et le sculk, mais pas pour ces deux-la. Les deux recettes sont desormais surchargees avec une table qui rend une plante par recolte ; les sols des nether sprouts ne changent pas. Les twisting et weeping vines gardent leur chance vanilla d'une sur trois sans outil.

---

## 2026-09-01

### Added

- **Create chromatic chain reopened** — Create 6.0.10 still registers Chromatic Compound, Refined Radiance, Shadow Steel and the Shadow and Radiant Casings, still ships the in-world conversion code, and still exposes `enableRefinedRadianceRecipe`, `enableShadowSteelRecipe` and `lightSourceCountForRefinedRadiance` in `create-server.toml`, but the jar no longer carries a single recipe producing any of them. Create Encased builds 44 machine variants on those two casings, so the whole Shadow Steel and Refined Radiance tier was unobtainable: across all 443 jars the only source of a Chromatic Compound was one epic chest loot table. Chromatic Compound is back as a superheated Mixing of Cinder Flour and Powdered Obsidian, and the two casings are made by Item Application on a Brass Casing, the same shape Create uses for its own Railway Casing, so both automate with a Deployer. Refined Radiance and Shadow Steel need no recipe: Create converts the dropped compound itself, through light sources or a fall past the world floor.

### Fixed

- **Oil Deposit could be relocated with a spell** — Ars Nouveau's Animate Block turns a block into a fighting entity that drops back as a solid block wherever it dies, and a player used it to lift a TFMG Oil Deposit to the surface. The deposit has an empty loot table and no block entity, so it cannot be picked up by hand: the spell was the only way to move it, and moving it skips the whole industrial pipe run down to the field. `EffectAnimate` gates on `EnchantedFallingBlock.canFall`, which reads the `ars_nouveau:gravity_blacklist` block tag, and that tag already pulls in `c:relocation_not_supported`. TFMG had declared the deposit in `create:non_movable`, which only stops Create contraptions, and never added it to the cross-mod convention tag. The Oil Deposit, the Large Switch and the Large Transformer, the three blocks TFMG marks non-movable, now sit in `c:relocation_not_supported`, which also closes the Gravity glyph and the Mekanism Cardboard Box, and they are listed a second time directly in `ars_nouveau:gravity_blacklist` so the fix survives a change to Ars Nouveau's own tag.

- **Endersoul Hand could carry off a Trophy Pedestal** — A player misclicked with the Endersoul Hand on a Twilight Forest Trophy Pedestal, picked it up, threw it around and got it back as an item. Mutant Monsters rejects a block only when it has a block entity or sits in its own holdable-immune tag, and that tag is a short vanilla list. Twilight Forest already declares everything it wants left alone in `twilightforest:common_protections`, so both Mutant Monsters tags now include it rather than repeating a hand-typed list. The nine boss spawners, the skull chest and the keepsake casket were never at risk, all of them having a block entity; what was actually exposed is the trophy pedestal, the stronghold shield, the two vanishing blocks and the five force fields, none of which have one. The same tags also pull in `c:relocation_not_supported`, which closes a second route to the TFMG oil deposit of the previous entry. The fix covers the Mutant Enderman as well: it picks blocks up through the same check.

- **Extruders drawn oversized inside limited barrels** — A Mechanical Extruder or Mechanical Brass Extruder placed in a Limited Barrel rendered wrong, on every wood type. Both extruder item models are 22 units tall because the pole is baked into them, while the in-world block model stops at 17 and leaves the pole to the block entity renderer. Sophisticated Storage draws barrel display items with `ItemDisplayContext.FIXED`, and neither model declares a `fixed` transform, so a 22 unit model landed in a slot sized for a 16 unit block. Two model overrides in `assets/create_mechanical_extruder/models/item/` now add that transform, scaling by 16/22 and dropping the result back onto the block floor. Only the fixed context changes, so inventory, hand and ground rendering keep the mod's own transforms; item frames gain the same fit.

- **Copy and Paste turned Sophisticated barrels into acacia** — Copying a dark oak Limited Barrel with the Building Gadget pasted an acacia one the player never owned. Sophisticated Storage keeps the wood type in the block entity, as an `Optional<WoodType>` on `WoodStorageBlockEntity`; the blockstate carries only facing, flat top and vertical facing. `GadgetCopyPaste` records blockstates and nothing else, so pasting built a fresh block entity with no wood type and the mod fell back to `WoodType.ACACIA`. The 36 barrels and chests are now in `buildinggadgets2:deny`, which `GadgetUtils.isValidBlockState` reads, so the Copy, Build and Exchange gadgets skip them instead of producing the wrong block. Cut and Paste is deliberately left working: it checks neither the tag nor `isValidBlockState` and carries block entity data through `TagPos`, so it remains the right tool for moving these blocks. Shulker boxes are untouched, having no wood type.

- **Sophisticated Storage pump upgrades made craftable** — The Pump, Advanced Pump and Experience Pump upgrades appear in the quest book but no recipe produced them anywhere in the pack, leaving a three-quest chain permanently blocked. The items are registered in the mod and enabled in `sophisticatedcore-common.toml`; the mod simply never ships a recipe, in either direction of its usual storage and backpack conversion pairs. Three recipes now sit in `data/arcadia/recipe/`, copied from the Sophisticated Backpacks recipe for the same item with the storage upgrade base swapped in, so the cost matches every other upgrade whose storage and backpack versions are priced alike. Be aware that these three upgrades do nothing once installed: `PumpUpgradeWrapper` and `XpPumpUpgradeWrapper` both read `IStorageWrapper.getFluidHandler()`, which Sophisticated Backpacks overrides through its Tank Upgrade and Sophisticated Storage never overrides, having no Tank Upgrade at all. The recipes exist to unblock the quest chain, not because the feature works.

### Ajouts

- **Chaine chromatique de Create rouverte** — Create 6.0.10 enregistre toujours le Compose Chromatique, la Radiance Raffinee, l'Acier des Ombres et les chassis Ombre et Radiant, embarque toujours le code de conversion au sol, et expose toujours `enableRefinedRadianceRecipe`, `enableShadowSteelRecipe` et `lightSourceCountForRefinedRadiance` dans `create-server.toml`, mais le jar ne contient plus aucune recette qui en produise. Create Encased construit 44 variantes de machines sur ces deux chassis : toute la tier Acier des Ombres et Radiance Raffinee etait donc inatteignable, et sur les 443 jars la seule source de Compose Chromatique etait une loot table de coffre epique. Le Compose Chromatique revient par un Mixing surchauffe de Farine de Cendres et de Poudre d'Obsidienne, et les deux chassis se font par Application d'Objet sur un Chassis en Laiton, la forme que Create emploie deja pour son propre Chassis Ferroviaire, donc automatisables au Deployeur. La Radiance Raffinee et l'Acier des Ombres n'ont besoin d'aucune recette : Create convertit lui-meme le compose lache au sol, par les sources de lumiere ou par une chute sous le plancher du monde.

### Correctifs

- **Le Gisement de petrole pouvait etre deplace au sort** — Le sort Animer un bloc d'Ars Nouveau transforme un bloc en creature qui se bat, et une fois morte le bloc se repose la ou elle tombe ; un joueur s'en est servi pour remonter un Gisement de petrole TFMG a la surface. Le gisement a une loot table vide et aucun block entity, il ne peut donc pas etre ramasse a la main : le sort etait le seul moyen de le bouger, et le bouger permet de sauter toute la descente de tuyaux industriels jusqu'au gisement. `EffectAnimate` passe par `EnchantedFallingBlock.canFall`, qui lit le tag de blocs `ars_nouveau:gravity_blacklist`, et ce tag inclut deja `c:relocation_not_supported`. TFMG avait declare le gisement dans `create:non_movable`, qui n'arrete que les contraptions Create, sans jamais l'ajouter au tag de convention cross-mod. Le Gisement de petrole, le Grand interrupteur et le Grand transformateur, les trois blocs que TFMG marque non deplacables, sont desormais dans `c:relocation_not_supported`, ce qui ferme au passage le glyphe Gravite et la Boite en carton de Mekanism, et ils sont listes une seconde fois directement dans `ars_nouveau:gravity_blacklist` pour que le correctif survive a un changement du tag d'Ars Nouveau.

- **La Main d'ame ender pouvait emporter un Piedestal a trophee** — Un joueur a mal clique avec l'Endersoul Hand sur un Piedestal a trophee de Twilight Forest, l'a ramasse, l'a lance et l'a recupere sous forme d'objet. Mutant Monsters ne refuse un bloc que s'il possede un block entity ou s'il figure dans son propre tag holdable-immune, lequel se limite a une courte liste vanilla. Twilight Forest declare deja tout ce qu'il veut voir intouchable dans `twilightforest:common_protections`, les deux tags de Mutant Monsters incluent donc ce tag plutot que de recopier une liste a la main. Les neuf invocateurs de boss, le coffre a crane et le cercueil souvenir n'ont jamais rien risque, ils ont tous un block entity ; ce qui etait reellement expose, c'est le piedestal a trophee, le bouclier de forteresse, les deux blocs evanescents et les cinq champs de force, qui n'en ont pas. Les memes tags incluent aussi `c:relocation_not_supported`, ce qui ferme une seconde voie vers le gisement de petrole TFMG de l'entree precedente. Le correctif couvre egalement le Mutant Enderman, qui ramasse les blocs via le meme controle.

- **Extruders affiches trop grands dans les limited barrels** — Un Mechanical Extruder ou un Mechanical Brass Extruder pose dans un Limited Barrel s'affichait mal, quelle que soit l'essence du baril. Les deux modeles d'objet des extruders font 22 unites de haut parce que le mat y est integre, alors que le modele de bloc en jeu s'arrete a 17 et laisse le mat au block entity renderer. Sophisticated Storage dessine les objets affiches sur un baril avec `ItemDisplayContext.FIXED`, et aucun des deux modeles ne declare de transformation `fixed` : un modele de 22 unites atterrissait donc dans un emplacement dimensionne pour un bloc de 16. Deux surcharges de modele dans `assets/create_mechanical_extruder/models/item/` ajoutent cette transformation, avec une mise a l'echelle de 16/22 et un recalage du resultat sur le plancher du bloc. Seul le contexte fixed change, l'inventaire, la main et le sol gardent les transformations du mod ; les cadres d'objet beneficient du meme ajustement.

- **Le copier-coller transformait les barils Sophisticated en acacia** — Copier un Baril limite en chene noir avec le Building Gadget en collait un en acacia que le joueur n'avait jamais possede. Sophisticated Storage garde l'essence dans le block entity, sous forme d'`Optional<WoodType>` sur `WoodStorageBlockEntity` ; la blockstate ne porte que l'orientation, le dessus plat et l'orientation verticale. `GadgetCopyPaste` n'enregistre que les blockstates, donc le collage creait un block entity neuf sans essence et le mod retombait sur `WoodType.ACACIA`. Les 36 barils et coffres sont desormais dans `buildinggadgets2:deny`, que lit `GadgetUtils.isValidBlockState`, si bien que les gadgets Copy, Build et Exchange les ignorent au lieu de poser le mauvais bloc. Le Cut and Paste reste volontairement fonctionnel : il ne consulte ni le tag ni `isValidBlockState` et transporte les donnees de block entity via `TagPos`, il demeure donc le bon outil pour deplacer ces blocs. Les shulker boxes ne sont pas concernees, elles n'ont pas d'essence.

- **Upgrades pompe de Sophisticated Storage rendues craftables** — Les upgrades Pompe, Pompe avancee et Pompe a experience figurent dans le quest book mais aucune recette ne les produisait nulle part dans le pack, ce qui bloquait definitivement une chaine de trois quetes. Les items sont bien enregistres par le mod et actives dans `sophisticatedcore-common.toml` ; le mod ne livre simplement aucune recette, dans aucun des deux sens de ses paires de conversion coffre et sacoche habituelles. Trois recettes sont desormais dans `data/arcadia/recipe/`, recopiees de la recette Sophisticated Backpacks du meme item avec la base d'upgrade coffre a la place, si bien que le cout est aligne sur tous les autres upgrades dont les versions coffre et sacoche valent la meme chose. A savoir : ces trois upgrades ne font rien une fois installees. `PumpUpgradeWrapper` et `XpPumpUpgradeWrapper` lisent tous deux `IStorageWrapper.getFluidHandler()`, que Sophisticated Backpacks surcharge via son Tank Upgrade et que Sophisticated Storage ne surcharge jamais, faute de Tank Upgrade. Les recettes existent pour debloquer la chaine de quetes, pas parce que la fonctionnalite marche.

---

## 2026-08-27

### Changed

- **Quest book translations completed** — The `ru_ru` and `zh_cn` quest books were never translated: Russian shipped as Cyrillic typed in Latin letters, Chinese as toneless pinyin. Russian was transliterated back to Cyrillic; Chinese was rebuilt from the English source and now carries real characters on all 28,196 values. Item, mob, glyph, ritual, spell school, robe and shelf names are read straight out of the mod jars, including the cases where the quest book uses a registry id rather than the display name, so a Chinese player reads the same words in the book and in their inventory. The French, Spanish and Portuguese books had also lost every accent and apostrophe and were restored (23,277 / 10,838 / 13,110 accented characters). Three formatting defects present in all seven locales were fixed along the way: a doubled colour code, a stray leading space in a subtitle, and a task label left half-translated.

- **Simply Swords quest rewards rebalanced** — The chapter handed out 10 Runic Tablets, 4 Runefused Gems, 3 Netherfused Gems, 5 Empowered Remnants, 3 Contained Remnants and 2 Tampered Remnants for free. Contained and Tampered Remnants turn into random unique weapons on their own, and tablets are otherwise loot-only, so the chapter was worth roughly four free uniques plus ten runic crafts or re-rolls per player. Since `default_consume_items` is `false` and rewards are per-player, a single shared set of weapons unlocked the whole chapter for an entire team. Rewards are now 3 Runic Tablets, 1 Runefused Gem, 1 Netherfused Gem and 1 Empowered Remnant total, all placed on real capstones (Runic Grimoire, netherite set, runic set, full unique collection, Awakened Lichblade, end of the remnant chain). Remnants that spawn weapons are gone entirely. Quest XP rises from 3,450 to 10,200 across the chapter to keep completion worth doing.

### Modifications

- **Traductions du quest book terminees** — Les livres `ru_ru` et `zh_cn` n'avaient jamais ete traduits : le russe etait du cyrillique tape en lettres latines, le chinois du pinyin sans tons. Le russe a ete retranslittere en cyrillique ; le chinois a ete reconstruit depuis la source anglaise et porte desormais de vrais caracteres sur les 28 196 valeurs. Les noms d'objets, de creatures, de glyphes, de rituels, d'ecoles de magie, de robes et d'etageres sont lus directement dans les jars des mods, y compris quand le quest book emploie un identifiant de registre plutot que le nom affiche, pour qu'un joueur chinois lise les memes mots dans le livre et dans son inventaire. Les livres francais, espagnol et portugais avaient aussi perdu tous leurs accents et apostrophes et ont ete restaures (23 277 / 10 838 / 13 110 caracteres accentues). Trois defauts de formatage presents dans les sept langues ont ete corriges au passage : un code couleur double, une espace parasite en tete de sous-titre, et un libelle de tache reste a moitie traduit.

- **Recompenses du quest book Simply Swords rebalancees** — Le chapitre distribuait gratuitement 10 Tablettes Runiques, 4 Gemmes Runefusionnees, 3 Gemmes Netherfusionnees, 5 Reliquats Renforces, 3 Reliquats Contenus et 2 Reliquats Falsifies. Les Reliquats Contenus et Falsifies se transforment tout seuls en armes uniques aleatoires, et les tablettes ne s'obtiennent autrement qu'en loot : le chapitre valait donc environ quatre uniques gratuites plus dix crafts ou re-rolls runiques par joueur. Comme `default_consume_items` vaut `false` et que les recompenses sont individuelles, un seul jeu d'armes partage debloquait tout le chapitre pour une equipe entiere. Les recompenses passent a 3 Tablettes Runiques, 1 Gemme Runefusionnee, 1 Gemme Netherfusionnee et 1 Reliquat Renforce au total, tous places sur de vrais paliers (Grimoire Runique, panoplie netherite, panoplie runique, collection unique complete, Lame de la liche eveillee, fin de la chaine des reliquats). Les reliquats qui generent des armes sont supprimes. L'XP du chapitre passe de 3 450 a 10 200 pour que la completion reste interessante.

---

## 2026-08-11

### Added

- **Magnetic Jammer** — New block suppressing item magnets over a 5 chunk radius (11x11 chunks, full height). Ground items inside the field carry the NeoForge `PreventRemoteMovement` flag, which the Sophisticated Backpacks and Storage magnet upgrades, the Immersive Engineering powerpack magnet and the Occultism greedy familiar all honour; manual pickup is unaffected. `create_sa:copper_magnet` ignores the convention and is countered separately. Crafted in a 5x5 Mechanical Crafter from TFMG coils and magnets, copper wire coils and a brass casing.
- **Stellar Forge chain** — The Occultism Dimensional Battlefield now pays out fragments instead of finished boss drops: `arcadia:star_fragment` for the Wither, `arcadia:dragon_shard` for the Ender Dragon. Four fragments feed a Create sequenced assembly line (3 loops, deploying / pressing / filling) to produce one nether star or one dragon egg. The boss fights themselves are untouched, so a hand-killed Wither still drops its 1-2 stars. Four new item textures generated by `_gen_star.py`.

### Changed

- **Schematic size cap raised** — `maxTotalSchematicSize` 256 to 2048 KB and `maxSchematicPacketSize` 1024 to 16384 bytes in `create-server.toml`. The old cap rejected most large builds on upload; the wider packets keep the transfer from crawling now that files can be eight times heavier.

### Ajouts

- **Brouilleur Magnetique** — Nouveau bloc qui neutralise les aimants a objets dans un rayon de 5 chunks (11x11 chunks, toute la hauteur). Les objets au sol dans le champ portent le drapeau NeoForge `PreventRemoteMovement`, respecte par les upgrades magnet de Sophisticated Backpacks et Storage, l'aimant du powerpack Immersive Engineering et le familier Greedy d'Occultism ; le ramassage a la main n'est pas affecte. `create_sa:copper_magnet` ignore la convention et est contre separement. Fabrique dans un Mechanical Crafter 5x5 a partir de bobines et aimants TFMG, de bobines de cuivre et d'un chassis en laiton.
- **Chaine Stellar Forge** — Le Dimensional Battlefield d'Occultism produit desormais des fragments au lieu des drops de boss finis : `arcadia:star_fragment` pour le Wither, `arcadia:dragon_shard` pour l'Ender Dragon. Quatre fragments alimentent une ligne d'assemblage sequentiel Create (3 boucles, deployeur / presse / bec verseur) pour donner une etoile du Nether ou un oeuf de dragon. Les combats de boss ne changent pas, un Wither tue a la main lache toujours ses 1-2 etoiles. Quatre nouvelles textures generees par `_gen_star.py`.

### Modifications

- **Plafond de taille des schematics releve** — `maxTotalSchematicSize` de 256 a 2048 Ko et `maxSchematicPacketSize` de 1024 a 16384 octets dans `create-server.toml`. L'ancien plafond rejetait la plupart des grandes constructions a l'upload ; les paquets plus larges evitent que le transfert traine maintenant que les fichiers peuvent etre huit fois plus lourds.

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

- **Duplicate CC: Tweaked removed** — Two CurseForge projects shipping the same computercraft mod id were installed together (official 1.113.1 and an unofficial 1.117.1 port). Kept the official project, removed the unofficial jar and its manifest entry (455 entries now).
- **Ore Excavation skyjade vein** — The drilling recipe output pointed to the nonexistent `deep_aether:raw_skyjade`; corrected to `deep_aether:skyjade`.
- **Winged/Unbound affix exclusivity** — The mutual exclusion between the two creative-flight Apotheosis affixes was only declared one-way; `winged.json` now also excludes `unbound`, matching the documented intent.
- **Spawner blacklist dangling entry** — Removed `animalgarden_owl:owl` from the datapack tag and its KubeJS mirror (the owl mod is not installed).
- **FancyMenu missing textures** — Restored `lordhosting.png`, `lordhosting_hover.png`, `loading1.png`, `loading2.png` into `config/fancymenu/assets/arcadia/` (the menu referenced them and logged texture errors).
- **French item lang gap** — Added the missing `item.arcadia.incomplete_netherite_block` key to `fr_fr.json`.
- **Stale documentation** — `modified_recipes.txt` listed dndecor bolt materials that do not exist in the installed mod version; rewrote the list with the real materials and dropped the owl from the farm-animal list.
- **Privacy hardening** — Untracked per-user runtime files from git (`arcadiaadminpanel/logins.json`, voicechat `username-cache.json` and `player-volumes.properties`) and added them to `.gitignore`; deleted orphan configs for uninstalled mods (`nvidium-config.json`, `emi.json`, `connector.json`), a stale 1.3 MB quest lang export, leftover JEI test-world state in defaultconfigs, and disabled the emotecraft debug flag.
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

- **Doublon CC: Tweaked supprimé** — Deux projets CurseForge livrant le même mod id computercraft étaient installés ensemble (officiel 1.113.1 et port non officiel 1.117.1). Le projet officiel est conservé, le jar non officiel et son entrée manifest sont retirés (455 entrées désormais).
- **Veine skyjade Ore Excavation** — La recette de forage pointait vers `deep_aether:raw_skyjade` qui n'existe pas ; corrigé en `deep_aether:skyjade`.
- **Exclusivité des affixes Winged/Unbound** — L'exclusion mutuelle des deux affixes de vol créatif Apotheosis n'était déclarée que dans un sens ; `winged.json` exclut maintenant aussi `unbound`, conformément à l'intention documentée.
- **Entrée morte de la blacklist des spawners** — `animalgarden_owl:owl` retiré du tag datapack et de son miroir KubeJS (le mod owl n'est pas installé).
- **Textures FancyMenu manquantes** — `lordhosting.png`, `lordhosting_hover.png`, `loading1.png`, `loading2.png` restaurées dans `config/fancymenu/assets/arcadia/` (le menu les référençait et loggait des erreurs de texture).
- **Trou de langue français** — Clé manquante `item.arcadia.incomplete_netherite_block` ajoutée à `fr_fr.json`.
- **Documentation obsolète** — `modified_recipes.txt` listait des matériaux de boulons dndecor inexistants dans la version installée ; liste réécrite avec les vrais matériaux et owl retiré de la liste des animaux de ferme.
- **Renforcement vie privée** — Fichiers runtime par utilisateur retirés du suivi git (`arcadiaadminpanel/logins.json`, `username-cache.json` et `player-volumes.properties` de voicechat) et ajoutés au `.gitignore` ; suppression des configs orphelines de mods non installés (`nvidium-config.json`, `emi.json`, `connector.json`), d'un export lang de quêtes obsolète de 1,3 Mo, des états JEI de mondes de test dans defaultconfigs, et désactivation du flag debug d'emotecraft.
- **Nettoyage du dépôt** — Suppression de 21 fichiers de sauvegarde `.toml.bak` obsolètes dans `config/`, ~170 logs archivés (`logs/*.log.gz`), anciens rapports de déconnexion dans `debug/`, deux heap dumps spark de 500+ Mo (`config/spark/heap-*.hprof`), le dossier vide `rapport_test/`, et l'obsolète `translation_workspace/` de 99 Mo (outillage de traduction plus utilisé).

### Performance

- **Hotspots du thread de rendu** — Mitigations au niveau config des hotspots du thread de rendu identifiés via profiling spark (héritées de la série de commits précédente, documentées ici).

---
