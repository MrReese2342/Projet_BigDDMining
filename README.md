# Projet BigDDMining (Big Data & Data Mining) – Extraction de connaissances biomédicales

Lien vers la répo Github: https://github.com/MrReese2342/Projet_BigDDMining

## Présentation générale

Ce projet a été réalisé dans le cadre du module **Big Data & Data Mining** du  
**Master 2 Génie Informatique Logiciel (M2 GIL)** – Université de Rouen Normandie (2025–2026).

L’objectif est de mettre en œuvre une **chaîne complète de traitement de données biomédicales** :
- intégration de données massives et hétérogènes (XML, JSON, graphe),
- fouille de données et de textes,
- extraction et analyse de **règles d’association**,
- visualisation des connaissances sous forme de graphes.

Les données exploitées proviennent principalement du corpus **LitCovid** et des annotations **PubTator Central**.

---

## Équipe

- **Abderrahmane El Hathout**
- **Mahad Moussa Abdillahi**

Encadrante : *Lina F. Soualmia*

---

## Données utilisées

- **LitCovid**  
  Corpus d’articles scientifiques liés à la COVID-19 (format BioC XML / JSON)
- **PubTator Central**  
  Annotations biomédicales automatiques (MeSH, maladies, gènes, etc.)
- **PubMed**  
  Descripteurs MeSH (MH) utilisés comme référence (gold standard)

Afin de respecter les contraintes techniques, le corpus a été **réduit à ~1000 articles** tout en conservant sa représentativité.

---

## Partie Big Data

### Bases de données utilisées
- **BaseX** : base XML native et base JSON native
- **PostgreSQL** : base relationnelle-objet (JSONB)
- **Neo4j** : base orientée graphe

### Fonctionnalités principales
- Import de données XML BioC
- Import et nettoyage de données JSON volumineuses
- Extraction :
  - PMID + titre + résumé
  - références bibliographiques
- Comparaison qualitative des SGBD (facilité, performances, requêtage)

---

## Partie Data Mining & Text Mining

### Préparation du corpus
- Nettoyage et normalisation des données
- Construction de jeux de données transactionnels
- Export vers des formats compatibles **Weka (ARFF)**

### Fouille de données
- Extraction de règles d’association entre :
  - concepts **MeSH (PubTator)**
  - descripteurs **MH (PubMed)**
- Algorithmes utilisés :
  - **Apriori** (limité par la mémoire)
  - **FP-Growth** (retenu)

### Fouille de textes
- Étiquetage morpho-syntaxique avec **TreeTagger**
- Extraction de termes candidats avec **YaTeA**
- Évaluation par rapport aux descripteurs MeSH
- Extraction de règles d’association entre termes

### Fouille mixte
- Combinaison :
  - MH (PubMed)
  - MeSH (PubTator)
  - Termes YaTeA
- Extraction de règles d’association multi-sources

---

## Représentation en graphe

- Construction de graphes de connaissances dans **Neo4j**
- Nœuds :
  - Articles
  - Concepts MeSH / MH
  - Termes candidats
- Arêtes :
  - Relations issues des règles d’association
- Filtrage basé sur des mesures statistiques (lift, confiance)

---

## Technologies & Outils

- **Python** (scripts de nettoyage, extraction, transformation)
- **BaseX**
- **PostgreSQL (JSONB)**
- **Neo4j**
- **Weka**
- **TreeTagger**
- **YaTeA**

---


