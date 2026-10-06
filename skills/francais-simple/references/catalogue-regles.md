# Catalogue des règles

Les 73 règles du projet, en texte intégral. Chaque règle porte un numéro stable. Le numéro sert de point d'ancrage aux alertes du linter et aux renvois de la checklist.

Ce catalogue reprend l'architecture de `AminBlg/SimpleEnglish` (MIT). Les règles sont des reformulations propres au projet, sans reprise de texte normatif.

## Règle de numérotation

Le projet utilise la plage `FR-1.1` à `FR-9.8`. Trois raisons motivent une numérotation propre.

1. Une règle française telle que l'interdiction du conditionnel n'a aucun numéro dans un catalogue anglais.
2. Reprendre la séquence officielle sous les mêmes numéros s'approche d'une œuvre dérivée.
3. L'ordre des sections reste lisible pour qui connaît les catalogues de langue contrôlée.

La protection contre l'erreur principale : aucun numéro ne peut être cité s'il n'est pas défini dans `SKILL.md`. Le script `evals/check_rules.py` lit tous les fichiers, extrait chaque motif `FR-\d+\.\d+` et échoue sur un numéro orphelin.

| Section | Titre | Règles |
| --- | --- | --- |
| FR-1 | Mots | 10 |
| FR-2 | Groupes nominaux | 6 |
| FR-3 | Verbes | 8 |
| FR-4 | Phrases | 10 |
| FR-5 | Rédaction procédurale | 8 |
| FR-6 | Rédaction descriptive | 8 |
| FR-7 | Consignes de sécurité | 5 |
| FR-8 | Typographie, nombres et décompte des mots | 10 |
| FR-9 | Pratiques d'écriture | 8 |

## FR-1 — Mots

### FR-1.1 — Un mot, un sens

Un mot porte un sens unique dans tout le document. Ne pas employer deux mots pour la même chose. Ne pas employer le même mot pour deux choses.

### FR-1.2 — Le mot le plus simple

Employer le mot le plus simple qui dit exactement la chose. Un mot rare oblige le lecteur à traduire avant de comprendre.

### FR-1.3 — Pas d'anglicisme

Quand un équivalent courant existe, écrire le mot français. Quand aucun équivalent n'existe, l'emprunt anglais reste possible. Il reste possible aussi quand la forme anglaise fait partie de l'interface citée. La liste des cas courants vit dans `mots-a-remplacer.md`.

### FR-1.4 — Jargon autorisé

Le jargon du domaine reste autorisé comme terme technique. Il reste à condition d'être employé de façon constante, et d'être expliqué à sa première occurrence quand le lecteur cible ne le connaît pas.

### FR-1.5 — Un terme ne devient pas un verbe

Un terme technique ne se transforme pas en verbe. Quand le terme est installé, `indexer` reste possible. Un dérivé verbal improvisé à partir d'un nom de produit produit une phrase illisible.

### FR-1.6 — Première occurrence

Expliquer tout terme que le lecteur cible ne connaît pas déjà, à sa première occurrence, en quelques mots.

### FR-1.7 — Sigles

Développer chaque sigle à sa première occurrence, puis employer le sigle seul. Un document qui développe le sigle à chaque occurrence fatigue le lecteur. Un document qui ne le développe jamais exclut le lecteur nouveau.

### FR-1.8 — Pas d'intensité vide

Pas d'adverbe d'intensité qui n'ajoute aucun fait. La liste des cas courants vit dans `mots-a-remplacer.md`.

### FR-1.9 — Pas de valorisation non mesurable

Pas de mot de valorisation qu'aucune mesure ne soutient. Écrire le fait mesurable à la place, ou ne rien écrire.

### FR-1.10 — Pas de jugement d'importance

Pas de mot qui juge l'importance de ce qui suit. Le lecteur décide de l'importance à partir du fait.

## FR-2 — Groupes nominaux

