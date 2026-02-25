#!/usr/bin/env python3
"""
Script de validation du challenge TP-01.
Vérifie que le workflow CI est correctement configuré.
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ PyYAML non installé. Exécutez: pip install pyyaml")
    sys.exit(1)


# Couleurs ANSI
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color

WORKFLOW_FILE = Path(".github/workflows/ci.yml")


def passed(msg: str) -> None:
    """Affiche un message de succès."""
    print(f"{GREEN}✅ {msg}{NC}")


def failed(msg: str, hint: str = "") -> None:
    """Affiche un message d'échec."""
    print(f"{RED}❌ {msg}{NC}")
    if hint:
        print(f"   {hint}")


def warn(msg: str) -> None:
    """Affiche un avertissement."""
    print(f"{YELLOW}⚠️  {msg}{NC}")


def deep_search(obj, key: str, value: str = None) -> bool:
    """Recherche récursive d'une clé (et optionnellement d'une valeur) dans un dict/list."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                if value is None:
                    return True
                if isinstance(v, str) and value in v:
                    return True
                if isinstance(v, list) and value in v:
                    return True
            if deep_search(v, key, value):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if deep_search(item, key, value):
                return True
    return False


def check_uses_action(workflow: dict, action_name: str) -> bool:
    """Vérifie si une action est utilisée dans le workflow."""
    jobs = workflow.get("jobs")
    if not jobs or not isinstance(jobs, dict):
        return False
    for job in jobs.values():
        if not job or not isinstance(job, dict):
            continue
        steps = job.get("steps", [])
        if not steps:
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = step.get("uses", "")
            if action_name in str(uses):
                return True
    return False


def check_run_command(workflow: dict, command: str) -> bool:
    """Vérifie si une commande run contient un texte donné."""
    jobs = workflow.get("jobs")
    if not jobs or not isinstance(jobs, dict):
        return False
    for job in jobs.values():
        if not job or not isinstance(job, dict):
            continue
        steps = job.get("steps", [])
        if not steps:
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            run = step.get("run", "")
            if command in str(run):
                return True
    return False


def check_python_version(workflow: dict, version: str) -> bool:
    """Vérifie si une version Python spécifique est configurée."""
    jobs = workflow.get("jobs")
    if not jobs or not isinstance(jobs, dict):
        return False
    for job in jobs.values():
        if not job or not isinstance(job, dict):
            continue
        steps = job.get("steps", [])
        if not steps:
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            with_block = step.get("with", {})
            if with_block and isinstance(with_block, dict):
                py_version = with_block.get("python-version", "")
                if version in str(py_version):
                    return True
    return False


def check_trigger(workflow: dict, trigger: str) -> bool:
    """Vérifie si un déclencheur est configuré."""
    on_block = workflow.get("on", {}) or workflow.get(
        True, {}
    )  # 'on' peut être interprété comme True en YAML
    if isinstance(on_block, dict):
        return trigger in on_block
    if isinstance(on_block, list):
        return trigger in on_block
    if isinstance(on_block, str):
        return trigger == on_block
    return False


def check_branch(workflow: dict, branch: str) -> bool:
    """Vérifie si une branche est mentionnée dans les déclencheurs."""
    on_block = workflow.get("on", {}) or workflow.get(True, {})
    if isinstance(on_block, dict):
        for trigger_config in on_block.values():
            if isinstance(trigger_config, dict):
                branches = trigger_config.get("branches", [])
                if branch in branches:
                    return True
    return False


def main() -> int:
    """Point d'entrée principal."""
    print("=========================================")
    print("🔍 Validation du Challenge TP-01")
    print("=========================================")
    print()

    passed_count = 0
    failed_count = 0

    # Test 1 : Le fichier existe
    if not WORKFLOW_FILE.exists():
        failed("Fichier ci.yml non trouvé", "Créez le fichier .github/workflows/ci.yml")
        return 1
    passed("Fichier ci.yml trouvé")
    passed_count += 1

    # Test 2 : Le fichier est un YAML valide
    try:
        with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
            workflow = yaml.safe_load(f)
        if workflow is None:
            failed("Le fichier YAML est vide", "Ajoutez le contenu du workflow")
            return 1
        passed("Syntaxe YAML valide")
        passed_count += 1
    except yaml.YAMLError as e:
        failed(f"Erreur de syntaxe YAML: {e}")
        return 1

    # Test 2b : La section jobs existe
    jobs = workflow.get("jobs")
    if not jobs or not isinstance(jobs, dict):
        failed(
            "Section 'jobs' manquante ou invalide",
            "Ajoutez: jobs:\\n  nom-du-job:\\n    runs-on: ubuntu-latest",
        )
        failed_count += 1
    else:
        passed("Section 'jobs' présente")
        passed_count += 1

    # Test 3 : Utilise actions/checkout
    if check_uses_action(workflow, "actions/checkout"):
        passed("Utilise actions/checkout")
        passed_count += 1
    else:
        failed("actions/checkout non trouvé", "Ajoutez: uses: actions/checkout@v4")
        failed_count += 1

    # Test 4 : Utilise actions/setup-python
    if check_uses_action(workflow, "actions/setup-python"):
        passed("Utilise actions/setup-python")
        passed_count += 1
    else:
        failed(
            "actions/setup-python non trouvé", "Ajoutez: uses: actions/setup-python@v5"
        )
        failed_count += 1

    # Test 5 : Python 3.11 configuré
    if check_python_version(workflow, "3.11"):
        passed("Python 3.11 configuré")
        passed_count += 1
    else:
        failed("Python 3.11 non configuré", "Ajoutez: python-version: '3.11'")
        failed_count += 1

    # Test 6 : Installation des dépendances
    if check_run_command(workflow, "pip install") and check_run_command(
        workflow, "requirements"
    ):
        passed("Installation des dépendances")
        passed_count += 1
    else:
        failed(
            "Installation des dépendances non trouvée",
            "Ajoutez: run: pip install -r requirements.txt",
        )
        failed_count += 1

    # Test 7 : Exécution de pytest
    if check_run_command(workflow, "pytest"):
        passed("Exécution de pytest")
        passed_count += 1
    else:
        failed("pytest non trouvé", "Ajoutez: run: pytest")
        failed_count += 1

    # Test 8 : Déclencheur push configuré
    if check_trigger(workflow, "push"):
        passed("Déclencheur push configuré")
        passed_count += 1
    else:
        failed("Déclencheur push non configuré", "Ajoutez: on: push:")
        failed_count += 1

    # Test 9 : Déclencheur pull_request configuré
    if check_trigger(workflow, "pull_request"):
        passed("Déclencheur pull_request configuré")
        passed_count += 1
    else:
        failed("Déclencheur pull_request non configuré", "Ajoutez: pull_request:")
        failed_count += 1

    # Test 10 : Branche main mentionnée
    if check_branch(workflow, "main"):
        passed("Branche main configurée")
        passed_count += 1
    else:
        warn("Branche main non explicitement mentionnée")

    # Résumé
    print()
    print("=========================================")
    print("📊 Résultats")
    print("=========================================")
    print()
    print(f"Tests réussis  : {GREEN}{passed_count}{NC}")
    print(f"Tests échoués  : {RED}{failed_count}{NC}")
    print()

    if failed_count == 0:
        print(f"{GREEN}🎉 Challenge réussi ! Votre workflow est prêt.{NC}")
        print()
        print("Prochaines étapes :")
        print("  1. Testez localement avec: act push")
        print("  2. Commitez et pushez vers GitHub")
        print("  3. Vérifiez l'exécution dans l'onglet Actions")
        return 0
    else:
        print(f"{RED}😢 Challenge non validé. Corrigez les erreurs ci-dessus.{NC}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
