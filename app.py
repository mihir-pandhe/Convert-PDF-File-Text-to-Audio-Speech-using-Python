import PyPDF2
from gtts import gTTS
import argparse
import os
import sys


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


def text_to_speech(text, output_file, lang="en"):
    if text.strip() == "":
        print("Error: No text to convert to speech.")
        return

    tts = gTTS(text, lang=lang)
    tts.save(output_file)
    print(f"Success: Audio saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Convert PDF text to audio speech")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("output_file", help="Output audio file path")
    parser.add_argument("--lang", default="en", help="Language for text-to-speech")
    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf_path)
    if text:
        text_to_speech(text, args.output_file, args.lang)


if __name__ == "__main__":
    main()
