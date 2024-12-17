import os
import cv2 as cv
import pytesseract
import numpy as np

# Configuration de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\pc\Desktop\M1\Approches experimentales\Tesseract-OCR\tesseract.exe"

# Définir le chemin vers le modèle EAST
EAST_MODEL_PATH = "frozen_east_text_detection.pb"
INPUT_DIR = "input_images/"
OUTPUT_DIR = "output/"

# Paramètres pour EAST
CONF_THRESHOLD = 0.5  # Seuil de confiance
NMS_THRESHOLD = 0.4   # Suppression non maximale


def decodeBoundingBoxes(scores, geometry, scoreThresh):
    """Décode les boîtes englobantes à partir des scores et géométries."""
    detections = []
    confidences = []

    height, width = scores.shape[2:4]
    for y in range(height):
        scoresData = scores[0, 0, y]
        anglesData = geometry[0, 4, y]
        xData = geometry[0, :4, y]

        for x in range(width):
            score = scoresData[x]
            if score < scoreThresh:
                continue

            offsetX, offsetY = x * 4.0, y * 4.0
            angle = anglesData[x]
            cos, sin = np.cos(angle), np.sin(angle)

            h = xData[0, x] + xData[2, x]
            w = xData[1, x] + xData[3, x]
            endX = int(offsetX + (cos * xData[1, x]) + (sin * xData[2, x]))
            endY = int(offsetY - (sin * xData[1, x]) + (cos * xData[2, x]))
            startX, startY = int(endX - w), int(endY - h)

            detections.append((startX, startY, endX, endY))
            confidences.append(float(score))

    return detections, confidences


def extract_text_from_image(image_path, east_model, output_dir):
    """Extrait du texte d'une image et sauvegarde les résultats."""
    # Charger l'image
    image = cv.imread(image_path)
    if image is None:
        print(f"Erreur : Impossible de lire l'image {image_path}")
        return

    # Redimensionner l'image pour EAST
    orig = image.copy()
    (H, W) = image.shape[:2]
    newW, newH = (320, 320)
    rW, rH = W / float(newW), H / float(newH)

    image = cv.resize(image, (newW, newH))
    blob = cv.dnn.blobFromImage(image, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)

    # Passer l'image dans EAST
    east_model.setInput(blob)
    scores, geometry = east_model.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])

    # Décoder les boîtes englobantes
    detections, confidences = decodeBoundingBoxes(scores, geometry, CONF_THRESHOLD)
    indices = cv.dnn.NMSBoxes(detections, confidences, CONF_THRESHOLD, NMS_THRESHOLD)

    extracted_text = ""
    for i in indices.flatten():
        startX, startY, endX, endY = detections[i]

        # Vérifier les coordonnées
        startX, startY, endX, endY = int(startX * rW), int(startY * rH), int(endX * rW), int(endY * rH)
        if startX < 0 or startY < 0 or endX > W or endY > H:
            print(f"Coordonnées invalides : ({startX}, {startY}), ({endX}, {endY})")
            continue

        # Extraire la région de texte et appliquer Tesseract OCR
        roi = orig[startY:endY, startX:endX]
        if roi.size == 0:
            print(f"Région vide pour les coordonnées : ({startX}, {startY}), ({endX}, {endY})")
            continue

        gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
        # Appliquer un seuillage adaptatif
        gray = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                            cv.THRESH_BINARY, 11, 2)
        text = pytesseract.image_to_string(gray, lang="eng+fra")
        extracted_text += text + "\n"

        # Dessiner les boîtes englobantes
        cv.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Sauvegarder l'image annotée
    os.makedirs(output_dir, exist_ok=True)
    output_image_path = os.path.join(output_dir, os.path.basename(image_path))
    cv.imwrite(output_image_path, orig)

    # Sauvegarder le texte extrait
    output_text_path = os.path.join(output_dir, "text_results.txt")
    with open(output_text_path, "a", encoding="utf-8") as file:
        file.write(f"Texte extrait de {image_path} :\n{extracted_text}\n{'-'*50}\n")

    print(f"Texte extrait sauvegardé pour {image_path} dans {output_dir}")


def main():
    # Charger le modèle EAST
    east_model = cv.dnn.readNet(EAST_MODEL_PATH)

    # Parcourir toutes les images du dossier
    for image_file in os.listdir(INPUT_DIR):
        image_path = os.path.join(INPUT_DIR, image_file)
        if os.path.isfile(image_path):
            print(f"Traitement de l'image : {image_file}")
            extract_text_from_image(image_path, east_model, OUTPUT_DIR)


if __name__ == "__main__":
    main()
