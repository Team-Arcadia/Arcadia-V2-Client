# Arcadia V2 Client

Une installation Minecraft complète et optimisée pour la version **1.21.1**, mettant en avant exploration, création et découverte.

## 📋 Table des matières

- [À propos](#à-propos)
- [Version](#version)
- [Installation](#installation)
- [Caractéristiques principales](#caractéristiques-principales)
- [Catégories de mods](#catégories-de-mods)
- [Structure du projet](#structure-du-projet)
- [Configuration](#configuration)
- [Support](#support)

## À propos

**Arcadia V2 Client** est une pack de mods soigneusement sélectionnés pour Minecraft 1.21.1 utilisant NeoForge. Ce projet offre une expérience enrichie avec plus de 300 mods couvrant:

- **Exploration**: nouvelles structures, biomes et dimensions
- **Création**: améliorations de la mécanique de crafting et des machines
- **Qualité de vie**: améliorations d'interface et de gameplay
- **Décoration**: blocs et features de design supplémentaires
- **Performance**: optimisations et corrections pour une meilleure expérience

## Version

- **Minecraft**: 1.21.1
- **Loader**: NeoForge
- **Client Type**: MultiPlayer Ready

## Installation

### Prérequis

- Java 21 (recommandé)
- Un launcher Minecraft compatible (Curse Client, Prism Launcher, etc.)
- Environ 12-15 GB d'espace disque

### Étapes

1. **Cloner ou télécharger le projet**

   ```bash
   git clone <repository-url>
   cd Arcadia-V2-Client
   ```

2. **Utiliser un launcher compatible**
   - Importez le dossier complet dans votre launcher
   - Ou utilisez le launcher Curse Client directement

3. **Lancer le client**
   - Assurez-vous que Java 21 est sélectionné
   - Lancez l'instance Minecraft
   - Profitez !

## Caractéristiques principales

### 🎨 Visuels & Ambiance

- Améliorations graphiques (Sodium, Iris, Sound Physics)
- Shaders supportés (dossier `shaderpacks/`)
- Packs de ressources custom (dossier `resourcepacks/`)
- Effets visuels améliorés (Better Third Person, Exposure, etc.)

### ⚙️ Mécanique de jeu

- **Create**: système d'ingénierie et d'automatisation avancé
- **Mekanism**: traitement des minerais et machines industrielles
- **Ars Nouveau**: magie et sorts
- **Twilight Forest**: nouvelle dimension épique avec boss
- **Aether**: dimension céleste avec biomes flottants

### 🏗️ Construction & Décoration

- Blocs décorés supplémentaires (MCW Mod series)
- Outils de construction améliorés (Building Gadgets)
- Système de frames (Framed Blocks)
- Meubles et housewares (Handcrafted, Another Furniture)

### 📚 Exploration & Aventure

- Structures générées (Dungeon Arise, Structory, Moogs)
- Villages et donjons augmentés
- Biomes enrichis (Biomes O'Plenty, Ecologics)
- Boss et créatures supplémentaires (Mowzie's Mobs, Mutant Monsters)

### 🎯 Qualité de vie

- JEI (Just Enough Items) pour la recherche de recettes
- Waystones pour les téléportations rapides
- Jade pour les infos des blocs
- Villagers améliorés
- Organisation d'inventaire (Sophisticated Backpacks)

### ⚡ Performance & Optimisations

- Sodium pour une meilleure frame rate
- ModernFix, FastFurnace, FastWorkbench
- Entity Culling pour moins de lag
- Ferritecore pour l'optimisation mémoire

## Catégories de mods

### Mods Core & Dépendances

- NeoForge Core, Architectury, Bookshelf, Balm
- Cloth Config, ForgeConfig API Port

### Exploration & Structures

- Dungeon Arise, Structory, Moogs Voyager Structures
- Twilight Forest Final Boss
- Empty Villages, Underground Bunkers

### Création & Automatisation

- Create + 30+ addons Create
- Mekanism + Generators + Tools
- Ars Nouveau, Ars Technica, Ars Creo
- Refined Storage

### Dimension

- Aether, Deep Aether
- Twilight Forest
- Various caves and nether structures

### Décoration & Bâtiment

- MCW Series (Bridges, Windows, Doors, Roofs, etc.)
- Framed Blocks, Chipped, Rechiseled
- Another Furniture, Handcrafted, Buildcraft

### Électronique & Programation

- CC:Tweaked (ComputerCraft)
- Immersive Engineering

### Magie & Enchants

- Irons Spellbooks
- Apotheosis (enchantements)

### Mobs & Créatures

- Mowzie's Mobs, Mutant Monsters
- Animal Garden
- Easy NPCs, Corpse

### Nourriture & Agriculture

- Farmer's Delight + addons
- Aquaculture, Botanypots
- Various delight addons (Nether, Twilight, Crate, etc.)

### Interface & Affichage

- JEI (Just Enough Items)
- Jade + JadeAddons
- Waystones, Legenday Tooltips
- Better F3, Spiffy HUD

### Optimisation

- Sodium + Sodiumoptionsapi
- Iris (Shaders)
- ImmediatelyFast, EntityCulling
- ModernFix, Ferritecore

### Client Quality of Life

- Inventory Tweaks
- MouseTweaks
- EMI (Empty and Miscellaneous Items)
- Controlling

## Structure du projet

```
Arcadia-V2-Client/
├── mods/                          # 300+ fichiers JAR de mods
├── config/                         # Configuration de tous les mods
├── saves/                          # Mondes sauvegardés
├── resourcepacks/                 # Packs de textures personnalisés
├── shaderpacks/                   # Shaders graphiques
├── kubejs/                        # Scripts KubeJS personnalisés
├── local/                         # Données locales
├── easy_npc/                      # Configuration des NPCs
├── crash-reports/                 # Rapports de crash (diagnostic)
├── logs/                          # Fichiers de logs
├── screenshots/                   # Captures d'écran
├── minecraftinstance.json         # Métadonnées d'instance
├── options.txt                    # Options de jeu
├── servers.dat                    # Serveurs sauvegardés
└── README.md                      # Ce fichier
```

## Configuration

### Mods

Chaque mod préférence peut être configurée via :

- **In-game**: Menu de configuration (Mod Menu, etc.)
- **Fichiers**: Dossier `config/` pour les fichiers `.toml` et `.json`

### Changer les Shaders

1. Utilisez `shaderpacks/` pour ajouter des shaders
2. En jeu: Shader selection (avec Iris)

### Ajouter des Packs de Ressources

1. Ajoutez les fichiers `.zip` dans `resourcepacks/`
2. Activez via les options graphiques

### Ajouter des Mods

1. Téléchargez le `.jar` compatible 1.21.1 NeoForge
2. Ajoutez-le au dossier `mods/`
3. Redémarrez le client

## Dépannage

### Le jeu crash au démarrage

- Vérifiez que vous avez Java 21+ d'installé
- Consultez `crash-reports/` pour les erreurs
- Essayez de supprimer le dossier `.mixin.out/` et relancez

### Faible performance (FPS)

- Activez Sodium et Iris si ce n'est pas fait
- Réduisez la distance de rendu (Render Distance)
- Désactivez les fancy graphics
- Vérifiez votre allocation RAM (6-8 GB recommandés)

### Mod incompatible

- Vérifiez la version du mod (1.21.1 NeoForge)
- Consultez le fichier log pour le message d'erreur exact
- Supprimez le mod problématique du dossier `mods/`

## Support

Pour des problèmes ou suggestions :

1. Vérifiez les logs dans le dossier `logs/`
2. Consultez la documentation des mods individuels
3. Signalez les problèmes via Git issues

## Licence

Veuillez consulter le fichier [LICENSE](LICENSE) pour les détails de licence.

## Crédits

Ce projet est une compilation de mods créés par de talentueux développeurs Minecraft. Merci à tous les créateurs de mods qui rendent cette expérience possible.

---

**Dernière mise à jour**: Avril 2026  
**Version Minecraft**: 1.21.1  
**Nombre de mods**: 300+
