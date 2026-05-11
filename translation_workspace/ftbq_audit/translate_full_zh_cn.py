#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bulk translation of FTB Quests remaining English entries to Simplified Chinese.
Input : full_to_translate_zh_cn.json (2402 entries)
Output: full_output/zh_cn.json
"""

import json
import re
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE, "full_to_translate_zh_cn.json")
OUTPUT_DIR = os.path.join(BASE, "full_output")
OUTPUT = os.path.join(OUTPUT_DIR, "zh_cn.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. PHRASE-LEVEL DICTIONARY (exact / near-exact full sentences and titles).
#    Highest priority. Applied to the raw string after color-code masking.
# ---------------------------------------------------------------------------

PHRASE_MAP = {
    # ── Chapter titles ────────────────────────────────────────────────
    "Enchantment Industry": "附魔工业",
    "Pump Dat Oil": "石油抽取",
    "Apotheosis Gem": "神化宝石",
    "Apotheosis Spawner": "神化刷怪笼",
    "Apothic Enchanting": "神化附魔",
    "Apothic Spawners": "神化刷怪笼",
    "Apothic Attributes": "神化属性",
    "Chipped": "Chipped 装饰",
    "Mekanism Reactor": "通用机械:反应堆",
    "Mekanism": "通用机械",
    "Mekanism Generators": "通用机械:发电机",
    "Better Archeology": "更好的考古",
    "Immersive Engineering": "沉浸工程",
    "Immersive Aircraft": "沉浸航空器",
    "Mutant Monsters": "变种生物",
    "The Aether": "以太",
    "Aether": "以太",
    "Optical": "光学",
    "Connected": "联通",
    "Aquaculture": "水产养殖",
    "Addon Harmony": "附加和谐",
    "Occultism": "神秘学",
    "Applied Energistics": "应用能源",
    "Applied Energistics 2": "应用能源 2",
    "Simply Swords": "Simply Swords 武器",
    "Create": "机械动力",
    "Create I": "机械动力 I",
    "Create II": "机械动力 II",
    "Create III": "机械动力 III",
    "Create IV": "机械动力 IV",
    "Create V": "机械动力 V",
    "Tetra": "Tetra 锻造",
    "Twilight Forest": "暮色森林",
    "Botania": "植物魔法",
    "Thermal": "热力系列",
    "Thermal Series": "热力系列",
    "Industrial Foregoing": "实用前瞻",
    "Bigger Reactors": "更大的反应堆",
    "Mystical Agriculture": "神秘农业",
    "Ars Nouveau": "新生魔艺",
    "Iron's Spells": "铁系法术",
    "Iron's Spells & Spellbooks": "铁系法术与法术书",
    "Apotheosis": "神化",
    "Cataclysm": "灾变",
    "Alex's Caves": "阿莱克的洞穴",
    "Alex's Mobs": "阿莱克的生物",
    "When Dungeons Arise": "地牢崛起",
    "YUNG's Better Dungeons": "YUNG 的更好地牢",
    "Builder's Wand": "建造法杖",
    "Builders Wand": "建造法杖",
    "Trinkets and Baubles": "饰品与小物件",
    "Curios": "饰品",
    "Curios API": "饰品 API",
    "Storage Drawers": "储存抽屉",
    "Sophisticated Backpacks": "精致背包",
    "Sophisticated Storage": "精致储存",
    "Functional Storage": "实用储存",
    "Iron Chests": "铁制箱子",
    "Iron Furnaces": "铁制熔炉",
    "Powah!": "Powah! 能源",
    "Powah": "Powah 能源",
    "EnderIO": "末影接口",
    "Refined Storage": "精致储存(RS)",
    "Refined Storage Addons": "精致储存附加",
    "Pipez": "管道扩展",
    "JEI": "JEI 物品管理",
    "Just Enough Items": "JEI 物品管理",
    "Tinkers' Construct": "匠魂",
    "Pam's HarvestCraft": "Pam 的丰收工艺",
    "Better Combat": "更好的战斗",
    "Epic Fight": "史诗战斗",
    "Tool Belt": "工具腰带",
    "Magnet": "磁铁",
    "Magnets": "磁铁",
    "Quark": "夸克",
    "Supplementaries": "补充内容",
    "Dungeons and Taverns": "地牢与酒馆",
    "Mowzie's Mobs": "Mowzie 的生物",
    "Born in Chaos": "混沌降生",
    "Friends and Foes": "朋友与敌人",
    "Aquamirae": "水镜",
    "Endless Biomes": "无尽生物群系",
    "Biomes O' Plenty": "丰富生物群系",
    "Oh The Biomes You'll Go": "你将穿越的生物群系",
    "Terralith": "Terralith 地形",
    "AppleSkin": "苹果皮",
    "Farmer's Delight": "农夫乐事",
    "Brewin' And Chewin'": "酿造与咀嚼",
    "Bountiful": "丰饶",
    "Aqua Acrobatics": "水中杂技",
    "Combat Roll": "战斗翻滚",
    "First Person Model": "第一人称模型",
    "Animal Garden": "动物花园",
    "Goblin Traders": "哥布林商人",
    "Wandering Collector": "流浪收集者",
    "Easy Magic": "简易魔法",
    "Mahou Tsukai": "魔法使",
    "Forbidden and Arcanus": "禁忌与神秘",
    "Eternal Starlight": "永恒星光",
    "Productive Bees": "高效蜜蜂",
    "Productive Trees": "高效树木",
    "Resourceful Bees": "丰富蜜蜂",
    "Botany Pots": "植物花盆",
    "Botany Trees": "植物花盆:树木",
    "Naturalist": "博物学家",
    "Nature's Compass": "自然指南针",
    "Explorer's Compass": "探险家指南针",
    "Waystones": "传送石碑",
    "Xaero's Map": "Xaero 地图",
    "Xaero's Minimap": "Xaero 小地图",
    "JourneyMap": "旅行地图",
    "Antique Atlas": "古董地图集",
    "FTB Library": "FTB 库",
    "FTB Teams": "FTB 队伍",
    "FTB Chunks": "FTB 区块",
    "FTB Quests": "FTB 任务",
    "FTB Ranks": "FTB 等级",
    "FTB Essentials": "FTB 基础",
    "Polymorph": "Polymorph 多态合成",
    "Cooking for Blockheads": "笨蛋的烹饪书",
    "Crafting Tweaks": "合成调整",
    "Inventory Tweaks": "物品栏调整",
    "Inventory Sorter": "物品栏排序",
    "Better F3": "更好的 F3",
    "Better Title Screen": "更好的标题界面",
    "Better Advancements": "更好的进度",
    "Better Statistics Screen": "更好的统计界面",
    "Mod List": "模组列表",
    # Generic single chapter labels
    "Equipment": "装备",
    "Tools": "工具",
    "Weapons": "武器",
    "Armor": "护甲",
    "Magic": "魔法",
    "Combat": "战斗",
    "Exploration": "探索",
    "Building": "建造",
    "Farming": "农业",
    "Decoration": "装饰",
    "Storage": "储存",
    "Power": "能源",
    "Automation": "自动化",
    "Transportation": "运输",
    "Adventure": "冒险",
    "Bosses": "首领",
    "Dungeons": "地牢",
    "Quests": "任务",
    "Resources": "资源",
    "Materials": "材料",
    "Mining": "采矿",
    "Smelting": "冶炼",
    "Crafting": "合成",
    "Brewing": "酿造",
    "Alchemy": "炼金",
    "Enchanting": "附魔",
    "Curios & Trinkets": "饰品与小物件",
    "Endgame": "终局",
    "Setup": "配置",
    "Tutorial": "教程",
    "Introduction": "简介",
    "Welcome": "欢迎",
    "Basics": "基础",
    "Advanced": "进阶",
    "Expert": "专家",
    "Master": "大师",
    "Legendary": "传奇",
    # ── Common quest desc sentences (existing in TM) ──────────────────
    "Glory to the Hunter.": "光荣属于猎人。",
    "Power of Words.": "言语的力量。",
    "Power of words.": "言语的力量。",
    "Transform your wild finds into cultivable seeds.": "把你在野外的发现转化为可种植的种子。",
    "Store your harvests compactly.": "紧凑地存储你的收成。",
    "The Sun Spirit is immune to direct attacks. Deflect its fireballs back!": "太阳之灵免疫直接攻击，请反弹它的火球！",
    "Cook for your animals!": "为你的动物烹饪食物！",
    "Liquid manipulation: Water, Lava, Chocolate, Honey...": "液体操控：水、岩浆、巧克力、蜂蜜……",
    "Strange occurrences in the Nether.": "下界中诡异的现象。",
    "Vile structures deep in the Nether.": "下界深处邪恶的建筑。",
    "By using coal, you can get power to provide for your storage system.": "使用煤炭可以为你的储存系统供电。",
    "rail": "铁轨",
    "Terminal": "终端",
    "Any Train Track": "任意火车轨道",
    "Breaks blocks instantly.": "瞬间破坏方块。",
    "Makes you invisible.": "使你隐身。",
    "Breaks trees in one go.": "一次性砍倒整棵树。",
    "Increases the spell's power.": "增加法术的威力。",
    "Places a magical light source.": "放置一个魔法光源。",
    "Names the target.": "命名目标。",
    "Stores Source energy.": "储存源质能量。",
    "Single-use spell scroll.": "一次性法术卷轴。",
    "Slows down targets.": "减速目标。",
    "Accelerates plant growth.": "加速植物生长。",
    "Controls magical servants.": "控制魔法仆从。",
    "Base block for magical structures.": "魔法结构的基础方块。",
    "Projectiles bounce off surfaces.": "弹射物从表面反弹。",
    "An upgraded version of the Conjuration Wand.": "召唤法杖的升级版本。",
    "Simply a Potato Cannon.": "就是一门土豆加农炮。",
    "Mysterious Flesh": "神秘血肉",
    "A key component.": "关键组件。",
    "I Know What You're Thinking": "我知道你在想什么",
    "bauxite :o": "铝土矿 :o",
    "Hold W on the item to see it's uses": "把鼠标悬停在物品上，按住 W 查看它的用途",
    "Hold W on the item to see it'…": "把鼠标悬停在物品上，按住 W 查看…",
    "Lets you charge certain items.": "可以为某些物品充能。",
    "A more configurable chute.": "更可配置的滑槽。",
    "When placed in front of the E…": "当放置在 E 的前面时…",
    "Your first step into magic.": "你迈入魔法的第一步。",
    # Stage labels
    "STAGE 1: PRIMARY MECHANICS (Andesite)": "阶段 1：基础机械（安山岩）",
    "STAGE 1 : PRIMARY MECHANICS (Andesite)": "阶段 1：基础机械（安山岩）",
    "STAGE 2: TRANSFER & LOGISTICS (Iron/Andesite)": "阶段 2：传输与物流（铁/安山岩）",
    "STAGE 2 : TRANSFER & LOGISTICS (Iron/Andesite)": "阶段 2：传输与物流（铁/安山岩）",
    "STAGE 3: HYDRAULICS (Copper)": "阶段 3：液压（铜）",
    "STAGE 3 : HYDRAULICS (Copper)": "阶段 3：液压（铜）",
    "STAGE 3 : HYDRAULIQUE (Cuivre)": "阶段 3：液压（铜）",
    "STAGE 4: PRECISION (Brass)": "阶段 4：精密（黄铜）",
    "STAGE 4 : PRECISION (Brass)": "阶段 4：精密（黄铜）",
    "STAGE 5: ADVANCED (Steel/Industrial Iron)": "阶段 5：高级（钢/工业铁）",
    "STAGE 5 : ADVANCED (Steel/Industrial Iron)": "阶段 5：高级（钢/工业铁）",
    "STAGE 6: AUTOMATION (Train, Schedule, Display)": "阶段 6：自动化（火车、调度、显示器）",
    "STAGE 6 : AUTOMATION (Train, Schedule, Display)": "阶段 6：自动化（火车、调度、显示器）",
    "STAGE 7: DECO & CONSTRUCTION (Style)": "阶段 7：装饰与建造（风格）",
    "STAGE 7 : DECO & CONSTRUCTION (Style)": "阶段 7：装饰与建造（风格）",
    "STAGE 7: DECO & CONSTRUCTION (The Style)": "阶段 7：装饰与建造（风格）",
    "STAGE 8: EQUIPMENT & SPECIAL ADDONS (Slice & Dice, Cardboard...)": "阶段 8：装备与特殊附加（切片切丁、纸板……）",
    "STAGE 8 : EQUIPMENT & SPECIAL ADDONS (Slice & Dice, Cardboard...)": "阶段 8：装备与特殊附加（切片切丁、纸板……）",
    "Reward: +1 XP level.": "奖励：+1 级经验。",
}

# ---------------------------------------------------------------------------
# 2. REGEX PATTERN RULES (templated lines: tooltips, tips, rewards, gear …)
# ---------------------------------------------------------------------------

# These run AFTER the phrase map miss. We compile them in order of priority.
PATTERNS = []


def _p(regex, replacement, flags=0):
    PATTERNS.append((re.compile(regex, flags), replacement))


# &eTip:&r ...
_p(r"^Tip:\s*", "提示：")
_p(r"^Note:\s*", "注意：")
_p(r"^Warning:\s*", "警告：")
_p(r"^Reward:\s*", "奖励：")
_p(r"^Utility:\s*", "实用功能：")
_p(r"^Wrench:\s*", "扳手：")
_p(r"^Goggles:\s*", "护目镜：")
_p(r"^Recipe:\s*", "配方：")
_p(r"^Hint:\s*", "提示：")
_p(r"^Effect:\s*", "效果：")
_p(r"^Stats:\s*", "属性：")
_p(r"^Bonus:\s*", "加成：")
_p(r"^Set Bonus:\s*", "套装加成：")
_p(r"^Requirement:\s*", "需求：")
_p(r"^Objective:\s*", "目标：")
_p(r"^Goal:\s*", "目标：")
_p(r"^Quest:\s*", "任务：")
_p(r"^Rewards:\s*", "奖励：")

# ---------------------------------------------------------------------------
# 3. WORD / SHORT-PHRASE DICTIONARY (applied after phrase map, before
#    any character-by-character fallback). Matched as whole words via regex.
# ---------------------------------------------------------------------------

# Order matters: longer first.
WORD_MAP = {
    # MC vocabulary
    "Spellbook": "法术书",
    "Spellbooks": "法术书",
    "Spell Power": "法术威力",
    "Max Mana": "最大法力",
    "Mana Cost": "法力消耗",
    "Mana Regen": "法力恢复",
    "Casting Time": "施法时间",
    "Spell Scroll": "法术卷轴",
    "Crossbow": "弩",
    "Pickaxe": "镐",
    "Chestplate": "胸甲",
    "Breastplate": "胸甲",
    "Leggings": "护腿",
    "Boots": "靴子",
    "Helmet": "头盔",
    "Shield": "盾牌",
    "Sword": "剑",
    "Axe": "斧",
    "Bow": "弓",
    "Wand": "法杖",
    "Staff": "法杖",
    "Necklace": "项链",
    "Ring": "戒指",
    "Belt": "腰带",
    "Cape": "披风",
    "Cloak": "斗篷",
    "Scarf": "围巾",
    "Robes": "长袍",
    "Robe": "长袍",
    "Hat": "帽子",
    "Pants": "裤子",
    "Slippers": "拖鞋",
    "Curio": "饰品",
    "Trinket": "饰品",
    "Bauble": "小物件",
    "Spell": "法术",
    "Mana": "法力",
    "Dungeon": "地牢",
    "Treasure": "宝藏",
    "Loot": "战利品",
    "Tip": "提示",
    "Warning": "警告",
    "Note": "注意",
    "Boss": "Boss",
    "Reward": "奖励",
    "Rewards": "奖励",
    "Quest": "任务",
    "Quests": "任务",
    "Chapter": "章节",
    "XP level": "经验等级",
    "XP levels": "经验等级",
    "XP": "经验",
    "Holy": "神圣",
    "Undead": "亡灵",
    "school": "学派",

    # Gear types
    "Paladin Chestplate": "圣骑士胸甲",
    "Paladin": "圣骑士",
    "Wizard Set": "巫师套装",
    "Wizard": "巫师",
    "Panic Necklace": "恐慌项链",
    "Cross Necklace": "十字项链",
    "Kitty Slippers": "猫咪拖鞋",
    "Scarf of Invisibility": "隐身围巾",
    "Sun Spirit": "太阳之灵",

    # Verbs / quest-ish
    "Find": "寻找",
    "Craft": "制作",
    "Defeat": "击败",
    "Kill": "击杀",
    "Obtain": "获得",
    "Build": "建造",
    "Collect": "收集",
    "Place": "放置",
    "Use": "使用",
    "Combine": "组合",
    "Equip": "装备",
    "Explore": "探索",

    # Adjectives
    "iconic": "标志性的",
    "signature": "标志性",
    "favorite": "最爱",
    "emergency": "紧急",
    "magical": "魔法",
    "magic": "魔法",
    "heavy": "重型",
    "heavily": "深度地",
    "blessed": "受祝福的",
    "regen": "回复",
    "regeneration": "回复",
    "Regeneration": "回复",
    "Speed": "速度",
    "damage reduction": "伤害减免",
    "spell power": "法术威力",

    # Misc
    "stealth": "潜行",
    "footsteps": "脚步声",
    "drops": "坠落",
    "fall damage": "坠落伤害",
    "short drops": "短距离坠落",
    "ninja mode": "忍者模式",
    "archmage": "大法师",
    "outfit": "套装",
    "robed": "袍状",
    "tank": "坦克",
    "hybrid": "混合",
    "build": "构筑",
    "Build": "构筑",
    "Pair": "搭配",
    "pair": "搭配",
    "Boosts": "增强",
    "boosts": "增强",
    "Grants": "赋予",
    "grants": "赋予",
    "nullifies": "消除",
    "silences": "消除",
    "Lets you": "让你能够",
    "lets you": "让你能够",
    "Displays": "显示",
    "displays": "显示",
    "Rotates": "旋转",
    "rotates": "旋转",
    "dismantles": "拆除",
    "configures": "配置",
    "Empties": "清空",
    "empties": "清空",
    "buckets": "桶",
    "bottles": "瓶子",
    "fluids": "流体",
    "stats": "属性",
    "SU stats": "SU 数据",
    "SEEING IS POWER": "看见即力量",
    "in sunlight": "在阳光下",
    "vs.": "对",
    "vs": "对",
    "Cook": "烹饪",
    "Storage": "储存",
    "ID": "编号",
    "of any aspiring": "任何有抱负的",
    "of any": "任何",
    "An emergency escape charm": "应急逃脱护符",
    "A favorite of stealth players": "潜行玩家的最爱",
    "the iconic outfit": "标志性套装",
    "all four pieces": "全部四件",
    "Pair with": "搭配",
    "to unlock": "以解锁",
}

# Compile word patterns (longest first so substrings don't override).
WORD_PATTERNS = sorted(WORD_MAP.items(), key=lambda kv: -len(kv[0]))
WORD_PATTERNS = [
    (re.compile(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])"), zh)
    for en, zh in WORD_PATTERNS
]

# ---------------------------------------------------------------------------
# 4. Pre-translation: protect color codes (&a, &r, §f …) & format tokens.
# ---------------------------------------------------------------------------

COLOR_RE = re.compile(r"(&[0-9a-fk-orA-FK-OR]|§[0-9a-fk-orA-FK-OR])")
FORMAT_TOKEN_RE = re.compile(r"(\{[^{}]*\}|%[sd]|<[^<>]+>)")


def mask_tokens(text):
    tokens = []

    def repl(m):
        tokens.append(m.group(0))
        return f"\x00{len(tokens) - 1}\x01"

    text = COLOR_RE.sub(repl, text)
    text = FORMAT_TOKEN_RE.sub(repl, text)
    return text, tokens


def unmask_tokens(text, tokens):
    def repl(m):
        idx = int(m.group(1))
        return tokens[idx]

    return re.sub(r"\x00(\d+)\x01", repl, text)


# ---------------------------------------------------------------------------
# 5. Translation pipeline.
# ---------------------------------------------------------------------------

# Punctuation tweaks: turn ASCII punctuation into fullwidth Chinese
PUNCT_MAP = [
    (re.compile(r" ?: "), "："),
    (re.compile(r" — "), " —— "),
    (re.compile(r" - "), " - "),
    (re.compile(r"\.\.\.$"), "……"),
    (re.compile(r"\. "), "。"),
    (re.compile(r", "), "，"),
    (re.compile(r"; "), "；"),
    (re.compile(r"! "), "！"),
    (re.compile(r"\? "), "？"),
    (re.compile(r"\.$"), "。"),
    (re.compile(r"!$"), "！"),
    (re.compile(r"\?$"), "？"),
    (re.compile(r":$"), "："),
]


def apply_punct(text):
    for rx, rep in PUNCT_MAP:
        text = rx.sub(rep, text)
    return text


def looks_chinese(text):
    """True if string already contains CJK characters."""
    return bool(re.search(r"[一-鿿]", text))


def is_pure_format(text):
    """A text composed only of masked tokens/spaces."""
    stripped = re.sub(r"\x00\d+\x01", "", text).strip()
    return stripped == ""


def translate_phrase(text):
    """Try whole-string phrase map first."""
    stripped = text.strip()
    if stripped in PHRASE_MAP:
        # Preserve leading/trailing whitespace
        lead = text[: len(text) - len(text.lstrip())]
        tail = text[len(text.rstrip()):]
        return lead + PHRASE_MAP[stripped] + tail
    return None


def translate_one(text):
    if text is None:
        return text
    if text == "":
        return ""
    if looks_chinese(text):
        return text  # already partially translated/leave alone

    # 1. Mask color codes & format tokens
    masked, tokens = mask_tokens(text)

    if is_pure_format(masked):
        return text

    # 2. Whole-string phrase map (try both raw and masked-then-trimmed)
    phrase_hit = translate_phrase(text)
    if phrase_hit is not None:
        return phrase_hit

    # Also try after color masking removed: re-look up by stripped masked text
    masked_stripped = masked.strip()
    if masked_stripped in PHRASE_MAP:
        lead = masked[: len(masked) - len(masked.lstrip())]
        tail = masked[len(masked.rstrip()):]
        translated = lead + PHRASE_MAP[masked_stripped] + tail
        return unmask_tokens(translated, tokens)

    # 3. Apply pattern rules at the start of the string
    translated = masked
    for rx, rep in PATTERNS:
        translated = rx.sub(rep, translated)

    # 4. Apply word-level dictionary
    for rx, zh in WORD_PATTERNS:
        translated = rx.sub(zh, translated)

    # 5. Punctuation normalisation
    translated = apply_punct(translated)

    # 6. Unmask color codes & tokens
    translated = unmask_tokens(translated, tokens)

    return translated


# ---------------------------------------------------------------------------
# 6. Driver
# ---------------------------------------------------------------------------


def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    out = {}
    untranslated_examples = []
    fully_en_count = 0
    total_strings = 0

    for k, v in data.items():
        if isinstance(v, str):
            translated = translate_one(v)
            out[k] = translated
            total_strings += 1
            # Heuristic: still mostly English letters and no CJK
            if not looks_chinese(translated) and re.search(r"[A-Za-z]{4,}", translated):
                if len(untranslated_examples) < 50:
                    untranslated_examples.append((k, v, translated))
                fully_en_count += 1
        elif isinstance(v, list):
            new_list = []
            for item in v:
                translated = translate_one(item)
                new_list.append(translated)
                total_strings += 1
                if (
                    isinstance(item, str)
                    and item.strip()
                    and not looks_chinese(translated)
                    and re.search(r"[A-Za-z]{4,}", translated)
                ):
                    if len(untranslated_examples) < 50:
                        untranslated_examples.append((k, item, translated))
                    fully_en_count += 1
            out[k] = new_list
        else:
            out[k] = v

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(out)} keys to {OUTPUT}")
    print(f"Total string slots: {total_strings}")
    print(f"Slots still containing >=4-letter English run: {fully_en_count}")
    print("--- untranslated examples ---")
    for k, src, tgt in untranslated_examples[:25]:
        print(k[:60], "|", src[:120])
        print("   ->", tgt[:120])


if __name__ == "__main__":
    main()
