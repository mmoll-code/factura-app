import fitz  # PyMuPDF
print(fitz.__file__)
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import os
import re
import unicodedata
import shutil
from app.core import config




INPUT_IMG_INVOICE = config.INPUT_IMG_INVOICE
OUTPUT_IMG_INVOICE = config.OUTPUT_IMG_INVOICE

def normalize_filename(filename):
    # Remove special characters and tildes
    filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
    # Remove remaining non-alphanumeric characters
    filename = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
    return filename

def pdf_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    pdf_document = fitz.open(pdf_path)
    image_files = []
    base_filename = normalize_filename(os.path.basename(pdf_path).split(".")[0])
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)  # Aumentar la resolución DPI si es necesario
        image_file = os.path.join(output_folder, f'{base_filename}_page_{page_num+1}.png')
        pix.save(image_file)
        image_files.append(image_file)
    
    return image_files

def enhance_image(image_path, output_path):
    with Image.open(image_path) as img:
        gray_img = img.convert('L')
        enhancer = ImageEnhance.Contrast(gray_img)
        enhanced_img = enhancer.enhance(2)  # Adjust this value as needed
        enhanced_img.save(output_path)

def process_image(image_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    base_filename = normalize_filename(os.path.basename(image_path).split(".")[0])
    enhanced_image_path = os.path.join(output_folder, f'{base_filename}_enhanced.png')
    
    enhance_image(image_path, enhanced_image_path)
    
    return enhanced_image_path

def process_pdf(pdf_path, output_folder):
    image_files = pdf_to_images(pdf_path, output_folder)
    processed_files = []
    for image_file in image_files:
        final_image_path = process_image(image_file, output_folder)
        processed_files.append(final_image_path)
    return processed_files

def process_all_files(input_folder, output_folder):
    all_processed_files = []
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if filename.lower().endswith('.pdf'):
            processed_files = process_pdf(file_path, output_folder)
        elif filename.lower().endswith(('.jpeg', '.jpg', '.png')):
            final_image_path = process_image(file_path, output_folder)
            processed_files = [final_image_path]
        else:
            continue  # Skip files that are not PDFs or images
        
        all_processed_files.extend(processed_files)
    return all_processed_files

def move_enhanced_files(output_folder):
    enhanced_folder = os.path.join(output_folder, 'output_images_enhanced')
    if not os.path.exists(enhanced_folder):
        os.makedirs(enhanced_folder)
    
    for filename in os.listdir(output_folder):
        if filename.endswith('_enhanced.png'):
            file_path = os.path.join(output_folder, filename)
            shutil.move(file_path, enhanced_folder)

    # Call the function to move the enhanced files


if __name__ == "__main__":
    # input_folder = 'fisicas1'  # Ruta a la carpeta de entrada
    # input_folder = 'fisicas2'  # Ruta a la carpeta de entrada
    input_folder = config.INPUT_IMG_INVOICE  # Ruta a la carpeta de entrada
    # output_folder = 'output_images2'
    output_folder = config.OUTPUT_IMG_INVOICE
    all_processed_files = process_all_files(input_folder, output_folder)
    # print("Processed files:", all_processed_files)
    move_enhanced_files(output_folder)


def run_processing_pipeline():
    input_folder = INPUT_IMG_INVOICE  # Ruta a la carpeta de entrada
    output_folder = OUTPUT_IMG_INVOICE  # Ruta a la carpeta de salida
    all_processed_files = process_all_files(input_folder, output_folder)
    # print("Processed files:", all_processed_files)
    move_enhanced_files(output_folder)


# Si querés seguir pudiendo ejecutarlo directamente desde consola:
if __name__ == "__main__":
    run_processing_pipeline()
