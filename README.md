Bonjour la tiime Team (ou l'inverse!)

Voici ma proposition pour le test technique. Cet exercice m'a interessé, et 
m'a pris environ 10h à réaliser, comprenant quelques recherches, l'écriture du code, ainsi
que la documentation des tâches et le README ci-présent. 

# Enoncé du test et choix pris

Le test technique propose la mise en place d'un DAG pour le traitement 
de données très simple composées d'un ID, d'un montant et d'un label, puis de réaliser
deux traitements distincts dessus, et enfin 
d'effectuer le monitoring de ces traitements. 
Il propose l'utilisation d'une librairie python permettant d'effectuer ce DAG et 
de déclarer des tâches. Après lecture de la documentation du module, je suis parti sur un 
moteur de workflow différent; à savoir Apache Airflow. Ce choix a été motivé notamment 
par la deuxième partie de l'énoncé; à savoir le monitoring, car Apache Airflow propose
un serveur web permettant justement de visualiser les traitements, les lancer, suivre les 
logs, visualiser les graphs, et modifier des paramètres a postériori. 

Concernant le moteur de stockage, j'ai choisi d'utiliser Postgres car vous l'utilisez en interne, 
et également parce qu'il est packagé avec Apache Airflow, et donc je pouvais m'en servir directement. 

J'ai un usage aussi très léger de la librairie Pandas, uniquement utilisée pour charger le CSV des transactions. 

Enfin, j'ai packagé ce projet dans un docker compose afin de vous simplifier le lancement.

### Technos 

- Python
- Apache Airflow
- PostgreSQL
- Docker
- Pandas

# Solution apportée

J'ai crée deux DAG

- le premier simule un traitement avec succès
- le second simule un traitement contenant des erreurs. Pour ce faire, j'ai retouché l'algo
des annotations afin de placer en erreur une transaction qui serait d'un montant trop élevé puis
je génére un rapport d'erreur de ces transactions en erreur. 

Le graphe du DAG final, dans le cas d'une erreur est le suivant : 

![Alt text](images/graph_avec_erreur.png?raw=true "Graph")

Afin que vous puissiez observer le résultat de la table des transactions finales, j'ai choisi de dumper la table finale des transactions
dans un fichier CSV appelé output_transactions.csv à la fin du process.
Les deux algorithmes d'annotation et de tag ne sont pas bloquant pour la génération de ce 
CSV final, et sont exécutés de manière parallèle. 

# Lancement de la solution

Les étapes pour lancer la solution sont les suivantes :

- Cloner le projet
- Dans repertoire du projet, lancer: 
```sh
docker-compose up airflow-init
```
attendre la fin de l'initialisation nécessaire pour Apache Airflow. La base de donnée 
est créée et initialisée.
- Puis lancer 
```sh
docker-compose up 
```
attendre la fin du lancement. 
- Se rendre sur 
```sh
http://localhost:8080/
```
Vous devriez atteindre une page d'authentification dont les identifiants/mdp sont :
 airflow / airflow

- Vous devriez arriver sur la page principale des DAG d'Apache AirFlow, comme cela : 
![Alt text](images/acceuil.png?raw=true "DAG")

- Se rendre dans le menu Admin > Connections et créer une connexion vers PostGre 
avec les informations suivantes : 

![Alt text](images/connexion_db.png?raw=true "Graph")

Vos DAG sont maintenant opérationnels. Vous pouvez retourner sur la page d'accueil et lancer
les deux DAG l'un à la suite de l'autre ( pour des raisons de simplicité, j'utilise la même table pour les transactions, dans les 
deux DAG). Le mot de passe à mettre pour cette connexion est "airflow".

# Lancement des DAG

Avant de lancer les DAG, sur l'écran d'acceuil, vous devez les activer avec le petit toggle button sur la gauche.
Vous pouvez lancer les DAG en cliquant sur la fleche. Vous pourrez voir le nombre de tâches en succès et le nombre de 
tâches en erreur directement sur l'interface et consulter les logs de celles-ci. 

La dernière tâche, ainsi que le callback en cas d'échecs générent des fichiers dans le volume monté présent dans /data/output/ 
dans le projet cloné. 

En cliquant sur le nom des DAG, vous pourrez voir les informations liées au DAG.

# Monitoring
Grâce à Airflow, vous pouvez monitorer les executions des jobs et avoir un rendu détaillé tâche par tâche, 
avec le temps d'execution pris, comme c'est le cas sur l'image ci-dessous

![Alt text](images/details.png?raw=true "Graph")

Le graph des tâches est également accessible.

# Modifications nécessaires pour une mise en production

Pour une MEP, plusieurs changements sont à réaliser. 
- Avoir un fichier de transactions quotidien, ou bi-hebdomadaire, reçu par la banque
et mettre en place le mécanisme de schedule d'Airflow
- Mettre en place des retry sur les tâches notamment pour les écritures dans la base, les
appels serveurs et tout autre tâche dont le succès dépend d'un élément extérieur.
- Mettre éventuellement en place un broker pour notifier les changements à réaliser en base
et déléguer la responsabilité du delivery à ce broker. Celui-ci permettrait également
de notifier plusieurs élements d'architecture des résultats des algos. Je pense notamment
à la base de données du backend chez vous.
- N'appliquer les traitements que sur les nouvelles transactions; en utilisant un champ de date
que j'imagine présent quelque part en réalité.

# Pistes d'amélioration

J'ai noté plusieurs pistes d'amélioration à apporter à ce DAG pour le rendre plus résilient et efficace.

- Découper les tâches liées à l'algorithme en plusieurs sous-tâches contenant un nombre limité de données. Cela permet
de bénéficier de la parallélisation d'AirFlow sur un cluster de machines notamment. 
- Mutualiser le code lié à la lecture / ecriture dans PostGre. Je ne l'ai pas fait ici, car j'utilise un hook directement 
sur la base de données, me permettant d'économiser le code d'ouverture de la connexion. 
- Avoir une gestion plus fine des erreurs; lister les problèmes possibles. 
- Utiliser le système de retry d'AirFlow dans le cas ou une tâche est en echec. 
- Avoir de l'alterting mail ou sur un autre backend. 
- Ajouter une documentation précise des tâches grâce au mécanisme de doc_task d'Airflow

# Conclusion

Cette solution permet de répondre à la problématique du test technique concernant le traitement des données
et le monitoring. Je suis curieux de connaître votre avis et 
vos pistes d'amélioration. J'ai 
pu approfondir ma connaissance d'Airflow grâce à ce travail et l'appliquer à un problème concret bien que simplifié :).
Je reste à l'écoute si vous avez la moindre question. 


A bientot !

