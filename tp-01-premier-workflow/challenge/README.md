# 🎯 Challenge : Automatiser un projet Python

## Contexte

Vous avez rejoint une équipe qui développe une bibliothèque Python. Les tests
sont actuellement lancés manuellement avec `pytest`. Votre mission :
**automatiser les tests** avec GitHub Actions.

## Objectif

Créer un workflow `.github/workflows/ci.yml` qui :

1. Se déclenche sur les `push` vers `main` et sur les `pull_request`
2. Récupère le code source
3. Installe Python 3.11
4. Installe les dépendances depuis `requirements.txt`
5. Exécute les tests avec `pytest`

## Fichiers fournis

Le projet contient déjà :

```
challenge/
├── .github/
│   └── workflows/
│       └── ci.yml          # À compléter par vous !
├── src/
│   └── calculator.py       # Code à tester
├── tests/
│   └── test_calculator.py  # Tests pytest
├── requirements.txt        # Dépendances
├── validate.py            # Script de validation
└── README.md              # Ce fichier
```

## Contraintes

Votre workflow doit :

- ⚠️ S'appeler exactement `ci.yml`
- ⚠️ Utiliser l'action `actions/checkout`
- ⚠️ Utiliser l'action `actions/setup-python`
- ⚠️ Installer Python 3.11
- ⚠️ Utiliser `pip install -r requirements.txt`
- ⚠️ Lancer les tests avec `pytest`

## Indices

### Action setup-python

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```

### Commandes Python

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer pytest
pytest
```

## Validation

⚠️ **Important** : Toutes les commandes ci-dessous doivent être exécutées
**depuis le dossier `challenge/`** :

```bash
cd tp-01-premier-workflow/challenge
```

### Étape 1 : Vérifier la syntaxe

```bash
actionlint .github/workflows/ci.yml
```

Aucune erreur ne doit s'afficher.

### Étape 2 : Tester localement

```bash
act push -j test
```

Les tests doivent passer (2 tests réussis).

### Étape 3 : Script de validation

```bash
python3 validate.py
```

Ce script vérifie :

- [ ] Le fichier `ci.yml` existe
- [ ] La syntaxe est valide (actionlint)
- [ ] Le workflow utilise `actions/checkout`
- [ ] Le workflow utilise `actions/setup-python`
- [ ] Python 3.11 est configuré
- [ ] Les dépendances sont installées
- [ ] pytest est exécuté

## Résultat attendu

```
✅ Fichier ci.yml trouvé
✅ Syntaxe valide (actionlint)
✅ Utilise actions/checkout
✅ Utilise actions/setup-python
✅ Python 3.11 configuré
✅ Installation des dépendances
✅ Exécution de pytest

🎉 Challenge réussi ! Votre workflow est prêt.
```

## Besoin d'aide ?

- Relisez la section "📚 Tutoriels" du README principal
- Consultez la [documentation setup-python](https://github.com/actions/setup-python)
- Utilisez `actionlint` pour identifier les erreurs de syntaxe

## Solution

Si vous êtes vraiment bloqué, la solution se trouve dans le dossier
`../solution/`. Mais essayez d'abord par vous-même !
