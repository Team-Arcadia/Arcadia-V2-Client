## Description

<!-- EN: Brief description of the changes -->
<!-- FR: Description breve des changements -->

## Type of Change / Type de changement

- [ ] Bug fix / Correction de bug
- [ ] New feature / Nouvelle fonctionnalite
- [ ] Balance tweak / Reequilibrage
- [ ] Recipe / KubeJS change
- [ ] FTB Quests content / Quete
- [ ] Localization / Localisation (EN, FR, ES, PT-BR, RU, ZH-CN)
- [ ] Config tuning
- [ ] Documentation
- [ ] CI/CD / tooling

## Affected Scope / Perimetre touche

- [ ] `kubejs/server_scripts/`
- [ ] `kubejs/startup_scripts/`
- [ ] `kubejs/client_scripts/`
- [ ] `kubejs/assets/` (textures / sounds / lang)
- [ ] `kubejs/data/` (datapack overrides)
- [ ] `config/` or `defaultconfigs/`
- [ ] `config/ftbquests/`
- [ ] `resourcepacks/ArcadiaLanguages/`
- [ ] `manifest.json` (mod added/removed/updated)
- [ ] Documentation (`README`, `KUBEJS_GUIDE`, etc.)

## Changes Made / Changements effectues

-
-
-

## Testing / Tests

- [ ] Tested in singleplayer / Teste en solo
- [ ] Tested on dedicated server / Teste sur serveur dedie
- [ ] `/reload` succeeds with no KubeJS errors in the console
- [ ] JEI shows the expected recipes / no missing items
- [ ] No regressions on other features I touched / Aucune regression
- [ ] SNBT files parse correctly (if FTB Quests / lang changes)
- [ ] Lang files synced in EN and FR (and other 5 langs if FTBQ)

## Checklist

- [ ] Code, variables, KubeJS identifiers in English
- [ ] Comments in English, minimalist
- [ ] No hardcoded UI strings — `Text.translate()` with lang keys
- [ ] Recipe IDs use `arcadia:` namespace with explicit `.id()`
- [ ] `// Priority: N` header set where load order matters
- [ ] Updated `ERROR_LOG.md` if a bug was fixed
- [ ] Updated `KUBEJS_GUIDE.md` if structure or conventions changed
