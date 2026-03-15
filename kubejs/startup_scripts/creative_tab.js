// Priority: 800
/*
    Register Custom Creative Tab for Arcadia.
    Optimized for Arcadia V2.
    Created by vyrriox.
*/

StartupEvents.registry('creative_mode_tab', event => {
    event.create('arcadia:main')
        .displayName('Arcadia')
        .icon(() => 'arcadia:arcadia_key')
        .content(() => [
            'arcadia:basic_key',
            'arcadia:common_key',
            'arcadia:rare_key',
            'arcadia:legendary_key',
            'arcadia:arcadia_key',
            'arcadia:vote_key',
            'arcadia:token_casino',
            // Music discs in order
            'arcadia:music_disc_mike_le_loulou',
            'arcadia:music_disc_vyrriox_trois_femmes',
            'arcadia:music_disc_vyrriox_sac_a_gros_pt1',
            'arcadia:music_disc_vyrriox_sac_a_gros_pt2',
            'arcadia:music_disc_vyrriox_patee',
            'arcadia:music_disc_vyrriox_la_naine_pt1',
            'arcadia:music_disc_vyrriox_la_naine_pt2',
            'arcadia:music_disc_vyrriox_la_naine_pt3',
            'arcadia:music_disc_vyrriox_la_femme_de_joie',
            'arcadia:music_disc_peter_le_frein_pt1',
            'arcadia:music_disc_peter_le_frein_pt2',
            'arcadia:music_disc_peter_le_frein_pt3',
            'arcadia:music_disc_peter_le_frein_pt4',
            'arcadia:music_disc_peter_le_frein_pt5',
            'arcadia:music_disc_boit_ton_picher',
            'arcadia:music_disc_dans_la_tavern_lulu',
            'arcadia:music_disc_janette',
            'arcadia:music_disc_la_boulette_pt1',
            'arcadia:music_disc_la_boulette_pt2'
        ]);
});
