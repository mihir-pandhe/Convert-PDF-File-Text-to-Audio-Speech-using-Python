import PyPDF2
from gtts import gTTS
import os


def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} does not exist.")
        return ""

    pdf_file = open(pdf_path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    pdf_file.close()
    return text


def text_to_speech(text, output_file):
    if text.strip() == "":
        print("Error: No text to convert to speech.")
        return

    tts = gTTS(text)
    tts.save(output_file)
    print(f"Success: Audio saved to {output_file}")


pdf_path = "./DATA.pdf"
text = extract_text_from_pdf(pdf_path)
if text:
    text_to_speech(text, "output.mp3")