### FR-2.1 — Trois noms au maximum

Trois noms empilés au maximum sans préposition. Au-delà, introduire une préposition ou une proposition. Une chaîne de quatre noms cache la relation entre les objets.

### FR-2.2 — Garder un article

Quand le sens le permet, garder un article ou un déterminant devant le nom. L'article porte la fonction du nom dans la phrase.

### FR-2.3 — Pas de nominalisation

Pas de nom d'action à la place d'un verbe. Un verbe reste un verbe. Le nom reste possible quand il nomme un objet stable, par exemple un fichier de configuration ou une prise de courant.

### FR-2.4 — Pas de verbe support

Pas de verbe support suivi d'un nom d'action. Le verbe porteur de l'action devient le verbe principal. La liste des locutions vit dans `mots-a-remplacer.md`.

### FR-2.5 — Répéter le nom

Un pronom ne remplace jamais un nom ambigu. Répéter le nom. La répétition coûte moins cher au lecteur qu'une recherche d'antécédent.

### FR-2.6 — Pas de « il » impersonnel

Pas d'emploi impersonnel de `il` dans une instruction ou une description. Écrire l'impératif, ou nommer le sujet de l'action.

## FR-3 — Verbes

### FR-3.1 — Quatre formes autorisées

Quatre formes verbales seulement : infinitif présent, infinitif d'ordre, présent de l'indicatif, futur de l'indicatif.

### FR-3.2 — Pas de subjonctif

Pas de subjonctif. Le subjonctif arrive par la subordination. Il signale une phrase trop construite, à casser en deux phrases.

### FR-3.3 — Pas de conditionnel

Pas de conditionnel, ni en `-rait`, ni en `-rais`. Le conditionnel porte une intention implicite. Le lecteur ne sait pas si la phrase énonce une obligation, une suggestion ou une option. Le conditionnel journalistique permet d'énoncer un fait non vérifié sans l'assumer, et disparaît pour la même raison.

### FR-3.4 — Pas de temps du passé

Pas de temps du passé ni de temps composé dans une procédure. Le présent porte le fait daté. Le passé reste légitime dans une note de version ou un journal de bord, et le présent avec une date explicite reste préférable.

### FR-3.5 — Participe passé adjectival

Le participe passé est autorisé en position d'adjectif. Il reste interdit comme verbe conjugué, c'est-à-dire derrière un auxiliaire.

### FR-3.6 — Pas de participe présent

Pas de participe présent, pas de gérondif. Le participe présent masque l'agent et l'enchaînement. La réécriture impose de nommer la relation entre les deux faits.

### FR-3.7 — Voix active

Écrire à la voix active. Le passif sans agent reste toléré quand l'agent est inconnu ou sans intérêt. Le passif avec agent explicite reste interdit, parce qu'il place l'action avant l'acteur.

### FR-3.8 — Modalité réduite

La modalité se réduit à `pouvoir` et `devoir`. Un modal porte un sens unique dans tout le document. Un modal sans complément de manière s'écrit avec le verbe principal.

## FR-4 — Phrases

### FR-4.1 — 20 mots en procédural

Une instruction compte 20 mots maximum. Le français s'allonge d'environ 20 % par rapport à l'anglais à contenu égal. La limite reste, et elle oblige à supprimer les nominalisations.

### FR-4.2 — 25 mots en descriptif

Une description compte 25 mots maximum. Au-delà, couper la phrase ou déplacer une proposition dans la phrase suivante.

### FR-4.3 — Une instruction par phrase

Une instruction par phrase. Deux verbes d'action dans une phrase forcent le lecteur à décider si les actions sont successives ou simultanées.

### FR-4.4 — Une subordination

Un seul niveau de subordination par phrase. La subordination imbriquée produit une phrase que le lecteur relit.

### FR-4.5 — Condition en tête

