# -*- coding: utf-8 -*-
"""
Generates translations for bin_3 quests across 7 languages.
Output: phase3_output/bin_3.json
"""
import json
import os

INPUT = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit/phase3_bins/bin_3.json"
OUTPUT = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit/phase3_output/bin_3.json"

LANGS = ["en_us", "en_gb", "fr_fr", "es_es", "pt_br", "ru_ru", "zh_cn"]

# Translations as (en_us, en_gb, fr_fr, es_es, pt_br, ru_ru, zh_cn)
# When unsure for non-FR/EN, English is kept (per instructions).
# Each entry maps quest_id -> dict { field -> [7 strings] }
QUESTS = {}

def add(qid, **fields):
    QUESTS[qid] = fields

# --- 1) ARS NOUVEAU GLYPHS (titles missing) ---
# Glyph Magnet
add("519233F9ECFFFB20", title=["Magnet Glyph","Magnet Glyph","Glyphe d'Aimant","Glifo de Imán","Glifo de Ímã","Глиф Магнита","磁石符文"])
# Glyph Homing
add("71581B67D5E286FA", title=["Homing Glyph","Homing Glyph","Glyphe de Poursuite","Glifo Buscador","Glifo Teleguiado","Глиф Самонаведения","追踪符文"])
# Block Swap
add("7B075FDC32A35CB3", title=["Place Block Glyph","Place Block Glyph","Glyphe d'Échange","Glifo de Intercambio","Glifo de Troca","Глиф Замены Блока","换块符文"])
# AOE
add("21AD79EB30B78FAD", title=["AOE Glyph","AOE Glyph","Glyphe de Zone","Glifo de Área","Glifo de Área","Глиф Области","范围符文"])
# Wind Launch
add("2AA23E847500A749", title=["Launch Glyph (Wind)","Launch Glyph (Wind)","Glyphe de Souffle","Glifo de Viento","Glifo de Vento","Глиф Ветра","狂风符文"])
# Summon Horse
add("43C0FAF8B75E09C8", title=["Summon Horse Glyph","Summon Horse Glyph","Glyphe Invocation Cheval","Glifo Invocar Caballo","Glifo Invocar Cavalo","Глиф Призыва Лошади","召唤马符文"])
# Mana Regen Potion
add("453952AA18061F1E", title=["Mana Regen Potion","Mana Regen Potion","Potion de Régén. de Mana","Poción Regen. Maná","Poção Regen. de Mana","Зелье Восст. Маны","法力恢复药水"])
# Ender Inventory
add("669C0739EC8B5FFE", title=["Ender Inventory Glyph","Ender Inventory Glyph","Glyphe Inventaire Ender","Glifo Inventario Ender","Glifo Inventário Ender","Глиф Эндер-Инвентаря","末影背包符文"])
# Moonrise
add("06047C5DB745510C", title=["Ritual of the Moon","Ritual of the Moon","Rituel de la Lune","Ritual de la Luna","Ritual da Lua","Ритуал Луны","月升仪式"])
# Evoker Fangs
add("75156AD38DDE3F28", title=["Evoker Fangs Glyph","Evoker Fangs Glyph","Glyphe de Crocs","Glifo Colmillos Evocador","Glifo Presas do Evocador","Глиф Клыков Заклинателя","唤魔者尖牙符文"])
# Conjure Ore
add("05C9AA7F60F8E8E3", title=["Ritual of Conjured Ore","Ritual of Conjured Ore","Rituel de Minerai Invoqué","Ritual de Mineral Invocado","Ritual de Minério Invocado","Ритуал Призванной Руды","召唤矿物仪式"])
# Smelt
add("5379E18EDC98F833", title=["Smelt Glyph","Smelt Glyph","Glyphe de Fusion","Glifo de Fundición","Glifo de Fundir","Глиф Плавки","熔炼符文"])
# Mana Boost
add("4CE831BD6230D025", title=["Mana Boost Jewelry","Mana Boost Jewelry","Bijou de Mana","Joya de Maná","Joia de Mana","Украшение Маны","法力宝石"])
# Launch
add("305D35797BFCE667", title=["Launch Glyph","Launch Glyph","Glyphe de Propulsion","Glifo de Impulso","Glifo de Lançamento","Глиф Запуска","抛射符文"])
# Extract (Silk Touch)
add("4DFFB39721E88262", title=["Extract Glyph","Extract Glyph","Glyphe d'Extraction","Glifo de Extracción","Glifo de Extração","Глиф Извлечения","精准提取符文"])
# Diminish
add("259ED6EB8AECC080", title=["Diminish Glyph","Diminish Glyph","Glyphe de Réduction","Glifo de Reducción","Glifo de Redução","Глиф Уменьшения","减效符文"])
# Wind Gust
add("5F75869125A047C6", title=["Wind Gust Glyph","Wind Gust Glyph","Glyphe de Rafale","Glifo de Ráfaga","Glifo de Rajada","Глиф Порыва","气流符文"])
# Flight aura (duplicate)
add("2321D8598D681106", title=["Ritual of Flight","Ritual of Flight","Rituel de Vol","Ritual de Vuelo","Ritual de Voo","Ритуал Полёта","飞行仪式"])
add("06AE90F879892AA6", title=["Ritual of Flight","Ritual of Flight","Rituel de Vol","Ritual de Vuelo","Ritual de Voo","Ритуал Полёта","飞行仪式"])
# Extract dup
add("74AC2138AE5F51C6", title=["Extract Glyph","Extract Glyph","Glyphe d'Extraction","Glifo de Extracción","Glifo de Extração","Глиф Извлечения","精准提取符文"])
# Dispel
add("140F1F2F3D4A2E3A", title=["Dispel Glyph","Dispel Glyph","Glyphe de Dissipation","Glifo de Disipación","Glifo de Dissipar","Глиф Развеивания","驱散符文"])
# Moonrise dup
add("51FC406464E63F78", title=["Ritual of the Moon","Ritual of the Moon","Rituel de la Lune","Ritual de la Luna","Ritual da Lua","Ритуал Луны","月升仪式"])
# Scribes Table
add("424BBFB3FF744762", title=["Scribe's Table","Scribe's Table","Table du Scribe","Mesa del Escriba","Mesa do Escriba","Стол Писаря","抄录工作台"])
add("53BB3F652D6289B6", title=["Scribe's Table","Scribe's Table","Table du Scribe","Mesa del Escriba","Mesa do Escriba","Стол Писаря","抄录工作台"])
add("01DB20A3C7872F95", title=["Scribe's Table","Scribe's Table","Table du Scribe","Mesa del Escriba","Mesa do Escriba","Стол Писаря","抄录工作台"])
# Worn Notebook
add("684BB69D5E77438E", title=["Worn Notebook","Worn Notebook","Carnet Usé","Cuaderno Gastado","Caderno Gasto","Изношенный Дневник","旧笔记本"])
# Delay
add("61A7C7A55DAAA22F", title=["Delay Glyph","Delay Glyph","Glyphe de Délai","Glifo de Demora","Glifo de Atraso","Глиф Задержки","延迟符文"])
# Mage learning chapter
add("741CCE9216974243", title=["The Basics","The Basics","Les Bases","Lo Básico","O Básico","Основы","基础知识"])
# Freeze
add("75F4EBE08A3621F5", title=["Freeze Glyph","Freeze Glyph","Glyphe de Gel","Glifo Congelar","Glifo Congelar","Глиф Заморозки","冰冻符文"])
# Harm AOE
add("0F25FC8DC160B80C", title=["Harm AOE","Harm AOE","Glyphe de Mal en Zone","Glifo Daño en Área","Glifo Dano em Área","Глиф Урона по Зоне","范围伤害符文"])
add("14B0CA9812BA8BB9", title=["Harm AOE","Harm AOE","Glyphe de Mal en Zone","Glifo Daño en Área","Glifo Dano em Área","Глиф Урона по Зоне","范围伤害符文"])
# Harm
add("4533E4B95F980347", title=["Harm Glyph","Harm Glyph","Glyphe de Mal","Glifo de Daño","Glifo de Dano","Глиф Урона","伤害符文"])
# Launch (jump)
add("78FA200E48A442E9", title=["Launch Glyph","Launch Glyph","Glyphe de Propulsion","Glifo de Impulso","Glifo de Lançamento","Глиф Запуска","抛射符文"])
# Ender dup
add("47CA3DFE38D564E1", title=["Ender Inventory Glyph","Ender Inventory Glyph","Glyphe Inventaire Ender","Glifo Inventario Ender","Glifo Inventário Ender","Глиф Эндер-Инвентаря","末影背包符文"])
# Drygmy summon
add("1AEAEE7920A55D56", title=["Summon Drygmy","Summon Drygmy","Invocation de Drygmy","Invocar Drygmy","Invocar Drygmy","Призыв Дригми","召唤德里格米"])
add("453D65CA832B31CB", title=["Summon Drygmy","Summon Drygmy","Invocation de Drygmy","Invocar Drygmy","Invocar Drygmy","Призыв Дригми","召唤德里格米"])
# Ritual brazier
add("54AB269EC33881F5", title=["Ritual Brazier","Ritual Brazier","Brasero Rituel","Brasero Ritual","Braseiro Ritual","Ритуальная Жаровня","仪式火盆"])
# Scrying
add("4925EF7E1FE614FA", title=["Scrying Glyph","Scrying Glyph","Glyphe de Clairvoyance","Glifo de Adivinación","Glifo de Vidência","Глиф Прозрения","透视符文"])
add("2D578021CCFB4E6F", title=["Scrying Glyph","Scrying Glyph","Glyphe de Clairvoyance","Glifo de Adivinación","Glifo de Vidência","Глиф Прозрения","透视符文"])
# Mana regen potion dup
add("4963261E6AA7E1C9", title=["Mana Regen Potion","Mana Regen Potion","Potion de Régén. de Mana","Poción Regen. Maná","Poção Regen. de Mana","Зелье Восст. Маны","法力恢复药水"])
# Light/highlight
add("30F27300EE6457DA", title=["Light Ritual","Light Ritual","Rituel de Lumière","Ritual de Luz","Ritual de Luz","Ритуал Света","光明仪式"])
# Magebloom Fiber
add("64DDBCA5CC5B0812", title=["Magebloom Fiber","Magebloom Fiber","Fibre de Magefleur","Fibra de Magoflor","Fibra de Magoflor","Волокно Магоцвета","法师花纤维"])
# Ignite
add("1C81C0D5C8D22C84", title=["Ignite Glyph","Ignite Glyph","Glyphe d'Embrasement","Glifo de Encender","Glifo de Acender","Глиф Поджога","点燃符文"])
# Wixie summon
add("06B93D90145EE4A2", title=["Summon Wixie","Summon Wixie","Invocation de Wixie","Invocar Wixie","Invocar Wixie","Призыв Виксии","召唤维克西"])
# Raid summon
add("7B71513C24C94CBA", title=["Summon Raid","Summon Raid","Invocation de Raid","Invocar Incursión","Invocar Raide","Призыв Рейда","召唤袭击"])
# Growth
add("1C25A975E1A673DC", title=["Source Berry Bush","Source Berry Bush","Buisson de Sourcebaie","Arbusto de Bayafuente","Arbusto de Bagafonte","Куст Источных Ягод","源能浆果树"])
# Cosmetic block
add("463E36BB299DD4A0", title=["Conjure Block Glyph","Conjure Block Glyph","Glyphe Bloc Conjuré","Glifo Bloque Conjurado","Glifo Bloco Conjurado","Глиф Призванного Блока","召唤方块符文"])
# Place Block
add("78F845F5E6E520F3", title=["Place Block Glyph","Place Block Glyph","Glyphe Placer Bloc","Glifo Colocar Bloque","Glifo Colocar Bloco","Глиф Установки Блока","放置符文"])
# Summon Wolves
add("3FA34D10461B0F16", title=["Summon Wolves","Summon Wolves","Invocation de Loups","Invocar Lobos","Invocar Lobos","Призыв Волков","召唤狼"])
# Summon Vex
add("3BCFFBF76406EAE1", title=["Summon Vex","Summon Vex","Invocation de Vex","Invocar Vex","Invocar Vex","Призыв Векса","召唤恼鬼"])
# Heal
add("5636DD2B9699DA0D", title=["Heal Glyph","Heal Glyph","Glyphe de Soin","Glifo de Curación","Glifo de Cura","Глиф Лечения","治疗符文"])
# Linger
add("3BB44C7AD8F80870", title=["Linger Glyph","Linger Glyph","Glyphe de Persistance","Glifo Persistente","Glifo de Persistência","Глиф Затяжного","持续符文"])
# Awaken
add("4AC9DE5FA0294AC5", title=["Awaken Ritual","Awaken Ritual","Rituel d'Éveil","Ritual de Despertar","Ritual de Despertar","Ритуал Пробуждения","唤醒仪式"])
add("044C66D113CA4FEE", title=["Awaken Ritual","Awaken Ritual","Rituel d'Éveil","Ritual de Despertar","Ritual de Despertar","Ритуал Пробуждения","唤醒仪式"])
# Haste/speed
add("4A4898ECCD0BC85F", title=["Haste Glyph","Haste Glyph","Glyphe de Célérité","Glifo de Prisa","Glifo de Pressa","Глиф Спешки","加速符文"])
# Reflect
add("21AA1EC0BF4F7757", title=["Spell Reflect","Spell Reflect","Réflexion de Sort","Reflejo de Hechizo","Reflexão de Feitiço","Отражение Заклинания","法术反射"])
# Sense magical blocks
add("4892993217A9239A", title=["Imbuement Chamber","Imbuement Chamber","Chambre d'Infusion","Cámara de Imbuir","Câmara de Imbuir","Камера Зачарования","注入室"])
# Crush
add("3A09EF20746F2963", title=["Crush Glyph","Crush Glyph","Glyphe d'Écrasement","Glifo de Aplastar","Glifo de Esmagar","Глиф Сокрушения","粉碎符文"])
# Bonemeal
add("11E6A88296CFA2F8", title=["Growth Glyph","Growth Glyph","Glyphe de Croissance","Glifo de Crecimiento","Glifo de Crescimento","Глиф Роста","生长符文"])
# Explosion
add("72389F89AFB3DEC7", title=["Explosion Glyph","Explosion Glyph","Glyphe d'Explosion","Glifo de Explosión","Glifo de Explosão","Глиф Взрыва","爆炸符文"])
# Dowsing rod
add("700467184ED62E0F", title=["Dowsing Rod","Dowsing Rod","Baguette de Sourcier","Vara de Zahorí","Pêndulo","Лоза Поиска","探矿杖"])
# Glyph press / chalk
add("1093BEFB6965D1D0", title=["Ritual Chalk","Ritual Chalk","Craie Rituelle","Tiza Ritual","Giz Ritual","Ритуальный Мел","仪式粉笔"])
# Split
add("66E7A87BDAC00C2C", title=["Split Glyph","Split Glyph","Glyphe de Division","Glifo de División","Glifo de Divisão","Глиф Расщепления","分裂符文"])
# Source Jar
add("4EFEAD14C5242D11", title=["Source Jar","Source Jar","Jarre de Source","Jarro de Origen","Jarro de Origem","Сосуд Источника","源能罐"])
add("0D0521B3B75C3035", title=["Source Jar","Source Jar","Jarre de Source","Jarro de Origen","Jarro de Origem","Сосуд Источника","源能罐"])
# Tier 1 / Tier 3 glyphs
add("5390681B92BC9EF2", title=["Tier 1 Glyphs","Tier 1 Glyphs","Glyphes Niveau 1","Glifos Nivel 1","Glifos Nível 1","Глифы 1 Уровня","一阶符文"])
add("45FC5370D2F3276C", title=["Tier 3 Glyphs","Tier 3 Glyphs","Glyphes Niveau 3","Glifos Nivel 3","Glifos Nível 3","Глифы 3 Уровня","三阶符文"])
# Threads / Mage spellbook upgrades
add("1582BFCB1B5840A8", title=["Apprentice Spellbook","Apprentice Spellbook","Grimoire d'Apprenti","Libro Aprendiz","Grimório de Aprendiz","Книга Ученика","学徒法术书"])
add("17F8F042B16B290B", title=["Apprentice Spellbook","Apprentice Spellbook","Grimoire d'Apprenti","Libro Aprendiz","Grimório de Aprendiz","Книга Ученика","学徒法术书"])
add("58ED00DB13CEFCF9", title=["Apprentice Spellbook","Apprentice Spellbook","Grimoire d'Apprenti","Libro Aprendiz","Grimório de Aprendiz","Книга Ученика","学徒法术书"])
# Magebloom seed
add("725D9E20292F86C7", title=["Magebloom Seeds","Magebloom Seeds","Graines de Magefleur","Semillas de Magoflor","Sementes de Magoflor","Семена Магоцвета","法师花种子"])
# Archwood
add("260DB8D11CDAF23F", title=["Archwood Logs","Archwood Logs","Bûches d'Arcanier","Troncos de Arcadia","Toras de Arquimadeira","Брёвна Архидрева","拱木原木"])
# Magic novice chapter intro
add("3B310D22AD8C3D51", title=["Novice Spellbook","Novice Spellbook","Grimoire de Novice","Libro de Novato","Grimório de Iniciante","Книга Новичка","新手法术书"])
add("7ED8D474F8FF1F7D", title=["Novice Spellbook","Novice Spellbook","Grimoire de Novice","Libro de Novato","Grimório de Iniciante","Книга Новичка","新手法术书"])
# Spell power amp
add("718D2BD5F451DCCD", title=["Amplify Glyph","Amplify Glyph","Glyphe d'Amplification","Glifo de Amplificar","Glifo de Amplificar","Глиф Усиления","增幅符文"])
# Pull
add("225C86D8B8C81511", title=["Pull Glyph","Pull Glyph","Glyphe de Traction","Glifo de Atracción","Glifo de Atrair","Глиф Притяжения","拉拽符文"])
# Slow
add("25C08950213F4C89", title=["Slow Glyph","Slow Glyph","Glyphe de Lenteur","Glifo de Lentitud","Glifo de Lentidão","Глиф Замедления","缓慢符文"])
# Interact
add("144474147B45D103", title=["Interact Glyph","Interact Glyph","Glyphe d'Interaction","Glifo de Interacción","Glifo de Interagir","Глиф Взаимодействия","交互符文"])
# Toss / throw
add("446B3AB4C4F61742", title=["Toss Glyph","Toss Glyph","Glyphe de Lancer","Glifo Lanzar","Glifo de Arremesso","Глиф Броска","抛掷符文"])
# Discount
add("7039E4225BD459A8", title=["Discount Jewelry","Discount Jewelry","Bijou de Réduction","Joya de Descuento","Joia de Desconto","Украшение Скидки","折扣宝石"])
# Starbuncle
add("6CD0327B0DF925CD", title=["Summon Starbuncle","Summon Starbuncle","Invocation de Starbuncle","Invocar Starbuncle","Invocar Starbuncle","Призыв Старбанкла","召唤星灵兽"])

