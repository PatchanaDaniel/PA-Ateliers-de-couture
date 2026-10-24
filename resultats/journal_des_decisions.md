# Journal des Décisions Méthodologiques — Projet 06
**Projet :** Ateliers de Couture — Consolidation et Analyse des Retards de Confection (2025)

## 1. Principes Directeurs
- **Intégrité de la source originale :** Le fichier `donnees/source_prioritaire.json` n'est jamais modifié.
- **Traçabilité totale :** Chaque modification unitaire est consignée dans `journal_nettoyage.csv` (ligne d'origine, colonne, valeur initiale, action, motif, valeur finale).
- **Refus de l'arbitraire :** Aucune donnée n'est reconstruite sur la base d'une simple intuition. Les clés contradictoires sans arbitrage temporel sont isolées en quarantaine.

## 2. Décisions de Nettoyage et d'Arbitrage

| Objet | Constat initial | Décision prise | Justification méthodologique |
| :--- | :--- | :--- | :--- |
| **Doublons stricts** | 60 copies parfaites (120 lignes physiques) | Suppression de la copie (60 lignes conservées, 60 retirées) | Redondance technique pure sans valeur informationnelle. |
| **Conflits de clé `id_operation`** | 40 paires (80 lignes) avec des délais et commentaires divergents | Mise en quarantaine intégrale des 80 lignes dans `quarantaine.csv` | Absence de colonne de mise à jour ou de log permettant de départager la bonne saisie. |
| **Dates invalides** | 55 occurrences de `31/02/2025` | Remplacement par `NaT` (absence) pour l'analyse temporelle | Date inexistante au calendrier grégorien ; la ligne reste conservée pour les agrégations globales non temporelles. |
| **Codes Sites** | Variations d'espaces et casse (`'s05'`, `' S03 '`), 9 occurrences de `'S99'` et 12 vides | Normalisation majuscules/strip. Conservation des sites inconnus sans imputation. | Respect strict du référentiel `referentiel_sites.csv` (S01 à S08). Pas d'attribution fictive d'un atelier. |
| **Catégories** | Casse hétérogène (`' robe'`) et 54 occurrences de `'AUTRE_NON_DOCUMENTE'` | Harmonisation de la casse (`Robe`, `Chemise`, `Boubou`, `Uniforme`). Maintien de `'AUTRE_NON_DOCUMENTE'` sans conversion vers le mode. | Éviter le biais statistique d'enrichir artificiellement la catégorie la plus fréquente. |
| **Délai promis** | Suffixe textuel (`"18 jours"`) et 52 valeurs négatives (`-26`) | Extraction numérique du nombre de jours. Rejet des valeurs négatives (`np.nan`). | Une promesse de livraison passée ou future ne peut être négative. L'unité est garantie par le champ. |
| **Délai réel** | Textes `"erreur_saisie"`, valeurs sentinelles `999999` et valeurs extrêmes `16000-37000` | Rejet des sentinelles et erreurs (`np.nan`). Maintien des valeurs extrêmes dans la base nettoyée, mais analyse basée sur la **médiane**. | La médiane est robuste aux valeurs aberrantes ; une division par 1000 sans documentation explicite violerait le principe d'objectivité. |
| **Statut** | Casse hétérogène (`" valide "`, `"VALIDE"`) et marqueur `"INCONNU"` | Normalisation (`Valide`, `A_verifier`, `Rejete`, `Inconnu`). | Seul le statut `Valide` entre dans les indicateurs métier, conformément au dictionnaire. |

## 3. Règle de Partitionnement Exclusif
L'exhaustivité de la source est garantie par l'équation stricte :
$$\text{Lignes initiales (1 100)} = \text{operations\_nettoyees.csv (960)} + \text{quarantaine.csv (80)} + \text{doublons stricts retirés (60)}$$
