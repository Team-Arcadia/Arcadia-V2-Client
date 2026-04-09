// Botany Pots - Modded Tree Compatibility
// Adds BOP, Twilight Forest, and Ars Nouveau saplings as growable crops

ServerEvents.recipes(event => {
    const dirtSoil = '#botanypots:soil/dirt'
    const netherSoil = '#botanypots:soil/nether'
    const growTime = 12000 // 10 minutes

    // ===== Biomes O' Plenty Trees (20) =====
    const bopTrees = [
        { sapling: 'dead_sapling',           log: 'dead_log',      soil: dirtSoil  },
        { sapling: 'empyreal_sapling',       log: 'empyreal_log',  soil: dirtSoil  },
        { sapling: 'fir_sapling',            log: 'fir_log',       soil: dirtSoil  },
        { sapling: 'hellbark_sapling',       log: 'hellbark_log',  soil: netherSoil },
        { sapling: 'jacaranda_sapling',      log: 'jacaranda_log', soil: dirtSoil  },
        { sapling: 'magic_sapling',          log: 'magic_log',     soil: dirtSoil  },
        { sapling: 'mahogany_sapling',       log: 'mahogany_log',  soil: dirtSoil  },
        { sapling: 'red_maple_sapling',      log: 'maple_log',     soil: dirtSoil  },
        { sapling: 'orange_maple_sapling',   log: 'maple_log',     soil: dirtSoil  },
        { sapling: 'yellow_maple_sapling',   log: 'maple_log',     soil: dirtSoil  },
        { sapling: 'palm_sapling',           log: 'palm_log',      soil: dirtSoil  },
        { sapling: 'pine_sapling',           log: 'pine_log',      soil: dirtSoil  },
        { sapling: 'redwood_sapling',        log: 'redwood_log',   soil: dirtSoil  },
        { sapling: 'umbran_sapling',         log: 'umbran_log',    soil: dirtSoil  },
        { sapling: 'willow_sapling',         log: 'willow_log',    soil: dirtSoil  },
        { sapling: 'cypress_sapling',        log: 'minecraft:oak_log',   soil: dirtSoil  },
        { sapling: 'flowering_oak_sapling',  log: 'minecraft:oak_log',   soil: dirtSoil  },
        { sapling: 'origin_sapling',         log: 'minecraft:oak_log',   soil: dirtSoil  },
        { sapling: 'rainbow_birch_sapling',  log: 'minecraft:birch_log', soil: dirtSoil  },
        { sapling: 'snowblossom_sapling',    log: 'minecraft:oak_log',   soil: dirtSoil  }
    ]

    bopTrees.forEach(tree => {
        let saplingId = tree.sapling.includes(':') ? tree.sapling : `biomesoplenty:${tree.sapling}`
        let logId = tree.log.includes(':') ? tree.log : `biomesoplenty:${tree.log}`

        event.recipes.botanypots.crop(
            saplingId,
            tree.soil,
            DisplayState.basic(saplingId),
            [
                DropItem.item(logId, 1.0),
                DropItem.item(saplingId, 0.25),
                DropItem.item('minecraft:stick', 0.15)
            ],
            growTime,
            0.0
        )
    })

    // ===== Twilight Forest Trees (10) =====
    const tfTrees = [
        { sapling: 'twilight_oak_sapling',      log: 'twilight_oak_log' },
        { sapling: 'canopy_sapling',            log: 'canopy_log' },
        { sapling: 'mangrove_sapling',          log: 'mangrove_log' },
        { sapling: 'darkwood_sapling',          log: 'dark_log' },
        { sapling: 'time_sapling',              log: 'time_log' },
        { sapling: 'transformation_sapling',    log: 'transformation_log' },
        { sapling: 'mining_sapling',            log: 'mining_log' },
        { sapling: 'sorting_sapling',           log: 'sorting_log' },
        { sapling: 'rainbow_oak_sapling',       log: 'twilight_oak_log' },
        { sapling: 'hollow_oak_sapling',        log: 'twilight_oak_log' }
    ]

    tfTrees.forEach(tree => {
        event.recipes.botanypots.crop(
            `twilightforest:${tree.sapling}`,
            dirtSoil,
            DisplayState.basic(`twilightforest:${tree.sapling}`),
            [
                DropItem.item(`twilightforest:${tree.log}`, 1.0),
                DropItem.item(`twilightforest:${tree.sapling}`, 0.25),
                DropItem.item('minecraft:stick', 0.15)
            ],
            growTime,
            0.0
        )
    })

    // ===== Ars Nouveau Archwood Trees (4) =====
    const arsColors = ['blue', 'green', 'red', 'purple']

    arsColors.forEach(color => {
        event.recipes.botanypots.crop(
            `ars_nouveau:${color}_archwood_sapling`,
            dirtSoil,
            DisplayState.basic(`ars_nouveau:${color}_archwood_sapling`),
            [
                DropItem.item(`ars_nouveau:${color}_archwood_log`, 1.0),
                DropItem.item(`ars_nouveau:${color}_archwood_sapling`, 0.25),
                DropItem.item('minecraft:stick', 0.15)
            ],
            growTime,
            0.0
        )
    })

    console.log('[Arcadia] Botany Pots: Added 34 modded tree crops (20 BOP + 10 TF + 4 Ars Nouveau)')
})