# --- 2) CREATE / TECH titles + descriptions ---
# Andesite Alloy
add("35C8DAE073F80B6B",
    title=["Andesite Alloy","Andesite Alloy","Alliage d'Andésite","Aleación de Andesita","Liga de Andesita","Сплав Андезита","安山合金"],
    subtitle=["The base for all Create.","The base for all Create.","La base de tout Create.","La base de Create.","A base de tudo no Create.","Основа всего Create.","创生模组的基础。"])
# Andesite shaft
add("2158DBFC4D50371A",
    title=["Andesite Shaft","Andesite Shaft","Arbre en Andésite","Eje de Andesita","Eixo de Andesita","Андезитовый Вал","安山轴"],
    subtitle=["The basic mechanical connector.","The basic mechanical connector.","Le connecteur mécanique de base.","Conector mecánico básico.","Conector mecânico básico.","Базовый механический соединитель.","基础机械连接件。"])
# Stress gauge
add("5D49BAADE0ADCBDB",
    title=["Stress Gauge","Stress Gauge","Jauge de Stress","Indicador de Estrés","Medidor de Estresse","Манометр Нагрузки","应力计"],
    desc=["Lets you see the current stress and capacity of a kinetic network.","Lets you see the current stress and capacity of a kinetic network.","Affiche la contrainte et la capacité actuelle d'un réseau cinétique.","Muestra la tensión y capacidad actual de una red cinética.","Mostra a tensão e capacidade atual de uma rede cinética.","Показывает текущее напряжение и ёмкость кинетической сети.","显示动能网络当前的应力和容量。"])
# Engineer goggles
add("3EA8BB346A4104AE",
    title=["Engineer's Goggles","Engineer's Goggles","Lunettes d'Ingénieur","Gafas de Ingeniero","Óculos de Engenheiro","Очки Инженера","工程师护目镜"],
    desc=["Essential for any Create engineer. See stress impact and more info on blocks.","Essential for any Create engineer. See stress impact and more info on blocks.","Indispensables pour tout ingénieur Create. Voyez la contrainte et plus d'infos.","Esenciales para todo ingeniero Create. Ver el impacto de estrés y más info.","Essenciais para todo engenheiro Create. Veja o impacto do estresse e mais info.","Необходимы для инженера Create. Показывают нагрузку и инфо о блоках.","创生模组工程师必备。查看应力等方块信息。"])
# Hydraulic Press
add("2C3CD6663D38750A",
    title=["Mechanical Press","Mechanical Press","Presse Mécanique","Prensa Mecánica","Prensa Mecânica","Механический Пресс","机械压力机"],
    desc=["Like a real hydraulic press. Compresses items and crafts sheets.","Like a real hydraulic press. Compresses items and crafts sheets.","Comme une vraie presse hydraulique. Compresse les objets et fabrique des feuilles.","Como una prensa hidráulica real. Comprime objetos y fabrica láminas.","Como uma prensa hidráulica real. Comprime itens e cria chapas.","Как настоящий гидропресс. Сжимает предметы и куёт листы.","如真正的液压机。压缩物品并锻造金属片。"])
# Mechanical Mixer
add("798CADF6B8930572",
    title=["Mechanical Mixer","Mechanical Mixer","Mixeur Mécanique","Mezclador Mecánico","Misturador Mecânico","Механический Миксер","机械搅拌器"],
    desc=["Auto-crafts shapeless recipes and mixes potions. Needs at least 30 RPM.","Auto-crafts shapeless recipes and mixes potions. Needs at least 30 RPM.","Auto-fabrique les recettes informelles et mélange les potions. Min. 30 RPM.","Auto-fabrica recetas sin forma y mezcla pociones. Mín. 30 RPM.","Auto-fabrica receitas amorfas e mistura poções. Mín. 30 RPM.","Авто-крафтит бесформенные рецепты и смешивает зелья. Мин. 30 об/мин.","自动合成无序配方和混合药水。至少30 RPM。"])
add("307C4902B2D899BA",
    title=["Mechanical Mixer","Mechanical Mixer","Mixeur Mécanique","Mezclador Mecánico","Misturador Mecânico","Механический Миксер","机械搅拌器"],
    desc=["A machine that auto-crafts shapeless recipes and mixes potions. Min 30 RPM.","A machine that auto-crafts shapeless recipes and mixes potions. Min 30 RPM.","Une machine qui auto-fabrique les recettes informelles et mélange les potions. Min. 30 RPM.","Una máquina que auto-fabrica recetas sin forma y mezcla pociones. Mín. 30 RPM.","Máquina que auto-fabrica receitas amorfas e mistura poções. Mín. 30 RPM.","Машина для авто-крафта бесформенных рецептов. Мин. 30 об/мин.","可自动合成无序配方的机器。最少30 RPM。"])
# Stress Stabilization Multiblock (Capacity)
add("1429BBBA9658CD9D",
    title=["Stress Capacity Network","Stress Capacity Network","Réseau de Capacité","Red de Capacidad","Rede de Capacidade","Сеть Ёмкости","应力容量网络"],
    desc=["A multi-block structure storing large amounts of kinetic energy.","A multi-block structure storing large amounts of kinetic energy.","Une structure multi-bloc stockant de grandes quantités d'énergie cinétique.","Estructura multi-bloque que almacena gran cantidad de energía cinética.","Estrutura multi-bloco que armazena grande quantidade de energia cinética.","Многоблочная конструкция, хранящая много кинетической энергии.","存储大量动能的多方块结构。"])
# RPM fine tune
add("7088750D467E771E",
    title=["Adjustable Gearshift","Adjustable Gearshift","Boîte de Vitesse","Caja de Cambios","Caixa de Câmbio","Регулятор Передач","可调齿轮箱"],
    desc=["Allows fine-tuning of RPM via redstone signal strength.","Allows fine-tuning of RPM via redstone signal strength.","Permet d'ajuster finement les RPM via la force du signal redstone.","Permite afinar las RPM mediante la fuerza de la señal de redstone.","Permite ajustar finamente as RPM via força do sinal de redstone.","Тонкая настройка об/мин с помощью сигнала редстоуна.","通过红石信号强度精确调节 RPM。"])
# Filter inversion
add("129CF51A1AC6554C",
    title=["Rotation Speed Controller","Rotation Speed Controller","Régulateur de Vitesse","Regulador de Rotación","Regulador de Rotação","Регулятор Скорости","旋转控制器"],
    subtitle=["Reverses rotational direction.","Reverses rotational direction.","Inverse le sens de rotation.","Invierte la dirección de rotación.","Inverte a direção da rotação.","Меняет направление вращения.","反转旋转方向。"])
# Inversion gearshift
add("06653E21053ACDF6",
    title=["Latching Gearshift","Latching Gearshift","Engrenage Bistable","Engranaje Bistable","Engrenagem Biestável","Защёлкивающаяся Передача","双稳齿轮"],
    desc=["A redstone component toggled by signals on either side.","A redstone component toggled by signals on either side.","Composant redstone bascule selon les signaux des côtés opposés.","Componente redstone que alterna con señales de lados opuestos.","Componente redstone que alterna com sinais de lados opostos.","Редстоун-компонент, переключаемый сигналами с двух сторон.","由两侧红石信号切换的组件。"])
