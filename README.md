# DocumentAnalyzer

## Description
DocumentAnalyzer est une application développée en Python avec OpenCV. Elle permet :
- L'extraction d'informations clés (texte, photo, éléments graphiques) à partir de cartes.
- La classification automatique des cartes en plusieurs catégories (identité, étudiant, fidélité).
- Une extension pour le traitement des flux vidéo.

## Fonctionnalités
1. **Extraction d'informations** : Détection et reconnaissance de texte, localisation de photos.
2. **Classification** : Analyse des informations pour déterminer le type de carte.
3. **Flux vidéo** : Démonstration en temps réel via webcam.

## Prérequis
- Python 3.8 ou supérieur
- Bibliothèques :
  - `opencv-python`
  - `numpy`
  - `pytesseract` (pour la reconnaissance optique des caractères)
  
## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/DocumentAnalyzer.git
   
2. Installer les dépendances 🔧:
   ```bash
   pip install -r requirements.txt

## Utilisation
- Mode image :
Placez vos fichiers dans le dossier input_images.
💫 Lancez le script principal :
   ```bash
   python main.py

- Mode vidéo :
Connectez une webcam et lancez :
   ```bash
   python video_processing.py


## Organisation du code
main.py : Script principal pour le traitement des images.
video_processing.py : Extension pour le traitement des flux vidéo.
modules/ : Contient les modules pour chaque étape (Prétraitement, extraction, classification,...).

## Résultats attendus
🔍 Extraction réussie de texte et images.
🧠 Précision de classification adaptée aux besoins industriels.
🎥 Détection en temps réel pour une démonstration en direct.

📧 **Contactez-moi :**  
[Mon profil LinkedIn](https://www.linkedin.com/in/sondoskocila/) 

