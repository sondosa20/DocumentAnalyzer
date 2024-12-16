import cv2
import os

def preprocess_image(image_path, output_path):
    """
    Prétraitement d'une image : niveaux de gris, flou gaussien, binarisation.
    
    Args:
        image_path (str): Chemin de l'image à prétraiter.
        output_path (str): Chemin où sauvegarder l'image prétraitée.

    Returns:
        binary (numpy.ndarray): Image prétraitée (binaire).
    """
    # chargement de l'image en niveaux de gris --> Accélère le traitement
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  

    # Réduction du bruit avec un flou gaussien
    blurred = cv2.GaussianBlur(image, (5, 5), 0)  

     # Appliquer une binarisation adaptative
    adaptive_binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # binarisation de l'image avec le seuil d'Otsu: utile pour detecter les formes et les contours, le texte, etc.
    #_, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) 
    

    # Sauvegarder l'image prétraitée
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, adaptive_binary)

    return adaptive_binary

def preprocess_all_images(input_folder, output_folder):  
     # Vérification de l'existence du dossier d'entrée
    if not os.path.exists(input_folder):
        print(f"Erreur : Le dossier {input_folder} n'existe pas.")
        return
    
    # Création du dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    # Parcourir tous les fichiers du dossier d'entrée
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        # Vérifier si le fichier est une image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')): 
            output_path = os.path.join(output_folder, filename)
            preprocess_image(input_path, output_path)
        else:
            print(f"Fichier non-image : {filename}")


# utilisation
input_folder = "input_images"
output_folder = "output"
preprocess_all_images(input_folder, output_folder)