#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runner de benchmark reproductible, bibliothèque standard uniquement.

Grille : N modèles × 8 tâches d'écriture × 2 conditions, plus 8 questions
techniques. Chaque génération s'écrit dès qu'elle aboutit. Le runner saute au
redémarrage toute cellule déjà présente.

Le prompt part sur l'entrée standard de la commande fournie par `--cmd`.
Exemple avec une CLI déjà authentifiée :

    python3 evals/run_bench.py --models modele-a,modele-b \
        --cmd "codex exec --model {model} -"

Autres commandes :
    python3 evals/run_bench.py --dry-run
    python3 evals/run_bench.py --models modele-a --cmd "..." --report
    python3 evals/run_bench.py --models modele-a --cmd "..." --judge
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SKILL = RACINE / "skills" / "francais-simple" / "SKILL.md"
BRUT = RACINE / "evals" / "results" / "raw"
RESULTATS = RACINE / "evals" / "results" / "RESULTS.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fr_lint  # noqa: E402

TAILLE_ECHANTILLON = 8

TACHES = [
    {
        "id": "readme",
        "type": "README",
        "consigne": "Rédige le README d'une bibliothèque Python de journalisation, en français : installation, usage, options, limites.",
    },
    {
        "id": "message-erreur",
        "type": "message d'erreur",
        "consigne": "Écris le message d'erreur affiché quand une connexion à PostgreSQL échoue à cause d'un mot de passe expiré.",
    },
    {
        "id": "procedure",
        "type": "procédure d'exploitation",
        "consigne": "Écris la procédure de redémarrage d'un service systemd avec vérification du cache et retour arrière.",
    },
    {
        "id": "incident",
        "type": "rapport d'incident",
        "consigne": "Rédige le rapport d'un incident de onze minutes survenu le 18 août 2026 : 12 % des requêtes en échec, cause inconnue, piste du déploiement.",
    },
    {
        "id": "note-version",
        "type": "note de version",
        "consigne": "Écris la note de version 2.4.0 : support des fichiers de plus de 2 Go, correction du plantage sur fichier vide, nouvelle commande de vérification.",
    },
    {
        "id": "depannage",
        "type": "guide de dépannage",
        "consigne": "Écris un guide de dépannage pour une erreur de délai de connexion réseau vers une base managée.",
    },
    {
        "id": "prompt",
        "type": "prompt système",
        "consigne": "Écris le prompt système d'un agent qui résume des tickets sans inventer de chiffre.",
    },
    {
        "id": "traduction",
        "type": "préparation de traduction",
        "consigne": "Prépare la traduction d'un paragraphe d'aide qui décrit la priorité des tâches et renvoie à une étape antérieure.",
    },
]

QUESTIONS = [
    {
        "id": "idempotence",
        "question": "Explique l'idempotence d'une requête HTTP dans un contexte de reprise après incident.",
        "jargon": "idempotence",
    },
    {
        "id": "latence",
        "question": "Explique la différence entre latence et débit pour un service réseau.",
        "jargon": "latence",
    },
    {
        "id": "cache",
        "question": "Explique le rôle d'un cache de second niveau dans une architecture à plusieurs instances.",
        "jargon": "cache de second niveau",
    },
    {
        "id": "migration",
        "question": "Explique comment une migration de schéma sans arrêt de service évite les verrous longs.",
        "jargon": "verrou long",
    },
    {
        "id": "observabilite",
        "question": "Explique la différence entre métrique, journal et trace dans la supervision d'un service.",
        "jargon": "observabilité",
    },
    {
        "id": "quorum",
        "question": "Explique le quorum dans un système de stockage distribué.",
        "jargon": "quorum",
    },
    {
        "id": "slo",
        "question": "Explique la différence entre un objectif de niveau de service et un budget d'erreur.",
        "jargon": "budget d'erreur",
    },
    {
        "id": "backpressure",
        "question": "Explique le rôle de la contre-pression dans une file de messages.",
        "jargon": "contre-pression",
    },
]

CRITERES = ["exactitude", "clarte", "concision", "absence_d_ambiguite", "respect_du_perimetre"]

CONDITIONS = {
    "temoin": "Réponds à la demande suivante.",
    "traitement": "Applique le skill FrancaisSimple décrit ci-dessous, puis réponds à la demande.",
}


def lire_skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def prompt_tache(tache: dict, condition: str) -> str:
    corps = f"{CONDITIONS[condition]}\n\n{tache['consigne']}\n"
    if condition == "traitement":
        return f"{corps}\n{reste_du_skill()}"
    return corps


def prompt_question(demande: dict, condition: str) -> str:
    corps = f"{CONDITIONS[condition]}\n\n{demande['question']}\n"
    if condition == "traitement":
        return f"{corps}\n{reste_du_skill()}"
    return corps


