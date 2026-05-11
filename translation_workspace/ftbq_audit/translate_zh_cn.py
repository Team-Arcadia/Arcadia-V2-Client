"""Translate FTB Quests titles/subtitles EN -> zh_cn for Arcadia V2."""
import json
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit")
IN_FILE = ROOT / "to_translate_zh_cn.json"
OUT_FILE = ROOT / "agent_outputs_other" / "zh_cn.json"

# ---------------- Translation tables ----------------

# Proper nouns kept as-is (chapter names, mod names, etc.)
PROPER_NOUNS = {
    "Ars Nouveau", "Ars Creo", "Apotheosis", "Apothic Enchanting", "Apothic Spawner",
    "Mekanism", "Create", "Chipped", "Optical", "Connected", "Better Archeology",
    "Immersive Engineering", "Immersive Aircraft", "Simply Swords", "Epic Ink",
    "The Aether", "Mutant Monsters", "Mekanism Reactor", "Pump Dat Oil",
    "Enchantment Industry", "Slice & Dice", "Cardboard", "Twilight Forest",
}

# Common mob name CN translations
MOB_NAMES = {
    "Adherent": "信徒",
    "Armored Giant": "装甲巨人",
    "Barakoa": "巴拉科亚",
    "Barakoana": "巴拉科亚娜",
    "Blaze": "烈焰人",
    "Bogged": "沼骸",
    "Breeze": "旋风人",
    "Carminite Broodling": "红玉幼虫",
    "Carminite Ghastguard": "红玉恶魂守卫",
    "Carminite Ghastling": "红玉幼恶魂",
    "Carminite Golem": "红玉魔像",
    "Cave Spider": "洞穴蜘蛛",
    "Cave Troll": "洞穴巨魔",
    "Creeper": "苦力怕",
    "Death Tome": "亡灵之书",
    "Drowned": "溺尸",
    "Elder Guardian": "远古守卫者",
    "Ender Dragon": "末影龙",
    "Enderman": "末影人",
    "Endermite": "末影螨",
    "Evoker": "唤魔者",
    "Ferrous Wroughtnaut": "铁锻巨像",
    "Fire Beetle": "火甲虫",
    "Foliaath": "食人花",
    "Frostmaw": "霜咬兽",
    "Ghast": "恶魂",
    "Giant Miner": "巨型矿工",
    "Goblin Knight": "哥布林骑士",
    "Harbinger Cube": "先驱方块",
    "Hedge Spider": "树篱蜘蛛",
    "Helmet Crab": "头盔螃蟹",
    "Hoglin": "疣猪兽",
    "Hostile Wolf": "敌对狼",
    "Ice Core": "冰核",
    "Illusioner": "幻术师",
    "King Spider": "蜘蛛王",
    "Kobold": "狗头人",
    "Magma Cube": "岩浆怪",
    "Maze Slime": "迷宫史莱姆",
    "Minotaur": "牛头怪",
    "Mist Wolf": "雾狼",
    "Mosquito Swarm": "蚊群",
    "Mutant Creeper": "变异苦力怕",
    "Mutant Enderman": "变异末影人",
    "Mutant Skeleton": "变异骷髅",
    "Mutant Snow Golem": "变异雪傀儡",
    "Mutant Zombie": "变异僵尸",
    "Naga": "娜迦",
    "Phantom": "幻翼",
    "Piglin": "猪灵",
    "Piglin Brute": "猪灵蛮兵",
    "Pillager": "掠夺者",
    "Pinch Beetle": "钳虫",
    "Ravager": "劫掠兽",
    "Redcap Goblin": "红帽哥布林",
    "Redcap Sapper": "红帽工兵",
    "Roving Cube": "游荡方块",
    "Shulker": "潜影贝",
    "Silverfish": "蠹虫",
    "Skeleton": "骷髅",
    "Skeleton Druid": "骷髅德鲁伊",
    "Slime Beetle": "史莱姆甲虫",
    "Snow Guardian": "雪之守卫者",
    "Spider": "蜘蛛",
    "Stray": "流浪者",
    "Swarm Spider": "蜂群蜘蛛",
    "Towerwood Borer": "塔木钻虫",
    "Twilight Wraith": "暮光幽魂",
    "Umvuthana": "乌姆乌塔纳",
    "Umvuthi": "乌姆乌提",
    "Vex": "恼鬼",
    "Vindicator": "卫道士",
    "Winter Wolf": "冬狼",
    "Witch": "女巫",
    "Wither": "凋灵",
    "Wither Skeleton": "凋灵骷髅",
    "Zoglin": "僵尸疣猪兽",
    "Zombie": "僵尸",
    "Zombie Villager": "僵尸村民",
    "Zombified Piglin": "僵尸猪灵",
}

