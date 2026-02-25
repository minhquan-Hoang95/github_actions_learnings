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

### Exercice 2 : Filtrer par chemin

Imaginez un monorepo avec plusieurs applications. Vous voulez que les tests
backend se lancent uniquement quand le code backend change.

```yaml
name: Backend CI

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'        # Tout dans backend/
      - 'shared/**'         # Code partagé
      - '!backend/docs/**'  # Sauf la documentation

permissions:
  contents: read

jobs:
  test-backend:
    runs-on: ubuntu-24.04

    steps:
      - uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1

      - name: Tester le backend
        run: echo "Tests backend lancés car fichiers backend modifiés"
```

**Patterns de chemins** :

- `**` : n'importe quel répertoire
- `*` : n'importe quel fichier
- `!` : exclusion (doit venir après une inclusion)

### Exercice 3 : workflow_dispatch avec inputs

Le déclenchement manuel est très utile pour les opérations ponctuelles. Ajoutons
des paramètres !

```yaml
name: Déploiement manuel

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environnement cible'
        required: true
        type: choice
        options:
          - dev
          - staging
          - production
      version:
        description: 'Version à déployer (ex: v1.2.3)'
        required: true
        type: string
      dry-run:
        description: 'Simulation (dry-run)'
        required: false
        type: boolean
        default: true

permissions:
  contents: read

jobs:
  deploy:
    name: Déploiement sur ${{ inputs.environment }}
    runs-on: ubuntu-24.04

    steps:
      - uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1
        with:
          ref: ${{ inputs.version }}

      - name: Afficher les paramètres
        run: |
          echo "Environnement: ${{ inputs.environment }}"
          echo "Version: ${{ inputs.version }}"
          echo "Dry-run: ${{ inputs.dry-run }}"

      - name: Déployer
        if: inputs.dry-run == false
        run: echo "Déploiement réel vers ${{ inputs.environment }}"

      - name: Simulation
        if: inputs.dry-run == true
        run: echo "🔍 Mode simulation activé"
```

**Types d'inputs disponibles** :

| Type | Description | Exemple |
|:-----|:------------|:--------|
| `string` | Texte libre | `'v1.0.0'` |
| `choice` | Liste déroulante | `dev`, `staging`, `prod` |
| `boolean` | Case à cocher | `true` / `false` |
| `environment` | Environnement GitHub | Avec protection |

**Test local** :

```bash
# Simuler un workflow_dispatch
act workflow_dispatch -j deploy \
  --input environment=staging \
  --input version=v1.0.0 \
  --input dry-run=true
```

### Exercice 4 : Workflows planifiés (schedule)

Les workflows planifiés utilisent la syntaxe **cron POSIX**. Parfait pour :
- Nettoyage automatique
- Rapports quotidiens
- Surveillance périodique

```yaml
name: Nettoyage hebdomadaire

on:
  schedule:
    # Tous les lundis à 3h00 UTC
    - cron: '0 3 * * 1'

  # Permettre le déclenchement manuel pour tester
  workflow_dispatch:

permissions:
  contents: write  # Pour supprimer des artefacts

jobs:
  cleanup:
    runs-on: ubuntu-24.04

    steps:
      - name: Afficher l'heure
        run: |
          echo "Nettoyage lancé à: $(date)"
          echo "Cron: ${{ github.event.schedule }}"

      - name: Nettoyer les anciens artefacts
        run: echo "Suppression des artefacts > 30 jours"
```

**Syntaxe cron** :

```
 ┌───────────── minute (0 - 59)
 │ ┌───────────── heure (0 - 23)
 │ │ ┌───────────── jour du mois (1 - 31)
 │ │ │ ┌───────────── mois (1 - 12)
 │ │ │ │ ┌───────────── jour de la semaine (0 - 6, 0 = dimanche)
 │ │ │ │ │
 * * * * *
```

**Exemples courants** :

| Cron | Signification |
|:-----|:--------------|
| `0 0 * * *` | Tous les jours à minuit UTC |
| `0 */6 * * *` | Toutes les 6 heures |
| `0 9 * * 1-5` | Du lundi au vendredi à 9h |
| `0 0 1 * *` | Le 1er de chaque mois |

