#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Translate chipped.json EN -> FR using rule-based token translation."""
import json
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

INPUT = r'c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/extracted_en/chipped.json'
OUTPUT = r'c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/agent_output/chipped.json'

# === MATERIALS — multi-token names first ===
# value: (french_name, gender, optional plural_form, optional starts_with_vowel)
# Multi-token must be checked before single tokens
MATERIALS_MULTI = [
    # multi-token materials, longest first
    (['stripped', 'acacia', 'log'],      ('bûche d\'acacia écorcée', 'f')),
    (['stripped', 'birch', 'log'],       ('bûche de bouleau écorcée', 'f')),
    (['stripped', 'oak', 'log'],         ('bûche de chêne écorcée', 'f')),
    (['stripped', 'spruce', 'log'],      ('bûche d\'épicéa écorcée', 'f')),
    (['stripped', 'jungle', 'log'],      ('bûche d\'acajou écorcée', 'f')),
    (['stripped', 'dark', 'oak', 'log'], ('bûche de chêne noir écorcée', 'f')),
    (['stripped', 'mangrove', 'log'],    ('bûche de palétuvier écorcée', 'f')),
    (['stripped', 'cherry', 'log'],      ('bûche de cerisier écorcée', 'f')),
    (['stripped', 'crimson', 'stem'],    ('tige cramoisie écorcée', 'f')),
    (['stripped', 'warped', 'stem'],     ('tige biscornue écorcée', 'f')),
    (['stripped', 'bamboo', 'block'],    ('bloc de bambou écorcé', 'm')),
    (['ad', 'astra', 'ochre', 'froglight'],       ('luminoraine ocre Ad Astra', 'f')),
    (['ad', 'astra', 'pearlescent', 'froglight'], ('luminoraine perlescente Ad Astra', 'f')),
    (['ad', 'astra', 'verdant', 'froglight'],     ('luminoraine verdoyante Ad Astra', 'f')),
    (['ochre', 'froglight'],         ('luminoraine ocre', 'f')),
    (['pearlescent', 'froglight'],   ('luminoraine perlescente', 'f')),
    (['verdant', 'froglight'],       ('luminoraine verdoyante', 'f')),
    (['dark', 'oak'],                ('chêne noir', 'm')),
    (['light', 'blue'],              ('bleu clair', 'm')),  # color
    (['light', 'gray'],              ('gris clair', 'm')),  # color
    (['soul', 'sand'],               ('sable des âmes', 'm')),
    (['soul', 'soil'],               ('terre des âmes', 'f')),
    (['end', 'stone'],               ('pierre de l\'End', 'f')),
    (['nether', 'wart'],             ('verrue du Nether', 'f')),
    (['nether', 'wart', 'block'],    ('bloc de verrue du Nether', 'm')),
    (['warped', 'wart', 'block'],    ('bloc de verrue biscornue', 'm')),
    (['warped', 'roots'],            ('racines biscornues', 'f', 'p')),
    (['crimson', 'roots'],           ('racines cramoisies', 'f', 'p')),
    (['nether', 'sprouts'],          ('pousses du Nether', 'f', 'p')),
    (['warped', 'fungus'],           ('champignon biscornu', 'm')),
    (['crimson', 'fungus'],          ('champignon cramoisi', 'm')),
    (['warped', 'stem'],             ('tige biscornue', 'f')),
    (['crimson', 'stem'],            ('tige cramoisie', 'f')),
    (['nether', 'bricks'],           ('briques du Nether', 'f', 'p')),
    (['red', 'nether', 'bricks'],    ('briques rouges du Nether', 'f', 'p')),
    (['cracked', 'nether', 'bricks'],('briques craquelées du Nether', 'f', 'p')),
    (['chiseled', 'nether', 'bricks'],('briques ciselées du Nether', 'f', 'p')),
    (['red', 'sand'],                ('sable rouge', 'm')),
    (['red', 'sandstone'],           ('grès rouge', 'm')),
    (['cut', 'sandstone'],           ('grès taillé', 'm')),
    (['cut', 'red', 'sandstone'],    ('grès rouge taillé', 'm')),
    (['smooth', 'sandstone'],        ('grès lisse', 'm')),
    (['smooth', 'red', 'sandstone'], ('grès rouge lisse', 'm')),
    (['chiseled', 'sandstone'],      ('grès ciselé', 'm')),
    (['chiseled', 'red', 'sandstone'],('grès rouge ciselé', 'm')),
    (['raw', 'iron'],                ('fer brut', 'm')),
    (['raw', 'gold'],                ('or brut', 'm')),
    (['raw', 'copper'],              ('cuivre brut', 'm')),
    (['raw', 'iron', 'block'],       ('bloc de fer brut', 'm')),
    (['raw', 'gold', 'block'],       ('bloc d\'or brut', 'm')),
    (['raw', 'copper', 'block'],     ('bloc de cuivre brut', 'm')),
    (['cut', 'copper'],              ('cuivre taillé', 'm')),
    (['exposed', 'copper'],          ('cuivre exposé', 'm')),
    (['weathered', 'copper'],        ('cuivre érodé', 'm')),
    (['oxidized', 'copper'],         ('cuivre oxydé', 'm')),
    (['waxed', 'copper'],            ('cuivre ciré', 'm')),
    (['gilded', 'blackstone'],       ('pierre noire dorée', 'f')),
    (['polished', 'blackstone'],     ('pierre noire polie', 'f')),
    (['polished', 'andesite'],       ('andésite polie', 'f')),
    (['polished', 'granite'],        ('granite poli', 'm')),
    (['polished', 'diorite'],        ('diorite polie', 'f')),
    (['polished', 'basalt'],         ('basalte poli', 'm')),
    (['polished', 'deepslate'],      ('ardoise des abîmes polie', 'f')),
    (['cobbled', 'deepslate'],       ('ardoise des abîmes taillée', 'f')),
    (['mossy', 'cobblestone'],       ('pierres taillées moussues', 'f', 'p')),
    (['mossy', 'stone', 'bricks'],   ('briques de pierre moussues', 'f', 'p')),
    (['cracked', 'stone', 'bricks'], ('briques de pierre craquelées', 'f', 'p')),
    (['chiseled', 'stone', 'bricks'],('briques de pierre ciselées', 'f', 'p')),
    (['stone', 'bricks'],            ('briques de pierre', 'f', 'p')),
    (['smooth', 'stone'],            ('pierre lisse', 'f')),
    (['smooth', 'basalt'],           ('basalte lisse', 'm')),
    (['smooth', 'quartz'],           ('quartz lisse', 'm')),
    (['chiseled', 'quartz', 'block'],('bloc de quartz ciselé', 'm')),
    (['quartz', 'block'],            ('bloc de quartz', 'm')),
    (['quartz', 'pillar'],           ('pilier de quartz', 'm')),
    (['quartz', 'bricks'],           ('briques de quartz', 'f', 'p')),
    (['packed', 'mud'],              ('boue compacte', 'f')),
    (['packed', 'ice'],              ('glace compactée', 'f')),
    (['blue', 'ice'],                ('glace bleue', 'f')),
    (['mud', 'bricks'],              ('briques de boue', 'f', 'p')),
    (['ice', 'bricks'],              ('briques de glace', 'f', 'p')),
    (['snow', 'block'],              ('bloc de neige', 'm')),
    (['snow', 'block', 'bricks'],    ('briques de neige', 'f', 'p')),
    (['amethyst', 'block'],          ('bloc d\'améthyste', 'm')),
    (['ancient', 'debris'],          ('débris antiques', 'm', 'p')),
    (['bone', 'block'],              ('bloc d\'os', 'm')),
    (['hay', 'block'],               ('bloc de foin', 'm')),
    (['magma', 'block'],             ('bloc de magma', 'm')),
    (['dripstone', 'block'],         ('roche concrétionnée', 'f')),
    (['mushroom', 'block'],          ('bloc de champignon', 'm')),
    (['mushroom', 'stem'],           ('tige de champignon', 'f')),
    (['red', 'mushroom'],            ('champignon rouge', 'm')),
    (['brown', 'mushroom'],          ('champignon marron', 'm')),
    (['carved', 'pumpkin'],          ('citrouille sculptée', 'f')),
    (['jack', 'o', 'lantern'],       ('citrouille-lanterne', 'f')),
    (['jack', 'o\'', 'lantern'],     ('citrouille-lanterne', 'f')),
    (['lily', 'pad'],                ('nénuphar', 'm')),
    (['iron', 'bars'],               ('barreaux de fer', 'm', 'p')),
    (['sea', 'lantern'],             ('lanterne aquatique', 'f')),
    (['redstone', 'lamp'],           ('lampe à redstone', 'f')),
    (['redstone', 'torch'],          ('torche de redstone', 'f')),
    (['soul', 'torch'],              ('torche des âmes', 'f')),
    (['soul', 'lantern'],            ('lanterne des âmes', 'f')),
    (['amethyst', 'cluster'],        ('amas d\'améthyste', 'm')),
    (['pointed', 'dripstone'],       ('roche concrétionnée pointue', 'f')),
    (['budding', 'amethyst'],        ('améthyste bourgeonnante', 'f')),
    (['suspicious', 'sand'],         ('sable suspect', 'm')),
    (['suspicious', 'gravel'],       ('gravier suspect', 'm')),
    (['crying', 'obsidian'],         ('obsidienne larmoyante', 'f')),
    (['rooted', 'dirt'],             ('terre enracinée', 'f')),
    (['coarse', 'dirt'],             ('terre stérile', 'f')),
    (['moss', 'block'],              ('bloc de mousse', 'm')),
    (['moss', 'carpet'],             ('tapis de mousse', 'm')),
    (['glow', 'lichen'],             ('lichen lumineux', 'm')),
    (['kelp'],                       ('varech', 'm')),
    (['dried', 'kelp'],              ('varech séché', 'm')),
    (['dried', 'kelp', 'block'],     ('bloc de varech séché', 'm')),
    (['dirt'],                       ('terre', 'f')),
    (['mud'],                        ('boue', 'f')),
    (['clay'],                       ('argile', 'f')),
    (['sand'],                       ('sable', 'm')),
    (['gravel'],                     ('gravier', 'm')),
    (['snow'],                       ('neige', 'f')),
    (['ice'],                        ('glace', 'f')),
    (['debris'],                     ('débris', 'm', 'p')),
    (['log'],                        ('bûche', 'f')),
    (['logs'],                       ('bûches', 'f', 'p')),
    (['leaves'],                     ('feuilles', 'f', 'p')),
    (['planks'],                     ('planches', 'f', 'p')),
    (['plank'],                      ('planche', 'f')),
    (['stem'],                       ('tige', 'f')),
    (['stems'],                      ('tiges', 'f', 'p')),
    (['roots'],                      ('racines', 'f', 'p')),
    (['sprouts'],                    ('pousses', 'f', 'p')),
    (['fungus'],                     ('champignon', 'm')),
    (['mushroom'],                   ('champignon', 'm')),
    (['mushrooms'],                  ('champignons', 'm', 'p')),
    (['vine'],                       ('liane', 'f')),
    (['vines'],                      ('lianes', 'f', 'p')),
    (['stone'],                      ('pierre', 'f')),
    (['cobblestone'],                ('pierres taillées', 'f', 'p')),
    (['granite'],                    ('granite', 'm')),
    (['andesite'],                   ('andésite', 'f')),
    (['diorite'],                    ('diorite', 'f')),
    (['deepslate'],                  ('ardoise des abîmes', 'f')),
    (['blackstone'],                 ('pierre noire', 'f')),
    (['basalt'],                     ('basalte', 'm')),
    (['sandstone'],                  ('grès', 'm')),
    (['prismarine'],                 ('prismarine', 'f')),
    (['calcite'],                    ('calcite', 'f')),
    (['tuff'],                       ('tuf', 'm')),
    (['copper'],                     ('cuivre', 'm')),
    (['iron'],                       ('fer', 'm')),
    (['gold'],                       ('or', 'm')),
    (['diamond'],                    ('diamant', 'm')),
    (['netherite'],                  ('netherite', 'f')),
    (['quartz'],                     ('quartz', 'm')),
    (['obsidian'],                   ('obsidienne', 'f')),
    (['amethyst'],                   ('améthyste', 'f')),
    (['emerald'],                    ('émeraude', 'f')),
    (['lapis'],                      ('lapis-lazuli', 'm')),
    (['redstone'],                   ('redstone', 'f')),
    (['coal'],                       ('charbon', 'm')),
    (['oak'],                        ('chêne', 'm')),
    (['birch'],                      ('bouleau', 'm')),
    (['spruce'],                     ('épicéa', 'm')),
    (['jungle'],                     ('acajou', 'm')),
    (['acacia'],                     ('acacia', 'm')),
    (['mangrove'],                   ('palétuvier', 'm')),
    (['cherry'],                     ('cerisier', 'm')),
    (['crimson'],                    ('cramoisi', 'm')),
    (['warped'],                     ('biscornu', 'm')),
    (['bamboo'],                     ('bambou', 'm')),
    (['netherrack'],                 ('netherrack', 'f')),
    (['endstone'],                   ('pierre de l\'End', 'f')),
    (['purpur'],                     ('purpur', 'm')),
    (['bone'],                       ('os', 'm')),
    (['hay'],                        ('foin', 'm')),
    (['glowstone'],                  ('pierre lumineuse', 'f')),
    (['shroomlight'],                ('shroomlight', 'm')),
    (['froglight'],                  ('luminoraine', 'f')),
    (['lodestone'],                  ('pierre de magnétite', 'f')),
    (['cobweb'],                     ('toile d\'araignée', 'f')),
    (['cobwebs'],                    ('toiles d\'araignée', 'f', 'p')),
    (['paper'],                      ('papier', 'm')),
    (['tar'],                        ('goudron', 'm')),
    (['pumpkin'],                    ('citrouille', 'f')),
    (['melon'],                      ('pastèque', 'f')),
    (['apple'],                      ('pomme', 'f')),
    (['flower'],                     ('fleur', 'f')),
    (['kelp'],                       ('varech', 'm')),
    (['sponge'],                     ('éponge', 'f')),
    (['glass'],                      ('verre', 'm')),
    (['wool'],                       ('laine', 'f')),
    (['concrete'],                   ('béton', 'm')),
    (['terracotta'],                 ('terre cuite', 'f')),
    (['carpet'],                     ('tapis', 'm')),
    (['ladder'],                     ('échelle', 'f')),
    (['torch'],                      ('torche', 'f')),
    (['lantern'],                    ('lanterne', 'f')),
    (['barrel'],                     ('tonneau', 'm')),
    (['crate'],                      ('caisse', 'f')),
    (['bookshelf'],                  ('bibliothèque', 'f')),
]

