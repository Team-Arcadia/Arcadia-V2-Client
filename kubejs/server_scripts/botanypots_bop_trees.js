// Botany Pots - Modded Tree Compatibility
// Adds BOP, Twilight Forest, and Ars Nouveau saplings as growable crops

ServerEvents.recipes(event => {
    const dirtSoil = '#botanypots:soil/dirt'
    const netherSoil = '#botanypots:soil/nether'
    const growTime = 12000 // 10 minutes

    // ===== Biomes O' Plenty Trees (13) =====
    const bopTrees = [
        { name: 'dead',      soil: dirtSoil  },
        { name: 'empyreal',  soil: dirtSoil  },
        { name: 'fir',       soil: dirtSoil  },
        { name: 'hellbark',  soil: netherSoil },
        { name: 'jacaranda', soil: dirtSoil  },
        { name: 'magic',     soil: dirtSoil  },
        { name: 'mahogany',  soil: dirtSoil  },
        { name: 'maple',     soil: dirtSoil  },
        { name: 'palm',      soil: dirtSoil  },
        { name: 'pine',      soil: dirtSoil  },
        { name: 'redwood',   soil: dirtSoil  },
        { name: 'umbran',    soil: dirtSoil  },
        { name: 'willow',    soil: dirtSoil  }
    ]

    bopTrees.forEach(tree => {
        event.recipes.botanypots.crop(
            `biomesoplenty:${tree.name}_sapling`,
            tree.soil,
            DisplayState.basic(`biomesoplenty:${tree.name}_sapling`),
            [
                DropItem.item(`biomesoplenty:${tree.name}_log`, 1.0),
                DropItem.item(`biomesoplenty:${tree.name}_sapling`, 0.25),
                DropItem.item('minecraft:stick', 0.15)
            ],
            growTime,
            0.0
        )
    })

    // ===== Twilight Forest Trees (10) =====
    const tfTrees = [
        'twilight_oak',
        'canopy',
        'mangrove',
        'darkwood',
        'time',
        'transformation',
        'mining',
        'sorting',
        'rainbow_oak',
        'hollow_oak'
    ]

    tfTrees.forEach(name => {
        let logName = name
        if (name === 'darkwood') logName = 'dark'
        if (name === 'hollow_oak') logName = 'twilight_oak'
        if (name === 'rainbow_oak') logName = 'twilight_oak'

        event.recipes.botanypots.crop(
            `twilightforest:${name}_sapling`,
            dirtSoil,
            DisplayState.basic(`twilightforest:${name}_sapling`),
            [
                DropItem.item(`twilightforest:${logName}_log`, 1.0),
                DropItem.item(`twilightforest:${name}_sapling`, 0.25),
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

    console.log('[Arcadia] Botany Pots: Added 27 modded tree crops (13 BOP + 10 TF + 4 Ars Nouveau)')
})