# Mech farms blocks
add("134E7417D5CCE12F",
    title=["Mechanical Harvesters","Mechanical Harvesters","Moissonneuses Mécaniques","Cosechadoras Mecánicas","Colheitadeiras Mecânicas","Механические Жатки","机械收割机"],
    desc=["Blocks that allow contraptions to harvest crops automatically.","Blocks that allow contraptions to harvest crops automatically.","Blocs permettant aux engins de récolter automatiquement.","Bloques que permiten a los artefactos cosechar automáticamente.","Blocos que permitem aos engenhos colher automaticamente.","Блоки, позволяющие контрапциям собирать урожай.","允许装置自动收获作物的方块。"])
add("3B925864D243F779",
    title=["Mechanical Harvesters","Mechanical Harvesters","Moissonneuses Mécaniques","Cosechadoras Mecánicas","Colheitadeiras Mecânicas","Механические Жатки","机械收割机"],
    desc=["Blocks that allow mechanisms to harvest crops.","Blocks that allow mechanisms to harvest crops.","Blocs permettant aux mécanismes de récolter les cultures.","Bloques que permiten a los mecanismos cosechar cultivos.","Blocos que permitem aos mecanismos colher.","Блоки, позволяющие механизмам собирать урожай.","允许机械装置收获作物的方块。"])
# Bearing
add("2BC564546A48616B",
    title=["Mechanical Bearing","Mechanical Bearing","Roulement Mécanique","Rodamiento Mecánico","Rolamento Mecânico","Механический Подшипник","机械轴承"],
    desc=["Allows contraptions to rotate around a point. Useful for farms.","Allows contraptions to rotate around a point. Useful for farms.","Permet aux engins de tourner autour d'un point. Pratique pour les fermes.","Permite que los artefactos giren alrededor de un punto. Útil para granjas.","Permite que engenhos girem em torno de um ponto. Útil para fazendas.","Позволяет контрапциям вращаться вокруг точки. Удобно для ферм.","让装置围绕一点旋转。适合农场。"])
# Gantry carriage
add("65A2AC554D856D93",
    title=["Gantry Carriage","Gantry Carriage","Chariot de Portique","Carro de Pórtico","Carro de Pórtico","Тележка Портала","龙门吊车架"],
    desc=["Allows contraptions to move across gantry shafts.","Allows contraptions to move across gantry shafts.","Permet aux engins de se déplacer le long des arbres-portique.","Permite a los artefactos moverse a lo largo de ejes pórtico.","Permite engenhos se moverem em eixos de pórtico.","Позволяет контрапциям перемещаться по портальным валам.","让装置沿龙门轴移动。"])
# Heavy steam wheel / big armored aircraft
add("63FF301B02B67929",
    title=["Heavy Skybus","Heavy Skybus","Forteresse Volante","Fortaleza Voladora","Fortaleza Voadora","Тяжёлый Воздушный Крейсер","重型空艇"],
    desc=["A slow but heavily armed flying fortress.","A slow but heavily armed flying fortress.","Une forteresse volante lente mais lourdement armée.","Una fortaleza voladora lenta pero muy armada.","Uma fortaleza voadora lenta mas pesadamente armada.","Медленная, но тяжело вооружённая летающая крепость.","缓慢但重装的空中堡垒。"])
# Funnel
add("170CD73C3833FC8D",
    title=["Funnel","Funnel","Entonnoir","Embudo","Funil","Воронка","漏斗"],
    desc=["Input/output one item at a time to inventories.","Input/output one item at a time to inventories.","Entre/sort un objet à la fois dans/des inventaires.","Entrada/salida de un objeto a la vez en inventarios.","Entrada/saída de um item por vez em inventários.","Подача/выгрузка по одному предмету в инвентари.","一次一个物品输入/输出库存。"])
# Smart chute
add("5CE5D30F408423D0",
    title=["Smart Chute","Smart Chute","Goulotte Intelligente","Conducto Inteligente","Conduto Inteligente","Умный Жёлоб","智能滑槽"],
    desc=["An advanced chute with filtering and higher stack sizes.","An advanced chute with filtering and higher stack sizes.","Une goulotte avancée avec filtrage et grandes piles.","Conducto avanzado con filtrado y mayor tamaño de pila.","Conduto avançado com filtragem e maior tamanho de pilha.","Продвинутый жёлоб с фильтрацией и большими стаками.","具有过滤功能和更大堆叠的高级滑槽。"])
# Chute
add("1CE6DB5F873483AF",
    title=["Chute","Chute","Goulotte","Conducto","Conduto","Жёлоб","滑槽"],
    desc=["Transfers items vertically between inventories.","Transfers items vertically between inventories.","Transfère les objets verticalement entre inventaires.","Transfiere objetos verticalmente entre inventarios.","Transfere itens verticalmente entre inventários.","Передаёт предметы вертикально между инвентарями.","在库存间垂直传输物品。"])
# Encased fan haunt (soulfire)
add("00DFC7824C3750FB",
    title=["Soulfire","Soulfire","Feu d'Âme","Fuego del Alma","Fogo da Alma","Адский Огонь","灵魂之火"],
    desc=["Placed in front of an Encased Fan to haunt items (e.g. sand to soul sand).","Placed in front of an Encased Fan to haunt items (e.g. sand to soul sand).","Devant un Ventilateur Encaissé pour hanter les objets (sable → sable des âmes).","Frente a un Ventilador Encajado para encantar objetos (arena → arena de almas).","Em frente ao Ventilador Encaixado para assombrar itens (areia → areia das almas).","Перед Закрытым Вентилятором, чтобы обращать предметы (песок → песок душ).","置于风扇前使物品灵魂化（沙→灵魂沙）。"])
# Encased fan blast (lava)
add("49EE6F88CD93352E",
    title=["Lava Blast","Lava Blast","Souffle de Lave","Soplo de Lava","Sopro de Lava","Огненный Дувной Поток","熔岩气流"],
    desc=["Placed in front of an Encased Fan to blast items.","Placed in front of an Encased Fan to blast items.","Devant un Ventilateur Encaissé pour fondre les objets.","Frente a un Ventilador Encajado para fundir objetos.","Em frente ao Ventilador Encaixado para fundir itens.","Перед Закрытым Вентилятором, чтобы плавить предметы.","置于风扇前熔炼物品。"])
# Encased fan smoke
add("28FCBC21C193E676",
    title=["Smoke Source","Smoke Source","Source de Fumée","Fuente de Humo","Fonte de Fumaça","Источник Дыма","烟雾源"],
    desc=["Placed in front of an Encased Fan to smoke items.","Placed in front of an Encased Fan to smoke items.","Devant un Ventilateur Encaissé pour fumer les objets.","Frente a un Ventilador Encajado para ahumar objetos.","Em frente ao Ventilador Encaixado para defumar itens.","Перед Закрытым Вентилятором, чтобы коптить предметы.","置于风扇前烟熏物品。"])
# Fluid pipe / tank etc.
add("143FDEF9826191F8",
    title=["Fluid Tank","Fluid Tank","Cuve à Fluide","Tanque de Fluido","Tanque de Fluido","Резервуар Жидкости","流体罐"],
    subtitle=["Stores fluids for presses, mixers, etc.","Stores fluids for presses, mixers, etc.","Stocke des fluides pour presses, mixeurs, etc.","Almacena fluidos para prensas, mezcladores, etc.","Armazena fluidos para prensas, misturadores, etc.","Хранит жидкости для прессов и миксеров.","为压力机、搅拌器等储存液体。"])
add("16CB62F26E67C6F9",
    title=["Spout","Spout","Bec Verseur","Pico Vertedor","Bico Vertedor","Носик","注液器"],
    desc=["Used for filling items with fluids and crafting with fluids.","Used for filling items with fluids and crafting with fluids.","Sert à remplir des objets avec des fluides ou à les transformer.","Para llenar objetos con fluidos y fabricar con fluidos.","Para encher itens com fluidos e fabricar com fluidos.","Заполняет предметы жидкостями для крафта.","用于给物品填充液体和液体合成。"])
# Andesite super glue use
add("4159B902CC6D38E0", desc=["Glues blocks together so they move as a contraption.","Glues blocks together so they move as a contraption.","Colle les blocs ensemble pour qu'ils bougent comme un engin.","Pega bloques para que se muevan como un artefacto.","Cola blocos para se moverem como um engenho.","Склеивает блоки, чтобы они двигались как контрапция.","将方块粘在一起作为装置移动。"])
# Andesite casing (Stage 7)
add("2E352BBD58FCC997", desc=["Decorative variant used for crafting and styling Stage 7 builds.","Decorative variant used for crafting and styling Stage 7 builds.","Variante décorative pour la phase 7.","Variante decorativa para construcciones fase 7.","Variante decorativa para construções da fase 7.","Декоративный вариант для построек этапа 7.","用于第7阶段构建的装饰变体。"])
# Water wheel
add("54D05D973D564069",
    title=["Water Wheel","Water Wheel","Roue Hydraulique","Rueda de Agua","Roda d'Água","Водяное Колесо","水车"],
    desc=["Generates rotational power from flowing water. Recolorable with wood planks.","Generates rotational power from flowing water. Recolorable with wood planks.","Génère de l'énergie rotationnelle à partir d'eau qui coule. Recolorable.","Genera energía rotacional a partir de agua corriente. Recoloreable.","Gera energia rotacional a partir de água corrente. Recolorível.","Производит вращение от текущей воды. Перекрашиваемое.","利用流水产生旋转动力。可重新上色。"])
# Diesel engine to rotational
add("737A99A32E3CC9CB",
    title=["Diesel Generator","Diesel Generator","Générateur Diesel","Generador Diésel","Gerador a Diesel","Дизельный Генератор","柴油发电机"],
    subtitle=["Converts fuel into rotational power.","Converts fuel into rotational power.","Convertit le carburant en énergie rotationnelle.","Convierte combustible en energía rotacional.","Converte combustível em energia rotacional.","Превращает топливо в вращение.","将燃料转化为旋转动力。"])
# Smokestack / blaze on CO2
add("1B9E6F09E7AB8C87",
    title=["Carbon Blaze Burner","Carbon Blaze Burner","Brûleur Carbone","Quemador de Carbono","Queimador de Carbono","Углеродная Горелка","碳烈焰熔炉"],
    subtitle=["Acts as a Blaze Burner. Vent the CO2.","Acts as a Blaze Burner. Vent the CO2.","Sert de Brûleur. Évacuez le CO2.","Actúa como un Quemador. Ventila el CO2.","Atua como Queimador. Ventile o CO2.","Действует как Горелка. Удаляйте CO2.","作为烈焰熔炉使用。需排放CO2。"])
# Combustion engine
add("2B30B5137906EE93",
    title=["Combustion Generator","Combustion Generator","Générateur à Combustion","Generador de Combustión","Gerador de Combustão","Генератор Сгорания","内燃发电机"],
    subtitle=["Min. 71 RPM. May explode! Be careful.","Min. 71 RPM. May explode! Be careful.","Min. 71 RPM. Risque d'explosion ! Attention.","Mín. 71 RPM. ¡Puede explotar! Cuidado.","Mín. 71 RPM. Pode explodir! Cuidado.","Мин. 71 об/мин. Может взорваться!","最少71 RPM。可能爆炸！"])
# Belt / Conveyor
add("4A670C64F73CA0F6",
    title=["Mechanical Belt","Mechanical Belt","Tapis Mécanique","Cinta Mecánica","Esteira Mecânica","Механическая Лента","机械传送带"],
    subtitle=["Transports items between points.","Transports items between points.","Transporte les objets entre deux points.","Transporta objetos entre puntos.","Transporta itens entre pontos.","Перевозит предметы между точками.","在各点间运输物品。"])
# Belt for mech mover
add("256BD25A3D3E3324",
    title=["Mechanical Belt","Mechanical Belt","Tapis Mécanique","Cinta Mecánica","Esteira Mecânica","Механическая Лента","机械传送带"],
    subtitle=["Used in contraptions to move items between inventories.","Used in contraptions to move items between inventories.","Utilisé dans les engins pour transporter des objets entre inventaires.","Usado en artefactos para mover objetos entre inventarios.","Usado em engenhos para mover itens entre inventários.","Используется в контрапциях для перемещения предметов.","在装置中在库存间移动物品。"])
# Linear actuator
add("2E3CD1685DAE2383",
    title=["Cart Rail Adapter","Cart Rail Adapter","Adaptateur de Rail","Adaptador de Riel","Adaptador de Trilho","Адаптер Рельсов","矿车导轨适配器"],
    desc=["Allows contraptions to traverse rails like minecarts.","Allows contraptions to traverse rails like minecarts.","Permet aux engins de parcourir les rails comme des wagonnets.","Permite a los artefactos circular por raíles como vagonetas.","Permite engenhos percorrerem trilhos como minecarts.","Позволяет контрапциям ездить по рельсам как вагонетки.","让装置像矿车一样在轨道上移动。"])
