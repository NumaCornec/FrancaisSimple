# Doctrine verbale

Le cœur du skill. C'est ici que le français diverge le plus de l'anglais. Une traduction littérale des catalogues anglais laisse passer les tics propres au français.

## Formes autorisées et formes interdites

| Autorisé | Interdit |
| --- | --- |
| Infinitif présent, par exemple `vérifier`, `lancer` | Subjonctif |
| Infinitif à valeur d'impératif, en tête d'instruction | Passé composé |
| Présent de l'indicatif | Plus-que-parfait, futur antérieur, passé simple, imparfait |
| Futur de l'indicatif | Conditionnel |
| Participe passé en position d'adjectif | Participe présent et gérondif |

La voix active reste la règle. Le passif sans agent reste toléré. Le passif avec agent explicite reste interdit.

## Pourquoi ces interdits

### Le conditionnel

Le conditionnel porte une intention implicite. Le lecteur ne sait pas si la phrase énonce une obligation, une suggestion ou une option.

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| Il conviendrait de vérifier les journaux. | Vérifier les journaux. |
| Le service devrait redémarrer. | Le service redémarre. |
| Il serait souhaitable de relancer la tâche. | Relancer la tâche. |

<!-- fin contre-exemple -->

Le conditionnel est aussi le mode du journalisme prudent. Il permet d'énoncer un fait non vérifié sans l'assumer. L'interdire force à écrire ce qui est su, et à marquer ce qui ne l'est pas.

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| Un incident aurait affecté 12 % du trafic. | 12 % des requêtes ont échoué, ou la cause n'est pas établie. |
| Le déploiement serait à l'origine des erreurs. | Le déploiement du 18 août à 14 h 00 a supprimé l'étape de préchauffage. |

<!-- fin contre-exemple -->

### Le subjonctif

Le subjonctif arrive par la subordination. Il signale une phrase trop construite.

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| Il faut que vous configuriez le service. | Configurer le service. |
| Afin que le service redémarre, vider le cache. | Vider le cache, puis redémarrer le service. |
| Vérifier que le service soit démarré. | Vérifier que le service est démarré. |

<!-- fin contre-exemple -->

### Le participe présent

Le participe présent masque l'agent et l'enchaînement. Il crée un lien de cause non explicitée. C'est le tic principal du français généré par machine. La réécriture impose de dire la relation.

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| Le service redémarre, permettant la reprise du trafic. | Le redémarrage reprend le trafic. |
| Supprimer le fichier en utilisant la commande `rm`. | Supprimer le fichier avec la commande `rm`. |
| Le cache étant vide, les instances échouent. | Le cache est vide. Les instances échouent. |

<!-- fin contre-exemple -->

### Les temps du passé

Une procédure décrit un état reproductible, pas un événement. Le passé reste légitime dans un journal de bord ou une note de version. Même dans ces documents, le présent avec une date explicite reste préférable.

### Le participe passé adjectival

Le participe passé adjectival survit. C'est la soupape qui rend la doctrine tenable.

Exemples autorisés : `la réponse mise en cache`, `les tables copiées`, `le fichier corrompu`.

Le participe passé reste interdit comme forme verbale conjuguée, c'est-à-dire derrière un auxiliaire.

## Modalité

Deux modaux, deux sens, un mot par sens dans tout le document.

| Autorisé | Sens | Interdit |
| --- | --- | --- |
| `devoir` | Obligation | Les locutions d'obligation indirecte |
| `pouvoir` | Capacité, permission explicite | Les locutions de capacité indirecte |
| `pouvoir` + négation | Interdiction | Les locutions d'interdiction atténuée |
| Impératif négatif | Interdiction | Les locutions d'évitement |

<!-- contre-exemple -->

| À supprimer | À écrire |
| --- | --- |
| Il est nécessaire de vérifier la configuration. | Vérifier la configuration. |
| Le service est susceptible de s'arrêter. | Le service s'arrête quand la mémoire est pleine. |
| Le service est en mesure de reprendre la tâche. | Le service peut reprendre la tâche. |
| Il est déconseillé de supprimer le cache. | Ne pas supprimer le cache. |
| Éviter de supprimer le cache. | Ne pas supprimer le cache. |

<!-- fin contre-exemple -->

## Limites de la doctrine

La doctrine produit un français plat, répétitif, sans hiérarchie de l'information. Ce résultat reste assumé. Le lecteur fatigué, c'est-à-dire le lecteur réel, comprend mieux un texte plat.

Deuxième limite : les temps interdits restent interdits dans le registre contrôlé. Le registre prose, celui d'une réponse de conversation, garde un français normal.

Troisième limite : le skill devient inadapté à l'écriture de marque, au blog et à la note de synthèse pour comité. Ces usages sortent du périmètre.
