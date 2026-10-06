# Résultats du benchmark

Chiffres recalculés depuis `evals/results/raw/` par `evals/check_numbers.py`. Aucun chiffre estimé.

<!-- chiffres
{
  "regles": 73,
  "sections": 9,
  "classes": 35,
  "taches": 8,
  "questions": 8,
  "modeles": 0,
  "cellules_brutes": 0,
  "violations_100_mots_temoin": null,
  "violations_100_mots_traitement": null,
  "reduction_pourcent": null,
  "phrase_longueur_moyenne_temoin": null,
  "phrase_longueur_moyenne_traitement": null
}
-->

## État

Aucune cellule brute n'existe dans `evals/results/raw/`. La grille est livrée vide.
Grille prévue : 8 tâches d'écriture et 8 questions techniques, 2 conditions, 8 × 2 × N cellules.
Le runner `evals/run_bench.py` est reprenable et écrit chaque réponse dès qu'elle aboutit.

## Protocole

- Mesure principale : violations du linter pour 100 mots, sur les huit tâches d'écriture.
- Mesure secondaire : longueur moyenne de phrase et défauts visibles, tirets longs, gras, titres, puces.
- Jugement : comparaison par paires à l'aveugle, dans les deux ordres, sans étiquette de condition.

## Limites

Taille de l'échantillon : huit tâches et huit questions par condition. Un écart de quelques dixièmes ne mesure rien.
Biais de famille possible quand le juge et le générateur partagent une famille de modèles.
Le linter ne mesure pas le choix des mots, la qualité de la terminologie, la vérité du contenu ni la lisibilité réelle par un humain.
Un texte peut obtenir zéro violation et rester mauvais.

## Ce qui n'a pas été mesuré

Aucune valeur n'est publiée pour une cellule unique. Une exécution par cellule mesure un tirage, pas un effet.