# Train conductor
add("063D47D4F61457BC",
    title=["Train Schedule","Train Schedule","Horaire de Train","Horario de Tren","Horário de Trem","Расписание Поезда","列车时刻表"],
    desc=["Programs train routes so mobs or Blaze Burners can drive them.","Programs train routes so mobs or Blaze Burners can drive them.","Programme les itinéraires pour que des mobs ou Brûleurs conduisent.","Programa rutas de tren para que mobs o Quemadores conduzcan.","Programa rotas para que mobs ou Queimadores conduzam.","Программирует маршруты для мобов или Горелок.","让生物或熔炉驾驶列车的路线规划。"])
# Minecart coupling
add("0FCB25BA5EB5E745",
    title=["Minecart Coupling","Minecart Coupling","Attelage de Wagonnet","Acoplador Vagoneta","Acoplador Minecart","Сцепка Вагонеток","矿车连接器"],
    desc=["Chains minecarts together, causing them to move as a group.","Chains minecarts together, causing them to move as a group.","Relie les wagonnets pour qu'ils bougent en groupe.","Encadena vagonetas para que se muevan en grupo.","Encadeia minecarts para se moverem em grupo.","Соединяет вагонетки в одну группу.","将矿车连成一组移动。"])
# Bulk haunt / smoke handling
# Sequenced Gearshift (rotation amount)
add("16CD1CC9F70A91AF",
    title=["Sequenced Gearshift","Sequenced Gearshift","Engrenage Séquencé","Engranaje Secuencial","Engrenagem Sequencial","Программируемая Передача","顺控齿轮"],
    desc=["Halves or doubles the rotation speed of connected chaindrives via redstone.","Halves or doubles the rotation speed of connected chaindrives via redstone.","Divise ou double la vitesse de rotation des chaînes via redstone.","Reduce a la mitad o duplica la velocidad de cadenas via redstone.","Reduz pela metade ou duplica a velocidade via redstone.","Удваивает или уменьшает скорость через редстоун.","通过红石将链速度减半或加倍。"])
# Speedometer FR
add("5606BB2A4AF29D36", desc=["Displays the current rotational speed in RPM.","Displays the current rotational speed in RPM.","Affiche la vitesse de rotation actuelle en RPM.","Muestra la velocidad rotacional actual en RPM.","Mostra a velocidade rotacional atual em RPM.","Показывает текущие об/мин.","显示当前转速 (RPM)。"])
# Clutch description (controlled by redstone)
add("312DB48A6C6601F2",
    title=["Clutch","Clutch","Embrayage","Embrague","Embreagem","Сцепление","离合器"],
    desc=["Stops rotational force passing through when powered by redstone.","Stops rotational force passing through when powered by redstone.","Bloque la force rotationnelle quand alimenté par redstone.","Detiene la fuerza rotacional cuando recibe redstone.","Para a força rotacional quando recebe redstone.","Останавливает вращение при сигнале редстоуна.","通电时阻止旋转传递。"])
# Stockpile switch
add("4E0503134BFF19F0",
    title=["Stockpile Switch","Stockpile Switch","Détecteur de Stock","Interruptor de Stock","Detector de Estoque","Датчик Запасов","库存开关"],
    desc=["A block that monitors fill levels of inventories and tanks.","A block that monitors fill levels of inventories and tanks.","Surveille le niveau de remplissage des inventaires et cuves.","Monitorea los niveles de inventarios y tanques.","Monitora os níveis de inventários e tanques.","Отслеживает уровень заполнения инвентарей и резервуаров.","监控库存和液罐的填充水平。"])
# Content Observer
# Fluid network related: 30C1D45E7545FA6C
add("30C1D45E7545FA6C",
    title=["Smart Fluid Pipe","Smart Fluid Pipe","Tuyau Intelligent","Tubería Inteligente","Tubo Inteligente","Умная Жидкостная Труба","智能流体管道"],
    desc=["Connect with a heat source to spread heat evenly across pipes unless pumped.","Connect with a heat source to spread heat evenly across pipes unless pumped.","Reliée à une source de chaleur, répartit la chaleur dans les tuyaux.","Conéctala a una fuente de calor para repartir el calor entre tuberías.","Conecte a uma fonte de calor para distribuir o calor.","Соединение с источником тепла равномерно греет трубы.","连接热源时在管道中均匀传热。"])
# Bulk smoking / fluid valve
add("34C2397EB064E79F",
    title=["Hose Pulley","Hose Pulley","Poulie à Tuyau","Polea de Manguera","Polia de Mangueira","Шланговый Шкив","水管滑轮"],
    desc=["Used to place or extract large bodies of liquid.","Used to place or extract large bodies of liquid.","Utilisé pour placer ou aspirer de grandes étendues de liquide.","Usada para colocar o extraer grandes cantidades de líquido.","Usada para colocar ou extrair grandes quantidades de líquido.","Ставит или собирает большие объёмы жидкости.","用于放置或抽取大量液体。"])
# Brass tunnel / weighted ejector
add("144823B916D67A5A",
    title=["Mechanical Pump Switch","Mechanical Pump Switch","Vanne Mécanique","Válvula Mecánica","Válvula Mecânica","Механический Клапан","机械阀门"],
    desc=["Lets you turn off parts of contraptions while they're formed.","Lets you turn off parts of contraptions while they're formed.","Permet de désactiver des parties d'engins en cours d'utilisation.","Permite apagar partes de artefactos mientras están formados.","Permite desligar partes de engenhos enquanto estão formados.","Отключает части контрапции, пока она собрана.","可在装置成型时关闭部分组件。"])
# Encased Fan / kinetic
add("145F388D56FB4A5F", desc=["Blocks that fell trees or allow contraptions to do so, plus stripping recipes.","Blocks that fell trees or allow contraptions to do so, plus stripping recipes.","Blocs qui abattent les arbres ou permettent aux engins de le faire.","Bloques que talan árboles o permiten que los artefactos lo hagan.","Blocos que derrubam árvores ou permitem engenhos fazê-lo.","Блоки, рубящие деревья или дающие контрапциям рубить.","可砍树或让装置砍树的方块。"])
# Wireless redstone link
add("7F5E2D38C40E93F7", desc=["Allows transferring redstone signals wirelessly within a certain range.","Allows transferring redstone signals wirelessly within a certain range.","Transfère des signaux redstone sans fil sur une certaine distance.","Transfiere señales de redstone inalámbricamente.","Transfere sinais de redstone sem fio.","Передаёт сигнал редстоуна по беспроводу в радиусе.","在一定范围内无线传输红石信号。"])
# Wrench
add("09524E957A2D47D9", desc=["Used to modify and rotate Create blocks.","Used to modify and rotate Create blocks.","Sert à modifier et orienter les blocs Create.","Para modificar y rotar bloques de Create.","Para modificar e girar blocos do Create.","Меняет и вращает блоки Create.","用于修改和旋转Create方块。"])
# Cogwheels
add("59DA39F9F3850E59", desc=["Cogwheels increase rotation speed or extend contraptions.","Cogwheels increase rotation speed or extend contraptions.","Les engrenages augmentent la vitesse ou prolongent les engins.","Engranajes aumentan la velocidad o extienden artefactos.","Engrenagens aumentam velocidade ou estendem engenhos.","Шестерни ускоряют вращение или удлиняют контрапции.","齿轮可加速旋转或延展装置。"])
# Hand crank
add("0945E885A92D06B7", desc=["Generates rotation by hand. Build muscle!","Generates rotation by hand. Build muscle!","Génère de la rotation à la main. Musclez-vous !","Genera rotación con la mano. ¡Fortalécete!","Gera rotação na mão. Ganhe músculo!","Производит вращение вручную. Качайте мышцы!","用手生成旋转动力。"])
# Schematic Table
add("1EC4FD8DDA264505", desc=["Loads and prints schematics for building.","Loads and prints schematics for building.","Charge et imprime les schémas de construction.","Carga e imprime esquemas para construir.","Carrega e imprime esquemas para construir.","Загружает и печатает схемы для построек.","加载并打印建筑蓝图。"])

# --- 3) STAGE-X DESC PATTERN (Create progression) ---
STAGES = {
    "STAGE 0": ("Stage 0 progression: starter kit.","Stage 0 progression: starter kit.","Progression Phase 0 : kit de départ.","Progresión Fase 0: kit de inicio.","Progressão Fase 0: kit inicial.","Прогрессия Этап 0: стартовый набор.","阶段0进度：起步套装。"),
    "STAGE 1": ("Stage 1: primary andesite mechanics.","Stage 1: primary andesite mechanics.","Phase 1 : mécanique andésite.","Fase 1: mecánica primaria de andesita.","Fase 1: mecânica primária de andesita.","Этап 1: основная механика андезита.","阶段1：基础安山机械。"),
    "STAGE 2": ("Stage 2: resource processing.","Stage 2: resource processing.","Phase 2 : traitement des ressources.","Fase 2: procesamiento de recursos.","Fase 2: processamento de recursos.","Этап 2: обработка ресурсов.","阶段2：资源处理。"),
    "STAGE 3": ("Stage 3: hydraulics (copper).","Stage 3: hydraulics (copper).","Phase 3 : hydraulique (cuivre).","Fase 3: hidráulica (cobre).","Fase 3: hidráulica (cobre).","Этап 3: гидравлика (медь).","阶段3：水力（铜）。"),
    "STAGE 4": ("Stage 4: precision (brass).","Stage 4: precision (brass).","Phase 4 : précision (laiton).","Fase 4: precisión (latón).","Fase 4: precisão (latão).","Этап 4: точность (латунь).","阶段4：精密（黄铜）。"),
    "STAGE 5": ("Stage 5: smart logistics.","Stage 5: smart logistics.","Phase 5 : logistique intelligente.","Fase 5: logística inteligente.","Fase 5: logística inteligente.","Этап 5: умная логистика.","阶段5：智能物流。"),
    "STAGE 6": ("Stage 6: trains & steam.","Stage 6: trains & steam.","Phase 6 : trains & vapeur.","Fase 6: trenes y vapor.","Fase 6: trens & vapor.","Этап 6: поезда и пар.","阶段6：列车与蒸汽。"),
    "STAGE 7": ("Stage 7: decor & construction (style).","Stage 7: decor & construction (style).","Phase 7 : déco & construction (style).","Fase 7: decoración y construcción.","Fase 7: decoração e construção.","Этап 7: декор и строительство.","阶段7：装饰与建造。"),
    "STAGE 8": ("Stage 8: equipment & special addons.","Stage 8: equipment & special addons.","Phase 8 : équipement & addons spéciaux.","Fase 8: equipo y addons especiales.","Fase 8: equipamentos e addons especiais.","Этап 8: снаряжение и спец. аддоны.","阶段8：装备与特殊附加组件。"),
    "STAGE 9": ("Stage 9: redstone components.","Stage 9: redstone components.","Phase 9 : composants redstone.","Fase 9: componentes de redstone.","Fase 9: componentes de redstone.","Этап 9: компоненты редстоуна.","阶段9：红石组件。"),
}

STAGE_DESC_IDS = {
    "1EC6CA5B58A2D540":"STAGE 5","6778A579D1DD4714":"STAGE 9","4C5BC8D9C4594444":"STAGE 6",
    "6A7CB0F3C7008081":"STAGE 7","2ABEA10A3E4DDA01":"STAGE 7","2BE27D81C77FA3D4":"STAGE 7",
    "1DD2029CA9EBAF7D":"STAGE 0","53E1F408BD3A75C2":"STAGE 0","5B51C5F19000416A":"STAGE 8",
    "1D63DA5F72C9489B":"STAGE 1","49EFAF906BC8402F":"STAGE 3","61967601821ADCD0":"STAGE 7",
    "126C57E1B7F48562":"STAGE 4","4FE787BC222C4D46":"STAGE 8","2624DBE232884561":"STAGE 1",
    "0DF335139E426778":"STAGE 8","1B8CDAFE0F355EF9":"STAGE 2","6D6FC9A96F6D47D0":"STAGE 8",
    "2F7C1609A78449E7":"STAGE 8","02395E401CC84E1D":"STAGE 7","40BC79E977D34D64":"STAGE 9",
    "2FCE8112453B4752":"STAGE 5","17A6FB4EC3994678":"STAGE 7","78993F67494225BA":"STAGE 2",
    "20929C815FAE4E42":"STAGE 1","5A101048011A4648":"STAGE 1","5A28A5797BAD468A":"STAGE 4",
    "78F8A77CCAC09A38":"STAGE 4","5AE82938FA044FE4":"STAGE 3","2F40DF4899014EF0":"STAGE 8",
    "1CE748D82E64D261":"STAGE 8","0C981CF1F57B4121":"STAGE 8","5995A101220947DE":"STAGE 7",
    "533C1747651ABDEC":"STAGE 7","51F371AAF46416AA":"STAGE 5","2D193511A5F5A82E":"STAGE 3",
    "3BD4062256CA49F4":"STAGE 5","555172382AF5148D":"STAGE 7","496F37DD49FF400B":"STAGE 6",
    "5D3DA503D8E4456E":"STAGE 9","44D53BA52AAE0B89":"STAGE 1","78039771CED04B83":"STAGE 2",
    "325849031C7BF8D8":"STAGE 0","7CC5DC6A0EB64D0C":"STAGE 0","7D4A2270647847D0":"STAGE 3",
    "1ABB86E331EC423E":"STAGE 3","50E525E8F48F8472":"STAGE 8","4924F9D0B45844AB":"STAGE 1",
    "213C4F0E01BEA535":"STAGE 1","092F956915174336":"STAGE 4","2563D724679F4C57":"STAGE 2",
    "70D8B3F19F4650F3":"STAGE 3","0727314604121363":"STAGE 5","2F87CD249BDA461F":"STAGE 5",
}

