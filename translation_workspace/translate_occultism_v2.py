#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass 2: Translate remaining unhandled occultism entries."""
import json
import re

OUTPUT = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2/agent_output/occultism.json"
INPUT = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2/untranslated_per_mod/occultism.json"

with open(OUTPUT, "r", encoding="utf-8") as f:
    cur = json.load(f)
with open(INPUT, "r", encoding="utf-8") as f:
    src = json.load(f)

# === Direct translations to add (handles all remaining non-book + many book entries) ===
ADD = {
    # advancements stub
    "Infusion": "Infusion",
    "Possession": "Possession",
    # condition fixes
    "This Condition is never fulfilled. Use a different condition in the recipe to make the ritual work.":
        "Cette condition n'est jamais remplie. Utilisez une autre condition dans la recette pour que le rituel fonctionne.",
    "Perform the ritual in a biome with the tag %s! It was performed in the biome %s which does not have the tag.":
        "Effectuez le rituel dans un biome ayant le tag %s ! Il a été effectué dans le biome %s, qui n'a pas ce tag.",
    "Nether": "Nether",
    "Afrit": "Afrit",
    "Foliot": "Foliot",
    "Marid": "Marid",
    "Drikwing": "Drikwing",
    "Mode": "Mode",
    "Pentacle": "Pentacle",
    "Foliot %s": "Foliot %s",
    # entity etc.
    "Enter the tags to filter for separated by \";\".\nE.g.: \"c:ores;*logs*\".\nUse \"*\" to match any character, e.g. \"*ore*\" to match ore tags from any mod. To filter for items, prefix the item id with \"item:\", E.g.: \"item:minecraft:chest\".":
        "Entrez les tags à filtrer séparés par « ; ».\nEx. : « c:ores;*logs* ».\nUtilisez « * » pour correspondre à n'importe quel caractère, par ex. « *ore* » pour faire correspondre les tags de minerai de tout mod. Pour filtrer des objets, préfixez l'ID de l'objet par « item: », ex. : « item:minecraft:chest ».",
    "Can replace any chalk glyph.\nShift + Right Click in a glyph to erase.\nIt can take on the appearance of any colored glyph.":
        "Peut remplacer n'importe quel glyphe à la craie.\nMaj + clic droit sur un glyphe pour l'effacer.\nIl peut prendre l'apparence de n'importe quel glyphe coloré.",
    "Can replace any chalk glyph.\nShift + Right Click in a glyph to erase.\nIt can take on the appearance of any foundation glyph.":
        "Peut remplacer n'importe quel glyphe à la craie.\nMaj + clic droit sur un glyphe pour l'effacer.\nIl peut prendre l'apparence de n'importe quel glyphe de fondation.",
    "Consumption may allow to see beyond the veil ... it may also cause general un-wellness. (Can grants Third Eye when eating)":
        "La consommation peut permettre de voir au-delà du voile... elle peut aussi causer un malaise général. (Peut conférer le Troisième Œil à la consommation)",
    "Consumption allows to see beyond the veil ... and a whole lot of other effects. (Grants Third Eye when eating)":
        "La consommation permet de voir au-delà du voile... et bien d'autres effets. (Confère le Troisième Œil à la consommation)",
    "Don't see anything?\nCheck the Troubleshooting page in the Dictionary of Spirits!\nIn the \"Getting Started\" tab find the Divination Rod item.\n":
        "Vous ne voyez rien ?\nConsultez la page de dépannage dans le Dictionnaire des esprits !\nDans l'onglet « Premiers pas », trouvez l'objet Baguette de divination.\n",
    "Obtained when completing a ritual without an output item if there is an upside-down sacrificial bowl within three blocks above of the central ritual bowl.":
        "Obtenu en complétant un rituel sans objet de résultat si un bol sacrificiel renversé se trouve à moins de trois blocs au-dessus du bol rituel central.",
    "Right-Click to store all your experience points.\nShift-Right-Click to receive all stored experience points.\nA small tax may apply due to numerical approximations.\n":
        "Clic droit pour stocker tous vos points d'expérience.\nMaj + clic droit pour recevoir tous les points stockés.\nUne petite taxe peut s'appliquer due aux approximations numériques.\n",
    "Purified Demon's Dream Essence, no longer provides any of the negative effects. (Grants Third Eye when eating)":
        "Essence du Rêve du Démon purifiée, ne procure plus d'effets négatifs. (Confère le Troisième Œil à la consommation)",
    # ritual_dummy.tooltip variations
    "The Dark Iesnium Ritual Bowl performs any ritual in only a quarter of the normal time. All other things will work like the Dark Golden Ritual Bowl.":
        "Le bol rituel d'iesnium sombre effectue n'importe quel rituel en seulement un quart du temps normal. Tout le reste fonctionne comme le bol rituel doré sombre.",
    "Allows the imprisoned Afrit to simulate spiritual battles to generate resources from mobs.":
        "Permet à l'Afrit emprisonné de simuler des combats spirituels pour générer des ressources à partir de mobs.",
    "Place a dimensional mineshaft/battlefield or a spirit worker above it to enable depositing results directly into an inventory below that block.":
        "Placez un puits/champ de bataille dimensionnel ou un esprit travailleur au-dessus pour déposer les résultats directement dans un inventaire sous ce bloc.",
    "This satchel allows you to open your ender chest without placing a block in the world, and also allows inventory sharing.":
        "Cette besace vous permet d'ouvrir votre coffre de l'Ender sans placer de bloc dans le monde, et permet aussi le partage d'inventaire.",
    "The Entity Wormhole is a basic teleportation device. Link with a compass to teleport player, mobs or items when touch this small portal.":
        "Le vortex d'entités est un dispositif de téléportation basique. Liez-le à une boussole pour téléporter joueur, mobs ou objets au contact de ce petit portail.",
    "The Dark Entity Wormhole is a basic teleportation device. Link with a compass to teleport player, mobs or items when touch this small portal.":
        "Le vortex d'entités sombre est un dispositif de téléportation basique. Liez-le à une boussole pour téléporter joueur, mobs ou objets au contact de ce petit portail.",
    "The Iesnium butcher knife is perfect for cutting heads and skulls, and continues to perform the functions of a regular butcher knife.":
        "Le couteau de boucher en iesnium est parfait pour trancher têtes et crânes, et conserve les fonctions d'un couteau de boucher classique.",
    "The Iesnium Ritual Bowl performs any ritual in only a quarter of the normal time. All other things will work like the Golden Ritual Bowl.":
        "Le bol rituel en iesnium effectue n'importe quel rituel en seulement un quart du temps normal. Tout le reste fonctionne comme le bol rituel doré.",
    "The spirit grindstone is an improvement on the common grindstone, which removes curses (keeping other enchantments) and repairs items more efficiently.":
        "La meule des esprits est une amélioration de la meule classique : elle retire les malédictions (en conservant les autres enchantements) et répare les objets plus efficacement.",
    "The Storage Stabilizer allows to store more items in the dimensional storage accessor.":
        "Le stabilisateur de stockage permet de stocker plus d'objets dans l'accesseur de stockage dimensionnel.",
    "The Dark Storage Stabilizer allows to store more items in the dimensional storage accessor.":
        "Le stabilisateur de stockage sombre permet de stocker plus d'objets dans l'accesseur de stockage dimensionnel.",
    "An Afrit will upgrade the apprentice ritual satchel to build pentacles all at once for the summoner. This recipe keep the items inside the satchel.":
        "Un Afrit améliorera la besace rituelle d'apprenti pour construire les pentacles d'un seul coup. Cette recette conserve les objets à l'intérieur.",
    "The Bat familiars provide night vision to their master.":
        "Les familiers chauve-souris confèrent la vision nocturne à leur maître.",
    "The Beholder familiars highlight nearby entities with a glow effect and shoot laser rays at enemies.":
        "Les familiers Beholder mettent en surbrillance les entités proches avec un effet lumineux et tirent des rayons lasers sur les ennemis.",
    "The Blacksmith familiars take stone their master mines and uses it to repair equipment.":
        "Les familiers Forgeron prennent la pierre minée par leur maître et l'utilisent pour réparer l'équipement.",
    "The Chimera familiars can be fed to grow in size and gain attack speed and damage. Once big enough, players can ride them.":
        "Les familiers Chimère peuvent être nourris pour grandir et gagner en vitesse d'attaque et en dégâts. Une fois assez grands, les joueurs peuvent les chevaucher.",
    "The Cthulhu familiars provide water breathing to their master.":
        "Les familiers Cthulhu permettent à leur maître de respirer sous l'eau.",
    "The Deer familiars provide jump boost to their master.":
        "Les familiers Cerf confèrent le saut amélioré à leur maître.",
    "The Devil familiars provide fire resistance to their master.":
        "Les familiers Diable confèrent la résistance au feu à leur maître.",
    "The Dragon familiars provide increased experience gain to their master.":
        "Les familiers Dragon augmentent le gain d'expérience de leur maître.",
    "The Fairy familiar keeps other familiars from dying, drains enemies of their life force and heals its master and their familiars.":
        "Le familier Fée empêche les autres familiers de mourir, draine la force vitale des ennemis et soigne son maître et ses familiers.",
    "The Greedy familiars pick up items for their master. When stored in a familiar ring, they increase the pickup range (like an item magnet).":
        "Les familiers Avide ramassent les objets pour leur maître. Quand ils sont rangés dans un anneau de familier, ils augmentent la portée de ramassage (comme un aimant à objets).",
    "The Guardian familiars prevent their master's violent demise.":
        "Les familiers Gardien empêchent la fin violente de leur maître.",
    "The Headless ratman familiars increase their master's attack damage against enemies of the kind it stole the head from.":
        "Les familiers Homme-rat sans tête augmentent les dégâts d'attaque de leur maître contre les ennemis du type dont il a volé la tête.",
    "The Drikwings will provide their owner with limited flight abilities when nearby.":
        "Les Drikwings offriront à leur propriétaire des capacités de vol limitées lorsqu'ils sont à proximité.",
    "The Parrot familiars behave exactly like tamed parrots.":
        "Les familiers Perroquet se comportent exactement comme des perroquets apprivoisés.",
    "Eldritch Spirits will forge an Celestial Chalice, that performs any ritual instantly. Here is your trophy.":
        "Les esprits Eldritch forgeront un calice céleste, qui effectue n'importe quel rituel instantanément. Voici votre trophée.",
    "Eldritch Spirits will forge an Eldritch Chalice, that performs any ritual instantly. Here is your trophy.":
        "Les esprits Eldritch forgeront un calice Eldritch, qui effectue n'importe quel rituel instantanément. Voici votre trophée.",
    "Eldritch Spirits will forge a Stabilized Dimensional Storage Actuator, works as an actuator with maximum stabilizers in only one block. This recipe keep the items inside the actuator.":
        "Les esprits Eldritch forgeront un actionneur de stockage dimensionnel stabilisé, fonctionnant comme un actionneur avec stabilisateurs maximum en un seul bloc. Cette recette conserve les objets à l'intérieur.",
    "Eldritch Spirits will forge a Dark Stabilized Dimensional Storage Actuator, works as an actuator with maximum stabilizers in only one block. This recipe keep the items inside the actuator.":
        "Les esprits Eldritch forgeront un actionneur de stockage dimensionnel stabilisé sombre, fonctionnant comme un actionneur avec stabilisateurs maximum en un seul bloc. Cette recette conserve les objets à l'intérieur.",
    "The Possessed Bee will drop cursed honey.":
        "L'Abeille possédée laissera tomber du miel maudit.",
    "The Possessed Blaze will drop at least two blaze rods and various nether-related items, including blocks, plants, and (very rarely) ancient debris.":
        "Le Blaze possédé laissera tomber au moins deux bâtons de blaze et divers objets liés au Nether, notamment des blocs, des plantes et (très rarement) des débris antiques.",
    "The Possessed Elder Guardian will drop at least one nautilus shell when killed, also can drop heart of the sea and the common drops.":
        "Le Gardien Ancien possédé laissera tomber au moins une coquille de nautile une fois tué, peut aussi laisser tomber le cœur de la mer et les butins habituels.",
    "The Possessed Enderman will always drop at least one ender pearl when killed.":
        "L'Enderman possédé laissera toujours tomber au moins une perle de l'Ender une fois tué.",
    "The Possessed Endermite drops End Stone.":
        "L'Endermite possédé laisse tomber de la pierre de l'End.",
    "The Possessed Ghast will always drop at least one ghast tear when killed.":
        "Le Ghast possédé laissera toujours tomber au moins une larme de Ghast une fois tué.",
    "The Goat of Mercy will drop the Cruelty Essence.":
        "La Chèvre de la Miséricorde laissera tomber l'Essence de Cruauté.",
    "The Possessed Guardian will drop stuff from coral reef.":
        "Le Gardien possédé laissera tomber du butin des récifs coralliens.",
    "The Possessed Hoglin has a chance to drop smithing template of netherite upgrade when killed.":
        "Le Hoglin possédé a une chance de laisser tomber un patron de forge d'amélioration en netherite une fois tué.",
    "Summons the strong and invulnerable iesnium golem to defend a region.":
        "Invoque le golem d'iesnium puissant et invulnérable pour défendre une région.",
    "The Possessed Phantom will always drop at least one phantom membrane when killed and is easy to trap.":
        "Le Fantôme possédé laissera toujours tomber au moins une membrane de fantôme une fois tué et est facile à piéger.",
    "Summons a common random passive animal. (Possibilities: chicken, cow, pig, sheep, squid, wolf)":
        "Invoque un animal passif aléatoire commun. (Possibilités : poule, vache, cochon, mouton, calamar, loup)",
    "Summons a rideable random passive animal. (Possibilities: pig, camel, donkey, horse, skeleton horse, zombie horse, llama, trader llama, mule, strider)":
        "Invoque un animal passif aléatoire chevauchable. (Possibilités : cochon, chameau, âne, cheval, cheval squelette, cheval zombie, lama, lama de marchand, mule, strider)",
    "Summons a small random passive animal. (Possibilities: allay, bat, bee, parrot, cat, ocelot, fox, rabbit)":
        "Invoque un petit animal passif aléatoire. (Possibilités : allay, chauve-souris, abeille, perroquet, chat, ocelot, renard, lapin)",
    "Summons a special random passive animal. (Possibilities: armadillo, mooshroom, panda, polar bear, goat, iron golem, sniffer)":
        "Invoque un animal passif aléatoire spécial. (Possibilités : tatou, champimeuh, panda, ours blanc, chèvre, golem de fer, renifleur)",
    "Summons a Water random passive animal. (Possibilities: axolotl, frog, dolphin, cod, salmon, tropical fish, pufferfish, squid, glow squid, tadpole, turtle, snow golem)":
        "Invoque un animal aquatique passif aléatoire. (Possibilités : axolotl, grenouille, dauphin, morue, saumon, poisson tropical, poisson-globe, calamar, calamar luminescent, têtard, tortue, golem de neige)",
    "The Possessed Shulker will always drop at least one shulker shell when killed.":
        "Le Shulker possédé laissera toujours tomber au moins une coquille de Shulker une fois tué.",
    "The Possessed Skeleton is immune to daylight and always drop at least one Skeleton Skull when killed.":
        "Le Squelette possédé est immunisé à la lumière du jour et laisse toujours tomber au moins un crâne de squelette une fois tué.",
    "Possess a Drikwing Familiar that can be tamed by anyone, not just the summoner.":
        "Possède un familier Drikwing qui peut être apprivoisé par n'importe qui, pas seulement par l'invocateur.",
    "Possess a Parrot that can be tamed by anyone, not just the summoner.":
        "Possède un perroquet qui peut être apprivoisé par n'importe qui, pas seulement par l'invocateur.",
    "Summons a villager or wandering Trader.":
        "Invoque un villageois ou un marchand ambulant.",
    "The Possessed Warden will always drop at least six echo shard and can drop anothers ancient stuff (smithing templates and discs) when killed.":
        "Le Warden possédé laissera toujours tomber au moins six éclats d'écho et peut laisser tomber d'autres objets anciens (patrons de forge et disques) une fois tué.",
    "The Possessed Weak Shulker will drop at least one chorus fruit when killed and can drop shulker shell.":
        "Le Shulker faible possédé laissera tomber au moins un fruit de chorus une fois tué et peut laisser tomber une coquille de Shulker.",
    "The Possessed Witch will drop a special filled bottle.":
        "La Sorcière possédée laissera tomber une fiole remplie spéciale.",
    "The Possessed Zombified Piglin will drop demonic meat.":
        "Le Cochon zombifié possédé laissera tomber de la viande démoniaque.",
    "The Crusher is a spirit summoned to crush ores into dusts, effectively (more than) doubling the metal output.\n§7§oNote: Some recipes may require higher or lower tier crushers.":
        "Le Broyeur est un esprit invoqué pour broyer les minerais en poussières, doublant (et plus) efficacement le rendement en métal.\n§7§oNote : certaines recettes peuvent nécessiter des broyeurs de palier supérieur ou inférieur.",
    "The Crystallizer is a spirit summoned to turn gem dusts back to gems and can extract extra gems from ores.\n§7§oNote: Some recipes may require higher or lower tier crystallizers.":
        "Le Cristalliseur est un esprit invoqué pour reconvertir les poussières de gemmes en gemmes et peut extraire des gemmes supplémentaires des minerais.\n§7§oNote : certaines recettes peuvent nécessiter des cristalliseurs de palier supérieur ou inférieur.",
    "The Smelter is a spirit summoned to make furnace, blast furnace, smoker and campfire recipes without using fuel and faster depending of the spirit.":
        "La Fonderie est un esprit invoqué pour exécuter les recettes de four, haut-fourneau, fumoir et feu de camp sans utiliser de carburant, plus rapidement selon l'esprit.",
    "Summons a Demonic Husband to support you: He will fight for you, help with cooking, and extend potion durations.":
        "Invoque un époux démoniaque pour vous soutenir : il combattra pour vous, vous aidera à cuisiner et prolongera la durée des potions.",
    "Summons a Demonic Wife to support you: She will fight for you, help with cooking, and extend potion durations.":
        "Invoque une épouse démonique pour vous soutenir : elle combattra pour vous, vous aidera à cuisiner et prolongera la durée des potions.",
    "The Crusher is a spirit summoned to crush ores into dusts, effectively doubling the metal output.\n§7§oNote: Some recipes may require higher or lower tier crushers.":
        "Le Broyeur est un esprit invoqué pour broyer les minerais en poussières, doublant efficacement le rendement en métal.\n§7§oNote : certaines recettes peuvent nécessiter des broyeurs de palier supérieur ou inférieur.",
    "The Gambler bets any gem for some other gems and nuggets, a trader with a taste of randomness":
        "Le Parieur mise n'importe quelle gemme contre d'autres gemmes et pépites, un marchand au goût du hasard",
    "The Machine Operator automatically transfers items between dimensional storage systems and connected inventories and machines.":
        "L'opérateur de machine transfère automatiquement les objets entre les systèmes de stockage dimensionnel et les inventaires et machines connectés.",
    "The Farmer will harvest crops in it's working area and deposit the dropped items into the specified chest.":
        "Le Fermier récoltera les cultures dans sa zone de travail et déposera les objets dans le coffre spécifié.",
    "The Lumberjack will harvest trees in it's working area and deposit the dropped items into the specified chest.":
        "Le Bûcheron abattra les arbres dans sa zone de travail et déposera les objets dans le coffre spécifié.",
    "The Otherworld Sapling Trader trades natural otherworld saplings for stable ones, that can be harvested without the third eye.":
        "Le marchand de pousses de l'Autre Monde échange des pousses naturelles contre des pousses stables, récoltables sans le Troisième Œil.",
    "The Transporter will move all items it can access from one inventory to another, including machines.":
        "Le Transporteur déplacera tous les objets accessibles d'un inventaire à un autre, y compris les machines.",
    "The Wild Horde Drowned consists of a few drowneds that drop items related to ocean trails.":
        "La horde sauvage de Noyés consiste en quelques noyés qui font tomber des objets liés aux pistes océaniques.",
    "The Wild Horde Husk consists of a few husks that drop items related to desert trails.":
        "La horde sauvage de Husks consiste en quelques husks qui font tomber des objets liés aux pistes du désert.",
    "Summons a group of common random passive animal. (Possibilities: chicken, cow, pig, sheep, squid, wolf)":
        "Invoque un groupe d'animaux passifs aléatoires communs. (Possibilités : poule, vache, cochon, mouton, calamar, loup)",
    "Summons a group of rideable random passive animal. (Possibilities: pig, camel, donkey, horse, skeleton horse, zombie horse, llama, trader llama, mule, strider)":
        "Invoque un groupe d'animaux passifs aléatoires chevauchables. (Possibilités : cochon, chameau, âne, cheval, cheval squelette, cheval zombie, lama, lama de marchand, mule, strider)",
    "Summons a group of small random passive animal. (Possibilities: allay, bat, bee, parrot, cat, ocelot, fox, rabbit)":
        "Invoque un groupe de petits animaux passifs aléatoires. (Possibilités : allay, chauve-souris, abeille, perroquet, chat, ocelot, renard, lapin)",
    "Summons a group of special random passive animal. (Possibilities: armadillo, mooshroom, panda, polar bear, goat, iron golem, sniffer)":
        "Invoque un groupe d'animaux passifs aléatoires spéciaux. (Possibilités : tatou, champimeuh, panda, ours blanc, chèvre, golem de fer, renifleur)",
    "Summons a group of Water random passive animal. (Possibilities: axolotl, frog, dolphin, cod, salmon, tropical fish, pufferfish, squid, glow squid, tadpole, turtle, snow golem)":
        "Invoque un groupe d'animaux aquatiques passifs aléatoires. (Possibilités : axolotl, grenouille, dauphin, morue, saumon, poisson tropical, poisson-globe, calamar, calamar luminescent, têtard, tortue, golem de neige)",
    "The Wild Horde Silverfish consists of a few silverfishs that drop items related to ruins trails.":
        "La horde sauvage de Poissons d'argent consiste en quelques poissons d'argent qui font tomber des objets liés aux pistes des ruines.",
    # ritual_satchel
    "A basic ritual satchel that can place ritual circles block by block.\nRight-Click a preview block to place it out of the satchel.\nShift-Right-Click to open the satchel and add ritual ingredients.\nAn item with durability will be used until only 1 durability remains, which will stop the glint effect.\n":
        "Une besace rituelle de base qui peut placer les cercles rituels bloc par bloc.\nClic droit sur un bloc d'aperçu pour le placer depuis la besace.\nMaj + clic droit pour ouvrir la besace et ajouter les ingrédients rituels.\nUn objet avec durabilité sera utilisé jusqu'à 1 point restant, ce qui arrêtera l'effet scintillant.\n",
    "An improved ritual satchel that can place an entire ritual circle at once.\nRight-Click any preview block to place all preview blocks out of the satchel.\nShift-Right-Click to open the satchel and add ritual ingredients.\nRight-Click a Golden Bowl to remove the ritual circle and collect the ingredients in the satchel.\n":
        "Une besace rituelle améliorée qui peut placer un cercle rituel entier d'un coup.\nClic droit sur n'importe quel bloc d'aperçu pour placer tous les blocs depuis la besace.\nMaj + clic droit pour ouvrir la besace et ajouter les ingrédients rituels.\nClic droit sur un bol doré pour retirer le cercle rituel et récolter les ingrédients dans la besace.\n",
    # soul_shattered
    "Alternatively, you can use the right-click or the dimensional battlefield to obtain extra loot.":
        "Vous pouvez aussi utiliser le clic droit ou le champ de bataille dimensionnel pour obtenir du butin supplémentaire.",
    "Obtain this by killing mobs with a weapon enchanted with fracture soul.\nCan be used to resurrect the mob.":
        "À obtenir en tuant des mobs avec une arme enchantée avec fracture d'âme.\nPeut être utilisé pour ressusciter le mob.",
    # sweet_honey_heart
    "§fMade with love, sugar and evilness\n§7Grants a great Absorption when eating\n§5Get it giving a Cursed Honey to a Demonic Partner":
        "§fFait avec amour, sucre et méchanceté\n§7Confère une grande Absorption à la consommation\n§5À obtenir en donnant du miel maudit à un partenaire démoniaque",
    # JEI ingredient
    "Can be obtained from a Otherworld Sapling Trader. Can be seen and harvested without §6Third Eye§r. See §6Dictionary of Spirits§r for information on how to summon the trader.":
        "Peut être obtenu auprès du marchand de pousses de l'Autre Monde. Peut être vu et récolté sans §6Troisième Œil§r. Consultez le §6Dictionnaire des esprits§r pour savoir comment invoquer le marchand.",
    "The Goat Familiar can be obtained by feeding a Golden Apple to a Chimera Familiar. See §6Dictionary§r §6of§r §6Spirits§r for more information.":
        "Le familier Chèvre peut être obtenu en donnant une pomme d'or à un familier Chimère. Consultez le §6Dictionnaire§r §6des§r §6esprits§r pour plus d'informations.",
    "The Shub Niggurath Familiar can be obtained by bringing a Goat Familiar to a Forest Biome and clicking the Goat first with any Black Dye, then Flint and then an Eye of Ender. See §6Dictionary§r §6of§r §6Spirits§r for more information.":
        "Le familier Shub-Niggurath peut être obtenu en amenant un familier Chèvre dans un biome de forêt et en cliquant sur la chèvre avec d'abord un colorant noir, puis du silex et enfin un œil de l'Ender. Consultez le §6Dictionnaire§r §6des§r §6esprits§r pour plus d'informations.",
}

