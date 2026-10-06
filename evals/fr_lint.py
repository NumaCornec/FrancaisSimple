#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linter déterministe du français technique contrôlé.

Architecture reprise de `AminBlg/SimpleEnglish` (MIT). Aucune règle n'est
recopiée d'un document normatif.

Usage :
    python3 evals/fr_lint.py fichier.md [fichier2.md ...]
    python3 evals/fr_lint.py fichier.md --json
    python3 evals/fr_lint.py --self-test

Bibliothèque standard uniquement. Le code de sortie vaut 0 quand aucune
violation ne reste hors d'un contre-exemple balisé, 1 sinon.

Zones protégées, jamais signalées :
  - le frontmatter YAML, les titres, les blocs de code, le code en ligne,
    les adresses URL, les messages entre guillemets ;
  - le texte entre `<!-- contre-exemple -->` et `<!-- fin contre-exemple -->` ;
  - le texte entre une ligne qui commence par `Avant` et une ligne qui
    commence par `Après`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

VERSION = "0.1.0"

# Classe de violation -> règles du catalogue. Une classe sans règle n'existe pas.
CLASSES: dict[str, tuple[str, ...]] = {
    "condition_finale": ("FR-4.5",),
    "phrase_longue_instruction": ("FR-4.1",),
    "phrase_longue_description": ("FR-4.2",),
    "conditionnel": ("FR-3.3",),
    "subjonctif": ("FR-3.2",),
    "passe_compose": ("FR-3.4",),
    "passe_compose_feminin": ("FR-3.4",),
    "passe_compose_faux_positif": ("FR-3.4",),
    "plus_que_parfait": ("FR-3.4",),
    "imparfait": ("FR-3.4",),
    "participe_present": ("FR-3.6",),
    "gerondif": ("FR-3.6",),
    "passif_avec_agent": ("FR-3.7",),
    "verbe_support": ("FR-2.3", "FR-2.4"),
    "nominalisation": ("FR-2.3",),
    "il_impersonnel": ("FR-2.6",),
    "modalite_floue": ("FR-3.8",),
    "hedging": ("FR-1.8", "FR-3.8"),
    "mot_vide": ("FR-1.8", "FR-1.9", "FR-1.10"),
    "formule_creuse": ("FR-6.3", "FR-6.6"),
    "connecteur_lourd": ("FR-4.10",),
    "annonce_de_plan": ("FR-6.5",),
    "point_virgule": ("FR-4.7",),
    "tiret_long": ("FR-4.8",),
    "parenthese_necessaire": ("FR-4.9",),
    "anglicisme": ("FR-1.3",),
    "style_telegraphique": ("FR-9.3",),
    "typographie_espaces": ("FR-8.1", "FR-8.2"),
    "accent_majuscule": ("FR-8.3",),
    "nombre_format": ("FR-8.4",),
    "unite_anglaise": ("FR-8.5",),
    "date_ambigue": ("FR-8.7",),
    "emoji": ("FR-8.10",),
    "abreviation": ("FR-8.10",),
    "registre_melange": ("FR-9.8",),
}

# Classes qui ne produisent jamais d'alerte : garde-fous de précision.
CLASSES_SANS_ALERTE = frozenset({"passe_compose_faux_positif"})

PLACEHOLDER = "\uE000"

FORMES_PASSE = re.compile(
    r"(?:[éè]es?|[éè]|ies?|ie|is|its?|it|us?|ues?|ue|erts?|ait|aits)$"
)

# Mots courts et adverbes qui suivent un auxiliaire sans être un participe.
FAUX_POSITIFS_PASSE = frozenset(
    """
    si ni qui ici ainsi aussi oui lui plus moins très bien mal tout tous toute
    toutes déjà encore jamais rien peu tant autant mieux pire lieu cours raison
    tort besoin envie peur honte faim soif sommeil froid chaud une un des du de
    le la les ce cette ces mon ton son notre votre leur leurs sa ma ta deux
    trois quatre cinq six sept huit neuf dix vingt cent mille nouveau beau haut
    bas fort faible grand petit moyen même tel quel
    """.split()
)

PARTICIPES_FEMININS = re.compile(
    r"\b(?:a|as|avons|avez|ont)\s+"
    r"(?:pas\s+)?(mise|mises|construite|construites|produite|produites|faite|"
    r"faites|ouverte|ouvertes|offerte|offertes|écrite|écrites|prise|prises|"
    r"apprise|apprises|reçue|reçues|vue|vues|due|dues|sue|sues|lue|lues|"
    r"connue|connues|tenue|tenues|venue|venues|devenue|devenues)\b"
)

EXCEPTIONS_CONDITIONNEL = frozenset(
    """
    trait traits attrait attraits portrait portraits extrait extraits distrait
    distraite distraits abstrait abstraite abstraits retrait retraite
    soustrait vrai vrais frais jamais mais
    """.split()
)

EXCEPTIONS_IMPARFAIT = frozenset(
    """
    fait faits trait traits extrait extraits portrait portraits attrait attraits
    retrait retraite souhait souhaits essai essais délai délais quai quais vrai
    vrais frais jamais mais français française palais anglais contrat contrats
    format détail détails résultat résultats parfait parfaite parfaits parfaites
    imparfait imparfaite imparfaits imparfaites bienfait méfait forfait surfaite
    """.split()
)

RADICAUX_IMPARFAIT = (
    "étudi vérifi analys configur install exécut lanc utilis modifi supprim ajout "
    "cré test déploy observ rédig écriv fais all ven part pren mett pouv dev "
    "voul sav dir li écout cherch montr expliqu corrig relaç relanç arrêt démarr "
    "redémarr présent termin occup prépar permett essay av ét"
).split()

