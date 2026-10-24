# Dictionnaire — Projet 06

Toutes les données sont synthétiques. Une ligne représente une commande de confection.

| Champ | Type cible | Définition et convention |
| --- | --- | --- |
| id_operation | texte | Clé unique attendue P06-NNNNN ; conserver les zéros |
| date_operation | date | Date de l’opération en 2025 ; formats source ISO ou jour/mois/année |
| id_site | texte | Clé étrangère vers referentiel_sites.csv ; codes S01 à S08 |
| categorie | texte | Valeurs attendues : Boubou, Chemise, Robe, Uniforme |
| delai_promis_jours | numérique | Mesure métier ; unité indiquée par le suffixe du champ |
| delai_reel_jours | numérique | Mesure métier ; unité indiquée par le suffixe du champ |
| statut | texte | Valide, A_verifier ou Rejete après normalisation ; seul Valide entre dans les indicateurs métier |
| commentaire | texte | Note libre ; ne constitue pas une preuve de correction |

## Règles métier

Les mesures delai_promis_jours et delai_reel_jours doivent être numériques et non négatives. Un délai réel supérieur au délai prévu est un résultat métier possible, pas une erreur.

Unités : kg = kilogrammes ; km = kilomètres ; fcfa = francs CFA XOF ; c = degrés Celsius ; min = minutes ; m2 = mètres carrés ; m3 = mètres cubes ; l = litres ; kw = kilowatts ; g = grammes ; heures et jours sont des durées. Les autres mesures sont des comptages, sauf heures/minutes disponibles, occupées ou utilisées qui sont des durées cumulées. La capacité d'équipe est un effectif informatif, constant par site. Ne l'utilisez pas comme population exposée ou comme durée d'ouverture.

Le référentiel contient id_site, nom_site, ville et capacite_equipe. Il est propre et fait autorité pour les codes de sites. Les huit sites sont fictifs. Les absences peuvent apparaître sous plusieurs marqueurs textuels. Les valeurs absentes ne représentent pas zéro.

En cas de conflit pour un même id_operation, aucune date de mise à jour ne permet d'arbitrer. Une mise en quarantaine est attendue. Les conversions réversibles et les normalisations documentées sont autorisées. Une mesure métier ne doit pas être reconstruite à partir d'une simple intuition.