# Color mapping: (m, f) — used when prefix appears
COLORS = {
    'white':      ('blanc', 'blanche'),
    'orange':     ('orange', 'orange'),
    'magenta':    ('magenta', 'magenta'),
    'yellow':     ('jaune', 'jaune'),
    'lime':       ('vert clair', 'vert clair'),
    'pink':       ('rose', 'rose'),
    'gray':       ('gris', 'grise'),
    'cyan':       ('cyan', 'cyan'),
    'purple':     ('violet', 'violette'),
    'blue':       ('bleu', 'bleue'),
    'brown':      ('marron', 'marron'),
    'green':      ('vert', 'verte'),
    'red':        ('rouge', 'rouge'),
    'black':      ('noir', 'noire'),
}
COLOR_MULTI = {
    ('light', 'blue'): ('bleu clair', 'bleu clair'),
    ('light', 'gray'): ('gris clair', 'gris clair'),
}

# === BASE TYPES — what the block IS (suffix to consume) ===
# (eng_tokens_tuple): (french_phrase, gender, plural?)
# Order matters — multi-token first
BASES_MULTI = [
    (['glass', 'pane'],         ('vitre', 'f')),
    (['glass', 'panes'],        ('vitres', 'f', 'p')),
    (['stained', 'glass', 'pane'], ('vitre teintée', 'f')),
    (['stained', 'glass', 'panes'], ('vitres teintées', 'f', 'p')),
    (['stained', 'glass'],      ('verre teinté', 'm')),
    (['glazed', 'terracotta'],  ('terre cuite émaillée', 'f')),
    (['fence', 'gate'],         ('portail', 'm')),
    (['pressure', 'plate'],     ('plaque de pression', 'f')),
    (['pillar', 'top'],         ('sommet de pilier', 'm')),
    (['mini', 'tiles'],         ('mini tuiles', 'f', 'p')),
    (['lily', 'pad'],           ('nénuphar', 'm')),
    (['iron', 'bars'],          ('barreaux de fer', 'm', 'p')),
    (['sea', 'lantern'],        ('lanterne aquatique', 'f')),
    (['redstone', 'lamp'],      ('lampe à redstone', 'f')),
    (['redstone', 'torch'],     ('torche de redstone', 'f')),
    (['soul', 'torch'],         ('torche des âmes', 'f')),
    (['soul', 'lantern'],       ('lanterne des âmes', 'f')),
    (['paper', 'lantern'],      ('lanterne en papier', 'f')),
    (['amethyst', 'cluster'],   ('amas d\'améthyste', 'm')),
    (['nether', 'sprouts'],     ('pousses du Nether', 'f', 'p')),
    (['warped', 'roots'],       ('racines biscornues', 'f', 'p')),
    (['crimson', 'roots'],      ('racines cramoisies', 'f', 'p')),
    (['mushroom', 'block'],     ('bloc de champignon', 'm')),
    (['mushroom', 'stem'],      ('tige de champignon', 'f')),
    (['mushroom'],              ('champignon', 'm')),
    (['scales'],                ('écailles', 'f', 'p')),
    (['remnants'],              ('restes', 'm', 'p')),
    (['carving'],               ('sculpture', 'f')),
    (['column'],                ('colonne', 'f')),
    (['mosaic'],                ('mosaïque', 'f')),
    (['shavings'],              ('copeaux', 'm', 'p')),
    (['panel'],                 ('panneau', 'm')),
    (['panels'],                ('panneaux', 'm', 'p')),
    (['mini', 'tile'],          ('mini tuile', 'f')),
    (['slab'],                  ('dalle', 'f')),
    (['slabs'],                 ('dalles', 'f', 'p')),
    (['stairs'],                ('escalier', 'm')),
    (['wall'],                  ('mur', 'm')),
    (['fence'],                 ('barrière', 'f')),
    (['door'],                  ('porte', 'f')),
    (['doors'],                 ('portes', 'f', 'p')),
    (['trapdoor'],              ('trappe', 'f')),
    (['trapdoors'],             ('trappes', 'f', 'p')),
    (['button'],                ('bouton', 'm')),
    (['sign'],                  ('panneau', 'm')),
    (['pillar'],                ('pilier', 'm')),
    (['bricks'],                ('briques', 'f', 'p')),
    (['brick'],                 ('brique', 'f')),
    (['tiles'],                 ('tuiles', 'f', 'p')),
    (['tile'],                  ('tuile', 'f')),
    (['carpet'],                ('tapis', 'm')),
    (['carpets'],               ('tapis', 'm', 'p')),
    (['lantern'],               ('lanterne', 'f')),
    (['lanterns'],              ('lanternes', 'f', 'p')),
    (['lamp'],                  ('lampe', 'f')),
    (['lamps'],                 ('lampes', 'f', 'p')),
    (['torch'],                 ('torche', 'f')),
    (['torches'],               ('torches', 'f', 'p')),
    (['barrel'],                ('tonneau', 'm')),
    (['barrels'],               ('tonneaux', 'm', 'p')),
    (['crate'],                 ('caisse', 'f')),
    (['ladder'],                ('échelle', 'f')),
    (['ladders'],               ('échelles', 'f', 'p')),
    (['bookshelf'],             ('bibliothèque', 'f')),
    (['bookshelves'],           ('bibliothèques', 'f', 'p')),
    (['pane'],                  ('vitre', 'f')),
    (['panes'],                 ('vitres', 'f', 'p')),
    (['plank'],                 ('planche', 'f')),
    (['planks'],                ('planches', 'f', 'p')),
    (['log'],                   ('bûche', 'f')),
    (['logs'],                  ('bûches', 'f', 'p')),
    (['wood'],                  ('bois', 'm')),
    (['leaves'],                ('feuilles', 'f', 'p')),
    (['block'],                 ('bloc', 'm')),
    (['blocks'],                ('blocs', 'm', 'p')),
    (['glass'],                 ('verre', 'm')),
    (['wool'],                  ('laine', 'f')),
    (['concrete'],              ('béton', 'm')),
    (['terracotta'],            ('terre cuite', 'f')),
    (['stem'],                  ('tige', 'f')),
    (['stems'],                 ('tiges', 'f', 'p')),
    (['roots'],                 ('racines', 'f', 'p')),
    (['sprouts'],               ('pousses', 'f', 'p')),
    (['vine'],                  ('liane', 'f')),
    (['vines'],                 ('lianes', 'f', 'p')),
    (['cobweb'],                ('toile d\'araignée', 'f')),
    (['cobwebs'],               ('toiles d\'araignée', 'f', 'p')),
    (['leaf'],                  ('feuille', 'f')),
    (['top'],                   ('sommet', 'm')),
    (['mushrooms'],             ('champignons', 'm', 'p')),
    (['froglights'],            ('luminoraines', 'f', 'p')),
    (['froglight'],             ('luminoraine', 'f')),
    (['shroomlights'],          ('shroomlights', 'm', 'p')),
    (['shroomlight'],           ('shroomlight', 'm')),
    (['lodestone'],             ('pierre de magnétite', 'f')),
    (['multimeter'],            ('multimètre', 'm')),
]

