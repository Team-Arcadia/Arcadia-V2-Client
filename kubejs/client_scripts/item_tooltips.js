/*
    Add tooltips to Arcadia Custom Keys.
*/
ItemEvents.modifyTooltips(event => {
    const keys = [
        'arcadia:basic_key',
        'arcadia:common_key',
        'arcadia:rare_key',
        'arcadia:legendary_key',
        'arcadia:arcadia_key',
        'arcadia:vote_key'
    ];

    // Add gray description for Keys
    event.add(keys, Text.translate('tooltip.arcadia.key_description').gray());

    // Add gray description for Casino Token
    event.add('arcadia:token_casino', Text.translate('tooltip.arcadia.token_casino').gray());
});
