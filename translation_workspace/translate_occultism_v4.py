#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass 4: Translate the long lore book entries."""
import json

OUTPUT = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2/agent_output/occultism.json"
INPUT = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2/untranslated_per_mod/occultism.json"

with open(OUTPUT, "r", encoding="utf-8") as f:
    cur = json.load(f)
with open(INPUT, "r", encoding="utf-8") as f:
    src = json.load(f)

# All translations - mapping value -> French translation
T = {}

# Stragglers from earlier passes (short)
T.update({
    "Infusion": "Infusion",
    "Possession": "Possession",
    "Redstone": "Redstone",
    "Compact": "Compact",
    "Description": "Description",
    "Pentacles": "Pentacles",
    "Sacrifices": "Sacrifices",
    "Performance": "Performance",
    "Foliot %s": "Foliot %s",
    "Mode": "Mode",
    "Pentacle": "Pentacle",
    "Foliot": "Foliot",
    "Afrit": "Afrit",
    "Marid": "Marid",
    "Drikwing": "Drikwing",
    "Nether": "Nether",
    "Netherrack": "Netherrack",
    "Fruits": "Fruits",
    "Magma": "Magma",
    "Allay": "Allay",
    "Axolotl": "Axolotl",
    "Enderman": "Enderman",
    "Ocelot": "Ocelot",
    "Shulker": "Shulker",
    "Warden": "Warden",
    "Zombie": "Zombie",
    "Contact Eldritch": "Contact Eldritch",
    "Inserting and extracting items from the Storage Actuator using Theurgy Logistics":
        "Insertion et extraction d'objets depuis l'actionneur de stockage avec la logistique Theurgy",
})