EXCEPTIONS_PARTICIPE_PRESENT = frozenset(
    """
    participant participants étudiant étudiants assistant assistants consultant
    consultants commandant dirigeant enseignante enseignant représentant
    représentants important importante importants importantes intéressant
    intéressante intéressants surprenant surprenante permanent permanente
    identifiant identifiants
    """.split()
)

GERONDIFS = frozenset(
    """
    permettant évitant utilisant effectuant suivant créant produisant causant
    entraînant générant provoquant lançant redémarrant contenant portant servant
    ayant étant faisant disant mettant prenant venant allant donnant indiquant
    précisant ajoutant supprimant modifiant vérifiant exécutant installant
    démarrant attendant retournant laissant plaçant tirant passant jouant
    """.split()
)

EXCEPTIONS_GERONDIF = frozenset(
    "avant provenance attente cours fonction amont aval revanche place".split()
)

LIEUX_APRES_PAR = frozenset(
    "port réseau câble chemin route canal tunnel proxy lien passerelle".split()
)

REMPLACEMENTS_NOMINALISATION = {
    "vérification": "vérifier",
    "suppression": "supprimer",
    "lancement": "lancer",
    "analyse": "analyser",
    "modification": "modifier",
    "installation": "installer",
    "récupération": "récupérer",
    "création": "créer",
    "utilisation": "utiliser",
    "validation": "valider",
    "exécution": "exécuter",
    "mise": "mettre",
    "prise": "prendre",
    "réalisation": "réaliser",
    "traitement": "traiter",
    "positionnement": "positionner",
}

NOMS_LEGITIMES = frozenset(
    """
    configuration documentation information version fonction question solution
    attention application option connexion migration installation opération
    présentation description position action section mention
    message image page plage garage voyage étage village nuage langage équipage
    visage paysage bagage mirage sillage courage orage structure nature culture
    voiture peinture ouverture écriture lecture procédure architecture
    température signature confiture clôture chaussure serrure monture toiture
    ceinture teinture brûlure importance différence existence expérience présence
    puissance chance urgence prudence violence naissance connaissance croissance
    abondance distance concurrence conférence référence préférence apparence
    assistance assurance document moment instrument complément monument parlement
    sentiment argument appartement département bâtiment aliment élément logement
    équipement médicament condition addition mission passion impression expression
    profession session pression dimension tension extension pension convention
    intention occasion télévision
    """.split()
)

FORMULES_CREUSES = (
    "il est important de noter",
    "il convient de souligner",
    "on notera que",
    "rappelons que",
    "force est de constater",
    "à noter que",
    "il faut garder à l'esprit",
    "veuillez noter",
    "n'hésitez pas à",
    "nous vous prions de",
    "nous espérons que",
    "bonne lecture",
)

CONNECTEURS_CERTAINS = (
    "cependant",
    "toutefois",
    "néanmoins",
    "par ailleurs",
    "dès lors",
    "en effet",
    "de ce fait",
    "à cet égard",
    "par conséquent",
    "en conséquence",
)

ANNONCES = (
    "nous allons voir",
    "dans cette section",
    "ce document présente",
    "cet article présente",
    "en résumé",
    "en définitive",
    "pour conclure",
    "nous verrons",
    "dans ce qui suit",
    "dans la suite de ce document",
)

HEDGING = (
    "éventuellement",
    "dans la mesure du possible",
    "le cas échéant",
    "en principe",
    "généralement",
    "normalement",
    "si possible",
    "autant que possible",
    "de préférence",
)

MODALITES_FLOUES = (
    r"\b(?:être|est|sont|sera|seront|serait|seraient)\s+(?:susceptibles?|à même de|en mesure de|en capacité de)\b",
    r"\b(?:avoir|a|ont)\s+la\s+(?:possibilité|capacité|faculté)\s+de\b",
)

MOTS_VALORISANTS = frozenset(
    "robuste performant optimal puissant moderne avancé fluide élégant".split()
)

MOTS_IMPORTANCE = frozenset(
    "crucial essentiel important primordial majeur fondamental clé incontournable".split()
)

ACCENTS_MAJUSCULES = {
    "Etat": "État",
    "Ecole": "École",
    "Universite": "Université",
    "Ile": "Île",
    "Oeuvre": "Œuvre",
    "Eglise": "Église",
    "Eleve": "Élève",
    "Etudiant": "Étudiant",
    "Etranger": "Étranger",
    "Evenement": "Événement",
    "Ete": "Été",
    "Editeur": "Éditeur",
    "Ecosysteme": "Écosystème",
    "Epreuve": "Épreuve",
    "Ecriture": "Écriture",
}

ANGLICISMES_CERTAINS = {
    r"\bdigital(?:e|es|aux?)?\b": "numérique",
    r"\bimpact(?:er|e|es|ent|era|eront|é|ée|és|ées|ait|aient)\b": "avoir un effet sur, modifier",
    r"\biniti(?:er|e|es|ent|era|eront|é|ée|és|ées)\b": "lancer, engager",
    r"\bsur base de\b": "d'après, à partir de",
    r"\bfai(?:re|t|s|sait|saient) sens\b": "avoir un sens",
    r"\bà date\b": "à ce jour",
}

ANGLICISMES_FAIBLES = {
    "opportunité": "occasion, possibilité",
    "challenger": "contester, remettre en question",
}

CONTEXTE_ARTEFACT = re.compile(
    r"\b(?:format|service|protocole|fichier|langage|type|requête|charges?|"
    r"connexion|version|instruction|commande)\b",
    re.IGNORECASE,
)

CONTEXTE_TOLERANCE = re.compile(
    r"\b(?:panne|pannes|erreur|erreurs|coupure|absence|défaillance|retard|"
    r"charge|lenteur|interruption)\b",
    re.IGNORECASE,
)