La condition précède la commande. Écrire `Augmenter le délai si le réseau est lent` force le lecteur à mémoriser la commande pendant qu'il lit la condition. Le contrôle mécanique porte sur les instructions.

### FR-4.6 — Ordre du texte, ordre des actions

L'ordre du texte est l'ordre des actions. Un renvoi vers une étape antérieure ou postérieure signale un plan mal ordonné.

### FR-4.7 — Pas de point-virgule

Pas de point-virgule dans le texte courant. Deux phrases séparées par un point portent chacune une idée.

### FR-4.8 — Pas de tiret long

Pas de tiret cadratin ni demi-cadratin dans le corps du texte. Le tiret long ouvre une incise dont le lecteur doit retrouver la fin. Il reste autorisé en tête de puce.

### FR-4.9 — Parenthèse non nécessaire

Pas de parenthèse qui porte une information nécessaire à la compréhension. Une information nécessaire appartient à la phrase. Une parenthèse porte un exemple court, une référence ou une précision secondaire.

### FR-4.10 — Pas de connecteur lourd

Pas de connecteur lourd. La liste des cas courants vit dans `mots-a-remplacer.md`. Le lien logique s'écrit par l'ordre des phrases, ou par un mot simple.

## FR-5 — Rédaction procédurale

### FR-5.1 — Une seule forme d'instruction

Une procédure n'emploie qu'une seule forme d'instruction, du début à la fin. Choisir l'infinitif et le tenir.

### FR-5.2 — Une action par étape

Une action par étape. Si deux actions sont simultanées, l'écrire. Un pas qui contient deux actions produit deux résultats partiels chez deux lecteurs.

### FR-5.3 — Moyens avant l'action

Donner les moyens avant l'action : outil, fichier, accès, droits. Le lecteur prépare avant de lancer.

### FR-5.4 — Numéroter ou puce

Numéroter les étapes ordonnées. Marquer d'une puce les listes non ordonnées. Le lecteur déduit l'ordre de la forme de la liste.

### FR-5.5 — Liste finie

Pas de `etc.`, pas de liste ouverte. Une liste est finie, ou elle n'est pas écrite.

### FR-5.6 — Résultat attendu

Quand la réussite n'est pas évidente, dire le résultat attendu. Le lecteur sait si l'étape a réussi.

### FR-5.7 — Pas de renvoi implicite

Jamais de renvoi implicite à une autre étape. Nommer l'étape, ou répéter l'action.

### FR-5.8 — Instruction positive

Pas d'instruction négative quand une instruction positive dit la même chose. Écrire l'action à faire. La forme négative ajoute une image mentale de l'action interdite.

## FR-6 — Rédaction descriptive

### FR-6.1 — Un sujet par paragraphe

Un sujet par paragraphe, six phrases au maximum. Un paragraphe long fait perdre le sujet au lecteur.

### FR-6.2 — Première phrase du paragraphe

La première phrase du paragraphe annonce le sujet. Le lecteur sait ce qu'il lit avant de lire.

### FR-6.3 — Énoncer le fait

Énoncer le fait, pas son importance. La liste des formules à supprimer vit dans `mots-a-remplacer.md`.

### FR-6.4 — Pas de moule rhétorique

Interdit de construire une phrase sur le moule `non seulement… mais`. Le moule impose une symétrie qui n'apporte aucun fait.

### FR-6.5 — Pas d'annonce, pas de récapitulation

Pas d'annonce de plan, pas de conclusion qui récapitule ce qui précède. Le lecteur vient chercher le fait, pas la structure du document.

### FR-6.6 — Pas de formule d'appel

Pas de formule d'appel au lecteur, pas de formule de clôture. La liste des cas courants vit dans `mots-a-remplacer.md`.

### FR-6.7 — Pas d'analogie

Pas d'analogie quand un fait suffit. L'analogie ajoute une image, donc une deuxième source de vérité.

### FR-6.8 — Ne pas mêler les genres

