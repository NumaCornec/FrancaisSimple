# Fixture des fautes attendues

Chaque ligne porte une annotation. La linter doit produire exactement les classes
annoncées. Un commentaire vide signifie qu'aucune classe ne doit remonter.

## Formes verbales

<!-- attendu: conditionnel -->
Le service devrait redémarrer après la mise à jour.

<!-- attendu: subjonctif -->
Vérifier que le service soit démarré.

<!-- attendu: passe_compose -->
Le déploiement a supprimé l'étape de préchauffage.

<!-- attendu: passe_compose_feminin -->
La tâche a produite un rapport.

<!-- attendu: plus_que_parfait -->
Le service avait redémarré avant la mise à jour.

<!-- attendu: imparfait -->
Les instances fonctionnaient avec un cache vide.

<!-- attendu: participe_present -->
Le service redémarre, permettant la reprise du trafic.

<!-- attendu: gerondif -->
Supprimer le fichier en utilisant la commande `rm`.

<!-- attendu: passif_avec_agent -->
Le rapport est écrit par le service.

## Groupes nominaux et modalité

<!-- attendu: verbe_support, nominalisation -->
Effectuer la vérification de la configuration avant l'installation.

<!-- attendu: nominalisation -->
La suppression des fichiers libère de l'espace disque.

<!-- attendu: il_impersonnel -->
Il est nécessaire de vérifier la configuration.

<!-- attendu: modalite_floue -->
Le service est en mesure de reprendre la tâche.

<!-- attendu: hedging -->
Le service redémarre généralement en trente secondes.

<!-- attendu: formule_creuse -->
Veuillez noter que le cache est vide.

## Discours

<!-- attendu: connecteur_lourd -->
Cependant, le service redémarre en trente secondes.

<!-- attendu: connecteur_lourd -->
Ainsi, le service reprend le trafic.

<!-- attendu: annonce_de_plan -->
Dans cette section, nous allons voir la configuration du cache.

<!-- attendu: point_virgule -->
Lancer la migration ; vérifier le journal.

<!-- attendu: tiret_long -->
Le service s'arrête — le trafic reprend après.

<!-- attendu: parenthese_necessaire -->
Le service redémarre (le cache est vidé au démarrage) en trente secondes.

<!-- attendu: anglicisme -->
La migration impactera la configuration de la base.

<!-- attendu: anglicisme -->
Le nouvel outil supporte le format CSV.

<!-- attendu: style_telegraphique -->
Vérifier existence du fichier de configuration.

## Typographie, nombres et mesure

<!-- attendu: typographie_espaces -->
Le fichier contient une erreur: la valeur est absente.

<!-- attendu: accent_majuscule -->
L'Etat de la machine reste stable.

<!-- attendu: nombre_format -->
Le fichier pèse 1,250.5 Mo.

<!-- attendu: unite_anglaise -->
Le cache occupe 20 GB sur le disque.

<!-- attendu: date_ambigue -->
Déployer la version du 08/18/26.

<!-- attendu: emoji -->
Le service redémarre 🚀 en trente secondes.

<!-- attendu: abreviation -->
Redémarrer le service, etc.

<!-- attendu: phrase_longue_instruction -->
Copier le fichier de configuration dans le dossier cible, puis vérifier chaque paramètre du service avant de redémarrer la machine de production.

<!-- attendu: phrase_longue_description -->
Le service de collecte lit chaque mesure du capteur, agrège les valeurs par minute, écrit le résultat dans la base locale et publie un résumé sur le réseau interne de supervision.

<!-- attendu: condition_finale -->
Augmenter le délai d'attente si le réseau est lent.

<!-- ensemble: registre_melange -->
Tu lances la migration.
Vous vérifiez le journal.
<!-- fin ensemble -->

<!-- attendu: mot_vide -->
Le service reste robuste et très réactif.