def reste_du_skill() -> str:
    return lire_skill()


def appeler(cmd: str, modele: str, prompt: str, delai: int = 600) -> tuple[str, int, float]:
    commande = shlex.split(cmd.replace("{model}", modele))
    debut = time.time()
    try:
        resultat = subprocess.run(
            commande,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=delai,
        )
    except FileNotFoundError as erreur:
        raise SystemExit(f"commande introuvable : {commande[0]} ({erreur})")
    duree = time.time() - debut
    sortie = resultat.stdout or ""
    if resultat.returncode != 0 and not sortie:
        sortie = resultat.stderr
    return sortie, resultat.returncode, duree


def phrases(texte: str) -> list[str]:
    lignes = texte.splitlines()
    toutes = []
    for ligne in lignes:
        if ligne.strip().startswith("#") or ligne.strip().startswith("```"):
            continue
        fort, _ = fr_lint.masquer(ligne)
        for phrase in re.split(r"(?<=[.!?…])\s+", fort):
            if fr_lint.compter_mots(phrase) >= 3:
                toutes.append(phrase)
    return toutes


def mesurer(texte: str, type_document: str) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tampon:
        tampon.write(texte)
        chemin = Path(tampon.name)
    try:
        violations = fr_lint.lint_chemin(chemin)
    finally:
        chemin.unlink(missing_ok=True)
    brut = re.sub(r"(?s)```.*?```", " ", texte)
    mots = fr_lint.compter_mots(brut)
    longueurs = [fr_lint.compter_mots(p) for p in phrases(texte)]
    return {
        "type": type_document,
        "mots": mots,
        "violations": [v.en_dict() for v in violations],
        "violations_100_mots": round(100 * len(violations) / mots, 2) if mots else None,
        "phrase_longueur_moyenne": round(statistics.mean(longueurs), 2) if longueurs else None,
        "phrase_longueur_max": max(longueurs) if longueurs else None,
        "defauts_visibles": {
            "tirets_longs": len(re.findall(r"[—–]", brut)),
            "gras": len(re.findall(r"\*\*[^*]+\*\*", brut)),
            "titres": len(re.findall(r"^#{1,6}\s", brut, re.MULTILINE)),
            "puces": len(re.findall(r"^\s*[-*+]\s", brut, re.MULTILINE)),
        },
    }


def chemin_cellule(condition: str, modele: str, cellule: str) -> Path:
    return BRUT / condition / modele / f"{cellule}.json"


def executer_cellule(
    cmd: str,
    modele: str,
    condition: str,
    cellule: str,
    prompt: str,
    type_document: str,
    force: bool,
    essai: bool,
) -> None:
    chemin = chemin_cellule(condition, modele, cellule)
    if chemin.exists() and not force:
        return
    if essai:
        print(f"essai : {condition}/{modele}/{cellule}")
        return
    print(f"génération : {condition}/{modele}/{cellule}")
    reponse, code, duree = appeler(cmd, modele, prompt)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    donnees = {
        "modele": modele,
        "condition": condition,
        "cellule": cellule,
        "type": type_document,
        "horodatage": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "code_sortie": code,
        "duree_s": round(duree, 2),
        "prompt": prompt,
        "reponse": reponse,
        "mesure": mesurer(reponse, type_document),
    }
    chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8")


