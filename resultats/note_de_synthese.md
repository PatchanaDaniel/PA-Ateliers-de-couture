# Note de Synthèse Décisionnelle — Ateliers de Couture
**Destinataire :** Direction Générale et Direction des Opérations  
**Auteur :** Analyste Data (Étudiant en Master Data Science, Confection & Modélisme)  
**Date :** 23 Octobre 2026  
**Objet :** Audit de qualité du registre 2025, pilotage des délais de confection et analyse des retards  

---

## 1. Contexte et Problématique Managériale
Une structure opérant au Sénégal dans le domaine de la confection textile regroupe la production de huit ateliers partenaires répartis sur le territoire (Dakar, Thiès, Saint-Louis, Kaolack, Ziguinchor, Louga, Fatick, Diourbel).  
La direction a constaté d'importantes divergences dans ses indicateurs de suivi et des retards fréquents de livraison. Elle a confié à son équipe Data la mission d'assainir le registre consolidé de l'année 2025 et d'apporter une réponse chiffrée, objective et reproductible à la question stratégique suivante :  
> **Pour quels vêtements les commandes dépassent-elles le plus souvent le délai promis ?**

---

## 2. Audit de Qualité et Traçabilité du Nettoyage
L'analyse a porté sur la source prioritaire officielle `donnees/source_prioritaire.json` (1 100 enregistrements bruts). Un audit initial approfondi a révélé une forte dégradation de la qualité des données en amont :
- **Doublons stricts :** 60 doublons parfaits (120 lignes physiques concernées), supprimés et consignés dans la piste d'audit.
- **Conflits d'identifiants (`id_operation`) :** 40 paires d'enregistrements (80 lignes) présentant des délais réels divergents pour la même commande, sans horodatage permettant de trancher. En application stricte du principe de précaution, ces 80 lignes ont été isolées dans `quarantaine.csv`.
- **Anomalies calendaires :** 55 occurrences d'une date impossible (`31/02/2025`), exclues des analyses temporelles tout en conservant l'enregistrement métier.
- **Pollution des mesures :** Présence d'unités textuelles (`"18 jours"`), de valeurs négatives impossibles (`-26 jours`), de codes sentinelles techniques (`999999`) et d'erreurs textuelles (`"erreur_saisie"`).

### Bilan de conservation du périmètre
Le registre initial de **1 100 lignes** est strictement conservé selon la partition exclusive :
$$\text{Total (1 100)} = \text{Données retenues et assainies (960)} + \text{Quarantaine (80)} + \text{Doublons stricts écartés (60)}$$

Pour l'analyse de la performance, le **périmètre métier valide** (statut `Valide`, atelier reconnu dans le référentiel, catégorie conforme et mesures exploitables) regroupe **726 commandes**.

---

## 3. Résultats Empiriques Clés

### A. Les Robes et Chemises : Principaux vecteurs de retard
Le calcul du taux de dépassement ($\frac{\sum \text{delai\_reel} > \text{delai\_promis}}{\text{Total commandes valides}}$) livre un résultat sans équivoque :
1. **Robe :** **73,68 %** de dépassement (140 retards sur 190 commandes). Retard médian de **10 jours**.
2. **Chemise :** **72,32 %** de dépassement (128 retards sur 177 commandes). Retard médian de **10 jours**.
3. **Boubou :** **70,83 %** de dépassement (119 retards sur 168 commandes). Retard médian de **6 jours**.
4. **Uniforme :** **67,02 %** de dépassement (128 retards sur 191 commandes). Retard médian de **8 jours**.

*Éclairage métier :* En atelier de confection, la confection d'une robe ou d'une chemise sur-mesure requiert un travail d'entoilage minutieux, l'ajustement du col, la pose de boutonnières et souvent des essayages intermédiaires. L'uniforme, quant à lui, repose sur des gabarits industriels standardisés, limitant les aléas.

### B. Hétérogénéité des Ateliers : Dakar et Fatick sous tension
- **S01 (Dakar) :** Volume le plus important du réseau (101 commandes valides) mais taux de retard de **79,21 %** et retard médian de **12 jours**.
- **S07 (Fatick) :** Taux de retard record à **80,68 %** pour 88 commandes (retard médian de **11,5 jours**).
- **S08 (Diourbel) :** Retard médian le plus lourd du réseau (**12,5 jours**, avec un délai réel médian de 26,5 jours contre 14 jours promis).
- **S02 (Thiès) :** Atelier le plus performant en termes de ponctualité, avec un taux de retard contenu à **63,37 %**.

### C. Dynamique Temporelle (2025)
- **Mai 2025 (Période optimale) :** Retard médian ramené à **2 jours** et taux de retard à **59,62 %** (délai promis médian de 17 jours contre 19 jours réels).
- **Août et Juin 2025 (Pics de tension) :** Le taux de retard grimpe à **78,18 %** en août, avec des écarts médians atteignant 11 à 15 jours.

---

## 4. Recommandations Opérationnelles Hiérarchisées

| Rang | Recommandation | Chiffre clé d'appui | Limite / Point de vigilance |
| :---: | :--- | :--- | :--- |
| **1** | **Allonger les délais promis contractuels sur les Robes et Chemises**<br>Rehausser de +8 jours le barème promis lors de la prise de commande pour absorber la variabilité technique de ces pièces. | **73,7 %** des robes et **72,3 %** des chemises dépassent leur délai, avec un retard médian de **10 jours**. | Risque d'arbitrage défavorable du client au profit d'ateliers concurrents promettant des délais irréalistes. |
| **2** | **Conduire un audit opérationnel prioritaire sur les ateliers S01 (Dakar) et S07 (Fatick)**<br>Auditer l'ordonnancement de coupe, la disponibilité des surjeteuses et l'approvisionnement en tissus. | Taux de retard supérieur à **79 %** à Dakar et Fatick malgré des effectifs réputés stables. | Sans données de pointage horaire réelles, impossibilité de distinguer panne machine, rupture d'étoffe ou absentéisme. |
| **3** | **Déployer un masque de saisie numérique avec contrôles de validation stricts**<br>Bloquer dès l'interface la saisie de doublons, de dates impossibles (31 février) ou de champs textuels dans les mesures numériques. | **120 doublons**, **80 conflits** et **55 dates au 31 février** recensés dans le registre brut. | Nécessite un temps d'accompagnement et de formation des chefs d'atelier sur site. |

---

## 5. Limites et Données Réelles Complémentaires
Toutes les données analysées proviennent d'un univers synthétique d'exercice. Pour transposer ces conclusions dans un cadre industriel réel, trois éléments complémentaires sont indispensables :
1. **La typologie des matières textiles :** Bazin riche, wax, lin ou popeline de coton ne se travaillent pas à la même cadence et expliquent une grande part de la variabilité des délais.
2. **Le suivi des approvisionnements :** Distinguer si un retard provient d'un goulet d'étranglement à la machine à coudre ou d'une rupture de tissu/fil chez le fournisseur.
3. **Le nombre de retouches client :** Mesurer le taux de non-conformité au premier essayage pour mesurer la qualité intrinsèque de la confection.
