# -*- coding: utf-8 -*-

import PyPDF2
from utils.general_utils import EmptyListError


class PDF2txt:

    def __init__(self, pdf_folder_path, txt_folder_path):

        self.pdf_folder_path = pdf_folder_path
        self.txt_folder_path = txt_folder_path

    @staticmethod
    def _read_pdf_file(file_path, not_machine_readable_patience=3):

        file_text_pages = []
        counter_empty = 0

        with file_path.open('rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            for pag in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(pag)
                page_text = page.extractText()
                if page_text == '':
                    counter_empty += 1
                    if counter_empty == not_machine_readable_patience \
                            and pag == not_machine_readable_patience:
                        # If the first N pages are empty, just skip and assume not MR.
                        break
                    continue
                file_text_pages.append(page_text)

        if file_text_pages:
            return file_text_pages
        else:
            raise EmptyListError('File {} is not machine readable'.format(file_path.name))

    @staticmethod
    def _write_file(file_path):
        raise NotImplementedError

    def _index_files(self):
        raise NotImplementedError



if __name__ =='__main__':

    from pathlib import Path

    # Example one: Image but MR
    pdf_example1 = Path('/Users/eduardofierro/Desktop/data/pdfs/d8cefefe8e1311e9be2fc8e0eb17424f.pdf')

    # Example two: Not MR
    pdf_example2 = Path('/Users/eduardofierro/Desktop/data/pdfs/d8cf0caa8e1311e9be2fc8e0eb17424f.pdf')

    # Example three: Tipical SIL doc
    pdf_example3 = Path('/Users/eduardofierro/Desktop/data/pdfs/d8cf0db88e1311e9be2fc8e0eb17424f.pdf')

    list_example1 = PDF2txt._read_pdf_file(pdf_example1)
    list_example2 = PDF2txt._read_pdf_file(pdf_example2)
    list_example3 = PDF2txt._read_pdf_file(pdf_example3)
