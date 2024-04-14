import requests
import PyPDF2
import re

from Essentials import Package_Tag, Txt_package, Pipeline_Actor

class Text_Extractor(Pipeline_Actor):
    def get_pdf(self, path, use_url: bool):

        # Достаём PDF-файл по его загрузочной (Download) URL-ссылке
        if use_url:
            try:
                pdf1 = requests.get(path)
                with open("my_pdf.pdf", 'wb') as my_data:
                    my_data.write(pdf1.content)

                open_pdf_file = open("my_pdf.pdf", 'rb')
            except:
                raise Exception('Unable to open PDF file')
        # Или находим PDF по пути файла

        else:
            try:
                open_pdf_file = open(path, 'rb')

            except:
                raise Exception('Unable to open PDF file')

        read_pdf = PyPDF2.PdfReader(open_pdf_file)

        if read_pdf.is_encrypted:
            read_pdf.decrypt("")

        return read_pdf

    def get_packages(self, path, use_url=True, start_page_n = 1):
        packages = [Txt_package]

        read_pdf = self.get_pdf(path, use_url)

        if type(start_page_n) != int:
            raise TypeError('Page input must be an integer.')

        if start_page_n > len(read_pdf.pages) or start_page_n <= 0:
            raise AssertionError('Page number outside of page range.')

        all_page_read = []
        split_page = []
        for i in range(len(read_pdf.pages)):
            if i < start_page_n:
                continue
            page = read_pdf.pages[i]

            # Отрезаем абзац со ссылками на литературу - он нам не нужен для суммвризации

            if re.search(r'\s.*references\s*', page.extract_text(), flags=re.IGNORECASE) != None:
                split_page = re.split(r'references\s', page.extract_text(), flags=re.IGNORECASE)
                all_page_read.append(split_page[0])
                break
            all_page_read.append(page.extract_text())

        packages.append(Txt_package(all_page_read, 0.0, Package_Tag.Pages))

        all_pg_str = ' '.join(all_page_read)

        packages.append(Txt_package([all_pg_str], 0.0, Package_Tag.FullText))

        return packages