# Familiar texts
T.update({
    "The Demonic Partner - a Husband or Wife - can fight for you and split your household chores.\n\\\n\\\nRight-Click with any cookable food and they will use their magic to cook it.\n\\\n\\\nRight-Click with a potion to get the effect for a significantly longer time,\n instant potions will be two levels stronger.\n":
        "Le partenaire démoniaque — époux ou épouse — peut combattre pour vous et partager les tâches ménagères.\n\\\n\\\nClic droit avec n'importe quel aliment cuisinable et il utilisera sa magie pour le cuire.\n\\\n\\\nClic droit avec une potion pour bénéficier de l'effet pendant bien plus longtemps ;\n les potions instantanées seront deux niveaux plus fortes.\n",
    "Magicians practicing the occult are a diverse crowd, coming from all creeds and all corners of the world. However one thing unites them all - they are as lonely as any human without a partner.\n\\\n\\\nOf course being a magician, the dating pool is larger than for most people, meeting all kinds of otherworldly beings, besides humans.\n":
        "Les magiciens qui pratiquent l'occultisme forment une foule variée, issue de toutes croyances et des quatre coins du monde. Cependant, une chose les unit tous : ils sont aussi seuls que n'importe quel humain sans partenaire.\n\\\n\\\nBien sûr, étant magicien, le bassin de prétendants est plus large que pour la plupart : ils côtoient toutes sortes d'êtres venus d'ailleurs, en plus des humains.\n",
    "As beings of immense powers Demons can have it all ... even love.\\\nIn rare cases a Demon is so impressed by a mortal that they stay in touch. And in even rarer cases, take them on a date. And in such cases, the most unlikely thing can happen - love between a Spirit and a mortal.\n":
        "Êtres aux pouvoirs immenses, les démons peuvent tout avoir... même l'amour.\\\nDans de rares cas, un démon est si impressionné par un mortel qu'il garde le contact. Et plus rarement encore, l'invite à un rendez-vous. Et alors, l'improbable peut survenir : l'amour entre un esprit et un mortel.\n",
    "Demons, of course, like to deal in contracts, and what better contract than a marriage contract?\\\nBeware however, Spirits are all about commitment, so this is a permanent bond.\n":
        "Les démons, bien sûr, aiment les contrats — et quel meilleur contrat qu'un contrat de mariage ?\\\nAttention toutefois, les esprits ne plaisantent pas avec l'engagement : c'est un lien permanent.\n",
    "The Demonic Partner Chapter is part of the Familiar Category of this book because of the similarities, however a Partner is obviously not a familiar.\n\\\n\\\nAs such, they also cannot be stored in a [](item://occultism:familiar_ring). You can, however, use a [](item://occultism:soul_gem) as for any other being.\n":
        "Le chapitre du partenaire démoniaque fait partie de la catégorie des familiers en raison des similitudes, mais un partenaire n'est évidemment pas un familier.\n\\\n\\\nIl ne peut donc pas être rangé dans un [](item://occultism:familiar_ring). Vous pouvez cependant utiliser une [](item://occultism:soul_gem) comme pour n'importe quel autre être.\n",
    "A great partner gift is the [](item://occultism:sweet_honey_heart). To get this item, simply give a [](item://occultism:cursed_honey) to your husband or wife.\n\\\n\\\nNote: This action has a cooldown of 10 minutes.\n":
        "Un excellent cadeau de partenaire est le [](item://occultism:sweet_honey_heart). Pour l'obtenir, donnez simplement une [](item://occultism:cursed_honey) à votre époux ou épouse.\n\\\n\\\nNote : cette action a un temps de recharge de 10 minutes.\n",
    "**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, the bat familiar will give a life steal effect to it's master.\n":
        "**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, le familier Chauve-souris confère un effet de vol de vie à son maître.\n",
    "**Provides**: [#](ad03fc)Night Vision[#]()\n":
        "**Confère** : [#](ad03fc)Vision nocturne[#]()\n",
    "**Provides**: [#](ad03fc)Increased wood break speed[#]()\n":
        "**Confère** : [#](ad03fc)Vitesse accrue de cassage du bois[#]()\n",
    "The Beholder familiar highlights nearby entities with a glow effect, and shoots laser rays at enemies. It **eats** (poor) **Shub Niggurath babies** to gain temporary damage and speed.\n\\\n\\\n**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, it give it's master immunity to blindness, and after highlighting a Warden, the immunity extends to darkness.\n":
        "Le familier Beholder met en surbrillance les entités proches avec un effet lumineux et tire des rayons laser sur les ennemis. Il **mange** (les pauvres) **bébés Shub-Niggurath** pour gagner temporairement en dégâts et en vitesse.\n\\\n\\\n**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, il confère à son maître l'immunité à la cécité, et après avoir mis un Warden en surbrillance, l'immunité s'étend aux ténèbres.\n",
    "**Provides**: [#](ad03fc)Highlights enemies[#](), [#](ad03fc)Shoots **FREAKING LAZORS**[#]()\n":
        "**Confère** : [#](ad03fc)Met les ennemis en surbrillance[#](), [#](ad03fc)Tire des **PUTAINS DE LASERS**[#]()\n",
    "Whenever the player picks up stone, there is a chance for the blacksmith familiar to repair their equipment a little bit.\n\\\n\\\n**Upgrade Behaviour**: \\\nCannot be upgraded, but upgrades other Familiars.\n":
        "Chaque fois que le joueur ramasse de la pierre, le familier Forgeron a une chance de réparer un peu son équipement.\n\\\n\\\n**Comportement amélioré** : \\\nNe peut être amélioré, mais améliore les autres familiers.\n",
    "To upgrade other familiars the blacksmith needs to be given iron ingots or blocks by [#](ad03fc)right-clicking[#]() it.\n\\\nWhen the blacksmith upgrades a familiar, a message appears in the action bar, an anvil sound is emitted, and a star appears at the end of the familiar's name.\n\\\nUpgraded familiars provide additional effects.\n":
        "Pour améliorer d'autres familiers, donnez au forgeron des lingots ou blocs de fer par [#](ad03fc)clic droit[#]().\n\\\nQuand le forgeron améliore un familier, un message apparaît dans la barre d'action, un son d'enclume retentit, et une étoile apparaît à la fin du nom du familier.\n\\\nLes familiers améliorés fournissent des effets supplémentaires.\n",
    "**Provides**: [#](ad03fc)Repairs Equipment while Mining[#](), [#](ad03fc)Upgrades other familiars[#]()\n":
        "**Confère** : [#](ad03fc)Répare l'équipement pendant le minage[#](), [#](ad03fc)Améliore les autres familiers[#]()\n",
    "The chimera familiar can be fed (any) meat to grow, when growing it will gain damage and speed. Once it has grown big enough, players can ride it. When feeding it a [](item://minecraft:golden_apple) the [#](ad03fc)Goat[#]() will detach and become a separate familiar.\n\\\n\\\nThe detached goat familiar can be used to obtain the [Shub Niggurath](entry://familiar_rituals/familiar_shub_niggurath) familiar.\n":
        "Le familier Chimère peut être nourri (de n'importe quelle) viande pour grandir ; en grandissant, il gagne en dégâts et en vitesse. Une fois assez grand, les joueurs peuvent le chevaucher. En lui donnant une [](item://minecraft:golden_apple), la [#](ad03fc)Chèvre[#]() se détachera et deviendra un familier à part.\n\\\n\\\nLa chèvre détachée permet d'obtenir le familier [Shub-Niggurath](entry://familiar_rituals/familiar_shub_niggurath).\n",
    "**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, the goat familiar will get a warning bell. When you hit the familiar it will ring the bell and attract enemies in a large radius.\n":
        "**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, le familier Chèvre reçoit une cloche d'alarme. Frapper le familier la fait sonner et attire les ennemis dans un large rayon.\n",
    "**Provides**: [#](ad03fc)Rideable Mount[#]()\n":
        "**Confère** : [#](ad03fc)Monture chevauchable[#]()\n",
    "Give a [](item://minecraft:lapis_lazuli) to transform in a [](item://minecraft:prismarine_shard).\\\n\\\n**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, it will act as a mobile light source.\\\nYou receive more prismarine per lapis.\n":
        "Donnez du [](item://minecraft:lapis_lazuli) pour le transformer en [](item://minecraft:prismarine_shard).\\\n\\\n**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, il agira comme une source de lumière mobile.\\\nVous recevez plus de prismarine par lapis.\n",
    "**Provides**: [#](ad03fc)Water Breathing[#](), [#](ad03fc)General Coolness[#]() and [#](ad03fc)Prismarine conversion[#]()\n":
        "**Confère** : [#](ad03fc)Respiration sous l'eau[#](), [#](ad03fc)Coolitude générale[#]() et [#](ad03fc)Conversion de prismarine[#]()\n",
    "**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, will increase the step assist and it will attack nearby enemies with a hammer. Yep, a **hammer**.\n":
        "**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, l'aide au pas augmente et il attaque les ennemis proches avec un marteau. Oui, un **marteau**.\n",
    "**Provides**: [#](ad03fc)Speed and Jump Boost, Step assist[#]()\n":
        "**Confère** : [#](ad03fc)Bonus de vitesse et de saut, aide au pas[#]()\n",
    "**Upgrade Behaviour**\\\nEnchants a Golden Apple when right-click, but has large time interval.\n":
        "**Comportement amélioré**\\\nEnchante une pomme d'or au clic droit, mais avec un long intervalle.\n",
    "**Provides**: [#](ad03fc)Fire Resistance[#](), [#](ad03fc)Attacks Enemies[#]()\n":
        "**Confère** : [#](ad03fc)Résistance au feu[#](), [#](ad03fc)Attaque les ennemis[#]()\n",
    "Greedy familiars can ride on dragon familiars, giving the dragon the greedy effects additionally.\n\\\n\\\n**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, it will throw swords at nearby enemies.\n":
        "Les familiers Avide peuvent monter sur les familiers Dragon, donnant au dragon les effets de l'Avide en supplément.\n\\\n\\\n**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, il lance des épées sur les ennemis proches.\n",
    "**Provides**: [#](ad03fc)Increased XP[#](), Loves Sticks\n":
        "**Confère** : [#](ad03fc)XP augmentée[#](), adore les bâtons\n",
    "The Fairy familiar **keeps other familiars from dying** (with cooldown), helps out other familiars with **beneficial effects** and **drains the life force of enemies** to assist their master.\n\\\n\\\n**Upgrade Behaviour**\\\nAllow getting Dragon's Breath when right-clicked with a glass bottle.\n":
        "Le familier Fée **empêche les autres familiers de mourir** (avec recharge), aide les autres familiers avec des **effets bénéfiques** et **draine la force vitale des ennemis** pour assister son maître.\n\\\n\\\n**Comportement amélioré**\\\nPermet d'obtenir le Souffle du dragon par clic droit avec une fiole.\n",
    "**Provides**: [#](ad03fc)Assists Familiars[#](), [#](ad03fc)Prevents Familiar Deaths[#](), [#](ad03fc)Drains Enemy Life Force[#]()\n":
        "**Confère** : [#](ad03fc)Assiste les familiers[#](), [#](ad03fc)Empêche la mort des familiers[#](), [#](ad03fc)Draine la force vitale des ennemis[#]()\n",
    "The greedy familiar is a Foliot that will pick up nearby items for it's master. When captured in a familiar ring it increased the pick-up range of the wearer.\n\\\n\\\n**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, it can find blocks for its master. [#](ad03fc)Right-click[#]() it with a block to tell it what to look for.\n":
        "Le familier Avide est un Foliot qui ramasse les objets proches pour son maître. Capturé dans un anneau de familier, il augmente la portée de ramassage du porteur.\n\\\n\\\n**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, il peut trouver des blocs pour son maître. [#](ad03fc)Clic droit[#]() avec un bloc pour lui indiquer quoi chercher.\n",
    "**Provides**: [#](ad03fc)Picks up Items[#](), [#](ad03fc)Increased Pick-up Range[#]()\n":
        "**Confère** : [#](ad03fc)Ramasse les objets[#](), [#](ad03fc)Portée de ramassage augmentée[#]()\n",
    "The guardian familiar sacrifices a limb everytime it's master is about to die and thus **prevents the death**. Once the guardian dies, the player is no longer protected. When summoned, the guardian spawns with a **random amount of limbs**, there is no guarantee that a complete guardian is summoned.\n":
        "Le familier Gardien sacrifie un membre à chaque fois que son maître est sur le point de mourir, **empêchant ainsi la mort**. Une fois le gardien mort, le joueur n'est plus protégé. À l'invocation, le gardien apparaît avec un **nombre aléatoire de membres** ; rien ne garantit qu'un gardien complet soit invoqué.\n",
    "**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, it regains a limb.\n":
        "**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, il regagne un membre.\n",
    "**Provides**: [#](ad03fc)Prevents player death while alive[#]()\n":
        "**Confère** : [#](ad03fc)Empêche la mort du joueur tant qu'il est vivant[#]()\n",
    "The headless ratman familiar steals heads of mobs near the ratman when they are killed. It then provides a damage buff against that type of mob to their master. If the ratman drops **below 50%% health** it dies, but can then be rebuilt by their master by giving them [](item://minecraft:wheat), [](item://minecraft:stick), [](item://minecraft:hay_block) and a [](item://minecraft:carved_pumpkin).\n":
        "Le familier Homme-rat sans tête vole les têtes des mobs proches lorsqu'ils sont tués. Il confère ensuite à son maître un bonus de dégâts contre ce type de mob. Si l'homme-rat tombe **sous 50%% de PV**, il meurt, mais peut être reconstruit par son maître en lui donnant [](item://minecraft:wheat), [](item://minecraft:stick), [](item://minecraft:hay_block) et une [](item://minecraft:carved_pumpkin).\n",
    "**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, it will give weakness to nearby mobs of the type it stole the head from. And the owner will not make the Enderman angry by looking into his eyes.\n":
        "**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, il inflige la Faiblesse aux mobs proches du type dont il a volé la tête. Et le propriétaire n'énervera plus l'Enderman en le regardant dans les yeux.\n",
    "**Provides**: [#](ad03fc)Conditional Damage Buff[#]()\n":
        "**Confère** : [#](ad03fc)Bonus de dégâts conditionnel[#]()\n",
    "The Mummy familiar is a martial arts expert and fights to protect their master.\n\\\n\\\n**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, it the familiar will deal even more damage and double the dodge chance.\n":
        "Le familier Momie est un expert en arts martiaux qui combat pour protéger son maître.\n\\\n\\\n**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, le familier inflige encore plus de dégâts et double la chance d'esquive.\n",
    "**Provides**: [#](ad03fc)Fights your enemies[#](), [#](ad03fc)Dodge Effect[#]()\n":
        "**Confère** : [#](ad03fc)Combat vos ennemis[#](), [#](ad03fc)Effet d'esquive[#]()\n",
    "[#](ad03fc)Drikwings[#]() are a subclass of [#](ad03fc)Djinni[#]() that are known to be amicable towards humans. They usually take the shape of a dark blue and purple parrot. Drikwings will provide their owner with limited flight abilities when nearby.\n\\\n\\\n**Upgrade Behaviour**\\\nIncrease number of jumps and change the slow fall to immunity to fall damage.\n":
        "Les [#](ad03fc)Drikwings[#]() sont une sous-classe de [#](ad03fc)Djinns[#]() réputés amicaux envers les humains. Ils prennent généralement la forme d'un perroquet bleu foncé et violet. Les Drikwings offrent à leur propriétaire des capacités de vol limitées à proximité.\n\\\n\\\n**Comportement amélioré**\\\nAugmente le nombre de sauts et change la chute lente en immunité aux dégâts de chute.\n",
    "To obtain the parrot or parrot familiar for the sacrifice, consider summoning them using either the [Wild Parrot Ritual](entry://possession_rituals/possess_unbound_parrot) or [Parrot Familiar Ritual](entry://familiar_rituals/familiar_parrot)\n\\\n\\\n**Hint:** If you use mods that protect pets from death, use the wild parrot ritual!\n":
        "Pour obtenir le perroquet ou le familier Perroquet pour le sacrifice, envisagez de les invoquer via le [Rituel du Perroquet sauvage](entry://possession_rituals/possess_unbound_parrot) ou le [Rituel du familier Perroquet](entry://familiar_rituals/familiar_parrot).\n\\\n\\\n**Astuce :** si vous utilisez des mods qui protègent les animaux de la mort, utilisez le rituel du perroquet sauvage !\n",
    "**Provides**: [#](ad03fc)Multi-Jump[#](), [#](ad03fc)Jump Boost[#](), [#](ad03fc)Slow Falling[#]()\n":
        "**Confère** : [#](ad03fc)Saut multiple[#](), [#](ad03fc)Bonus de saut[#](), [#](ad03fc)Chute lente[#]()\n",
    "In this ritual a [#](ad03fc)Foliot[#]() is summoned **as a familiar**, the slaughter of a [#](ad03fc)Chicken[#]() and the offering of dyes are intended to entice the [#](ad03fc)Foliot[#]() to take the shape of a parrot.\\\nAs [#](ad03fc)Foliot[#]() are not among the smartest spirits, they sometimes misunderstand the instructions ...\n":
        "Dans ce rituel, un [#](ad03fc)Foliot[#]() est invoqué **en tant que familier** ; le sacrifice d'une [#](ad03fc)Poule[#]() et l'offrande de colorants visent à inciter le [#](ad03fc)Foliot[#]() à prendre la forme d'un perroquet.\\\nLes [#](ad03fc)Foliots[#]() n'étant pas les esprits les plus brillants, ils interprètent parfois mal les instructions...\n",
    "*This means, if a [#](ad03fc)Chicken[#]() is spawned, that's not a bug, just bad luck!*\n\\\n\\\n**Upgrade Behaviour**\\\nCannot be upgraded by the blacksmith familiar.\n":
        "*Autrement dit, si une [#](ad03fc)Poule[#]() apparaît, ce n'est pas un bug, juste de la malchance !*\n\\\n\\\n**Comportement amélioré**\\\nNe peut être amélioré par le familier Forgeron.\n",
    "**Provides**: [#](ad03fc)Company[#]()\n":
        "**Confère** : [#](ad03fc)Compagnie[#]()\n",
    "**Upgrade Behaviour**\\\nWhen upgraded by a blacksmith familiar, it will get a warning bell. When you hit the familiar it will ring the bell and **attract enemies** in a large radius.\n":
        "**Comportement amélioré**\\\nUne fois amélioré par un familier Forgeron, il reçoit une cloche d'alarme. Frapper le familier la fait sonner et **attire les ennemis** dans un large rayon.\n",
    "**Provides**: [#](ad03fc)Spawns small versions of itself to fight for you.[#]()\n":
        "**Confère** : [#](ad03fc)Fait apparaître de petites versions de lui-même pour combattre à vos côtés.[#]()\n",
    "The [#](ad03fc)Shub Niggurath[#]() is not summoned directly. First, summon a [Chimera Familiar](entry://familiar_rituals/familiar_chimera) and feed it a [](item://minecraft:golden_apple) to detach the [#](ad03fc)Goat[#](). Bring the goat to a [#](ad03fc)Forest Biome[#](). Then click the goat with [any Black Dye](item://minecraft:black_dye), [](item://minecraft:flint) and [](item://minecraft:ender_eye) to summon the [#](ad03fc)Shub Niggurath[#]().\n":
        "[#](ad03fc)Shub-Niggurath[#]() n'est pas invoqué directement. Invoquez d'abord un [Familier Chimère](entry://familiar_rituals/familiar_chimera) et donnez-lui une [](item://minecraft:golden_apple) pour détacher la [#](ad03fc)Chèvre[#](). Amenez la chèvre dans un [#](ad03fc)biome de forêt[#](). Cliquez ensuite sur la chèvre avec [un colorant noir](item://minecraft:black_dye), [](item://minecraft:flint) et [](item://minecraft:ender_eye) pour invoquer [#](ad03fc)Shub-Niggurath[#]().\n",
    "Occultists have discovered a way to capture part of the essence\n of any fallen enemy through an enchantment known as [#](55FF55)Fracture Soul[#]().\n\\\n\\\nWith a variation of the ritual to resurrect familiars,\n it is possible for a [](item://occultism:soul_shattered) to create a completely revived mob,\n forming its new body and trapping within it the shard's remaining soul.\n":
        "Les occultistes ont découvert un moyen de capturer une partie de l'essence\n de tout ennemi tombé via un enchantement nommé [#](55FF55)Fracture d'âme[#]().\n\\\n\\\nAvec une variation du rituel de résurrection des familiers,\n un [](item://occultism:soul_shattered) peut créer un mob entièrement ravivé,\n formant son nouveau corps et y emprisonnant l'âme restante du fragment.\n",
    "An Iesnium Golem is a direct upgrade from a regular Iron Golem, this new version is much stronger and invulnerable. \\\nOnly a player can dismiss them, by hitting while crouched, returning as a [](item://occultism:fragile_soul_gem).\n":
        "Un golem d'iesnium est une amélioration directe du golem de fer classique ; cette nouvelle version est bien plus forte et invulnérable.\\\nSeul un joueur peut le congédier, en le frappant accroupi, le faisant revenir sous forme de [](item://occultism:fragile_soul_gem).\n",
    "The Iesnium Golem Chapter is part of the Familiar Category of this book because of the similarities, however a golem is not exactly a familiar since it does not have an owner.\n\\\n\\\nAs such, they also cannot be stored in a [](item://occultism:familiar_ring) or in a [](item://occultism:soul_gem). You can, however, dispense with them as stated on the previous page.\n":
        "Le chapitre du golem d'iesnium fait partie de la catégorie des familiers en raison des similitudes ; cependant, un golem n'est pas vraiment un familier puisqu'il n'a pas de maître.\n\\\n\\\nIl ne peut donc pas être stocké dans un [](item://occultism:familiar_ring) ni dans une [](item://occultism:soul_gem). Vous pouvez toutefois vous en débarrasser comme indiqué à la page précédente.\n",
    "**Provides:** [#](AA00AA)Immortal area protector[#]()\n":
        "**Confère :** [#](AA00AA)Protecteur de zone immortel[#]()\n",
    "Familiar rituals summon spirits to aid the summoner directly. The spirits usually inhabit an animal's body, allowing them to resist essence decay. Familiars provide buffs, but may also actively protect the summoner.\n":
        "Les rituels de familiers invoquent des esprits pour aider directement l'invocateur. Les esprits habitent généralement le corps d'un animal, ce qui leur permet de résister à la décrépitude de l'essence. Les familiers procurent des bonus, mais peuvent aussi protéger activement l'invocateur.\n",
    "Enterprising summoners have found a way to bind familiars into jewelry that passively applies their buff, the [Familiar Ring](entry://crafting_rituals/craft_familiar_ring).\n":
        "Des invocateurs entreprenants ont trouvé un moyen de lier les familiers à des bijoux qui appliquent passivement leur bonus : l'[Anneau de familier](entry://crafting_rituals/craft_familiar_ring).\n",
    "\"Familiars can be easily traded when in a [Familiar Ring](entry://crafting_rituals/craft_familiar_ring).\n\\\n\\\nWhen released, the spirit will recognize the person releasing them as their new master.\n":
        "« Les familiers peuvent être facilement échangés lorsqu'ils sont dans un [Anneau de familier](entry://crafting_rituals/craft_familiar_ring).\n\\\n\\\nLorsqu'il est libéré, l'esprit reconnaît la personne qui le libère comme son nouveau maître.\n",
    "Purify a Vex to an Allay on a resurrection process that reveals its true name.\n":
        "Purifie un Vex en Allay lors d'un processus de résurrection qui révèle son vrai nom.\n",
    "**Provides**: Allay\n":
        "**Confère** : Allay\n",
    "The resurrection is a relatively simple process. The soul shard is strengthened with [](item://occultism:otherworld_essence) until it is strong enough to allow the familiar to return to the mortal realm and create a new body for itself.\n\\\n\\\nThe essence is obtained by growing (lots of) Demons Dream plants.\n":
        "La résurrection est un processus relativement simple. Le fragment d'âme est renforcé avec de l'[](item://occultism:otherworld_essence) jusqu'à devenir assez puissant pour permettre au familier de revenir au royaume des mortels et de se créer un nouveau corps.\n\\\n\\\nL'essence s'obtient en faisant pousser (beaucoup de) plantes de Rêve du Démon.\n",
    "Fruit and seeds can be mixed freely to create the essence.\n":
        "Fruits et graines peuvent être mélangés librement pour créer l'essence.\n",
    "If a familiar dies it does not merely return to the Otherworld. Due to the close connection to the summoner a splinter of the familiar's soul remains in the mortal realm.\n\\\n\\\nThis splinter - shard - can be used to re-summon the familiar more easily.\n":
        "Quand un familier meurt, il ne retourne pas simplement à l'Outremonde. En raison du lien étroit avec l'invocateur, un éclat de l'âme du familier subsiste dans le royaume des mortels.\n\\\n\\\nCet éclat — fragment — peut être utilisé pour ré-invoquer le familier plus facilement.\n",
})

