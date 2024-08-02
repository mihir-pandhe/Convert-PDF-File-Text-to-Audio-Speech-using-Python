import PyPDF2


def extract_text_from_pdf(pdf_path):
    pdf_file = open(pdf_path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    pdf_file.close()
    return text


pdf_path = "./DATA .pdf"
print(extract_text_from_pdf(pdf_path))
