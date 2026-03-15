// Priority: 100

/*
    Hardening Vanilla & Modded recipes for Arcadia V2.
    Author: vyrriox
    
    This script modifies recipes to make them harder/more complex,
    integrating Create materials (Sheets/Plates, Cogwheels) and increasing
    base resource costs.
    
    Optimized & Organized.
*/

ServerEvents.recipes((event) => {
    // --- CONSTANTS ---
    const IRON_SHEET = "create:iron_sheet";
    const GOLD_SHEET = "create:golden_sheet";
    const COPPER_SHEET = "create:copper_sheet";
    const COGWHEEL = "create:cogwheel";
    const REINFORCE_BLOCK = "minecraft:breeze_rod";

    console.info("[Arcadia V2] Loading Harder Recipes Script (Optimized)...");

    // ==========================================
    // 0. BASICS & WOOD
    // ==========================================

    // Sticks (2 Logs -> 4 Sticks)
    event.remove({ output: "minecraft:stick" });
    event.shaped("4x minecraft:stick", ["L", "L"], { L: "#minecraft:logs" });

    // Modded Sticks
    event.remove({ output: "aether:skyroot_stick" });
    event.shaped("4x aether:skyroot_stick", ["L", "L"], {
        L: "#aether:skyroot_logs",
    });

    event.remove({ output: "immersiveengineering:stick_treated" });
    event.shaped(Item.of("immersiveengineering:stick_treated", 2), ["P", "P"], {
        P: "#immersiveengineering:treated_wood",
    });

    // Crafting Table: Requires Leather (Forces hunting)
    event.remove({ output: "minecraft:crafting_table" });
    event.shaped("minecraft:crafting_table", ["PP", "PL"], {
        P: "#minecraft:planks",
        L: "minecraft:leather",
    });

    // Aether Crafting Tables (Logs)
    event.remove({ output: "aether:skyroot_crafting_table" });
    event.remove({ output: "deep_aether:skyroot_crafting_table" });

    // ==========================================
    // 1. TOOLS, WEAPONS & ARMOR
    // ==========================================

    // --- IRON (Uses Iron Sheets) ---
    const ironItems = [
        "minecraft:iron_sword",
        "minecraft:iron_pickaxe",
        "minecraft:iron_axe",
        "minecraft:iron_shovel",
        "minecraft:iron_hoe",
        "minecraft:iron_helmet",
        "minecraft:iron_chestplate",
        "minecraft:iron_leggings",
        "minecraft:iron_boots",
        "cosmeticweaponsmod:iron_battleaxe",
    ];
    ironItems.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:iron_ingot", IRON_SHEET),
    );

    // Create Diesel Generators Hammer (Iron Sheets)
    event.replaceInput(
        { output: "createdieselgenerators:hammer" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // --- GOLD (Uses Gold Sheets) ---
    const goldItems = [
        "minecraft:golden_sword",
        "minecraft:golden_pickaxe",
        "minecraft:golden_axe",
        "minecraft:golden_shovel",
        "minecraft:golden_hoe",
        "minecraft:golden_helmet",
        "minecraft:golden_chestplate",
        "minecraft:golden_leggings",
        "minecraft:golden_boots",
        "cosmeticweaponsmod:golden_battleaxe",
    ];
    goldItems.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:gold_ingot", GOLD_SHEET),
    );

    // --- DIAMOND (Reinforced with Breeze Rod) ---
    const diamondItems = [
        "minecraft:diamond_sword",
        "minecraft:diamond_pickaxe",
        "minecraft:diamond_axe",
        "minecraft:diamond_shovel",
        "minecraft:diamond_hoe",
        "minecraft:diamond_helmet",
        "minecraft:diamond_chestplate",
        "minecraft:diamond_leggings",
        "minecraft:diamond_boots",
        "cosmeticweaponsmod:diamond_battleaxe",
    ];
    diamondItems.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:stick", REINFORCE_BLOCK),
    );

    // --- STONE (Requires Stone instead of Cobblestone) ---
    const stoneItems = [
        "minecraft:stone_sword",
        "minecraft:stone_pickaxe",
        "minecraft:stone_axe",
        "minecraft:stone_shovel",
        "minecraft:stone_hoe",
        "cosmeticweaponsmod:stone_battleaxe",
    ];
    stoneItems.forEach((item) =>
        event.replaceInput(
            { output: item },
            "minecraft:cobblestone",
            "minecraft:stone",
        ),
    );

    // --- LEATHER (Adds String) ---
    const leatherItems = [
        "minecraft:leather_helmet",
        "minecraft:leather_chestplate",
        "minecraft:leather_leggings",
        "minecraft:leather_boots",
    ];
    leatherItems.forEach((item) => event.remove({ output: item }));

    event.shaped("minecraft:leather_helmet", ["LLL", "L L", "S S"], {
        L: "minecraft:leather",
        S: "minecraft:string",
    });
    event.shaped("minecraft:leather_chestplate", ["L L", "LLL", "SSS"], {
        L: "minecraft:leather",
        S: "minecraft:string",
    });
    event.shaped("minecraft:leather_leggings", ["LLL", "L L", "S S"], {
        L: "minecraft:leather",
        S: "minecraft:string",
    });
    event.shaped("minecraft:leather_boots", ["L L", "S S"], {
        L: "minecraft:leather",
        S: "minecraft:string",
    });

    // --- NETHERITE INGOT (Sequenced Assembly) ---
    event.remove({ output: "minecraft:netherite_ingot" });
    // Process: Scrap (+1 Scrap, +2 Gold Sheets) x3 -> Press
    // 80% Success (Ingot), 20% Failure (Scrap Refund)
    event.recipes.create
        .sequenced_assembly(
            [
                CreateItem.of("minecraft:netherite_ingot", 0.8),
                CreateItem.of("minecraft:netherite_scrap", 0.2),
            ],
            "minecraft:netherite_scrap",
            [
                event.recipes.createDeploying("minecraft:netherite_scrap", [
                    "minecraft:netherite_scrap",
                    "minecraft:netherite_scrap",
                ]),
                event.recipes.createDeploying("minecraft:netherite_scrap", [
                    "minecraft:netherite_scrap",
                    GOLD_SHEET,
                ]),
                event.recipes.createDeploying("minecraft:netherite_scrap", [
                    "minecraft:netherite_scrap",
                    GOLD_SHEET,
                ]),
                event.recipes.createPressing(
                    "minecraft:netherite_scrap",
                    "minecraft:netherite_scrap",
                ),
            ],
        )
        .transitionalItem("minecraft:netherite_scrap")
        .loops(3);

    // ==========================================
    // 2. STORAGE
    // ==========================================

    // Chest (Logs)
    event.remove({ output: "minecraft:chest" });
    event.shaped("minecraft:chest", ["LLL", "L L", "LLL"], {
        L: "#minecraft:logs",
    });

    // Barrel (Iron Nuggets)
    event.replaceInput(
        { output: "minecraft:barrel" },
        "#minecraft:wooden_slabs",
        "minecraft:iron_nugget",
    );

    // Ender Chest (Gold Sheets)
    event.shaped("minecraft:ender_chest", ["POP", "OEO", "POP"], {
        P: GOLD_SHEET,
        O: "minecraft:obsidian",
        E: "minecraft:ender_eye",
    });

    // Storage Blocks (Factorization via Mixer)
    const storageBlocks = [
        // Vanilla
        { block: "minecraft:iron_block", input: "minecraft:iron_ingot" },
        { block: "minecraft:gold_block", input: "minecraft:gold_ingot" },
        { block: "minecraft:diamond_block", input: "minecraft:diamond" },
        { block: "minecraft:emerald_block", input: "minecraft:emerald" },
        { block: "minecraft:redstone_block", input: "minecraft:redstone" },
        { block: "minecraft:lapis_block", input: "minecraft:lapis_lazuli" },
        { block: "minecraft:netherite_block", input: "minecraft:netherite_ingot" },
        // Mekanism
        { block: "mekanism:block_tin", input: "mekanism:ingot_tin" },
        { block: "mekanism:block_uranium", input: "mekanism:ingot_uranium" },
        { block: "mekanism:block_lead", input: "mekanism:ingot_lead" },
        { block: "mekanism:block_osmium", input: "mekanism:ingot_osmium" },
        {
            block: "mekanism:block_refined_glowstone",
            input: "mekanism:ingot_refined_glowstone",
        },
        {
            block: "mekanism:block_refined_obsidian",
            input: "mekanism:ingot_refined_obsidian",
        },
        { block: "mekanism:block_steel", input: "mekanism:ingot_steel" },
        { block: "mekanism:block_bronze", input: "mekanism:ingot_bronze" },
        // Immersive Engineering
        {
            block: "immersiveengineering:storage_constantan",
            input: "immersiveengineering:ingot_constantan",
        },
        {
            block: "immersiveengineering:storage_uranium",
            input: "immersiveengineering:ingot_uranium",
        },
        {
            block: "immersiveengineering:storage_nickel",
            input: "immersiveengineering:ingot_nickel",
        },
        {
            block: "immersiveengineering:storage_lead",
            input: "immersiveengineering:ingot_lead",
        },
        {
            block: "immersiveengineering:storage_aluminum",
            input: "immersiveengineering:ingot_aluminum",
        },
        {
            block: "immersiveengineering:storage_silver",
            input: "immersiveengineering:ingot_silver",
        },
        {
            block: "immersiveengineering:storage_steel",
            input: "immersiveengineering:ingot_steel",
        },
        {
            block: "immersiveengineering:storage_electrum",
            input: "immersiveengineering:ingot_electrum",
        },
        // Create Nuclear
        { block: "createnuclear:steel_block", input: "createnuclear:steel_ingot" },
        { block: "createnuclear:lead_block", input: "createnuclear:lead_ingot" },
        // Aquaculture
        {
            block: "aquaculture:neptunium_block",
            input: "aquaculture:neptunium_ingot",
        },
    ];

    storageBlocks.forEach((recipe) => {
        event.remove({ output: recipe.block });
        // Mixer Recipe: 9 Ingots + 1 Alloy + 500mb Lava --> 1 Block (No Heat)
        event.recipes.create.mixing(recipe.block, [
            `9x ${recipe.input}`,
            `1x create:andesite_alloy`,
            Fluid.of("minecraft:lava", 500),
        ]);
    });

    // ==========================================
    // 3. WORKSTATIONS
    // ==========================================

    // Furnace (8 Cobbles + Campfire)
    event.remove({ output: "minecraft:furnace" });
    event.shaped("minecraft:furnace", ["CCC", "CFC", "CCC"], {
        C: "minecraft:cobblestone",
        F: "minecraft:campfire",
    });

    // Smoker (6 Logs)
    event.remove({ output: "minecraft:smoker" });
    event
        .shaped("minecraft:smoker", ["L L", "LFL", "L L"], {
            F: "minecraft:furnace",
            L: "#minecraft:logs",
        })
        .id("minecraft:smoker");

    // Blast Furnace (Iron Sheets)
    event.replaceInput(
        { output: "minecraft:blast_furnace" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Anvil (Iron Sheets)
    event.replaceInput(
        { output: "minecraft:anvil" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Smithing Table (Iron Sheets)
    event.replaceInput(
        { output: "minecraft:smithing_table" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );
    event.replaceInput(
        { output: "minecraft:smithing_table" },
        "#minecraft:planks",
        "#minecraft:logs",
    );

    // Grindstone (Cogwheels)
    event.remove({ output: "minecraft:grindstone" });
    event.shaped("minecraft:grindstone", ["RSR", "L L"], {
        S: "minecraft:stone_slab",
        R: COGWHEEL,
        L: "#minecraft:logs",
    });

    // Stonecutter (Iron Sheet)
    event.replaceInput(
        { output: "minecraft:stonecutter" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Cauldron (Iron Sheets)
    event.replaceInput(
        { output: "minecraft:cauldron" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Brewing Stand (Copper Sheets)
    event.replaceInput(
        { output: "minecraft:brewing_stand" },
        "minecraft:cobblestone",
        COPPER_SHEET,
    );

    // Enchanting Table (Red Wool + Diamonds moved)
    event.remove({ output: "minecraft:enchanting_table" });
    event.shaped("minecraft:enchanting_table", [" B ", "WOW", "DOD"], {
        B: "minecraft:book",
        W: "minecraft:red_wool",
        O: "minecraft:obsidian",
        D: "minecraft:diamond",
    });

    // Cartography Table (Compass)
    event.remove({ output: "minecraft:cartography_table" });
    event.shaped("minecraft:cartography_table", ["CP", "LL"], {
        C: "minecraft:compass",
        P: "minecraft:paper",
        L: "#minecraft:logs",
    });

    // Fletching Table (Feather)
    event.remove({ output: "minecraft:fletching_table" });
    event.shaped("minecraft:fletching_table", ["FI", "LL"], {
        F: "minecraft:flint",
        I: "minecraft:feather",
        L: "#minecraft:logs",
    });

    // Inscription Table (Irons Spellbooks) - Gold Sheets
    event.remove({ output: "irons_spellbooks:inscription_table" });
    event.shaped("irons_spellbooks:inscription_table", [" B ", "POP", "O O"], {
        B: "minecraft:book",
        P: GOLD_SHEET,
        O: "minecraft:obsidian",
    });

    // Create Schematicannon
    event.remove({ output: "create:schematicannon" });
    event.shaped("create:schematicannon", [" I ", "LDL", "SCS"], {
        I: IRON_SHEET,
        L: "#minecraft:logs",
        D: "minecraft:dispenser",
        S: "minecraft:smooth_stone",
        C: COGWHEEL,
    });

    // Create Mechanical Arm (Added Transistor + Fixed Ingredients)
    event.remove({ output: "create:mechanical_arm" });
    event.shaped("create:mechanical_arm", ["BBA", "BPT", " C "], {
        B: "create:brass_sheet",
        A: "create:andesite_alloy",
        P: "create:precision_mechanism",
        C: "create:brass_casing",
        T: "tfmg:transistor_item",
    });

    // Create Rotation Speed Controller (Added Transistor + Complex Ingredients)
    event.remove({ output: "create:rotation_speed_controller" });
    event.shaped("create:rotation_speed_controller", [" P ", "TCT", " G "], {
        P: "create:precision_mechanism",
        T: "tfmg:transistor_item",
        C: "create:brass_casing",
        G: "create:large_cogwheel",
    });

    // Create Electric Motor (Complex: Transistor, Converter, Spool, Capacitor)
    event.remove({ output: "createaddition:electric_motor" });
    event.recipes.create.mechanical_crafting("createaddition:electric_motor", [
        " SVS ",
        "T B T",
        "W R W",
        " C C "
    ], {
        S: "create:brass_sheet",
        V: "tfmg:converter",
        T: "tfmg:transistor_item",
        B: "create:brass_casing",
        W: "createaddition:copper_spool",
        R: "createaddition:iron_rod",
        C: "createaddition:capacitor"
    });

    // Apotheosis Tables
    event.remove({ output: "apotheosis:reforging_table" });
    event.shaped("apotheosis:reforging_table", ["NDN", "DSD", "PPP"], {
        N: "minecraft:netherite_scrap",
        D: "minecraft:diamond_block",
        S: "apotheosis:simple_reforging_table",
        P: GOLD_SHEET,
    });

    event.remove({ output: "apotheosis:simple_reforging_table" });
    event.shaped("apotheosis:simple_reforging_table", [" I ", "IAI", "PPP"], {
        I: IRON_SHEET,
        A: "minecraft:anvil",
        P: "minecraft:smooth_stone",
    });

    event.remove({ output: "apotheosis:salvaging_table" });
    event.shaped("apotheosis:salvaging_table", ["III", "LST", "PPP"], {
        I: IRON_SHEET,
        L: "minecraft:lava_bucket",
        S: "minecraft:smithing_table",
        T: "minecraft:iron_pickaxe",
        P: REINFORCE_BLOCK,
    });

    event.remove({ output: "apotheosis:gem_cutting_table" });
    event.shaped("apotheosis:gem_cutting_table", [" S ", "CAC", "PPP"], {
        S: "minecraft:shears",
        C: "minecraft:amethyst_shard",
        A: "minecraft:stonecutter",
        P: "#minecraft:planks",
    });

    // ==========================================
    // 4. DECORATION & UTILITIES
    // ==========================================

    // Beds (Logs)
    const bedColors = [
        "white",
        "orange",
        "magenta",
        "light_blue",
        "yellow",
        "lime",
        "pink",
        "gray",
        "light_gray",
        "cyan",
        "purple",
        "blue",
        "brown",
        "green",
        "red",
        "black",
    ];
    bedColors.forEach((color) => {
        let bedId = `minecraft:${color}_bed`;
        event.replaceInput(
            { output: bedId },
            "#minecraft:planks",
            "#minecraft:logs",
        );
    });

    // Lanterns (Iron Sheets)
    event.remove({ output: "minecraft:lantern" });
    event.shaped("minecraft:lantern", [" P ", " T ", " P "], {
        P: IRON_SHEET,
        T: "minecraft:torch",
    });
    event.remove({ output: "minecraft:soul_lantern" });
    event.shaped("minecraft:soul_lantern", [" P ", " T ", " P "], {
        P: IRON_SHEET,
        T: "minecraft:soul_torch",
    });

    // Torches (Yield Nerf: 2x)
    event.remove({ output: "minecraft:torch" });
    event.shaped("2x minecraft:torch", ["C", "S"], {
        C: "minecraft:coal",
        S: "minecraft:stick",
    });
    event.shaped("2x minecraft:torch", ["C", "S"], {
        C: "minecraft:charcoal",
        S: "minecraft:stick",
    });

    event.remove({ output: "minecraft:soul_torch" });
    event.shaped("2x minecraft:soul_torch", ["C", "S", "O"], {
        C: "minecraft:coal",
        S: "minecraft:stick",
        O: "minecraft:soul_soil",
    });
    event.shaped("2x minecraft:soul_torch", ["C", "S", "O"], {
        C: "minecraft:charcoal",
        S: "minecraft:stick",
        O: "minecraft:soul_soil",
    });
    event.shaped("2x minecraft:soul_torch", ["C", "S", "O"], {
        C: "minecraft:coal",
        S: "minecraft:stick",
        O: "minecraft:soul_sand",
    });
    event.shaped("2x minecraft:soul_torch", ["C", "S", "O"], {
        C: "minecraft:charcoal",
        S: "minecraft:stick",
        O: "minecraft:soul_sand",
    });

    event.remove({ output: "minecraft:redstone_torch" });
    event.shaped("minecraft:redstone_torch", ["R", "S"], {
        R: "minecraft:redstone",
        S: "minecraft:stick",
    });

    event.remove({ output: "framedblocks:framed_torch" });
    event.shaped("2x framedblocks:framed_torch", ["C", "F"], {
        C: "minecraft:coal",
        F: "framedblocks:framed_cube",
    });

    // Bucket (Iron Sheets)
    event.replaceInput(
        { output: "minecraft:bucket" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Shears (Iron Sheet + Stick)
    event.remove({ output: "minecraft:shears" });
    event.shaped("minecraft:shears", [" P", "S "], {
        P: IRON_SHEET,
        S: "minecraft:stick",
    });

    // Compass (Iron Sheets + Gold Nugget)
    event.remove({ output: "minecraft:compass" });
    event.shaped("minecraft:compass", [" P ", "PRP", " N "], {
        P: IRON_SHEET,
        R: "minecraft:redstone",
        N: "minecraft:gold_nugget",
    });

    // Book (String)
    event.remove({ output: "minecraft:book" });
    event.shapeless("minecraft:book", [
        "minecraft:paper",
        "minecraft:paper",
        "minecraft:paper",
        "minecraft:leather",
        "minecraft:string",
    ]);

    // Clock (Gold Sheets)
    event.replaceInput(
        { output: "minecraft:clock" },
        "minecraft:gold_ingot",
        GOLD_SHEET,
    );

    // Fishing Rod (Fishing Line - Aquaculture)
    event.remove({ output: "minecraft:fishing_rod" });
    event.shaped("minecraft:fishing_rod", ["  S", " SF", "S N"], {
        S: "minecraft:stick",
        F: "minecraft:string",
        N: "aquaculture:fishing_line",
    });

    // Lead (Iron Nugget)
    event.remove({ output: "minecraft:lead" });
    event.shaped("2x minecraft:lead", ["SS ", "SN ", "  S"], {
        S: "minecraft:string",
        N: "minecraft:iron_nugget",
    });

    // Saddle (Iron Sheets) - Remove Aether
    event.remove({ mod: "aether", output: "minecraft:saddle" });
    event.remove({ mod: "aether", output: "aether:saddle" });
    event.shaped("minecraft:saddle", ["LLL", "S S", "P P"], {
        L: "minecraft:leather",
        S: "minecraft:string",
        P: IRON_SHEET,
    });

    // Ladder (Zipline Rope)
    event.remove({ output: "minecraft:ladder" });
    event.shaped("3x minecraft:ladder", ["S S", "SFS", "S S"], {
        S: "minecraft:stick",
        F: "parcool:zipline_rope",
    });

    // Framed Ladder (Framed Cube)
    event.remove({ output: "framedblocks:framed_ladder" });
    event.shaped("3x framedblocks:framed_ladder", ["S S", "SBS", "S S"], {
        S: "minecraft:stick",
        B: "framedblocks:framed_cube",
    });

    // Item Frame (Iron Nugget)
    event.remove({ output: "minecraft:item_frame" });
    event.shaped("minecraft:item_frame", ["SNS", "SLS", "SSS"], {
        S: "minecraft:stick",
        N: "minecraft:iron_nugget",
        L: "minecraft:leather",
    });

    // Painting (Paper)
    event.remove({ output: "minecraft:painting" });
    event.shaped("minecraft:painting", ["SSS", "PWP", "SSS"], {
        S: "minecraft:stick",
        W: "#minecraft:wool",
        P: "minecraft:paper",
    });

    // Golden Foods (Gold Sheets)
    event.replaceInput(
        { output: "minecraft:golden_apple" },
        "minecraft:gold_ingot",
        GOLD_SHEET,
    );

    event.remove({ output: "minecraft:golden_carrot" });
    event.shaped("minecraft:golden_carrot", [" P ", "PCP", " P "], {
        P: GOLD_SHEET,
        C: "minecraft:carrot",
    });

    // Lightning Rod (Copper Sheets)
    event.replaceInput(
        { output: "minecraft:lightning_rod" },
        "minecraft:copper_ingot",
        COPPER_SHEET,
    );

    // Spyglass (Copper Sheets)
    event.replaceInput(
        { output: "minecraft:spyglass" },
        "minecraft:copper_ingot",
        COPPER_SHEET,
    );

    // Chain (Iron Sheet + Nugget)
    event.replaceInput(
        { output: "minecraft:chain" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Flint and Steel (Iron Sheet)
    event.replaceInput(
        { output: "minecraft:flint_and_steel" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Blaze Powder (4x Pepper Powder)
    event.remove({ output: "minecraft:blaze_powder" });
    event.shapeless("minecraft:blaze_powder", [
        "mynethersdelight:pepper_powder",
        "mynethersdelight:pepper_powder",
        "mynethersdelight:pepper_powder",
        "mynethersdelight:pepper_powder",
    ]);

    // Daylight Detector (Gold Sheets)
    event.replaceInput(
        { output: "minecraft:daylight_detector" },
        "minecraft:quartz",
        GOLD_SHEET,
    );

    // ==========================================
    // 5. REDSTONE, LOGIC & TRANSPORT
    // ==========================================

    // Piston (Iron Sheet + Cogwheel)
    event.remove({ output: "minecraft:piston" });
    event.shaped("minecraft:piston", ["WWW", "CPC", "RGR"], {
        W: "#minecraft:planks",
        C: "minecraft:cobblestone",
        P: IRON_SHEET,
        R: "minecraft:redstone",
        G: COGWHEEL,
    });

    // Hopper (Iron Sheet + Chest)
    event.replaceInput(
        { output: "minecraft:hopper" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Dispenser (Cogwheel)
    event.remove({ output: "minecraft:dispenser" });
    event.shaped("minecraft:dispenser", ["CCC", "CBC", "RGR"], {
        C: "minecraft:cobblestone",
        B: "minecraft:bow",
        R: "minecraft:redstone",
        G: COGWHEEL,
    });

    // Dropper (Cogwheel)
    event.remove({ output: "minecraft:dropper" });
    event.shaped("minecraft:dropper", ["CCC", "C C", "RGR"], {
        C: "minecraft:cobblestone",
        R: "minecraft:redstone",
        G: COGWHEEL,
    });

    // Observer (Smooth Stone)
    event.replaceInput(
        { output: "minecraft:observer" },
        "minecraft:cobblestone",
        "minecraft:smooth_stone",
    );

    // Repeater (Gold Nugget)
    event.remove({ output: "minecraft:repeater" });
    event.shaped("minecraft:repeater", ["TNT", "SSS"], {
        T: "minecraft:redstone_torch",
        N: "minecraft:gold_nugget",
        S: "minecraft:stone",
    });

    // Comparator (Gold Sheet)
    event.remove({ output: "minecraft:comparator" });
    event.shaped("minecraft:comparator", [" T ", "TQT", "SPS"], {
        T: "minecraft:redstone_torch",
        Q: "minecraft:quartz",
        S: "minecraft:stone",
        P: GOLD_SHEET,
    });

    // Lever (Stone)
    event.replaceInput(
        { output: "minecraft:lever" },
        "minecraft:cobblestone",
        "minecraft:stone",
    );

    // Jukebox (Logs + Cogwheel)
    event.remove({ output: "minecraft:jukebox" });
    event.shaped("minecraft:jukebox", ["LRL", "LDL", "LRL"], {
        L: "#minecraft:logs",
        D: "minecraft:diamond",
        R: COGWHEEL,
    });

    // Note Block (Logs)
    event.replaceInput(
        { output: "minecraft:note_block" },
        "#minecraft:planks",
        "#minecraft:logs",
    );

    // Bell (Gold Sheets)
    event.remove({ output: "minecraft:bell" });
    event.shaped("minecraft:bell", ["PSP", " S ", " S "], {
        P: GOLD_SHEET,
        S: "minecraft:stone",
    });

    // Pressure Plates (Wooden/Iron/Gold)
    const woodTypes = [
        "oak",
        "spruce",
        "birch",
        "jungle",
        "acacia",
        "dark_oak",
        "mangrove",
        "cherry",
        "bamboo",
    ];
    woodTypes.forEach((type) => {
        let log = `#minecraft:${type}_logs`;
        if (type === "bamboo") log = "minecraft:bamboo_block";

        let pplate = `minecraft:${type}_pressure_plate`;
        event.remove({ output: pplate });
        event.shaped(pplate, ["LL"], { L: log });
    });

    // Weighted Pressure Plates
    event.remove({ output: "minecraft:heavy_weighted_pressure_plate" });
    event.shaped("minecraft:heavy_weighted_pressure_plate", ["PP"], {
        P: IRON_SHEET,
    });
    event.remove({ output: "minecraft:light_weighted_pressure_plate" });
    event.shaped("minecraft:light_weighted_pressure_plate", ["PP"], {
        P: GOLD_SHEET,
    });

    // Minecart (Iron Sheets + Cogwheel)
    event.remove({ output: "minecraft:minecart" });
    event.shaped("minecraft:minecart", ["P P", "PGP"], {
        P: IRON_SHEET,
        G: COGWHEEL,
    });

    // Rails (Iron / Gold Sheets)
    event.replaceInput(
        { output: "minecraft:rail" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );
    event.replaceInput(
        { output: "minecraft:powered_rail" },
        "minecraft:gold_ingot",
        GOLD_SHEET,
    );
    event.replaceInput(
        { output: "minecraft:detector_rail" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );
    event.replaceInput(
        { output: "minecraft:activator_rail" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // Boats (Shovel + Planks)
    const boatTypes = [
        "oak",
        "spruce",
        "birch",
        "jungle",
        "acacia",
        "dark_oak",
        "mangrove",
        "cherry",
        "bamboo",
    ];
    boatTypes.forEach((type) => {
        let boatId = `minecraft:${type}_boat`;
        let plankId = `minecraft:${type}_planks`;
        if (type === "bamboo") {
            boatId = "minecraft:bamboo_raft";
            plankId = "minecraft:bamboo_planks";
        }
        event.remove({ output: boatId });
        event.shaped(boatId, ["P P", "PSP"], {
            P: plankId,
            S: "minecraft:wooden_shovel",
        });
    });

    // ==========================================
    // 6. COMBAT & EXPLOSIVES
    // ==========================================

    // TNT (String)
    event.remove({ output: "minecraft:tnt" });
    event.shaped("minecraft:tnt", ["GSG", "SFS", "GSG"], {
        G: "minecraft:gunpowder",
        S: "minecraft:sand",
        F: "minecraft:string",
    });

    // Bow (Leather)
    event.remove({ output: "minecraft:bow" });
    event.shaped("minecraft:bow", [" SC", "L C", " SC"], {
        S: "minecraft:stick",
        C: "minecraft:string",
        L: "minecraft:leather",
    });

    // Crossbow (Iron Sheet + Cogwheel)
    event.remove({ output: "minecraft:crossbow" });
    event.shaped("minecraft:crossbow", ["SIS", "CWC", " L "], {
        S: "minecraft:stick",
        I: IRON_SHEET,
        C: "minecraft:string",
        W: COGWHEEL,
        L: "#minecraft:logs",
    });

    // Shield (Iron Sheet)
    event.replaceInput(
        { output: "minecraft:shield" },
        "minecraft:iron_ingot",
        IRON_SHEET,
    );

    // ==========================================
    // 7. MOD COMPATIBILITY
    // ==========================================

    // Aether Gloves
    event.remove({ output: "aether:leather_gloves" });
    event.shaped("aether:leather_gloves", ["LL", "SS"], {
        L: "minecraft:leather",
        S: "minecraft:string",
    });
    event.remove({ output: "aether:iron_gloves" });
    event.shaped("aether:iron_gloves", ["PP", "PP"], { P: IRON_SHEET });
    event.remove({ output: "aether:golden_gloves" });
    event.shaped("aether:golden_gloves", ["PP", "PP"], { P: GOLD_SHEET });
    event.remove({ output: "aether:diamond_gloves" });
    event.shaped("aether:diamond_gloves", ["DD", "OO"], {
        D: "minecraft:diamond",
        O: REINFORCE_BLOCK,
    });
    event.remove({ output: "aether:netherite_gloves" });
    event.smithing(
        "aether:netherite_gloves",
        "minecraft:netherite_upgrade_smithing_template",
        "aether:diamond_gloves",
        "minecraft:netherite_ingot",
    );

    // Better Copper (Copper Sheets)
    const copperGear = [
        "bettercopper:copper_sword",
        "bettercopper:copper_axe",
        "bettercopper:copper_helmet",
        "bettercopper:copper_chestplate",
        "bettercopper:copper_leggings",
        "bettercopper:copper_boots",
        "bettercopper:copper_pickaxe",
        "bettercopper:copper_shovel",
        "bettercopper:copper_hoe",
    ];
    copperGear.forEach((item) => event.remove({ output: item }));
    event.shaped("bettercopper:copper_sword", ["C", "C", "S"], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_axe", ["CC", "CS", " S"], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_pickaxe", ["CCC", " S ", " S "], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_shovel", ["C", "S", "S"], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_hoe", ["CC", " S", " S"], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_helmet", ["CCC", "C C"], {
        C: COPPER_SHEET,
    });
    event.shaped("bettercopper:copper_chestplate", ["C C", "CCC", "CCC"], {
        C: COPPER_SHEET,
    });
    event.shaped("bettercopper:copper_leggings", ["CCC", "C C", "C C"], {
        C: COPPER_SHEET,
    });
    event.shaped("bettercopper:copper_boots", ["C C", "C C"], {
        C: COPPER_SHEET,
    });

    // Mekanism (Lapis Tools)
    event.remove({ output: "mekanismtools:lapis_lazuli_sword" });
    event.shaped("mekanismtools:lapis_lazuli_sword", ["L", "L", "S"], {
        L: "minecraft:lapis_lazuli",
        S: "minecraft:stick",
    });

    event.remove({ output: "mekanismtools:lapis_lazuli_shield" });
    event.shaped("mekanismtools:lapis_lazuli_shield", ["LIL", "LPL", " L "], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
        P: "#minecraft:planks",
    });

    const lapisArmor = [
        "mekanismtools:lapis_lazuli_helmet",
        "mekanismtools:lapis_lazuli_chestplate",
        "mekanismtools:lapis_lazuli_leggings",
        "mekanismtools:lapis_lazuli_boots",
    ];
    lapisArmor.forEach((item) => event.remove({ output: item }));
    event.shaped("mekanismtools:lapis_lazuli_helmet", ["LIL", "L L"], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
    });
    event.shaped("mekanismtools:lapis_lazuli_chestplate", ["I I", "LIL", "LLL"], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
    });
    event.shaped("mekanismtools:lapis_lazuli_leggings", ["LIL", "L L", "L L"], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
    });
    event.shaped("mekanismtools:lapis_lazuli_boots", ["I I", "L L"], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
    });

    // Mekanism Steel (Iron Sheets replacement)
    const mekanismSteel = [
        "mekanismtools:steel_pickaxe",
        "mekanismtools:steel_axe",
        "mekanismtools:steel_shovel",
        "mekanismtools:steel_hoe",
        "mekanismtools:steel_sword",
        "mekanismtools:steel_paxel",
    ];
    mekanismSteel.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:iron_ingot", IRON_SHEET),
    );

    // Create Whisk
    event.remove({ output: "create:whisk" });
    event.shaped("create:whisk", [" A ", "BAB", "BBB"], {
        A: "create:andesite_alloy",
        B: "minecraft:iron_bars",
    });

    // Create SA (Copper Sheets)
    const createSaCopper = [
        "create_sa:copper_helmet",
        "create_sa:copper_chestplate",
        "create_sa:copper_leggings",
        "create_sa:copper_boots",
        "create_sa:copper_pickaxe",
        "create_sa:copper_axe",
        "create_sa:copper_sword",
        "create_sa:copper_shovel",
        "create_sa:copper_hoe",
        "create_sa:copper_jetpack_chestplate",
        "create_sa:copper_exoskeleton_chestplate",
    ];
    createSaCopper.forEach((item) => {
        event.replaceInput(
            { output: item },
            "minecraft:copper_ingot",
            COPPER_SHEET,
        );
        event.replaceInput({ output: item }, "#forge:ingots/copper", COPPER_SHEET);
    });

    // Simply Swords
    const simplyIronWeapons = [
        "simplyswords:iron_claymore",
        "simplyswords:iron_greathammer",
        "simplyswords:iron_halberd",
        "simplyswords:iron_spear",
        "simplyswords:iron_glaive",
        "simplyswords:iron_warglaive",
        "simplyswords:iron_cutlass",
        "simplyswords:iron_sai",
        "simplyswords:iron_longsword",
        "simplyswords:iron_twinblade",
        "simplyswords:iron_rapier",
        "simplyswords:iron_katana",
        "simplyswords:iron_scythe",
        "simplyswords:iron_chakram",
        "simplyswords:iron_greataxe",
    ];
    simplyIronWeapons.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:iron_ingot", IRON_SHEET),
    );

    const simplyGoldWeapons = [
        "simplyswords:gold_claymore",
        "simplyswords:gold_greathammer",
        "simplyswords:gold_halberd",
        "simplyswords:gold_spear",
        "simplyswords:gold_glaive",
        "simplyswords:gold_warglaive",
        "simplyswords:gold_cutlass",
        "simplyswords:gold_sai",
        "simplyswords:gold_longsword",
        "simplyswords:gold_twinblade",
        "simplyswords:gold_rapier",
        "simplyswords:gold_katana",
        "simplyswords:gold_scythe",
        "simplyswords:gold_chakram",
        "simplyswords:gold_greataxe",
    ];
    simplyGoldWeapons.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:gold_ingot", GOLD_SHEET),
    );

    const simplyDiamondWeapons = [
        "simplyswords:diamond_claymore",
        "simplyswords:diamond_greathammer",
        "simplyswords:diamond_halberd",
        "simplyswords:diamond_spear",
        "simplyswords:diamond_glaive",
        "simplyswords:diamond_warglaive",
        "simplyswords:diamond_cutlass",
        "simplyswords:diamond_sai",
        "simplyswords:diamond_longsword",
        "simplyswords:diamond_twinblade",
        "simplyswords:diamond_rapier",
        "simplyswords:diamond_katana",
        "simplyswords:diamond_scythe",
        "simplyswords:diamond_chakram",
        "simplyswords:diamond_greataxe",
    ];
    simplyDiamondWeapons.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:stick", REINFORCE_BLOCK),
    );

    // Misc Items (Knives, etc.)
    const ironMisc = [
        "aquaculture:iron_fillet_knife",
        "aquaculture:iron_fishing_rod",
        "farmersdelight:iron_knife",
        "cosmeticweaponsmod:iron_knife",
    ];
    ironMisc.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:iron_ingot", IRON_SHEET),
    );

    const goldMisc = [
        "aquaculture:gold_fillet_knife",
        "aquaculture:gold_fishing_rod",
        "farmersdelight:golden_knife",
        "cosmeticweaponsmod:golden_knife",
    ];
    goldMisc.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:gold_ingot", GOLD_SHEET),
    );

    const diamondMisc = [
        "aquaculture:diamond_fillet_knife",
        "aquaculture:diamond_fishing_rod",
        "farmersdelight:diamond_knife",
        "cosmeticweaponsmod:diamond_knife",
    ];
    diamondMisc.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:stick", REINFORCE_BLOCK),
    );

    const copperMisc = ["create_things_and_misc:copper_knife"];
    copperMisc.forEach((item) => {
        event.replaceInput(
            { output: item },
            "minecraft:copper_ingot",
            COPPER_SHEET,
        );
        event.replaceInput({ output: item }, "#forge:ingots/copper", COPPER_SHEET);
    });

    const stoneMisc = [
        "aquaculture:stone_fillet_knife",
        "cosmeticweaponsmod:stone_knife",
    ];
    stoneMisc.forEach((item) =>
        event.replaceInput(
            { output: item },
            "minecraft:cobblestone",
            "minecraft:stone",
        ),
    );

    const woodMisc = [
        "aquaculture:wooden_fillet_knife",
        "cosmeticweaponsmod:wooden_knife",
    ];
    woodMisc.forEach((item) =>
        event.replaceInput(
            { output: item },
            "#minecraft:planks",
            "#minecraft:logs",
        ),
    );

    // DnDesires Gold Whisk
    event.replaceInput(
        { output: "dndesires:gold_whisk" },
        "minecraft:gold_ingot",
        "supplementaries:gold_gate",
    );
    event.replaceInput(
        { output: "dndesires:gold_whisk" },
        "#forge:plates/gold",
        "supplementaries:gold_gate",
    );
    event.replaceInput(
        { output: "dndesires:gold_whisk" },
        "create:golden_sheet",
        "supplementaries:gold_gate",
    );

    // Advanced Netherite (Mixer Recipes)
    const advNetherite = [
        "advancednetherite:netherite_iron_ingot",
        "advancednetherite:netherite_gold_ingot",
        "advancednetherite:netherite_emerald_ingot",
        "advancednetherite:netherite_diamond_ingot",
    ];
    advNetherite.forEach((item) => event.remove({ output: item }));

    // Iron Netherite (6 Iron + 1 Netherite)
    event.recipes.create
        .mixing("advancednetherite:netherite_iron_ingot", [
            "minecraft:netherite_ingot",
            "6x minecraft:iron_ingot",
        ])
        .heated();

    // Gold Netherite (6 Gold + 1 Iron Netherite)
    event.recipes.create
        .mixing("advancednetherite:netherite_gold_ingot", [
            "advancednetherite:netherite_iron_ingot",
            "6x minecraft:gold_ingot",
        ])
        .heated();

    // Emerald Netherite (6 Emerald + 1 Gold Netherite)
    event.recipes.create
        .mixing("advancednetherite:netherite_emerald_ingot", [
            "advancednetherite:netherite_gold_ingot",
            "6x minecraft:emerald",
        ])
        .heated();

    // Diamond Netherite (6 Diamond + 1 Emerald Netherite)
    event.recipes.create
        .mixing("advancednetherite:netherite_diamond_ingot", [
            "advancednetherite:netherite_emerald_ingot",
            "6x minecraft:diamond",
        ])
        .heated();

    console.info("[Arcadia V2] Harder Recipes Script (Fin) Loaded!");
});