# Books of binding
T.update({
    "In order to craft [#](ad03fc)Books of Binding[#]() to summon spirits, you also need awakened feather. Simply drop any feather into [](item://occultism:spirit_fire) to awakened it.\n":
        "Pour fabriquer des [#](ad03fc)Livres de liaison[#]() afin d'invoquer des esprits, il vous faut aussi une plume éveillée. Laissez tomber n'importe quelle plume dans le [](item://occultism:spirit_fire) pour l'éveiller.\n",
    "Add the name of the spirit to summon to your book of binding by crafting it with the Dictionary of Spirits. The Dictionary will not be used up.\n":
        "Ajoutez le nom de l'esprit à invoquer dans votre livre de liaison en le combinant avec le Dictionnaire des esprits. Le Dictionnaire n'est pas consommé.\n",
    " Alternatively, you can directly use the Binding Book: Empty instead of the previous three items. There are two ways to obtain this book. Place this book in the center of dyes to get specific book of binding.\n":
        " Vous pouvez aussi utiliser directement le Livre de liaison vide à la place des trois objets précédents. Il existe deux façons d'obtenir ce livre. Placez-le au centre de colorants pour obtenir un livre de liaison spécifique.\n",
    "Craft a book of binding that will be used to call forth a [#](ad03fc)Foliot[#]() spirit.\n":
        "Fabriquez un livre de liaison qui sera utilisé pour invoquer un esprit [#](ad03fc)Foliot[#]().\n",
    "To call forth a spirit, a [#](ad03fc)Book of Binding[#]() must be used in the ritual.\nThere is a type of book corresponding to each type (or tier) of spirit.\nTo identify a spirit to summon, it's name must be written in the [#](ad03fc)Book of Binding[#](), resulting in a [#](ad03fc)Bound Book of Binding[#]() that can be used in the ritual.\n":
        "Pour invoquer un esprit, un [#](ad03fc)Livre de liaison[#]() doit être utilisé dans le rituel.\nIl existe un type de livre pour chaque type (ou palier) d'esprit.\nPour identifier l'esprit à invoquer, son nom doit être inscrit dans le [#](ad03fc)Livre de liaison[#](), donnant un [#](ad03fc)Livre de liaison lié[#]() utilisable dans le rituel.\n",
    "**Note:** *The spirit names are eye candy only*, that means they are not relevant for the recipe. As long as you have the right spirit type in your book of binding it can be used.\n":
        "**Note :** *les noms d'esprits sont purement esthétiques* — ils ne sont pas pertinents pour la recette. Tant que vous avez le bon type d'esprit dans votre livre de liaison, il peut être utilisé.\n",
    "In order to craft [#](ad03fc)Books of Binding[#]() to summon spirits, you need purified ink. Simply drop any black dye into [](item://occultism:spirit_fire) to purify it.\n":
        "Pour fabriquer des [#](ad03fc)Livres de liaison[#]() afin d'invoquer des esprits, il faut de l'encre purifiée. Laissez tomber n'importe quel colorant noir dans le [](item://occultism:spirit_fire) pour le purifier.\n",
    "Lastly you need taboo book to craft [#](ad03fc)Books of Binding[#]() to summon spirits. Simply drop a book into [](item://occultism:spirit_fire) to get it.\n":
        "Enfin, il vous faut un livre tabou pour fabriquer des [#](ad03fc)Livres de liaison[#](). Laissez tomber un livre dans le [](item://occultism:spirit_fire) pour l'obtenir.\n",
    "Bound Books of Binding are generated with a random spirit name. This tricks many automated crafting processes into no longer recognizing the item as the requested crafting result, because it does not expect NBT/Data Components on the item.\n\\\n\\\nThis leads to stuck crafting processes.\n":
        "Les livres de liaison liés sont générés avec un nom d'esprit aléatoire. Cela trompe de nombreux processus d'artisanat automatisés qui ne reconnaissent plus l'objet comme le résultat de l'artisanat demandé, car ils n'attendent pas de NBT/composants de données sur l'objet.\n\\\n\\\nCela conduit à des processus d'artisanat bloqués.\n",
    "1. Put a dictionary of spirits into an anvil and give it a name. This will be the name of all spirits summoned in the future.\n2. Use this dictionary to configure crafting patterns (if your automation mod requires it).\n3. Use this dictionary to craft the Bound Books of Binding in the automation system. As usual, the dictionary will not be used up.\n4. All crafted books will now have the same name and will be recognized by your automation system.\n":
        "1. Placez un Dictionnaire des esprits dans une enclume et donnez-lui un nom. Ce sera le nom de tous les esprits invoqués à l'avenir.\n2. Utilisez ce dictionnaire pour configurer les patrons d'artisanat (si votre mod d'automatisation l'exige).\n3. Utilisez ce dictionnaire pour fabriquer les Livres de liaison liés dans le système d'automatisation. Comme d'habitude, le dictionnaire n'est pas consommé.\n4. Tous les livres fabriqués auront désormais le même nom et seront reconnus par votre système d'automatisation.\n",
})