# Tag c entries (truncated processing)
ADD.update({
    "Iesnium Storage Blocks": "Blocs de stockage d'iesnium",
})

# Update the output
for k, v in src.items():
    cur_v = cur.get(k)
    if cur_v == v and v in ADD:
        cur[k] = ADD[v]

# === Now handle the BIG book.dictionary_of_spirits batch with comprehensive translations ===

BOOK = {
    # craft rituals - spotlight texts
    "Unlike other rituals, creating a [](item://minecraft:bee_nest) is a service provided by [#](AA00AA)Wild Spirits[#]()\nand not bound any spirit to the final object. You sacrifice the items and the Wild Spirits\n uses his power to forge that item for you.\n\n":
        "Contrairement aux autres rituels, la création d'une [](item://minecraft:bee_nest) est un service rendu par les [#](AA00AA)Esprits sauvages[#]()\net aucun esprit n'est lié à l'objet final. Vous sacrifiez les objets et les Esprits sauvages\n utilisent leur pouvoir pour forger cet objet pour vous.\n\n",
    "Unlike other rituals, creating a [](item://minecraft:bell) is a service provided by [#](AA00AA)Wild Spirits[#]()\nand not bound any spirit to the final object. You sacrifice the items and the Wild Spirits\n uses his power to forge that item for you.\n\n":
        "Contrairement aux autres rituels, la création d'une [](item://minecraft:bell) est un service rendu par les [#](AA00AA)Esprits sauvages[#]()\net aucun esprit n'est lié à l'objet final. Vous sacrifiez les objets et les Esprits sauvages\n utilisent leur pouvoir pour forger cet objet pour vous.\n\n",
    "The [#](AA00AA)Afrit[#]() miner harvests ores, like djinni miners, and additionally\n mines some deepslate ores. This miner is faster and more efficient\n than the djinnis, thus damaging the magic lamp even more slowly.\n":
        "Le mineur [#](AA00AA)Afrit[#]() récolte les minerais, comme les mineurs djinns, et mine en plus\n certains minerais d'ardoise des abîmes. Ce mineur est plus rapide et plus efficace\n que les djinns, et endommage donc la lampe magique encore plus lentement.\n",
    "By compressing [#](AA00AA)MMM[#]() you get an extremely powerful miner, but something starts watching you.\n [](item://occultism:mining_dim_core) are a extremely rarely mined by a Marid.\n":
        "En compressant [#](AA00AA)MMM[#]() vous obtenez un mineur extrêmement puissant, mais quelque chose commence à vous observer.\n Les [](item://occultism:mining_dim_core) sont extrêmement rarement minés par un Marid.\n",
    "Unlike other rituals, creating a [](item://minecraft:budding_amethyst) is a service provided by [#](AA00AA)Wild Spirits[#]() and not bound any spirit to the\n final object. You sacrifice the items and the Wild Spirits uses his power to forge that item for you.\n":
        "Contrairement aux autres rituels, la création d'une [](item://minecraft:budding_amethyst) est un service rendu par les [#](AA00AA)Esprits sauvages[#]() et aucun esprit n'est lié à\n l'objet final. Vous sacrifiez les objets et les Esprits sauvages utilisent leur pouvoir pour forger cet objet pour vous.\n",
    "The dimensional matrix is the entry point to a small dimension used for storing items.\n A [#](AA00AA)Djinni[#]() bound to the matrix keeps the dimension stable, often supported by additional\n spirits in storage stabilizers, to increase the dimension size.\n":
        "La matrice dimensionnelle est le point d'entrée vers une petite dimension utilisée pour le stockage d'objets.\n Un [#](AA00AA)Djinn[#]() lié à la matrice garde la dimension stable, souvent soutenu par des esprits supplémentaires\n dans les stabilisateurs de stockage, pour augmenter la taille de la dimension.\n",
    "If you want to save your miners before they break, check \"Server Configuration > Items\".\n By setting the \"Save miners before breaking\" option to \"on\", a miner will go to the output\n of the dimensional mineshaft when it reaches 1 durability. The effects of enchantments can also be turned off.\n":
        "Si vous souhaitez sauver vos mineurs avant qu'ils ne se brisent, consultez « Configuration serveur > Objets ».\n En activant l'option « Sauver les mineurs avant la casse », un mineur ira dans la sortie\n du puits dimensionnel à 1 point de durabilité. Les effets des enchantements peuvent aussi être désactivés.\n",
    "Void mining": "Minage du vide",
    "The dimensional mineshaft will discard any items it cannot store, so it is important\nto regularly empty the mineshaft, either manually, with hoppers or using a transporter spirit.\\\nInteractions per side:\n+ Top -> lamp slot;\n+ Bottom -> ores slots;\n+ Other -> all slots;\n":
        "Le puits dimensionnel jettera tout objet qu'il ne peut stocker, il est donc important\nde le vider régulièrement, manuellement, avec des entonnoirs ou via un esprit transporteur.\\\nInteractions par face :\n+ Dessus -> emplacement lampe ;\n+ Dessous -> emplacements minerais ;\n+ Autres -> tous les emplacements ;\n",
    "You've noticed that your miner can be enchanted? Here's how effective it is!\\\n **Efficiency:** Increase the progress bar by the smaller of two RNB;\\\n **Fortune:** Mine a number of extra results equals smaller of three RNB;\\\n **Silk touch:** Multiply the count of mined result by 1 plus a RNB;\\\n RNB = random number between 0 and the enchantment level.\n":
        "Vous avez remarqué que votre mineur peut être enchanté ? Voici son efficacité !\\\n **Efficacité :** augmente la barre de progression du plus petit de deux RNB ;\\\n **Fortune :** mine un nombre de résultats supplémentaires égal au plus petit de trois RNB ;\\\n **Toucher de soie :** multiplie le nombre de résultats minés par 1 plus un RNB ;\\\n RNB = nombre aléatoire entre 0 et le niveau d'enchantement.\n",
    "The **Unbreaking** and **Mending** enchantments function as vanilla.\n\\\n With other methods (mods) you can make your miner unusable (**unusing**)\n when it's close to breaking, or even truly unbreakable (**eternal**).\n":
        "Les enchantements **Solidité** et **Raccommodage** fonctionnent comme en vanilla.\n\\\n Avec d'autres méthodes (mods), vous pouvez rendre votre mineur inutilisable (**unusing**)\n quand il est proche de la casse, ou même véritablement incassable (**eternal**).\n",
    " The dimensional mineshaft has two interactions with redstone:\n 1. The spirit will stop working when receives a redstone signal;\n 2. A comparator can be used to extract a signal based on occupied slots and lamp durability.\n  Tip, if the comparator sends a power of 10, it is better to stop the operations.\n":
        " Le puits dimensionnel a deux interactions avec la redstone :\n 1. L'esprit cessera de travailler quand il reçoit un signal redstone ;\n 2. Un comparateur peut extraire un signal basé sur les emplacements occupés et la durabilité de la lampe.\n  Astuce : si le comparateur envoie une puissance de 10, mieux vaut arrêter les opérations.\n",
    " The dimensional mineshaft houses a [#](AA00AA)Djinni[#]() which opens up a stable connection into an\n  uninhabited dimension, perfectly suited for mining. While the portal is too small\n   to transfer humans, other spirits can use it to enter the mining dimension and bring back resources.\n\n":
        " Le puits dimensionnel abrite un [#](AA00AA)Djinn[#]() qui ouvre une connexion stable vers une\n  dimension inhabitée, parfaitement adaptée au minage. Le portail est trop petit\n   pour transporter des humains, mais d'autres esprits peuvent l'emprunter pour entrer dans la dimension minière et rapporter des ressources.\n\n",
    "The [#](AA00AA)Djinni[#]() miner harvests ores specifically. By discarding other blocks it is able to mine faster and\n more efficiently. The greater power of the djinni it damages the magic lamp relatively quickly.\n":
        "Le mineur [#](AA00AA)Djinn[#]() récolte spécifiquement les minerais. En écartant les autres blocs, il peut miner plus vite\n et plus efficacement. La puissance accrue du djinn endommage la lampe magique relativement rapidement.\n",
    "Forging an [](item://occultism:eldritch_chalice) is one service provide by [#](AA00AA)Eldritch Spirits[#](), this block will\n helps occult masters twist time, performing any ritual instantly.\\\n All other things will works like the Golden or Iesnium Ritual Bowl.\n":
        "Forger un [](item://occultism:eldritch_chalice) est un service rendu par les [#](AA00AA)Esprits Eldritch[#](), ce bloc aidera\n les maîtres occultes à plier le temps, effectuant n'importe quel rituel instantanément.\\\n Tout le reste fonctionne comme le bol rituel doré ou en iesnium.\n",
    "Also in the Celestial version.\n":
        "Aussi disponible en version céleste.\n",
    "Familiar Rings consist of a [](item://occultism:soul_gem), that contains a [#](AA00AA)Djinni[#](), mounted on a ring.\n The [#](AA00AA)Djinni[#]() in the ring allows the familiar captured in the soul gem to apply effects to the wearer.\n":
        "Les anneaux de familier consistent en une [](item://occultism:soul_gem) contenant un [#](AA00AA)Djinn[#](), montée sur un anneau.\n Le [#](AA00AA)Djinn[#]() dans l'anneau permet au familier capturé dans la gemme d'âme d'appliquer ses effets au porteur.\n",
    "To use a [](item://occultism:familiar_ring), simply capture a summoned (and tamed) familiar by [#](AA00AA)right-clicking[#](),\n and then wear the ring as [#](AA00AA)Curio[#]() to make use of the effects the familiar provides.\n\\\n\\\nWhen released from a familiar ring, the spirit will recognize the person releasing them as their new master.\n":
        "Pour utiliser un [](item://occultism:familiar_ring), capturez simplement un familier invoqué (et apprivoisé) par [#](AA00AA)clic droit[#](),\n puis portez l'anneau en [#](AA00AA)Curio[#]() pour bénéficier des effets que confère le familier.\n\\\n\\\nLorsqu'il est libéré d'un anneau de familier, l'esprit reconnaît la personne qui le libère comme son nouveau maître.\n",
    "Miner spirits use [](item://occultism:dimensional_mineshaft) to acquire resources from other dimensions.\n They are summoned and bound into magic lamps, which they can leave only through the mineshaft.\n The magic lamp degrades over time, once it breaks the spirit is released back to [#](AA00AA)The Other Place[#]().\n":
        "Les esprits mineurs utilisent les [](item://occultism:dimensional_mineshaft) pour acquérir des ressources d'autres dimensions.\n Ils sont invoqués et liés à des lampes magiques, qu'ils ne peuvent quitter que par le puits.\n La lampe magique se dégrade avec le temps ; une fois brisée, l'esprit est libéré vers [#](AA00AA)L'Autre Lieu[#]().\n",
    "To summon miner spirits, you first need to craft a [Magic Lamp](entry://getting_started/magic_lamps) to hold them.\n The key ingredient for that is [](item://occultism:spirit_attuned_gem).\n":
        "Pour invoquer des esprits mineurs, vous devez d'abord fabriquer une [Lampe magique](entry://getting_started/magic_lamps) pour les contenir.\n L'ingrédient clé est la [](item://occultism:spirit_attuned_gem).\n",
    "The [#](AA00AA)Foliot[#]() miner harvests block without much aim and returns anything it finds.\n The mining process is quite slow, due to this the Foliot expends only minor\n amounts of energy, damaging the lamp it is housed in slowly over time.\n":
        "Le mineur [#](AA00AA)Foliot[#]() récolte les blocs sans grand discernement et rapporte tout ce qu'il trouve.\n Le processus de minage est assez lent ; de ce fait, le Foliot dépense peu\n d'énergie, endommageant la lampe qui l'abrite lentement avec le temps.\n",
    "The [](item://occultism:iesnium_anvil) is a [#](AA00AA)Marid[#]() infusion.\nThis anvil has some improvements:\n1. Is unbreakable;\n2. Can exceed the maximum level of enchantments by 1;\n3. Marid will pay half of the showed level cost (round up);\n4. The cost increase of working with the same item is reduced;\n5. The maximum cost limit is increased;\n":
        "L'[](item://occultism:iesnium_anvil) est une infusion de [#](AA00AA)Marid[#]().\nCette enclume a plusieurs améliorations :\n1. Elle est incassable ;\n2. Peut dépasser de 1 le niveau maximum des enchantements ;\n3. Le Marid paie la moitié du coût en niveau affiché (arrondi au supérieur) ;\n4. L'augmentation du coût en travaillant le même objet est réduite ;\n5. La limite maximale de coût est augmentée ;\n",
    "The [](item://occultism:iesnium_sacrificial_bowl) is an [#](AA00AA)Afrit[#]() infusion\n that helps expert occultists save time,\n performing any ritual in only a quarter of the normal time.\n All other things will works like the Golden Ritual Bowl.\n":
        "L'[](item://occultism:iesnium_sacrificial_bowl) est une infusion d'[#](AA00AA)Afrit[#]()\n qui aide les occultistes experts à gagner du temps,\n effectuant n'importe quel rituel en seulement un quart du temps normal.\n Tout le reste fonctionne comme le bol rituel doré.\n",
    "For players who are on the path of otherrock, there is also the dark version.\n":
        "Pour les joueurs qui suivent la voie de la pierre d'ailleurs, il existe aussi la version sombre.\n",
    "Otherworld ores usually can only be mined with Otherworld metal tools.\n The [](item://occultism:infused_pickaxe) is a makeshift solution to this Chicken-and-Egg problem.\n Brittle spirit attuned gems house a [#](AA00AA)Djinni[#]() that allows harvesting the,\n but the durability is extremely low. A more durable version is the [Iesnium Pickaxe](entry://getting_started/iesnium_pickaxe).\n":
        "Les minerais d'outremonde ne peuvent généralement être minés qu'avec des outils en métal d'outremonde.\n La [](item://occultism:infused_pickaxe) est une solution de fortune à ce problème de la poule et de l'œuf.\n Les gemmes attunées fragiles abritent un [#](AA00AA)Djinn[#]() qui permet de les récolter,\n mais la durabilité est extrêmement faible. Une version plus résistante est la [Pioche en iesnium](entry://getting_started/iesnium_pickaxe).\n",
    "The [#](AA00AA)Marid[#]() miner is the most powerful miner spirit, it has the fasted mining speed and best magic lamp\n preservation. Unlike other miner spirits they also can mine the rarest ores, such as [](item://minecraft:ancient_debris) and [](item://occultism:iesnium_ore).\n":
        "Le mineur [#](AA00AA)Marid[#]() est l'esprit mineur le plus puissant ; il a la vitesse de minage la plus rapide et la meilleure préservation\n de la lampe magique. Contrairement aux autres esprits mineurs, il peut aussi miner les minerais les plus rares, tels que les [](item://minecraft:ancient_debris) et le [](item://occultism:iesnium_ore).\n",
    "Forging the [](item://occultism:chalk_rainbow) is a service provided by an [#](AA00AA)Eldritch Spirit[#]().\nThis chalk can replace any chalk, with extra features.\n1. Use a [](item://occultism:spirit_attuned_gem) to toggle the random color changes or\nuse any dye to set the color of glyph, items will not be consumed.\n2. Use this chalk in a glyph while crouched will erase the glyph, acting as a [](item://occultism:brush).\n3. Hold a dye in your other hand to define the color when placing the glyph.\n":
        "Forger la [](item://occultism:chalk_rainbow) est un service rendu par un [#](AA00AA)Esprit Eldritch[#]().\nCette craie peut remplacer n'importe quelle craie, avec des fonctions supplémentaires.\n1. Utilisez une [](item://occultism:spirit_attuned_gem) pour activer les changements de couleur aléatoires ou\nutilisez n'importe quel colorant pour fixer la couleur du glyphe ; les objets ne seront pas consommés.\n2. Utiliser cette craie sur un glyphe en étant accroupi effacera le glyphe, agissant comme une [](item://occultism:brush).\n3. Tenez un colorant dans l'autre main pour définir la couleur lors du placement du glyphe.\n",
    "Forging the [](item://occultism:chalk_void) is a service provided by an [#](AA00AA)Eldritch Spirit[#]().\nThis chalk has the same abilities as the [](item://occultism:chalk_rainbow)\n but the color flickering is white to black.\n":
        "Forger la [](item://occultism:chalk_void) est un service rendu par un [#](AA00AA)Esprit Eldritch[#]().\nCette craie a les mêmes capacités que la [](item://occultism:chalk_rainbow)\n mais l'oscillation de couleur va du blanc au noir.\n",
    "The Goggles will, however, not give the ability to harvest otherworld materials.\n That means when wearing goggles, an [Infused Pick](entry://getting_started/infused_pickaxe), or even better, an [Iesnium Pick](entry://getting_started/iesnium_pickaxe) needs to be\n used to break blocks in order to obtain their Otherworld variants.\n":
        "Les lunettes ne donnent toutefois pas la capacité de récolter les matériaux d'outremonde.\n Cela signifie qu'en portant les lunettes, une [Pioche imprégnée](entry://getting_started/infused_pickaxe), ou mieux encore, une [Pioche en iesnium](entry://getting_started/iesnium_pickaxe) doit être\n utilisée pour casser les blocs et obtenir leurs variantes d'outremonde.\n",
    "The [](item://occultism:otherworld_goggles) give the wearer permanent [#](AA00AA)Third Eye[#](), allowing to view even blocks hidden from those partaking of [Demon's Dream](entry://getting_started/demons_dream).\n\\\n\\\nThis elegantly solves the general issue of summoners being in a drugged haze, causing all sorts of havoc.\n":
        "Les [](item://occultism:otherworld_goggles) confèrent à leur porteur le [#](AA00AA)Troisième Œil[#]() permanent, permettant de voir même les blocs cachés à ceux qui consomment du [Rêve du Démon](entry://getting_started/demons_dream).\n\\\n\\\nCela résout élégamment le problème général des invocateurs plongés dans une brume narcotique, causant toutes sortes de désastres.\n",
    "Summoning a spirit into the lenses used to craft goggles is one of the\n first of the more complex rituals apprentice summoners usually attempt,\n showing that their skills are progressing beyond the basics.\n":
        "Invoquer un esprit dans les lentilles utilisées pour fabriquer les lunettes est l'un des\n premiers rituels plus complexes que les apprentis invocateurs tentent généralement,\n montrant que leurs compétences progressent au-delà des bases.\n",
    "Otherworld Goggles make use of a [#](AA00AA)Foliot[#]() bound into the lenses.\n The Foliot shares its ability to view higher planes with the wearer,\n thus allowing them to see Otherworld materials.\n":
        "Les lunettes d'outremonde utilisent un [#](AA00AA)Foliot[#]() lié aux lentilles.\n Le Foliot partage sa capacité à voir les plans supérieurs avec le porteur,\n lui permettant ainsi de voir les matériaux d'outremonde.\n",
    "Unlike other rituals, creating a [](item://minecraft:reinforced_deepslate) is a service provided by [#](AA00AA)Wild Spirits[#]() and not bound any spirit to the\n final object. You sacrifice the items and the Wild Spirits uses his power to forge that item for you.\n":
        "Contrairement aux autres rituels, la création de [](item://minecraft:reinforced_deepslate) est un service rendu par les [#](AA00AA)Esprits sauvages[#]() et aucun esprit n'est lié à\n l'objet final. Vous sacrifiez les objets et les Esprits sauvages utilisent leur pouvoir pour forger cet objet pour vous.\n",
    "A [#](AA00AA)Foliot[#]() is bound to the satchel, tasked with **slightly** warping reality. This allows to store more\n items in the satchel than its size would indicate, making it a practical travellers companion.\n":
        "Un [#](AA00AA)Foliot[#]() est lié à la besace, chargé de **légèrement** déformer la réalité. Cela permet de stocker plus\n d'objets dans la besace que sa taille ne le laisserait supposer, en faisant un compagnon de voyage pratique.\n",
    "Soul gems are diamonds set in precious metals, which are then infused with a [#](AA00AA)Djinni[#]().\n The spirit creates a small dimension that allows the temporary entrapment of living beings.\n Beings of great power or size cannot be stored, however.\n":
        "Les gemmes d'âme sont des diamants sertis dans des métaux précieux, puis imprégnés d'un [#](AA00AA)Djinn[#]().\n L'esprit crée une petite dimension qui permet l'emprisonnement temporaire d'êtres vivants.\n Les êtres de grand pouvoir ou de grande taille ne peuvent toutefois pas y être stockés.\n",
    "To capture an entity, [#](AA00AA)right-click[#]() it with the soul gem. \\\n[#](AA00AA)right-click[#]() again to release the entity.\n\\\n\\\nBosses cannot be captured.\n":
        "Pour capturer une entité, faites [#](AA00AA)clic droit[#]() dessus avec la gemme d'âme. \\\n[#](AA00AA)Clic droit[#]() à nouveau pour libérer l'entité.\n\\\n\\\nLes boss ne peuvent pas être capturés.\n",
    "Forging the [](item://occultism:storage_controller_stabilized) is one service provide by [#](AA00AA)Eldritch Spirits[#](),\n this block will helps occult masters twist space, placing the stabilizers in the same\n position as the actuator in some extra-planar dimension invisible even to the best eyes.\\\n By default this item receives two bonus stabilizer tier 5\\\n Other external stabilizers do not affect this block.\\\n The recipe keep items inside!\n":
        "Forger le [](item://occultism:storage_controller_stabilized) est un service rendu par les [#](AA00AA)Esprits Eldritch[#](),\n ce bloc aidera les maîtres occultes à plier l'espace, plaçant les stabilisateurs à la même\n position que l'actionneur dans une dimension extra-planaire invisible même aux meilleurs yeux.\\\n Par défaut, cet objet reçoit en bonus deux stabilisateurs de palier 5.\\\n Les autres stabilisateurs externes n'affectent pas ce bloc.\\\n La recette conserve les objets à l'intérieur !\n",
    "This simple storage stabilizer is inhabited by a [#](AA00AA)Foliot[#]() that supports the dimensional matrix\n in keeping the storage dimension stable, thus allowing to store more items.\n\\\n\\\nBy default each Tier 1 Stabilizer adds **64** item types and 512000 items storage capacity.\n":
        "Ce simple stabilisateur de stockage est habité par un [#](AA00AA)Foliot[#]() qui aide la matrice dimensionnelle\n à maintenir la dimension de stockage stable, permettant ainsi de stocker plus d'objets.\n\\\n\\\nPar défaut, chaque stabilisateur de palier 1 ajoute **64** types d'objets et 512 000 emplacements de stockage.\n",
    "This improved stabilizer is inhabited by a [#](AA00AA)Djinni[#]() that supports the dimensional matrix\n in keeping the storage dimension stable, thus allowing to store more items.\n\\\n\\\nBy default each Tier 2 Stabilizer adds **128** item types and 1024000 items storage capacity.\n":
        "Ce stabilisateur amélioré est habité par un [#](AA00AA)Djinn[#]() qui aide la matrice dimensionnelle\n à maintenir la dimension de stockage stable, permettant ainsi de stocker plus d'objets.\n\\\n\\\nPar défaut, chaque stabilisateur de palier 2 ajoute **128** types d'objets et 1 024 000 emplacements de stockage.\n",
    "This advanced stabilizer is inhabited by a [#](AA00AA)Afrit[#]() that supports the dimensional matrix\n in keeping the storage dimension stable, thus allowing to store more items.\n\\\n\\\nBy default each Tier 3 Stabilizer adds **256** item types and 2048000 items storage capacity.\n":
        "Ce stabilisateur avancé est habité par un [#](AA00AA)Afrit[#]() qui aide la matrice dimensionnelle\n à maintenir la dimension de stockage stable, permettant ainsi de stocker plus d'objets.\n\\\n\\\nPar défaut, chaque stabilisateur de palier 3 ajoute **256** types d'objets et 2 048 000 emplacements de stockage.\n",
    "This highly advanced storage stabilizer is inhabited by a [#](AA00AA)Marid[#]() that supports the dimensional matrix\n in keeping the storage dimension stable, thus allowing to store more items.\n\\\n\\\nBy default each Tier 4 Stabilizer adds **512** item types and 4098000 items storage capacity.\n":
        "Ce stabilisateur de stockage hautement avancé est habité par un [#](AA00AA)Marid[#]() qui aide la matrice dimensionnelle\n à maintenir la dimension de stockage stable, permettant ainsi de stocker plus d'objets.\n\\\n\\\nPar défaut, chaque stabilisateur de palier 4 ajoute **512** types d'objets et 4 098 000 emplacements de stockage.\n",
    "The stable wormhole allows access to a dimensional matrix from a remote destination.\n\\\n\\\nShift-click a [](item://occultism:storage_controller) to link it, then place the wormhole in the world to use it as a remote access point.\n":
        "Le vortex stable permet d'accéder à une matrice dimensionnelle depuis une destination éloignée.\n\\\n\\\nMaj + clic sur un [](item://occultism:storage_controller) pour le lier, puis placez le vortex dans le monde pour l'utiliser comme point d'accès distant.\n",
    "The storage actuator base imprisons a [#](AA00AA)Foliot[#]() responsible for\n interacting with items in a dimensional storage matrix.\n":
        "La base de l'actionneur de stockage emprisonne un [#](AA00AA)Foliot[#]() chargé\n d'interagir avec les objets dans une matrice de stockage dimensionnelle.\n",
    "All inventory system blocks have a dark version,\n they function exactly like their counterpart.\n":
        "Tous les blocs du système d'inventaire ont une version sombre,\n ils fonctionnent exactement comme leur équivalent.\n",
    "The [](item://occultism:storage_remote) can be linked to a [](item://occultism:storage_controller) by shift-clicking.\n The [#](AA00AA)Djinni[#]() bound to the accessor will then be able to\n access items from the actuator even from across dimensions.\n":
        "Le [](item://occultism:storage_remote) peut être lié à un [](item://occultism:storage_controller) par maj + clic.\n Le [#](AA00AA)Djinn[#]() lié à l'accesseur pourra alors\n accéder aux objets de l'actionneur même à travers les dimensions.\n",
    "Occultism offers two storage solutions: the first is based on satchels, portable inventories with different functions depending on the type.\n Some are already obtainable, while others will require evolve in the mod first.\n":
        "L'Occultisme propose deux solutions de stockage : la première est basée sur les besaces, des inventaires portables aux fonctions variées selon le type.\n Certaines sont déjà disponibles, tandis que d'autres nécessiteront d'évoluer dans le mod.\n",
    "The second option is to follow the entries below that show the rituals related to the Magic Storage system.\n For full step-by-step instructions on building the storage system, see the [Magic Storage](category://storage) category.\n":
        "La deuxième option est de suivre les entrées ci-dessous qui présentent les rituels liés au système de stockage magique.\n Pour des instructions complètes étape par étape sur la construction du système de stockage, consultez la catégorie [Stockage magique](category://storage).\n",
    "Unlike other rituals, creating a [](item://minecraft:wild_armor_trim_smithing_template) is a service provided by [#](AA00AA)Wild Spirits[#]() and not bound any spirit to the\n final object. You sacrifice the items and the Wild Spirits uses his power to forge that item for you.\n \\\n Other connected items also follow this same operating principle.\n":
        "Contrairement aux autres rituels, la création d'un [](item://minecraft:wild_armor_trim_smithing_template) est un service rendu par les [#](AA00AA)Esprits sauvages[#]() et aucun esprit n'est lié à\n l'objet final. Vous sacrifiez les objets et les Esprits sauvages utilisent leur pouvoir pour forger cet objet pour vous.\n \\\n D'autres objets connexes suivent ce même principe de fonctionnement.\n",
    " The dimensional battlefield will discard any items it cannot store, so it is important\n  to regularly empty the output, either manually, with hoppers or using a transporter spirit.\\\n  Interactions per side:\n  + Top -> input slots (gem, weapon, fuel);\n  + Bottom -> loot slots;\n  + Other -> all slots;\n":
        " Le champ de bataille dimensionnel jettera tout objet qu'il ne peut stocker, il est donc important\n  de vider régulièrement la sortie, manuellement, avec des entonnoirs ou via un esprit transporteur.\\\n  Interactions par face :\n  + Dessus -> emplacements d'entrée (gemme, arme, carburant) ;\n  + Dessous -> emplacements de butin ;\n  + Autres -> tous les emplacements ;\n",
    "  As you know, weapons can be enchanted. Applying looting increases the amount of drops obtained.\n  \\\n  Sharpness speeds up the process, though not as effectively as Smite, Bane of\n  Arthropods, or Impaling when the mob is vulnerable to those enchantments.\n":
        "  Comme vous le savez, les armes peuvent être enchantées. Appliquer Pillage augmente la quantité de butins obtenus.\n  \\\n  Tranchant accélère le processus, mais moins efficacement que Châtiment, Fléau\n  des arthropodes ou Empalement lorsque le mob est vulnérable à ces enchantements.\n",
    "The **Unbreaking** and **Mending** enchantments function as vanilla.\n\\\n With other methods (mods) you can make the weapon unusable (**unusing**)\n when it's close to breaking, or even truly unbreakable (**eternal**).\n":
        "Les enchantements **Solidité** et **Raccommodage** fonctionnent comme en vanilla.\n\\\n Avec d'autres méthodes (mods), vous pouvez rendre l'arme inutilisable (**unusing**)\n quand elle est proche de la casse, ou même véritablement incassable (**eternal**).\n",
    " Spiritual fuel is used to clone the captured mob,\n  allowing it to be defeated in order to obtain its loot.\n  Some resources can be used: [](item://occultism:datura_seeds), [](item://occultism:datura), [](item://occultism:demons_dream_essence), [](item://occultism:otherworld_essence).\n  \\\n  The higher the quality of the resource, the greater its value.\n  A total value equal to the mob’s health is required to initiate the battle.\n":
        " Le carburant spirituel sert à cloner le mob capturé,\n  permettant de le vaincre pour obtenir son butin.\n  Plusieurs ressources peuvent être utilisées : [](item://occultism:datura_seeds), [](item://occultism:datura), [](item://occultism:demons_dream_essence), [](item://occultism:otherworld_essence).\n  \\\n  Plus la qualité de la ressource est élevée, plus sa valeur est grande.\n  Une valeur totale égale aux PV du mob est requise pour déclencher le combat.\n",
    " [](item://occultism:soul_gem) is the default and produces basic drops when simulating possessed mobs.\n  Using a [](item://occultism:fragile_soul_gem) comes with a chance of failure.\n  Finally, use the [](item://occultism:trinity_gem) improves efficiency, allowing the farming of\n  possessed mobs and bosses, and triples the loot from other mobs.\n  The [](item://occultism:soul_shattered) doesn't need spiritual fuel, but can be consumed after the process.\n":
        " La [](item://occultism:soul_gem) est le choix par défaut et produit les butins de base en simulant les mobs possédés.\n  Utiliser une [](item://occultism:fragile_soul_gem) comporte un risque d'échec.\n  Enfin, utiliser la [](item://occultism:trinity_gem) améliore l'efficacité, permettant de farmer\n  les mobs possédés et les boss, et triple le butin des autres mobs.\n  Le [](item://occultism:soul_shattered) n'a pas besoin de carburant spirituel, mais peut être consommé après le processus.\n",
    " The dimensional battlefield has two interactions with redstone:\n  1. The spirit will stop working when receives a redstone signal;\n  2. A comparator can be used to extract a signal based on occupied slots and weapon durability.\n  Tip, if the comparator sends a power of 15, it is better to stop the operations.\n":
        " Le champ de bataille dimensionnel a deux interactions avec la redstone :\n  1. L'esprit cessera de travailler quand il reçoit un signal redstone ;\n  2. Un comparateur peut extraire un signal basé sur les emplacements occupés et la durabilité de l'arme.\n  Astuce : si le comparateur envoie une puissance de 15, mieux vaut arrêter les opérations.\n",
    " The dimensional battlefield houses an [#](AA00AA)Afrit[#]() that opens a stable gateway\n  to a combat arena, perfectly suited for epic battles. Although the\n  portal is too small to transport humans, the afrit is able to pass\n  through it, carrying a few items to farm mob drops within the dimension.\n":
        " Le champ de bataille dimensionnel abrite un [#](AA00AA)Afrit[#]() qui ouvre une passerelle stable\n  vers une arène de combat, parfaitement adaptée aux batailles épiques. Bien que le\n  portail soit trop petit pour transporter des humains, l'afrit peut y passer,\n  emportant quelques objets pour farmer les butins de mobs dans cette dimension.\n",
    " To activate the Dimensional Battlefield, you must supply:\n  + A mob captured with [](item://occultism:soul_gem) (or one of its variants).\n  + A weapon for the afrit to wield in combat.\n  + A source of spiritual fuel, such as [](item://occultism:datura)\n":
        " Pour activer le champ de bataille dimensionnel, vous devez fournir :\n  + Un mob capturé avec une [](item://occultism:soul_gem) (ou l'une de ses variantes).\n  + Une arme que l'afrit maniera au combat.\n  + Une source de carburant spirituel, comme [](item://occultism:datura)\n",
    " The dimensional extractor contains a [#](AA00AA)Djinni[#]() that quickly collects\n  resources generated by dimensional machines or worker spirits\n  and transfers the results to an inventory below.\n":
        " L'extracteur dimensionnel contient un [#](AA00AA)Djinn[#]() qui collecte rapidement\n  les ressources générées par les machines dimensionnelles ou les esprits travailleurs\n  et transfère les résultats vers un inventaire situé en dessous.\n",
    " It's very simple to use: just place your machines/spirits on top of it\n  and connect an inventory directly below that accepts items from the top side.\n  \\\n  NOTE: If the inventory is full, the djinn will simply discard the excess items.\n":
        " Très simple à utiliser : placez vos machines/esprits dessus\n  et connectez un inventaire juste en dessous qui accepte les objets par le haut.\n  \\\n  NOTE : si l'inventaire est plein, le djinn jettera simplement les objets en excès.\n",
    "Additionally, using [#](AA00AA)Shift + Right-Click[#]() will bind the satchel to you,\n allowing to share your ender chest with any other player,\n making this a great way to send items over long distances to friends.\n":
        "De plus, [#](AA00AA)Maj + clic droit[#]() liera la besace à vous,\n permettant de partager votre coffre de l'Ender avec n'importe quel autre joueur,\n une excellente façon d'envoyer des objets à des amis sur de longues distances.\n",
    "A [#](AA00AA)Djinni[#]() is bound to the ender satchel, tasked with **slightly** warping the space.\n This allows open your ender chest from anywhere, making it a practical traveller's companion.\n\n":
        "Un [#](AA00AA)Djinn[#]() est lié à la besace de l'Ender, chargé de **légèrement** déformer l'espace.\n Cela permet d'ouvrir votre coffre de l'Ender de n'importe où, en faisant un compagnon de voyage pratique.\n\n",
    "To set the destination, you''ll need a compass. Right-click to place it and shift+right-click to remove it.\n+ A standard compass takes you to the world spawn;\n+ A compass attached to a lodestone takes you to the top of it. (After placing it in the wormhole, the lodestone can be broken);\n":
        "Pour définir la destination, vous aurez besoin d'une boussole. Clic droit pour la placer et maj + clic droit pour la retirer.\n+ Une boussole standard vous emmène au point d'apparition du monde ;\n+ Une boussole attachée à une magnétite vous emmène à son sommet. (Après l'avoir placée dans le vortex, la magnétite peut être cassée) ;\n",
    "If you hold the gem in your off-hand, it will change the pitch viewing angle.\n A six-pointed star in the center of the portal indicates the current setting:\n+ Emerald -> Forward\n+ Iron -> Tilted Down\n+ Redstone -> Straight Down\n+ Diamond -> Tilted Up\n+ Gold -> Straight Up\n":
        "Si vous tenez la gemme dans votre main secondaire, cela modifiera l'angle d'inclinaison.\n Une étoile à six branches au centre du portail indique le réglage actuel :\n+ Émeraude -> Devant\n+ Fer -> Incliné vers le bas\n+ Redstone -> Droit vers le bas\n+ Diamant -> Incliné vers le haut\n+ Or -> Droit vers le haut\n",
    "Using a [](item://occultism:spirit_attuned_gem) will define the yaw viewing angle after teleportation.\nAn iesnium nugget will point to the set direction like a compass rose.\n":
        "Utiliser une [](item://occultism:spirit_attuned_gem) définira l'angle de lacet après la téléportation.\nUne pépite d'iesnium pointera vers la direction définie comme une rose des vents.\n",
    "+ A compass renamed \"[#](AA00AA)HOME[#]()\" teleport for your personal spawn point;\n+ A compass renamed \"[#](AA00AA)RTP[#]()\" acts as a Random Teleport;\n\\\nAlternatively, you can use special compasses:\n+ [](item://minecraft:recovery_compass) teleports to the location of your last death, works only for players;\n+ [](item://occultism:vitality_compass) teleports to the linked creature, it needs to be in a loaded chunk;\n":
        "+ Une boussole renommée « [#](AA00AA)HOME[#]() » téléporte à votre point d'apparition personnel ;\n+ Une boussole renommée « [#](AA00AA)RTP[#]() » fait office de téléportation aléatoire ;\n\\\nVous pouvez aussi utiliser des boussoles spéciales :\n+ La [](item://minecraft:recovery_compass) téléporte à l'emplacement de votre dernière mort, ne fonctionne que pour les joueurs ;\n+ La [](item://occultism:vitality_compass) téléporte vers la créature liée ; elle doit se trouver dans un chunk chargé ;\n",
    "If the wormhole contains an [Vitality Compass](entry://crafting_rituals/vitality_compass), you can use a fishing rod to pull the linked\n entity into the portal, the hook needs to stop in the portal before you pull.\n":
        "Si le vortex contient une [Boussole de vitalité](entry://crafting_rituals/vitality_compass), vous pouvez utiliser une canne à pêche pour tirer l'entité\n liée dans le portail ; l'hameçon doit s'arrêter dans le portail avant que vous tiriez.\n",
    "The [](item://occultism:entity_wormhole) is a mystical teleportation device maintained by a [#](AA00AA)Djinni[#](),\n capable of instantly transporting living beings across vast distances. Once attuned,\n it creates a stable rift that creatures can step through, linking distant points as if\n they were side by side. The Djinni ensures the wormhole remains open and aligned,\n making it a reliable—though undeniably arcane—means of travel.\n\n":
        "Le [](item://occultism:entity_wormhole) est un dispositif de téléportation mystique entretenu par un [#](AA00AA)Djinn[#](),\n capable de transporter instantanément des êtres vivants sur de vastes distances. Une fois accordé,\n il crée une faille stable que les créatures peuvent traverser, reliant des points distants comme\n s'ils étaient côte à côte. Le Djinn s'assure que le vortex reste ouvert et aligné,\n en faisant un moyen de voyage fiable — bien qu'indéniablement arcane.\n\n",
    "You can also choose the [](item://occultism:otherrock) version if you want.\n":
        "Vous pouvez aussi choisir la version [](item://occultism:otherrock) si vous le souhaitez.\n",
    "Fragile Soul gems are eggs infused by a [#](AA00AA)Foliot[#](). The spirit creates a small dimension\n that allows the temporary entrapment of living beings.\n Beings of great power or size cannot be stored, however. \\\n Be careful, this item will break after transporting a creature.\n":
        "Les gemmes d'âme fragiles sont des œufs imprégnés par un [#](AA00AA)Foliot[#](). L'esprit crée une petite dimension\n qui permet l'emprisonnement temporaire d'êtres vivants.\n Les êtres de grand pouvoir ou de grande taille ne peuvent toutefois pas y être stockés.\\\n Attention, cet objet se brise après avoir transporté une créature.\n",
    "To capture an entity, [#](55FF55)right-click[#]() it with the soul gem. \\\n[#](55FF55)Right-click[#]() again to release the entity.\n\\\n\\\nBosses cannot be captured.\n":
        "Pour capturer une entité, faites [#](55FF55)clic droit[#]() dessus avec la gemme d'âme.\\\n[#](55FF55)Clic droit[#]() à nouveau pour libérer l'entité.\n\\\n\\\nLes boss ne peuvent pas être capturés.\n",
    "Like forging the wild armor trim, upgrading a [](item://minecraft:leather_horse_armor)\n is a service provided by [#](AA00AA)Wild Spirits[#]() and not bound any spirit to the final object.\n You sacrifice the items and the [#](AA00AA)Wild Spirits[#]() uses his power to forge that item for you.\n Use the respective materials to obtain [](item://minecraft:iron_horse_armor),\n [](item://minecraft:golden_horse_armor) or [](item://minecraft:diamond_horse_armor).\n\n":
        "Comme pour forger la garniture d'armure sauvage, améliorer une [](item://minecraft:leather_horse_armor)\n est un service rendu par les [#](AA00AA)Esprits sauvages[#]() et aucun esprit n'est lié à l'objet final.\n Vous sacrifiez les objets et les [#](AA00AA)Esprits sauvages[#]() utilisent leur pouvoir pour forger cet objet pour vous.\n Utilisez les matériaux respectifs pour obtenir une [](item://minecraft:iron_horse_armor),\n [](item://minecraft:golden_horse_armor) ou [](item://minecraft:diamond_horse_armor).\n\n",
    "This knife is an [#](AA00AA)Afrit[#]() infusion that enhances the butcher knife with iesnium,\n increasing its damage while preserving the tallow drop property.\n \\\n Additionally, certain mobs may drop their heads, and attacks against spirits deal triple damage.\n":
        "Ce couteau est une infusion d'[#](AA00AA)Afrit[#]() qui améliore le couteau de boucher avec de l'iesnium,\n augmentant ses dégâts tout en préservant la propriété de drop de suif.\n \\\n De plus, certains mobs peuvent laisser tomber leur tête, et les attaques contre les esprits infligent le triple des dégâts.\n",
    "Knowledge Tablet is an item infused by a [#](AA00AA)Foliot[#](). The spirit can hold a enormous\n quantity of experience points. Keeping safe and allowing giving XP to other players.\n":
        "La tablette de savoir est un objet imprégné par un [#](AA00AA)Foliot[#](). L'esprit peut contenir une énorme\n quantité de points d'expérience. Gardez-la en sécurité et donnez de l'XP à d'autres joueurs.\n",
    "This item use is very simple: \\\n[#](55FF55)Right-Click[#]() will storage all of your experience points. \\\n[#](55FF55)Shift-Right-Click[#]() receive all stored points. \\\n\\\nNOTE: Sometimes, with big values, you can lost a small quantity of point due numerical approximations.\n":
        "Cet objet est très simple à utiliser :\\\n[#](55FF55)Clic droit[#]() stockera tous vos points d'expérience.\\\n[#](55FF55)Maj + clic droit[#]() pour récupérer tous les points stockés.\\\n\\\nNOTE : parfois, avec de grandes valeurs, vous pouvez perdre une petite quantité de points à cause d'approximations numériques.\n",
    "Binding rituals infuse spirits into items, where their powers are used for one specific purpose.\n The created items can act like simple empowering enchantments, or fulfill complex tasks to aid the summoner.\n":
        "Les rituels de liaison imprègnent les objets d'esprits, dont les pouvoirs servent un but précis.\n Les objets créés peuvent agir comme de simples enchantements amplificateurs ou accomplir des tâches complexes pour aider l'invocateur.\n",
    "With simple materials, a [#](AA00AA)Djinni[#]() can repair any chalk for you.\n By evolving in the occult path, an [#](AA00AA)Afrit[#]() can repair miners, tools and armors.\n Any item repaired in this way retains its properties.\n":
        "Avec des matériaux simples, un [#](AA00AA)Djinn[#]() peut réparer n'importe quelle craie pour vous.\n En progressant sur la voie occulte, un [#](AA00AA)Afrit[#]() peut réparer mineurs, outils et armures.\n Tout objet réparé de cette manière conserve ses propriétés.\n",
    "The [](item://occultism:spirit_grindstone) is a [#](AA00AA)Djinni[#]() infusion.\nThis grindstone has some differences:\n1. Remove only curses from enchanted items;\n2. The returned XP is 100%% of removed curses (instead 50%%-100%%);\n3. When combining two items, the enchantments of the top one will be maintained;\n4. The repair rate gets an extra bonus, sum of durability values plus 20%%\n (instead of just 5%% of maximum durability), so repairing at the right time will be rewarding;\n":
        "La [](item://occultism:spirit_grindstone) est une infusion de [#](AA00AA)Djinn[#]().\nCette meule a quelques différences :\n1. Retire uniquement les malédictions des objets enchantés ;\n2. L'XP retournée représente 100%% des malédictions retirées (au lieu de 50%%-100%%) ;\n3. En combinant deux objets, les enchantements de celui du haut sont conservés ;\n4. Le taux de réparation reçoit un bonus supplémentaire, somme des durabilités plus 20%%\n (au lieu de seulement 5%% de la durabilité max), donc réparer au bon moment sera très avantageux ;\n",
    "This extremely advanced stabilizer maybe is inhabited by a [#](AA00AA)Ancient Spirit[#]() that supports\n the dimensional matrix in keeping the storage dimension stable, thus allowing to store even more items.\n\\\n\\\nBy default each Tier 5 Stabilizer adds **1024** item types and 8196000 items storage capacity.\n\n":
        "Ce stabilisateur extrêmement avancé est peut-être habité par un [#](AA00AA)Esprit ancien[#]() qui aide\n la matrice dimensionnelle à maintenir la dimension de stockage stable, permettant ainsi de stocker encore plus d'objets.\n\\\n\\\nPar défaut, chaque stabilisateur de palier 5 ajoute **1024** types d'objets et 8 196 000 emplacements de stockage.\n\n",
    "Forging the [](item://occultism:trinity_gem) is a service provided by an [#](AA00AA)Eldritch Spirit[#]().\nThis gem is upgraded version of [](item://occultism:soul_gem) created with\n3 distinct essences, 3 powerful dusts and 3 iesnium dusts.\nThe trinity gem has an empty entity blacklist (by default).\n":
        "Forger la [](item://occultism:trinity_gem) est un service rendu par un [#](AA00AA)Esprit Eldritch[#]().\nCette gemme est une version améliorée de la [](item://occultism:soul_gem) créée avec\n3 essences distinctes, 3 poussières puissantes et 3 poussières d'iesnium.\nLa gemme de la trinité a une liste noire d'entités vide (par défaut).\n",
    " The [](item://occultism:true_sight_staff) employs an [#](AA00AA)Marid[#]() to assist the summoner in tasks of finding and interacting with the otherworld.\n Unlike [#](AA00AA)Foliot[#]() in the otherworld goggles, which can only provide vision, with this staff in the off-hand or curio slot, the occultist can collect otherworld materials.\n The divining rods search abilities receive an upgrade, now is possible locate any block.\n\n":
        " Le [](item://occultism:true_sight_staff) emploie un [#](AA00AA)Marid[#]() pour assister l'invocateur dans la recherche et l'interaction avec l'outremonde.\n Contrairement au [#](AA00AA)Foliot[#]() des lunettes d'outremonde, qui ne fournit que la vision, avec ce bâton en main secondaire ou en emplacement Curio, l'occultiste peut collecter les matériaux d'outremonde.\n Les capacités de recherche des baguettes de divination sont améliorées : il est maintenant possible de localiser n'importe quel bloc.\n\n",
    "The [](item://occultism:vitality_compass) is a mystical tool infused with a [#](AA00AA)Foliot[#]()\n that allows it to be attuned to the essence of living beings.\n By right-clicking on a creature, you bind its life force to the compass,\n allowing the needle to always point toward its location no matter the distance (while loaded).\n":
        "La [](item://occultism:vitality_compass) est un outil mystique imprégné d'un [#](AA00AA)Foliot[#]()\n qui permet de l'accorder à l'essence des êtres vivants.\n En faisant clic droit sur une créature, vous liez sa force vitale à la boussole,\n permettant à l'aiguille de toujours pointer vers sa position, quelle que soit la distance (tant qu'elle est chargée).\n",
}

DIRECT_BIG = {**ADD, **BOOK}

# Apply
applied = 0
for k, v in src.items():
    if cur.get(k) == v:  # still untranslated
        if v in DIRECT_BIG:
            cur[k] = DIRECT_BIG[v]
            applied += 1

print(f"Pass 2 applied: {applied}")
remaining = [k for k in src if cur.get(k) == src[k]]
print(f"Remaining unhandled: {len(remaining)}")

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(cur, f, ensure_ascii=False, indent="\t")
print("Saved.")
