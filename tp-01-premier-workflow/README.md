# TP 01 : Votre premier workflow GitHub Actions

🟢 **Niveau** : Débutant
⏱️ **Durée estimée** : 30 minutes

## Introduction

Vous venez de rejoindre une équipe de développement. Actuellement, les tests
sont lancés manuellement : chaque développeur doit penser à exécuter `npm test`
avant de Pousser. Résultat : des bugs passent régulièrement en production car
quelqu'un a oublié de tester.

Votre mission : **automatiser l'exécution des tests** pour qu'ils se lancent
à chaque push. Plus personne ne pourra oublier.

## Objectifs

À la fin de ce TP, vous saurez :

- [ ] Créer un fichier de workflow dans le bon répertoire
- [ ] Structurer un workflow avec `name`, `on`, `jobs` et `steps`
- [ ] Configurer un déclencheur sur l'événement `push`
- [ ] Utiliser des actions officielles (`actions/checkout`, `actions/setup-node`)
- [ ] Valider votre workflow localement **avant** de le Pousser

## Pré-requis

### Lectures recommandées

Avant de commencer ce TP, il est fortement recommandé de lire les articles
suivants pour bien comprendre les concepts de base :

- [Introduction à GitHub Actions](https://blog.stephane-robert.info/docs/pipeline-cicd/github/) : concepts clés
- [Premiers pas avec les workflows](https://blog.stephane-robert.info/docs/pipeline-cicd/github/workflows/) : structure d'un workflow
- [Debug des workflows](https://blog.stephane-robert.info/docs/pipeline-cicd/github/optimiser/debug/) : diagnostiquer les problèmes
- [Sécurité GitHub Actions](https://blog.stephane-robert.info/docs/pipeline-cicd/github/securite/) : bonnes pratiques
- [Pinning des actions GitHub](https://blog.stephane-robert.info/docs/pipeline-cicd/github/securite/pinning/) : éviter les risques liés aux actions tierces
- [actionlint](https://blog.stephane-robert.info/docs/pipeline-cicd/github/actionlint/) : valider la syntaxe YAML
- [act](https://blog.stephane-robert.info/docs/pipeline-cicd/github/act/) : exécuter les workflows en local
- [GitHub CLI (gh)](https://blog.stephane-robert.info/docs/pipeline-cicd/github/gh-cli/) : gérer les workflows depuis le terminal

### Outils installés

Vérifiez que ces outils sont disponibles sur votre machine :

```bash
# Docker
docker --version

# Git
git --version

# GitHub CLI
gh --version

# act (exécution locale des workflows)
act --version

# actionlint (linter pour workflows)
actionlint --version
```

⚠️ Si un outil manque, consultez le [README principal](../README.md) pour les
instructions d'installation.

### Lectures préalables

Avant de commencer, **lisez attentivement** ces pages :

1. **[Introduction à GitHub Actions](https://blog.stephane-robert.info/docs/pipeline-cicd/github/)**
   Comprendre les concepts : workflow, job, step, runner

2. **[Syntaxe YAML des workflows](https://blog.stephane-robert.info/docs/pipeline-cicd/github/workflows/syntaxe-yaml/)**
   Maîtriser la syntaxe : indentation, listes, dictionnaires

3. **[actionlint : valider vos workflows](https://blog.stephane-robert.info/docs/pipeline-cicd/github/optimiser/actionlint/)**
   Détecter les erreurs avant de Pousser

4. **[act : exécuter les workflows en local](https://blog.stephane-robert.info/docs/pipeline-cicd/github/optimiser/act/)**
   Tester sans consommer vos minutes GitHub

## 🔄 Rappels

### Structure d'un repository GitHub Actions

Les workflows doivent **obligatoirement** être placés dans :

```
.github/
└── workflows/
    └── mon-workflow.yml
```

⚠️ Attention : c'est `.github` (avec un point) et non `github`.

### Anatomie d'un workflow

Un workflow minimal contient 4 parties :

```yaml
# 1. Nom affiché dans l'interface GitHub
name: CI

# 2. Quand le workflow s'exécute
on:
  push:
    branches: [main]

# 3. Les jobs (tâches) à exécuter
jobs:
  # Identifiant du job (pas d'espaces)
  build:
    # Machine virtuelle utilisée
    runs-on: ubuntu-24.04

    # 4. Les étapes du job
    steps:
      - name: Description de l'étape
        run: echo "Hello World"
```

### Les clés essentielles

| Clé | Rôle | Exemple |
|:----|:-----|:--------|
| `name` | Nom affiché dans GitHub | `name: Tests CI` |
| `on` | Événement déclencheur | `on: push` |
| `jobs` | Conteneur des tâches | `jobs:` |
| `runs-on` | Type de runner | `runs-on: ubuntu-latest` |
| `steps` | Liste des étapes | `steps:` |
| `uses` | Appeler une action | `uses: actions/checkout@v4` |
| `run` | Exécuter une commande | `run: npm test` |

### Événements courants

| Événement | Déclencheur |
|:----------|:------------|
| `push` | À chaque push sur le repo |
| `pull_request` | À l'ouverture/mise à jour d'une PR |
| `workflow_dispatch` | Déclenchement manuel depuis l'UI |
| `schedule` | Planification cron |

## 📚 Tutoriels

### Exercice 1 : Créer la structure

Créons l'arborescence nécessaire pour notre premier workflow.

Commencez par vous placer à la racine de votre projet :

```bash
cd tp-01-premier-workflow
```

**Étape 1** : Créez le répertoire des workflows

```bash
mkdir -p .github/workflows
```

**Étape 2** : Créez un fichier de workflow vide

```bash
touch .github/workflows/ci.yml
```

**Étape 3** : Vérifiez la structure

```bash
tree .github
# Résultat attendu :
# .github
# └── workflows
#     └── ci.yml
```

### Exercice 2 : Écrire un workflow minimal

Ouvrez `.github/workflows/ci.yml` et ajoutez ce contenu :

```yaml
# Nom affiché dans l'onglet Actions de GitHub
name: CI

# Déclencheur : à chaque push
on:
  push:

# Les jobs à exécuter
jobs:
  # Job nommé "hello"
  hello:
    # Exécuter sur la dernière version d'Ubuntu
    runs-on: ubuntu-24.04

    # Liste des étapes
    steps:
      # Première étape : afficher un message
      - name: Dire bonjour
        run: echo "Bonjour depuis GitHub Actions !"
```

**Validation avec actionlint** :

```bash
actionlint .github/workflows/ci.yml
# Aucune sortie = pas d'erreur
```

**Test local avec act** :

```bash
act push --list
# Affiche les jobs qui seraient exécutés

act push -j hello
# Exécute le job "hello" localement
```

Résultat attendu :

```bash
[CI/hello] 🚀 Start image=catthehacker/ubuntu:act-24.04
[CI/hello]   🐳 docker pull ...
[CI/hello] ⭐ Run Main Dire bonjour
[CI/hello]   | Bonjour depuis GitHub Actions !
[CI/hello]   ✅ Success - Main Dire bonjour
```

### Exercice 3 : Ajouter le checkout du code

Un workflow de CI doit d'abord **récupérer le code** du repository. C'est le
rôle de l'action `actions/checkout`. Pour cela allez sur le [**marketplace
GitHub**](https://github.com/marketplace).

Modifiez votre workflow :

```yaml
name: CI

on:
  push:

jobs:
  test:
    runs-on: ubuntu-24.04

    steps:
      # Étape 1 : Récupérer le code source
      - name: Checkout du code
        uses: actions/checkout@v6.0.1

      # Étape 2 : Afficher les fichiers
      - name: Lister les fichiers
        run: ls -la
```

**Explication** :

- `uses: actions/checkout@v4` appelle une **action** du Marketplace
- `@v4` indique la version majeure de l'action
- Sans cette étape, le runner démarre avec un répertoire vide !

**Test local** :

```bash
act push -j test
```

Vous devriez voir la liste des fichiers de votre projet.

On va piner le sha pour plus de sécurité dans le prochain TP.

```bash
npx pin-github-action .github/workflows/ci.yml
```

### Exercice 4 : Configurer Node.js et exécuter des tests

Pour un projet Node.js, on doit installer Node avant de lancer les tests.

Créez un fichier `package.json` minimal si vous n'en avez pas :

```bash
cat > package.json << 'EOF'
{
  "name": "tp-01",
  "scripts": {
    "test": "echo 'Tests réussis !' && exit 0"
  }
}
EOF
```

Mettez à jour le workflow :

```yaml
name: CI

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # Récupérer le code
      - name: Checkout du code
        uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1

      # Installer Node.js
      - name: Installer Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      # Exécuter les tests
      - name: Lancer les tests
        run: npm test
```

**Nouveautés** :

- `actions/setup-node@v4` installe Node.js sur le runner
- `with:` permet de passer des paramètres à l'action
- `node-version: '20'` spécifie la version de Node

**Validation** :

```bash
# On pine les actions
npx pin-github-action .github/workflows/ci.yml

# Vérifier la syntaxe
actionlint .github/workflows/ci.yml

# Tester localement
act push -j test
```

### Exercice 5 : Filtrer par branche

Actuellement, le workflow s'exécute sur **tous** les push, même sur des
branches de feature. Limitons-le aux branches `main` et `develop`.

```yaml
name: CI

on:
  push:
    branches:
      - main
      - develop

jobs:
  test:
    runs-on: ubuntu-24.04

    steps:
      - name: Checkout du code
        uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1

      - name: Installer Node.js
        uses: actions/setup-node@395ad3262231945c25e8478fd5baf05154b1d79f # v6.1.0
        with:
          node-version: '20'

      - name: Lancer les tests
        run: npm test
```

**Test** :

```bash
# Simuler un push sur main
act push -j test --eventpath <(echo '{"ref": "refs/heads/main"}')

# Simuler un push sur une autre branche
act push -j test --eventpath <(echo '{"ref": "refs/heads/feature"}')
# Le job ne devrait pas se déclencher (filtré par la condition branches)
```

### Exercice 6 : Ajouter le déclenchement manuel

Pour pouvoir relancer le workflow à la demande depuis l'interface GitHub,
ajoutez `workflow_dispatch` :

```yaml
name: CI

on:
  push:
    branches:
      - main
      - develop
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-24.04

    steps:
      - name: Checkout du code
        uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1

      - name: Installer Node.js
        uses: actions/setup-node@395ad3262231945c25e8478fd5baf05154b1d79f # v6.1.0
        with:
          node-version: '20'

      - name: Lancer les tests
        run: npm test
```

Avec `workflow_dispatch`, un bouton "Run workflow" apparaîtra dans l'onglet
Actions de votre depot sur GitHub.

**Test local** :

```bash
# Simuler un déclenchement manuel
act workflow_dispatch -j test
```

### Exercice 7 : Workflow complet avec bonnes pratiques

Voici la version finale avec les bonnes pratiques :

```yaml
name: CI

# Déclencheurs
on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
  workflow_dispatch:

# Permissions minimales (bonne pratique sécurité)
permissions:
  contents: read

jobs:
  test:
    name: Tests unitaires
    runs-on: ubuntu-24.04

    steps:
      - name: Checkout du code
        uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1

      - name: Installer Node.js 20
        uses: actions/setup-node@395ad3262231945c25e8478fd5baf05154b1d79f # v6.1.0
        with:
          node-version: '20'

      - name: Installer les dépendances
        run: npm ci

      - name: Lancer les tests
        run: npm test
```

**Améliorations** :

1. `pull_request` : teste aussi les PRs avant merge
2. `permissions: contents: read` : principe du moindre privilège
3. `name: Tests unitaires` : nom explicite dans l'UI
4. `npm ci` : plus rapide et déterministe que `npm install`

**Validation finale** :

```bash
# Linter
actionlint .github/workflows/ci.yml

# Test local
act push -j test
```

## 🎯 Challenge

Vous avez compris les bases. Maintenant, c'est à vous de jouer !

Rendez-vous dans le dossier [`challenge/`](./challenge/) pour l'exercice
autonome.

## Récapitulatif

| Concept | Ce qu'il faut retenir |
|:--------|:---------------------|
| **Emplacement** | `.github/workflows/*.yml` |
| **Structure** | `name`, `on`, `jobs`, `steps` |
| **Déclencheurs** | `push`, `pull_request`, `workflow_dispatch` |
| **Actions** | `uses: owner/action@version` |
| **Commandes** | `run: commande shell` |
| **Validation** | `actionlint` puis `act` |

Et on pine toujours les actions avec :

On pine toujours les actions après chaque modification :

```bash
npx pin-github-action .github/workflows/ci.yml
```

## Félicitations !