import streamlit as st
import cv2
import pytesseract
from pytesseract import Output
from PIL import Image
import numpy as np

# Configuration de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\pc\Desktop\M1\Approches experimentales\Tesseract-OCR\tesseract.exe"

# Chargement du classificateur pour la détection de visages
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# --- 1. Fonction de détection de visages et textes ---
def detect_faces_and_texts(img):
    """
    Détecte les visages et les textes dans une image, dessine des boîtes et retourne les données.
    """
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Détecter les visages
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    # Dessiner les rectangles autour des visages
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Détecter le texte avec Tesseract
    data = pytesseract.image_to_data(img, output_type=Output.DICT, lang="eng+fra")
    for i in range(len(data["text"])):
        if int(data["conf"][i]) > 50:  # Seuil de confiance
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            # Dessiner un rectangle autour de l zone detectée
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img, data

# --- 2. Fonction d'extraction de texte ---
def extract_text(image):
    """
    Extrait le texte d'une image en utilisant Tesseract OCR après prétraitement.
    """
    # Conversion en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarisation par la méthode d'Otsu: seuillage automatique
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Ajustement du contraste --> Contraste: alpha et Luminosité: beta
    contrast_img = cv2.convertScaleAbs(thresh, alpha=1.5, beta=10)

    # Extraction du texte avec Tesseract
    custom_config = r'--oem 3 --psm 6 -l eng+fra'
    text = pytesseract.image_to_string(contrast_img, config=custom_config)
    
    return text.strip()

# --- 3. Fonction de classification ---
def classify_card(text):
    """
    Classifie le type de carte en fonction du texte extrait.
    """
    keywords = {
        "Carte d'identité": ["nationale", "nom", "prénom", "identité", "n°", "<<<<<<<<<"],
        "Carte étudiant": ["étudiant", "université", "ine", "école", "matricule"],
        "Carte de fidélité": ["fidélité", "points", "client", "gratuit"]
    }

    # Supprimer les espaces et convertir en minuscules
    text_cleaned = text.replace(" ", "").lower()

    # Compter les occurrences des mots-clés
    scores = {key: sum(word.lower() in text_cleaned for word in words) for key, words in keywords.items()}

    if max(scores.values()) == 0:
        return "Type inconnu"

    return max(scores, key=scores.get)

# --- 4. Interface Streamlit ---
def main():
    st.title("Détection et Classification des Cartes")
    st.write("Choisissez une image pour détecter les visages, extraire le texte et classer le type de carte.")

    # Chargement de l'image
    uploaded_file = st.file_uploader("Téléchargez une image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Chargement de l'image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Afficher l'image originale
        st.subheader("Image Originale")
        st.image(image, channels="BGR", use_container_width=True)

        # Appliquer la détection
        processed_image, data = detect_faces_and_texts(image)

        # Extraire le texte
        extracted_text = extract_text(image)

        # Classifier le type de carte
        card_type = classify_card(extracted_text)

        # Afficher l'image annotée
        st.subheader("Image Annotée")
        st.image(processed_image, channels="BGR", use_container_width=True)  

        # Afficher les résultats
        st.subheader("Résultats de l'Extraction")
        st.text_area("Texte Extrait :", extracted_text, height=150)
        st.write(f"**Type de Carte :** {card_type}")

        # Télécharger l'image annotée
        result_image = cv2.imencode(".jpg", processed_image)[1].tobytes()
        st.download_button(label="Télécharger l'image annotée", data=result_image, file_name="result.jpg")

        # Télécharger le texte extrait
        st.download_button(label="Télécharger le texte extrait", data=extracted_text, file_name="text.txt")

# Lancer l'application
if __name__ == "__main__":
    main()
