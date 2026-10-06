# Checklist de vérification

La passe complète avant livraison. Les motifs de recherche sont classés par section. Le linter exécute les contrôles mécaniques, la lecture humaine traite le reste.

## Convention de balisage des contre-exemples

Un document du dépôt montre parfois une faute volontaire. Ce passage s'entoure d'un bloc balisé, et le linter le signale comme contre-exemple au lieu d'une violation.

```
<!-- contre-exemple -->
Phrase fautive, montrée pour l'exemple.
<!-- fin contre-exemple -->
```

Un bloc de code délimité par trois accents graves reste hors du décompte et hors des contrôles. C'est le balisage à employer pour une liste de mots ou une commande.

## Passe 1 — Longueur

Compter les mots des trois phrases les plus longues. La limite est de 20 mots pour une instruction et de 25 mots pour une description. Un identifiant, une commande, un chemin, un message entre guillemets et un nombre avec son unité comptent pour un mot.

## Passe 2 — Formes verbales

```
Formes interdites : subjonctif · conditionnel · passé composé · plus-que-parfait
imparfait · passé simple · futur antérieur · participe présent · gérondif
```

Motifs recherchables, classés par règle.

```
FR-3.2 : afin que · pour que · bien que · avant que · il faut que
FR-3.3 : -rait · -raient · -rais · -rions · -riez
FR-3.4 : a + participe passé · est + participe passé · avait + participe passé · était + participe passé
FR-3.6 : « , » suivi d'un mot en -ant · « en » suivi d'un mot en -ant
FR-3.7 : est/sont/sera + participe passé + par
FR-3.8 : être susceptible de · être à même de · être en mesure de · avoir la possibilité de
```

## Passe 3 — Conditions et subordination

Chaque condition précède sa commande. Chercher `si`, `quand`, `lorsque` et `dès que` dans la seconde moitié d'une instruction. Vérifier aussi le nombre de niveaux de subordination, un seul par phrase.

## Passe 4 — Vocabulaire

Chercher les variantes du même concept et garder un seul terme. Vérifier les sigles développés à leur première occurrence. Vérifier les termes techniques expliqués à leur première occurrence.

```
Motifs : nominalisations en -tion · -sion · -ment · -age · -ure · -ance · -ence
verbes supports : procéder à · effectuer · réaliser · mettre en œuvre · opérer · assurer
modalité floue : éventuellement · le cas échéant · en principe · généralement
formules creuses : il est important de noter · on notera que · veuillez noter · n'hésitez pas à
connecteurs lourds : cependant · toutefois · néanmoins · par ailleurs · dès lors · en effet
```

## Passe 5 — Typographie, nombres et unités

```
espace avant : ; ! ?  ·  guillemets français  ·  majuscules accentuées
virgule décimale  ·  espace de milliers  ·  unités Go, Mo, ko, o
date longue et heure avec fuseau  ·  aucune abréviation de commodité
aucun emoji  ·  aucun gras d'insistance  ·  aucune majuscule d'emphase
```

## Passe humaine

Trois règles résistent au contrôle mécanique. Les relire à la main.

- FR-9.5 — Aucun spécifique inventé. Un chiffre, une cause ou un terme exact sort de la source, jamais du modèle.
- FR-9.6 — Les faits restent intacts. Le style change, le contenu ne change pas.
- FR-9.7 — Chaque phrase se comprend sans la suivante.

## Exécution du linter

```
python3 evals/fr_lint.py fichier.md
python3 evals/fr_lint.py fichier.md --json
python3 evals/fr_lint.py --self-test
```

Le rapport trie par confiance décroissante. Une alerte de confiance `certain` demande une correction. Une alerte de confiance `faible` revient au rédacteur.
