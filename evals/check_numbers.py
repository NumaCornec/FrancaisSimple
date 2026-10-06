#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie chaque chiffre publié contre les fichiers bruts.

Relit `evals/results/RESULTS.md` et `README.md`. Recalcule les compteurs depuis
le dépôt et les mesures depuis `evals/results/raw/`. Échoue si un chiffre ne se
reproduit pas, et refuse toute publication de pourcentage sans donnée brute.

Usage : python3 evals/check_numbers.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SKILL = RACINE / "skills" / "francais-simple" / "SKILL.md"
RESULTS = RACINE / "evals" / "results" / "RESULTS.md"
README = RACINE / "README.md"
BRUT = RACINE / "evals" / "results" / "raw"

BLOC = re.compile(r"<!-- chiffres\s*(\{.*?\})\s*-->", re.DOTALL)


def charger_chiffres() -> dict:
    texte = RESULTS.read_text(encoding="utf-8")
    m = BLOC.search(texte)
    if not m:
        raise SystemExit("bloc <!-- chiffres ... --> absent de RESULTS.md")
    return json.loads(m.group(1))


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import fr_lint  # noqa: E402
    import run_bench  # noqa: E402

    declares = charger_chiffres()
    calcules = {
        "regles": len(
            {m.group(0) for m in re.finditer(r"FR-\d+\.\d+", SKILL.read_text(encoding="utf-8"))}
        ),
        "sections": len(
            {
                m.group(1)
                for m in re.finditer(r"FR-(\d+)\.\d+", SKILL.read_text(encoding="utf-8"))
            }
        ),
        "classes": len(fr_lint.CLASSES),
        "taches": len(run_bench.TACHES),
        "questions": len(run_bench.QUESTIONS),
    }
    resume = run_bench.resume()
    calcules["modeles"] = len(resume["modeles"])
    calcules["cellules_brutes"] = resume["cellules_brutes"]

    tous = run_bench.cellules_existantes()
    for condition in ("temoin", "traitement"):
        ecriture = [c for c in tous if c["condition"] == condition and c["type"] != "question"]
        calcules[f"violations_100_mots_{condition}"] = run_bench.moyenne(
            [c["mesure"]["violations_100_mots"] for c in ecriture]
        )
        calcules[f"phrase_longueur_moyenne_{condition}"] = run_bench.moyenne(
            [c["mesure"]["phrase_longueur_moyenne"] for c in tous if c["condition"] == condition]
        )
    if (
        calcules["violations_100_mots_temoin"]
        and calcules["violations_100_mots_traitement"] is not None
    ):
        calcules["reduction_pourcent"] = round(
            100
            * (
                calcules["violations_100_mots_temoin"]
                - calcules["violations_100_mots_traitement"]
            )
            / calcules["violations_100_mots_temoin"],
            1,
        )
    else:
        calcules["reduction_pourcent"] = None

    erreurs = []
    for cle, valeur in calcules.items():
        if cle not in declares:
            erreurs.append(f"chiffre absent de RESULTS.md : {cle}")
            continue
        if declares[cle] != valeur:
            erreurs.append(
                f"{cle} : RESULTS.md annonce {declares[cle]!r}, le calcul donne {valeur!r}"
            )

    texte_readme = README.read_text(encoding="utf-8") if README.exists() else ""
    for motif, cle in (
        (r"(\d+)\s+rules", "regles"),
        (r"(\d+)\s+sections", "sections"),
        (r"(\d+)\s+(?:violation\s+)?classes", "classes"),
    ):
        for m in re.finditer(motif, texte_readme):
            if int(m.group(1)) != calcules[cle]:
                erreurs.append(
                    f"README.md annonce {m.group(1)} pour {cle}, le calcul donne {calcules[cle]}"
                )

    if calcules["cellules_brutes"] == 0:
        for chemin in (RESULTS, README):
            if not chemin.exists():
                continue
            texte = chemin.read_text(encoding="utf-8")
            if chemin == RESULTS:
                texte = BLOC.sub("", texte)
            for m in re.finditer(r"\d+(?:[.,]\d+)?\s*%", texte):
                erreurs.append(
                    f"{chemin.name} publie un pourcentage sans donnée brute : {m.group(0)}"
                )

    print(f"Chiffres déclarés : {len(declares)}. Cellules brutes : {calcules['cellules_brutes']}.")
    if erreurs:
        for erreur in erreurs:
            print("ÉCHEC : " + erreur)
        return 1
    print("OK : chaque chiffre publié se recalcule depuis les fichiers bruts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