# === ADJECTIVES — translate words that AREN'T material/base ===
# (m_form, f_form, position) - position 'before' is for short common adjs
ADJECTIVES = {
    'classic':       ('classique', 'classique', 'after'),
    'modern':        ('moderne', 'moderne', 'after'),
    'rustic':        ('rustique', 'rustique', 'after'),
    'simple':        ('simple', 'simple', 'after'),
    'ornate':        ('orné', 'ornée', 'after'),
    'fancy':         ('fantaisie', 'fantaisie', 'after'),
    'antique':       ('antique', 'antique', 'after'),
    'historical':    ('historique', 'historique', 'after'),
    'victorian':     ('victorien', 'victorienne', 'after'),
    'traditional':   ('traditionnel', 'traditionnelle', 'after'),
    'bulk':          ('massif', 'massive', 'after'),
    'mesh':          ('maillé', 'maillée', 'after'),
    'meshed':        ('maillé', 'maillée', 'after'),
    'mosaic':        ('en mosaïque', 'en mosaïque', 'after'),
    'paneled':       ('à panneaux', 'à panneaux', 'after'),
    'panelled':      ('à panneaux', 'à panneaux', 'after'),
    'airy':          ('aéré', 'aérée', 'after'),
    'tall':          ('haut', 'haute', 'after'),
    'small':         ('petit', 'petite', 'before'),
    'big':           ('grand', 'grande', 'before'),
    'large':         ('grand', 'grande', 'before'),
    'tiny':          ('minuscule', 'minuscule', 'after'),
    'mini':          ('mini', 'mini', 'after'),
    'micro':         ('micro', 'micro', 'after'),
    'short':         ('court', 'courte', 'after'),
    'long':          ('long', 'longue', 'after'),
    'thin':          ('fin', 'fine', 'after'),
    'thick':         ('épais', 'épaisse', 'after'),
    'thicc':         ('épais', 'épaisse', 'after'),
    'wide':          ('large', 'large', 'after'),
    'wider':         ('plus large', 'plus large', 'after'),
    'flat':          ('plat', 'plate', 'after'),
    'soft':          ('mou', 'molle', 'after'),
    'rough':         ('rugueux', 'rugueuse', 'after'),
    'rought':        ('rugueux', 'rugueuse', 'after'),
    'hard':          ('dur', 'dure', 'after'),
    'hardened':      ('durci', 'durcie', 'after'),
    'fine':          ('fin', 'fine', 'after'),
    'heavy':         ('lourd', 'lourde', 'after'),
    'compact':       ('compact', 'compacte', 'after'),
    'dense':         ('dense', 'dense', 'after'),
    'solid':         ('solide', 'solide', 'after'),
    'sturdy':        ('robuste', 'robuste', 'after'),
    'strong':        ('robuste', 'robuste', 'after'),
    'reinforced':    ('renforcé', 'renforcée', 'after'),
    'fortified':     ('fortifié', 'fortifiée', 'after'),
    'supported':     ('soutenu', 'soutenue', 'after'),
    'smooth':        ('lisse', 'lisse', 'after'),
    'smoothed':      ('lissé', 'lissée', 'after'),
    'polished':      ('poli', 'polie', 'after'),
    'rounded':       ('arrondi', 'arrondie', 'after'),
    'round':         ('rond', 'ronde', 'after'),
    'square':        ('carré', 'carrée', 'after'),
    'rectangle':     ('rectangulaire', 'rectangulaire', 'after'),
    'triangular':    ('triangulaire', 'triangulaire', 'after'),
    'hexagonical':   ('hexagonal', 'hexagonale', 'after'),
    'circular':      ('circulaire', 'circulaire', 'after'),
    'cubed':         ('cubique', 'cubique', 'after'),
    'curly':         ('bouclé', 'bouclée', 'after'),
    'curled':        ('enroulé', 'enroulée', 'after'),
    'curvy':         ('sinueux', 'sinueuse', 'after'),
    'arched':        ('arqué', 'arquée', 'after'),
    'arch':          ('en arc', 'en arc', 'after'),
    'striped':       ('rayé', 'rayée', 'after'),
    'stiped':        ('rayé', 'rayée', 'after'),
    'lined':         ('ligné', 'lignée', 'after'),
    'line':          ('en ligne', 'en ligne', 'after'),
    'checkered':     ('à damiers', 'à damiers', 'after'),
    'dotted':        ('pointillé', 'pointillée', 'after'),
    'dot':           ('à points', 'à points', 'after'),
    'spotted':       ('moucheté', 'mouchetée', 'after'),
    'speckled':      ('tacheté', 'tachetée', 'after'),
    'freckled':      ('moucheté', 'mouchetée', 'after'),
    'patterned':     ('à motifs', 'à motifs', 'after'),
    'patched':       ('rapiécé', 'rapiécée', 'after'),
    'webbed':        ('toilé', 'toilée', 'after'),
    'paved':         ('pavé', 'pavée', 'after'),
    'tiled':         ('carrelé', 'carrelée', 'after'),
    'herringbone':   ('en chevrons', 'en chevrons', 'after'),
    'cross':         ('en croix', 'en croix', 'after'),
    'crossed':       ('croisé', 'croisée', 'after'),
    'crossbolted':   ('boulonné en croix', 'boulonnée en croix', 'after'),
    'diagonal':      ('diagonal', 'diagonale', 'after'),
    'vertical':      ('vertical', 'verticale', 'after'),
    'vertically':    ('verticalement', 'verticalement', 'after'),
    'horizontal':    ('horizontal', 'horizontale', 'after'),
    'offset':        ('décalé', 'décalée', 'after'),
    'shifted':       ('décalé', 'décalée', 'after'),
    'centered':      ('centré', 'centrée', 'after'),
    'center':        ('central', 'centrale', 'after'),
    'cornered':      ('en coin', 'en coin', 'after'),
    'edged':         ('bordé', 'bordée', 'after'),
    'edge':          ('à bord', 'à bord', 'after'),
    'bordered':      ('bordé', 'bordée', 'after'),
    'borderless':    ('sans bordure', 'sans bordure', 'after'),
    'framed':        ('encadré', 'encadrée', 'after'),
    'ringed':        ('cerclé', 'cerclée', 'after'),
    'ring':          ('en anneau', 'en anneau', 'after'),
    'circle':        ('en cercle', 'en cercle', 'after'),
    'spiraled':      ('spiralé', 'spiralée', 'after'),
    'spiral':        ('en spirale', 'en spirale', 'after'),
    'twisted':       ('tordu', 'tordue', 'after'),
    'crooked':       ('tordu', 'tordue', 'after'),
    'slanted':       ('incliné', 'inclinée', 'after'),
    'leaning':       ('penché', 'penchée', 'after'),
    'stacked':       ('empilé', 'empilée', 'after'),
    'layered':       ('en couches', 'en couches', 'after'),
    'layed':         ('posé', 'posée', 'after'),
    'placed':        ('placé', 'placée', 'after'),
    'pressed':       ('pressé', 'pressée', 'after'),
    'pegged':        ('chevillé', 'chevillée', 'after'),
    'nailed':        ('cloué', 'clouée', 'after'),
    'bolted':        ('boulonné', 'boulonnée', 'after'),
    'tied':          ('ficelé', 'ficelée', 'after'),
    'roped':         ('cordé', 'cordée', 'after'),
    'rope':          ('en corde', 'en corde', 'after'),
    'chained':       ('enchaîné', 'enchaînée', 'after'),
    'linked':        ('lié', 'liée', 'after'),
    'bundled':       ('groupé', 'groupée', 'after'),
    'bond':          ('lié', 'liée', 'after'),
    'overlapping':   ('superposé', 'superposée', 'after'),
    'crated':        ('encaissé', 'encaissée', 'after'),
    'boxed':         ('en boîte', 'en boîte', 'after'),
    'enclosed':      ('clos', 'close', 'after'),
    'sided':         ('à côtés', 'à côtés', 'after'),
    'sides':         ('à côtés', 'à côtés', 'after'),
    'side':          ('latéral', 'latérale', 'after'),
    'planked':       ('en planches', 'en planches', 'after'),
    'carved':        ('sculpté', 'sculptée', 'after'),
    'chiseled':      ('ciselé', 'ciselée', 'after'),
    'engraved':      ('gravé', 'gravée', 'after'),
    'etched':        ('gravé', 'gravée', 'after'),
    'embossed':      ('embossé', 'embossée', 'after'),
    'inscribed':     ('inscrit', 'inscrite', 'after'),
    'inlayed':       ('incrusté', 'incrustée', 'after'),
    'detailed':      ('détaillé', 'détaillée', 'after'),
    'decorated':     ('décoré', 'décorée', 'after'),
    'cracked':       ('craquelé', 'craquelée', 'after'),
    'crumbled':      ('effrité', 'effritée', 'after'),
    'eroded':        ('érodé', 'érodée', 'after'),
    'damaged':       ('endommagé', 'endommagée', 'after'),
    'fractured':     ('fracturé', 'fracturée', 'after'),
    'distorted':     ('déformé', 'déformée', 'after'),
    'broken':        ('brisé', 'brisée', 'after'),
    'mangled':       ('déchiqueté', 'déchiquetée', 'after'),
    'crusted':       ('encroûté', 'encroûtée', 'after'),
    'crunched':      ('écrasé', 'écrasée', 'after'),
    'crunchy':       ('croustillant', 'croustillante', 'after'),
    'rotted':        ('pourri', 'pourrie', 'after'),
    'rotten':        ('pourri', 'pourrie', 'after'),
    'ancient':       ('antique', 'antique', 'before'),
    'old':           ('ancien', 'ancienne', 'after'),
    'weathered':     ('érodé', 'érodée', 'after'),
    'exposed':       ('exposé', 'exposée', 'after'),
    'oxidized':      ('oxydé', 'oxydée', 'after'),
    'waxed':         ('ciré', 'cirée', 'after'),
    'rusted':        ('rouillé', 'rouillée', 'after'),
    'scabbed':       ('croûté', 'croûtée', 'after'),
    'dirty':         ('sale', 'sale', 'after'),
    'grimy':         ('crasseux', 'crasseuse', 'after'),
    'dusty':         ('poussiéreux', 'poussiéreuse', 'after'),
    'dusted':        ('poussiéreux', 'poussiéreuse', 'after'),
    'muddy':         ('boueux', 'boueuse', 'after'),
    'sandy':         ('sablonneux', 'sablonneuse', 'after'),
    'wet':           ('mouillé', 'mouillée', 'after'),
    'dried':         ('séché', 'séchée', 'after'),
    'fired':         ('cuit', 'cuite', 'after'),
    'frosted':       ('givré', 'givrée', 'after'),
    'seared':        ('saisi', 'saisie', 'after'),
    'burning':       ('enflammé', 'enflammée', 'after'),
    'glowing':       ('luminescent', 'luminescente', 'after'),
    'glow':          ('lueur', 'lueur', 'after'),
    'shimmering':    ('scintillant', 'scintillante', 'after'),
    'lighted':       ('éclairé', 'éclairée', 'after'),
    'mossy':         ('moussu', 'moussue', 'after'),
    'overgrown':     ('envahi', 'envahie', 'after'),
    'rooted':        ('enraciné', 'enracinée', 'after'),
    'leafy':         ('feuillu', 'feuillue', 'after'),
    'flowery':       ('fleuri', 'fleurie', 'after'),
    'flowered':      ('fleuri', 'fleurie', 'after'),
    'flowering':     ('fleuri', 'fleurie', 'after'),
    'floral':        ('floral', 'florale', 'after'),
    'fertile':       ('fertile', 'fertile', 'after'),
    'natural':       ('naturel', 'naturelle', 'after'),
    'lush':          ('luxuriant', 'luxuriante', 'after'),
    'wilted':        ('flétri', 'flétrie', 'after'),
    'dead':          ('mort', 'morte', 'after'),
    'pale':          ('pâle', 'pâle', 'after'),
    'pointed':       ('pointu', 'pointue', 'after'),
    'piked':         ('piqué', 'piquée', 'after'),
    'thorned':       ('épineux', 'épineuse', 'after'),
    'horned':        ('cornu', 'cornue', 'after'),
    'sprouting':     ('germant', 'germante', 'after'),
    'creeping':      ('rampant', 'rampante', 'after'),
    'creepy':        ('flippant', 'flippante', 'after'),
    'creeper':       ('creeper', 'creeper', 'after'),
    'spider':        ('araignée', 'araignée', 'after'),
    'happy':         ('heureux', 'heureuse', 'after'),
    'sad':           ('triste', 'triste', 'after'),
    'glad':          ('content', 'contente', 'after'),
    'angry':         ('en colère', 'en colère', 'after'),
    'anguished':     ('angoissé', 'angoissée', 'after'),
    'unamused':      ('mécontent', 'mécontente', 'after'),
    'overjoyed':     ('ravi', 'ravie', 'after'),
    'horrified':     ('horrifié', 'horrifiée', 'after'),
    'scared':        ('apeuré', 'apeurée', 'after'),
    'patient':       ('patient', 'patiente', 'after'),
    'wise':          ('sage', 'sage', 'after'),
    'devious':       ('sournois', 'sournoise', 'after'),
    'cute':          ('mignon', 'mignonne', 'after'),
    'silly':         ('idiot', 'idiote', 'after'),
    'spooky':        ('effrayant', 'effrayante', 'after'),
    'smiling':       ('souriant', 'souriante', 'after'),
    'smile':         ('au sourire', 'au sourire', 'after'),
    'smug':          ('suffisant', 'suffisante', 'after'),
    'watching':      ('observant', 'observante', 'after'),
    'stern':         ('sévère', 'sévère', 'after'),
    'meming':        ('meme', 'meme', 'after'),
    'duh':           ('blasé', 'blasée', 'after'),
    'owo':           ('owo', 'owo', 'after'),
    'pacman':        ('Pac-Man', 'Pac-Man', 'after'),
    'corny':         ('ringard', 'ringarde', 'after'),
    'wicked':        ('méchant', 'méchante', 'after'),
    'reanimated':    ('réanimé', 'réanimée', 'after'),
    'poisonous':     ('toxique', 'toxique', 'after'),
    'rich':          ('riche', 'riche', 'after'),
    'safe':          ('sûr', 'sûre', 'after'),
    'sweet':         ('sucré', 'sucrée', 'after'),
    'warm':          ('chaud', 'chaude', 'after'),
    'sunny':         ('ensoleillé', 'ensoleillée', 'after'),
    'starry':        ('étoilé', 'étoilée', 'after'),
    'star':          ('en étoile', 'en étoile', 'after'),
    'snowflake':     ('flocon', 'flocon', 'after'),
    'umbrella':      ('parapluie', 'parapluie', 'after'),
    'whirlwind':     ('tourbillon', 'tourbillon', 'after'),
    'tropics':       ('tropiques', 'tropiques', 'after'),
    'beach':         ('plage', 'plage', 'after'),
    'desert':        ('désert', 'désert', 'after'),
    'pearl':         ('perle', 'perle', 'after'),
    'woven':         ('tissé', 'tissée', 'after'),
    'woved':         ('tissé', 'tissée', 'after'),
    'weaved':        ('tissé', 'tissée', 'after'),
    'wickered':      ('en osier', 'en osier', 'after'),
    'knitted':       ('tricoté', 'tricotée', 'after'),
    'quilted':       ('matelassé', 'matelassée', 'after'),
    'stringed':      ('cordé', 'cordée', 'after'),
    'stringy':       ('filandreux', 'filandreuse', 'after'),
    'tripped':       ('trippé', 'trippée', 'after'),
    'ribbled':       ('strié', 'striée', 'after'),
    'ropeplank':     ('en planche cordée', 'en planche cordée', 'after'),
    'hewn':          ('équarri', 'équarrie', 'after'),
    'sanded':        ('poncé', 'poncée', 'after'),
    'cut':           ('taillé', 'taillée', 'after'),
    'stripped':      ('écorcé', 'écorcée', 'after'),
    'haired':        ('poilu', 'poilue', 'after'),
    'harsh':         ('rude', 'rude', 'after'),
    'crafted':       ('façonné', 'façonnée', 'after'),
    'warty':         ('verruqueux', 'verruqueuse', 'after'),
    'warted':        ('verruqueux', 'verruqueuse', 'after'),
    'shroomy':       ('champignonneux', 'champignonneuse', 'after'),
    'shrooming':     ('champignonneux', 'champignonneuse', 'after'),
    'windowed':      ('vitré', 'vitrée', 'after'),
    'window':        ('à fenêtre', 'à fenêtre', 'after'),
    'shuttered':     ('à volets', 'à volets', 'after'),
    'sliding':       ('coulissant', 'coulissante', 'after'),
    'barred':        ('barré', 'barrée', 'after'),
    'bared':         ('à barreaux', 'à barreaux', 'after'),
    'bars':          ('à barreaux', 'à barreaux', 'after'),
    'barbed':        ('barbelé', 'barbelée', 'after'),
    'gated':         ('à portail', 'à portail', 'after'),
    'keyhole':       ('à serrure', 'à serrure', 'after'),
    'sighthole':     ('à judas', 'à judas', 'after'),
    'screen':        ('écran', 'écran', 'after'),
    'grid':          ('en grille', 'en grille', 'after'),
    'grill':         ('en grill', 'en grill', 'after'),
    'cage':          ('en cage', 'en cage', 'after'),
    'gilded':        ('doré', 'dorée', 'after'),
    'golden':        ('doré', 'dorée', 'after'),
    'plated':        ('plaqué', 'plaquée', 'after'),
    'wrought':       ('forgé', 'forgée', 'after'),
    'metal':         ('métallique', 'métallique', 'after'),
    'wooden':        ('en bois', 'en bois', 'after'),
    'leaded':        ('plombé', 'plombée', 'after'),
    'lead':          ('en plomb', 'en plomb', 'after'),
    'varnished':     ('verni', 'vernie', 'after'),
    'glazed':        ('émaillé', 'émaillée', 'after'),
    'stained':       ('teinté', 'teintée', 'after'),
    'clear':         ('transparent', 'transparente', 'after'),
    'tinted':        ('teinté', 'teintée', 'after'),
    'faded':         ('délavé', 'délavée', 'after'),
    'high':          ('haut', 'haute', 'after'),
    'pointless':     ('sans pointe', 'sans pointe', 'after'),
    'symbol':        ('symbole', 'symbole', 'after'),
    'symbolic':      ('symbolique', 'symbolique', 'after'),
    'sigil':         ('sigil', 'sigil', 'after'),
    'rune':          ('rune', 'rune', 'after'),
    'runic':         ('runique', 'runique', 'after'),
    'lightstick':    ('bâton lumineux', 'bâton lumineux', 'after'),
    'light':         ('lumineux', 'lumineuse', 'after'),
    'dark':          ('sombre', 'sombre', 'before'),
    'bright':        ('lumineux', 'lumineuse', 'after'),
    'shrunken':      ('rétréci', 'rétrécie', 'after'),
    'minimized':     ('minimisé', 'minimisée', 'after'),
    'stretched':     ('étiré', 'étirée', 'after'),
    'massive':       ('massif', 'massive', 'after'),
    'giant':         ('géant', 'géante', 'after'),
    'porous':        ('poreux', 'poreuse', 'after'),
    'half':          ('demi', 'demie', 'before'),
    'full':          ('plein', 'pleine', 'after'),
    'empty':         ('vide', 'vide', 'after'),
    'single':        ('simple', 'simple', 'after'),
    'double':        ('double', 'double', 'after'),
    'dual':          ('dual', 'dual', 'after'),
    'trio':          ('en trio', 'en trio', 'after'),
    'quad':          ('quadruple', 'quadruple', 'after'),
    'two':           ('deux', 'deux', 'before'),
    'all':           ('tous', 'toutes', 'before'),
    'inverted':      ('inversé', 'inversée', 'after'),
    'upside':        ('à l\'envers', 'à l\'envers', 'after'),
    'down':          ('à l\'envers', 'à l\'envers', 'after'),
    'top':           ('haut', 'haut', 'after'),
    'ad':            ('Ad', 'Ad', 'before'),
    'astra':         ('Astra', 'Astra', 'before'),
    'ochre':         ('ocre', 'ocre', 'after'),
    'pearlescent':   ('perlescent', 'perlescente', 'after'),
    'verdant':       ('verdoyant', 'verdoyante', 'after'),
    'crying':        ('larmoyant', 'larmoyante', 'after'),
    'budding':       ('bourgeonnant', 'bourgeonnante', 'after'),
    'bud':           ('bourgeon', 'bourgeon', 'after'),
    'bulb':          ('bulbe', 'bulbe', 'after'),
    'bulbed':        ('bulbeux', 'bulbeuse', 'after'),
    'bulby':         ('bulbeux', 'bulbeuse', 'after'),
    'cluster':       ('amas', 'amas', 'after'),
    'clustered':     ('en amas', 'en amas', 'after'),
    'sticky':        ('collant', 'collante', 'after'),
    'jack':          ('Jack', 'Jack', 'before'),
    'fresh':         ('frais', 'fraîche', 'after'),
    'preview':       ('aperçu', 'aperçu', 'after'),
    'special':       ('spécial', 'spéciale', 'after'),
    'secret':        ('secret', 'secrète', 'after'),
    'loreful':       ('légendaire', 'légendaire', 'after'),
    'loose':         ('lâche', 'lâche', 'after'),
    'bushel':        ('boisseau', 'boisseau', 'after'),
    'bushy':         ('touffu', 'touffue', 'after'),
    'bloomed':       ('épanoui', 'épanouie', 'after'),
    'blooming':      ('épanoui', 'épanouie', 'after'),
    'bloom':         ('floraison', 'floraison', 'after'),
    'bubbling':      ('bouillonnant', 'bouillonnante', 'after'),
    'blank':         ('vierge', 'vierge', 'after'),
    'blobby':        ('informe', 'informe', 'after'),
    'bolby':         ('informe', 'informe', 'after'),
    'blocky':        ('cubique', 'cubique', 'after'),
    'boarded':       ('barricadé', 'barricadée', 'after'),
    'botanical':     ('botanique', 'botanique', 'after'),
    'bowl':          ('en bol', 'en bol', 'after'),
    'fish':          ('poisson', 'poisson', 'after'),
    'corrupted':     ('corrompu', 'corrompue', 'after'),
    'elemental':     ('élémentaire', 'élémentaire', 'after'),
    'ender':         ('de l\'End', 'de l\'End', 'after'),
    'time':          ('temporel', 'temporelle', 'after'),
    'erratic':       ('erratique', 'erratique', 'after'),
    'pancake':       ('crêpe', 'crêpe', 'after'),
    'donut':         ('beignet', 'beignet', 'after'),
    'fruit':         ('fruit', 'fruit', 'after'),
    'nice':          ('sympa', 'sympa', 'after'),
    'eye':           ('œil', 'œil', 'after'),
    'eyed':          ('aux yeux', 'aux yeux', 'after'),
    'kitty':         ('chat', 'chat', 'after'),
    'heart':         ('cœur', 'cœur', 'after'),
    'autumnkin':     ('Autumnkin', 'Autumnkin', 'after'),
    'rosekin':       ('Rosekin', 'Rosekin', 'after'),
    'lumpkin':       ('Lumpkin', 'Lumpkin', 'after'),
    'pimpkin':       ('Pimpkin', 'Pimpkin', 'after'),
    'kabotchkin':    ('Kabotchkin', 'Kabotchkin', 'after'),
    'goldkin':       ('Goldkin', 'Goldkin', 'after'),
    'dewkin':        ('Dewkin', 'Dewkin', 'after'),
    'boo':           ('Boo', 'Boo', 'after'),
    'franken':       ('Franken', 'Franken', 'after'),
    'grizly':        ('grisâtre', 'grisâtre', 'after'),
    'grown':         ('cultivé', 'cultivée', 'after'),
    'harp':          ('en harpe', 'en harpe', 'after'),
    'hanging':       ('suspendu', 'suspendue', 'after'),
    'hazard':        ('de danger', 'de danger', 'after'),
    'hooded':        ('à capuche', 'à capuche', 'after'),
    'ivy':           ('au lierre', 'au lierre', 'after'),
    'knotted':       ('noué', 'nouée', 'after'),
    'laced':         ('lacé', 'lacée', 'after'),
    'lauching':      ('rieur', 'rieuse', 'after'),
    'lit':           ('allumé', 'allumée', 'after'),
    'loded':         ('chargé', 'chargée', 'after'),
    'lumpy':         ('grumeleux', 'grumeleuse', 'after'),
    'mixed':         ('mixte', 'mixte', 'after'),
    'paddle':        ('palette', 'palette', 'after'),
    'pikes':         ('à piques', 'à piques', 'after'),
    'rectangle':     ('rectangulaire', 'rectangulaire', 'after'),
    'ripe':          ('mûr', 'mûre', 'after'),
    'sheet':         ('en feuille', 'en feuille', 'after'),
    'shelved':       ('en étagère', 'en étagère', 'after'),
    'sifted':        ('tamisé', 'tamisée', 'after'),
    'slight':        ('léger', 'légère', 'after'),
    'slotted':       ('rainuré', 'rainurée', 'after'),
    'spongy':        ('spongieux', 'spongieuse', 'after'),
    'sprinkled':     ('saupoudré', 'saupoudrée', 'after'),
    'stepped':       ('en marches', 'en marches', 'after'),
    'sugarcane':     ('en canne à sucre', 'en canne à sucre', 'after'),
    'suspicious':    ('suspect', 'suspecte', 'after'),
    'swampy':        ('marécageux', 'marécageuse', 'after'),
    'tube':          ('en tube', 'en tube', 'after'),
    'tubed':         ('tubulaire', 'tubulaire', 'after'),
    'trampled':      ('piétiné', 'piétinée', 'after'),
    'wiggly':        ('ondulé', 'ondulée', 'after'),
    'wired':         ('câblé', 'câblée', 'after'),
    'wither':        ('wither', 'wither', 'after'),
    'young':         ('jeune', 'jeune', 'before'),
    'zippered':      ('zippé', 'zippée', 'after'),
    'spaced':        ('espacé', 'espacée', 'after'),
    'stop':          ('d\'arrêt', 'd\'arrêt', 'after'),
    'tar':           ('au goudron', 'au goudron', 'after'),
    'umbrella':      ('parapluie', 'parapluie', 'after'),
    'vined':         ('couvert de lianes', 'couverte de lianes', 'after'),
    'warning':       ('d\'avertissement', 'd\'avertissement', 'after'),
    'waved':         ('ondulé', 'ondulée', 'after'),
    'firewood':      ('en bois de feu', 'en bois de feu', 'after'),
    'mangled':       ('emmêlé', 'emmêlée', 'after'),
    'remnants':      ('vestiges', 'vestiges', 'after'),
    'pressed':       ('pressé', 'pressée', 'after'),
    'i':             ('I', 'I', 'before'),
    'k':             ('K', 'K', 'before'),
    'l':             ('L', 'L', 'before'),
    'm':             ('M', 'M', 'before'),
    'd':             ('D', 'D', 'before'),
    'f':             ('F', 'F', 'before'),
    'o':             ('O', 'O', 'before'),
    "o'":            ("O'", "O'", 'before'),
    'arrow':         ('flèche', 'flèche', 'after'),
    'shack':         ('cabane', 'cabane', 'after'),
    'pearl':         ('perlé', 'perlée', 'after'),
    'pad':           ('coussin', 'coussin', 'after'),
    'wart':          ('verrue', 'verrue', 'after'),
    'bramble':       ('ronces', 'ronces', 'after'),
    'pikes':         ('à piques', 'à piques', 'after'),
    'multi':         ('multi', 'multi', 'before'),
    'scaled':        ('écaillé', 'écaillée', 'after'),
    'scaly':         ('écailleux', 'écailleuse', 'after'),
    'flimsy':        ('fragile', 'fragile', 'after'),
    'scattered':     ('éparpillé', 'éparpillée', 'after'),
    'old':           ('ancien', 'ancienne', 'before'),
    'pikes':         ('à piques', 'à piques', 'after'),
    'lined':         ('aligné', 'alignée', 'after'),
    'leaf':          ('en feuille', 'en feuille', 'after'),
    'pointed':       ('pointu', 'pointue', 'after'),
    'flowered':      ('fleuri', 'fleurie', 'after'),
    'lily':          ('nénuphar', 'nénuphar', 'after'),
    'pointed':       ('pointu', 'pointue', 'after'),
    'pad':           ('coussin', 'coussin', 'after'),
    'sided':         ('latéral', 'latérale', 'after'),
    'panel':         ('en panneau', 'en panneau', 'after'),
    'panels':        ('en panneaux', 'en panneaux', 'after'),
    'pumpkins':      ('citrouilles', 'citrouilles', 'after'),
    'sands':         ('sables', 'sables', 'after'),
    'brick':         ('en briques', 'en briques', 'after'),
    'bricks':        ('en briques', 'en briques', 'after'),
    'bricked':       ('en briques', 'en briques', 'after'),
    'bricky':        ('briqueté', 'briquetée', 'after'),
    'tile':          ('en tuiles', 'en tuiles', 'after'),
    'tiles':         ('en tuiles', 'en tuiles', 'after'),
    'block':         ('en blocs', 'en blocs', 'after'),
    'prismal':       ('prismatique', 'prismatique', 'after'),
    'basket':        ('en panier', 'en panier', 'after'),
    'beach':         ('plage', 'plage', 'after'),
    'big':           ('grand', 'grande', 'before'),
    'fired':         ('cuit', 'cuite', 'after'),
    'glass':         ('vitré', 'vitrée', 'after'),
    'fine':          ('fin', 'fine', 'after'),
    'leaded':        ('plombé', 'plombée', 'after'),
    'sponges':       ('en éponges', 'en éponges', 'after'),
    'ladder':        ('en échelle', 'en échelle', 'after'),
    'p':             ('P', 'P', 'before'),
    'h':             ('H', 'H', 'before'),
    'n':             ('N', 'N', 'before'),
    'piked':         ('à pointes', 'à pointes', 'after'),
    'multi':         ('multi-', 'multi-', 'before'),
    'pumpkin':       ('citrouille', 'citrouille', 'after'),
    'panel':         ('en panneau', 'en panneau', 'after'),
    'lantern':       ('lanterne', 'lanterne', 'after'),
    'multimeter':    ('multimètre', 'multimètre', 'after'),
    'semi':          ('semi-', 'semi-', 'before'),
    'patient':       ('patient', 'patiente', 'after'),
    'paddle':        ('en palette', 'en palette', 'after'),
    'patterned':     ('à motifs', 'à motifs', 'after'),
    'angled':        ('en angles', 'en angles', 'after'),
    'barky':         ('rugueux', 'rugueuse', 'after'),
    'chunky':        ('gros', 'grosse', 'after'),
    'cobbled':       ('taillé', 'taillée', 'after'),
    'disordered':    ('désordonné', 'désordonnée', 'after'),
    'droopy':        ('tombant', 'tombante', 'after'),
    'faced':         ('à face', 'à face', 'after'),
    'glittering':    ('scintillant', 'scintillante', 'after'),
    'graveled':      ('graveleux', 'graveleuse', 'after'),
    'hipped':        ('en croupe', 'en croupe', 'after'),
    'hived':         ('en ruche', 'en ruche', 'after'),
    'packed':        ('compact', 'compacte', 'after'),
    'railed':        ('à rambardes', 'à rambardes', 'after'),
    'seeded':        ('en graines', 'en graines', 'after'),
    'squished':      ('écrasé', 'écrasée', 'after'),
    'chipped':       ('ébréché', 'ébréchée', 'after'),
    'by':            ('par', 'par', 'before'),
    # words that appear and should be kept properly
    'pattern':       ('motif', 'motif', 'after'),
    # missed bits
    'pearl':         ('perle', 'perle', 'after'),
}