⚠️ **Important** :
- L'heure est en **UTC** (pas en heure locale)
- Intervalle minimal : **5 minutes**
- Les workflows peuvent avoir jusqu'à **15 min de retard** sous forte charge

### Exercice 5 : pull_request vs pull_request_target

**Question de sécurité critique** : quelle est la différence ?

```yaml
# ❌ DANGEREUX pour les PRs externes (forks)
name: PR dangereuse

on:
  pull_request_target:  # ⚠️ Exécute avec les permissions du repo de base

permissions:
  contents: write  # Accès en écriture !

jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # Code du fork
      # ❌ Code malveillant du fork peut accéder aux secrets !
```

```yaml
# ✅ SÛR pour les PRs externes
name: PR sécurisée

on:
  pull_request:  # Exécute dans le contexte du fork (pas de secrets)

permissions:
  contents: read  # Lecture seule

jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1
      # ✅ Pas d'accès aux secrets sensibles
      - run: npm test
```

**Règle d'or** :

- `pull_request` : pour les tests (pas de secrets)
- `pull_request_target` : uniquement si vous savez ce que vous faites
  (typiquement pour commenter la PR)

### Exercice 6 : Combiner plusieurs événements

Vous pouvez déclencher un workflow sur plusieurs événements :

```yaml
name: CI/CD

on:
  # 1. Tests sur toutes les PRs
  pull_request:
    branches: [main]

  # 2. Déploiement sur push vers main
  push:
    branches: [main]

  # 3. Déploiement manuel possible
  workflow_dispatch:
    inputs:
      deploy:
        type: boolean
        default: false

permissions:
  contents: read

jobs:
  test:
    name: Tests
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1
      - run: npm test

  deploy:
    name: Déploiement
    runs-on: ubuntu-24.04
    # Ne déployer que si push sur main OU workflow_dispatch avec deploy=true
    if: github.event_name == 'push' || (github.event_name == 'workflow_dispatch' && inputs.deploy == true)
    needs: test

    steps:
      - uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1
      - run: echo "Déploiement en cours..."
```

### Exercice 7 : Événements avancés

```yaml
name: Événements multiples

on:
  # Déclenché quand une release est publiée
  release:
    types: [published]

  # Déclenché quand on commente une issue
  issue_comment:
    types: [created]

  # Déclenché quand un workflow externe se termine
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

permissions:
  contents: read

jobs:
  handle-event:
    runs-on: ubuntu-24.04

    steps:
      - name: Identifier l'événement
        run: |
          echo "Type d'événement: ${{ github.event_name }}"

          if [ "${{ github.event_name }}" == "release" ]; then
            echo "Release détectée: ${{ github.event.release.tag_name }}"
          elif [ "${{ github.event_name }}" == "issue_comment" ]; then
            echo "Commentaire: ${{ github.event.comment.body }}"
          elif [ "${{ github.event_name }}" == "workflow_run" ]; then
            echo "Workflow terminé: ${{ github.event.workflow_run.conclusion }}"
          fi
```

## 🎯 Challenge

Rendez-vous dans le dossier [`challenge/`](./challenge/) pour l'exercice autonome.

Vous devrez créer un workflow qui :
- Se déclenche sur les PRs vers `main`
- Se déclenche tous les jours à 9h UTC
- Permet le déclenchement manuel avec choix d'environnement
- Ne s'exécute que si des fichiers Python sont modifiés

## Récapitulatif

| Concept | Ce qu'il faut retenir |
|:--------|:---------------------|
| **push** | Tests et CI sur les commits |
| **pull_request** | Tests avant merge (sûr pour forks) |
| **pull_request_target** | ⚠️ Dangereux, éviter sauf besoin spécifique |
| **workflow_dispatch** | Déclenchement manuel avec inputs |
| **schedule** | Tâches planifiées (cron) |
| **Filtres** | branches, paths, tags pour cibler précisément |

## Pour aller plus loin

- [Liste complète des événements](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [Sécurité des workflows](https://blog.stephane-robert.info/docs/pipeline-cicd/github/securite/)
- [Expressions de filtrage](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet)
- [crontab.guru](https://crontab.guru/) : générateur d'expressions cron

## Prochaine étape

**TP 03** : Contexts et expressions - Accéder aux métadonnées et créer des
workflows dynamiques.