for qid, stage in STAGE_DESC_IDS.items():
    QUESTS.setdefault(qid, {})["desc"] = list(STAGES[stage])

# --- 4) Other specific quests ---
# Crank/dough/Bakery
add("672E780AF6F5C4C0",
    subtitle=["Flour, dough, and pie crust. The foundation of all desserts.","Flour, dough, and pie crust. The foundation of all desserts.","Farine, pâte et croûte. La base de tous les desserts.","Harina, masa y costra. La base de todos los postres.","Farinha, massa e crosta. A base de todas as sobremesas.","Мука, тесто и корж. Основа всех десертов.","面粉、面团和派皮。所有甜点的基础。"])
# Seed master
add("0724B9C43D7EDE61",
    subtitle=["Transform your wild finds into seeds.","Transform your wild finds into seeds.","Transformez vos trouvailles sauvages en graines.","Convierte tus hallazgos salvajes en semillas.","Transforme suas descobertas selvagens em sementes.","Превратите ваши находки в семена.","将野生发现转化为种子。"])
add("0000000000000500",
    subtitle=["Transform your wild finds into seeds.","Transform your wild finds into seeds.","Transformez vos trouvailles sauvages en graines.","Convierte tus hallazgos salvajes en semillas.","Transforme suas descobertas selvagens em sementes.","Превратите ваши находки в семена.","将野生发现转化为种子。"])
# Banquet desserts
add("0000000000001300",
    subtitle=["Banquet dishes placed on the ground like cakes.","Banquet dishes placed on the ground like cakes.","Plats festifs posés au sol comme un gâteau.","Platos festivos colocados en el suelo como pasteles.","Pratos de banquete colocados no chão como bolos.","Праздничные блюда, как торты.","像蛋糕一样放在地上的盛宴菜肴。"])
# Harvest box
add("0000000000000064",
    subtitle=["Store your surplus crates. 9 in, 1 block out.","Store your surplus crates. 9 in, 1 block out.","Stockez votre surplus en caisses. 9 entrent, 1 bloc sort.","Almacena tu excedente. 9 entran, 1 bloque sale.","Armazene seu excedente. 9 entram, 1 bloco sai.","Сохраняйте излишки. 9 в, 1 блок выходит.","储存剩余物资。9进，1块出。"])
# Compost
add("0000000000000032",
    subtitle=["Mix dirt, straw, and waste to make compost.","Mix dirt, straw, and waste to make compost.","Mélangez terre, paille et déchets pour faire du compost.","Mezcla tierra, paja y residuos para hacer compost.","Misture terra, palha e resíduos para fazer composto.","Смешайте землю, солому и отходы для компоста.","混合土、稻草和废物制堆肥。"])
# Forager trail
add("0000000000000021",
    subtitle=["Crops don't just appear. Find their wild ancestors.","Crops don't just appear. Find their wild ancestors.","Les cultures n'apparaissent pas. Trouvez leurs ancêtres sauvages.","Los cultivos no aparecen solos. Encuentra sus ancestros silvestres.","Plantações não aparecem do nada. Encontre seus ancestrais.","Растения не появляются сами. Найдите дикие прообразы.","作物不会凭空出现，寻找其野生祖先。"])
# Mech arm
add("0000000000003110",
    subtitle=["Picks up items from A and places them at B.","Picks up items from A and places them at B.","Récupère les objets en A pour les placer en B.","Recoge objetos en A y los coloca en B.","Pega itens em A e coloca em B.","Берёт предметы из A и кладёт в B.","从A处取物放到B处。"])
# Mech farming
add("0000000000009250",
    subtitle=["Automate your farms with these tools.","Automate your farms with these tools.","Automatisez vos fermes avec ces outils.","Automatiza tus granjas con estas herramientas.","Automatize suas fazendas com estas ferramentas.","Автоматизируйте свои фермы.","用这些工具自动化你的农场。"])
# Mech pistons
add("0000000000009500",
    subtitle=["Tools to move structures around.","Tools to move structures around.","Outils pour déplacer des structures.","Herramientas para mover estructuras.","Ferramentas para mover estruturas.","Инструменты для перемещения построек.","用于移动结构的工具。"])
# Linear movement
add("0000000000009510",
    subtitle=["Linear movement & lifting systems.","Linear movement & lifting systems.","Mouvement linéaire et levage.","Movimiento lineal y elevación.","Movimento linear e elevação.","Линейное движение и подъём.","直线运动与升降系统。"])
# Cutting board
add("59BE873078D5A1E9",
    subtitle=["Place items on it and right-click with a knife.","Place items on it and right-click with a knife.","Placez les objets et faites clic-droit avec un couteau.","Coloca objetos y haz clic derecho con un cuchillo.","Coloque itens e clique direito com a faca.","Положите предметы и нажмите ПКМ с ножом.","放置物品并右键使用刀子。"])
# Bake speculaas
add("282C3F04D7E7C4F3",
    subtitle=["Bake your first batch of cookies!","Bake your first batch of cookies!","Cuisez votre premier biscuit speculaas !","¡Hornea tu primera galleta speculaas!","Asse seu primeiro biscoito speculaas!","Испеките первое печенье!","烤你的第一批斯派库拉斯饼干！"],
    desc=["Use the oven and dough to bake cookies.","Use the oven and dough to bake cookies.","Utilisez le four et la pâte pour cuire des biscuits.","Usa el horno y la masa para hornear galletas.","Use o forno e a massa para assar biscoitos.","Используйте печь и тесто для печенья.","用烤箱和面团烤饼干。"])
# Knife - sharp start
add("21814F0D828365CE",
    subtitle=["Knives harvest straw and process food.","Knives harvest straw and process food.","Les couteaux récoltent paille et préparent la nourriture.","Cuchillos cosechan paja y procesan comida.","Facas colhem palha e processam comida.","Ножи собирают солому и обрабатывают еду.","刀子用于收割稻草和处理食物。"])
add("72A51B10AD8FCAA7",
    subtitle=["Your primary tool for the kitchen.","Your primary tool for the kitchen.","Votre outil principal en cuisine.","Tu herramienta principal en cocina.","Sua ferramenta principal na cozinha.","Ваш главный инструмент.","你厨房中的主要工具。"])
# Fire in kitchen
add("05A3A9F6A969EAC8",
    subtitle=["Stove, Cooking Pot and Skillet basics.","Stove, Cooking Pot and Skillet basics.","Cuisinière, Marmite et Poêle, les essentiels.","Estufa, Olla y Sartén, lo esencial.","Fogão, Panela e Frigideira: o essencial.","Печь, Котёл и Сковорода: основа.","炉灶、锅与煎锅基础。"])
# Farmer utilities
add("7AD4856057105C86",
    subtitle=["Rope to climb, net to catch falls.","Rope to climb, net to catch falls.","Corde pour grimper, filet pour amortir.","Cuerda para trepar, red para caídas.","Corda para escalar, rede para quedas.","Верёвка для лазания, сеть от падений.","攀登绳与防摔网。"])
# Master of Arcana
add("24DB3B65004B2623",
    subtitle=["Collect all glyphs to master Ars Nouveau.","Collect all glyphs to master Ars Nouveau.","Collectez tous les glyphes pour maîtriser Ars Nouveau.","Recoge todos los glifos para dominar Ars Nouveau.","Colete todos os glifos para dominar Ars Nouveau.","Соберите все глифы для мастерства Ars Nouveau.","收集所有符文精通Ars Nouveau。"])
# Premier sort
add("50C3F1754B8446BA",
    subtitle=["Use the Scribe's Table to create spells.","Use the Scribe's Table to create spells.","Utilisez la Table du Scribe pour créer des sorts.","Usa la Mesa del Escriba para crear hechizos.","Use a Mesa do Escriba para criar feitiços.","Используйте Стол Писаря для заклинаний.","用抄录工作台创建法术。"])
# Smarter Basket
add("75BA8D3D6C0B9D1C", desc=["Now interacts directly with Belts and Mechanical Arms.","Now interacts directly with Belts and Mechanical Arms.","Interagit désormais directement avec les Tapis et Bras Mécaniques.","Ahora interactúa directamente con Cintas y Brazos Mecánicos.","Agora interage diretamente com Esteiras e Braços.","Теперь работает с лентами и манипуляторами.","现在可与传送带和机械臂直接交互。"])
# Train tracks
add("48E5D56C47DF6642", desc=["Lay these so your trains have somewhere to run.","Lay these so your trains have somewhere to run.","Posez-les pour que vos trains puissent rouler.","Colócalas para que tus trenes puedan circular.","Coloque-as para que seus trens possam andar.","Уложите их, чтобы поезда могли ездить.","铺设它们让你的列车有路可走。"])
# Bakery / Dough
# Magic chapter intro
# Nether call (subtitle)
add("8D1D960FCFF06FBF",
    subtitle=["Face enhanced mobs in fiery depths.","Face enhanced mobs in fiery depths.","Affrontez des mobs améliorés dans les profondeurs ardentes.","Enfréntate a mobs mejorados en las profundidades ardientes.","Enfrente mobs aprimorados nas profundezas ardentes.","Бросьте вызов улучшенным мобам в адских глубинах.","面对火热深渊中强化的怪物。"])
add("7B93433AFC09E0AD",
    subtitle=["Face enhanced mobs in fiery depths.","Face enhanced mobs in fiery depths.","Affrontez des mobs améliorés dans les profondeurs ardentes.","Enfréntate a mobs mejorados en las profundidades ardientes.","Enfrente mobs aprimorados nas profundezas ardentes.","Бросьте вызов улучшенным мобам в адских глубинах.","面对火热深渊中强化的怪物。"])
# Mekanism chapter subtitle
add("5B7691798717BA45",
    subtitle=["Master ore quintupling and nuclear energy.","Master ore quintupling and nuclear energy.","Maîtrisez le quintuplement des minerais et le nucléaire.","Domina la quintuplicación de minerales y energía nuclear.","Domine quintuplicação de minérios e energia nuclear.","Освойте пятикратную переработку и ядерную энергию.","掌握矿物五倍化与核能。"])
# Mekanism reactor
add("7E2D119C6F13A0B8",
    subtitle=["Build a thermonuclear fusion reactor.","Build a thermonuclear fusion reactor.","Construisez un réacteur à fusion thermonucléaire.","Construye un reactor de fusión termonuclear.","Construa um reator de fusão termonuclear.","Постройте термоядерный реактор.","建造热核聚变反应堆。"])
# Twilight Forest
add("6943EC451A810470",
    subtitle=["Defeat Naga, Lich King and legendary bosses.","Defeat Naga, Lich King and legendary bosses.","Vainquez le Naga, le Roi-Liche et plus.","Derrota a Naga, Rey Lich y jefes legendarios.","Derrote Naga, Rei Lich e chefes lendários.","Победите Нагу, Король-Лича и легендарных боссов.","击败娜迦、巫妖王等传奇Boss。"])
# Endgame
add("AF91631B5B6F9E7D",
    subtitle=["Face the ultimate challenges.","Face the ultimate challenges.","Affrontez les défis ultimes.","Enfrenta los desafíos finales.","Enfrente os desafios finais.","Встретьте окончательные испытания.","面对终极挑战。"])
# Ancient fortress
add("218176856FE03570",
    subtitle=["Find a Nether Fortress.","Find a Nether Fortress.","Trouvez une forteresse du Nether.","Encuentra una Fortaleza del Nether.","Encontre uma Fortaleza do Nether.","Найдите Адскую крепость.","找到一座下界要塞。"])
# Spooky scary
add("0013A1535FD46C0D",
    subtitle=["Obtain a Wither Skeleton Skull.","Obtain a Wither Skeleton Skull.","Obtenez un Crâne de Wither Squelette.","Consigue un Cráneo de Esqueleto Wither.","Obtenha um Crânio de Esqueleto Wither.","Получите череп иссушённого скелета.","获得凋灵骷髅头。"])
# Inscriber presses
add("7981B799E989BC33",
    subtitle=["Break the Mysterious Cube at a meteor's centre.","Break the Mysterious Cube at a meteor's centre.","Brisez le Cube Mystérieux au centre du météore.","Rompe el Cubo Misterioso del meteorito.","Quebre o Cubo Misterioso do meteoro.","Разбейте Загадочный Куб в центре метеорита.","破坏陨石中心的神秘方块。"])
# Spaceship
add("15E9F4AD4BA672FB",
    subtitle=["Summon a stationary spaceship above your base.","Summon a stationary spaceship above your base.","Invoquez un vaisseau stationnaire au-dessus de votre base.","Invoca una nave estacionaria sobre tu base.","Invoque uma nave estacionária sobre sua base.","Призовите неподвижный корабль над базой.","在基地上方召唤静止的飞船。"])
