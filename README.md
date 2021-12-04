Bonjour la tiime Team (ou l'inverse!)

Voici ma proposition pour le test technique. Cet exercice m'a interessé, et 
m'a pris environ 10h à réaliser, comprenant quelques recherches, l'écriture du code, ainsi
que la documentation des tâches et le README ci-présent. 

# Enoncé du test et choix pris

Le test technique propose la mise en place d'un DAG pour le traitement 
de données très simple composées d'un ID, d'un montant et d'un label, puis d'effectuer
deux traitements distincts dessus, et enfin 
d'effectuer le monitoring de ces traitements. 
Il propose l'utilisation d'une librairie python permettant d'effectuer ce DAG et 
de déclarer des tâches. Après lecture de la documentation du module, je suis parti sur un 
moteur de workflow différent; à savoir Apache Airflow. Ce choix a été motivé notamment 
par la deuxième partie de l'énoncé; à savoir le monitoring, car Apache Airflow propose
un serveur web permettant justement de visualiser les traitements, les lancer, suivre les 
logs, visualiser les graphs, et modifier des paramètres a postériori. 

Concernant le moteur de stockage, je suis parti sur Postgre car vous l'utilisez en interne, 
et egalement parce qu'il est packagé avec Apache Airflow, et donc je pouvais m'en servir directement. 

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
des annotations afin de placer en erreur une transaction qui dépasserait un montant iréalliste, puis
je génére un rapport d'erreur des transactions présentant un montant trop élevé. 

Le graphe du DAG final, dans le cas d'une erreur est le suivant 

![Alt text](images/graph_avec_erreur.png?raw=true "Graph")

Afin que vous puissiez observer le résultat de la table des transactions finales, j'ai choisi de dumper la table finale des transactions
dans un fichier CSV appelé output_transactions.csv à la fin du process.
Les deux algorithmes d'annotation et de tag ne sont pas bloquant pour la génération de ce 
CSV final, et sont executés de manière parallèle. 

# Lancement de la solution

Les étapes pour lancer la solution sont les suivantes :

- Cloner le projet
- Dans repertoire du projet, lancez: 
```sh
docker-compose up airflow-init
```
attendre la fin de l'initialisation nécessaire pour Apache Airflow. La base de donnée 
est créée et initialisée.
- Puis lancez 
```sh
docker-compose up 
```
attendre la fin du lancement. 
- Rendez vous sur 
```sh
http://localhost:8080/
```
vous devriez atteindre une page d'authentification dont les identifiants/mdp sont :
 airflow / airflow

- Vous devriez arriver sur la page principale des DAG d'Apache AirFlow, comme cela : 
![Alt text](images/acceuil.png?raw=true "DAG")

- Rendez vous dans le menu Admin > Connections et créez une connexion vers PostGre 
avec les informations suivantes : 

![Alt text](images/connexion_db.png?raw=true "Graph")

Vos DAG sont maintenant opérationnels. Vous pouvez retourner sur la page d'accueil et lancer
les deux DAG l'un a la suite de l'autre ( pour des raisons de simplicité, j'utilise la même table pour les transactions, dans les 
deux DAG). Le mot de passe a mettre pour cette connexion est airflow.

# Lancement des DAG

Avant de lancer les DAG, sur l'écran d'acceuil, vous devez les activer avec le petit toggle button sur la gauche.
Vous pouvez lancer les DAG en cliquant sur la fleche. Vous pourrez voir le nombre de tâches en succès et le nombre de 
tâches en erreurs directement sur l'interface, et consulter les logs de celles ci. 

La dernière tâche, ainsi que le callback en cas d'echecs générent des fichiers dans le volume monté présent dans /data/output/ 
dans le projet cloné. 

En cliquant sur le nom des DAG, vous pourrez voir les informations liées au DAG.

# Monitoring
Grace à Airflow, vous pouvez monitorer les executions des jobs et avoir un rendu détaillé tâche par tâche, 
avec le temps d'execution pris. Comme c'est le cas sur l'image ci-dessous

![Alt text](images/details.png?raw=true "Graph")

Le graph des tâches est également accessible. 

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

J'espère que ma solution vous aura interessé. Je suis curieux de connaitre votre avis et 
vos pistes d'amélioration. C'était vraiment très interessant pour moi de faire ce projet. J'ai 
pu approfondir ma connaissance d'Airflow et l'appliquer à un problème concret bien que simplifié :).
N'hesitez pas bien sûr si vous rencontrez des problèmes de lancement ou toute autre question ! 


A bientot !

