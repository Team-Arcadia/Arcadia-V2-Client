// Priority: 950
/*
    Custom Armor Materials for Arcadia V2
    Registered via StartupEvents.registry('armor_material')
    Author: vyrriox
*/

StartupEvents.registry('armor_material', event => {
    // Adept Armor Material - Cultist/Sect
    event.create('arcadia:adept')
        .defense({ BOOTS: 2, LEGGINGS: 5, CHESTPLATE: 6, HELMET: 2, BODY: 5 })
        .enchantmentValue(15)
        .toughness(1.0)
        .knockbackResistance(0.05)

    // Heretic Armor Material - Rebel cult
    event.create('arcadia:heretic')
        .defense({ BOOTS: 2, LEGGINGS: 5, CHESTPLATE: 6, HELMET: 2, BODY: 5 })
        .enchantmentValue(15)
        .toughness(1.0)
        .knockbackResistance(0.05)

    // Echo Warden - astral plate tuned around diamond protection
    event.create('arcadia:echo_warden')
        .defense({ BOOTS: 3, LEGGINGS: 6, CHESTPLATE: 8, HELMET: 3, BODY: 8 })
        .enchantmentValue(18)
        .toughness(2.0)
        .knockbackResistance(0.08)

    // Ashen Vanguard - heavy obsidian and ember plate
    event.create('arcadia:ashen_vanguard')
        .defense({ BOOTS: 3, LEGGINGS: 6, CHESTPLATE: 8, HELMET: 3, BODY: 8 })
        .enchantmentValue(12)
        .toughness(2.5)
        .knockbackResistance(0.10)

    // Runic Mechanist - brass machinery bound with verdant magic
    event.create('arcadia:runic_mechanist')
        .defense({ BOOTS: 3, LEGGINGS: 6, CHESTPLATE: 8, HELMET: 3, BODY: 8 })
        .enchantmentValue(20)
        .toughness(2.0)
        .knockbackResistance(0.08)
})
