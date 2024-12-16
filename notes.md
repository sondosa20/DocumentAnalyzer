## Module 1 : Prétraitement des images 
**Fonctionnalités principales** :
- Convertir les images en niveaux de gris. (pour l'optimisation des algorithmes)
- Réduire le bruit avec des filtres (Gaussian blur, Median blur).
- Effectuer une binarisation (Otsu's threshold).
- Sauvegardez les résultats prétraités dans le dossier output/

---

## Module 2 : Extraction d’informations
**Fonctionnalités principales** :
- Texte : Utilisez pytesseract pour extraire du texte des cartes.
- Images : Identifiez et segmentez les zones contenant des photos ou des graphiques.

---

## Module 3 : Classification
**Description** : Ce module construit, entraîne et évalue les modèles de machine learning.  
**Fonctionnalités principales** :
- Analysez les caractéristiques extraites (texte, taille des photos,..)
- Utilisez scikit-learn pour entraîner un modèle simple (par exemple, une régression logistique ou SVM).

---

## Extension au flux vidéo 
**Fonctionnalités principales** :
- Capturez des images depuis la webcam avec OpenCV.
- Appliquez les modules de prétraitement, d'extraction, et de classification sur chaque image.

---

## 5. Module d'Automatisation
**Description** : Ce module automatise l'exécution des pipelines de données et leur déploiement.  
**Fonctionnalités principales** :
- Orchestration avec des outils comme Airflow ou Luigi.
- Automatisation des pipelines pour des exécutions récurrentes.

---

## Instructions pour Contribuer
Pour modifier ou ajouter des fonctionnalités à un module :
1. Identifiez le module concerné.
2. Ajoutez la description de la nouvelle fonctionnalité dans la section **Fonctionnalités principales**.
3. Testez les modifications avant de les intégrer au projet principal.