# Whole-string exact translations (for common repeated strings)
EXACT = {
    # Ars Nouveau chapter titles / phrases
    "The Ars Universe": "新生魔艺宇宙",
    "Ars Nouveau: The Arcana": "新生魔艺：奥秘",
    "Ars Creo : L'Alchemy Magique": "魔艺创造：魔法炼金",
    "Arcane Essence": "奥术精华",
    "Arcane discovery.": "奥术发现。",
    "Arcane scholarship.": "奥术学识。",
    "Weave the arcana.": "编织奥秘。",
    "Master the glyphs.": "精通符文。",
    "Channel the source.": "引导源能。",
    "A novice's journey.": "新手之旅。",
    "Spellcraft mastery.": "法术工艺精通。",
    "The mage's arsenal.": "法师的武器库。",
    "Unleash the elements.": "释放元素之力。",
    "Runic mysteries.": "符文奥秘。",
    "Ritual mastery.": "仪式精通。",
    "Spirits beckon.": "灵魂召唤。",
    "Demonic pact.": "恶魔契约。",
    "Occult knowledge.": "神秘知识。",
    "Tier up!": "升级！",
    "Science prevails.": "科学胜出。",
    "Chemical mastery.": "化学精通。",
    "Industrial evolution.": "工业进化。",
    "The Other side.": "彼端世界。",
    # Backpack chapter
    "Pack it better.": "装得更好。",
    "Backpack evolution.": "背包进化。",
    "Carry the world.": "携带整个世界。",
    "Upgrade your carry.": "升级你的负重。",
    "Upgrade installed.": "升级已安装。",
    # Create stages
    "STAGE 1: PRIMARY MECHANICS (Andesite)": "阶段1：基础机械（安山岩）",
    "STAGE 1 : PRIMARY MECHANICS (Andesite)": "阶段1：基础机械（安山岩）",
    "STAGE 3: HYDRAULICS (Copper)": "阶段3：液压（铜）",
    "STAGE 3 : HYDRAULICS (Copper)": "阶段3：液压（铜）",
    "STAGE 3 : HYDRAULIQUE (Cuivre)": "阶段3：液压（铜）",
    "STAGE 4: PRECISION (Brass)": "阶段4：精密（黄铜）",
    "STAGE 4 : PRECISION (Brass)": "阶段4：精密（黄铜）",
    "STAGE 7: DECO & CONSTRUCTION (The Style)": "阶段7：装饰与建筑（风格）",
    "STAGE 7 : DECO & CONSTRUCTION (Style)": "阶段7：装饰与建筑（风格）",
    "STAGE 7 : DECO & CONSTRUCTION (The Style)": "阶段7：装饰与建筑（风格）",
    "STAGE 8: EQUIPMENT & SPECIAL ADDONS (Slice & Dice, Cardboard...)": "阶段8：装备与特殊扩展（Slice & Dice，Cardboard...）",
    "STAGE 8 : EQUIPMENT & SPECIAL ADDONS (Slice & Dice, Cardboard...)": "阶段8：装备与特殊扩展（Slice & Dice，Cardboard...）",
    "Epic Ink": "史诗墨水",
}