Ne pas mêler procédural et descriptif dans un même passage. Une note placée dans une procédure est un passage descriptif : elle suit FR-6, pas FR-5.

## FR-7 — Consignes de sécurité

### FR-7.1 — Trois niveaux

Trois niveaux seulement : `AVERTISSEMENT` pour un risque de blessure ou de mort, `ATTENTION` pour un risque de dégât matériel, `REMARQUE` pour une information.

### FR-7.2 — Ordre puis cause

Donner l'ordre, puis la cause. Jamais la cause seule.

### FR-7.3 — Risque expliqué

Un niveau sans explication du risque est interdit. Un avertissement sans cause est un avertissement que le lecteur contourne.

### FR-7.4 — Pas d'instruction en remarque

Pas d'instruction dans une `REMARQUE`. Un lecteur qui cherche une action ne lit pas les remarques.

### FR-7.5 — Consigne indépendante

La consigne forme une phrase indépendante, placée avant l'étape qu'elle protège. Elle porte le niveau, le risque et l'ordre.

## FR-8 — Typographie, nombres et décompte des mots

### FR-8.1 — Espaces insécables françaises

Espace insécable avant `:`, `;`, `!`, `?` et à l'intérieur des guillemets français.

### FR-8.2 — Guillemets français

Guillemets français dans le texte courant. Les guillemets droits sont réservés au code et aux identifiants.

### FR-8.3 — Majuscules accentuées

Accentuer les majuscules. Écrire `État`, `École`, `Université`, `Île`, `Œuvre`.

### FR-8.4 — Nombres français

Virgule décimale. Espace insécable comme séparateur de milliers. Écrire `1 250,5`.

### FR-8.5 — Unités françaises

Unités et symboles dans leur forme française. Écrire `Go`, `Mo`, `ko`, et `o` pour octet.

### FR-8.6 — Valeur et unité

Espace insécable entre la valeur et l'unité. Écrire `20 Go`, jamais `20Go`.

### FR-8.7 — Dates et heures

Formats de date et d'heure sans ambiguïté, avec le fuseau nommé quand il compte. Écrire `18 août 2026`, `14 h 02`, `14 h 02 UTC`.

### FR-8.8 — Décompte des éléments techniques

Un identifiant, une commande, un chemin, un drapeau, un message entre guillemets ou un libellé d'interface compte pour un mot. Un nombre avec son unité compte pour un mot.

### FR-8.9 — Blocs de code

Les blocs de code ne sont pas décomptés et ne sont pas réécrits. Le code, les commandes, les drapeaux et les chemins restent intacts.

### FR-8.10 — Pas de décoration

Pas d'abréviation de commodité, pas d'emoji, pas de gras d'insistance, pas de majuscules d'emphase.

## FR-9 — Pratiques d'écriture

### FR-9.1 — Cadre avant rédaction

Définir le public cible, le contexte d'usage et l'objectif avant de rédiger. Pour un document long, écrire ces trois éléments en note d'en-tête.

### FR-9.2 — Information non déductible

Chaque phrase apporte une information que le lecteur ne peut pas déduire. Une phrase qui répète la précédente sous une autre forme occupe l'attention sans rien ajouter.

### FR-9.3 — Pas de style télégraphique

Pas de style télégraphique. Garder les articles, garder `que`, garder les prépositions. La concision vient du choix des mots, pas de leur suppression.

### FR-9.4 — Un terme, un sens

Un terme, un sens. À la relecture finale, chercher les variantes du même concept.

### FR-9.5 — Pas d'invention

Ne pas inventer de spécifique. Si la source ne donne pas de chiffre, de cause ou de terme exact, garder l'énoncé général.

### FR-9.6 — Faits intacts

Ne pas modifier les faits. Réécrire le style, pas le contenu. Un modèle qui réécrit fabrique volontiers le chiffre qui rend la phrase plus concrète.

### FR-9.7 — Phrase autoportante

