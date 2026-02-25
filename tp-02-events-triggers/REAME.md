#TP 02 : Événements et déclencheurs ( Events and Triggers)

🟢 **Niveau** : Débutant
⏱️ **Durée estimée** : 45 minutes

## Introduction

Dans le TP01, vous avez créé un workflow qui se déclenche sur `push`. Mais Github Action offre bien plus de possibilités ! Imaginez :

- Lancer des tests uniquement sur les Pull Requests
- Nettoyer des ressources chaque nuit à 3h du matin
- Déclencher un déploiement quand une release est publiée  
- Réagir quand un commentaire contient `/deploy`

Ce TP vous apprendre à **maîtriser les événements** pour déclencher vos workflows au bon moment, dans les bonnes conditions.

## Objectif 

À la fin de ce TP, vous saurez :

- [] Comprendre les différents types d'événements Github
- [] Filtrer les événements par branche, tag ou chemin 
- [] Utiliser `workflow_dispatch` avec des inputs
- [] Combiner plusieurs événements dans un même workflow
- [] Utiliser les événements planifiés (cron)
- [] Différencier `pull_request` et `pull_request_target`

## Pré-requis

### TP précédents

- ✅ TP 01 complété (premier workflow)

### Lectures recommandées

**Obligatoires** :

- [Événements déclencheurs](https://blog.stephane-robert.info/docs/pipeline-cicd/github/workflows/#les-%C3%A9v%C3%A9nements-d%C3%A9clencheurs-on)
- [Workflows plannifiés (schedule)]
- [Workflow_dispatch]

**Complémentaires** :

- [Filtres de branches et chemins]
- [Référence complète des événements]

## 🔄 Rappels

### Anatomie de la section `on:`

La clé `on` définit **quand** le workflow s'exécute

```yaml
#Format simple : un seul événement
on:
 push:

# Format détaillé : plusieurs événements
on:
 push:
 pull_request:
 workflow_dispatch:

# Avec filtres
on: 
 push:
  branches:
   - main
   - 'releases/**'
  paths:
   - 'src/**'
   - '!src/docs/**'
```

### Événements courants

| Événement | Quand se déclenche-t-il ? | Usage typique |
|:----------|:-------------------------|:--------------|
| `push`    | À chaque push | CI (tests, build) |
| `pull_request` | Ouverture/mise à jour d'une PR | Tests avant merge |
| `workflow_dispatch` | Déclenchement manuel | Déploiements maintenance |
| `schedule`| Planification cron | Nettoyage, rapports |
| `release` | Publication d'une release | Déploiement prod |
| `issue_comment` | Commentaire sur issue/PR | ChatOps |

### Filtres disponibles

| Filtre | Exemple | Description |
|:-------|:--------|:------------|
| `branches` | `branches: [main]` | Branches incluses |
| `branches-ignore` | `branches-ignore: [dev]` | Branches exclues |
| `tags` | `tags: ['v*']` | Tags matchés |
| `paths` | `paths: ['src/**']` | Fichiers modifiés |
| `paths-ignore` | `paths-ignore: ['docs/**']` | Fichiers exclus |

⚠️ **Important** : `branches` et `branches-ignore` sont **mutuellement exclusifs**

## 📚 Tutoriels

### Exercice 1 : Filtrer par branche

Créons un workflow qui s'exécute **uniquement** sur les branches de production et de staging

**Contexte** : Vous ne voulez pas gaspiller des minutes Github sur toutes les branches de feature

Créez `.github/workflows/deploy.yml` :

```yaml
name: Deploy

on:
  push:
    branches:
      - main         # Production
      - staging      # Pré-production
      - 'releases/**' # Pattern : releases/v1.0, releases/v2.0, etc.

permissions:
  contents: read

jobs:
  deploy:
    name: Déploiement
    runs-on: ubuntu-24.04

    steps:
      - name: Checkout code
        uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1

      - name: Afficher la branche
        run: |
          echo "Déploiement sur la branche: ${{ github.ref_name }}"
          echo "Événement: ${{ github.event_name }}"
```

Readme · MD
# TP 02 : Événements et déclencheurs (Events & Triggers)

🟢 **Niveau** : Débutant
⏱️ **Durée estimée** : 45 minutes

## Introduction

Dans le TP01, vous avez créé un workflow qui se déclenche sur `push`. Mais GitHub
Actions offre bien plus de possibilités ! Imaginez :

- Lancer des tests uniquement sur les Pull Requests
- Nettoyer des ressources chaque nuit à 3h du matin
- Déclencher un déploiement quand une release est publiée
- Réagir quand un commentaire contient `/deploy`

Ce TP vous apprendra à **maîtriser les événements** pour déclencher vos workflows
au bon moment, dans les bonnes conditions.

## Objectifs

À la fin de ce TP, vous saurez :

- [ ] Comprendre les différents types d'événements GitHub
- [ ] Filtrer les événements par branche, tag ou chemin
- [ ] Utiliser `workflow_dispatch` avec des inputs
- [ ] Combiner plusieurs événements dans un même workflow
- [ ] Utiliser les événements planifiés (cron)
- [ ] Différencier `pull_request` et `pull_request_target`

## Pré-requis

### TP précédents

- ✅ TP 01 complété (premier workflow)

### Lectures recommandées

**Obligatoires** :

- [Événements déclencheurs](https://blog.stephane-robert.info/docs/pipeline-cicd/github/workflows/events/)
- [Workflows planifiés (schedule)](https://blog.stephane-robert.info/docs/pipeline-cicd/github/workflows/events/#schedule)
- [workflow_dispatch](https://blog.stephane-robert.info/docs/pipeline-cicd/github/workflows/events/#workflow_dispatch)

**Complémentaires** :

- [Filtres de branches et chemins](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore)
- [Référence complète des événements](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)

## 🔄 Rappels

### Anatomie de la section `on:`

La clé `on:` définit **quand** le workflow s'exécute :

```yaml
# Format simple : un seul événement
on: push

# Format détaillé : plusieurs événements
on:
  push:
  pull_request:
  workflow_dispatch:

# Avec filtres
on:
  push:
    branches:
      - main
      - 'releases/**'
    paths:
      - 'src/**'
      - '!src/docs/**'
```

### Événements courants

| Événement | Quand se déclenche-t-il ? | Usage typique |
|:----------|:-------------------------|:--------------|
| `push` | À chaque push | CI (tests, build) |
| `pull_request` | Ouverture/màj d'une PR | Tests avant merge |
| `workflow_dispatch` | Déclenchement manuel | Déploiements, maintenance |
| `schedule` | Planification cron | Nettoyage, rapports |
| `release` | Publication d'une release | Déploiement prod |
| `issue_comment` | Commentaire sur issue/PR | ChatOps |

### Filtres disponibles

| Filtre | Exemple | Description |
|:-------|:--------|:------------|
| `branches` | `branches: [main]` | Branches incluses |
| `branches-ignore` | `branches-ignore: [dev]` | Branches exclues |
| `tags` | `tags: ['v*']` | Tags matchés |
| `paths` | `paths: ['src/**']` | Fichiers modifiés |
| `paths-ignore` | `paths-ignore: ['docs/**']` | Fichiers exclus |

⚠️ **Important** : `branches` et `branches-ignore` sont **mutuellement exclusifs**.

## 📚 Tutoriels

### Exercice 1 : Filtrer par branche

Créons un workflow qui s'exécute **uniquement** sur les branches de production
et de staging.

**Contexte** : Vous ne voulez pas gaspiller des minutes GitHub sur toutes les
branches de feature.

Créez `.github/workflows/deploy.yml` :

```yaml
name: Deploy

on:
  push:
    branches:
      - main         # Production
      - staging      # Pré-production
      - 'releases/**' # Pattern : releases/v1.0, releases/v2.0, etc.

permissions:
  contents: read

jobs:
  deploy:
    name: Déploiement
    runs-on: ubuntu-24.04

    steps:
      - name: Checkout code
        uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1

      - name: Afficher la branche
        run: |
          echo "Déploiement sur la branche: ${{ github.ref_name }}"
          echo "Événement: ${{ github.event_name }}"
```

**Test local** :

```bash
# Simuler un push sur main
act push --eventpath <(echo '{"ref": "refs/heads/main"}')

# Simuler un push sur une feature branch (ne doit PAS se déclencher)
act push --eventpath <(echo '{"ref": "refs/heads/feature/test"}')
```