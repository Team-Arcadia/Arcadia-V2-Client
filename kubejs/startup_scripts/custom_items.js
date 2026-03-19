// Priority: 900
/*
    Registering Custom Items for Arcadia V2.
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.
*/

StartupEvents.registry('item', event => {
    // Keys & Utility
    event.create('arcadia:basic_key').texture('arcadia:item/basic_key');
    event.create('arcadia:common_key').texture('arcadia:item/common_key');
    event.create('arcadia:rare_key').texture('arcadia:item/rare_key');
    event.create('arcadia:legendary_key').texture('arcadia:item/legendary_key');
    event.create('arcadia:arcadia_key').rarity('epic').glow(true).texture('arcadia:item/arcadia_key');
    event.create('arcadia:vote_key').texture('arcadia:item/vote_key');
    event.create('arcadia:token_casino').texture('arcadia:item/token_casino');

    // Music Discs (19 tracks)
    const discs = [
        'mike_le_loulou', 'vyrriox_trois_femmes', 'vyrriox_sac_a_gros_pt1', 'vyrriox_sac_a_gros_pt2',
        'vyrriox_patee', 'vyrriox_la_naine_pt1', 'vyrriox_la_naine_pt2', 'vyrriox_la_naine_pt3',
        'vyrriox_la_femme_de_joie', 'peter_le_frein_pt1', 'peter_le_frein_pt2', 'peter_le_frein_pt3',
        'peter_le_frein_pt4', 'peter_le_frein_pt5', 'boit_ton_picher', 'dans_la_tavern_lulu',
        'janette', 'la_boulette_pt1', 'la_boulette_pt2', 'au_pactole'
    ];

    discs.forEach(id => {
        event.create(`arcadia:music_disc_${id}`)
            .displayName('Music Disc')
            .jukeboxPlayable(`arcadia:${id}`)
            .texture('arcadia:item/music_disc_custom')
            .rarity('rare')
            .maxStackSize(1);
    });

    // Transitional Items for Sequenced Assembly
    event.create('arcadia:incomplete_netherite_block')
        .texture('minecraft:item/netherite_scrap')
        .displayName('Incomplete Netherite Block');
});
