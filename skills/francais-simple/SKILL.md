---
name: francais-simple
description: "À employer pour toute rédaction ou réécriture technique en français : documentation, README, procédures d'exploitation, messages d'erreur, rapports d'incident, notes de version, prompts système, préparation de traduction. Déclencheurs : « écris ça simplement », « rédige en français contrôlé », « réécris ce message d'erreur », « applique FrancaisSimple ». Ne pas employer pour du marketing, du contenu de marque ou un article de blog."
---

# FrancaisSimple

## Ce que fait le skill

Les modèles chargent le français technique de conditionnel, de subjonctif, de participe présent et de nominalisation. Ce skill interdit ces formes, impose une forme verbale unique par procédure, et garde le code et les faits intacts.

## Les deux registres

| Registre | Emploi | Forme |
| --- | --- | --- |
| Réponse | conversation | prose seule. La première phrase répond. Aucun titre, aucun gras, aucune liste, aucun tiret long, aucune formule d'ouverture ou de clôture. |
| Document | livrable écrit | catalogue complet. La classification commande la forme verbale et la limite de mots. |

Le registre document ne s'impose jamais à une réponse de conversation.

## Classification

| Type | But | Forme verbale | Limite | Unité |
| --- | --- | --- | --- | --- |
| Procédural | faire agir | infinitif d'ordre, une seule forme du début à la fin | 20 mots | une action par étape |
| Descriptif | faire connaître | présent, futur | 25 mots | un sujet par paragraphe |

## Catalogue condensé

Texte intégral dans `references/catalogue-regles.md`. Tout numéro cité dans le dépôt existe ci-dessous.

### FR-1 Mots

- FR-1.1 Un mot porte un sens unique dans tout le document.
- FR-1.2 Employer le mot le plus simple qui dit exactement la chose.
- FR-1.3 Pas d'anglicisme quand un équivalent français courant existe.
- FR-1.4 Le jargon du domaine reste autorisé comme terme technique, employé de façon constante.
- FR-1.5 Un terme technique ne se transforme pas en verbe.
- FR-1.6 Expliquer tout terme inconnu du lecteur cible à sa première occurrence.
- FR-1.7 Développer chaque sigle à sa première occurrence, puis l'employer seul.
- FR-1.8 Pas d'adverbe d'intensité vide.
- FR-1.9 Pas de mot de valorisation non mesurable.
- FR-1.10 Pas de mot qui juge l'importance de ce qui suit.

### FR-2 Groupes nominaux

- FR-2.1 Trois noms empilés au maximum sans préposition.
- FR-2.2 Garder un article devant le nom quand le sens le permet.
- FR-2.3 Pas de nominalisation. Un verbe reste un verbe.
- FR-2.4 Pas de verbe support.
- FR-2.5 Un pronom ne remplace jamais un nom ambigu. Répéter le nom.
- FR-2.6 Pas d'emploi impersonnel de « il » dans une instruction.

### FR-3 Verbes

- FR-3.1 Quatre formes autorisées : infinitif présent, infinitif d'ordre, présent, futur.
- FR-3.2 Pas de subjonctif.
- FR-3.3 Pas de conditionnel.
- FR-3.4 Pas de temps du passé ni de temps composé dans une procédure.
- FR-3.5 Le participe passé reste autorisé comme adjectif, jamais comme verbe conjugué.
- FR-3.6 Pas de participe présent, pas de gérondif.
- FR-3.7 Voix active. Le passif sans agent reste toléré, jamais le passif avec agent.
- FR-3.8 La modalité se réduit à « pouvoir » et « devoir ».

### FR-4 Phrases

- FR-4.1 20 mots maximum pour une instruction.
- FR-4.2 25 mots maximum pour une description.
- FR-4.3 Une instruction par phrase.
- FR-4.4 Un seul niveau de subordination par phrase.
- FR-4.5 La condition précède la commande.
- FR-4.6 L'ordre du texte est l'ordre des actions.
- FR-4.7 Pas de point-virgule.
- FR-4.8 Pas de tiret cadratin ni demi-cadratin dans le corps du texte.
- FR-4.9 Pas de parenthèse qui porte une information nécessaire.
- FR-4.10 Pas de connecteur lourd.

### FR-5 Rédaction procédurale

- FR-5.1 Une seule forme d'instruction du début à la fin.
- FR-5.2 Une action par étape. Dire une simultanéité quand elle existe.
- FR-5.3 Donner les moyens avant l'action : outil, fichier, accès, droits.
- FR-5.4 Numéroter les étapes ordonnées, marquer d'une puce les listes non ordonnées.
- FR-5.5 Pas de « etc. », pas de liste ouverte.
- FR-5.6 Dire le résultat attendu quand il n'est pas évident.
- FR-5.7 Jamais de renvoi implicite à une autre étape.
- FR-5.8 Pas d'instruction négative quand une instruction positive dit la même chose.

