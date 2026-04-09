/*
    Add tooltips to all Arcadia Custom Items.
    Tooltips use translation keys for FR/EN support.
    Author: vyrriox
*/
ItemEvents.modifyTooltips(event => {
    // === Keys ===
    const keys = [
        'arcadia:basic_key',
        'arcadia:common_key',
        'arcadia:rare_key',
        'arcadia:legendary_key',
        'arcadia:arcadia_key',
        'arcadia:vote_key'
    ];
    event.add(keys, Text.translate('tooltip.arcadia.key_description').gray());
    event.add('arcadia:token_casino', Text.translate('tooltip.arcadia.token_casino').gray());

    // === Fusion Core Chain - Tier 0 ===
    event.add('arcadia:alloy_blend', Text.translate('tooltip.arcadia.alloy_blend').gray());
    event.add('arcadia:diamond_matrix', Text.translate('tooltip.arcadia.diamond_matrix').aqua());
    event.add('arcadia:infused_steel', Text.translate('tooltip.arcadia.infused_steel').gray());
    event.add('arcadia:nether_concentrate', Text.translate('tooltip.arcadia.nether_concentrate').red());
    event.add('arcadia:energized_dust', Text.translate('tooltip.arcadia.energized_dust').yellow());
    event.add('arcadia:wiring_bundle', Text.translate('tooltip.arcadia.wiring_bundle').gray());

    // === Fusion Core Chain - Tier 1 ===
    event.add('arcadia:refined_alloy_ingot', Text.translate('tooltip.arcadia.refined_alloy_ingot').blue());
    event.add('arcadia:hardened_steel_compound', Text.translate('tooltip.arcadia.hardened_steel_compound').blue());
    event.add('arcadia:energized_crystal', Text.translate('tooltip.arcadia.energized_crystal').lightPurple());
    event.add('arcadia:treated_composite_plate', Text.translate('tooltip.arcadia.treated_composite_plate').blue());

    // === Fusion Core Chain - Tier 2 ===
    event.add('arcadia:quantum_circuit', Text.translate('tooltip.arcadia.quantum_circuit').green());
    event.add('arcadia:plasma_cell', Text.translate('tooltip.arcadia.plasma_cell').gold());
    event.add('arcadia:reinforced_casing', Text.translate('tooltip.arcadia.reinforced_casing').green());
    event.add('arcadia:thermal_conductor', Text.translate('tooltip.arcadia.thermal_conductor').gold());

    // === Fusion Core Chain - Tier 3 ===
    event.add('arcadia:fusion_matrix', Text.translate('tooltip.arcadia.fusion_matrix').lightPurple());
    event.add('arcadia:containment_field_generator', Text.translate('tooltip.arcadia.containment_field_generator').lightPurple());
    event.add('arcadia:neutron_reflector', Text.translate('tooltip.arcadia.neutron_reflector').lightPurple());

    // === FUSION CORE - Final ===
    event.add('arcadia:fusion_core', [
        Text.translate('tooltip.arcadia.fusion_core.1').lightPurple().bold(),
        Text.translate('tooltip.arcadia.fusion_core.2').red(),
        Text.translate('tooltip.arcadia.fusion_core.3').gray().italic()
    ]);

    // === HEART OF ARCADIA ===
    event.add('arcadia:heart_of_arcadia', [
        Text.translate('tooltip.arcadia.heart_of_arcadia.1').lightPurple().bold(),
        Text.translate('tooltip.arcadia.heart_of_arcadia.2').red().italic(),
        Text.translate('tooltip.arcadia.heart_of_arcadia.3').gold()
    ]);

    // === ADEPT ARMOR SET ===
    const adeptPieces = [
        'arcadia:adept_helmet',
        'arcadia:adept_chestplate',
        'arcadia:adept_leggings',
        'arcadia:adept_boots'
    ];
    event.add(adeptPieces, [
        Text.translate('tooltip.arcadia.adept_armor.1').darkPurple().italic(),
        Text.translate('tooltip.arcadia.adept_armor.2').red(),
        Text.translate('tooltip.arcadia.adept_armor.3').gray()
    ]);

    // === HERETIC ARMOR SET ===
    const hereticPieces = [
        'arcadia:heretic_helmet',
        'arcadia:heretic_chestplate',
        'arcadia:heretic_leggings',
        'arcadia:heretic_boots'
    ];
    event.add(hereticPieces, [
        Text.translate('tooltip.arcadia.heretic_armor.1').darkRed().italic(),
        Text.translate('tooltip.arcadia.heretic_armor.2').red(),
        Text.translate('tooltip.arcadia.heretic_armor.3').gray()
    ]);

    // === ADEPT UNIQUE ITEMS ===
    const adeptItems = [
        'adept_grimoire', 'adept_pendant', 'adept_candle', 'adept_incense', 'adept_staff',
        'adept_seal', 'adept_chalice', 'adept_orb', 'adept_scroll', 'adept_relic'
    ];
    adeptItems.forEach(id => {
        event.add(`arcadia:${id}`, Text.translate(`tooltip.arcadia.${id}`).darkPurple().italic());
    });

    // === HERETIC UNIQUE ITEMS ===
    const hereticItems = [
        'heretic_tome', 'heretic_blood_vial', 'heretic_dagger', 'heretic_chain', 'heretic_skull_totem',
        'heretic_icon', 'heretic_crystal', 'heretic_bone_charm', 'heretic_poison_flask', 'heretic_mark'
    ];
    hereticItems.forEach(id => {
        event.add(`arcadia:${id}`, Text.translate(`tooltip.arcadia.${id}`).darkRed().italic());
    });
});
