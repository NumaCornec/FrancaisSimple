# Cas pièges

Chaque paire oppose une ligne fautive à une ligne correcte, ou une ligne correcte
à une ligne piégeuse. L'annotation donne la classe attendue sur la ligne suivante.

## Participe passé féminin et participe court

<!-- attendu: passe_compose_feminin -->
La tâche a produite un rapport.

<!-- attendu: passe_compose -->
La tâche a mis à jour le rapport.

## Auxiliaire suivi d'un mot court

<!-- propre -->
Le rapport a si peu de détails que le lecteur pose une question.

<!-- propre -->
Le service a plus de trois instances actives.

## Si intensif contre condition finale

<!-- propre -->
Le service a si peu de temps pour répondre.

<!-- attendu: condition_finale -->
Redémarrer le service si la configuration change.

## En provenance contre gérondif

<!-- propre -->
Les paquets en provenance du réseau interne arrivent ici.

<!-- attendu: gerondif -->
Configurer le service en modifiant le fichier de configuration.

## Noms en -ait ou -ais contre imparfait

<!-- propre -->
Le trait du portrait reste visible sur cet extrait.

<!-- propre -->
Le délai de trente secondes reste fixe.

<!-- propre -->
Le fichier fait trente octets.

<!-- attendu: imparfait -->
Le script faisait un appel réseau chaque minute.

## Supporter tolérer contre prendre en charge

<!-- propre -->
Le service supporte une panne réseau sans perdre de données.

<!-- attendu: anglicisme -->
Cet outil supporte le format CSV et le format JSON.

## Librairie commerce contre librairie logicielle

<!-- propre -->
La librairie du quartier vend des livres anciens.

<!-- attendu: anglicisme -->
Importer la librairie de calcul dans le projet.

## Deux-points dans une adresse URL

<!-- propre -->
La documentation se trouve sur https://exemple.fr:8443/guide

<!-- attendu: typographie_espaces -->
Le fichier contient une erreur: la valeur est absente.

## Par le port contre passif avec agent

<!-- propre -->
Le trafic passe par le port 5432.

<!-- attendu: passif_avec_agent -->
Le rapport est lu par le service de supervision.

## Présent passif contre passé composé

<!-- propre -->
Le fichier est supprimé après la migration.

<!-- attendu: passe_compose -->
Le fichier a été supprimé après la migration.

## Configuration légitime contre nominalisation fautive

<!-- propre -->
La configuration de la base reste inchangée.

<!-- attendu: nominalisation -->
La suppression des anciennes tables libère de l'espace.

## Participe présent contre groupe nominal

<!-- propre -->
Le cache, un participant actif de la chaîne, redémarre.

<!-- attendu: participe_present -->
Le cache se vide, provoquant un redémarrage.

## Décompte des mots avec un long chemin

<!-- propre -->
Ouvrir le fichier `C:\Program Files\sqlpipe\config source\delais par defaut.yaml` avec un éditeur de texte, lire la valeur du délai et fermer le fichier.

<!-- attendu: phrase_longue_instruction -->
Ouvrir le fichier `C:\Program Files\sqlpipe\config source\delais par defaut.yaml` avec un éditeur de texte, lire la valeur du délai en secondes, comparer la valeur avec la limite documentée et fermer le fichier.