# Fluid Tank
add("2ECB37A4ACDED6B2",
    subtitle=["Store liquids for later use.","Store liquids for later use.","Stockez des liquides pour plus tard.","Almacena líquidos para uso posterior.","Armazene líquidos para uso posterior.","Хранит жидкости впрок.","储存液体以备后用。"])
# Diesel generator (Immersive)
add("3ECEA347016AE153",
    subtitle=["Generates electricity from Biodiesel.","Generates electricity from Biodiesel.","Génère de l'électricité à partir de Biodiesel.","Genera electricidad a partir de Biodiésel.","Gera eletricidade a partir de Biodiesel.","Производит электричество из Биодизеля.","用生物柴油发电。"])
# Inscriber presses dup -> already
# Congrats
add("4967FB1D252151AC",
    subtitle=["You finished it. Take a breath!","You finished it. Take a breath!","Vous avez terminé. Respirez !","¡Lo terminaste. Respira!","Você terminou. Respire!","Вы дошли до конца. Поздравляем!","你完成了，喘口气吧！"])
# Mech farms more / Inscriber dup

# Items / consumable / boss / hunters specific:
add("6D45CBE1391A9C3B",
    title=["Tater","Tater","Patate","Patata","Batata","Картошка","土豆"])
# Diesel silencer
add("5F54692C554A45BE",
    title=["Diesel Silencer","Diesel Silencer","Silencieux Diesel","Silenciador Diésel","Silenciador a Diesel","Глушитель Дизеля","柴油消音器"],
    desc=["Use on a Diesel Engine to silence it.","Use on a Diesel Engine to silence it.","Utilisez sur un Moteur Diesel pour le rendre silencieux.","Úsalo en un Motor Diésel para silenciarlo.","Use em um Motor a Diesel para silenciá-lo.","Используйте на Дизельном Двигателе для тишины.","用于消除柴油机噪音。"])
# Pickaxe head cooling
add("61EC2741A22844E2",
    title=["Cool the Pickaxe Head","Cool the Pickaxe Head","Refroidir la Tête de Pioche","Enfriar la Punta de Pico","Esfriar a Cabeça de Picareta","Охладите Кирку","冷却镐头"],
    subtitle=["Use a Cauldron of Water on the Hot Iron Head.","Use a Cauldron of Water on the Hot Iron Head.","Utilisez un chaudron d'eau sur la tête chaude.","Usa un caldero de agua sobre la punta caliente.","Use um caldeirão de água sobre a cabeça quente.","Используйте котёл с водой на горячую киркy.","用装水的炼药锅冷却铁镐头。"])
# Throwables
add("193B45B3804B5254",
    subtitle=["Items meant to be thrown.","Items meant to be thrown.","Objets à lancer.","Objetos para lanzar.","Itens para arremessar.","Метательные предметы.","用于投掷的物品。"],
    desc=["Bombs, grenades, and improvised projectiles.","Bombs, grenades, and improvised projectiles.","Bombes, grenades et projectiles improvisés.","Bombas, granadas y proyectiles improvisados.","Bombas, granadas e projéteis improvisados.","Бомбы, гранаты и метательные снаряды.","炸弹、手雷及临时投掷物。"])
# T1 Pistols
add("30F5C75D995786A1",
    subtitle=["Tier 1 sidearms.","Tier 1 sidearms.","Armes de poing niveau 1.","Pistolas Nivel 1.","Pistolas Nível 1.","Пистолеты 1 уровня.","一级手枪。"],
    desc=["Basic pistols for early combat.","Basic pistols for early combat.","Pistolets de base pour les premiers combats.","Pistolas básicas para combate inicial.","Pistolas básicas para combate inicial.","Базовые пистолеты для раннего боя.","早期战斗用基础手枪。"])
# Mage basics intro (subtitle present, no title/desc)
# Star meteorites
add("6AFA4723DACF735F",
    title=["Sky Stone Meteor","Sky Stone Meteor","Météorite de Pierre Céleste","Meteorito de Piedra Celeste","Meteorito de Pedra Celeste","Метеорит Небесного Камня","天石陨石"],
    subtitle=["Find meteorites with budding source crystals.","Find meteorites with budding source crystals.","Trouvez des météores avec des cristaux source en germination.","Encuentra meteoritos con cristales en brote.","Encontre meteoritos com cristais brotando.","Найдите метеориты с растущими кристаллами.","寻找带有萌芽水晶的陨石。"])
# Throwables / churros
add("34DAAF880FC0F5BB",
    subtitle=["Crispy fried churros.","Crispy fried churros.","Churros frits croustillants.","Churros fritos crujientes.","Churros fritos crocantes.","Хрустящие жареные чуррос.","酥炸吉拿果。"],
    desc=["Fry dough until golden and crispy.","Fry dough until golden and crispy.","Frire la pâte jusqu'à doré et croustillant.","Fríe la masa hasta dorar.","Frite a massa até dourar.","Жарьте тесто до золотистого цвета.","炸面团至金黄酥脆。"])
# Deepfry ice
add("4AA3033E2554D625",
    subtitle=["Fried ice? Crazy idea.","Fried ice? Crazy idea.","De la glace frite ? Folie.","¿Hielo frito? Una locura.","Gelo frito? Loucura.","Жареный лёд? Безумие.","炸冰？疯狂之举。"],
    desc=["Try frying ice in oil and see what happens.","Try frying ice in oil and see what happens.","Essayez de frire de la glace dans l'huile.","Intenta freír hielo en aceite.","Tente fritar gelo no óleo.","Попробуйте жарить лёд в масле.","试着把冰放进油里炸。"])
# Zanite armor
add("53C744149690F211",
    subtitle=["Zanite gear set.","Zanite gear set.","Panoplie de Zanite.","Set Zanite.","Conjunto Zanite.","Снаряжение Заните.","沙赞铁套装。"],
    desc=["Strong gear that gets faster as it wears.","Strong gear that gets faster as it wears.","Équipement plus rapide à mesure qu'il s'use.","Equipo que se vuelve más rápido al desgastarse.","Equipamento que fica mais rápido com o uso.","Снаряжение, ускоряющееся при износе.","随损耗加快的强力装备。"])
# Smithing tongs / fire (Tinkers steel?)
add("11613E54FFDAE519",
    title=["Smithing Tongs","Smithing Tongs","Pinces de Forge","Tenazas de Herrero","Tenazes de Ferreiro","Кузнечные Клещи","锻造钳"],
    subtitle=["Use bellows to upgrade fire to High Fire.","Use bellows to upgrade fire to High Fire.","Soufflet pour augmenter le feu en Grand Feu.","Usa fuelles para mejorar a Fuego Alto.","Use o fole para elevar a Fogo Alto.","Используйте мехи для Сильного Огня.","用风箱将火升级为高温火。"])
# Silver dungeon
add("478642D47E8F9E17",
    title=["Silver Dungeons","Silver Dungeons","Donjons d'Argent","Mazmorras de Plata","Masmorras de Prata","Серебряные Подземелья","白银地牢"],
    subtitle=["Home of the Valkyries.","Home of the Valkyries.","Demeure des Valkyries.","Hogar de las Valquirias.","Lar das Valquírias.","Дом Валькирий.","女武神的居所。"])
# Spirit horse extra entry
# Diary
add("15CC52773BC12069",
    title=["Explosive Diary","Explosive Diary","Journal Explosif","Diario Explosivo","Diário Explosivo","Взрывной Дневник","炸药日记"],
    desc=["A diary that goes boom...","A diary that goes boom...","Un journal qui explose...","Un diario que explota...","Um diário que explode...","Дневник, который взрывается...","会爆炸的日记。"])
# Crystal magnet
add("046435AD378CE0C8",
    title=["Master Magnet","Master Magnet","Aimant Maître","Imán Maestro","Ímã Mestre","Главный Магнит","顶级磁石"],
    desc=["The strongest magnet, very expensive to craft.","The strongest magnet, very expensive to craft.","L'aimant le plus puissant, très coûteux.","El imán más fuerte, muy costoso.","O ímã mais forte, muito caro.","Сильнейший магнит, очень дорогой.","最强的磁石，造价高昂。"])
# Mob trophies / heads
add("3A2B3C4D5E6F7007",
    subtitle=["Slay many creepers.","Slay many creepers.","Tuez de nombreux creepers.","Mata muchos creepers.","Mate muitos creepers.","Убейте много криперов.","击杀大量苦力怕。"],
    desc=["Hunt creepers and earn rewards.","Hunt creepers and earn rewards.","Chassez les creepers et gagnez des récompenses.","Caza creepers y gana recompensas.","Cace creepers e ganhe recompensas.","Охотьтесь на криперов за награды.","狩猎苦力怕获得奖励。"])
add("4A2B3C4D5E6F7004",
    subtitle=["Slay more spiders.","Slay more spiders.","Tuez plus d'araignées.","Mata más arañas.","Mate mais aranhas.","Убейте больше пауков.","击杀更多蜘蛛。"],
    desc=["Hunt spiders to advance.","Hunt spiders to advance.","Chassez les araignées pour progresser.","Caza arañas para avanzar.","Cace aranhas para avançar.","Охотьтесь на пауков.","狩猎蜘蛛以推进。"])
add("4A2B3C4D5E6F7007",
    subtitle=["Slay more spiders.","Slay more spiders.","Tuez plus d'araignées.","Mata más arañas.","Mate mais aranhas.","Убейте больше пауков.","击杀更多蜘蛛。"],
    desc=["Hunt spiders to advance.","Hunt spiders to advance.","Chassez les araignées pour progresser.","Caza arañas para avanzar.","Cace aranhas para avançar.","Охотьтесь на пауков.","狩猎蜘蛛以推进。"])
add("4A2B3C4D5E6F700A",
    subtitle=["Slay even more spiders.","Slay even more spiders.","Tuez encore plus d'araignées.","Mata aún más arañas.","Mate ainda mais aranhas.","Убейте ещё больше пауков.","击杀更多蜘蛛。"],
    desc=["Top tier spider hunter.","Top tier spider hunter.","Chasseur d'araignées de haut niveau.","Cazador de arañas avanzado.","Caçador avançado de aranhas.","Высший охотник на пауков.","顶级蜘蛛猎手。"])
add("5A2B3C4D5E6F7004",
    subtitle=["Slay more endermen.","Slay more endermen.","Tuez plus d'endermen.","Mata más endermen.","Mate mais endermen.","Убейте больше эндерменов.","击杀更多末影人。"],
    desc=["Hunt endermen to advance.","Hunt endermen to advance.","Chassez les endermen pour progresser.","Caza endermen para avanzar.","Cace endermen para avançar.","Охотьтесь на эндерменов.","狩猎末影人推进进度。"])
add("1A2B3C4D5E6F7007",
    subtitle=["Slay many zombies.","Slay many zombies.","Tuez de nombreux zombies.","Mata muchos zombies.","Mate muitos zumbis.","Убейте много зомби.","击杀大量僵尸。"],
    desc=["Hunt zombies and progress.","Hunt zombies and progress.","Chassez les zombies pour progresser.","Caza zombies para avanzar.","Cace zumbis para avançar.","Охота на зомби.","狩猎僵尸。"])
# Gold boss
add("080D80999BADAA4C",
    title=["The Golden Boss","The Golden Boss","Boss Doré","Jefe Dorado","Chefe Dourado","Золотой Босс","黄金Boss"],
    desc=["Defeat the gold boss.","Defeat the gold boss.","Vainquez le boss doré.","Vence al jefe dorado.","Derrote o chefe dourado.","Победите золотого босса.","击败黄金Boss。"])
# Marble guard key
add("6C44DDF01B250631",
    title=["Marble Guard Key","Marble Guard Key","Clé du Garde de Marbre","Llave del Guardia de Mármol","Chave do Guardião de Mármore","Ключ Мраморного Стража","大理石守卫之钥"],
    subtitle=["Use on the Weeping Stone to summon the Marble Guard.","Use on the Weeping Stone to summon the Marble Guard.","Utilisez sur la Pierre Pleurante pour invoquer le Garde de Marbre.","Úsala en la Piedra Llorona para invocar al Guardia.","Use na Pedra Chorona para invocar o Guarda.","Используйте на Плачущем Камне для призыва.","在哭泣石上召唤大理石守卫。"])
# Weeping rituals (Mysterious Flesh)
add("703C427FD167102E",
    subtitle=["A strange chunk of unknown flesh.","A strange chunk of unknown flesh.","Un étrange morceau de chair inconnue.","Un trozo extraño de carne desconocida.","Um pedaço estranho de carne desconhecida.","Странный кусок неизвестной плоти.","一块神秘的肉。"],
    desc=["Used in dark rituals. Handle with care.","Used in dark rituals. Handle with care.","Utilisée dans des rites sombres. Maniez avec soin.","Usada en rituales oscuros. Trátala con cuidado.","Usada em rituais sombrios. Manuseie com cuidado.","Используется в тёмных ритуалах.","用于黑暗仪式。请小心。"])
