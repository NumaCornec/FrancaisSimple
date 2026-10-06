# Mots et locutions à remplacer

Fichier ouvert, pas liste d'autorisation. Chaque entrée indique la règle qui la porte. Toute alerte reste citable. Les suffixes de nom d'action les plus fréquents servent de déclencheur : `-tion`, `-sion`, `-ment`, `-age`, `-ure`, `-ance`, `-ence`.

## Anglicismes (FR-1.3)

Deux cas demandent un arbitrage humain. `supporter` est un anglicisme au sens de prendre en charge, et du français correct au sens de tolérer. `librairie` est correct au sens de commerce de livres, et fautif au sens de bibliothèque logicielle. Le linter alerte et laisse l'arbitrage au rédacteur.

<!-- contre-exemple -->

| Anglicisme | À écrire |
| --- | --- |
| supporter un format | prendre en charge, accepter |
| librairie logicielle | bibliothèque |
| digital | numérique |
| initier une action | lancer, engager, démarrer |
| impacter | avoir un effet sur, modifier |
| adresser un problème | traiter, résoudre |
| délivrer une fonctionnalité | livrer, fournir |
| opportunité au sens d'ouverture | occasion, possibilité |
| challenger une décision | contester, remettre en question |
| sur base de | d'après, à partir de |
| au niveau de, au sens de concernant | pour, dans, concernant |
| basé sur | fondé sur, repose sur |
| faire sens | avoir un sens |
| à date | à ce jour |

<!-- fin contre-exemple -->

## Nominalisations et verbes supports (FR-2.3, FR-2.4)

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| procéder à la vérification de la configuration | vérifier la configuration |
| effectuer le lancement du service | lancer le service |
| réaliser une analyse du journal | analyser le journal |
| mettre en œuvre la suppression des fichiers | supprimer les fichiers |
| opérer une modification du paramètre | modifier le paramètre |
| permettre la récupération des données | récupérer les données |
| la prise en compte des paramètres | les paramètres sont pris en compte |
| dans le cadre de la mise à jour | quand on met à jour |
| à des fins de vérification | pour vérifier |
| en vue de l'obtention d'un accès | pour obtenir un accès |
| suite à la modification | après la modification |

<!-- fin contre-exemple -->

## Adverbes vides et valorisation (FR-1.8, FR-1.9, FR-1.10)

```
très · vraiment · particulièrement · extrêmement · totalement · absolument · parfaitement
robuste · performant · optimal · puissant · moderne · avancé · fluide · élégant
crucial · essentiel · important · primordial · majeur · fondamental · clé · incontournable
```

Un adverbe d'intensité remplace un fait mesuré. Un mot de valorisation remplace une qualité démontrée. Un mot d'importance remplace un argument.

## Formules creuses (FR-6.3, FR-6.5, FR-6.6)

```
il est important de noter que · il convient de souligner que · on notera que
rappelons que · force est de constater que · à noter que
il faut garder à l'esprit que · nous allons voir que · dans cette section, nous
ce document présente · pour conclure · en résumé · en définitive
veuillez noter que · n'hésitez pas à · nous vous prions de · nous espérons que · bonne lecture
```

## Modalité floue (FR-3.8, FR-1.8)

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| il est nécessaire de X | X, à l'impératif |
| il est recommandé de X | X, ou dire qui recommande et pourquoi |
| X pourrait être Y | dire ce qui est |
| X devrait être Y | X est Y, ou X doit Y si l'obligation est réelle |
| être susceptible de | pouvoir, ou décrire la condition |
| être à même de, être en mesure de, avoir la possibilité de | pouvoir |
| éventuellement | dire sous quelle condition |
| dans la mesure du possible | dire la limite réelle |
| le cas échéant | dire le cas |
| en principe | dire le principe |
| généralement | dire la fréquence, ou supprimer |

<!-- fin contre-exemple -->

## Participe présent et gérondif (FR-3.6)

