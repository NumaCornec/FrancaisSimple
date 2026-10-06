# Cas d'usage

Un patron par type de document. Le patron donne l'ordre des informations et les interdits locaux. Le catalogue et la doctrine s'appliquent par-dessus.

## Message d'erreur

Ordre : état constaté, cause, ordre qui corrige.

1. Écrire ce que le programme constate, avec le message d'origine entre guillemets.
2. Écrire la cause connue. Si la cause n'est pas connue, l'écrire.
3. Écrire l'action qui corrige, à l'infinitif ou à l'impératif.

Aucune excuse, aucune interjection, aucun `Oups`, aucune formule `veuillez vous assurer`. Le message d'erreur s'affiche au pire moment, et le lecteur cherche une action.

Exemple : `La connexion à la base échoue. Le mot de passe du fichier de configuration a expiré. Renouveler le mot de passe, puis relancer la migration.`

## Procédure d'exploitation

Ordre : prérequis, étapes numérotées, résultat attendu, retour arrière.

1. Donner les moyens avant l'action, dans une liste non ordonnée.
2. Numéroter les étapes ordonnées, une action par étape.
3. Ajouter une consigne de sécurité avant l'étape qu'elle protège.
4. Si l'étape est risquée, décrire le retour arrière.

La procédure garde une seule forme d'instruction du début à la fin. L'infinitif reste le défaut.

## Rapport d'incident

Ordre : fait, impact mesuré, chronologie, cause, correctif, prévention.

1. Écrire le fait en premier, avec la date et l'heure.
2. Donner l'impact en chiffres mesurés, jamais en adjectifs.
3. Raconter la chronologie au présent, sans conditionnel.
4. Distinguer ce qui est établi de ce qui reste inconnu. Si la cause n'est pas établie, l'écrire.

Le passé reste possible dans la chronologie d'un journal de bord. Le présent avec une date explicite reste préférable.

## Note de version

Ordre : version, date, ajouts, corrections, ruptures, actions de migration.

1. Nommer la version et la date.
2. Décrire chaque changement en une phrase, à l'infinitif ou au présent.
3. Marquer les ruptures de compatibilité, puis donner l'action de migration.
4. Ne pas qualifier la version d'importante. Le lecteur lit les changements.

## Prompt système et AGENTS.md

Un prompt s'adresse à un lecteur qui ne peut pas poser de question. Le conditionnel y est lu comme une option, et l'interdiction y gagne plus de valeur qu'ailleurs.

1. Écrire les contraintes à l'infinitif ou à l'impératif.
2. Écrire les conditions avant les actions.
3. Donner un exemple court par contrainte non évidente.
4. Aucune préférence sans critère. `Préférer les phrases courtes` devient `Limiter chaque phrase à 20 mots`.

Le même patron s'applique à `AGENTS.md`, à un fichier de règles d'éditeur et à une instruction personnalisée de harnais.

## Préparation de traduction

Ordre : texte source stabilisé, termes figés, ambiguïtés levées.

1. Terminer les choix de vocabulaire avant la traduction.
2. Écrire un terme par concept, et le tenir.
3. Transformer chaque pronom ambigu en nom.
4. Supprimer les jeux de mots et les tournures propres à une langue.
5. Écrire les unités et les dates dans un format sans ambiguïté.

Le texte préparé sert de source stable. Une phrase qui se comprend sans son contexte se traduit sans consultation.

## Ce que le skill refuse

Le marketing, le contenu de marque, l'article de blog et la note de synthèse destinée à un comité sortent du périmètre. Le skill produit une langue plate, et ces usages demandent une hiérarchie éditoriale.