CONTEXTE_LOGICIEL = re.compile(
    r"\b(?:python|javascript|npm|paquet|logiciel|code|dépendance|importer|"
    r"installer|développeur|compilateur)\b",
    re.IGNORECASE,
)

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D\u2764]"
)


@dataclass
class Ligne:
    numero: int
    brute: str
    masque_fort: str
    masque_faible: str
    exclue: bool = False
    balisee: bool = False


@dataclass
class Violation:
    classe: str
    ligne: int
    confiance: str
    extrait: str
    suggestion: str | None = None
    contre_exemple: bool = False

    @property
    def regles(self) -> tuple[str, ...]:
        return CLASSES[self.classe]

    def en_dict(self) -> dict:
        return {
            "classe": self.classe,
            "regles": list(self.regles),
            "confiance": self.confiance,
            "ligne": self.ligne,
            "longueur": len(self.extrait),
            "extrait": self.extrait,
            "suggestion": self.suggestion,
            "contre_exemple": self.contre_exemple,
        }


def masquer(texte: str) -> tuple[str, str]:
    """Masque les zones protégées. Retourne (masque fort, masque faible)."""
    faible = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texte)
    faible = re.sub(r"`+[^`]*`+", PLACEHOLDER, faible)
    faible = re.sub(r"\b(?:https?|ftp)://\S+", PLACEHOLDER, faible)
    faible = re.sub(r"\bwww\.\S+", PLACEHOLDER, faible)
    faible = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", PLACEHOLDER, faible)
    fort = re.sub(r"«[^»]*»", PLACEHOLDER, faible)
    fort = re.sub(r'"[^"\n]*"', PLACEHOLDER, fort)
    return fort, faible


def decouper(chemin: Path) -> list[Ligne]:
    """Lit un fichier et retourne les lignes avec leurs masques."""
    lignes: list[Ligne] = []
    texte = chemin.read_text(encoding="utf-8")
    dans_code = False
    dans_contre_exemple = False
    dans_avant = False
    dans_frontmatter = False
    for numero, brute in enumerate(texte.splitlines(), start=1):
        nu = brute.strip()
        if numero == 1 and nu == "---":
            dans_frontmatter = True
            lignes.append(Ligne(numero, brute, "", "", exclue=True))
            continue
        if dans_frontmatter:
            lignes.append(Ligne(numero, brute, "", "", exclue=True))
            if nu == "---":
                dans_frontmatter = False
            continue
        if re.match(r"^\s*(?:```|~~~)", brute):
            dans_code = not dans_code
            lignes.append(Ligne(numero, brute, "", "", exclue=True))
            continue
        if dans_code:
            lignes.append(Ligne(numero, brute, "", "", exclue=True))
            continue
        if "<!-- contre-exemple -->" in brute:
            dans_contre_exemple = True
            lignes.append(Ligne(numero, brute, "", "", exclue=True))
            continue
        if "<!-- fin contre-exemple -->" in brute:
            dans_contre_exemple = False
            lignes.append(Ligne(numero, brute, "", "", exclue=True))
            continue
        if re.match(r"^\s*\*{0,2}Avant\b", brute):
            dans_avant = True
            lignes.append(Ligne(numero, brute, "", "", exclue=True))
            continue
        if dans_avant and re.match(r"^\s*\*{0,2}Après\b", brute):
            dans_avant = False
            lignes.append(Ligne(numero, brute, "", "", exclue=True))
            continue
        fort, faible = masquer(brute)
        lignes.append(
            Ligne(
                numero,
                brute,
                fort,
                faible,
                exclue=False,
                balisee=dans_contre_exemple or dans_avant,
            )
        )
    return lignes


def est_titre(ligne: Ligne) -> bool:
    return ligne.brute.lstrip().startswith("#")


def est_tableau(ligne: Ligne) -> bool:
    return ligne.brute.lstrip().startswith("|")


def premier_mot(ligne: Ligne) -> str:
    texte = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", ligne.masque_fort)
    texte = re.sub(r"^\*+|\*+$", "", texte.strip())
    mot = texte.split(" ")[0].strip("«»\"'.,:()[]*")
    return mot.lower()


def mot_est_instruction(mot: str) -> bool:
    if not mot:
        return False
    if mot.startswith("ne pas") or mot.startswith("ne jamais"):
        return True
    if re.match(r"^[a-zà-ÿ]{3,}(?:er|ir|re)$", mot) and mot not in {"hier", "mer", "cher"}:
        return True
    if mot.endswith("ez") and mot not in {"assez", "nez", "chez", "gaz"}:
        return True
    return False


def est_instruction(ligne: Ligne) -> bool:
    return mot_est_instruction(premier_mot(ligne))


def est_instruction_texte(texte: str) -> bool:
    texte = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", texte.strip())
    texte = re.sub(r"^\*+|\*+$", "", texte.strip())
    mot = texte.split(" ")[0].strip("«»\"'.,:()[]*").lower()
    return mot_est_instruction(mot)


def compter_mots(texte: str) -> int:
    return len(re.findall(r"\S+", texte))


def nettoyer_texte(ligne: Ligne) -> str:
    texte = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", ligne.masque_fort)
    return texte.strip()


def ajouter(
    trouves: list[Violation],
    classe: str,
    ligne: Ligne,
    extrait: str,
    suggestion: str | None = None,
    confiance: str | None = None,
) -> None:
    if classe in CLASSES_SANS_ALERTE:
        return
    trouves.append(
        Violation(
            classe=classe,
            ligne=ligne.numero,
            confiance=confiance or confiance_de(classe),
            extrait=re.sub(r"\s+", " ", extrait).strip()[:120],
            suggestion=suggestion,
        )
    )