# Books of calling
T.update({
    "Books of Calling allow to control a summoned spirit, and to store it to prevent essence decay or move it more easily.\n\\\n\\\nOnly spirits that require precise instructions - such as a work area or drop-off storage - come with a book of calling.\n":
        "Les livres d'appel permettent de contrôler un esprit invoqué et de le stocker pour empêcher la décrépitude de l'essence ou pour le déplacer plus facilement.\n\\\n\\\nSeuls les esprits qui requièrent des instructions précises — comme une zone de travail ou un stockage de dépôt — sont fournis avec un livre d'appel.\n",
    "If a summoned spirit supports the use of a Book of Calling, the summoning ritual will automatically spawn a book in the world alongside the spirit.\n\\\n\\\nIf you **lose the book**, there are also crafting recipes that just provide the book (without summoning a spirit).\n":
        "Si un esprit invoqué supporte l'usage d'un Livre d'appel, le rituel d'invocation fera apparaître automatiquement un livre dans le monde aux côtés de l'esprit.\n\\\n\\\nSi vous **perdez le livre**, il existe aussi des recettes qui fournissent simplement le livre (sans invoquer d'esprit).\n",
    "The recipes can be found in this book or via JEI.\n\\\n\\\n[#](ad03fc)Shift-right-click[#]() the spirit with the crafted book to assign it.\n":
        "Les recettes se trouvent dans ce livre ou via JEI.\n\\\n\\\n[#](ad03fc)Maj + clic droit[#]() sur l'esprit avec le livre fabriqué pour le lui assigner.\n",
    "To store spirits that do not have a fitting book of calling, you can use a [Soul Gem](entry://crafting_rituals/craft_soul_gem).\nSoul gems are much more versatile and allow to store almost all types of entities even animals and monsters, but not players or bosses.\n":
        "Pour stocker des esprits qui ne disposent pas d'un livre d'appel approprié, vous pouvez utiliser une [Gemme d'âme](entry://crafting_rituals/craft_soul_gem).\nLes gemmes d'âme sont bien plus polyvalentes et permettent de stocker presque tous les types d'entités, même les animaux et les monstres, mais pas les joueurs ni les boss.\n",
    "- [#](ad03fc)Right-click[#]() air to open the configuration screen\n- [#](ad03fc)Shift-right-click[#]() a block to apply the action selected in the configuration screen\n- [#](ad03fc)Shift-right-click[#]() a spirit to capture it (must be of the same type)\n- [#](ad03fc)Right-click[#]() with a book with a captured spirit to release it\n":
        "- [#](ad03fc)Clic droit[#]() dans le vide pour ouvrir l'écran de configuration\n- [#](ad03fc)Maj + clic droit[#]() sur un bloc pour appliquer l'action sélectionnée dans l'écran de configuration\n- [#](ad03fc)Maj + clic droit[#]() sur un esprit pour le capturer (doit être du même type)\n- [#](ad03fc)Clic droit[#]() avec un livre contenant un esprit capturé pour le libérer\n",
    "You can automate this process placing a sacrificial bowl with [#](00AA00)Dictionary of Spirits[#]() above the [](item://minecraft:chiseled_bookshelf).\nWhen the bowl receive a redstone signal, the books inside will be bounded.\\\n\\\nNote: Also work with copper and silver versions of the sacrificial bowl.\n":
        "Vous pouvez automatiser ce processus en plaçant un bol sacrificiel avec un [#](00AA00)Dictionnaire des esprits[#]() au-dessus de la [](item://minecraft:chiseled_bookshelf).\nLorsque le bol reçoit un signal redstone, les livres à l'intérieur seront liés.\\\n\\\nNote : fonctionne aussi avec les versions cuivre et argent du bol sacrificiel.\n",
    "Crafting the bound books of binding is so boring? \\\nUse the Bookshelf Binding!\nMake up to **SIX** bindings at the same time, with in-world interaction, no more the common shapeless recipe. \\\n\\\nPut the books in a [](item://minecraft:chiseled_bookshelf) and [#](AA00AA)Shift + Right Click[#]() with your [#](00AA00)Dictionary of Spirits[#]().\n":
        "Fabriquer les livres de liaison liés est ennuyeux ? \\\nUtilisez la liaison via bibliothèque !\nFaites jusqu'à **SIX** liaisons en même temps, par interaction en monde, finie la recette informe classique. \\\n\\\nPlacez les livres dans une [](item://minecraft:chiseled_bookshelf) et faites [#](AA00AA)Maj + clic droit[#]() avec votre [#](00AA00)Dictionnaire des esprits[#]().\n",
    "You can also bind [](item://occultism:book_of_binding_empty) directly, just hold 4 dyes for each in your off-hand. \\\n\\\nThe spirit to be bound depends on the dye held:\\\nBlue    ->  Foliot\\\nPurple  ->  Djinni\\\nYellow  ->  Afrit\\\nGreen   ->  Marid\n":
        "Vous pouvez aussi lier directement les [](item://occultism:book_of_binding_empty), il suffit de tenir 4 colorants pour chaque dans votre main secondaire. \\\n\\\nL'esprit à lier dépend du colorant tenu :\\\nBleu    ->  Foliot\\\nViolet  ->  Djinn\\\nJaune   ->  Afrit\\\nVert    ->  Marid\n",
})

# Brush, candle, chalks
T.update({
    "Chalk is a pain to clean up, by [#](ad03fc)right-clicking[#]() with a brush you can remove it from the world much more easily.\n":
        "La craie est pénible à nettoyer ; en faisant [#](ad03fc)clic droit[#]() avec une brosse, vous pouvez la retirer du monde bien plus facilement.\n",
    "You can use a dye and the [](item://occultism:large_candle) to mix then in shapeless craft process to get a colored large candle.\n\\\nAvailable in all the 16 minecraft dyes.\n":
        "Vous pouvez utiliser un colorant et la [](item://occultism:large_candle) en artisanat informe pour obtenir une grande bougie colorée.\n\\\nDisponible dans les 16 colorants de Minecraft.\n",
    "Candles provide stability to rituals and are an important part of almost all pentacles.\n**Large Candles also act like bookshelves for enchantment purposes.**\n\\\n\\\nCandles from Minecraft and other Mods may be used in place of Occultism candles.\n":
        "Les bougies apportent de la stabilité aux rituels et sont un élément important de presque tous les pentacles.\n**Les grandes bougies agissent aussi comme des bibliothèques pour l'enchantement.**\n\\\n\\\nLes bougies de Minecraft et d'autres mods peuvent remplacer les bougies de l'Occultisme.\n",
    "Just like the candles from Minecraft, [](item://occultism:large_candle) and colored versions can be lit, turning in a great light source.\n\\\nIn addition, you can use a [](item://minecraft:torch), [](item://minecraft:soul_torch), [](item://minecraft:redstone_torch) or [](item://occultism:spirit_torch) to change the type of fire.\n\\\nAlso can be waterlogged.\n":
        "Tout comme les bougies de Minecraft, la [](item://occultism:large_candle) et ses versions colorées peuvent être allumées, devenant une excellente source de lumière.\n\\\nDe plus, vous pouvez utiliser une [](item://minecraft:torch), [](item://minecraft:soul_torch), [](item://minecraft:redstone_torch) ou [](item://occultism:spirit_torch) pour changer le type de flamme.\n\\\nElles peuvent aussi être immergées.\n",
    "Key ingredient for large candles. Kill large animals like pigs, cows or sheep with a [](item://occultism:butcher_knife)\nto harvest [](item://occultism:tallow).\n":
        "Ingrédient clé des grandes bougies. Tuez de grands animaux comme cochons, vaches ou moutons avec un [](item://occultism:butcher_knife)\npour récolter du [](item://occultism:tallow).\n",
    "Right-clicking on Spirit Fire with a Chalk will change the color of the flames.\\\n\\\nDye dye dye, its muffin time.\n":
        "Faire un clic droit sur le feu spirituel avec une craie change la couleur des flammes.\\\n\\\nTeins, teins, teins, c'est l'heure du muffin.\n",
    "For more advanced rituals the basic [White Chalk](entry://occultism:dictionary_of_spirits/getting_started/ritual_prep_chalk) is not sufficient. Instead chalks made from more arcane materials are required.\n":
        "Pour les rituels plus avancés, la [Craie blanche](entry://occultism:dictionary_of_spirits/getting_started/ritual_prep_chalk) de base ne suffit pas. Il faut alors des craies faites à partir de matériaux plus arcanes.\n",
    "Follow the progression in [Pentacle page](category://pentacles) to get the 16 chalks and do all pentacles,\n":
        "Suivez la progression dans la [page des Pentacles](category://pentacles) pour obtenir les 16 craies et réaliser tous les pentacles.\n",
    "Infusion rituals are all about crafting powerful items, by binding (\"infusing\") spirits into objects.The spirits will provide special functionality to the items.\n":
        "Les rituels d'infusion permettent de fabriquer des objets puissants en liant (« imprégnant ») des esprits dans des objets. Les esprits confèrent des fonctionnalités spéciales aux objets.\n",
    "To find more about Infusing items, see the [Infusion Rituals](category://crafting_rituals) Category.\n":
        "Pour en savoir plus sur l'imprégnation des objets, consultez la catégorie [Rituels d'infusion](category://crafting_rituals).\n",
})

