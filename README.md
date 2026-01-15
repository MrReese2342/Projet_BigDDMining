# Big Data & Data Mining - BigDDMining

## Vu d'ensemble du projet
Ce projet porte sur l’extraction de connaissances à partir de données non structurées
et semi-structurées. Les données considérées sont des textes ainsi que des documents
au format XML et JSON, nécessitant une phase de prétraitement. L’objectif est d’extraire
des associations entre des concepts ou des termes biomédicaux à partir de résumés
d’articles scientifiques en anglais.

La partie Big Data consiste à constituer des collections de documents et à comparer
différents systèmes de gestion de bases de données selon des critères de performance
tels que le temps de chargement, le temps d’exécution des requêtes et le temps d’export.

La partie Data Mining vise à extraire des connaissances à partir des données traitées
lors de la phase Big Data, en utilisant des méthodes d’extraction de règles
d’association.

## Technologies
- BaseX (XML native database)
- PostgreSQL (JSONB support)
- Neo4j (graph database)
- Weka (association rule mining)
- Overleaf (report writing)

## Structure du repo
- `data/raw`: raw datasets
- `data/processed`: cleaned and transformed data
- `scripts`: preprocessing and export scripts
- `basex`, `mongodb`, `postgres`, `neo4j`: Big Data experiments
- `weka`: Data Mining experiments
- `report`: figures and tables for the report

## Auteurs
- Abderrahmane EL HATHOUT
- Mahad MOUSSA ABDILLAHI

