import os
import shutil
from PIL import Image
import gradio as gr
import atexit
import time

# Constantes pour les chemins de dossiers
INPUT_FOLDER = os.path.abspath("input_images")
RESULTS_FOLDER = os.path.abspath("results")

def setup_folders():
    """Crée les dossiers nécessaires s'ils n'existent pas"""
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

def cleanup_on_exit():
    """Nettoie les dossiers temporaires à la fermeture"""
    for folder in [INPUT_FOLDER, RESULTS_FOLDER]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

def highlight_element(image):
    """Fonction fictive pour surligner un élément dans une image"""
    return image.copy()  # Retourne une copie de l'image

def process_image(image):
    try:
        setup_folders()  # S'assure que les dossiers existent
        
        # Détecter le format de l'image
        format = image.format or 'PNG'
        
        # Utiliser des noms de fichiers uniques avec timestamp
        timestamp = int(time.time())
        base_name = f"image_{timestamp}"
        
        highlighted_result_path = os.path.join(RESULTS_FOLDER, f"{base_name}_h.{format.lower()}")

        # Créer et sauvegarder l'image surlignée
        highlighted_image = highlight_element(image)
        highlighted_image.save(highlighted_result_path, format=format)

        return highlighted_image  # Retourne uniquement l'image surlignée
    except Exception as e:
        print(f"Erreur lors du traitement de l'image: {str(e)}")
        raise

def gradio_interface(image):
    try:
        return process_image(image)
    except Exception as e:
        print(f"Erreur lors de l'interface Gradio: {str(e)}")
        raise

if __name__ == "__main__":
    # Créer les dossiers au démarrage
    setup_folders()
    
    # Enregistrer le nettoyage à la fermeture
    atexit.register(cleanup_on_exit)
    
    # Créer l'interface utilisateur
    interface = gr.Interface(
        fn=gradio_interface,
        inputs=gr.Image(type="pil"),
        outputs=gr.Image(label="Image avec Élément Surligné"),
        title="Traitement d'Image avec Élément Surligné",
        description="Téléchargez une image pour voir l'élément surligné."
    )
    
    interface.launch()