# Délais de connexion

sqlpipe s'arrête avec `dial tcp: i/o timeout` quand le service ne peut pas joindre le port Postgres.

## Diagnostic

1. Vérifier que l'hôte qui exécute sqlpipe joint le port Postgres. Un pare-feu ou un groupe de sécurité bloque souvent la connexion.
2. Si la base est managée, vérifier que l'instance accepte les connexions depuis l'adresse IP de sqlpipe.
3. Si le réseau est lent, augmenter `source.connect_timeout_seconds` dans la configuration.

Le délai par défaut est de trente secondes. Un délai plus court provoque un arrêt du service.

## Comportement du service

Le service lit la configuration de la base au démarrage. La configuration de la base reste inchangée après l'installation.

Le script s'arrête quand il a si peu de temps pour finir la tâche. Le rapport a si peu de détails que le lecteur pose une question.

Les paquets en provenance du réseau interne arrivent sur l'interface locale. Le participant à la réunion lit le délai affiché dans le journal.

Le trafic passe par le port 5432. Le service joint la base par le port 5432 à chaque démarrage.

La documentation se trouve à l'adresse https://exemple.fr:8443/guide/index.html et reste disponible hors ligne.

1. Ouvrir le fichier `C:\Program Files\sqlpipe\config source\delais par defaut.yaml` avec un éditeur de texte, lire la valeur du délai et fermer le fichier.

Le journal s'écrit dans /var/log/sqlpipe/service.log. Le fichier `config.yaml` contient la valeur 1 250,5 dans la section des délais.

La version publiée le 18 août 2026 à 14 h 02 UTC corrige le délai par défaut. Le service redémarre en trente secondes.
