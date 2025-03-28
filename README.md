# lifapcd-image-viewer

## Description
Ce projet implémente une classe `Image` permettant de manipuler des images au format PPM. Il inclut des fonctionnalités telles que :
- La création et la modification d'images.
- La sauvegarde et le chargement d'images au format PPM.
- L'affichage des images dans la console ou via SDL2.

Le projet est divisé en plusieurs exécutables pour tester et démontrer les fonctionnalités.

## Structure du projet
```
lifapcd-image-viewer/
├── bin/                # Contient les exécutables générés
├── data/               # Contient les fichiers PPM utilisés (images)
├── doc/                # Contient la documentation générée par Doxygen
├── src/                # Contient les fichiers source (.cpp)
│   ├── mainTest.cpp    # Tests unitaires pour la classe Image
│   ├── mainExemple.cpp # Exemple d'utilisation de la classe Image
│   ├── mainAffichage.cpp # Affichage d'images avec SDL2
│   ├── Image.cpp       # Implémentation de la classe Image
│   ├── ImageViewer.cpp # Gestion de l'affichage avec SDL2
├── include/            # Contient les fichiers d'en-tête (.h)
├── CMakeLists.txt      # Fichier de configuration CMake
└── README.md           # Documentation du projet
```

## Prérequis
- **CMake** (version 3.0 ou supérieure)
- **SDL2** (pour l'exécutable `affichage`)
- Un compilateur compatible avec C++11 ou supérieur (par exemple, `g++`).

## Compilation
1. Créez un répertoire de build :
   ```bash
   mkdir build
   cd build
   ```

2. Configurez le projet avec CMake :
   ```bash
   cmake ..
   ```

3. Compilez le projet :
   ```bash
   make
   ```

Les exécutables seront générés dans le répertoire `bin`.

## Exécutables
### 1. `test`
- **Description :** Exécute des tests unitaires pour vérifier le bon fonctionnement de la classe `Image`.
- **Commande :**
  ```bash
  ./bin/test
  ```

### 2. `exemple`
- **Description :** Montre un exemple d'utilisation de la classe `Image`, incluant la création, la modification et la sauvegarde d'images.
- **Commande :**
  ```bash
  ./bin/exemple
  ```

### 3. `affichage`
- **Description :** Affiche une image PPM en utilisant SDL2.
- **Commande :**
  ```bash
  ./bin/affichage
  ```

## Documentation
La documentation est générée avec **Doxygen**. Pour la générer, utilisez la commande suivante :
```bash
make doc
```
La documentation sera disponible dans le répertoire `doc`.

## Auteurs
- **GOSSET Raphaël**
- **LANGE Théo**
- **LAASSIBI Yanis**
