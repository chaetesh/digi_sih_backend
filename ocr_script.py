import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import fitz  # PyMuPDF
import os
import sys
import re
import json

pytesseract.pytesseract.tesseract_cmd = r'tesseract'


def convert_pdf_to_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(image_path)
        image_paths.append(image_path)

    return image_paths


def extract_text_from_images(image_paths):
    extracted_text = ""

    for image_path in image_paths:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        extracted_text += text + "\n"

    return extracted_text


def split_text_into_words(text):
    words = re.split(r'[ \(\)\[\]\{\},.:;!?_-]', text)
    words = [word.strip() for word in words if word.strip()]
    return words


def clean_text(word_list):
    cleaned_text = ' '.join(word_list)
    cleaned_text = cleaned_text.strip().lower()
    return cleaned_text


def extract_caste(text, caste_dict):
    for caste, category in caste_dict.items():
        if re.search(rf'\b{re.escape(caste.lower())}\b', text, re.IGNORECASE):
            return f"{caste} ({category})"
    return 'Caste not found'


# Caste dictionary
caste_dict = {


    # Other Backward Classes (OBC)
    'Kurmi': 'OBC', 'Yadav': 'OBC', 'Jat': 'OBC', 'Lohar': 'OBC', 'Teli': 'OBC', 'Kumhar': 'OBC', 'Darzi': 'OBC',
    'Banjara': 'OBC', 'Sonar': 'OBC', 'Gupta': 'OBC', 'Sahu': 'OBC', 'Kalal': 'OBC', 'Bairwa': 'OBC', 'Koli': 'OBC',
    'Meo': 'OBC', 'Ahir': 'OBC', 'Nai': 'OBC', 'Kashyap': 'OBC', 'Gondhali': 'OBC', 'Kahar': 'OBC', 'Dhobi': 'OBC',
    'Patwa': 'OBC', 'Kachhi': 'OBC', 'Mallaha': 'OBC', 'Saini': 'OBC', 'Gurjar': 'OBC', 'Kalwar': 'OBC',
    'Prajapati': 'OBC', 'Rajbhar': 'OBC', 'Kevat': 'OBC', 'Khatik': 'OBC', 'Lodhi': 'OBC', 'Nat': 'OBC',
    'Nonia': 'OBC', 'Koeri': 'OBC', 'Tanti': 'OBC', 'Karmakar': 'OBC', 'Chandravanshi': 'OBC', 'Mahishya': 'OBC',
    'Sadgop': 'OBC', 'Kaibarta': 'OBC', 'Sunri': 'OBC', 'Khandayat': 'OBC', 'Gudia': 'OBC', 'Gopala': 'OBC',
    'Chasa': 'OBC', 'Mali': 'OBC', 'Ahom': 'OBC', 'Chutia': 'OBC', 'Koch': 'OBC', 'Meitei': 'OBC', 'Agnikulakshatriya': 'OBC',
    'Arya Vysya': 'OBC', 'Balija': 'OBC', 'Bestha': 'OBC', 'Chakali': 'OBC', 'Ediga': 'OBC', 'Goud': 'OBC', 'Kuruba': 'OBC',
    'Mangali': 'OBC', 'Mudaliar': 'OBC', 'Mudiraj': 'OBC', 'Mutrasi': 'OBC', 'Padmasali': 'OBC', 'Rajaka': 'OBC',
    'Setti Balija': 'OBC', 'Telaga': 'OBC', 'Uppara': 'OBC', 'Vaddera': 'OBC', 'Yadava': 'OBC', 'Perika': 'OBC',
    'Thogata Veera Kshatriya': 'OBC', 'Vanniyar': 'OBC', 'Thevar': 'OBC', 'Gounder': 'OBC', 'Vannar': 'OBC',
    'Maravar': 'OBC', 'Ganiga': 'OBC', 'Madivala': 'OBC', 'Ezhava': 'OBC', 'Thiyya': 'OBC', 'Vishwakarma': 'OBC',
    'Billava': 'OBC', 'Dhangar': 'OBC',

    # Forward Castes (General Category)
    'Brahmin': 'Forward Caste', 'Kshatriya': 'Forward Caste', 'Vaishya': 'Forward Caste', 'Kayastha': 'Forward Caste',
    'Rajput': 'Forward Caste', 'Thakur': 'Forward Caste', 'Bhumihar': 'Forward Caste', 'Tyagi': 'Forward Caste',
    'Agarwal': 'Forward Caste', 'Khatri': 'Forward Caste', 'Punjabi Khatri': 'Forward Caste', 'Arora': 'Forward Caste',
    'Sindhi': 'Forward Caste', 'Gaur Brahmin': 'Forward Caste', 'Chandravanshi Kshatriya': 'Forward Caste',
    'Madhesiya': 'Forward Caste', 'Khandelwal': 'Forward Caste', 'Vaishnav': 'Forward Caste', 'Oswal': 'Forward Caste',
    'Digambar Jain': 'Forward Caste', 'Svetambar Jain': 'Forward Caste', 'Baidya': 'Forward Caste',
    'Kayastha Bengali': 'Forward Caste', 'Brahmin Bengali': 'Forward Caste', 'Karana': 'Forward Caste',
    'Brahmin Assamese': 'Forward Caste', 'Kalita': 'Forward Caste', 'Kamma': 'Forward Caste', 'Reddy': 'Forward Caste',
    'Velama': 'Forward Caste', 'Kapu': 'Forward Caste', 'Vysya': 'Forward Caste', 'Iyer': 'Forward Caste',
    'Iyengar': 'Forward Caste', 'Mudaliar': 'Forward Caste', 'Nadar': 'Forward Caste', 'Vellalar': 'Forward Caste',
    'Chettiar': 'Forward Caste', 'Lingayat': 'Forward Caste', 'Vokkaliga': 'Forward Caste', 'Namboodiri Brahmin': 'Forward Caste',
    'Nair': 'Forward Caste', 'Menon': 'Forward Caste', 'OC': 'OC',



    # Scheduled Castes (SC)
    'Chamar': 'SC', 'Jatav': 'SC', 'Valmiki': 'SC', 'Mahar': 'SC', 'Bhangi': 'SC', 'Pasi': 'SC', 'Balmiki': 'SC',
    'Khatik': 'SC', 'Dhobi': 'SC', 'Musahar': 'SC', 'Dhanuk': 'SC', 'Dom': 'SC', 'Kori': 'SC', 'Dusadh': 'SC',
    'Halalkhor': 'SC', 'Koli': 'SC', 'Mehtar': 'SC', 'Bhovi': 'SC', 'Hajjam': 'SC', 'Rai Sikh': 'SC', 'Bagdi': 'SC',
    'Namasudra': 'SC', 'Rajbanshi': 'SC', 'Bauri': 'SC', 'Adi Andhra': 'SC', 'Mala': 'SC', 'Madiga': 'SC',
    'Dommara': 'SC', 'Pambada': 'SC', 'Dakkal': 'SC', 'Jambavan': 'SC', 'Masti': 'SC', 'Pulaya': 'SC',
    'Paraiyar': 'SC', 'Pallan': 'SC', 'Arunthathiyar': 'SC', 'Chakkiliyar': 'SC', 'Holeya': 'SC', 'Cheruman': 'SC',
    'Mannan': 'SC', 'Valluvan': 'SC', 'Madiga': 'SC', 'Mala': 'SC',

    # Scheduled Tribes (ST)
    'Santhal': 'ST', 'Oraon': 'ST', 'Munda': 'ST', 'Meena': 'ST', 'Gond': 'ST', 'Bhil': 'ST', 'Sahariya': 'ST',
    'Lodha': 'ST', 'Kharwar': 'ST', 'Khond': 'ST', 'Korku': 'ST', 'Bhot': 'ST', 'Pahari Korwa': 'ST', 'Tharu': 'ST',
    'Kol': 'ST', 'Baiga': 'ST', 'Bhutia': 'ST', 'Bodo': 'ST', 'Mishing': 'ST', 'Deori': 'ST', 'Rabha': 'ST',
    'Karbi': 'ST', 'Naga': 'ST', 'Khasi': 'ST', 'Garo': 'ST', 'Hmar': 'ST', 'Kuki': 'ST', 'Biate': 'ST', 'Tiwa': 'ST',
    'Dimasa': 'ST', 'Koya': 'ST', 'Lambada': 'ST', 'Yanadi': 'ST', 'Sugali': 'ST', 'Yerukala': 'ST', 'Chenchu': 'ST',
    'Kondareddy': 'ST', 'Irula': 'ST', 'Kaniyan': 'ST', 'Kattunayakan': 'ST', 'Kurumba': 'ST', 'Paliyan': 'ST',
    'Soliga': 'ST', 'Jenukuruba': 'ST', 'Koraga': 'ST', 'Toda': 'ST', 'Siddis': 'ST', 'Paniya': 'ST',
    'Kurichiya': 'ST', 'Malayarayan': 'ST', 'Kadar': 'ST', 'Adiyan': 'ST'
}
# Main OCR processing function


def process_ocr(file_path, output_folder):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == ".pdf":
        image_paths = convert_pdf_to_images(file_path, output_folder)
        extracted_text = extract_text_from_images(image_paths)

        for image_path in image_paths:
            os.remove(image_path)
    else:
        img = Image.open(file_path)
        img = img.convert('L')  # Preprocessing steps
        img = img.filter(ImageFilter.SHARPEN)
        img = ImageEnhance.Contrast(img).enhance(2)
        extracted_text = pytesseract.image_to_string(img)

    words = split_text_into_words(extracted_text)
    cleaned_text = clean_text(words)
    caste_info = extract_caste(cleaned_text, caste_dict)

    return {"text": extracted_text, "caste_info": caste_info}


if __name__ == "__main__":
    file_path = sys.argv[1]
    output_folder = sys.argv[2]
    result = process_ocr(file_path, output_folder)
    print(json.dumps(result))