CONFIANCE_FAIBLE = frozenset(
    {
        "nominalisation",
        "hedging",
        "anglicisme",
        "style_telegraphique",
        "imparfait",
        "participe_present",
        "parenthese_necessaire",
    }
)


def confiance_de(classe: str) -> str:
    return "faible" if classe in CONFIANCE_FAIBLE else "certain"


def est_faux_positif_passe(candidat: str) -> bool:
    """Garde-fou de la classe passe_compose_faux_positif."""
    mot = candidat.lower()
    if mot in FAUX_POSITIFS_PASSE:
        return True
    if len(mot) < 3:
        return True
    return False


def sentence_lengths(ligne: Ligne, trouves: list[Violation]) -> None:
    if est_titre(ligne) or est_tableau(ligne) or ligne.exclue or ligne.balisee:
        return
    texte = nettoyer_texte(ligne)
    if not texte:
        return
    phrases = re.split(r"(?<=[.!?…])\s+", texte)
    for rang, phrase in enumerate(phrases):
        if not phrase.strip():
            continue
        total = compter_mots(phrase)
        instruction = est_instruction_texte(phrase) or (rang == 0 and est_instruction(ligne))
        if instruction and total > 20:
            ajouter(trouves, "phrase_longue_instruction", ligne, phrase)
        elif not instruction and total > 25:
            ajouter(trouves, "phrase_longue_description", ligne, phrase)


def condition_finale(ligne: Ligne, trouves: list[Violation]) -> None:
    if est_titre(ligne) or est_tableau(ligne):
        return
    texte = nettoyer_texte(ligne)
    for rang, phrase in enumerate(re.split(r"(?<=[.!?…])\s+", texte)):
        if not (est_instruction_texte(phrase) or (rang == 0 and est_instruction(ligne))):
            continue
        m = re.search(r"\b(si|quand|lorsque|dès que)\b", phrase)
        if not m or m.start() < 3:
            continue
        avant = phrase[: m.start()]
        confiance = "certain" if avant.rstrip().endswith(",") else "faible"
        ajouter(
            trouves,
            "condition_finale",
            ligne,
            phrase,
            "placer la condition en tête de phrase",
            confiance,
        )


