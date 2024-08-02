import os
import argparse
import nltk
from gtts import gTTS
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


def download_nltk_data():
    if not os.path.exists(nltk.data.find("tokenizers/punkt")):
        nltk.download("punkt")


def extract_text_from_pdf(pdf_path, start_page, end_page):
    if not os.path.isfile(pdf_path):
        print(f"Error: File {pdf_path} does not exist.")
        return ""

    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page_num in range(start_page, end_page + 1):
                if page_num >= len(pdf_reader.pages):
                    break
                page = pdf_reader.pages[page_num]
                text += page.extract_text() or ""
            return text
    except Exception as e:
        print(f"Error: An issue occurred while reading the PDF file: {e}")
        return ""


def summarize_text(text):
    download_nltk_data()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)
    return " ".join([str(sentence) for sentence in summary])


def text_to_speech(text, output_file, lang):
    if text.strip() == "":
        print("Error: No text to convert to speech.")
        return

    try:
        tts = gTTS(text, lang=lang)
        tts.save(output_file)
        print(f"Success: Audio saved to {output_file}")
    except Exception as e:
        print(f"Error: An issue occurred while converting text to speech: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert PDF text to audio speech.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument(
        "output_file", type=str, help="Path to save the output audio file"
    )
    parser.add_argument(
        "--lang", type=str, default="en", help="Language for speech synthesis"
    )
    parser.add_argument(
        "--start_page", type=int, default=0, help="Starting page number"
    )
    parser.add_argument("--end_page", type=int, default=1, help="Ending page number")
    parser.add_argument(
        "--chunk_size", type=int, default=1000, help="Chunk size for processing text"
    )
    parser.add_argument(
        "--summarize", action="store_true", help="Summarize the text before conversion"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--search",
        type=str,
        default=None,
        help="Keyword to search in the extracted text",
    )

    args = parser.parse_args()

    print(
        f"Extracting text from {args.pdf_path} starting at page {args.start_page} to {args.end_page}..."
    )
    text = extract_text_from_pdf(args.pdf_path, args.start_page, args.end_page)
    if args.verbose:
        print(f"Extracted text preview: {text[:100]}...")

    if args.search:
        if args.search in text:
            print(f"Keyword '{args.search}' found in the extracted text.")
        else:
            print(f"Keyword '{args.search}' not found in the extracted text.")

    if args.summarize:
        print("Summarizing text...")
        text = summarize_text(text)

    text_to_speech(text, args.output_file, args.lang)


if __name__ == "__main__":
    main()