# Magic mage chapter intro
# Polished pickaxe head
add("39320A2E09986EBB",
    title=["Polish Pickaxe Head","Polish Pickaxe Head","Polir la Tête de Pioche","Pulir la Punta de Pico","Polir a Cabeça de Picareta","Отполировать Кирку","抛光镐头"],
    subtitle=["Sneak-right-click a grindstone with the rough head.","Sneak-right-click a grindstone with the rough head.","Faufilez-vous et faites clic-droit sur une meule.","Agáchate y haz clic derecho en una rueda de afilar.","Agache e clique direito numa pedra de amolar.","Шифт+ПКМ по точилу с грубой киркой.","潜行右键磨石抛光镐头。"])
# Nether portal needed
add("2C0630DEFE9C1703",
    title=["Nether Portal","Nether Portal","Portail du Nether","Portal del Nether","Portal do Nether","Портал в Нижний Мир","下界传送门"],
    subtitle=["Needed to access the Nether.","Needed to access the Nether.","Nécessaire pour accéder au Nether.","Necesario para acceder al Nether.","Necessário para acessar o Nether.","Нужен для входа в Нижний мир.","用于进入下界。"])
# Particles warning
add("5DD7826AA70B237A",
    title=["Particle Warning","Particle Warning","Avertissement Particules","Aviso de Partículas","Aviso de Partículas","Предупреждение о Частицах","粒子警告"],
    subtitle=["Careful! Spawns a lot of particles.","Careful! Spawns a lot of particles.","Attention ! Beaucoup de particules.","¡Cuidado! Genera muchas partículas.","Cuidado! Gera muitas partículas.","Осторожно! Много частиц.","注意！会产生大量粒子。"])
# Pickaxe stone
add("45585FBFF0EE3711",
    title=["Flint Pickaxe","Flint Pickaxe","Pioche en Silex","Pico de Pedernal","Picareta de Sílex","Кремневая Кирка","燧石镐"],
    subtitle=["Mine stone or pick up rocks for cobblestone.","Mine stone or pick up rocks for cobblestone.","Minez la pierre ou ramassez des cailloux.","Mina piedra o recoge guijarros.","Mine pedra ou pegue seixos.","Добывайте камень или собирайте камешки.","挖石头或捡石子合成圆石。"])
# Concrete mixture
add("1BFD0A51D3AE51E6",
    title=["Concrete Mix","Concrete Mix","Mélange de Béton","Mezcla de Hormigón","Mistura de Concreto","Бетонная Смесь","混凝土混合物"],
    subtitle=["Used to make liquid concrete or mixture.","Used to make liquid concrete or mixture.","Sert à faire du béton liquide.","Para hacer hormigón líquido.","Para fazer concreto líquido.","Для жидкого бетона.","用于制造液态混凝土。"])
# Hello item tooltip
add("57FB95F9223D0DBA",
    title=["Item Tooltip","Item Tooltip","Info-bulle d'Objet","Información de Objeto","Dica do Item","Подсказка Предмета","物品提示"],
    subtitle=["Hold W on the item to see its uses.","Hold W on the item to see its uses.","Maintenez W sur l'objet pour voir ses usages.","Mantén W para ver sus usos.","Segure W para ver os usos.","Удерживайте W для информации.","按住W查看用途。"])
# Creosote burner
add("14929C9B1FEC3ADF",
    title=["Creosote Burner","Creosote Burner","Brûleur à Créosote","Quemador de Creosota","Queimador de Creosoto","Креозотовая Горелка","木焦油燃烧器"],
    subtitle=["Runs on creosote.","Runs on creosote.","Fonctionne au créosote.","Funciona con creosota.","Funciona com creosoto.","Работает на креозоте.","以木焦油运行。"])
# Spaceship boss / quest (Fly a Phyg)
add("0DA9BD57864C9496",
    title=["Phyg Mount","Phyg Mount","Phyg Volant","Phyg Volador","Phyg Voador","Летающий Файг","飞猪坐骑"],
    desc=["Saddle a Phyg and fly through the Aether!","Saddle a Phyg and fly through the Aether!","Sellez un Phyg et volez à travers l'Aether !","¡Ensilla un Phyg y vuela por el Aether!","Sele um Phyg e voe pelo Aether!","Оседлайте Файга и летите через Эфир!","骑上飞猪在以太遨游！"])
# Blue Aercloud
add("73E44DE5235FABB5",
    title=["Aercloud Bounce","Aercloud Bounce","Rebond Aercloud","Rebote Aercloud","Salto Aercloud","Прыжок на Аэрооблаке","蓝云弹跳"],
    desc=["Jump on a Blue Aercloud to bounce!","Jump on a Blue Aercloud to bounce!","Sautez sur un Aercloud Bleu pour rebondir !","¡Salta sobre una Aercloud Azul para rebotar!","Salte numa Aercloud Azul para quicar!","Прыгайте на Голубом Аэрооблаке.","跳上蓝色以太云会弹跳。"])
# Aether food
add("0000000000000060",
    subtitle=["Aether-themed dishes and treats.","Aether-themed dishes and treats.","Plats inspirés de l'Aether.","Platos inspirados en el Aether.","Pratos inspirados no Aether.","Блюда в стиле Эфира.","以太主题美食。"],
    desc=["Cook unique recipes from the Aether dimension.","Cook unique recipes from the Aether dimension.","Cuisinez des recettes uniques de la dimension Aether.","Cocina recetas únicas del Aether.","Cozinhe receitas únicas do Aether.","Готовьте уникальные блюда Эфира.","烹饪以太维度独特的食谱。"])
# Mech farm subtitle
# Mass-storage chest / vault
# Clutches - already
# Tier 4 unlock
add("0380566D141BB870",
    subtitle=["Unlock Tier 4 progression.","Unlock Tier 4 progression.","Débloquez le Niveau 4.","Desbloquea el Nivel 4.","Desbloqueie o Nível 4.","Откройте 4 уровень.","解锁第4阶段。"],
    desc=["Complete previous tiers to unlock advanced content.","Complete previous tiers to unlock advanced content.","Terminez les niveaux précédents pour débloquer du contenu avancé.","Completa niveles previos para contenido avanzado.","Complete os níveis anteriores para conteúdo avançado.","Завершите предыдущие уровни.","完成之前阶段以解锁高级内容。"])
# T3 Rifles
add("2073BC0DA6934F44",
    subtitle=["Tier 3 long-range firearms.","Tier 3 long-range firearms.","Fusils longue portée niveau 3.","Rifles de largo alcance Nivel 3.","Rifles de longo alcance Nível 3.","Винтовки 3 уровня.","三级步枪。"],
    desc=["Powerful rifles for high-tier combat.","Powerful rifles for high-tier combat.","Fusils puissants pour combats avancés.","Rifles potentes para combate avanzado.","Rifles potentes para combate avançado.","Мощные винтовки для боя.","用于高级战斗的强力步枪。"])
add("5C838B3F85D10B06",
    subtitle=["Tier 2 long-range firearms.","Tier 2 long-range firearms.","Fusils longue portée niveau 2.","Rifles Nivel 2.","Rifles Nível 2.","Винтовки 2 уровня.","二级步枪。"],
    desc=["Mid-tier rifles for improved firepower.","Mid-tier rifles for improved firepower.","Fusils intermédiaires pour plus de puissance.","Rifles intermedios para más potencia.","Rifles intermediários para mais poder.","Винтовки среднего уровня.","中级步枪火力升级。"])
# T2 Lasers
add("2A8927BE3C9BE42D",
    subtitle=["Tier 1 laser weapons.","Tier 1 laser weapons.","Armes laser niveau 1.","Armas láser Nivel 1.","Armas laser Nível 1.","Лазеры 1 уровня.","一级激光武器。"],
    desc=["Basic energy weapons. Quiet, accurate.","Basic energy weapons. Quiet, accurate.","Armes énergétiques de base. Silencieuses.","Armas energéticas básicas. Silenciosas.","Armas energéticas básicas. Silenciosas.","Базовое энергетическое оружие.","基础能量武器。安静精准。"])
add("75501D53C27D9E44",
    subtitle=["Tier 2 laser weapons.","Tier 2 laser weapons.","Armes laser niveau 2.","Armas láser Nivel 2.","Armas laser Nível 2.","Лазеры 2 уровня.","二级激光武器。"],
    desc=["Improved laser tech for combat.","Improved laser tech for combat.","Tech laser améliorée.","Tecnología láser mejorada.","Tecnologia laser melhorada.","Улучшенная лазерная техника.","改进的激光武器技术。"])
# T2 LMGs
add("452406199120154F",
    subtitle=["Tier 2 light machine guns.","Tier 2 light machine guns.","Mitrailleuses légères niveau 2.","LMGs Nivel 2.","LMGs Nível 2.","Лёгкие пулемёты 2 уровня.","二级轻机枪。"],
    desc=["Suppressive fire and high capacity.","Suppressive fire and high capacity.","Tir de suppression et grande capacité.","Fuego de supresión y alta capacidad.","Fogo de supressão e alta capacidade.","Подавляющий огонь, большая ёмкость.","压制性火力和高容量。"])
# T3 SMGs
add("04FE720F8A825040",
    subtitle=["Tier 3 submachine guns.","Tier 3 submachine guns.","Pistolets-mitrailleurs niveau 3.","Subfusiles Nivel 3.","Submetralhadoras Nível 3.","Пистолет-пулемёт 3 уровня.","三级冲锋枪。"],
    desc=["High rate of fire and tight grouping.","High rate of fire and tight grouping.","Cadence élevée et précision serrée.","Alta cadencia y precisión.","Alta cadência e precisão.","Высокая скорость стрельбы.","高射速和精准度。"])
# Grain bags
add("7593331021924FFA",
    subtitle=["Bag of grain and fibers.","Bag of grain and fibers.","Sac de grains et fibres.","Bolsa de grano y fibras.","Saco de grãos e fibras.","Мешок зерна и волокон.","谷物纤维袋。"],
    desc=["Stores 9 of the same crop in one block.","Stores 9 of the same crop in one block.","Stocke 9 cultures identiques en un bloc.","Almacena 9 cultivos iguales en un bloque.","Armazena 9 cultivos iguais num bloco.","9 одинаковых культур в одном блоке.","9个相同作物存为一块。"])
# Ready for adventure
add("6DD78E64E1C6EB6E",
    subtitle=["Equipped and ready to explore.","Equipped and ready to explore.","Équipé et prêt à explorer.","Equipado y listo para explorar.","Equipado e pronto para explorar.","Готов к приключениям.","装备齐全准备探险。"],
    desc=["Complete the basic gear setup before heading out.","Complete the basic gear setup before heading out.","Complétez l'équipement de base avant de partir.","Completa el equipo básico antes de salir.","Complete o equipamento básico antes de sair.","Подготовьте снаряжение перед выходом.","出发前完成基础装备。"])
# Climbing safety
add("61A59240C36DBBC3",
    subtitle=["Climbing and safety gear.","Climbing and safety gear.","Équipement de grimpe et sécurité.","Equipo de escalada y seguridad.","Equipamento de escalada e segurança.","Снаряжение для лазанья.","攀爬与安全装备。"],
    desc=["Ropes, hooks, and nets to climb safely.","Ropes, hooks, and nets to climb safely.","Cordes, crochets et filets pour grimper en sécurité.","Cuerdas, ganchos y redes para escalar.","Cordas, ganchos e redes para escalar.","Верёвки, крюки и сетки.","绳索、钩子和网，安全攀爬。"])
# Exchange?
add("61F0CC8CFB51E81F",
    subtitle=["Exchange items in JEI/EMI?","Exchange items in JEI/EMI?","Échange dans JEI/EMI ?","¿Intercambio en JEI/EMI?","Troca em JEI/EMI?","Обмен предметами через JEI/EMI?","JEI/EMI 中交换？"],
    desc=["Look up trades or exchange recipes.","Look up trades or exchange recipes.","Consultez les recettes d'échange.","Consulta recetas de intercambio.","Consulte receitas de troca.","Просмотрите рецепты обмена.","查看交换配方。"])
# First step skyroot
add("F054A4125EA906B5",
    subtitle=["Begin your Aether adventure.","Begin your Aether adventure.","Commencez votre aventure Aether.","Comienza tu aventura en el Aether.","Comece sua aventura no Aether.","Начните приключение в Эфире.","开始你的以太冒险。"],
    desc=["Get a piece of Skyroot wood.","Get a piece of Skyroot wood.","Obtenez du bois de Skyroot.","Consigue madera de Skyroot.","Consiga madeira de Skyroot.","Получите древесину Скайрута.","获得一块天空根木。"])
# Creeper trophy
add("013102F28DEEDD9B",
    subtitle=["Kill a creeper.","Kill a creeper.","Tuez un creeper.","Mata un creeper.","Mate um creeper.","Убейте крипера.","击杀苦力怕。"],
    desc=["Defeat your first creeper.","Defeat your first creeper.","Vainquez votre premier creeper.","Vence a tu primer creeper.","Derrote seu primeiro creeper.","Победите первого крипера.","击败你的第一只苦力怕。"])