### FR-6 Rédaction descriptive

- FR-6.1 Un sujet par paragraphe, six phrases au maximum.
- FR-6.2 La première phrase du paragraphe annonce le sujet.
- FR-6.3 Énoncer le fait, pas son importance.
- FR-6.4 Pas de moule « non seulement… mais ».
- FR-6.5 Pas d'annonce de plan, pas de conclusion récapitulative.
- FR-6.6 Pas de formule d'appel au lecteur, pas de formule de clôture.
- FR-6.7 Pas d'analogie quand un fait suffit.
- FR-6.8 Ne pas mêler procédural et descriptif dans un même passage.

### FR-7 Consignes de sécurité

- FR-7.1 Trois niveaux : « AVERTISSEMENT », « ATTENTION », « REMARQUE ».
- FR-7.2 Donner l'ordre, puis la cause.
- FR-7.3 Un niveau sans explication du risque est interdit.
- FR-7.4 Pas d'instruction dans une « REMARQUE ».
- FR-7.5 La consigne forme une phrase indépendante, placée avant l'étape qu'elle protège.

### FR-8 Typographie, nombres et décompte des mots

- FR-8.1 Espace insécable avant « : », « ; », « ! », « ? » et dans les guillemets français.
- FR-8.2 Guillemets français dans le texte courant. Guillemets droits pour le code et les identifiants.
- FR-8.3 Accentuer les majuscules.
- FR-8.4 Virgule décimale, espace insécable comme séparateur de milliers.
- FR-8.5 Unités et symboles dans leur forme française.
- FR-8.6 Espace insécable entre la valeur et l'unité.
- FR-8.7 Date et heure sans ambiguïté, fuseau nommé quand il compte.
- FR-8.8 Un identifiant, une commande, un chemin, un message ou un libellé compte pour un mot.
- FR-8.9 Les blocs de code ne se décomptent pas et ne se réécrivent pas.
- FR-8.10 Pas d'abréviation de commodité, pas d'emoji, pas de gras d'insistance, pas de majuscules d'emphase.

### FR-9 Pratiques d'écriture

- FR-9.1 Définir le public cible, le contexte et l'objectif avant de rédiger.
- FR-9.2 Chaque phrase apporte une information non déductible.
- FR-9.3 Pas de style télégraphique. Garder les articles, le mot « que » et les prépositions.
- FR-9.4 Un terme, un sens. Chercher les variantes du même concept à la relecture.
- FR-9.5 Ne pas inventer de spécifique. Si la source se tait, garder l'énoncé général.
- FR-9.6 Ne pas modifier les faits. Réécrire le style, pas le contenu.
- FR-9.7 Une phrase se comprend sans avoir lu la suivante.
- FR-9.8 Un seul registre d'adresse dans tout le document. Le vouvoiement est le défaut.

## Périmètre refusé

Le marketing, le contenu de marque et l'article de blog sortent du périmètre. Ce skill produit une langue plate et ne cherche pas une voix de marque.

## Limites

Aucun outil ne certifie la conformité à une norme de langue contrôlée. Un texte peut respecter chaque règle et rester faux ou inutile. Le FALC, l'accessibilité numérique et la mise en page relèvent d'autres référentiels. Le skill s'arrête avant le FALC, dont la validation reste hors de portée.

## Auto-contrôle avant livraison

Cette étape est obligatoire. Cinq passes.

1. Compter les mots des trois phrases les plus longues.
2. Chercher les motifs des sections FR-3 et FR-4.
3. Vérifier que chaque condition précède sa commande.
4. Chercher les variantes du même concept.
5. Vérifier la typographie, les unités et les nombres.

L'outil `evals/fr_lint.py` exécute les contrôles mécaniques de FR-1 à FR-9. La lecture humaine reste nécessaire pour FR-9.5, FR-9.6 et FR-9.7.

Les 73 règles en texte intégral, la filiation et les classes du linter vivent dans `references/`. Les mots à remplacer, les patrons par document et la passe de vérification aussi.

---

Projet non officiel, sans affiliation ni approbation de l'ASD, du STEMG ou du GIFAS. Aucun texte normatif ni contenu de dictionnaire n'est reproduit ici. Les règles sont des reformulations pédagogiques avec des exemples propres au projet. `ASD-STE100` est une marque déposée de l'ASD.
