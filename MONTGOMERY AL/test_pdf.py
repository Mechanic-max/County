
import PyPDF2
pdf_file = open('1001013003026040.pdf', 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()
page_content = str(page_content)
page_content = page_content.strip("\n")
print(page_content.encode('utf-8'))