def conditionnel(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r"\b[a-zà-ÿ]{2,}(?:raient|rait|rions|riez|rais)\b",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        mot = m.group(0).lower()
        if mot in EXCEPTIONS_CONDITIONNEL:
            continue
        suggestion = None
        if mot in {"serait", "seraient"}:
            suggestion = "employer le présent de l'indicatif"
        ajouter(trouves, "conditionnel", ligne, m.group(0), suggestion)


def subjonctif(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r"\b(?:afin|pour|bien|avant|sans|de peur|de crainte|jusqu'à ce|en attendant)"
        r"\s*qu[e']",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        ajouter(trouves, "subjonctif", ligne, m.group(0))
    for m in re.finditer(r"\bil faut qu[e']", ligne.masque_fort, re.IGNORECASE):
        ajouter(trouves, "subjonctif", ligne, m.group(0))
    for m in re.finditer(
        r"\bqu[e'](?:\s+[a-zà-ÿ'’-]+){0,3}\s+"
        r"(?:soit|soient|sois|ait|aient|aies|puisse|puissent|doive|doivent|"
        r"fasse|fassent|vienne|viennent|prenne|prennent|sache|sachent|faille|"
        r"vaille|serve|servent|mette|mettent|reçoive|reçoivent|parte|partent)\b",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        ajouter(trouves, "subjonctif", ligne, m.group(0))


def passe_compose(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in PARTICIPES_FEMININS.finditer(ligne.masque_fort):
        ajouter(trouves, "passe_compose_feminin", ligne, m.group(0))
    for m in re.finditer(
        r"\b(a|as|avons|avez|ont)\s+"
        r"(?:pas\s+|plus\s+|moins\s+|jamais\s+|rien\s+|déjà\s+|bien\s+|"
        r"encore\s+|trop\s+|si\s+|aussi\s+|tout\s+)?"
        r"([a-zà-ÿ]+)\b",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        candidat = m.group(2)
        if est_faux_positif_passe(candidat):
            continue
        if candidat in FAUX_POSITIFS_PASSE:
            continue
        if not FORMES_PASSE.search(candidat):
            continue
        if len(candidat) < 3:
            continue
        confiance = "certain" if candidat.endswith(("é", "ée", "és", "ées")) else "faible"
        ajouter(trouves, "passe_compose", ligne, m.group(0), None, confiance)


def plus_que_parfait(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r"\b(avait|avaient)\s+(?:pas\s+)?([a-zà-ÿ]+)\b",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        candidat = m.group(2)
        if est_faux_positif_passe(candidat) or not FORMES_PASSE.search(candidat):
            continue
        ajouter(trouves, "plus_que_parfait", ligne, m.group(0))


def imparfait(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r"\b([a-zà-ÿ]{4,})(ait|aient|ions|iez|ais)\b",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        mot = m.group(0).lower()
        radical = m.group(1).lower()
        terminaison = m.group(2)
        if mot in EXCEPTIONS_IMPARFAIT:
            continue
        if mot.endswith(("rait", "raient")):
            continue
        if terminaison in {"ions", "iez", "ais"}:
            if not radical.endswith("i") and not any(
                radical.startswith(rad) for rad in RADICAUX_IMPARFAIT
            ):
                continue
            if not radical.endswith("i") and terminaison == "ais":
                continue
        ajouter(
            trouves,
            "imparfait",
            ligne,
            m.group(0),
            None,
            "certain" if terminaison in {"ait", "aient"} else "faible",
        )


def participe_present(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r",\s+([a-zà-ÿ]{3,}ant(?:s|e|es)?)\b", ligne.masque_fort, re.IGNORECASE
    ):
        mot = m.group(1)
        if mot.lower() in EXCEPTIONS_PARTICIPE_PRESENT:
            continue
        confiance = "certain" if mot.lower() in GERONDIFS else "faible"
        ajouter(trouves, "participe_present", ligne, m.group(0), None, confiance)


def gerondif(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r"\ben\s+([a-zà-ÿ]{4,}ant)\b", ligne.masque_fort, re.IGNORECASE
    ):
        if m.group(1).lower() in EXCEPTIONS_GERONDIF:
            continue
        ajouter(trouves, "gerondif", ligne, m.group(0))


def passif_avec_agent(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r"\b(est|sont|sera|seront|semble|semblent)\s+"
        r"([a-zà-ÿ]+(?:é|ée|és|ées|is|it|us?|ert))\s+par\s+"
        r"(le|la|les|un|une|des|l')\s*([a-zà-ÿ]\w*)",
        ligne.masque_fort,
    ):
        if m.group(4).lower() in LIEUX_APRES_PAR:
            continue
        ajouter(trouves, "passif_avec_agent", ligne, m.group(0), "écrire à la voix active")


def verbe_support(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r"\b(procéder à|procède à|procèdent à|effectuer|effectue|effectuent|"
        r"réaliser|réalise|réalisent|mettre en œuvre|met en œuvre|mettent en œuvre|"
        r"opérer|opère|opèrent|assurer|assure|assurent)\s+"
        r"(?:la|le|les|l'|un|une|des|du|au|aux)?\s*"
        r"([a-zà-ÿ]{4,}(?:tion|sion|ment|age|ure|ance|ence))\b",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        ajouter(trouves, "verbe_support", ligne, m.group(0), "employer le verbe d'action")


def nominalisation(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(
        r"\b(?:la|le|les|l'|une|un|des|du|au|aux|cette|cet|ce|ces|sa|son|ses|"
        r"ma|mon|mes|ta|ton|tes|notre|nos|votre|vos|leur|leurs)\s+"
        r"([a-zà-ÿ]{4,}(?:tion|sion|ment|age|ure|ance|ence))\s+"
        r"(de la|de l'|de|du|des|d')\b",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        nom = m.group(1).lower()
        if nom in NOMS_LEGITIMES:
            continue
        if nom in REMPLACEMENTS_NOMINALISATION:
            ajouter(
                trouves,
                "nominalisation",
                ligne,
                m.group(0),
                f"employer le verbe « {REMPLACEMENTS_NOMINALISATION[nom]} »",
                "certain",
            )
            continue
        ajouter(trouves, "nominalisation", ligne, m.group(0), None, "faible")


def il_impersonnel(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r"\bil\s+(faut|convient)\b", ligne.masque_fort, re.IGNORECASE):
        ajouter(trouves, "il_impersonnel", ligne, m.group(0), "employer l'impératif")
    for m in re.finditer(
        r"\bil\s+est\s+(nécessaire|possible|recommandé|important|utile|"
        r"préférable|souhaitable|interdit|obligatoire|conseillé)\b",
        ligne.masque_fort,
        re.IGNORECASE,
    ):
        ajouter(trouves, "il_impersonnel", ligne, m.group(0), "employer l'impératif")


def modalite_floue(ligne: Ligne, trouves: list[Violation]) -> None:
    for motif in MODALITES_FLOUES:
        for m in re.finditer(motif, ligne.masque_fort, re.IGNORECASE):
            ajouter(trouves, "modalite_floue", ligne, m.group(0), "employer « pouvoir » ou « devoir »")


def hedging(ligne: Ligne, trouves: list[Violation]) -> None:
    for mot in HEDGING:
        for m in re.finditer(
            r"\b" + re.escape(mot) + r"\b", ligne.masque_fort, re.IGNORECASE
        ):
            ajouter(trouves, "hedging", ligne, m.group(0), "dire la condition ou la fréquence réelle")


def formule_creuse(ligne: Ligne, trouves: list[Violation]) -> None:
    for mot in FORMULES_CREUSES:
        for m in re.finditer(re.escape(mot), ligne.masque_fort, re.IGNORECASE):
            ajouter(trouves, "formule_creuse", ligne, m.group(0), "supprimer la formule")


def connecteur_lourd(ligne: Ligne, trouves: list[Violation]) -> None:
    for mot in CONNECTEURS_CERTAINS:
        for m in re.finditer(r"\b" + re.escape(mot) + r"\b", ligne.masque_fort, re.IGNORECASE):
            ajouter(trouves, "connecteur_lourd", ligne, m.group(0), "lier les phrases par l'ordre")
    for m in re.finditer(r"\bainsi\b", ligne.masque_fort, re.IGNORECASE):
        ajouter(trouves, "connecteur_lourd", ligne, m.group(0), None, "faible")
    for m in re.finditer(r"(?:^|[.!?»]\s)Or,", ligne.masque_fort):
        ajouter(trouves, "connecteur_lourd", ligne, m.group(0))


def annonce_de_plan(ligne: Ligne, trouves: list[Violation]) -> None:
    for mot in ANNONCES:
        for m in re.finditer(re.escape(mot), ligne.masque_fort, re.IGNORECASE):
            ajouter(trouves, "annonce_de_plan", ligne, m.group(0), "supprimer l'annonce")


def point_virgule(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r";", ligne.masque_fort):
        ajouter(trouves, "point_virgule", ligne, m.group(0), "couper en deux phrases")


def tiret_long(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r"[—–]", ligne.masque_faible):
        avant = ligne.masque_faible[: m.start()]
        if not avant.strip() or re.fullmatch(r"\s*(?:[-*+]|\d+[.)])", avant):
            continue
        if re.fullmatch(
            r"\s*(?:[-*+]|\d+[.)])\s+(?:[A-Za-zÀ-ÿ0-9][\wÀ-ÿ.-]*\s*)?", avant
        ):
            continue
        ajouter(trouves, "tiret_long", ligne, ligne.brute[max(0, m.start() - 30) : m.start() + 30])


def parenthese_necessaire(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r"\(([^()]*)\)", ligne.masque_faible):
        interieur = m.group(1)
        if compter_mots(interieur) > 6 or re.search(
            r"\b(?:est|sont|sera|seront|doit|doivent|peut|peuvent|permet|"
            r"permettent|faut|convient|a été|ont été)\b",
            interieur,
            re.IGNORECASE,
        ):
            ajouter(trouves, "parenthese_necessaire", ligne, m.group(0), "intégrer l'information à la phrase", "faible")


def anglicisme(ligne: Ligne, trouves: list[Violation]) -> None:
    texte = ligne.masque_fort
    for motif, remplacement in ANGLICISMES_CERTAINS.items():
        for m in re.finditer(motif, texte, re.IGNORECASE):
            ajouter(trouves, "anglicisme", ligne, m.group(0), remplacement, "certain")
    for m in re.finditer(r"\badresser\s+(?:un|le|ce|des|les)\s+(?:problème|problèmes|question|sujet|dossier)\b", texte):
        ajouter(trouves, "anglicisme", ligne, m.group(0), "traiter, résoudre", "certain")
    for m in re.finditer(r"\bbas[ée]e?s?\s+sur\b", texte):
        ajouter(trouves, "anglicisme", ligne, m.group(0), "fondé sur, repose sur", "certain")
    for m in re.finditer(
        r"\bsupport(?:er|e|es|ent|era|eront|é|ée|és|ées|ait|aient)\b",
        texte,
        re.IGNORECASE,
    ):
        debut = max(0, m.start() - 60)
        contexte = texte[debut : m.end() + 60]
        suite = texte[m.end() : m.end() + 40]
        if CONTEXTE_TOLERANCE.search(suite) or re.match(r"\s+que\b", suite):
            continue
        if CONTEXTE_ARTEFACT.search(contexte):
            ajouter(trouves, "anglicisme", ligne, m.group(0), "prendre en charge, accepter", "faible")
    for m in re.finditer(r"\blibrairie\b", texte, re.IGNORECASE):
        debut = max(0, m.start() - 80)
        contexte = texte[debut : m.end() + 80]
        if CONTEXTE_LOGICIEL.search(contexte) and not re.search(r"\blivres?\b|\bcommerce\b", contexte):
            ajouter(trouves, "anglicisme", ligne, m.group(0), "bibliothèque", "faible")
    for mot, remplacement in ANGLICISMES_FAIBLES.items():
        for m in re.finditer(r"\b" + re.escape(mot) + r"\b", texte, re.IGNORECASE):
            ajouter(trouves, "anglicisme", ligne, m.group(0), remplacement, "faible")
    for m in re.finditer(r"\bau niveau de\b", texte, re.IGNORECASE):
        ajouter(trouves, "anglicisme", ligne, m.group(0), "pour, dans, concernant", "faible")
    for m in re.finditer(r"\bdélivrer\s+(?:une?|des|les|la|le)\s+(?:fonctionnalité|service|valeur|jeton|attestation)", texte, re.IGNORECASE):
        ajouter(trouves, "anglicisme", ligne, m.group(0), "livrer, fournir", "faible")
    for m in re.finditer(r"\b(?:très|vraiment|particulièrement|extrêmement|totalement|absolument|parfaitement)\b", texte, re.IGNORECASE):
        ajouter(trouves, "mot_vide", ligne, m.group(0), "supprimer l'adverbe", "certain")
    for m in re.finditer(r"\b(?:" + "|".join(sorted(MOTS_VALORISANTS)) + r")\b", texte, re.IGNORECASE):
        ajouter(trouves, "mot_vide", ligne, m.group(0), "écrire le fait mesuré", "certain")
    for m in re.finditer(r"\b(?:" + "|".join(sorted(MOTS_IMPORTANCE)) + r")\b", texte, re.IGNORECASE):
        ajouter(trouves, "mot_vide", ligne, m.group(0), "supprimer le jugement d'importance", "certain")


def style_telegraphique(ligne: Ligne, trouves: list[Violation]) -> None:
    texte = nettoyer_texte(ligne)
    for m in re.finditer(
        r"^(?:[A-ZÀ-Ý][a-zà-ÿ]*(?:er|ir|re)|Ne pas)\s+"
        r"(?!(?:le|la|les|l'|un|une|des|du|de|d'|au|aux|ce|cet|cette|ces|mon|ma|"
        r"mes|ton|ta|tes|son|sa|ses|notre|nos|votre|vos|leur|leurs|tout|toute|"
        r"tous|toutes|chaque|quelque|quelques|plusieurs|deux|trois|quatre|cinq|"
        r"six|sept|huit|neuf|dix|plus|moins)\b)"
        r"([a-zà-ÿ]{4,})\s+(de la|de l'|de|du|des|d'|après|avant|au|aux|avec)\b",
        texte,
    ):
        if re.search(r"(?:er|ir|re)$", m.group(1)):
            continue
        ajouter(trouves, "style_telegraphique", ligne, m.group(0), "rétablir l'article ou le déterminant", "faible")
    for m in re.finditer(
        r",\s*([a-zà-ÿ]{3,}(?:er|ir|re))\s+([a-zà-ÿ]{3,})\s*[.!]",
        texte,
    ):
        if m.group(2).lower() in {
            "le",
            "la",
            "les",
            "un",
            "une",
            "des",
            "du",
            "ce",
            "cette",
            "ces",
            "son",
            "sa",
            "ses",
            "votre",
            "vos",
        }:
            continue
        ajouter(trouves, "style_telegraphique", ligne, m.group(0), "rétablir l'article ou le déterminant", "faible")


def typographie_espaces(ligne: Ligne, trouves: list[Violation]) -> None:
    texte = ligne.masque_faible
    for m in re.finditer(r":", texte):
        avant = texte[: m.start()]
        apres = texte[m.end() :]
        if avant.endswith(("/", ":")) or apres.startswith(("//", ":")):
            continue
        if avant and not avant[-1].isspace():
            ajouter(trouves, "typographie_espaces", ligne, ligne.brute[max(0, m.start() - 25) : m.end() + 25], "ajouter l'espace insécable avant le deux-points")
    for m in re.finditer(r'"[^"\n]{2,}"', texte):
        ajouter(trouves, "typographie_espaces", ligne, m.group(0), "employer les guillemets français", "faible")


def accent_majuscule(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r"\b(?:" + "|".join(ACCENTS_MAJUSCULES) + r")\b", ligne.masque_faible):
        mot = m.group(0)
        if mot.isupper():
            continue
        ajouter(trouves, "accent_majuscule", ligne, mot, ACCENTS_MAJUSCULES[mot])


def nombre_format(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r"\b\d{1,3}(?:,\d{3})+\b", ligne.masque_faible):
        ajouter(trouves, "nombre_format", ligne, m.group(0), "employer l'espace insécable comme séparateur de milliers")
    for m in re.finditer(r"(?<![\w.,/-])\d+\.\d+(?![\w.])", ligne.masque_faible):
        ajouter(trouves, "nombre_format", ligne, m.group(0), "employer la virgule décimale")


def unite_anglaise(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r"\b\d+(?:[.,]\d+)?\s*(?:GB|MB|KB|TB|PB|kB)\b", ligne.masque_faible):
        ajouter(trouves, "unite_anglaise", ligne, m.group(0), "employer Go, Mo, ko, To, Po")


def date_ambigue(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", ligne.masque_faible):
        ajouter(trouves, "date_ambigue", ligne, m.group(0), "écrire la date en toutes lettres")
    for m in re.finditer(r"\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\b", ligne.masque_faible):
        ajouter(trouves, "date_ambigue", ligne, m.group(0), "écrire l'heure au format français avec le fuseau")
    for m in re.finditer(r"\b\d{1,2}\s*(?:AM|PM)\b", ligne.masque_faible):
        ajouter(trouves, "date_ambigue", ligne, m.group(0), "écrire l'heure au format français avec le fuseau")


def emoji(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in EMOJI.finditer(ligne.masque_faible):
        ajouter(trouves, "emoji", ligne, m.group(0), "supprimer l'emoji")


def abreviation(ligne: Ligne, trouves: list[Violation]) -> None:
    for m in re.finditer(r"\b(?:etc|env|cf|p\.\s?ex|i\.e|e\.g)\.", ligne.masque_fort):
        ajouter(trouves, "abreviation", ligne, m.group(0), "écrire le mot en entier")


def registre_melange(
    lignes: list[Ligne], trouves: list[Violation], inclure_balisees: bool = False
) -> None:
    tu = re.compile(r"\b(?:tu|te|toi|ton|ta|tes|tien|tienne)\b", re.IGNORECASE)
    vous = re.compile(r"\b(?:vous|votre|vos)\b", re.IGNORECASE)
    ligne_tu = None
    vu_vous = False
    for ligne in lignes:
        if ligne.exclue or est_titre(ligne):
            continue
        if ligne.balisee and not inclure_balisees:
            continue
        if tu.search(ligne.masque_fort):
            if ligne_tu is None:
                ligne_tu = ligne
        if vous.search(ligne.masque_fort):
            vu_vous = True
    if ligne_tu is not None and vu_vous:
        ajouter(
            trouves,
            "registre_melange",
            ligne_tu,
            ligne_tu.brute,
            "garder un seul registre d'adresse, le vouvoiement par défaut",
        )
        trouves[-1].contre_exemple = ligne_tu.balisee


def analyser_lignes(lignes: list[Ligne], inclure_balisees: bool = False) -> list[Violation]:
    trouves: list[Violation] = []
    for ligne in lignes:
        if ligne.exclue or est_titre(ligne):
            continue
        if ligne.balisee and not inclure_balisees:
            continue
        avant = len(trouves)
        sentence_lengths(ligne, trouves)
        condition_finale(ligne, trouves)
        conditionnel(ligne, trouves)
        subjonctif(ligne, trouves)
        passe_compose(ligne, trouves)
        plus_que_parfait(ligne, trouves)
        imparfait(ligne, trouves)
        participe_present(ligne, trouves)
        gerondif(ligne, trouves)
        passif_avec_agent(ligne, trouves)
        verbe_support(ligne, trouves)
        nominalisation(ligne, trouves)
        il_impersonnel(ligne, trouves)
        modalite_floue(ligne, trouves)
        hedging(ligne, trouves)
        formule_creuse(ligne, trouves)
        connecteur_lourd(ligne, trouves)
        annonce_de_plan(ligne, trouves)
        point_virgule(ligne, trouves)
        tiret_long(ligne, trouves)
        parenthese_necessaire(ligne, trouves)
        anglicisme(ligne, trouves)
        style_telegraphique(ligne, trouves)
        typographie_espaces(ligne, trouves)
        accent_majuscule(ligne, trouves)
        nombre_format(ligne, trouves)
        unite_anglaise(ligne, trouves)
        date_ambigue(ligne, trouves)
        emoji(ligne, trouves)
        abreviation(ligne, trouves)
        if ligne.balisee:
            for violation in trouves[avant:]:
                violation.contre_exemple = True
    registre_melange(lignes, trouves, inclure_balisees)
    return trouves


def trier(violations: list[Violation]) -> list[Violation]:
    rang = {"certain": 0, "faible": 1}
    return sorted(violations, key=lambda v: (rang.get(v.confiance, 2), v.ligne, v.classe))


def lint_chemin(chemin: Path, inclure_balisees: bool = False) -> list[Violation]:
    lignes = decouper(chemin)
    return trier(analyser_lignes(lignes, inclure_balisees))


def lint_texte(texte: str) -> list[Violation]:
    lignes = []
    for numero, brute in enumerate(texte.splitlines(), start=1):
        fort, faible = masquer(brute)
        lignes.append(Ligne(numero, brute, fort, faible))
    return trier(analyser_lignes(lignes))


def formater(violations: list[Violation], chemin: str) -> str:
    lignes = []
    for v in violations:
        regles = ", ".join(v.regles)
        suite = f" → {v.suggestion}" if v.suggestion else ""
        lignes.append(
            f"{chemin}:{v.ligne}: {v.confiance} {v.classe} ({regles}) : « {v.extrait} »{suite}"
        )
    return "\n".join(lignes)


# --------------------------------------------------------------------------
# Auto-test
# --------------------------------------------------------------------------

ANNOTATION = re.compile(r"^<!-- (attendu|ensemble): ?(.*?) -->$")
PROPRE = re.compile(r"^<!-- propre -->$")
FIN_ENSEMBLE = re.compile(r"^<!-- fin ensemble -->$")


def iterer_cas(chemin: Path):
    """Parcourt une fixture annotée. Rend (ligne, classes attendues, texte)."""
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    en_attente = None
    ensemble = None
    bloc: list[str] = []
    depart = 0
    for numero, brute in enumerate(lignes, start=1):
        nu = brute.strip()
        if FIN_ENSEMBLE.match(nu):
            yield depart, ensemble or set(), "\n".join(bloc)
            ensemble = None
            bloc = []
            continue
        if ensemble is not None:
            bloc.append(brute)
            continue
        m = ANNOTATION.match(nu)
        if m:
            en_attente = {c.strip() for c in m.group(2).split(",") if c.strip()}
            if m.group(1) == "ensemble":
                ensemble = en_attente
                depart = numero
            continue
        if PROPRE.match(nu):
            en_attente = set()
            continue
        if not nu or nu.startswith("<!--") or nu.startswith("#"):
            continue
        if en_attente is None:
            continue
        yield numero, en_attente, brute
        en_attente = None


def auto_test() -> int:
    base = Path(__file__).resolve().parent / "fixtures"
    echecs = 0

    propre = base / "texte-propre.md"
    violations = [v for v in lint_chemin(propre) if not v.contre_exemple]
    if violations:
        print(f"ÉCHEC : {propre.name} doit produire 0 violation, {len(violations)} trouvée(s).")
        print(formater(violations, propre.name))
        echecs += 1
    else:
        print(f"OK : {propre.name} produit 0 violation.")

    for nom in ("fautes-attendues.md", "cas-pieges.md"):
        chemin = base / nom
        for numero, attendues, texte in iterer_cas(chemin):
            trouvees = {
                v.classe
                for v in lint_texte(texte)
                if v.classe not in CLASSES_SANS_ALERTE
            }
            if trouvees != attendues:
                echecs += 1
                print(
                    f"ÉCHEC : {nom}:{numero}\n"
                    f"  texte    : {texte.strip()}\n"
                    f"  attendu  : {sorted(attendues) or 'aucune'}\n"
                    f"  trouvé   : {sorted(trouvees) or 'aucune'}"
                )
    if echecs == 0:
        print("OK : tous les cas pièges sont détectés, toutes les lignes propres restent muettes.")
    return 1 if echecs else 0


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(
        description="Linter déterministe du français technique contrôlé."
    )
    parseur.add_argument("fichiers", nargs="*", type=Path)
    parseur.add_argument("--json", action="store_true", help="sortie machine")
    parseur.add_argument("--self-test", action="store_true", help="suite de tests interne")
    parseur.add_argument("--version", action="version", version=VERSION)
    parseur.add_argument(
        "--liste-classes", action="store_true", help="afficher les classes et leurs règles"
    )
    parseur.add_argument(
        "--verifier-balises",
        action="store_true",
        help="exiger que toute violation reste dans une zone balisée",
    )
    args = parseur.parse_args(argv)

    if args.self_test:
        return auto_test()
    if args.liste_classes:
        for classe, regles in sorted(CLASSES.items()):
            print(f"{classe} : {', '.join(regles)}")
        return 0
    if not args.fichiers:
        parseur.print_help()
        return 2

    rapport = {}
    total_hors = 0
    total_dans = 0
    for chemin in args.fichiers:
        if not chemin.exists():
            print(f"fichier absent : {chemin}", file=sys.stderr)
            return 2
        violations = lint_chemin(chemin, inclure_balisees=True)
        rapport[str(chemin)] = [v.en_dict() for v in violations]
        hors = [v for v in violations if not v.contre_exemple]
        dans = [v for v in violations if v.contre_exemple]
        total_hors += len(hors)
        total_dans += len(dans)
        if not args.json:
            print(formater(hors, str(chemin)))
            if dans and args.verifier_balises:
                for v in dans:
                    print("contre-exemple " + formater([v], str(chemin)).strip())

    if args.json:
        print(json.dumps({"fichiers": rapport, "hors_contre_exemple": total_hors}, ensure_ascii=False, indent=2))
    else:
        print(
            f"Total : {total_hors} violation(s) hors contre-exemple, "
            f"{total_dans} dans un contre-exemple balisé."
        )
    return 1 if total_hors else 0


if __name__ == "__main__":
    raise SystemExit(main())