# Color-coded common Ars French titles -> CN (some entries already in French)
EXACT_COLORED = {
    "&aL'Enchantement Arcanique&r": "&a奥术附魔&r",
    "&eLa Source de Magie&r": "&e魔法之源&r",
    "&5Les Familiers Magiques&r": "&5魔法宠物&r",
    "&6La Table du Scribe&r": "&6抄写员之桌&r",
    "&6Premiers Glyphes&r": "&6初始符文&r",
    "&4Les Wilden Hostiles&r": "&4敌对野荒兽&r",
    "&dBienvenue dans l'Arcane&r": "&d欢迎来到奥秘&r",
    "&7Les premiers pas du mage&r": "&7法师的第一步&r",
    "&6Automation Arcanique&r": "&6奥术自动化&r",
    "&7Protection et puissance arcanique&r": "&7奥术防护与力量&r",
    "&3L'Armure du Mage&r": "&3法师之甲&r",
    "&7Large-scale magic&r": "&7大规模魔法&r",
    "&dLe Rituel Arcanique&r": "&d奥术仪式&r",
    "&7Invoquer des compagnons arcaniques&r": "&7召唤奥术伙伴&r",
    "&7Store arcane energy&r": "&7储存奥术能量&r",
    "&7Ascension vers l'Archimage&r": "&7晋升大法师&r",
    "&bComplete Ars Master&r": "&b完全魔艺大师&r",
    "&7Predator's reward&r": "&7掠食者的奖励&r",
    "&7Bounty hunter's mark&r": "&7赏金猎人之印&r",
    "&7Permanent large-scale magic&r": "&7永久大规模魔法&r",
    "&7Create your own custom spells&r": "&7创造你自己的法术&r",
    "&7Flames dance along its searing edge&r": "&7火焰沿其灼热边缘起舞&r",
    "&7Where coal becomes something greater&r": "&7当煤炭蜕变为更伟大之物&r",
    "&7Nature's wrath woven into thorned steel&r": "&7自然之怒编入荆刺之钢&r",
    "&7A leviathan's fury given form&r": "&7利维坦之怒化作实形&r",
    "&7The lich has fully risen — beware its wrath&r": "&7巫妖已完全苏醒 — 当心其怒火&r",
}

# Phrase-level fragments (applied to plain English text after color stripping logic)
PHRASES = [
    # Order matters: longer phrases first
    ("Bounty hunter's mark", "赏金猎人之印"),
    ("Predator's reward", "掠食者的奖励"),
    ("Awakens nearby blocks", "唤醒附近的方块"),
    ("Places a magical light source", "放置一个魔法光源"),
    ("Lets you create your own custom functional clock", "让你创造自己的自定义功能时钟"),
    ("Launches the target into the air", "将目标击飞至空中"),
    ("Periodically grants random buffs", "定期给予随机增益"),
    ("Draws permanent ritual circles", "绘制永久仪式法阵"),
    ("Massively accelerates plant growth", "大幅加速植物生长"),
    ("Targets entities more precisely", "更精确地瞄准实体"),
    ("Create your own custom spells", "创造你自己的法术"),
    ("Store arcane energy", "储存奥术能量"),
    ("Large-scale magic", "大规模魔法"),
    ("Permanent large-scale magic", "永久大规模魔法"),
    ("Complete Ars Master", "完全魔艺大师"),
    ("The lich has fully risen", "巫妖已完全苏醒"),
    ("beware its wrath", "当心其怒火"),
    ("Flames dance along its searing edge", "火焰沿其灼热边缘起舞"),
    ("Where coal becomes something greater", "当煤炭蜕变为更伟大之物"),
    ("Nature's wrath woven into thorned steel", "自然之怒编入荆刺之钢"),
    ("A leviathan's fury given form", "利维坦之怒化作实形"),
    # Generic actions
    ("Defeat the", "击败"),
    ("Defeat", "击败"),
    ("Kill the", "击杀"),
    ("Kill", "击杀"),
    ("Slay the", "斩杀"),
    ("Slay", "斩杀"),
    ("Hunt the", "猎杀"),
    ("Hunt", "猎杀"),
    ("Find the", "寻找"),
    ("Find", "寻找"),
    ("Craft the", "制作"),
    ("Craft", "制作"),
    ("Build the", "建造"),
    ("Build", "建造"),
    ("Obtain the", "获得"),
    ("Obtain", "获得"),
    ("Collect the", "收集"),
    ("Collect", "收集"),
    ("Mine the", "开采"),
    ("Mine", "开采"),
    ("Get the", "获取"),
    ("Get", "获取"),
    ("Use the", "使用"),
    ("Use", "使用"),
    ("Make the", "制造"),
    ("Make", "制造"),
    ("Place the", "放置"),
    ("Place", "放置"),
    ("Enchant the", "附魔"),
    ("Enchant", "附魔"),
    ("Upgrade the", "升级"),
    ("Upgrade", "升级"),
    ("Reward", "奖励"),
    ("Quest", "任务"),
    ("Task", "任务"),
    # Common adjectives
    ("Master", "大师"),
    ("Hunter", "猎人"),
    ("Welcome to", "欢迎来到"),
    ("Introduction", "介绍"),
    ("The basics", "基础"),
    ("Basics", "基础"),
    # Materials
    ("Netherite", "下界合金"),
    ("Diamond", "钻石"),
    ("Iron", "铁"),
    ("Golden", "金"),
    ("Gold", "金"),
    ("Stone", "石"),
    ("Wooden", "木"),
    ("Wood", "木"),
    ("Copper", "铜"),
    ("Brass", "黄铜"),
    ("Andesite", "安山岩"),
    # Tools
    ("Sword", "剑"),
    ("Bow", "弓"),
    ("Crossbow", "弩"),
    ("Shield", "盾牌"),
    ("Pickaxe", "镐"),
    ("Axe", "斧"),
    ("Shovel", "锹"),
    ("Hoe", "锄"),
    # Armor
    ("Helmet", "头盔"),
    ("Chestplate", "胸甲"),
    ("Leggings", "护腿"),
    ("Boots", "靴子"),
    # Colors
    ("Red", "红色"),
    ("Blue", "蓝色"),
    ("Green", "绿色"),
    ("Yellow", "黄色"),
    ("White", "白色"),
    ("Black", "黑色"),
]

