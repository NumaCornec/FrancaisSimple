# Exemples avant et après

Sept paires écrites à la main, chacune étiquetée par type de document et par règle illustrée. Les blocs `Avant` montrent une faute. Les blocs `Après` respectent le catalogue.

## 1. Message d'erreur — FR-3.3, FR-3.6, FR-3.8

**Avant**

> **Erreur de connexion.** Il conviendrait de vérifier la configuration, le service n'étant pas en mesure de joindre la base. Veuillez vous assurer que le mot de passe serait correct.

**Après**

La connexion à la base échoue. Le mot de passe du fichier de configuration n'est plus valide. Renouveler le mot de passe, puis relancer la migration.

## 2. Procédure d'exploitation — FR-2.3, FR-2.4, FR-4.5

**Avant**

> Procéder à la vérification du cache. Effectuer le redémarrage du service si le cache est vide. Réaliser ensuite une analyse des journaux.

**Après**

1. Vérifier le contenu du cache.
2. Si le cache est vide, redémarrer le service.
3. Analyser les journaux du service.

## 3. Rapport d'incident — FR-3.3, FR-4.8, FR-6.3

**Avant**

> Un incident aurait affecté 12 % du trafic — il est important de noter que la cause reste inconnue. Le déploiement serait à l'origine des erreurs.

**Après**

Le 18 août 2026 à 14 h 00, 12 % des requêtes échouent pendant onze minutes. La cause n'est pas établie. La version publiée le même jour supprime l'étape de préchauffage. Cette piste reste à confirmer.

## 4. Note de version — FR-1.9, FR-3.4, FR-8.10

**Avant**

> **Version 2.4.0**
>
> Cette version **majeure** apporte un moteur **robuste** et **performant**. Nous avons également corrigé divers problèmes.

**Après**

Version 2.4.0, publiée le 18 août 2026. Le moteur accepte les fichiers de plus de 2 Go. La lecture d'un fichier vide ne bloque plus le service. La commande `sqlpipe --check` affiche la version du schéma.

## 5. Prompt système — FR-3.8, FR-1.8, FR-4.5

**Avant**

> Tu devrais répondre de manière très concise, généralement en quelques phrases. Si possible, il conviendrait d'éviter le conditionnel.

**Après**

```
Réponds en prose. La première phrase porte le résultat.
Limite chaque phrase à 20 mots.
Si la demande sort du périmètre, écris-le en une phrase.
N'emploie pas le conditionnel.
```

## 6. Préparation de traduction — FR-2.5, FR-9.3

**Avant**

> Vérifier existence du fichier. Le supprimer, puis relancer celui-ci.

**Après**

1. Vérifier que le fichier de configuration existe.
2. Supprimer le fichier de configuration.
3. Relancer le service avec le fichier livré par défaut.

## 7. Documentation d'API — FR-1.3, FR-4.10, FR-8.5

**Avant**

> Cependant, l'outil supporte un corps de requête de 10 MB et cette librairie est basée sur un parseur rapide.

**Après**

L'outil accepte un corps de requête de 10 Mo. La bibliothèque de lecture repose sur un analyseur strict. Un corps plus grand provoque une erreur `413 Payload Too Large`.
