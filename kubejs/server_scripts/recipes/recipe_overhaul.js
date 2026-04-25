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

    // Sticks: restored to vanilla (2 planks -> 4 sticks) after player feedback

    // Crafting Table: Requires Leather (Forces hunting)
    event.remove({ output: "minecraft:crafting_table" });
    event.shaped("minecraft:crafting_table", ["PP", "PL"], {
        P: "#minecraft:planks",
        L: "minecraft:leather",
    });

    // Aether Crafting Tables (Logs) - only remove if they exist
    event.remove({ output: "aether:skyroot_crafting_table", allowEmpty: true });
    event.remove({ output: "deep_aether:skyroot_crafting_table", allowEmpty: true });

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
    event.remove({ mod: "aether", output: "minecraft:saddle", allowEmpty: true });
    event.remove({ mod: "aether", output: "aether:saddle", allowEmpty: true });
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

    // ============================================================
    // 10. CROSS-MOD HARDENING — Storage, Magic, Tech
    // ============================================================

    // --- STORAGE LECTERN (Ars) — APEX ENDGAME ---
    // Requires all 4 Arcadia bridges + Fusion Matrix (Arcadia tier 3 chain).
    // Forces completion of: Tech path (Industrial Heart), Magic path (Rune Matrix),
    // Arcane-tech bridge (Arcane Circuit), Occult bridge (Ethereal Alloy), Fusion chain.
    event.remove({ output: 'ars_nouveau:storage_lectern' });
    event.recipes.create.mechanical_crafting(
        'ars_nouveau:storage_lectern',
        [
            " ARA ",
            "EFPFE",
            "RPHPR",
            "EFPFE",
            " ARA "
        ], {
            A: ARCANE_CIRCUIT,
            R: RUNE_MATRIX,
            E: ETHEREAL_ALLOY,
            F: 'arcadia:fusion_matrix',
            P: 'create:precision_mechanism',
            H: INDUSTRIAL_HEART
        }
    ).id('arcadia:storage_lectern_apex');

    // --- ARS NOUVEAU cross-mod ---
    event.remove({ output: 'ars_nouveau:source_jar' });
    event.shaped('ars_nouveau:source_jar', [
        'GSG',
        'G G',
        'GBG'
    ], {
        G: 'minecraft:glass',
        S: 'ars_nouveau:source_gem',
        B: 'create:brass_ingot'
    }).id('arcadia:source_jar');

    event.remove({ output: 'ars_nouveau:imbuement_chamber' });
    event.shaped('ars_nouveau:imbuement_chamber', [
        'SAS',
        'G G',
        'STS'
    ], {
        S: 'tfmg:steel_ingot',
        A: 'ars_nouveau:source_gem_block',
        G: 'create:golden_sheet',
        T: '#c:logs/archwood'
    }).id('arcadia:imbuement_chamber');

    event.remove({ output: 'ars_nouveau:relay' });
    event.shaped('ars_nouveau:relay', [
        ' S ',
        'GAG',
        ' M '
    ], {
        S: 'ars_nouveau:source_gem',
        G: 'create:golden_sheet',
        A: 'minecraft:amethyst_block',
        M: 'mekanism:alloy_infused'
    }).id('arcadia:relay');

    event.remove({ output: 'ars_nouveau:enchanting_apparatus' });
    event.recipes.create.mechanical_crafting(
        'ars_nouveau:enchanting_apparatus',
        [
            " GPG ",
            "GASAG",
            "PS SP",
            "GASAG",
            " GPG "
        ], {
            G: 'create:golden_sheet',
            P: 'create:precision_mechanism',
            A: '#c:logs/archwood',
            S: 'ars_nouveau:source_gem'
        }
    ).id('arcadia:enchanting_apparatus');

    // --- IRON'S SPELLBOOKS cross-mod ---
    event.remove({ output: 'irons_spellbooks:inscription_table' });
    event.shaped('irons_spellbooks:inscription_table', [
        'BIG',
        'SSS',
        'L L'
    ], {
        B: 'minecraft:book',
        I: 'minecraft:ink_sac',
        G: 'ars_nouveau:source_gem',
        S: 'create:golden_sheet',
        L: '#c:logs/archwood'
    }).id('arcadia:inscription_table');

    event.remove({ output: 'irons_spellbooks:scroll_forge' });
    event.shaped('irons_spellbooks:scroll_forge', [
        'G G',
        'SMS',
        'OOO'
    ], {
        G: 'ars_nouveau:source_gem',
        S: 'create:golden_sheet',
        M: 'mekanism:alloy_infused',
        O: 'minecraft:obsidian'
    }).id('arcadia:scroll_forge');

    event.remove({ output: 'irons_spellbooks:arcane_anvil' });
    event.recipes.create.mechanical_crafting(
        'irons_spellbooks:arcane_anvil',
        [
            "SSSSS",
            "  T  ",
            " TTT "
        ], {
            S: 'tfmg:steel_ingot',
            T: 'create:brass_casing'
        }
    ).id('arcadia:arcane_anvil');

    // --- OCCULTISM cross-mod ---
    event.remove({ output: 'occultism:golden_sacrificial_bowl' });
    event.shaped('occultism:golden_sacrificial_bowl', [
        'G G',
        'SAS',
        ' P '
    ], {
        G: 'create:golden_sheet',
        S: 'ars_nouveau:source_gem',
        A: 'minecraft:gold_block',
        P: 'create:precision_mechanism'
    }).id('arcadia:golden_sacrificial_bowl');

    event.remove({ output: 'occultism:chalk_white_impure' });
    event.shaped('occultism:chalk_white_impure', [
        ' M ',
        'BCB',
        ' M '
    ], {
        M: 'ars_nouveau:magebloom_fiber',
        B: 'minecraft:bone_meal',
        C: 'minecraft:calcite'
    }).id('arcadia:chalk_white_impure');

    // --- APOTHEOSIS cross-mod ---
    // hellshelf/seashelf removed from Apotheosis 1.21 — custom bookshelves handled by ApothicEnchanting instead.

    // --- RS + FLUX NETWORKS cross-mod ---
    event.remove({ output: 'refinedstorage:controller' });
    event.recipes.create.mechanical_crafting(
        'refinedstorage:controller',
        [
            " SPS ",
            "SQDQS",
            "PDRDP",
            "SQDQS",
            " SPS "
        ], {
            S: 'refinedstorage:quartz_enriched_iron',
            P: 'create:precision_mechanism',
            Q: 'create:brass_casing',
            D: 'minecraft:diamond',
            R: 'minecraft:redstone_block'
        }
    ).id('arcadia:rs_controller');

    event.remove({ output: 'fluxnetworks:flux_plug' });
    event.shaped('fluxnetworks:flux_plug', [
        'SFS',
        'FPF',
        'SFS'
    ], {
        S: 'tfmg:steel_ingot',
        F: 'fluxnetworks:flux_dust',
        P: 'create:precision_mechanism'
    }).id('arcadia:flux_plug');

    event.remove({ output: 'fluxnetworks:flux_point' });
    event.shaped('fluxnetworks:flux_point', [
        'SFS',
        'FBF',
        'SFS'
    ], {
        S: 'tfmg:steel_ingot',
        F: 'fluxnetworks:flux_dust',
        B: 'create:brass_casing'
    }).id('arcadia:flux_point');

    // ============================================================
    // 11. LIGHT CROSS-MOD — Small touches, not hard, just interconnected
    // ============================================================

    // --- Ars Nouveau: Novice Spellbook needs a touch of Create ---
    event.remove({ output: 'ars_nouveau:novice_spell_book' });
    event.shaped('ars_nouveau:novice_spell_book', [
        ' SG',
        'SBS',
        'LS '
    ], {
        S: 'ars_nouveau:source_gem',
        G: 'create:golden_sheet',
        B: 'minecraft:book',
        L: 'minecraft:leather'
    }).id('arcadia:novice_spell_book');

    // --- Ars: Scribes Table needs Create cogwheel ---
    event.remove({ output: 'ars_nouveau:scribes_table' });
    event.shaped('ars_nouveau:scribes_table', [
        'SBF',
        'LCL',
        'L L'
    ], {
        S: 'ars_nouveau:source_gem',
        B: 'minecraft:book',
        F: 'minecraft:feather',
        L: '#c:logs/archwood',
        C: COGWHEEL
    }).id('arcadia:scribes_table');

    // --- Ars: Wand needs brass ---
    event.remove({ output: 'ars_nouveau:wand' });
    event.shaped('ars_nouveau:wand', [
        '  S',
        ' B ',
        'G  '
    ], {
        S: 'ars_nouveau:source_gem',
        B: 'create:brass_ingot',
        G: 'create:golden_sheet'
    }).id('arcadia:ars_wand');

    // --- Irons: Alchemist Cauldron needs TFMG ---
    event.remove({ output: 'irons_spellbooks:alchemist_cauldron' });
    event.shaped('irons_spellbooks:alchemist_cauldron', [
        'T T',
        'T T',
        'TTT'
    ], {
        T: 'tfmg:steel_ingot'
    }).id('arcadia:alchemist_cauldron');

    // --- Occultism: Candle needs Ars magebloom ---
    event.remove({ output: 'occultism:large_candle_white' });
    event.shaped('4x occultism:large_candle_white', [
        'S',
        'M',
        'M'
    ], {
        S: 'minecraft:string',
        M: 'ars_nouveau:magebloom_fiber'
    }).id('arcadia:occultism_candle');

    // --- Occultism: Spirit Fire needs blaze + source gem ---
    event.remove({ output: 'occultism:spirit_fire' });
    event.shapeless('occultism:spirit_fire', [
        'minecraft:flint_and_steel',
        'ars_nouveau:source_gem',
        'minecraft:soul_sand'
    ]).id('arcadia:spirit_fire');

    // --- Waystones: Waystone needs Create + Ars ---
    event.remove({ output: 'waystones:waystone' });
    event.shaped('waystones:waystone', [
        ' S ',
        'EPE',
        'SSS'
    ], {
        S: 'minecraft:stone_bricks',
        E: 'minecraft:ender_pearl',
        P: 'ars_nouveau:source_gem'
    }).id('arcadia:waystone');

    // --- Waystones: Warp Stone needs source gem ---
    event.remove({ output: 'waystones:warp_stone' });
    event.shaped('waystones:warp_stone', [
        ' E ',
        'ESE',
        ' E '
    ], {
        E: 'minecraft:ender_pearl',
        S: 'ars_nouveau:source_gem'
    }).id('arcadia:warp_stone');

    // --- Farmers Delight: Cooking Pot needs Create sheets ---
    event.remove({ output: 'farmersdelight:cooking_pot' });
    event.shaped('farmersdelight:cooking_pot', [
        'S S',
        'SWS',
        'III'
    ], {
        S: IRON_SHEET,
        W: 'minecraft:water_bucket',
        I: 'minecraft:iron_ingot'
    }).id('arcadia:cooking_pot');

    // --- Farmers Delight: Stove needs TFMG steel ---
    event.remove({ output: 'farmersdelight:stove' });
    event.shaped('farmersdelight:stove', [
        'SSS',
        'ICI',
        'III'
    ], {
        S: 'tfmg:steel_ingot',
        I: 'minecraft:iron_ingot',
        C: 'minecraft:campfire'
    }).id('arcadia:stove');

    // --- RS: Disk Drive needs Create brass ---
    event.remove({ output: 'refinedstorage:disk_drive' });
    event.shaped('refinedstorage:disk_drive', [
        'BGB',
        'QRQ',
        'BGB'
    ], {
        B: 'create:brass_ingot',
        G: 'minecraft:glass',
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone'
    }).id('arcadia:rs_disk_drive');

    // --- RS: Importer needs Create brass ---
    event.remove({ output: 'refinedstorage:importer' });
    event.shaped('refinedstorage:importer', [
        ' B ',
        'QRQ',
        ' Q '
    ], {
        B: 'create:brass_ingot',
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone'
    }).id('arcadia:rs_importer');

    // --- RS: Exporter needs Create brass ---
    event.remove({ output: 'refinedstorage:exporter' });
    event.shaped('refinedstorage:exporter', [
        ' Q ',
        'QRQ',
        ' B '
    ], {
        B: 'create:brass_ingot',
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone'
    }).id('arcadia:rs_exporter');

    // --- RS: Crafter needs precision mechanism ---
    event.remove({ output: 'refinedstorage:autocrafter' });
    event.shaped('refinedstorage:autocrafter', [
        'QRQ',
        'RPR',
        'QRQ'
    ], {
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone',
        P: 'create:precision_mechanism'
    }).id('arcadia:rs_autocrafter');

    // --- RS: Wireless Transmitter needs ender + brass ---
    event.remove({ output: 'refinedstorage:wireless_transmitter' });
    event.shaped('refinedstorage:wireless_transmitter', [
        ' E ',
        'BQB',
        ' R '
    ], {
        E: 'minecraft:ender_pearl',
        B: 'create:brass_ingot',
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone_block'
    }).id('arcadia:rs_wireless_transmitter');

    // Sophisticatedbackpacks: vanilla recipes restored (custom overrides removed).

    // --- Building Gadgets: Gadget needs Create + Mek ---
    event.remove({ output: 'buildinggadgets2:gadget_building' });
    event.shaped('buildinggadgets2:gadget_building', [
        'SPS',
        'BRB',
        'SIS'
    ], {
        S: IRON_SHEET,
        P: 'create:precision_mechanism',
        B: 'create:brass_ingot',
        R: 'minecraft:redstone_block',
        I: 'mekanism:alloy_infused'
    }).id('arcadia:gadget_building');

    // --- Building Gadgets: Copy Paste needs more ---
    event.remove({ output: 'buildinggadgets2:gadget_copy_paste' });
    event.shaped('buildinggadgets2:gadget_copy_paste', [
        'SPS',
        'BRB',
        'SES'
    ], {
        S: IRON_SHEET,
        P: 'create:precision_mechanism',
        B: 'create:brass_ingot',
        R: 'minecraft:redstone_block',
        E: 'minecraft:ender_pearl'
    }).id('arcadia:gadget_copy_paste');

    // --- Building Gadgets: Cut Paste needs even more ---
    event.remove({ output: 'buildinggadgets2:gadget_cut_paste' });
    event.shaped('buildinggadgets2:gadget_cut_paste', [
        'SPS',
        'DRD',
        'SES'
    ], {
        S: IRON_SHEET,
        P: 'create:precision_mechanism',
        D: 'minecraft:diamond',
        R: 'minecraft:redstone_block',
        E: 'minecraft:ender_pearl'
    }).id('arcadia:gadget_cut_paste');

    // --- Building Gadgets: Destruction needs diamond + steel ---
    event.remove({ output: 'buildinggadgets2:gadget_destruction' });
    event.shaped('buildinggadgets2:gadget_destruction', [
        'DPD',
        'TRT',
        'DED'
    ], {
        D: 'minecraft:diamond',
        P: 'create:precision_mechanism',
        T: 'tfmg:steel_ingot',
        R: 'minecraft:redstone_block',
        E: 'minecraft:ender_pearl'
    }).id('arcadia:gadget_destruction');

    // --- Spyglass: Create brass ---
    event.remove({ output: 'minecraft:spyglass' });
    event.shaped('minecraft:spyglass', [
        ' A ',
        ' B ',
        ' B '
    ], {
        A: 'minecraft:amethyst_shard',
        B: 'create:brass_ingot'
    }).id('arcadia:spyglass');

    // --- Clock: Create cogwheel ---
    event.remove({ output: 'minecraft:clock' });
    event.shaped('minecraft:clock', [
        ' G ',
        'GCG',
        ' G '
    ], {
        G: 'minecraft:gold_ingot',
        C: COGWHEEL
    }).id('arcadia:clock');

    // --- Compass: Create cogwheel ---
    event.remove({ output: 'minecraft:compass' });
    event.shaped('minecraft:compass', [
        ' I ',
        'ICR',
        ' I '
    ], {
        I: 'minecraft:iron_ingot',
        C: COGWHEEL,
        R: 'minecraft:redstone'
    }).id('arcadia:compass');

    // --- Nature's Compass: Expensive exploration tool ---
    event.remove({ output: 'naturescompass:naturescompass' });
    event.recipes.create.mechanical_crafting(
        'naturescompass:naturescompass',
        [
            " LSL ",
            "LACAL",
            "SCPCS",
            "LACAL",
            " LSL "
        ], {
            L: '#minecraft:logs',
            S: '#minecraft:saplings',
            A: 'ars_nouveau:source_gem',
            C: 'minecraft:compass',
            P: 'create:precision_mechanism'
        }
    ).id('arcadia:natures_compass');

    // ============================================================
    // 12. BRIDGE COMPONENTS (cross-mod gate items)
    //     Used by sections 13-29 to harden mid/late-game crafts.
    // ============================================================

    const ARCANE_CIRCUIT = 'arcadia:arcane_circuit';
    const ETHEREAL_ALLOY = 'arcadia:ethereal_alloy';
    const INDUSTRIAL_HEART = 'arcadia:industrial_heart';
    const RUNE_MATRIX = 'arcadia:rune_matrix';
    const MEK_ALLOY_INFUSED = 'mekanism:alloy_infused';
    const MEK_ALLOY_REINFORCED = 'mekanism:alloy_reinforced';
    const MEK_ALLOY_ATOMIC = 'mekanism:alloy_atomic';
    const TFMG_STEEL_INGOT = 'tfmg:steel_ingot';
    const TFMG_HEAVY_PLATE = 'tfmg:heavy_plate';
    const TFMG_STEEL_MECHANISM = 'tfmg:steel_mechanism';
    const IE_PLATE_STEEL = 'immersiveengineering:plate_steel';
    const IE_COMPONENT_STEEL = 'immersiveengineering:component_steel';
    const SOURCE_GEM = 'ars_nouveau:source_gem';
    const SOURCE_GEM_BLOCK = 'ars_nouveau:source_gem_block';
    const MAGEBLOOM_CLOTH = 'ars_nouveau:magebloom_fiber';
    const ARCHWOOD = '#c:logs/archwood';
    const BRASS_SHEET = 'create:brass_sheet';

    // 12A. ARCANE CIRCUIT (Create + TFMG + Mekanism + Ars Nouveau)
    // MEDIUM tier bridge. Required by mid-game electronics and magic devices.
    event.recipes.create.mixing(
        ARCANE_CIRCUIT,
        [
            '2x create:precision_mechanism',
            '2x ' + SOURCE_GEM,
            '2x tfmg:transistor_item',
            MEK_ALLOY_INFUSED,
            Fluid.of('tfmg:creosote', 500)
        ]
    ).heated().id('arcadia:arcane_circuit');

    // 12B. ETHEREAL ALLOY (Ars + Mekanism + Occultism + Create)
    // HARD tier bridge. Required by soul-bound items.
    event.recipes.create.mixing(
        ETHEREAL_ALLOY,
        [
            '4x ' + SOURCE_GEM,
            '2x ' + MEK_ALLOY_REINFORCED,
            'occultism:spirit_attuned_gem',
            '2x ' + BRASS_SHEET,
            Fluid.of('minecraft:lava', 1000)
        ]
    ).heated().id('arcadia:ethereal_alloy');

    // 12C. INDUSTRIAL HEART (Create + TFMG + Mekanism + Immersive Engineering)
    // HARD tier bridge. Required by heavy industrial machinery.
    event.recipes.create.sequenced_assembly(
        [Item.of(INDUSTRIAL_HEART, 1)],
        TFMG_HEAVY_PLATE,
        [
            event.recipes.createDeploying('arcadia:incomplete_industrial_heart', ['arcadia:incomplete_industrial_heart', TFMG_STEEL_MECHANISM]),
            event.recipes.createDeploying('arcadia:incomplete_industrial_heart', ['arcadia:incomplete_industrial_heart', 'create:precision_mechanism']),
            event.recipes.createDeploying('arcadia:incomplete_industrial_heart', ['arcadia:incomplete_industrial_heart', MEK_ALLOY_REINFORCED]),
            event.recipes.createDeploying('arcadia:incomplete_industrial_heart', ['arcadia:incomplete_industrial_heart', IE_COMPONENT_STEEL]),
            event.recipes.createPressing('arcadia:incomplete_industrial_heart', 'arcadia:incomplete_industrial_heart')
        ]
    ).transitionalItem('arcadia:incomplete_industrial_heart').loops(4).id('arcadia:industrial_heart');

    // 12D. RUNE MATRIX (Ars + Occult + Create + Apotheosis)
    // ENDGAME tier bridge. Required by archmage-tier items and Apotheosis sockets.
    event.recipes.create.mechanical_crafting(
        RUNE_MATRIX,
        [
            "GMAMG",
            "MACAM",
            "ACECA",
            "MACAM",
            "GMAMG"
        ], {
            G: SOURCE_GEM_BLOCK,
            M: MAGEBLOOM_CLOTH,
            A: ARCANE_CIRCUIT,
            C: 'apotheosis:rare_material',
            E: 'minecraft:echo_shard'
        }
    ).id('arcadia:rune_matrix');

    // ============================================================
    // 13. MEKANISM HARDENING
    //     T1 machines + brass/cogwheel; T2/T3 + PM; endgame + AA + bridges.
    // ============================================================

    // T1 Machines — cross-mod Create gears (iron sheet + Create parts instead of raw ingots)
    event.replaceInput({ output: 'mekanism:enrichment_chamber' }, 'minecraft:redstone', IRON_SHEET);
    event.replaceInput({ output: 'mekanism:crusher' }, 'minecraft:redstone', COGWHEEL);
    event.replaceInput({ output: 'mekanism:metallurgic_infuser' }, 'minecraft:redstone', 'create:precision_mechanism');

    // osmium_compressor: original uses '#mekanism:alloys/infused', '#c:circuits/advanced', steel_casing, bucket.
    // Replace bucket with IRON_SHEET for a visible hardening.
    event.remove({ output: 'mekanism:osmium_compressor' });
    event.shaped('mekanism:osmium_compressor', ['ACA', 'SXS', 'ACA'], {
        A: '#mekanism:alloys/infused',
        C: '#c:circuits/advanced',
        S: IRON_SHEET,
        X: 'mekanism:steel_casing'
    }).id('arcadia:mek_osmium_compressor');

    // combiner: original uses '#mekanism:alloys/reinforced', '#c:circuits/elite', steel_casing, stone_crafting_materials tag.
    // Replace stone with deepslate (harder) for a visible hardening.
    event.remove({ output: 'mekanism:combiner' });
    event.shaped('mekanism:combiner', ['ACA', 'DXD', 'ACA'], {
        A: '#mekanism:alloys/reinforced',
        C: '#c:circuits/elite',
        D: 'minecraft:deepslate',
        X: 'mekanism:steel_casing'
    }).id('arcadia:mek_combiner');

    // T2 Machines — require TFMG Steel + PM (harder)
    event.remove({ output: 'mekanism:purification_chamber' });
    event.shaped('mekanism:purification_chamber', ['RPR', 'IEI', 'SCS'], {
        R: TFMG_STEEL_INGOT,
        P: 'create:precision_mechanism',
        I: 'mekanism:advanced_control_circuit',
        E: 'mekanism:enrichment_chamber',
        S: MEK_ALLOY_REINFORCED,
        C: 'mekanism:steel_casing'
    }).id('arcadia:mek_purification_chamber');

    event.remove({ output: 'mekanism:chemical_injection_chamber' });
    event.shaped('mekanism:chemical_injection_chamber', ['RPR', 'IEI', 'SCS'], {
        R: MEK_ALLOY_REINFORCED,
        P: 'create:precision_mechanism',
        I: 'mekanism:elite_control_circuit',
        E: 'mekanism:purification_chamber',
        S: TFMG_STEEL_INGOT,
        C: 'mekanism:steel_casing'
    }).id('arcadia:mek_chemical_injection_chamber');

    event.remove({ output: 'mekanism:pressurized_reaction_chamber' });
    event.recipes.create.mechanical_crafting(
        'mekanism:pressurized_reaction_chamber',
        [
            "SPS",
            "ACM",
            "SRS"
        ], {
            S: TFMG_STEEL_INGOT,
            P: 'create:precision_mechanism',
            A: 'mekanism:advanced_control_circuit',
            C: 'mekanism:steel_casing',
            M: ARCANE_CIRCUIT,
            R: MEK_ALLOY_REINFORCED
        }
    ).id('arcadia:mek_prc');

    event.replaceInput({ output: 'mekanism:thermal_evaporation_controller' }, 'minecraft:iron_ingot', TFMG_STEEL_INGOT);
    event.replaceInput({ output: 'mekanism:thermal_evaporation_controller' }, 'minecraft:redstone', 'create:brass_casing');

    event.replaceInput({ output: 'mekanism:solar_neutron_activator' }, 'minecraft:iron_ingot', MEK_ALLOY_ATOMIC);

    // T2 Control Circuit — gated behind Arcane Circuit
    event.remove({ output: 'mekanism:advanced_control_circuit' });
    event.shapeless('mekanism:advanced_control_circuit', [
        'mekanism:basic_control_circuit', MEK_ALLOY_INFUSED, ARCANE_CIRCUIT
    ]).id('arcadia:mek_advanced_circuit');

    // T3/Endgame
    event.remove({ output: 'mekanism:ultimate_control_circuit' });
    event.recipes.create.sequenced_assembly(
        [Item.of('mekanism:ultimate_control_circuit', 1)],
        'mekanism:elite_control_circuit',
        [
            event.recipes.createDeploying('mekanism:elite_control_circuit', ['mekanism:elite_control_circuit', MEK_ALLOY_ATOMIC]),
            event.recipes.createDeploying('mekanism:elite_control_circuit', ['mekanism:elite_control_circuit', 'create:precision_mechanism']),
            event.recipes.createDeploying('mekanism:elite_control_circuit', ['mekanism:elite_control_circuit', ARCANE_CIRCUIT]),
            event.recipes.createPressing('mekanism:elite_control_circuit', 'mekanism:elite_control_circuit')
        ]
    ).transitionalItem('mekanism:elite_control_circuit').loops(4).id('arcadia:mek_ultimate_circuit');

    event.remove({ output: 'mekanism:digital_miner' });
    event.recipes.create.mechanical_crafting(
        'mekanism:digital_miner',
        [
            " HAH ",
            "AIPIA",
            "PRMRP",
            "AIPIA",
            " HAH "
        ], {
            H: INDUSTRIAL_HEART,
            A: MEK_ALLOY_ATOMIC,
            I: IE_PLATE_STEEL,
            P: 'create:precision_mechanism',
            R: RUNE_MATRIX,
            M: 'mekanism:robit'
        }
    ).id('arcadia:mek_digital_miner');

    event.remove({ output: 'mekanism:teleporter' });
    event.recipes.create.mechanical_crafting(
        'mekanism:teleporter',
        [
            " EAE ",
            "APCPA",
            "ACTCA",
            "APCPA",
            " EAE "
        ], {
            E: 'minecraft:ender_eye',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            C: SOURCE_GEM_BLOCK,
            T: 'mekanism:teleportation_core'
        }
    ).id('arcadia:mek_teleporter');

    event.remove({ output: 'mekanism:teleportation_core' });
    event.recipes.create.mixing('mekanism:teleportation_core', [
        '4x minecraft:diamond',
        '4x minecraft:gold_ingot',
        '2x ' + MEK_ALLOY_ATOMIC,
        '2x minecraft:ender_pearl',
        SOURCE_GEM,
        Fluid.of('minecraft:lava', 1000)
    ]).heated().id('arcadia:mek_teleportation_core');

    event.remove({ output: 'mekanism:qio_drive_array' });
    event.recipes.create.mechanical_crafting(
        'mekanism:qio_drive_array',
        [
            "SASAS",
            "APCPA",
            "SCMCS",
            "APCPA",
            "SASAS"
        ], {
            S: IE_PLATE_STEEL,
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            C: 'mekanism:elite_control_circuit',
            M: ARCANE_CIRCUIT
        }
    ).id('arcadia:mek_qio_drive_array');

    event.remove({ output: 'mekanism:qio_dashboard' });
    event.shaped('mekanism:qio_dashboard', ['GAG', 'PDP', 'SCS'], {
        G: 'create:brass_casing',
        A: ARCANE_CIRCUIT,
        P: 'create:precision_mechanism',
        D: 'mekanism:qio_drive_array',
        S: MEK_ALLOY_ATOMIC,
        C: 'mekanism:elite_control_circuit'
    }).id('arcadia:mek_qio_dashboard');

    event.remove({ output: 'mekanism:antiprotonic_nucleosynthesizer' });
    event.recipes.create.mechanical_crafting(
        'mekanism:antiprotonic_nucleosynthesizer',
        [
            "  FAF  ",
            " FAPAF ",
            "FAMCNAF",
            "APCRCPA",
            "FANCMAF",
            " FAPAF ",
            "  FAF  "
        ], {
            F: 'arcadia:fusion_matrix',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            M: ARCANE_CIRCUIT,
            C: 'mekanism:ultimate_control_circuit',
            N: 'minecraft:nether_star',
            R: RUNE_MATRIX
        }
    ).id('arcadia:mek_antiprotonic');

    event.remove({ output: 'mekanism:sps_casing' });
    event.shaped('mekanism:sps_casing', ['ARA', 'RCR', 'ARA'], {
        A: MEK_ALLOY_ATOMIC,
        R: 'mekanism:structural_glass',
        C: 'create:brass_casing'
    }).id('arcadia:mek_sps_casing');

    // MekanismGenerators apex — tied to Arcadia fusion chain
    event.remove({ output: 'mekanismgenerators:fusion_reactor_controller' });
    event.recipes.create.mechanical_crafting(
        'mekanismgenerators:fusion_reactor_controller',
        [
            "  FMF  ",
            " FCPCF ",
            "FCMAMCF",
            "MPAHAPM",
            "FCMAMCF",
            " FCPCF ",
            "  FMF  "
        ], {
            F: 'arcadia:fusion_matrix',
            M: 'arcadia:plasma_cell',
            C: 'arcadia:containment_field_generator',
            P: 'create:precision_mechanism',
            A: MEK_ALLOY_ATOMIC,
            H: INDUSTRIAL_HEART
        }
    ).id('arcadia:mek_fusion_controller');

    // MekanismTools refined tier — add breeze rod + source gem
    const mekRefinedTools = [
        'mekanismtools:refined_glowstone_sword', 'mekanismtools:refined_glowstone_pickaxe',
        'mekanismtools:refined_glowstone_axe', 'mekanismtools:refined_glowstone_shovel',
        'mekanismtools:refined_glowstone_hoe', 'mekanismtools:refined_glowstone_paxel',
        'mekanismtools:refined_obsidian_sword', 'mekanismtools:refined_obsidian_pickaxe',
        'mekanismtools:refined_obsidian_axe', 'mekanismtools:refined_obsidian_shovel',
        'mekanismtools:refined_obsidian_hoe', 'mekanismtools:refined_obsidian_paxel'
    ];
    mekRefinedTools.forEach(item => event.replaceInput({ output: item }, 'minecraft:stick', REINFORCE_BLOCK));

    const mekRefinedArmor = [
        'mekanismtools:refined_glowstone_helmet', 'mekanismtools:refined_glowstone_chestplate',
        'mekanismtools:refined_glowstone_leggings', 'mekanismtools:refined_glowstone_boots',
        'mekanismtools:refined_obsidian_helmet', 'mekanismtools:refined_obsidian_chestplate',
        'mekanismtools:refined_obsidian_leggings', 'mekanismtools:refined_obsidian_boots'
    ];
    mekRefinedArmor.forEach(item => event.replaceInput({ output: item, allowEmpty: true }, 'minecraft:leather', SOURCE_GEM));

    // HDPE ROD — harden: 4 pellets + 1 brass sheet (Create) in a 2x3 shaped craft.
    event.remove({ output: 'mekanism:hdpe_rod' });
    event.shaped('mekanism:hdpe_rod', ['PP', 'PP', 'B '], {
        P: 'mekanism:hdpe_pellet',
        B: BRASS_SHEET
    }).id('arcadia:hdpe_rod');

    // HDPE SHEET — endgame Create Sequenced Assembly (5 loops, 5 ingredients per loop + molten steel).
    // Default: 3 pellets in Enrichment Chamber. New: full Create + TFMG + Mek chain.
    // Per sheet: 1 hdpe_pellet + 5 hdpe_rods + 5 brass_sheets + 5 heavy_plates + 5 alloy_reinforced + 2500mb molten_steel.
    event.remove({ output: 'mekanism:hdpe_sheet' });
    event.recipes.create.sequenced_assembly(
        [Item.of('mekanism:hdpe_sheet', 1)],
        'mekanism:hdpe_pellet',
        [
            event.recipes.createDeploying('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', 'mekanism:hdpe_rod']),
            event.recipes.createDeploying('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', BRASS_SHEET]),
            event.recipes.createDeploying('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', TFMG_HEAVY_PLATE]),
            event.recipes.createDeploying('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', MEK_ALLOY_REINFORCED]),
            event.recipes.createFilling('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', Fluid.of('tfmg:molten_steel', 500)]),
            event.recipes.createPressing('mekanism:hdpe_pellet', 'mekanism:hdpe_pellet')
        ]
    ).transitionalItem('mekanism:hdpe_pellet').loops(5).id('arcadia:hdpe_sheet');

    // ============================================================
    // 14. TFMG HARDENING
    // ============================================================

    event.replaceInput({ output: 'tfmg:converter' }, 'minecraft:copper_ingot', 'createaddition:copper_spool');
    event.replaceInput({ output: 'tfmg:converter' }, 'createaddition:copper_wire', 'createaddition:copper_spool');

    // Transistor: original sequenced_assembly uses '#c:wires/copper' tag. Rewrite to force copper_spool.
    event.remove({ id: 'tfmg:sequenced_assembly/transistor' });
    event.remove({ output: 'tfmg:transistor_item' });
    const incompleteTransistor = 'tfmg:unfinished_transistor';
    event.recipes.create.sequenced_assembly(
        [ Item.of('tfmg:transistor_item', 4) ],
        'tfmg:plastic_sheet',
        [
            event.recipes.createDeploying(incompleteTransistor, [incompleteTransistor, 'createaddition:copper_spool']),
            event.recipes.createDeploying(incompleteTransistor, [incompleteTransistor, 'tfmg:n_semiconductor']),
            event.recipes.createDeploying(incompleteTransistor, [incompleteTransistor, 'tfmg:p_semiconductor']),
            event.recipes.createDeploying(incompleteTransistor, [incompleteTransistor, 'tfmg:n_semiconductor'])
        ]
    ).transitionalItem(incompleteTransistor).loops(1).id('arcadia:tfmg_transistor_fix');

    event.remove({ output: 'tfmg:industrial_mixer' });
    event.recipes.create.mechanical_crafting(
        'tfmg:industrial_mixer',
        [
            "SCS",
            "PMP",
            "SHS"
        ], {
            S: TFMG_HEAVY_PLATE,
            C: COGWHEEL,
            P: 'create:precision_mechanism',
            M: 'create:mechanical_mixer',
            H: 'create:brass_casing'
        }
    ).id('arcadia:tfmg_industrial_mixer');

    event.remove({ output: 'tfmg:centrifuge' });
    event.recipes.create.mechanical_crafting(
        'tfmg:centrifuge',
        [
            "SPS",
            "CHC",
            "SMS"
        ], {
            S: TFMG_HEAVY_PLATE,
            P: 'create:precision_mechanism',
            C: 'create:brass_casing',
            H: TFMG_STEEL_MECHANISM,
            M: MEK_ALLOY_REINFORCED
        }
    ).id('arcadia:tfmg_centrifuge');

    event.remove({ output: 'tfmg:heavy_machinery_casing' });
    event.shaped('tfmg:heavy_machinery_casing', ['HPH', 'PHP', 'HPH'], {
        H: TFMG_HEAVY_PLATE,
        P: INDUSTRIAL_HEART
    }).id('arcadia:tfmg_heavy_machinery_casing');

    event.remove({ output: 'tfmg:large_engine' });
    event.shaped('tfmg:large_engine', ['HHH', 'PIP', 'CMC'], {
        H: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        I: INDUSTRIAL_HEART,
        C: 'createaddition:copper_spool',
        M: TFMG_STEEL_MECHANISM
    }).id('arcadia:tfmg_large_engine');

    event.remove({ output: 'tfmg:radial_engine' });
    event.shaped('tfmg:radial_engine', ['HCH', 'PIP', 'HMH'], {
        H: TFMG_HEAVY_PLATE,
        C: 'create:brass_casing',
        P: 'create:precision_mechanism',
        I: INDUSTRIAL_HEART,
        M: TFMG_STEEL_MECHANISM
    }).id('arcadia:tfmg_radial_engine');

    event.remove({ output: 'tfmg:turbine_engine' });
    event.shaped('tfmg:turbine_engine', ['HCH', 'IMI', 'HCH'], {
        H: TFMG_HEAVY_PLATE,
        C: 'create:brass_casing',
        I: INDUSTRIAL_HEART,
        M: 'create:precision_mechanism'
    }).id('arcadia:tfmg_turbine_engine');

    event.remove({ output: 'tfmg:steel_distillation_controller' });
    event.shaped('tfmg:steel_distillation_controller', ['HPH', 'CMC', 'HPH'], {
        H: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        C: 'create:brass_casing',
        M: TFMG_STEEL_MECHANISM
    }).id('arcadia:tfmg_distillation_controller');

    event.replaceInput({ output: 'tfmg:blast_furnace_hatch' }, 'minecraft:iron_ingot', TFMG_HEAVY_PLATE);

    // ============================================================
    // 15. IMMERSIVE ENGINEERING HARDENING
    // ============================================================

    event.remove({ output: 'immersiveengineering:hammer' });
    event.shaped('immersiveengineering:hammer', [' II', ' SI', 'S  '], {
        I: IRON_SHEET,
        S: 'minecraft:stick'
    }).id('arcadia:ie_hammer');

    event.remove({ output: 'immersiveengineering:light_engineering' });
    event.shaped('immersiveengineering:light_engineering', ['SWS', 'ICI', 'SWS'], {
        S: IRON_SHEET,
        W: 'immersiveengineering:wirecoil_copper',
        I: 'immersiveengineering:component_iron',
        C: COGWHEEL
    }).id('arcadia:ie_light_engineering');

    event.remove({ output: 'immersiveengineering:heavy_engineering' });
    event.shaped('immersiveengineering:heavy_engineering', ['SPS', 'PCP', 'SPS'], {
        S: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        C: IE_COMPONENT_STEEL
    }).id('arcadia:ie_heavy_engineering');

    event.remove({ output: 'immersiveengineering:revolver' });
    event.shaped('immersiveengineering:revolver', [' GS', 'CPM', 'HB '], {
        G: 'immersiveengineering:gunpart_hammer',
        S: IE_PLATE_STEEL,
        C: 'create:brass_sheet',
        P: 'create:precision_mechanism',
        M: IE_COMPONENT_STEEL,
        H: 'immersiveengineering:coil_mv',
        B: 'immersiveengineering:wooden_grip'
    }).id('arcadia:ie_revolver');

    event.remove({ output: 'immersiveengineering:drill' });
    event.recipes.create.mechanical_crafting(
        'immersiveengineering:drill',
        [
            "  SHS",
            " SPCS",
            "SMECS",
            " SPCS",
            "  SHS"
        ], {
            S: TFMG_HEAVY_PLATE,
            H: INDUSTRIAL_HEART,
            P: 'create:precision_mechanism',
            C: IE_COMPONENT_STEEL,
            M: 'immersiveengineering:heavy_engineering',
            E: 'immersiveengineering:capacitor_mv'
        }
    ).id('arcadia:ie_drill');

    event.remove({ output: 'immersiveengineering:railgun' });
    event.recipes.create.mechanical_crafting(
        'immersiveengineering:railgun',
        [
            "SSSSS",
            "CPAPC",
            "SMHMS",
            "CPAPC",
            "SSSSS"
        ], {
            S: IE_PLATE_STEEL,
            C: 'immersiveengineering:capacitor_hv',
            P: 'create:precision_mechanism',
            A: MEK_ALLOY_ATOMIC,
            M: 'immersiveengineering:heavy_engineering',
            H: INDUSTRIAL_HEART
        }
    ).id('arcadia:ie_railgun');

    // Note: IE Excavator and Arc Furnace are multiblocks, not crafted items — no override needed.

    // ============================================================
    // 16. CREATE ADDITION HARDENING
    // ============================================================

    event.remove({ output: 'createaddition:capacitor' });
    event.shaped('createaddition:capacitor', ['BEB', 'GRG', 'GWG'], {
        B: 'create:brass_sheet',
        E: 'create:electron_tube',
        G: 'minecraft:gold_ingot',
        R: 'minecraft:redstone',
        W: 'createaddition:copper_wire'
    }).id('arcadia:ca_capacitor');

    event.remove({ output: 'createaddition:modular_accumulator' });
    event.recipes.create.mechanical_crafting(
        'createaddition:modular_accumulator',
        [
            "GCG",
            "CAC",
            "GCG"
        ], {
            G: GOLD_SHEET,
            C: 'createaddition:capacitor',
            A: ARCANE_CIRCUIT
        }
    ).id('arcadia:ca_modular_accumulator');

    // createaddition:charger item does not exist — removed.
    event.remove({ output: 'createaddition:portable_energy_interface' });
    event.shaped('createaddition:portable_energy_interface', ['SCS', 'PMP', 'SCS'], {
        S: IRON_SHEET,
        C: 'createaddition:capacitor',
        P: 'create:precision_mechanism',
        M: 'create:copper_casing'
    }).id('arcadia:ca_portable_energy');

    event.remove({ output: 'createaddition:tesla_coil' });
    event.recipes.create.mechanical_crafting(
        'createaddition:tesla_coil',
        [
            " W ",
            "CPC",
            "HAH"
        ], {
            W: 'createaddition:copper_spool',
            C: 'createaddition:capacitor',
            P: 'create:precision_mechanism',
            H: TFMG_HEAVY_PLATE,
            A: MEK_ALLOY_ATOMIC
        }
    ).id('arcadia:ca_tesla_coil');

    event.remove({ output: 'createaddition:alternator' });
    event.shaped('createaddition:alternator', ['BWB', 'WAW', 'BWB'], {
        B: 'create:brass_sheet',
        W: 'createaddition:copper_spool',
        A: 'create:andesite_casing'
    }).id('arcadia:ca_alternator');

    event.remove({ output: 'createaddition:rolling_mill' });
    event.shaped('createaddition:rolling_mill', [' S ', 'SCS', 'PBP'], {
        S: IRON_SHEET,
        C: COGWHEEL,
        P: 'create:precision_mechanism',
        B: 'create:brass_casing'
    }).id('arcadia:ca_rolling_mill');

    // ============================================================
    // 17. CREATE NUCLEAR HARDENING
    // ============================================================

    event.remove({ output: 'createnuclear:reactor_casing' });
    event.shaped('createnuclear:reactor_casing', ['HPH', 'PCP', 'HPH'], {
        H: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        C: 'createnuclear:steel_block'
    }).id('arcadia:cn_reactor_casing');

    event.remove({ output: 'createnuclear:reactor_controller' });
    event.recipes.create.mechanical_crafting(
        'createnuclear:reactor_controller',
        [
            "CAC",
            "PRP",
            "CAC"
        ], {
            C: 'createnuclear:reactor_casing',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            R: RUNE_MATRIX
        }
    ).id('arcadia:cn_reactor_controller');

    event.remove({ output: 'createnuclear:reactor_core' });
    event.shaped('createnuclear:reactor_core', ['CPC', 'URU', 'CPC'], {
        C: 'createnuclear:reactor_casing',
        P: 'create:precision_mechanism',
        U: 'createnuclear:uranium_rod',
        R: 'createnuclear:reinforced_glass'
    }).id('arcadia:cn_reactor_core');

    event.remove({ output: 'createnuclear:reactor_frame' });
    event.shaped('createnuclear:reactor_frame', ['HPH', 'P P', 'HPH'], {
        H: 'createnuclear:lead_ingot',
        P: TFMG_HEAVY_PLATE
    }).id('arcadia:cn_reactor_frame');

    event.remove({ output: 'createnuclear:reinforced_glass' });
    event.shaped('createnuclear:reinforced_glass', ['LGL', 'GPG', 'LGL'], {
        L: 'createnuclear:lead_ingot',
        G: 'minecraft:glass',
        P: 'create:precision_mechanism'
    }).id('arcadia:cn_reinforced_glass');

    // ============================================================
    // 18. CREATE DIESEL GENERATORS HARDENING
    // ============================================================

    event.remove({ output: 'createdieselgenerators:diesel_engine' });
    event.recipes.create.mechanical_crafting(
        'createdieselgenerators:diesel_engine',
        [
            "SPS",
            "CHC",
            "SMS"
        ], {
            S: TFMG_HEAVY_PLATE,
            P: 'create:precision_mechanism',
            C: 'create:brass_casing',
            H: INDUSTRIAL_HEART,
            M: 'createaddition:copper_spool'
        }
    ).id('arcadia:cdg_diesel_engine');

    event.remove({ output: 'createdieselgenerators:large_diesel_engine' });
    event.recipes.create.mechanical_crafting(
        'createdieselgenerators:large_diesel_engine',
        [
            "SHS",
            "DID",
            "SPS"
        ], {
            S: TFMG_HEAVY_PLATE,
            H: INDUSTRIAL_HEART,
            D: 'createdieselgenerators:diesel_engine',
            I: TFMG_STEEL_MECHANISM,
            P: 'create:precision_mechanism'
        }
    ).id('arcadia:cdg_large_diesel_engine');

    event.remove({ output: 'createdieselgenerators:huge_diesel_engine' });
    event.recipes.create.mechanical_crafting(
        'createdieselgenerators:huge_diesel_engine',
        [
            "SHHHS",
            "HDIDH",
            "SHAHS",
            "HDIDH",
            "SHHHS"
        ], {
            S: TFMG_HEAVY_PLATE,
            H: INDUSTRIAL_HEART,
            D: 'createdieselgenerators:large_diesel_engine',
            I: TFMG_STEEL_MECHANISM,
            A: MEK_ALLOY_ATOMIC
        }
    ).id('arcadia:cdg_huge_diesel_engine');

    event.remove({ output: 'createdieselgenerators:distillation_controller' });
    event.shaped('createdieselgenerators:distillation_controller', ['HPH', 'CIC', 'HPH'], {
        H: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        C: 'create:brass_casing',
        I: TFMG_STEEL_MECHANISM
    }).id('arcadia:cdg_distillation_controller');

    // ============================================================
    // 19. ADVANCED PERIPHERALS HARDENING
    // ============================================================

    event.remove({ output: 'advancedperipherals:peripheral_casing' });
    event.shaped('advancedperipherals:peripheral_casing', ['SHS', 'HAH', 'SHS'], {
        S: TFMG_HEAVY_PLATE,
        H: IE_PLATE_STEEL,
        A: ARCANE_CIRCUIT
    }).id('arcadia:ap_peripheral_casing');

    event.remove({ output: 'advancedperipherals:rs_bridge' });
    event.recipes.create.mechanical_crafting(
        'advancedperipherals:rs_bridge',
        [
            "SPS",
            "PAQ",
            "SPS"
        ], {
            S: 'advancedperipherals:peripheral_casing',
            P: 'create:precision_mechanism',
            A: ARCANE_CIRCUIT,
            Q: 'refinedstorage:quartz_enriched_iron'
        }
    ).id('arcadia:ap_rs_bridge');

    event.remove({ output: 'advancedperipherals:me_bridge' });
    event.recipes.create.mechanical_crafting(
        'advancedperipherals:me_bridge',
        [
            "SAS",
            "PMP",
            "SAS"
        ], {
            S: 'advancedperipherals:peripheral_casing',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            M: ARCANE_CIRCUIT
        }
    ).id('arcadia:ap_me_bridge');

    event.remove({ output: 'advancedperipherals:chunk_controller' });
    event.recipes.create.mechanical_crafting(
        'advancedperipherals:chunk_controller',
        [
            "EAE",
            "PSP",
            "EAE"
        ], {
            E: 'minecraft:ender_pearl',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            S: 'advancedperipherals:peripheral_casing'
        }
    ).id('arcadia:ap_chunk_controller');

    event.remove({ output: 'advancedperipherals:player_detector' });
    event.shaped('advancedperipherals:player_detector', ['SES', 'EAE', 'SPS'], {
        S: 'advancedperipherals:peripheral_casing',
        E: 'minecraft:ender_eye',
        A: ARCANE_CIRCUIT,
        P: 'create:precision_mechanism'
    }).id('arcadia:ap_player_detector');

    // ============================================================
    // 20. REFINED STORAGE + EXTRADISKS HARDENING
    // ============================================================

    event.remove({ output: 'refinedstorage:grid' });
    event.shaped('refinedstorage:grid', ['SQS', 'GPG', 'SCS'], {
        S: IRON_SHEET,
        Q: 'minecraft:quartz',
        G: 'minecraft:glass_pane',
        P: 'create:precision_mechanism',
        C: 'create:brass_casing'
    }).id('arcadia:rs_grid');

    event.remove({ output: 'refinedstorage:crafting_grid' });
    event.shaped('refinedstorage:crafting_grid', [' C ', 'GRG', ' P '], {
        C: 'minecraft:crafting_table',
        G: 'minecraft:glass_pane',
        R: 'refinedstorage:grid',
        P: 'create:precision_mechanism'
    }).id('arcadia:rs_crafting_grid');

    event.remove({ output: 'refinedstorage:wireless_grid' });
    event.shaped('refinedstorage:wireless_grid', [' E ', 'GRG', ' B '], {
        E: 'minecraft:ender_pearl',
        G: 'minecraft:glass_pane',
        R: 'refinedstorage:grid',
        B: 'create:brass_casing'
    }).id('arcadia:rs_wireless_grid');

    event.remove({ output: 'refinedstorage:64k_storage_part' });
    event.recipes.create.mechanical_crafting(
        'refinedstorage:64k_storage_part',
        [
            "GPG",
            "QRQ",
            "GPG"
        ], {
            G: 'minecraft:glass',
            P: 'create:precision_mechanism',
            Q: 'refinedstorage:quartz_enriched_iron',
            R: MEK_ALLOY_REINFORCED
        }
    ).id('arcadia:rs_64k_part');

    event.remove({ output: 'extradisks:1024k_item_storage_part' });
    event.recipes.create.mechanical_crafting(
        'extradisks:1024k_item_storage_part',
        [
            "GAG",
            "PKP",
            "GSG"
        ], {
            G: 'minecraft:glass',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            K: 'extradisks:256k_item_storage_part',
            S: SOURCE_GEM_BLOCK
        }
    ).id('arcadia:rs_1024k_part');

    event.remove({ output: 'extradisks:4096k_item_storage_part' });
    event.recipes.create.sequenced_assembly(
        [Item.of('extradisks:4096k_item_storage_part', 1)],
        'extradisks:1024k_item_storage_part',
        [
            event.recipes.createDeploying('extradisks:1024k_item_storage_part', ['extradisks:1024k_item_storage_part', MEK_ALLOY_ATOMIC]),
            event.recipes.createDeploying('extradisks:1024k_item_storage_part', ['extradisks:1024k_item_storage_part', 'arcadia:fusion_matrix']),
            event.recipes.createDeploying('extradisks:1024k_item_storage_part', ['extradisks:1024k_item_storage_part', 'create:precision_mechanism']),
            event.recipes.createPressing('extradisks:1024k_item_storage_part', 'extradisks:1024k_item_storage_part')
        ]
    ).transitionalItem('extradisks:1024k_item_storage_part').loops(5).id('arcadia:rs_4096k_part');

    event.remove({ output: 'extradisks:infinite_item_storage_part' });
    event.recipes.create.mechanical_crafting(
        'extradisks:infinite_item_storage_part',
        [
            " NAN ",
            "AFMFA",
            "NMXMN",
            "AFMFA",
            " NAN "
        ], {
            N: 'minecraft:nether_star',
            A: MEK_ALLOY_ATOMIC,
            F: 'arcadia:fusion_core',
            M: RUNE_MATRIX,
            X: 'extradisks:1048576k_item_storage_part'
        }
    ).id('arcadia:rs_infinite_part');

    // ============================================================
    // 21. FLUX NETWORKS HARDENING
    // ============================================================

    event.remove({ output: 'fluxnetworks:flux_controller' });
    event.recipes.create.mechanical_crafting(
        'fluxnetworks:flux_controller',
        [
            "FCF",
            "PSP",
            "FAF"
        ], {
            F: 'fluxnetworks:flux_core',
            C: SOURCE_GEM_BLOCK,
            P: 'create:precision_mechanism',
            S: 'minecraft:ender_eye',
            A: MEK_ALLOY_ATOMIC
        }
    ).id('arcadia:flux_controller');

    event.remove({ output: 'fluxnetworks:basic_flux_storage' });
    event.shaped('fluxnetworks:basic_flux_storage', ['CBC', 'FSF', 'CTC'], {
        C: 'create:brass_casing',
        B: 'fluxnetworks:flux_core',
        F: 'fluxnetworks:flux_block',
        S: TFMG_STEEL_INGOT,
        T: TFMG_HEAVY_PLATE
    }).id('arcadia:flux_storage');

    event.remove({ output: 'fluxnetworks:gargantuan_flux_storage' });
    event.recipes.create.mechanical_crafting(
        'fluxnetworks:gargantuan_flux_storage',
        [
            "HFH",
            "FSF",
            "HAH"
        ], {
            H: 'fluxnetworks:herculean_flux_storage',
            F: 'arcadia:fusion_matrix',
            A: MEK_ALLOY_ATOMIC,
            S: SOURCE_GEM_BLOCK
        }
    ).id('arcadia:flux_gargantuan_storage');

    // ============================================================
    // 22. ARS NOUVEAU EXTRAS HARDENING
    // ============================================================

    event.remove({ output: 'ars_nouveau:apprentice_spell_book' });
    event.shaped('ars_nouveau:apprentice_spell_book', ['MAM', 'NGN', 'MPM'], {
        M: MAGEBLOOM_CLOTH,
        A: ARCANE_CIRCUIT,
        N: SOURCE_GEM_BLOCK,
        G: 'ars_nouveau:novice_spell_book',
        P: 'create:precision_mechanism'
    }).id('arcadia:ars_apprentice_spellbook');

    event.remove({ output: 'ars_nouveau:archmage_spell_book' });
    event.recipes.create.mechanical_crafting(
        'ars_nouveau:archmage_spell_book',
        [
            "SAS",
            "ARA",
            "SAS"
        ], {
            S: SOURCE_GEM_BLOCK,
            A: MAGEBLOOM_CLOTH,
            R: RUNE_MATRIX
        }
    ).id('arcadia:ars_archmage_spellbook');

    event.remove({ output: 'ars_nouveau:enchanters_sword' });
    event.shaped('ars_nouveau:enchanters_sword', [' S ', ' S ', ' P '], {
        S: SOURCE_GEM_BLOCK,
        P: REINFORCE_BLOCK
    }).id('arcadia:ars_enchanters_sword');

    event.remove({ output: 'ars_nouveau:enchanters_shield' });
    event.shaped('ars_nouveau:enchanters_shield', ['SGS', 'SPS', ' S '], {
        S: SOURCE_GEM_BLOCK,
        G: ETHEREAL_ALLOY,
        P: 'create:precision_mechanism'
    }).id('arcadia:ars_enchanters_shield');

    event.remove({ output: 'ars_nouveau:enchanters_mirror' });
    event.shaped('ars_nouveau:enchanters_mirror', [' E ', 'SRS', ' P '], {
        E: 'minecraft:ender_eye',
        S: SOURCE_GEM_BLOCK,
        R: RUNE_MATRIX,
        P: 'create:precision_mechanism'
    }).id('arcadia:ars_enchanters_mirror');

    event.remove({ output: 'ars_nouveau:mob_jar' });
    event.shaped('ars_nouveau:mob_jar', ['GBG', 'EPE', 'GBG'], {
        G: 'minecraft:glass',
        B: 'create:brass_casing',
        E: ETHEREAL_ALLOY,
        P: 'create:precision_mechanism'
    }).id('arcadia:ars_mob_jar');

    event.remove({ output: 'ars_nouveau:alteration_table' });
    event.shaped('ars_nouveau:alteration_table', ['MAM', 'SFS', 'LLL'], {
        M: MAGEBLOOM_CLOTH,
        A: 'minecraft:feather',
        S: SOURCE_GEM,
        F: RUNE_MATRIX,
        L: ARCHWOOD
    }).id('arcadia:ars_alteration_table');

    event.remove({ output: 'ars_nouveau:agronomic_sourcelink' });
    event.shaped('ars_nouveau:agronomic_sourcelink', ['SAS', 'WCW', 'LLL'], {
        S: SOURCE_GEM_BLOCK,
        A: ARCHWOOD,
        W: 'minecraft:wheat',
        C: 'create:brass_casing',
        L: ARCHWOOD
    }).id('arcadia:ars_agronomic_sourcelink');

    // ============================================================
    // 23. ARS CREO / ARS TECHNICA HARDENING
    //     kinetic_sourcelink/source_crafter/source_mixer do not exist in these addon versions.
    //     Ars Creo adds starbuncle_wheel only; Ars Technica adds source_motor + armor sets.
    // ============================================================

    // ============================================================
    // 24. IRON'S SPELLBOOKS HARDENING
    // ============================================================

    event.remove({ output: 'irons_spellbooks:netherite_spell_book' });
    event.recipes.create.mechanical_crafting(
        'irons_spellbooks:netherite_spell_book',
        [
            "NAN",
            "DRD",
            "NPN"
        ], {
            N: 'minecraft:netherite_ingot',
            A: MEK_ALLOY_ATOMIC,
            D: 'irons_spellbooks:diamond_spell_book',
            R: RUNE_MATRIX,
            P: 'create:precision_mechanism'
        }
    ).id('arcadia:is_netherite_spellbook');

    event.remove({ output: 'irons_spellbooks:dragonskin_spell_book' });
    event.shaped('irons_spellbooks:dragonskin_spell_book', ['SNS', 'NRN', 'SNS'], {
        S: SOURCE_GEM_BLOCK,
        N: 'irons_spellbooks:netherite_spell_book',
        R: RUNE_MATRIX
    }).id('arcadia:is_dragonskin_spellbook');

    const archevokerArmor = [
        'irons_spellbooks:archevoker_helmet',
        'irons_spellbooks:archevoker_chestplate',
        'irons_spellbooks:archevoker_leggings',
        'irons_spellbooks:archevoker_boots'
    ];
    archevokerArmor.forEach(item => event.replaceInput({ output: item, allowEmpty: true }, 'irons_spellbooks:arcane_ingot', ETHEREAL_ALLOY));

    // ============================================================
    // 25. OCCULTISM HARDENING
    // ============================================================

    event.remove({ output: 'occultism:divination_rod' });
    event.shaped('occultism:divination_rod', [' GA', ' SG', 'S  '], {
        G: GOLD_SHEET,
        A: ARCANE_CIRCUIT,
        S: 'minecraft:stick'
    }).id('arcadia:occultism_divination_rod');

    event.remove({ output: 'occultism:infused_pickaxe' });
    event.shaped('occultism:infused_pickaxe', ['EEE', ' S ', ' S '], {
        E: ETHEREAL_ALLOY,
        S: REINFORCE_BLOCK
    }).id('arcadia:occultism_infused_pickaxe');

    event.remove({ output: 'occultism:otherworld_goggles' });
    event.shaped('occultism:otherworld_goggles', ['EGE', 'SES', ' O '], {
        E: ETHEREAL_ALLOY,
        G: GOLD_SHEET,
        S: SOURCE_GEM,
        O: 'minecraft:obsidian'
    }).id('arcadia:occultism_goggles');

    // soul_gem_empty is obtained via Djinni ritual only — not craftable, skipped.

    // ============================================================
    // 26. APOTHEOSIS HARDENING
    // ============================================================

    event.remove({ output: 'apotheosis:sigil_of_socketing' });
    event.shaped('apotheosis:sigil_of_socketing', [' G ', 'RPR', ' G '], {
        G: 'apotheosis:rare_material',
        R: RUNE_MATRIX,
        P: 'create:precision_mechanism'
    }).id('arcadia:apo_sigil_socketing');

    // Sigil of Enhancement: add RUNE_MATRIX bridge + halve output count (2 instead of 4)
    event.remove({ output: 'apotheosis:sigil_of_enhancement' });
    event.shaped(Item.of('apotheosis:sigil_of_enhancement', 2), ['GEG', 'EME', 'GEG'], {
        G: 'apotheosis:gem_dust',
        E: 'apotheosis:gem_fused_slate',
        M: RUNE_MATRIX
    }).id('arcadia:apo_sigil_enhancement');

    // Sigil of Rebirth: add ARCANE_CIRCUIT corners + halve output count (3 instead of 6)
    event.remove({ output: 'apotheosis:sigil_of_rebirth' });
    event.shaped(Item.of('apotheosis:sigil_of_rebirth', 3), ['AGA', 'EEE', 'AGA'], {
        A: ARCANE_CIRCUIT,
        G: 'apotheosis:gem_fused_slate',
        E: 'apotheosis:gem_dust'
    }).id('arcadia:apo_sigil_rebirth');

    // --- APEX: Sigil of Supremacy ---
    // The ultimate affix-upgrade sigil. Requires ALL 4 Arcadia bridges, the Fusion chain (tier 3),
    // Industrial Hearts, 4 Nether Stars and 1 Apotheosis Mythic Material.
    // Per sigil: 4 nether_star, 8 arcane_circuit, 4 rune_matrix, 4 ethereal_alloy,
    // 2 fusion_matrix, 2 industrial_heart, 1 mythic_material.
    event.remove({ output: 'apotheosis:sigil_of_supremacy' });
    event.recipes.create.mechanical_crafting(
        'apotheosis:sigil_of_supremacy',
        [
            "NARAN",
            "ACFCA",
            "RIMIR",
            "ACFCA",
            "NARAN"
        ], {
            N: 'minecraft:nether_star',
            A: ARCANE_CIRCUIT,
            R: RUNE_MATRIX,
            C: ETHEREAL_ALLOY,
            F: 'arcadia:fusion_matrix',
            I: INDUSTRIAL_HEART,
            M: 'apotheosis:mythic_material'
        }
    ).id('arcadia:apo_sigil_supremacy');

    // vial_of_expulsion was removed from Apotheosis 1.21 — skipped.

    // ============================================================
    // 27. AETHER HARDENING (gravitite + phoenix)
    // ============================================================

    const aetherGravititeTools = [
        'aether:gravitite_sword', 'aether:gravitite_pickaxe', 'aether:gravitite_axe',
        'aether:gravitite_shovel', 'aether:gravitite_hoe'
    ];
    aetherGravititeTools.forEach(item => event.replaceInput({ output: item }, 'aether:skyroot_stick', REINFORCE_BLOCK));

    // Gravitite armor: vanilla recipe uses only '#aether:processed/gravitite' tag.
    // We rebuild each piece to add a gold_sheet hardening slot (visible change).
    const aetherGravititeArmor = [
        { id: 'aether:gravitite_helmet',     pattern: ['GGG', 'GSG'] },
        { id: 'aether:gravitite_chestplate', pattern: ['GSG', 'GGG', 'GGG'] },
        { id: 'aether:gravitite_leggings',   pattern: ['GGG', 'GSG', 'G G'] },
        { id: 'aether:gravitite_boots',      pattern: ['GSG', 'G G'] },
        { id: 'aether:gravitite_gloves',     pattern: ['GSG'] }
    ];
    aetherGravititeArmor.forEach(armor => {
        event.remove({ output: armor.id });
        event.shaped(armor.id, armor.pattern, {
            G: '#aether:processed/gravitite',
            S: GOLD_SHEET
        }).id('arcadia:' + armor.id.split(':')[1]);
    });

    // Phoenix armor: loot-only in current Aether build (no vanilla craft), nothing to harden.

    // ============================================================
    // 28. AQUACULTURE HARDENING (neptunium tier)
    // ============================================================

    const aquaNeptuniumTools = [
        'aquaculture:neptunium_sword', 'aquaculture:neptunium_pickaxe',
        'aquaculture:neptunium_axe', 'aquaculture:neptunium_shovel',
        'aquaculture:neptunium_hoe'
    ];
    aquaNeptuniumTools.forEach(item => event.replaceInput({ output: item, allowEmpty: true }, 'minecraft:stick', REINFORCE_BLOCK));

    const aquaNeptuniumArmor = [
        'aquaculture:neptunium_helmet', 'aquaculture:neptunium_chestplate',
        'aquaculture:neptunium_leggings', 'aquaculture:neptunium_boots'
    ];
    aquaNeptuniumArmor.forEach(item => event.replaceInput({ output: item, allowEmpty: true }, 'aquaculture:neptunium_ingot', SOURCE_GEM));

    console.info("[Arcadia V2] Harder Recipes Script (Fin) Loaded!");
});