# Item drain / dough French
# Big Grinder
add("0C981CF1F57B4121",)  # already in stage
# Brass blockset / Edison
add("6CD6BF0D17D1605E",
    desc=["Craft a Light Bulb. Edison would be proud!","Craft a Light Bulb. Edison would be proud!","Fabriquez une Ampoule. Edison serait fier !","¡Crea una bombilla! Edison estaría orgulloso.","Faça uma lâmpada! Edison se orgulharia.","Создайте лампочку! Эдисон был бы рад.","制造一个灯泡。爱迪生会为你骄傲！"])
# Sticker description? In stage list
# Steam wheel / Item Vault desc already handled
# Hose Pulley dup (already)
# Item drain
add("70D8B3F19F4650F3",)  # already in STAGES via mapping
# Throwable copter
add("3A95793467582862",
    title=["Pedal Copter","Pedal Copter","Hélicoptère à Pédale","Helicóptero de Pedal","Helicóptero a Pedal","Велокоптер","脚踏直升机"],
    desc=["Muscle-powered copter. Give it a good push and fly!","Muscle-powered copter. Give it a good push and fly!","Hélico à pédales. Poussez bien et envolez-vous !","Helicóptero a pedales. Empújalo y vuela.","Helicóptero a pedais. Empurre e voe.","Велокоптер. Толкайте и взлетайте.","脚踏直升机，推一下就起飞。"])
# Cheese grater / Belt grinder
add("56FD7B7332D5B294",
    desc=["Obtain a Mechanical Belt Grinder.","Obtain a Mechanical Belt Grinder.","Obtenez une Meule à Bande mécanique.","Consigue una Esmeriladora Mecánica.","Obtenha um Esmerilhador Mecânico.","Получите Шлифовальный Станок.","获得机械皮带打磨机。"])
# Circuit breaker
add("5C5DE3ECE4E39C5F",
    desc=["Trigger an Overstress Clutch.","Trigger an Overstress Clutch.","Déclenchez un embrayage en surcharge.","Activa un embrague sobrecargado.","Acione uma embreagem sobrecarregada.","Активируйте сцепление перегрузки.","触发应力过载离合器。"])
# Mech belt grinder / sword stuff already
# Cooking pot mech
# Crank
# Cogwheels (5 stage descriptions already covered)
# Adjustable Chain Gearshift / Cogwheels stage
# Chocolate bucket etc.
# More: Inscriber, Diary, Mob trophies, Compteur de Vitesse, Stages all covered.
# Speed gauge title already
# Big millstone variant (Crushing Wheels)
add("7665792DA38DAB20",
    title=["Crushing Wheels","Crushing Wheels","Roues de Broyage","Ruedas Trituradoras","Rodas Trituradoras","Дробильные Колёса","破碎轮"],
    desc=["An upgrade to the millstone, with different recipes worth keeping both.","An upgrade to the millstone, with different recipes worth keeping both.","Évolution de la meule, recettes différentes - gardez les deux.","Mejora del molino, distintas recetas.","Melhoria do moinho, receitas diferentes.","Улучшение мельницы с иными рецептами.","磨石的升级版，配方不同。"])
# Crusher / grinder 4007D36163F8555E
add("4007D36163F8555E",
    title=["Millstone","Millstone","Meule","Molino","Moinho","Жёрнов","磨石"],
    desc=["Grind everything to dust.","Grind everything to dust.","Réduisez tout en poussière.","Tritura todo a polvo.","Triture tudo a pó.","Размельчите всё в пыль.","将一切磨成粉。"])
# Train conductor / Train Tracks already
# Wand of symmetry stage
# Cardboard armor (stage)
# Crafter chain & Brass casing stage descs covered
# Andesite Crusher already in stages

# Chainsaw blocks
add("7C2001A571863797", desc=["Blocks for tree felling or stripping logs.","Blocks for tree felling or stripping logs.","Blocs pour abattre les arbres et écorcer.","Bloques para talar y descortezar.","Blocos para derrubar e descascar.","Блоки для рубки и снятия коры.","用于砍树和剥皮的方块。"])

# Compact cart aluminum etc.
# More Create blocks
# Mechanical drill / saw / harvester / plough are bundled under one
# Train coupling already
# Brass casing stage
# Misc descriptions for incomplete subtitle entries
add("2CE8AD0D97FF0CD2",
    title=["Blaze Burner Straw","Blaze Burner Straw","Paille de Brûleur","Paja del Quemador","Palha do Queimador","Соломинка Горелки","熔炉吸管"],
    desc=["Pipe liquids into Blaze Burners. Press 'U' to see accepted liquids.","Pipe liquids into Blaze Burners. Press 'U' to see accepted liquids.","Tuyaute des liquides dans les Brûleurs. 'U' pour voir les liquides acceptés.","Canaliza líquidos a los Quemadores. 'U' para ver líquidos válidos.","Canalize líquidos aos Queimadores. 'U' para ver os aceitos.","Подаёт жидкости в горелки. 'U' для списка.","为熔炉输送液体。按U查看可接受液体。"])
# Brass Tunnel
add("1C901D6957027EB8",
    title=["Create Central Kitchen","Create Central Kitchen","Cuisine Centrale Create","Cocina Central de Create","Cozinha Central do Create","Кулинарный Цех Create","创生中央厨房"],
    desc=["Tools and methods to automate food processing in Create.","Tools and methods to automate food processing in Create.","Outils pour automatiser la cuisine avec Create.","Herramientas para automatizar la cocina con Create.","Ferramentas para automatizar a cozinha com Create.","Инструменты для автоматизации кухни.","在Create中自动化食物处理。"])
# Mech press 7665 already
# Repeater pulse
add("00CAE1781B96E802", desc=["A repeater that sends a pulse after a configurable delay.","A repeater that sends a pulse after a configurable delay.","Répétiteur qui envoie une impulsion après un délai configurable.","Repetidor que envía un pulso tras un retraso ajustable.","Repetidor que envia pulso após atraso ajustável.","Повторитель с настраиваемой задержкой.","可配置延时后发出脉冲的中继器。"])
# Observer
add("62810050F55539AE", desc=["A block that scans the world or inventories for specific items.","A block that scans the world or inventories for specific items.","Bloc qui surveille le monde ou les inventaires pour des objets précis.","Bloque que escanea el mundo o inventarios.","Bloco que escaneia o mundo ou inventários.","Блок, ищущий предметы в мире или инвентарях.","扫描世界或库存中特定物品的方块。"])
# Conveyor
add("5A28A5797BAD468A",)  # Stage 4 polished
# Gun rope
# Conditioner / placeholder
# Plough
add("11D65694A6D21224",
    title=["Mechanical Plough","Mechanical Plough","Charrue Mécanique","Arado Mecánico","Arado Mecânico","Механический Плуг","机械犁"],
    subtitle=["Tills dirt and clears rails.","Tills dirt and clears rails.","Laboure la terre et retire les rails.","Labra tierra y retira raíles.","Lavra terra e remove trilhos.","Возделывает землю и убирает рельсы.","耕地或清除铁轨。"])
# Cooled steam engine
# Wireless redstone

# Diving Boots Brass
add("312320F8FF1FDF24",
    title=["Brass Diving Boots","Brass Diving Boots","Bottes de Plongée en Laiton","Botas de Buceo Latón","Botas de Mergulho Latão","Латунные Сапоги","黄铜潜水靴"],
    desc=["An upgraded version of Copper Diving Boots.","An upgraded version of Copper Diving Boots.","Version améliorée des bottes de plongée en cuivre.","Versión mejorada de las botas de buceo de cobre.","Versão melhorada das botas de mergulho de cobre.","Улучшенная версия медных сапог.","铜潜水靴的升级版。"])
# Brass diving helmet (soldier-looking)
add("55BA739B45176F11",
    title=["Brass Diving Helmet","Brass Diving Helmet","Casque de Plongée Laiton","Casco de Buceo Latón","Capacete de Mergulho Latão","Латунный Шлем","黄铜潜水头盔"],
    desc=["An upgraded version of the Copper Diving Helmet.","An upgraded version of the Copper Diving Helmet.","Version améliorée du casque de plongée en cuivre.","Versión mejorada del casco de cobre.","Versão melhorada do capacete de cobre.","Улучшенная версия медного шлема.","铜潜水头盔的升级版。"])
add("2AB0806AA6A7076C",
    title=["Brass Diving Helmet","Brass Diving Helmet","Casque de Plongée Laiton","Casco de Buceo Latón","Capacete de Mergulho Latão","Латунный Шлем","黄铜潜水头盔"],
    desc=["An upgraded version of the Copper Diving Helmet.","An upgraded version of the Copper Diving Helmet.","Version améliorée du casque de plongée en cuivre.","Versión mejorada del casco de cobre.","Versão melhorada do capacete de cobre.","Улучшенная версия медного шлема.","铜潜水头盔的升级版。"])
# Brass casing (Mechanical material - 741500BAD9E30C78)
add("741500BAD9E30C78",
    title=["Brass Casing","Brass Casing","Caisson en Laiton","Carcasa de Latón","Caixa de Latão","Латунный Корпус","黄铜外壳"],
    desc=["A material used in advanced mechanical crafting.","A material used in advanced mechanical crafting.","Matériau pour fabrications mécaniques avancées.","Material para fabricación mecánica avanzada.","Material para fabricação mecânica avançada.","Материал для продвинутых механических крафтов.","用于高级机械合成的材料。"])
# Connecting wire
add("5D19586551060173",
    title=["Wire Coil","Wire Coil","Bobine de Fil","Bobina de Cable","Bobina de Fio","Катушка Провода","线圈"],
    desc=["Used to connect electrical connectors.","Used to connect electrical connectors.","Sert à relier les connecteurs électriques.","Para conectar conectores eléctricos.","Para conectar conectores elétricos.","Соединяет электрические разъёмы.","用于连接电气连接器。"])
# Blaze burner extra hint
add("47AFC34A3A389CBC",
    desc=["Right-click a blaze spawner or blaze to fill the burner.","Right-click a blaze spawner or blaze to fill the burner.","Clic droit sur un blaze ou son spawner pour le remplir.","Clic derecho en un blaze o spawner para llenarlo.","Clique direito num blaze ou spawner para encher.","ПКМ по бластеру или спавнеру.","右键烈焰人或刷怪笼以填充。"])

# Andesite/Brass overlap leftovers
# Sticker
# Schematic table
# Sticker stage
# Speedometer stage
# Wand of symmetry stage already
# Speedometer subtitle stage already

# A few remaining single items:
# Master of Arcana / first spell already
# Note: dup-aware: already handled all

# Items left from missing fields lookup:
# 5DD7826AA70B237A - particles warning DONE
# 39320A2E09986EBB - polish DONE
# 2C0630DEFE9C1703 - nether portal DONE
# 11613E54FFDAE519 - smithing tongs DONE
# 478642D47E8F9E17 - silver dungeons DONE
# 45585FBFF0EE3711 - flint pickaxe DONE

# Items with subtitle only missing remaining: e.g. 6943EC451A810470 done
# Crafters - endgame stage 2F40DF4899014EF0 stage8 done
# Crusher - endgame 0C981CF1F57B4121 stage8 done
# Item Drain stage descriptions covered

def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        bin_data = json.load(f)

    output = {}
    missing_handled = []
    for q in bin_data:
        qid = q["id"]
        missing = q["missing_fields"]
        if qid not in QUESTS:
            # Fallback: synthesize generic content based on current text
            QUESTS[qid] = {}
        entry = QUESTS[qid]
        out = {lang: {} for lang in LANGS}
        for field in missing:
            key = field
            data = entry.get(field)
            if data is None:
                # No explicit data: synthesize from existing
                fallback = synthesize(q, field)
                data = fallback
            for i, lang in enumerate(LANGS):
                val = data[i]
                if field == "quest_desc" or field == "desc":
                    out[lang]["quest_desc"] = [val]
                elif field == "quest_subtitle" or field == "subtitle":
                    out[lang]["quest_subtitle"] = val
                else:
                    out[lang]["title"] = val
        # rename keys to expected schema
        cleaned = {}
        for lang, fields in out.items():
            cleaned_fields = {}
            for k, v in fields.items():
                cleaned_fields[k] = v
            cleaned[lang] = cleaned_fields
        output[qid] = cleaned

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(output)} quests to {OUTPUT}")

    # Report any quests where we used fallback
    fallback_ids = [qid for qid in (q["id"] for q in bin_data) if qid not in QUESTS or not QUESTS[qid]]
    print(f"Used fallback for {len(fallback_ids)} quests")

def synthesize(quest, field):
    """Generate a sensible fallback for unmapped quests."""
    cur_title = quest.get("current_title","")
    cur_sub = quest.get("current_subtitle","")
    cur_desc = quest.get("current_desc","")
    if field == "title":
        # Use current_title cleanly, or derive from subtitle
        candidate = cur_title or (cur_sub.split(".")[0][:30] if cur_sub else "Quest")
        # strip ID-like
        if candidate.startswith("create:"):
            candidate = candidate.replace("create:","").replace("_"," ").title()
        return [candidate]*7
    if field == "subtitle":
        s = cur_sub or (cur_title or "")
        if len(s) > 80:
            s = s[:77] + "..."
        return [s]*7
    if field == "desc":
        d = cur_desc or cur_sub or cur_title or ""
        return [d]*7
    return [""]*7

if __name__ == "__main__":
    main()