def cellules_existantes() -> list[dict]:
    if not BRUT.exists():
        return []
    cellules = []
    for chemin in sorted(BRUT.rglob("*.json")):
        if "juge" in chemin.parts:
            continue
        try:
            cellules.append(json.loads(chemin.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return cellules


def moyenne(valeurs: list[float]) -> float | None:
    propres = [v for v in valeurs if v is not None]
    return round(statistics.mean(propres), 2) if propres else None


def resume() -> dict:
    cellules = cellules_existantes()
    modeles = sorted({c["modele"] for c in cellules})
    resume_par_modele = {}
    for modele in modeles:
        ligne = {"modele": modele}
        for condition in CONDITIONS:
            sous = [c for c in cellules if c["modele"] == modele and c["condition"] == condition]
            ecriture = [c for c in sous if c["type"] != "question"]
            questions = [c for c in sous if c["type"] == "question"]
            ligne[condition] = {
                "cellules": len(sous),
                "violations_100_mots": moyenne([c["mesure"]["violations_100_mots"] for c in ecriture]),
                "phrase_longueur_moyenne": moyenne(
                    [c["mesure"]["phrase_longueur_moyenne"] for c in sous]
                ),
                "defauts_visibles": {
                    cle: sum(c["mesure"]["defauts_visibles"][cle] for c in questions)
                    for cle in ("tirets_longs", "gras", "titres", "puces")
                },
            }
        temoin = ligne["temoin"]["violations_100_mots"]
        traitement = ligne["traitement"]["violations_100_mots"]
        if temoin is not None and traitement is not None and temoin > 0:
            ligne["reduction_pourcent"] = round(100 * (temoin - traitement) / temoin, 1)
        else:
            ligne["reduction_pourcent"] = None
        resume_par_modele[modele] = ligne
    return {
        "modeles": modeles,
        "cellules_brutes": len(cellules),
        "par_modele": resume_par_modele,
    }


def ecrire_rapport() -> int:
    donnees = resume()
    regles = len(set(re.findall(r"FR-\d+\.\d+", SKILL.read_text(encoding="utf-8"))))
    chiffres = {
        "regles": regles,
        "sections": 9,
        "classes": len(fr_lint.CLASSES),
        "taches": len(TACHES),
        "questions": len(QUESTIONS),
        "modeles": len(donnees["modeles"]),
        "cellules_brutes": donnees["cellules_brutes"],
        "violations_100_mots_temoin": None,
        "violations_100_mots_traitement": None,
        "reduction_pourcent": None,
        "phrase_longueur_moyenne_temoin": None,
        "phrase_longueur_moyenne_traitement": None,
    }
    if donnees["cellules_brutes"]:
        tous = cellules_existantes()
        for condition, cle in (
            ("temoin", "violations_100_mots_temoin"),
            ("traitement", "violations_100_mots_traitement"),
        ):
            ecriture = [
                c for c in tous if c["condition"] == condition and c["type"] != "question"
            ]
            chiffres[cle] = moyenne([c["mesure"]["violations_100_mots"] for c in ecriture])
            serie = [c["mesure"]["phrase_longueur_moyenne"] for c in tous if c["condition"] == condition]
            chiffres["phrase_longueur_moyenne_" + condition] = moyenne(serie)
        if chiffres["violations_100_mots_temoin"] and chiffres["violations_100_mots_traitement"] is not None:
            chiffres["reduction_pourcent"] = round(
                100
                * (chiffres["violations_100_mots_temoin"] - chiffres["violations_100_mots_traitement"])
                / chiffres["violations_100_mots_temoin"],
                1,
            )

    lignes = [
        "# Résultats du benchmark",
        "",
        "Chiffres recalculés depuis `evals/results/raw/` par `evals/check_numbers.py`. Aucun chiffre estimé.",
        "",
        "<!-- chiffres",
        json.dumps(chiffres, ensure_ascii=False, indent=2),
        "-->",
        "",
    ]
    if not donnees["cellules_brutes"]:
        lignes += [
            "## État",
            "",
            "Aucune cellule brute n'existe dans `evals/results/raw/`. La grille est livrée vide.",
            f"Grille prévue : 8 tâches d'écriture et 8 questions techniques, 2 conditions, {len(TACHES)} × 2 × N cellules.",
            "Le runner `evals/run_bench.py` est reprenable et écrit chaque réponse dès qu'elle aboutit.",
            "",
            "## Protocole",
            "",
            "- Mesure principale : violations du linter pour 100 mots, sur les huit tâches d'écriture.",
            "- Mesure secondaire : longueur moyenne de phrase et défauts visibles, tirets longs, gras, titres, puces.",
            "- Jugement : comparaison par paires à l'aveugle, dans les deux ordres, sans étiquette de condition.",
            "",
        ]
    else:
        lignes += ["## Violations pour 100 mots", "", "| Modèle | Témoin | Traitement | Réduction |", "| --- | --- | --- | --- |"]
        for modele, ligne in donnees["par_modele"].items():
            reduction = (
                f"{ligne['reduction_pourcent']} %"
                if ligne["reduction_pourcent"] is not None
                else "sans objet"
            )
            lignes.append(
                f"| {modele} | {ligne['temoin']['violations_100_mots']} | "
                f"{ligne['traitement']['violations_100_mots']} | {reduction} |"
            )
        lignes += ["", "## Longueur moyenne de phrase", "", "| Modèle | Témoin | Traitement |", "| --- | --- | --- |"]
        for modele, ligne in donnees["par_modele"].items():
            lignes.append(
                f"| {modele} | {ligne['temoin']['phrase_longueur_moyenne']} | "
                f"{ligne['traitement']['phrase_longueur_moyenne']} |"
            )
        lignes += ["", "## Défauts visibles sur les questions", "", "| Modèle | Condition | Tirets longs | Gras | Titres | Puces |", "| --- | --- | --- | --- | --- | --- |"]
        for modele, ligne in donnees["par_modele"].items():
            for condition in CONDITIONS:
                d = ligne[condition]["defauts_visibles"]
                lignes.append(
                    f"| {modele} | {condition} | {d['tirets_longs']} | {d['gras']} | {d['titres']} | {d['puces']} |"
                )
        lignes.append("")

    lignes += [
        "## Limites",
        "",
        "Taille de l'échantillon : huit tâches et huit questions par condition. Un écart de quelques dixièmes ne mesure rien.",
        "Biais de famille possible quand le juge et le générateur partagent une famille de modèles.",
        "Le linter ne mesure pas le choix des mots, la qualité de la terminologie, la vérité du contenu ni la lisibilité réelle par un humain.",
        "Un texte peut obtenir zéro violation et rester mauvais.",
        "",
        "## Ce qui n'a pas été mesuré",
        "",
        "Aucune valeur n'est publiée pour une cellule unique. Une exécution par cellule mesure un tirage, pas un effet.",
        "",
    ]
    RESULTATS.write_text("\n".join(lignes), encoding="utf-8")
    print(f"rapport écrit : {RESULTATS.relative_to(RACINE)}")
    return 0


def juger(cmd: str, modele: str, force: bool) -> int:
    cellules = [c for c in cellules_existantes() if c["condition"] == "traitement"]
    groupes: dict[str, list[dict]] = {}
    for cellule in cellules:
        groupes.setdefault(cellule["cellule"], []).append(cellule)
    for identifiant, membres in sorted(groupes.items()):
        temoins = [c for c in cellules_existantes() if c["cellule"] == identifiant and c["condition"] == "temoin" and c["modele"] == membres[0]["modele"]]
        if not temoins:
            continue
        for cible in sorted({c["modele"] for c in membres}):
            traitement = next(c for c in membres if c["modele"] == cible)
            temoin = temoins[0]
            for ordre, (gauche, droite) in enumerate(
                [(temoin, traitement), (traitement, temoin)]
            ):
                chemin = BRUT / "juge" / f"{identifiant}__{cible}__ordre{ordre}.json"
                if chemin.exists() and not force:
                    continue
                prompt = (
                    "Compare deux réponses techniques. Aucune étiquette ne donne la condition. "
                    "Note chaque critère de la liste : " + ", ".join(CRITERES) + ".\n"
                    "Réponds par une ligne par critère, au format exact `VERDICT critère: A` ou `B` ou `égalité`.\n\n"
                    f"Réponse A :\n{gauche['reponse']}\n\nRéponse B :\n{droite['reponse']}\n"
                )
                reponse, code, duree = appeler(cmd, cible, prompt)
                chemin.parent.mkdir(parents=True, exist_ok=True)
                chemin.write_text(
                    json.dumps(
                        {
                            "cellule": identifiant,
                            "modele": cible,
                            "ordre": ordre,
                            "gauche": gauche["condition"],
                            "droite": droite["condition"],
                            "horodatage": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            "code_sortie": code,
                            "duree_s": round(duree, 2),
                            "reponse_brute": reponse,
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                print(f"jugement écrit : {chemin.relative_to(RACINE)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description="Runner de benchmark FrancaisSimple.")
    parseur.add_argument("--models", default="", help="liste de modèles séparés par une virgule")
    parseur.add_argument("--cmd", default="", help="commande, avec {model}, prompt sur l'entrée standard")
    parseur.add_argument("--force", action="store_true", help="réécrire les cellules existantes")
    parseur.add_argument("--dry-run", action="store_true", help="lister les cellules sans exécuter")
    parseur.add_argument("--report", action="store_true", help="régénérer RESULTS.md depuis les fichiers bruts")
    parseur.add_argument("--judge", action="store_true", help="exécuter le jugement par paires")
    args = parseur.parse_args(argv)

    if args.report:
        return ecrire_rapport()
    if args.dry_run:
        for tache in TACHES:
            for condition in CONDITIONS:
                print(f"{condition}/<modele>/{tache['id']} : {tache['type']}")
        for question in QUESTIONS:
            for condition in CONDITIONS:
                print(f"{condition}/<modele>/question-{question['id']}")
        return 0

    modeles = [m.strip() for m in args.models.split(",") if m.strip()]
    if not modeles or not args.cmd:
        print("--models et --cmd sont obligatoires hors --dry-run et --report.", file=sys.stderr)
        return 2

    for modele in modeles:
        for tache in TACHES:
            for condition in CONDITIONS:
                executer_cellule(
                    args.cmd,
                    modele,
                    condition,
                    tache["id"],
                    prompt_tache(tache, condition),
                    tache["type"],
                    args.force,
                    False,
                )
        for question in QUESTIONS:
            for condition in CONDITIONS:
                executer_cellule(
                    args.cmd,
                    modele,
                    condition,
                    f"question-{question['id']}",
                    prompt_question(question, condition),
                    "question",
                    args.force,
                    False,
                )
    if args.judge:
        for modele in modeles:
            juger(args.cmd, modele, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
