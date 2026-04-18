import zipfile
import os
import json
import sys

MODS_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/mods"
OUT_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/_analysis"
os.makedirs(OUT_DIR, exist_ok=True)

TARGETS = [
    ("aether-1.21.1-1.5.10-neoforge.jar", "aether"),
    ("BetterCopper-neoforge-1.21-1.3.jar", "bettercopper"),
    ("Aquaculture-1.21.1-2.7.19.jar", "aquaculture"),
    ("FarmersDelight-1.21.1-1.2.10.jar", "farmersdelight"),
    ("MyNethersDelight-1.21.1-1.9.jar", "nethersdelight"),
    ("artifacts-neoforge-13.2.1.jar", "artifacts"),
    ("CosmeticWeapons - 1.1.0.1 - 1.21.1 - NeoForge.jar", "cosmeticweapons"),
    ("DnDesires-1.21.1-2.2d-BETA.jar", "dndesires"),
    ("advancednetherite-neoforge-2.3.1-1.21.1.jar", "advancednetherite"),
    ("create_jetpack-forge-5.1.2.jar", "create_jetpack"),
    ("create-stuff-additions1.21.1_v2.1.0e.jar", "create_sa"),
    ("create_things_and_misc-4.1.0-neoforge-1.21.1.jar", "ctam"),
]

for jar, modid in TARGETS:
    path = os.path.join(MODS_DIR, jar)
    if not os.path.exists(path):
        print(f"MISSING: {jar}")
        continue
    out_sub = os.path.join(OUT_DIR, modid)
    os.makedirs(out_sub, exist_ok=True)
    try:
        with zipfile.ZipFile(path) as z:
            # Lang file
            lang_candidates = [n for n in z.namelist() if n.endswith("lang/en_us.json")]
            lang_text = {}
            for lc in lang_candidates:
                try:
                    data = z.read(lc).decode("utf-8")
                    lang_text[lc] = data
                except Exception as e:
                    lang_text[lc] = f"ERR:{e}"
            with open(os.path.join(out_sub, "langs.txt"), "w", encoding="utf-8") as f:
                for k, v in lang_text.items():
                    f.write(f"===== {k} =====\n")
                    f.write(v)
                    f.write("\n\n")

            # Recipe list (first 400 entries)
            recipes = [n for n in z.namelist() if "/recipe/" in n or n.startswith("data/") and "/recipes/" in n]
            with open(os.path.join(out_sub, "recipe_list.txt"), "w", encoding="utf-8") as f:
                for r in recipes[:600]:
                    f.write(r + "\n")

            # Sample up to 25 recipes
            with open(os.path.join(out_sub, "sample_recipes.txt"), "w", encoding="utf-8") as f:
                count = 0
                for r in recipes:
                    if count >= 40:
                        break
                    if not r.endswith(".json"):
                        continue
                    try:
                        txt = z.read(r).decode("utf-8")
                    except Exception:
                        continue
                    f.write(f"===== {r} =====\n")
                    f.write(txt)
                    f.write("\n\n")
                    count += 1

            # Also save item list (just names)
            with open(os.path.join(out_sub, "all_entries.txt"), "w", encoding="utf-8") as f:
                for n in z.namelist():
                    f.write(n + "\n")
        print(f"OK: {jar}")
    except Exception as e:
        print(f"ERR {jar}: {e}")

print("DONE")
