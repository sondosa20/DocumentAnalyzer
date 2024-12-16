import os

# Définir la structure du projet
structure = {
    "DocumentAnalyzer": [
        "README.md",
        "requirements.txt",
        "LICENSE",
        ".gitignore",
        "input_images/",
        "output/extracted_texts/",
        "output/classified_cards/",
        "modules/preprocessing.py",
        "modules/feature_extraction.py",
        "modules/classification.py",
        "modules/video_processing.py",
        "main.py",
        "video_processing.py",
        "tests/test_preprocessing.py",
        "tests/test_extraction.py",
        "tests/test_classification.py",
    ]
}

# Fonction pour créer les fichiers et dossiers
def create_project_structure(structure):
    for root, items in structure.items():
        if not os.path.exists(root):
            os.mkdir(root)  # Créer le dossier racine
        for item in items:
            path = os.path.join(root, item)
            if item.endswith("/"):
                os.makedirs(path, exist_ok=True)  
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w") as f:
                    f.write("")  

create_project_structure(structure)
print("The project structure has been successfully generated!")