# Demon's dream
T.update({
    "**Hint**: The otherworld materials you obtain by harvesting under the effects of[#](ad03fc)Third Eye[#]() **can be obtained more easily using [](item://occultism:spirit_fire)**. Proceed with the next entry in this book to learn more about spirit fire.\n":
        "**Astuce** : les matériaux d'outremonde que vous récoltez sous l'effet du [#](ad03fc)Troisième Œil[#]() **peuvent être obtenus plus facilement avec le [](item://occultism:spirit_fire)**. Passez à l'entrée suivante de ce livre pour en savoir plus sur le feu spirituel.\n",
    "Demon's Dream is a herb that gives humans the [#](ad03fc)Third Eye[#](),\nallowing them to see where the [#](ad03fc)Otherworld[#]() intersects with our own.\nSeeds can be found **by breaking grass**.\n**Consuming** the grown fruit activates the ability *with a certain chance*.\n":
        "Le Rêve du Démon est une herbe qui confère aux humains le [#](ad03fc)Troisième Œil[#](),\nleur permettant de voir où l'[#](ad03fc)Outremonde[#]() croise le nôtre.\nDes graines peuvent être trouvées **en cassant l'herbe**.\n**Consommer** le fruit mûr active la capacité *avec une certaine probabilité*.\n",
    "Multiple Demon's Dream fruits or seeds can be compressed into an essence that is much more potent. It *guarantees* the [#](ad03fc)Third Eye[#]() and provides it for a longer amount of time, but comes with a lot of (positive and negative) side effects.\n":
        "Plusieurs fruits ou graines de Rêve du Démon peuvent être compressés en une essence bien plus puissante. Elle *garantit* le [#](ad03fc)Troisième Œil[#]() et le procure pour une durée plus longue, mais s'accompagne de nombreux effets secondaires (positifs et négatifs).\n",
    "The essence can be purified in spirit fire (more on that later!) to obtain a version free from all negative side effects, while retaining the positive.\n":
        "L'essence peut être purifiée dans le feu spirituel (nous y reviendrons !) pour obtenir une version dénuée de tout effet négatif, tout en conservant les effets positifs.\n",
})

# Divination, familiar rituals intro, first ritual, etc.
T.update({
    "An additional function of the Divination Rod is to locate any ore,\n however this is not a default function and needs to be enabled,\n as we recommend using the Greedy familiar or Theurgy mod for this type of divination.\n If you want to enable this feature directly in Occultism Divination Rod, check\n \"Server Configuration > Items\" and set \"Divination c:ores\" to \"on\".\n":
        "Une fonction supplémentaire de la baguette de divination est de localiser n'importe quel minerai,\n mais cette fonction n'est pas activée par défaut et doit l'être manuellement,\n car nous recommandons d'utiliser le familier Avide ou le mod Theurgy pour ce type de divination.\n Si vous souhaitez activer cette fonctionnalité directement dans la baguette de divination de l'Occultisme, consultez\n « Configuration serveur > Objets » et passez « Divination c:ores » sur « on ».\n",
    "[#](ad03fc)Right-clicking[#]() without holding after a successful search will show the last found target block again.\n\\\n\\\nIf the mod *\"Theurgy\"* is installed the rod will not highlight the target block, but instead send a particle effect in the direction of the target block.\n":
        "[#](ad03fc)Clic droit[#]() sans maintenir après une recherche réussie réaffichera le dernier bloc cible trouvé.\n\\\n\\\nSi le mod *« Theurgy »* est installé, la baguette ne mettra pas en surbrillance le bloc cible, mais enverra à la place un effet de particules dans sa direction.\n",
    "If the rod does not create highlighted blocks for you, you can try to:\n- If you have theurgy mod installed, then a particle effect will be used instead, set the particles to all or decreased in the video settings\n- Open occultism-client.toml in your instance's /config folder and set useAlternativeDivinationRodRenderer = true\n":
        "Si la baguette ne met pas de blocs en surbrillance, essayez :\n- Si vous avez le mod theurgy, un effet de particules est utilisé à la place ; passez les particules sur « toutes » ou « diminuées » dans les paramètres vidéo.\n- Ouvrez occultism-client.toml dans le dossier /config de votre instance et passez useAlternativeDivinationRodRenderer à true.\n",
    "Familiars provide a variety of bonus effects, such as feather falling, water breathing, jump boosts and more, and may also assist you in combat.\n\\\n\\\nStore them in a [Familiar Ring](entry://crafting_rituals/craft_familiar_ring) to equip them as a curio.\n":
        "Les familiers procurent divers effets bonus, comme la chute amortie, la respiration sous l'eau, le bonus de saut, et bien plus, et peuvent aussi vous aider au combat.\n\\\n\\\nRangez-les dans un [Anneau de familier](entry://crafting_rituals/craft_familiar_ring) pour les équiper en Curio.\n",
    "To find more about Familiars, see the [Familiar Rituals](category://familiar_rituals) Category.\n":
        "Pour en savoir plus sur les familiers, consultez la catégorie [Rituels de familiers](category://familiar_rituals).\n",
    "Instead of right-clicking the golden ritual bowl with the final ingredient, you can also use a Hopper or any type of pipe to insert the item into the bowl. The ritual will start automatically.\\\nNote that any rituals that summon tamed animals or familiars will summon them untamed instead.\n":
        "Au lieu de faire clic droit sur le bol rituel doré avec l'ingrédient final, vous pouvez aussi utiliser un entonnoir ou n'importe quel type de tuyau pour y insérer l'objet. Le rituel démarrera automatiquement.\\\nNote : tout rituel qui invoque des animaux apprivoisés ou des familiers les invoquera non apprivoisés à la place.\n",
    "The setup of upside-down bowl, also produce [](item://occultism:flame_of_automation) when the ritual don't has an item as output.\nFor example, this can be used to automate spirit summoning and possessing, as a return to your system (it will come with the NBT of the ritual performed).\n":
        "La configuration du bol renversé produit aussi une [](item://occultism:flame_of_automation) quand le rituel n'a pas d'objet en résultat.\nCela permet par exemple d'automatiser l'invocation et la possession d'esprits, comme retour vers votre système (il aura le NBT du rituel effectué).\n",
    "Some possible locations for the sacrificial bowls.\n":
        "Quelques emplacements possibles pour les bols sacrificiels.\n",
    "Next, place *at least* 4 [Sacrificial Bowls](item://occultism:sacrificial_bowl) close to the pentacle.\n\\\n\\\nThey must be placed **anywhere** within 8 blocks of the central [](item://occultism:golden_sacrificial_bowl). **The exact location does not matter.**\n":
        "Ensuite, placez *au moins* 4 [Bols sacrificiels](item://occultism:sacrificial_bowl) à proximité du pentacle.\n\\\n\\\nIls doivent être placés **n'importe où** dans un rayon de 8 blocs autour du [](item://occultism:golden_sacrificial_bowl) central. **L'emplacement exact n'a pas d'importance.**\n",
    "One suggestion is to use any block that interacts with redstone and an observer.\n":
        "Une suggestion est d'utiliser n'importe quel bloc qui interagit avec la redstone et un observateur.\n",
    "You can place another [](item://occultism:golden_sacrificial_bowl) in the third block below the\n original [](item://occultism:golden_sacrificial_bowl). Every time this new bowl receives an\n block update, it clones the actual signal strength of the original bowl.\n":
        "Vous pouvez placer un autre [](item://occultism:golden_sacrificial_bowl) au troisième bloc sous le\n [](item://occultism:golden_sacrificial_bowl) d'origine. Chaque fois que ce nouveau bol reçoit\n une mise à jour de bloc, il clone la force réelle du signal du bol d'origine.\n",
    "These pages will walk the gentle reader through the process of the [first ritual](entry://summoning_rituals/summon_crusher_t1) step by step.\n\\\nWe **start** by placing the [](item://occultism:golden_sacrificial_bowl) and drawing the appropriate pentacle, [Aviar's Circle](entry://pentacles/summon_foliot) as seen on the left around it.\n":
        "Ces pages guident le lecteur, étape par étape, à travers le processus du [premier rituel](entry://summoning_rituals/summon_crusher_t1).\n\\\nNous **commençons** par placer le [](item://occultism:golden_sacrificial_bowl) et tracer le pentacle approprié, le [Cercle d'Aviar](entry://pentacles/summon_foliot) comme on le voit à gauche.\n",
    "Only the color and location of the chalk marks is relevant, not the glyph/sign.\n":
        "Seules la couleur et la position des marques de craie comptent, pas le glyphe/signe.\n",
    "Ritual recipe pages, such as the previous pageshow not only the ingredients, but also the pentacle that you need to draw with chalk in order to use the ritual.\n\\\n\\\n**To show the pentacle, click the blue link** at the center top of the ritual page. You can then even preview it in-world.\n":
        "Les pages de recettes rituelles, comme la précédente, montrent non seulement les ingrédients, mais aussi le pentacle à tracer à la craie pour utiliser le rituel.\n\\\n\\\n**Pour afficher le pentacle, cliquez sur le lien bleu** au centre supérieur de la page du rituel. Vous pouvez même le prévisualiser dans le monde.\n",
    "Depending on the ritual state the golden bowl will emit a different redstone level:\n- **0** if no ritual is active\n- **1** if the ritual is active, but waiting for a sacrifice\n- **2** if the ritual is active, but waiting for an item to be used\n- **8** if the ritual is active and running\n":
        "Selon l'état du rituel, le bol doré émet un niveau de redstone différent :\n- **0** si aucun rituel n'est actif\n- **1** si le rituel est actif, mais attend un sacrifice\n- **2** si le rituel est actif, mais attend qu'un objet soit utilisé\n- **8** si le rituel est actif et en cours\n",
    "Now it is time to place the ingredients you see on the next page in the (regular, not golden) sacrificial bowls. The ingredients will be consumed from the bowls as the ritual progresses.\n":
        "Il est maintenant temps de placer les ingrédients indiqués à la page suivante dans les bols sacrificiels (réguliers, pas dorés). Les ingrédients seront consommés depuis les bols au fur et à mesure du rituel.\n",
    "Finally, [#](ad03fc)right-click[#]() the [](item://occultism:golden_sacrificial_bowl) with the **bound** book of binding you created before and wait until the crusher spawns.\n\\\n\\\nNow all that remains is to drop appropriate ores near the crusher and wait for it to turn it into dust.\n":
        "Enfin, faites [#](ad03fc)clic droit[#]() sur le [](item://occultism:golden_sacrificial_bowl) avec le livre de liaison **lié** que vous avez créé et attendez que le broyeur apparaisse.\n\\\n\\\nIl ne reste plus qu'à laisser tomber les minerais appropriés près du broyeur et à attendre qu'il les transforme en poussière.\n",
    "If you want to hold crafted items instead of dropping them into the world, place a sacrificial bowl facing down above the golden one.\nThis works up to three blocks higher and can also be used with a copper or silver sacrificial bowl.\n":
        "Si vous voulez conserver les objets fabriqués plutôt que les laisser tomber dans le monde, placez un bol sacrificiel orienté vers le bas au-dessus du bol doré.\nCela fonctionne jusqu'à trois blocs au-dessus et peut aussi être utilisé avec un bol sacrificiel en cuivre ou argent.\n",
    "If a ritual appears stuck - no items being consumed - you should see grey particles around the [](item://occultism:golden_sacrificial_bowl). If this is the case the ritual requires you to either [use a specific item](entry://rituals/item_use) or [sacrifice a specific mob](entry://rituals/sacrifice).\n\\\n\\\nFind the ritual in the [Rituals](category://rituals) category and check for instructions.\n":
        "Si un rituel semble bloqué — aucun objet n'est consommé — vous devriez voir des particules grises autour du [](item://occultism:golden_sacrificial_bowl). Dans ce cas, le rituel exige soit d'[utiliser un objet spécifique](entry://rituals/item_use), soit de [sacrifier un mob spécifique](entry://rituals/sacrifice).\n\\\n\\\nTrouvez le rituel dans la catégorie [Rituels](category://rituals) et consultez les instructions.\n",
    "Right-click a spirit with [](item://occultism:datura) to heal it.\n\\\n\\\nThis will work on **Familiars**, **Summoned Spirits** and also **Possessed Mobs**.\n":
        "Faites clic droit sur un esprit avec du [](item://occultism:datura) pour le soigner.\n\\\n\\\nCela fonctionne sur les **familiers**, les **esprits invoqués** et aussi les **mobs possédés**.\n",
    "When compressing Demon's Dream fruits or seeds into essence, a much stronger instant healing effect can be achieved. This comes at the cost of efficiency: Feeding 9 fruits to a spirit in succession will heal it more than feeding it 9 fruits worth of essence.\n":
        "En compressant les fruits ou graines de Rêve du Démon en essence, on obtient un effet de soin instantané bien plus fort. Cela se fait au prix de l'efficacité : nourrir 9 fruits à la suite à un esprit le soignera plus que de lui donner l'équivalent de 9 fruits sous forme d'essence.\n",
    "Purifying the Demon's Dream Essence will yield a version that heals even more, negating the efficiency loss.\n":
        "Purifier l'Essence du Rêve du Démon donne une version qui soigne encore plus, annulant la perte d'efficacité.\n",
})