COLOR_RE = re.compile(r"(§[0-9a-fk-or]|&[0-9a-fk-or])", re.IGNORECASE)
HUNTER_RE = re.compile(r"^Hunter:\s+([A-Za-z\s\'-]+?)\s*\((\d+)\)\s*$")

# Cache for translated strings
_cache = {}


def translate_hunter(val):
    m = HUNTER_RE.match(val)
    if not m:
        return None
    mob = m.group(1).strip()
    count = m.group(2)
    cn = MOB_NAMES.get(mob, mob)
    return f"猎人：{cn} ({count})"


def translate_text(text):
    """Translate a single plain-text segment (no color codes)."""
    if not text or not text.strip():
        return text

    stripped = text.strip()

    # Exact match in proper nouns -> keep
    if stripped in PROPER_NOUNS:
        return text

    # Exact lookup
    if stripped in EXACT:
        # Preserve leading/trailing whitespace
        prefix = text[: len(text) - len(text.lstrip())]
        suffix = text[len(text.rstrip()):]
        return prefix + EXACT[stripped] + suffix

    # Hunter pattern
    hunter = translate_hunter(stripped)
    if hunter:
        prefix = text[: len(text) - len(text.lstrip())]
        suffix = text[len(text.rstrip()):]
        return prefix + hunter + suffix

    # Apply phrase replacements
    result = text
    for en, cn in PHRASES:
        # Word-boundary-ish replacement (case-sensitive)
        pattern = r"\b" + re.escape(en) + r"\b"
        result = re.sub(pattern, cn, result)

    # Apply mob name replacements as well
    for mob, cn in MOB_NAMES.items():
        pattern = r"\b" + re.escape(mob) + r"\b"
        result = re.sub(pattern, cn, result)

    return result


def translate_value(val):
    """Translate a full value, preserving color codes and structure."""
    if not isinstance(val, str) or not val:
        return val
    if val in _cache:
        return _cache[val]

    # Whole-string exact (with color codes)
    if val in EXACT_COLORED:
        _cache[val] = EXACT_COLORED[val]
        return _cache[val]

    # Whole-string exact (no color)
    if val in EXACT:
        _cache[val] = EXACT[val]
        return _cache[val]

    # Hunter pattern (often plain)
    hunter = translate_hunter(val)
    if hunter:
        _cache[val] = hunter
        return _cache[val]

    # Normalize unicode section sign to & for consistency, but preserve format
    # We process by splitting on color codes and translating only text segments.
    parts = COLOR_RE.split(val)
    out = []
    for p in parts:
        if not p:
            out.append(p)
            continue
        if COLOR_RE.fullmatch(p):
            out.append(p)
        else:
            out.append(translate_text(p))
    result = "".join(out)
    _cache[val] = result
    return result


def main():
    with IN_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entries from {IN_FILE.name}")

    out = {}
    for k, v in data.items():
        out[k] = translate_value(v)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(out)} entries to {OUT_FILE}")
    # Sanity verification
    assert len(out) == len(data), "Key count mismatch"
    print("OK: key count matches")


if __name__ == "__main__":
    main()