Faux positifs à ne pas signaler : `en provenance`, `en attente`, `en cours`, `en fonction`, `en amont`, `en aval`, `en revanche`. Ces locutions ne sont pas des gérondifs. Le motif du linter exige le suffixe `-ant` directement après `en `.

## Temps composés (FR-3.4)

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| Le déploiement a supprimé l'étape de préchauffage. | Le déploiement supprime l'étape de préchauffage. |
| Les instances ont redémarré avec un cache vide. | Les instances redémarrent avec un cache vide. |
| Le service était indisponible. | Le service est indisponible de 14 h 02 à 14 h 31. |

<!-- fin contre-exemple -->

## Style télégraphique (FR-9.3)

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| Vérifier existence du fichier de configuration. | Vérifier que le fichier de configuration existe. |
| Redémarrer service après modification. | Redémarrer le service après la modification. |
| Config invalide, relancer setup. | La configuration est incorrecte. Relancer l'installation. |

<!-- fin contre-exemple -->

Le style télégraphique ne produit pas du français contrôlé. Il produit du français abîmé.

## Pléonasmes (FR-9.2)

```
voire même · au jour d'aujourd'hui · prévoir à l'avance · collaborer ensemble
réunir ensemble · monter en haut · descendre en bas · petit détail
solution alternative · option facultative · s'avérer vrai · être en mesure de pouvoir
```

## Typographie et nombres (FR-8)

<!-- contre-exemple -->

| Défaut | Correction |
| --- | --- |
| Etat, Ecole, Universite | État, École, Université |
| "texte" | guillemets français |
| mot: mot | mot, deux-points et espace avant |
| 1,250.5 | 1 250,5 |
| 20 GB, 500 MB | 20 Go, 500 Mo |
| 08/18/26, 2:02 PM | 18 août 2026, 14 h 02 |
| etc. en fin d'instruction | la liste est finie, ou supprimée |
| env., p. ex., cf. | environ, par exemple, voir |

<!-- fin contre-exemple -->

## Ce qui reste intact

Blocs de code et code en ligne. Identifiants et noms de fonctions. Commandes et drapeaux. Chemins de fichiers et adresses URL. Messages d'erreur et lignes de journal entre guillemets. Noms de produits, clés de configuration et libellés d'interface. Nombres avec leur unité.

La règle vaut aussi pour l'orthographe. Un identifiant qui contient `Etat` sans accent, une erreur en anglais et un libellé de bouton en anglais ne se corrigent pas. Le document les cite tels qu'ils sont.

## Exemple complet

**Avant**, sortie de modèle non éditée.

<!-- contre-exemple -->

**Délais de connexion.** Si sqlpipe se bloque ou échoue avec `dial tcp: i/o timeout`, vous devriez vérifier que l'hôte qui exécute sqlpipe peut effectivement joindre le port Postgres (généralement 5432) — il s'agit souvent d'un groupe de sécurité ou d'une règle de pare-feu bloquant la connexion. Dans le cas où vous vous connectez à une base managée (RDS, Cloud SQL, etc.), il conviendrait de confirmer que l'instance autorise les connexions depuis l'IP de sqlpipe.

<!-- fin contre-exemple -->

**Après**, classé procédural, conditions en tête, une action par étape, résultat attendu donné.

**Délais de connexion.** sqlpipe s'arrête avec `dial tcp: i/o timeout` quand il ne peut pas joindre le port Postgres, 5432 par défaut.

1. Vérifier que l'hôte qui exécute sqlpipe peut joindre le port Postgres. Un pare-feu ou un groupe de sécurité bloque souvent la connexion.
2. Si la base est managée, vérifier que l'instance accepte les connexions depuis l'adresse IP de sqlpipe.
3. Si le réseau est lent, augmenter `source.connect_timeout_seconds` dans la configuration.

Le délai par défaut est de trente secondes.

Ce qui change : la phrase de quarante mots passe sous la limite de vingt. Le conditionnel devient une instruction à l'infinitif. Chaque condition passe avant sa commande. Le tiret cadratin disparaît. Le code et le message d'erreur restent intacts.