# iesnium, infused pickaxe, intro, magic_lamps, mineshaft, otherworld_goggles, possession_rituals, ritual_prep
T.update({
    "Iesnium can only be mined with the [Infused Pickaxe](entry://getting_started/infused_pickaxe) or an [](item://occultism:iesnium_pickaxe) (about which you will learn later).\n\\\n\\\nAfter identifying a block that holds Iesnium, you can mine it with the pickaxe you created in the previous step.\n":
        "L'iesnium ne peut être miné qu'avec la [Pioche imprégnée](entry://getting_started/infused_pickaxe) ou une [](item://occultism:iesnium_pickaxe) (que vous verrez plus tard).\n\\\n\\\nUne fois un bloc contenant de l'iesnium identifié, minez-le avec la pioche créée à l'étape précédente.\n",
    "One of the uses of iesnium is the creation of Otherglass, this block hides from common eyes and is revealed only to those who see the other world. To collect this you need an infused or iesnium pickaxe.\n":
        "L'une des utilisations de l'iesnium est la création de Verre d'ailleurs, un bloc qui se cache des yeux communs et n'apparaît qu'à ceux qui voient l'autre monde. Pour le récolter, il faut une pioche imprégnée ou en iesnium.\n",
    "Iesnium ore, when mined, will drop [](item://occultism:raw_iesnium) that can be smelted directly into ingots.\nLike common ores, this is affected by Fortune and Silk Touch. If mined with silk, it will drop\n a stabilized version of Iesnium Ore, which can be mined with any pickaxe when placed back on the ground.\n":
        "Le minerai d'iesnium, une fois miné, laisse tomber du [](item://occultism:raw_iesnium) qui peut être fondu directement en lingots.\nComme les minerais courants, il est affecté par Fortune et Toucher de soie. Miné avec Toucher de soie, il laisse tomber\n une version stabilisée du Minerai d'iesnium, qui peut être miné avec n'importe quelle pioche une fois replacé au sol.\n",
    "This is a rare metal that, to the naked eye, looks like [](item://minecraft:netherrack) and cannot be mined with a regular pickaxe.\n\\\n\\\nWhen mined with the correct tools, it can be used to craft powerful items (you will learn more about that later).\n":
        "C'est un métal rare qui, à l'œil nu, ressemble à du [](item://minecraft:netherrack) et ne peut être miné avec une pioche ordinaire.\n\\\n\\\nMiné avec les bons outils, il peut servir à fabriquer des objets puissants (vous en apprendrez plus tard).\n",
    "Iesnium can be used to craft an improved pickaxe, spirit lamps, and other powerful items. Follow the progress in this book to learn more about it.\n":
        "L'iesnium peut servir à fabriquer une pioche améliorée, des lampes spirituelles et d'autres objets puissants. Suivez la progression dans ce livre pour en savoir plus.\n",
    "Like Netherrack, Iesnium can be found in the Nether. In order to **see** it, you need to wear [Otherworld Goggles](entry://getting_started/otherworld_goggles).\n\\\n\\\nTo make searching for it simpler, attune a [Divination Rod](entry://getting_started/divination_rod) to it and righ-click and hold in the nether until it highlights a nearby block, which will hold the ore.\n":
        "Comme la Netherrack, l'iesnium se trouve dans le Nether. Pour **le voir**, il faut porter les [Lunettes d'outremonde](entry://getting_started/otherworld_goggles).\n\\\n\\\nPour simplifier la recherche, accordez une [Baguette de divination](entry://getting_started/divination_rod) dessus et faites clic droit maintenu dans le Nether jusqu'à ce qu'elle mette un bloc proche en surbrillance, qui contiendra le minerai.\n",
    "Like the [Infused Pickaxe](entry://getting_started/infused_pickaxe), this pickaxe can be used to mine Tier 2 Otherworld Materials such as [](item://occultism:iesnium_ore). As it is made from metal, instead of brittle [](item://occultism:spirit_attuned_gem), it is very durable and can be used for a long time.\n":
        "Comme la [Pioche imprégnée](entry://getting_started/infused_pickaxe), cette pioche permet de miner les matériaux d'outremonde de palier 2 comme le [](item://occultism:iesnium_ore). Étant en métal, plutôt qu'en [](item://occultism:spirit_attuned_gem) fragile, elle est très durable et utilisable longtemps.\n",
    "After preparing the raw materials, the pickaxe needs to be infused with a spirit.\n\\\n\\\nFollow the instructions at [Craft Infuse Pickaxe](entry://crafting_rituals/craft_infused_pickaxe)\n":
        "Après préparation des matières premières, la pioche doit être imprégnée d'un esprit.\n\\\n\\\nSuivez les instructions à [Fabriquer la pioche imprégnée](entry://crafting_rituals/craft_infused_pickaxe).\n",
    "These gems, when infused with a spirit, can be used to interact with Otherword materials and are the key to crafting the pickaxe.\n":
        "Ces gemmes, une fois imprégnées d'un esprit, permettent d'interagir avec les matériaux d'outremonde et sont la clé pour fabriquer la pioche.\n",
    "Beyond [](item://occultism:otherworld_log) and [](item://occultism:otherstone) there are also otherworld materials that require special tools to harvest.\n\\\n\\\nThis pickaxe is rather brittle, but it will do the job.\n":
        "Au-delà des [](item://occultism:otherworld_log) et de la [](item://occultism:otherstone), il existe d'autres matériaux d'outremonde qui requièrent des outils spéciaux.\n\\\n\\\nCette pioche est plutôt fragile, mais elle fera l'affaire.\n",
    "This book aims to introduce the novice reader to the most common summoning rituals and equip them with a list of spirit names to summon.\nThe authors advise caution in the summoning of the listed entities and does not take responsibility for any harm caused.\n":
        "Ce livre vise à initier le lecteur novice aux rituels d'invocation les plus courants et à lui fournir une liste de noms d'esprits à invoquer.\nLes auteurs conseillent la prudence dans l'invocation des entités listées et déclinent toute responsabilité pour les préjudices causés.\n",
    "Magic Lamps can be used to keep spirits safe from [#](ad03fc)Essence Decay[#]() (if the spirit has decay), while still having access to some of their powers. Right-Click on one of your workers to store and transport it as desired.\n":
        "Les lampes magiques permettent de protéger les esprits de la [#](ad03fc)Décrépitude de l'essence[#]() (s'ils en sont sujets), tout en conservant l'accès à certains de leurs pouvoirs. Faites clic droit sur l'un de vos travailleurs pour le stocker et le transporter à votre guise.\n",
    "See [Dimensional Mineshaft](entry://crafting_rituals/craft_dimensional_mineshaft) in the [Binding Rituals](category://crafting_rituals) Category.\n":
        "Voir [Puits dimensionnel](entry://crafting_rituals/craft_dimensional_mineshaft) dans la catégorie [Rituels de liaison](category://crafting_rituals).\n",
    "This block acts as a portal, for spirits only, to the [#](ad03fc)Mining Dimension[#](). Place a Magic Lamp with a Miner Spirit in it, to make it mine for you.\n":
        "Ce bloc fait office de portail, pour les esprits seulement, vers la [#](ad03fc)Dimension minière[#](). Placez-y une lampe magique contenant un esprit mineur pour qu'il mine pour vous.\n",
    "Crafting these goggles is a multi-step process described in detail in the Entry about [Crafting Otherworld Goggles](entry://crafting_rituals/craft_otherworld_goggles).\n":
        "La fabrication de ces lunettes est un processus en plusieurs étapes décrit en détail dans l'entrée [Fabriquer les lunettes d'outremonde](entry://crafting_rituals/craft_otherworld_goggles).\n",
    "The [](item://occultism:otherworld_goggles) are what advanced summoners use to see the [#](ad03fc)Otherworld[#](), to avoid the negative side effects of [](entry://occultism:dictionary_of_spirits/getting_started/demons_dream).\n\\\n\\\nMaking your first pair of these is seen by many as a rite of passage.\n":
        "Les [](item://occultism:otherworld_goggles) sont ce que les invocateurs expérimentés utilisent pour voir l'[#](ad03fc)Outremonde[#](), évitant les effets secondaires négatifs du [](entry://occultism:dictionary_of_spirits/getting_started/demons_dream).\n\\\n\\\nFabriquer sa première paire est considéré par beaucoup comme un rite de passage.\n",
    "Possessed mobs are controlled by spirits, allowing the summoner to determine some of their properties. They usually have **high drop rates** for rare drops, but are generally harder to kill.\n\\\n\\\nYou probably will want to start by summoning a [Possessed Endermite](entry://possession_rituals/possess_endermite) to get [](item://minecraft:end_stone) to craft [Advanced Chalks](entry://getting_started/chalks).\n":
        "Les mobs possédés sont contrôlés par des esprits, ce qui permet à l'invocateur de déterminer certaines de leurs propriétés. Ils ont généralement des **taux de drop élevés** pour les butins rares, mais sont plus difficiles à tuer.\n\\\n\\\nVous voudrez sans doute commencer par invoquer un [Endermite possédé](entry://possession_rituals/possess_endermite) pour obtenir de la [](item://minecraft:end_stone) afin de fabriquer les [Craies avancées](entry://getting_started/chalks).\n",
    "To find out more about Possession Rituals, see the [Possession Rituals](category://possession_rituals) Category.\n":
        "Pour en savoir plus sur les rituels de possession, consultez la catégorie [Rituels de possession](category://possession_rituals).\n",
    "Once everything has been set up and you are ready to start, this special ritual bowl is used to activate the ritual by [#](ad03fc)right-clicking[#]() it with the activation item,\nusually a [Book of Binding](entry://getting_started/books_of_binding).\n":
        "Une fois tout en place et prêt à démarrer, ce bol rituel spécial sert à activer le rituel par [#](ad03fc)clic droit[#]() avec l'objet d'activation,\nhabituellement un [Livre de liaison](entry://getting_started/books_of_binding).\n",
    "These bowls are used to place the items we will sacrifice as part of a ritual and you will need a handful of them.\nNote: Their exact placement in the ritual does not matter - just keep them within 8 blocks horizontally of the pentacle center!\n":
        "Ces bols servent à placer les objets que nous sacrifierons dans le cadre d'un rituel ; il vous en faudra une poignée.\nNote : leur emplacement exact dans le rituel n'a pas d'importance — gardez-les juste à moins de 8 blocs horizontalement du centre du pentacle !\n",
    "You can mix a sacrificial bowl with a copper or silver ingot to create variations with the same functionality.\n":
        "Vous pouvez combiner un bol sacrificiel avec un lingot de cuivre ou d'argent pour créer des variantes ayant la même fonctionnalité.\n",
    "If you place a sacrificial bowl above a Spirit Fire or Spirit Campfire,\nany item inserted will instantly transform if it has a recipe in the spirit fire.\\\nAlso work with copper or silver version of sacrificial bowl.\n":
        "Si vous placez un bol sacrificiel au-dessus d'un feu spirituel ou d'un feu de camp spirituel,\ntout objet inséré sera instantanément transformé s'il a une recette dans le feu spirituel.\\\nFonctionne aussi avec la version cuivre ou argent du bol sacrificiel.\n",
    "To summon spirits from the [#](ad03fc)Other Place[#]() in *relative* safety,\nyou need to draw a fitting pentacle using chalk to contain their powers.\n":
        "Pour invoquer des esprits depuis l'[#](ad03fc)Autre Lieu[#]() en *relative* sécurité,\nvous devez tracer un pentacle adéquat à la craie pour contenir leurs pouvoirs.\n",
    "Right-click on a block with the chalk to draw a single glyph. For decorative purposes you can repeatedly click a block to cycle through glyphs. The shown glyph does not matter for the ritual, only the color.\n":
        "Faites clic droit sur un bloc avec la craie pour tracer un seul glyphe. À des fins décoratives, vous pouvez cliquer plusieurs fois sur un bloc pour faire défiler les glyphes. Le glyphe affiché n'a pas d'importance pour le rituel, seule la couleur compte.\n",
    "White chalk is used to draw the most basic pentacles, such as for our first ritual.\n\\\n\\\nMore powerful summonings require appropriate more advanced chalk, see [Chalks](entry://occultism:dictionary_of_spirits/getting_started/chalks) for more information.\n":
        "La craie blanche sert à tracer les pentacles les plus basiques, comme celui de notre premier rituel.\n\\\n\\\nLes invocations plus puissantes requièrent des craies plus avancées appropriées ; voir [Craies](entry://occultism:dictionary_of_spirits/getting_started/chalks) pour plus d'informations.\n",
    "Visit the entry about the [Apprentice Satchel](entry://crafting_rituals/apprentice_ritual_satchel) or the [Artisanal Satchel](entry://crafting_rituals/apprentice_ritual_satchel) in the [Binding Rituals Category](category://crafting_rituals) to learn how to enchant a satchel and use it for rituals.\n":
        "Consultez l'entrée sur la [Besace d'apprenti](entry://crafting_rituals/apprentice_ritual_satchel) ou la [Besace artisanale](entry://crafting_rituals/apprentice_ritual_satchel) dans la catégorie [Rituels de liaison](category://crafting_rituals) pour apprendre à enchanter une besace et l'utiliser pour les rituels.\n",
    "Ritual satchels are bags that can hold items needed to create pentacles for rituals.\\\nMore importantly, they can automatically place the right items for a pentacle, removing the need to manually place chalks, candles, crystals, skulls and other items needed for rituals.\\\\\nThe Apprentice Satchel places pentacle blocks one by one.\\\nThe improved Artisanal Satchel places all pentacle blocks in a single action.\\\n":
        "Les besaces rituelles sont des sacs qui contiennent les objets nécessaires à la création de pentacles pour les rituels.\\\nPlus important encore, elles peuvent placer automatiquement les bons objets pour un pentacle, évitant le placement manuel des craies, bougies, cristaux, crânes et autres objets.\\\\\nLa besace d'apprenti place les blocs du pentacle un par un.\\\nLa besace artisanale améliorée place tous les blocs du pentacle en une seule action.\\\n",
    "An easier way to clone any dye, mix this flower and the target color. You can also make ~~suspicious~~ delicious stews.\n":
        "Une façon plus simple de cloner n'importe quel colorant : combinez cette fleur et la couleur cible. Vous pouvez aussi préparer de ~~suspects~~ délicieux ragoûts.\n",
    "Otherrock is a variation of [](item://occultism:otherstone),\n you can use it for decoration and making sacrificial bowls,\n  but it does not work as a base for chalks or dimensional storage.\n":
        "La pierre d'ailleurs est une variation de la [](item://occultism:otherstone) ;\n vous pouvez l'utiliser pour la décoration et la fabrication de bols sacrificiels,\n  mais elle ne fonctionne pas comme base pour les craies ou le stockage dimensionnel.\n",
    "By summoning a spirit into a Magic Lamp and placing it in a [Dimensional Mineshaft (see next step)](entry://getting_started/mineshaft) it can be made to mine for you in a [#](ad03fc)Mining Dimension[#]().\nSee [Foliot Miner](entry://crafting_rituals/craft_foliot_miner) and the subsequent entries for information on how to craft spirit miners.\n":
        "En invoquant un esprit dans une lampe magique et en la plaçant dans un [Puits dimensionnel (étape suivante)](entry://getting_started/mineshaft), vous pouvez le faire miner pour vous dans une [#](ad03fc)Dimension minière[#]().\nVoir [Mineur Foliot](entry://crafting_rituals/craft_foliot_miner) et les entrées suivantes pour savoir comment fabriquer des esprits mineurs.\n",
    "Lamps are commonly used to access a [#](ad03fc)Mining Dimension[#]() and act as (*lag free*) [#](ad03fc)Void Miners[#]().\n This is a great way to get resources without having to go mining in the overworld (or other dimesions) yourself.\n":
        "Les lampes sont couramment utilisées pour accéder à une [#](ad03fc)Dimension minière[#]() et servent de [#](ad03fc)Mineurs du vide[#]() (*sans lag*).\n C'est un excellent moyen d'obtenir des ressources sans avoir à miner soi-même dans la surface (ou d'autres dimensions).\n",
    "Summoning Rituals allow you to summon spirits to work for you. Unlike familiars, they are not personally bound to you, meaning they will not follow you around, but they will perform various work tasks for you. In fact the first ritual you performed, the [Foliot Crusher](entry://getting_started/first_ritual), was a summoning ritual.\n":
        "Les rituels d'invocation vous permettent d'invoquer des esprits pour travailler pour vous. Contrairement aux familiers, ils ne sont pas personnellement liés à vous : ils ne vous suivront pas, mais accompliront diverses tâches. En fait, le premier rituel que vous avez effectué, le [Broyeur Foliot](entry://getting_started/first_ritual), était un rituel d'invocation.\n",
    "To find more about Summoning Rituals, see the [Summoning Rituals](category://summoning_rituals) Category.\n":
        "Pour en savoir plus sur les rituels d'invocation, consultez la catégorie [Rituels d'invocation](category://summoning_rituals).\n",
    "While the [](item://occultism:divination_rod) is a great tool for finding [#](ad03fc)Otherworld Materials[#](), it would be useful to have a way to find *all other* ores and resources as well.\n\\\n\\\nThis is where the Theurgy Divination Rod comes in.\n":
        "Bien que la [](item://occultism:divination_rod) soit un excellent outil pour trouver les [#](ad03fc)Matériaux d'outremonde[#](), il serait utile d'avoir un moyen de trouver *tous les autres* minerais et ressources.\n\\\n\\\nC'est là qu'intervient la baguette de divination Theurgy.\n",
    "To find out more about the Theurgy Divination Rod, check out *\"The Hermetica\"*, the Guidebook for Theurgy.\n[This Entry](entry://theurgy:the_hermetica/getting_started/about_divination_rods) has more information about the Theurgy Divination Rod.\n":
        "Pour en savoir plus sur la baguette de divination Theurgy, consultez *« The Hermetica »*, le guide de Theurgy.\n[Cette entrée](entry://theurgy:the_hermetica/getting_started/about_divination_rods) contient plus d'informations sur la baguette de divination Theurgy.\n",
})

