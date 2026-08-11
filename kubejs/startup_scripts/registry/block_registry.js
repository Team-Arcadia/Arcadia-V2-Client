// Priority: 900
/**
 * @author vyrriox
 */
StartupEvents.registry('block', event => {
    event.create('arcadia:atm')
        .displayName('ATM')
        .soundType('metal')
        .hardness(5.0)
        .resistance(6.0)
        .requiresTool(true)
        .tagBlock('mineable/pickaxe')
        .tagBlock('needs_iron_tool')
        .texture('arcadia:block/atm')

    // Suppresses item magnets in a 5 chunk radius, see server_scripts/blocks/magnet_jammer.js.
    // Blast proof on purpose: a player breaking it is the only way it can leave the world,
    // which is what keeps the tracked field list in sync.
    event.create('arcadia:magnet_jammer')
        .displayName('Magnetic Jammer')
        .soundType('metal')
        .hardness(5.0)
        .resistance(1200.0)
        .requiresTool(true)
        .tagBlock('mineable/pickaxe')
        .tagBlock('needs_iron_tool')
        .texture('arcadia:block/magnet_jammer')
})
