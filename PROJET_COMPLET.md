# Projet 06 — Ateliers de couture

## 1. Situation et mission

Une structure entièrement fictive implantée dans plusieurs villes du Sénégal vous confie son registre de ateliers de couture. Les équipes ont consolidé des saisies manuelles et des exports provenant de plusieurs postes. La direction constate que les totaux ne concordent pas et ne sait pas encore quels indicateurs utiliser. Elle vous recrute comme analyste pour transformer ces exports en résultats vérifiables. Une ligne représente une commande de confection. Plusieurs opérations peuvent avoir lieu le même jour dans un même site. Les villes servent uniquement de contexte : ces données ne mesurent aucune situation réelle au Sénégal.

Votre réponse finale doit traiter cette question centrale : **Pour quels vêtements les commandes dépassent-elles le plus souvent le délai promis ?**

## 2. Objectifs observables

À l'issue du projet, vous devrez être capable de :

- importer une source JSON sans perdre silencieusement des enregistrements ;
- construire un audit chiffré de qualité et justifier chaque règle de nettoyage ;
- expliquer et calculer les indicateurs adaptés à une commande de confection, en particulier **delai_reel_jours − delai_promis_jours** ;
- produire une comparaison temporelle et une comparaison entre sites sans confondre volumes et performances ;
- publier un tableau de bord Dash filtrable et conserver une piste d'audit reproductible.

## 3. Ressources et périmètre

Ouvrez `DICTIONNAIRE_DONNEES.md` avant de coder. `donnees/operations_sales.csv` contient **1 100 lignes physiques** et 8 colonnes. `donnees/referentiel_sites.csv` contient les 8 sites autorisés. Le registre concerne l'année 2025. Les identifiants sont fictifs. Aucune donnée personnelle réelle n'est utilisée.

Source à traiter en priorité : **JSON**. Utilisez le fichier source_prioritaire correspondant dans donnees/. Le CSV contient les mêmes enregistrements et sert de secours ou de contrôle, pas de lot supplémentaire à concaténer.

Les données sont volontairement très sales. Les anomalies concernent notamment les absences, les formats, les clés, les domaines et les doublons. Certaines valeurs surprenantes peuvent être valides. Le dictionnaire décrit les conventions attendues, sans donner la position des erreurs.

## 4. Déroulement et questions obligatoires

### Phase A — Comprendre et acquérir

1. Reformulez le besoin de la direction en cinq lignes. Distinguez une décision, un indicateur et une donnée nécessaire à son calcul.
2. Décrivez l'unité d'observation, la clé attendue et la relation entre opérations et sites. Pourquoi une date et un site ne constituent-ils pas une clé unique ?
3. Chargez la source prioritaire. Affichez son chemin relatif, le nombre de lignes, les colonnes et cinq observations. Pour JSON, extrayez la liste `operations`. Pour HTML, utilisez BeautifulSoup et la table `operations`. Pour SQLite, ouvrez la table `operations` avec sqlite3. Aucun accès Internet n'est nécessaire.
4. Rédigez une fonction Python qui contrôle la présence des colonnes attendues. Que doit-elle signaler si une colonne manque ?

### Phase B — Auditer avant de corriger

5. Pour chaque colonne, indiquez le type lu, le type attendu, le nombre de valeurs absentes après reconnaissance des marqueurs et le nombre de valeurs distinctes.
6. Détectez séparément les lignes strictement identiques et les identifiants répétés avec contenus différents. Combien de lignes et de clés sont concernées ?
7. Recensez les formats de date, les dates impossibles, les chaînes placées dans des mesures et les catégories non documentées. Donnez deux exemples par famille présente.
8. Contrôlez les bornes et les règles métier du dictionnaire. Distinguez erreur certaine, valeur plausible atypique et cas indécidable.
9. Contrôlez les clés de sites avec une jointure gauche. Combien de références restent inconnues avant et après normalisation ? Vérifiez que la jointure n'augmente pas le nombre de lignes.
10. Produisez un tableau de qualité initial. Le taux d'anomalies par règle doit préciser son dénominateur. Les taux peuvent se chevaucher : ne les additionnez pas comme des groupes disjoints.

### Phase C — Nettoyer en conservant les preuves

11. Conservez la source intacte et ajoutez un numéro de ligne source. Écrivez un journal comportant ligne, colonne, valeur initiale, action, justification et valeur obtenue.
12. Normalisez espaces, casse, catégories et marqueurs d'absence avec des fonctions réutilisables. Comment empêchez-vous qu'une catégorie inconnue soit transformée arbitrairement en catégorie fréquente ?
13. Convertissez les deux mesures en respectant les unités. Signalez les échecs de conversion. Convertissez les dates selon leurs formats explicites et excluez les dates impossibles de l'analyse temporelle en les comptabilisant.
14. Proposez un traitement par colonne des absences. Comparez suppression ciblée, conservation et imputation. Justifiez les colonnes que vous refusez d'imputer.
15. Supprimez les copies exactes en conservant leur trace. Pour une clé avec valeurs contradictoires, mettez les lignes en quarantaine faute de source faisant autorité. Ne choisissez pas automatiquement la première ou la dernière ligne.
16. Appliquez les règles métier. Une valeur extrême ne se supprime pas uniquement parce qu'elle apparaît hors des moustaches d'un boxplot. Expliquez votre décision pour cinq cas.
17. Produisez `operations_nettoyees.csv`, `quarantaine.csv` et `journal_nettoyage.csv`. Documentez une règle d'appartenance exclusive entre données retenues, doublons retirés et quarantaine. Vérifiez la conservation du nombre initial de lignes.
18. Relancez le contrôle qualité et comparez les taux avant et après. Quels problèmes restent indécidables ?