def is_color(token):
    return token.lower() in COLORS


def match_prefix(tokens, table):
    """Find longest matching prefix; returns (entry, length) or (None, 0)."""
    best_entry = None
    best_len = 0
    for keys, entry in table:
        n = len(keys)
        if n > best_len and len(tokens) >= n:
            if [t.lower() for t in tokens[:n]] == [k.lower() for k in keys]:
                best_entry = entry
                best_len = n
    return best_entry, best_len


def match_suffix(tokens, table):
    """Find longest matching suffix; returns (entry, length, start_index) or (None, 0, len)."""
    best_entry = None
    best_len = 0
    for keys, entry in table:
        n = len(keys)
        if n > best_len and len(tokens) >= n:
            if [t.lower() for t in tokens[-n:]] == [k.lower() for k in keys]:
                best_entry = entry
                best_len = n
    if best_entry is None:
        return None, 0, len(tokens)
    return best_entry, best_len, len(tokens) - best_len


def detect_color(tokens):
    """Find a color anywhere in tokens. Returns (color_tuple, start, length) or (None, -1, 0)."""
    # Check multi first (light_blue, light_gray)
    for i in range(len(tokens) - 1):
        key = (tokens[i].lower(), tokens[i+1].lower())
        if key in COLOR_MULTI:
            return COLOR_MULTI[key], i, 2
    for i, t in enumerate(tokens):
        if t.lower() in COLORS:
            return COLORS[t.lower()], i, 1
    return None, -1, 0


