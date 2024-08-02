import PyPDF2
from gtts import gTTS
import argparse
import os
import sys


def extract_text_from_pdf(pdf_path, start_page=0, end_page=None, chunk_size=50):
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} does not exist.")
        return ""

    pdf_file = open(pdf_path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    num_pages = len(pdf_reader.pages)

    if end_page is None or end_page > num_pages:
        end_page = num_pages

    if start_page < 0 or start_page >= num_pages:
        print(f"Error: Start page {start_page} is out of range.")
        return ""

    for page_num in range(start_page, end_page):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
        if (page_num - start_page + 1) % chunk_size == 0 or page_num + 1 == end_page:
            sys.stdout.write(f"\rExtracting text: {page_num + 1}/{end_page} pages")
            sys.stdout.flush()
    pdf_file.close()
    print()
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
    parser.add_argument(
        "--start_page", type=int, default=0, help="Starting page number"
    )
    parser.add_argument("--end_page", type=int, help="Ending page number")
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=50,
        help="Number of pages to process at a time",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Increase output verbosity"
    )
    args = parser.parse_args()

    if args.verbose:
        print(
            f"Extracting text from {args.pdf_path} starting at page {args.start_page} to {args.end_page if args.end_page else 'end'}..."
        )

    text = extract_text_from_pdf(
        args.pdf_path, args.start_page, args.end_page, args.chunk_size
    )
    if text:
        if args.verbose:
            print(f"Converting extracted text to speech with language '{args.lang}'...")
        text_to_speech(text, args.output_file, args.lang)


if __name__ == "__main__":
    main()