### Phase D — Répondre au besoin métier

19. Après nettoyage, quelle est la réponse chiffrée à la question suivante : Pour quels vêtements les commandes dépassent-elles le plus souvent le délai promis ? Présentez le calcul, son périmètre et son dénominateur.

20. Quels sites combinent fort volume et retard médian élevé ? Présentez un tableau comparatif et expliquez les limites de la comparaison.

21. Comment les médianes de delai_promis_jours et de delai_reel_jours évoluent-elles par mois et par catégorie ? Ajoutez les sommes uniquement pour les mesures additives, en justifiant ce choix. Identifiez deux mois contrastés sans inventer leur cause.

22. Quels sont les trois sites les plus atypiques pour delai_promis_jours et delai_reel_jours ? Comparez moyenne, médiane et intervalle interquartile avant de proposer une explication prudente.

23. Que devient votre indicateur principal si vous excluez toutes les valeurs manquantes, puis si vous appliquez une imputation justifiée sur les seules mesures autorisées ? Quantifiez la différence. Ne remplacez pas un identifiant, une date ou un statut par une valeur inventée.

24. Quelle décision opérationnelle proposeriez-vous à partir de ces résultats de simulation ? Formulez trois recommandations hiérarchisées, chacune appuyée par un chiffre et accompagnée d’une limite.

### Phase E — Visualiser et communiquer

25. Construisez au moins cinq graphiques : comparaison par catégorie, évolution mensuelle, histogramme, boxplot par site et nuage de points reliant `delai_promis_jours` à `delai_reel_jours`. Pour chacun, indiquez titre, unité, effectif utilisé et une interprétation de trois phrases. N'interprétez pas une association comme une causalité.
26. Réalisez une application Dash avec filtres de dates, site et catégorie. Affichez nombre d'opérations, indicateur principal et au moins deux graphiques qui réagissent aux filtres. Prévoyez un message pour un filtre sans données et évitez les divisions par zéro.
27. Stockez les données nettoyées dans une nouvelle base `resultats/analyse.sqlite`. Écrivez trois requêtes SQL : résumé par catégorie, évolution mensuelle et classement des sites. Comparez les résultats à ceux de Pandas avec une tolérance explicite sur les décimaux.
28. Rédigez une note de deux pages : problème, qualité des données, résultats, recommandations et limites. Expliquez quelles conclusions resteraient impossibles sans données réelles supplémentaires.

## 5. Définitions et règles de calcul

Les mesures delai_promis_jours et delai_reel_jours doivent être numériques et non négatives. Un délai réel supérieur au délai prévu est un résultat métier possible, pas une erreur.

Indicateur principal à expliquer : **delai_reel_jours − delai_promis_jours**. Les sommes et ratios portent sur les opérations dont le statut normalisé est `Valide`, dont les mesures requises sont utilisables et dont la clé a été résolue. Les autres observations restent dans la piste d'audit. Les agrégations temporelles exigent aussi une date exploitable. Annoncez l'effectif utilisé pour chaque résultat.

Pour un ratio agrégé, utilisez le rapport des sommes si la question demande un taux pondéré. Comparez-le à la moyenne des ratios individuels sans les confondre. Un dénominateur nul donne un résultat indéfini, jamais zéro par défaut. Les nombres non entiers sont autorisés pour les masses, durées et volumes. Les champs de comptage (`quantite`, `plants`, `visiteurs`, `participants`, `places`, `kits`, `dossiers`, `billets`, `entrees`, `bouteilles`, `articles`) doivent être entiers : une fraction non nulle y est une anomalie à résoudre ou mettre en quarantaine.

## 6. Livrables attendus

- notebook `analyse.ipynb` commenté, avec réponses numérotées aux 28 questions ;
- dossier `resultats/` : données nettoyées, quarantaine, journal, tableau qualité avant/après, trois exports d'analyse et base SQLite ;
- cinq graphiques exportés et application `app.py` avec consignes d'exécution ;
- note de synthèse, liste des dépendances et journal des décisions.

## 7. Organisation et évaluation

Travail en binôme, charge indicative de 18 à 24 heures : cadrage et acquisition 2 h, audit 3 h, nettoyage 5 h, analyse 4 h, visualisation et Dash 5 h, restitution et contrôles 3 h. Ajustez selon votre maîtrise.

Barème sur 100 : compréhension et acquisition 10 ; audit chiffré 20 ; nettoyage traçable et justifié 25 ; analyses métier 20 ; graphiques et Dash 15 ; reproductibilité et note 10. Une suppression massive non justifiée ou un classement sans dénominateur dégrade la qualité de l'analyse même si le code s'exécute.

## 8. Vérifications finales

Le notebook doit s'exécuter de haut en bas après redémarrage du noyau. Les sources brutes doivent rester inchangées. Les clés du résultat doivent être uniques. Les sites retenus doivent appartenir au référentiel. Les lignes en quarantaine doivent avoir une raison. Les figures et indicateurs doivent partager le même périmètre. Aucune conclusion ne doit présenter les données synthétiques comme une observation réelle.