def find_material(tokens):
    """Find a material somewhere in the tokens. Returns (entry, start, length) or None."""
    # Try longest match. Prefer scanning from later in the array (because adjectives go first).
    # We scan all positions, prefer longest, and prefer last position.
    best = None
    for i in range(len(tokens)):
        for keys, entry in MATERIALS_MULTI:
            n = len(keys)
            if i + n <= len(tokens) and [t.lower() for t in tokens[i:i+n]] == [k.lower() for k in keys]:
                # prefer longer; if equal length, prefer later position
                if best is None or n > best[2] or (n == best[2] and i > best[1]):
                    best = (entry, i, n)
    return best


def pluralize(word):
    """Naive French pluralization for adjectives."""
    if not word:
        return word
    # already plural
    if word.endswith(('s', 'x', 'z')):
        return word
    if word.endswith('al'):
        return word[:-2] + 'aux'
    if word.endswith('eau'):
        return word + 'x'
    return word + 's'


def translate_adjective(tok, gender, plural=False):
    t = tok.lower()
    if t in ADJECTIVES:
        m, f, pos = ADJECTIVES[t]
        word = (m if gender == 'm' else f)
        if plural:
            # only pluralize if the form is a real adjective (no spaces/preposition phrases)
            if ' ' not in word and not word.startswith(('en ', 'à ', 'au ', 'aux ', 'sans ', 'de ', "d'")):
                word = pluralize(word)
        return word, pos
    # Unknown adjective: try to translate as a material reference (used as adjective)
    # e.g., "Diamond Spruce Planks" → keep diamond as "en diamant" type, but here we just keep
    # the word as a French equivalent if known
    if t in COLORS:
        col_m, col_f = COLORS[t]
        word = col_f if gender == 'f' else col_m
        if plural:
            if ' ' not in word and word not in ('orange', 'magenta', 'cyan', 'rose', 'marron'):
                word = pluralize(word)
        return word, 'after'
    # Try material lookup
    for keys, entry in MATERIALS_MULTI:
        if len(keys) == 1 and keys[0].lower() == t:
            return entry[0], 'after'
    # Unknown — drop the word capitalized; better than leaving English
    return tok.lower(), 'after'