# Pentacles
T.update({
    "The black chalk has a composition as rigid as it is supernatural. Mixing the essence of\n Wither with netherite turns this chalk into an extremely valuable tool.\n":
        "La craie noire a une composition aussi rigide que surnaturelle. Mélanger l'essence du\n Wither avec du netherite fait de cette craie un outil extrêmement précieux.\n",
    "Perfect for the foundation of any pentacle, the power of the black chalk is sufficient\n to replace any other \"colorless\" chalk.\n":
        "Parfaite pour la fondation de tout pentacle, la puissance de la craie noire suffit\n à remplacer toute autre craie « incolore ».\n",
    "To obtain the essence of a [#](AA00AA)Marid[#]() for [](item://occultism:chalk_blue) you need to\n [summon and kill an Unbound Marid](entry://summoning_rituals/marid_essence).\n":
        "Pour obtenir l'essence d'un [#](AA00AA)Marid[#]() pour la [](item://occultism:chalk_blue), il faut\n [invoquer et tuer un Marid non lié](entry://summoning_rituals/marid_essence).\n",
    "Just as the red chalk is made from the essence of Afrit, the blue chalk is made\n from the essence of Marid, allowing for control over these powerful spirits.\n":
        "Tout comme la craie rouge est faite de l'essence d'Afrit, la craie bleue est faite\n de l'essence de Marid, permettant le contrôle de ces puissants esprits.\n",
    "The purpose of the blue chalk is to overcome the willpower of a Marid; its sometimes\n excessive use serves as a guarantee that any Marid will be controlled.\n Should the control fail, it would generate extreme fury in the invoked Marid.\n":
        "Le but de la craie bleue est de surmonter la volonté d'un Marid ; son usage parfois\n excessif sert de garantie que tout Marid sera contrôlé.\n Si le contrôle échoue, cela provoquerait une fureur extrême chez le Marid invoqué.\n",
    "To obtain the [](item://occultism:cruelty_essence) for [](item://occultism:chalk_brown) you need to\n [summon and kill a Mercy Goat](entry://possession_rituals/possess_goat)\n":
        "Pour obtenir l'[](item://occultism:cruelty_essence) pour la [](item://occultism:chalk_brown), il faut\n [invoquer et tuer une Chèvre de la Miséricorde](entry://possession_rituals/possess_goat).\n",
    "The brown chalk is made with the essence of cruelty, and obtaining it certainly lives up\n to its name. Do the ends justify the means? Does morality truly exist? What is your morality?\n":
        "La craie marron est faite de l'essence de cruauté, et son obtention est à la hauteur\n de son nom. La fin justifie-t-elle les moyens ? La moralité existe-t-elle vraiment ? Quelle est la vôtre ?\n",
    "This chalk is known to be part of an \"Alignment Test.\" Anyone who possesses it is\n automatically classified as \"Evil.\" What kind of spirits will these glyphs attract?\n":
        "Cette craie est connue pour faire partie d'un « Test d'alignement ». Quiconque la possède est\n automatiquement classé comme « Maléfique ». Quel type d'esprits ces glyphes attireront-ils ?\n",
    "**Purpose:** Contact [#](AA00AA)Eldritch[#]()\\\n\\\nThis strange pentacle uses forbidden knowledge, bringing together paraphernalia from ancient traditions.\\\nThe level of power that can be achieved almost cheats the common reality.\n":
        "**But :** Contacter les [#](AA00AA)Eldritch[#]()\\\n\\\nCe pentacle étrange utilise un savoir interdit, rassemblant des accessoires de traditions anciennes.\\\nLe niveau de puissance atteignable triche presque avec la réalité commune.\n",
    "- [Eldritch Ancient Miner](entry://crafting_rituals/craft_ancient_miner)\n- [Storage Stabilizer Tier 5](entry://crafting_rituals/stabilizer_tier5)\n- [Stabilized Storage](entry://crafting_rituals/craft_stabilized_storage)\n- [Eldritch Chalice](entry://crafting_rituals/craft_eldritch_chalice)\n- [Mastery Chalks](entry://crafting_rituals/craft_master_chalks)\n- [Trinity Gem](entry://crafting_rituals/trinity_gem)\n":
        "- [Mineur ancien Eldritch](entry://crafting_rituals/craft_ancient_miner)\n- [Stabilisateur de stockage palier 5](entry://crafting_rituals/stabilizer_tier5)\n- [Stockage stabilisé](entry://crafting_rituals/craft_stabilized_storage)\n- [Calice Eldritch](entry://crafting_rituals/craft_eldritch_chalice)\n- [Craies de maîtrise](entry://crafting_rituals/craft_master_chalks)\n- [Gemme de la trinité](entry://crafting_rituals/trinity_gem)\n",
    "**Purpose:** Contact [#](AA00AA)Wild Spirits[#]()\\\n\\\n**Osorins Unbound Calling** has a unique form, mixing different aspects obtained in each chalk\n and none of the common stabilizing paraphernalia. Therefore, the pentacle offers no protection\n  to the occultist, but acts as an irresistible contact with the [#](AA00AA)Wild Spirits[#]().\n":
        "**But :** Contacter les [#](AA00AA)Esprits sauvages[#]()\\\n\\\n**L'Appel non lié d'Osorin** a une forme unique, mêlant divers aspects obtenus dans chaque craie\n et aucun des accessoires stabilisateurs habituels. Le pentacle n'offre donc aucune protection\n  à l'occultiste, mais agit comme un contact irrésistible avec les [#](AA00AA)Esprits sauvages[#]().\n",
})

# Apply
applied = 0
for k, v in src.items():
    if cur.get(k) == v and v in T:
        cur[k] = T[v]
        applied += 1

# Write everything that's still untranslated as a passthrough (we ran out of explicit lookups)
# But this is a sub-strategy: keep the English text for lore where we don't have a French version

# Actually, let me just save what we have
print(f"Pass 4 applied: {applied}")
remaining = [k for k in src if cur.get(k) == src[k]]
print(f"Remaining: {len(remaining)}")

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(cur, f, ensure_ascii=False, indent="\t")
print("Saved.")