Une phrase se comprend sans avoir lu la suivante.

### FR-9.8 — Un seul registre d'adresse

Un seul registre d'adresse dans tout le document : tutoiement ou vouvoiement, jamais les deux. Le vouvoiement est le défaut.

## Filiation

| Section | Ascendance | Apport propre |
| --- | --- | --- |
| FR-1 Mots | STE, section des mots, ISO 24495-1 | Anglicismes, adverbes vides, mots de valorisation |
| FR-2 Groupes nominaux | STE | Nominalisations et verbes supports |
| FR-3 Verbes | Français rationalisé (GIFAS) | Conditionnel, subjonctif, participe présent, modalité |
| FR-4 Phrases | STE | Connecteurs lourds, ponctuation française |
| FR-5 Procédural | STE | Harmonie de l'infinitif, moyens avant l'action |
| FR-6 Descriptif | STE | Formules d'appel, annonces de plan |
| FR-7 Sécurité | STE | Aucun |
| FR-8 Typographie | Spécifiquement français | Intégralité |
| FR-9 Pratiques | ISO 24495-1, FALC (public cible) | Anti-invention, anti-télégraphique |

## Classes de violations du linter

Le linter `evals/fr_lint.py` produit les classes suivantes. Aucune classe n'existe sans règle correspondante, et `evals/check_rules.py` vérifie cette correspondance dans les deux sens.

| Classe | Règle | Confiance par défaut |
| --- | --- | --- |
| `condition_finale` | FR-4.5 | certain |
| `phrase_longue_instruction` | FR-4.1 | certain |
| `phrase_longue_description` | FR-4.2 | certain |
| `conditionnel` | FR-3.3 | certain |
| `subjonctif` | FR-3.2 | certain |
| `passe_compose` | FR-3.4 | certain |
| `passe_compose_feminin` | FR-3.4 | certain |
| `passe_compose_faux_positif` | FR-3.4 | garde-fou, ne produit aucune alerte |
| `plus_que_parfait` | FR-3.4 | certain |
| `imparfait` | FR-3.4 | certain |
| `participe_present` | FR-3.6 | certain |
| `gerondif` | FR-3.6 | certain |
| `passif_avec_agent` | FR-3.7 | certain |
| `verbe_support` | FR-2.3, FR-2.4 | certain |
| `nominalisation` | FR-2.3 | faible |
| `il_impersonnel` | FR-2.6 | certain |
| `modalite_floue` | FR-3.8 | certain |
| `hedging` | FR-1.8, FR-3.8 | faible |
| `mot_vide` | FR-1.8, FR-1.9, FR-1.10 | certain |
| `formule_creuse` | FR-6.3, FR-6.6 | certain |
| `connecteur_lourd` | FR-4.10 | mixte |
| `annonce_de_plan` | FR-6.5 | certain |
| `point_virgule` | FR-4.7 | certain |
| `tiret_long` | FR-4.8 | certain |
| `parenthese_necessaire` | FR-4.9 | faible |
| `anglicisme` | FR-1.3 | mixte |
| `style_telegraphique` | FR-9.3 | faible |
| `typographie_espaces` | FR-8.1, FR-8.2 | certain |
| `accent_majuscule` | FR-8.3 | certain |
| `nombre_format` | FR-8.4 | certain |
| `unite_anglaise` | FR-8.5 | certain |
| `date_ambigue` | FR-8.7 | certain |
| `emoji` | FR-8.10 | certain |
| `abreviation` | FR-8.10 | certain |
| `registre_melange` | FR-9.8 | certain |

## Frontière du catalogue

Le catalogue ne contient pas de dictionnaire de mots approuvés. Le principe du vocabulaire contrôlé s'applique, la liste fermée n'existe pas.

Le catalogue ne contient pas de règle de mise en page, ni de règle d'accessibilité numérique. Le FALC et le RGAA traitent un autre sujet.