def translate_value(value):
    """Main translation logic."""
    # Hardcoded specific terms (override)
    SPECIAL = {
        'Alchemy Bench': 'Banc alchimique',
        'Alchemy Book': 'Livre d\'alchimie',
        "Botanist's Workbench": 'Établi du botaniste',
        'Carpenter\'s Workbench': 'Établi du charpentier',
        'Glassblower\'s Workbench': 'Établi du souffleur de verre',
        'Shepherd\'s Workbench': 'Établi du berger',
        'Mason\'s Workbench': 'Établi du maçon',
        'Tinkering Table': 'Table de bricolage',
        'Workbench': 'Établi',
        'Chisel': 'Ciseau',
        'Multimeter': 'Multimètre',
        'Needles': 'Aiguilles',
        'Saw': 'Scie',
        'Watering Can': 'Arrosoir',
        'Chipped': 'Chipped',
    }
    if value in SPECIAL:
        return SPECIAL[value]

    # Tokenize
    tokens = value.split()
    if not tokens:
        return value

    # Handle "Acacia Doors" / "Acacia Trapdoors" — used in tag.item.* keys
    # Format: "<material> <base_plural>" → output as French
    # Already handled by general logic.

    # Special: "Chipped" alone
    if len(tokens) == 1:
        # Try as material
        mat = find_material(tokens)
        if mat:
            entry, _, _ = mat
            name = entry[0]
            return name[0].upper() + name[1:]
        # Try as adjective (e.g. "Autumnkin", "Dewkin")
        t = tokens[0].lower()
        if t in ADJECTIVES:
            m, f, _ = ADJECTIVES[t]
            return m[0].upper() + m[1:]
        # fallback: keep as-is
        return value

    # Find suffix base
    base, base_len, base_start = match_suffix(tokens, BASES_MULTI)

    if base is None:
        # No base found — entire phrase is material(s) + adjectives
        # Try treating whole thing as a material
        mat = find_material(tokens)
        if mat:
            entry, m_start, m_len = mat
            mat_fr, mat_gender = entry[0], entry[1]
            mat_plural = (len(entry) > 2 and entry[2] == 'p')
            rest_tokens = tokens[:m_start] + tokens[m_start + m_len:]
            # detect color
            color_entry, color_start, color_len = detect_color(rest_tokens)
            if color_entry:
                adj_tokens = rest_tokens[:color_start] + rest_tokens[color_start + color_len:]
            else:
                adj_tokens = rest_tokens
            adj_part = ' '.join(translate_adjective(t, mat_gender, plural=mat_plural)[0] for t in adj_tokens)
            color_part = ''
            if color_entry:
                c = color_entry[1] if mat_gender == 'f' else color_entry[0]
                if mat_plural and ' ' not in c and c not in ('orange', 'magenta', 'cyan', 'rose', 'marron'):
                    c = pluralize(c)
                color_part = c
            parts = [mat_fr]
            if adj_part:
                parts.append(adj_part)
            if color_part:
                parts.append(color_part)
            result = ' '.join(parts)
            return result[0].upper() + result[1:]
        # Total fallback: translate as adjectives only
        adj_part = ' '.join(translate_adjective(t, 'm')[0] for t in tokens)
        return adj_part[0].upper() + adj_part[1:] if adj_part else value

    base_fr, base_gender = base[0], base[1]
    base_plural = (len(base) > 2 and base[2] == 'p')

    # Remaining tokens before the base
    pre_tokens = tokens[:base_start]

    # Find material in pre tokens
    mat = find_material(pre_tokens)
    if mat:
        mat_entry, mat_start, mat_len = mat
        mat_fr = mat_entry[0]
        mat_gender = mat_entry[1]
        # Determine "en X" or "de X" based on first letter
        first = mat_fr[0].lower()
        if first in 'aeiouhâêîôûéèà':
            mat_link = "d'" + mat_fr
        else:
            mat_link = "en " + mat_fr
        # Adjectives are tokens before mat_start AND after mat_start+mat_len
        rest_tokens = pre_tokens[:mat_start] + pre_tokens[mat_start + mat_len:]
    else:
        mat_link = None
        rest_tokens = pre_tokens

    # Now detect color in rest_tokens (excluded from material zone)
    color_entry, color_start, color_len = detect_color(rest_tokens)
    if color_entry:
        adj_tokens = rest_tokens[:color_start] + rest_tokens[color_start + color_len:]
    else:
        adj_tokens = rest_tokens

    # Translate adjectives, agreeing with base gender, pluralized if base is plural
    adj_translated = []
    for t in adj_tokens:
        tr, _ = translate_adjective(t, base_gender, plural=base_plural)
        adj_translated.append(tr)
    adj_str = ' '.join(adj_translated).strip()

    # Build result: <Base> <adj> <color> <en/de material>
    parts = []
    parts.append(base_fr)
    if adj_str:
        parts.append(adj_str)
    if color_entry:
        col = color_entry[1] if base_gender == 'f' else color_entry[0]
        if base_plural and ' ' not in col and col not in ('orange', 'magenta', 'cyan', 'rose', 'marron'):
            col = pluralize(col)
        parts.append(col)
    if mat_link:
        parts.append(mat_link)

    result = ' '.join(p for p in parts if p)
    return result[0].upper() + result[1:] if result else value


def main():
    d = json.load(open(INPUT, encoding='utf-8'))
    g = json.load(open(r'c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/glossary_compact.json', encoding='utf-8'))

    out = {}
    untranslated = []
    for k, v in d.items():
        # First check glossary lowercase
        gloss = g.get(v.lower())
        if gloss:
            out[k] = gloss
            continue
        # Container/item special keys
        try:
            tr = translate_value(v)
            out[k] = tr
        except Exception as e:
            print(f"Error on {k}={v!r}: {e}", file=sys.stderr)
            out[k] = v
            untranslated.append((k, v))

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent='\t')

    print(f"Translated {len(out)} keys")
    if untranslated:
        print(f"Untranslated ({len(untranslated)}):")
        for k, v in untranslated[:20]:
            print(f"  {k} = {v}")

    # Sample some outputs
    print("\nSamples:")
    import random
    random.seed(42)
    sample_keys = random.sample(list(d.keys()), 30)
    for k in sample_keys:
        print(f"  {d[k]!r:60} -> {out[k]!r}")


if __name__ == '__main__':
    main()
