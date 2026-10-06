#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle croisé des numéros de règle et des classes du linter.

Lit `SKILL.md`, les fichiers de `references/` et les autres documents du dépôt.
Échoue si un numéro `FR-x.y` est cité sans être défini, si une règle définie
n'est jamais citée ailleurs, ou si une classe du linter n'a pas de règle.

Usage : python3 evals/check_rules.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SKILL = RACINE / "skills" / "francais-simple" / "SKILL.md"
CATALOGUE = RACINE / "skills" / "francais-simple" / "references" / "catalogue-regles.md"

MOTIF_NUMERO = re.compile(r"FR-(\d+)\.(\d+)")
MOTIF_CLASSE_TABLEAU = re.compile(r"^\|\s*`([a-z_]+)`\s*\|", re.MULTILINE)

# Structure déclarée par le catalogue.
SECTIONS_ATTENDUES = {
    1: 10,
    2: 6,
    3: 8,
    4: 10,
    5: 8,
    6: 8,
    7: 5,
    8: 10,
    9: 8,
}

FICHIERS_IGNORES = {".git", "__pycache__", "node_modules"}
EXTENSIONS = {".md", ".py", ".json", ".yml", ".yaml"}


def fichiers_du_depot() -> list[Path]:
    trouves = []
    for chemin in sorted(RACINE.rglob("*")):
        if any(part in FICHIERS_IGNORES for part in chemin.parts):
            continue
        if chemin.is_file() and chemin.suffix in EXTENSIONS:
            trouves.append(chemin)
    return trouves


def numeros(texte: str) -> set[str]:
    return {f"FR-{m.group(1)}.{m.group(2)}" for m in MOTIF_NUMERO.finditer(texte)}


def verifier_frontmatter() -> list[str]:
    """Contrôle le frontmatter lu par les harnais et par `npx skills`.

    Une valeur non citée qui contient « : » casse l'analyse YAML de `npx skills`
    et rend le skill invisible.
    """
    erreurs: list[str] = []
    lignes = SKILL.read_text(encoding="utf-8").splitlines()
    if not lignes or lignes[0].strip() != "---":
        return ["SKILL.md ne commence pas par un frontmatter YAML"]
    fin = next((i for i, ligne in enumerate(lignes[1:], start=1) if ligne.strip() == "---"), None)
    if fin is None:
        return ["frontmatter YAML non fermé dans SKILL.md"]
    champs = {}
    for ligne in lignes[1:fin]:
        if not ligne.strip():
            continue
        if ":" not in ligne:
            erreurs.append(f"ligne de frontmatter sans clé : {ligne!r}")
            continue
        cle, valeur = ligne.split(":", 1)
        champs[cle.strip()] = valeur.strip()
    for cle in ("name", "description"):
        if not champs.get(cle):
            erreurs.append(f"frontmatter incomplet : {cle} manquant")
    if champs.get("name") and champs["name"] != SKILL.parent.name:
        erreurs.append(
            f"le nom {champs['name']!r} diffère du dossier {SKILL.parent.name!r}"
        )
    description = champs.get("description", "")
    if description and not (description.startswith('"') and description.endswith('"')):
        if ": " in description:
            erreurs.append(
                "description non citée contenant « : », l'analyse YAML casse"
            )
    return erreurs


def main() -> int:
    erreurs: list[str] = verifier_frontmatter()
    if not SKILL.exists():
        print(f"fichier absent : {SKILL}")
        return 2

    texte_skill = SKILL.read_text(encoding="utf-8")
    definies = numeros(texte_skill)

    attendues: set[str] = set()
    for section, compte in SECTIONS_ATTENDUES.items():
        for rang in range(1, compte + 1):
            attendues.add(f"FR-{section}.{rang}")
    if definies != attendues:
        manquantes = sorted(attendues - definies)
        en_trop = sorted(definies - attendues)
        if manquantes:
            erreurs.append(f"règles définies absentes de SKILL.md : {', '.join(manquantes)}")
        if en_trop:
            erreurs.append(f"numéros hors nomenclature dans SKILL.md : {', '.join(en_trop)}")

    citations: dict[str, set[str]] = {}
    for chemin in fichiers_du_depot():
        try:
            texte = chemin.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for numero in numeros(texte):
            citations.setdefault(numero, set()).add(str(chemin.relative_to(RACINE)))

    orphelins = sorted(n for n in citations if n not in definies)
    for numero in orphelins:
        for fichier in sorted(citations[numero]):
            erreurs.append(f"numéro orphelin {numero} dans {fichier}")

    jamais_citees = sorted(
        n
        for n in definies
        if not any(
            fichier != str(SKILL.relative_to(RACINE))
            for fichier in citations.get(n, set())
        )
    )
    if jamais_citees:
        erreurs.append(f"règles définies jamais citées ailleurs : {', '.join(jamais_citees)}")

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import fr_lint  # noqa: E402

    classes_code = set(fr_lint.CLASSES)
    texte_catalogue = CATALOGUE.read_text(encoding="utf-8")
    classes_doc = set(MOTIF_CLASSE_TABLEAU.findall(texte_catalogue))
    for classe in sorted(classes_code - classes_doc):
        erreurs.append(f"classe {classe} absente du tableau des classes dans catalogue-regles.md")
    for classe in sorted(classes_doc - classes_code):
        erreurs.append(f"classe {classe} documentée mais absente de fr_lint.py")
    for classe, regles in sorted(fr_lint.CLASSES.items()):
        for regle in regles:
            if regle not in definies:
                erreurs.append(f"classe {classe} liée à la règle inconnue {regle}")

    print(f"SKILL.md définit {len(definies)} règles sur {len(attendues)} attendues.")
    print(f"Citations relevées dans {len(citations)} numéros distincts.")
    print(f"Linter : {len(classes_code)} classes, documentées : {len(classes_doc)}.")
    if erreurs:
        for erreur in erreurs:
            print("ÉCHEC : " + erreur)
        return 1
    print("OK : aucun numéro orphelin, aucune règle muette, aucune classe sans règle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
