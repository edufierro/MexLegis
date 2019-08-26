# -*- coding: utf-8 -*-

import PyPDF2
from PyPDF2.utils import PdfReadError
import re
import pandas as pd
import subprocess
from utils.general_utils import EmptyListError
from utils.click_utlis import info, warn, error
from utils.file_utils import remove_temp
from tqdm import tqdm

supported_parsers = {'PyPDF2', 'pdftotext'}


class PDF2txt:

    def __init__(self, pdf_folder_path, txt_folder_path, table_file_path, parser):

        self.pdf_folder_path = pdf_folder_path
        self.txt_folder_path = txt_folder_path
        self.table_file_path = table_file_path
        self.main_table = self._read_main_table()
        self.parser = parser

    def export_pdfs_to_text(self):
        info('Converting pdfs to txts..')
        for index, row in tqdm(self.main_table.iterrows(),
                               desc='Files',
                               total=self.main_table.shape[0]):
            current_pdf_file_path = self.pdf_folder_path / '{}.pdf'.format(row.iniciativa_id)
            try:
                if self.parser == 'PyPDF2':
                    pages_text = self._read_pdf_file_pdftotext(current_pdf_file_path)
                elif self.parser == 'pdftotext':
                    pages_text = self._read_pdf_file_pdftotext(current_pdf_file_path)
                else:
                    error('Parser not supported. Select on of {}'.format(supported_parsers), fatal=True)
            except EmptyListError:
                warn('File {} is not machine readable. Skipping'.format(row.iniciativa_id))
                self.main_table.ix[index, 'Status'] = 'Not machine readable'
                remove_temp(str(current_pdf_file_path).replace('.pdf', '.txt'))
                continue
            except PdfReadError:
                warn('Exception while parsing file {}. Skipping.'.format(row.iniciativa_id))
                self.main_table.ix[index, 'Status'] = 'Parsing Error'
                remove_temp(str(current_pdf_file_path).replace('.pdf', '.txt'))
                continue
            except OSError:
                warn('OS error in file {}. Check PDF file existance. Skipping.'.format(row.iniciativa_id))
                self.main_table.ix[index, 'Status'] = 'OSError'
                remove_temp(str(current_pdf_file_path).replace('.pdf', '.txt'))
                continue

            txt_file_path = self.txt_folder_path / '{}.txt'.format(row.iniciativa_id)
            self._write_file(pages_text, txt_file_path)
            self.main_table.ix[index, 'Status'] = 'Exported as txt'

        info('Exporting updated main table')
        self._export_main_table()

    def _export_main_table(self):
        self.main_table.to_csv(self.table_file_path, index=False)

    def _read_main_table(self):
        return pd.read_csv(self.table_file_path)

    @staticmethod
    def _read_pdf_file_PyPDF2(file_path, not_machine_readable_patience=3):  # NOQA

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
    def _read_pdf_file_pdftotext(file_path, not_machine_readable_patience=3):

        # TODO: This functions can be simplified a bit.

        file_text_pages = []
        counter_empty = 0

        with file_path.open('rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            num_pages = pdf_reader.getNumPages()

        for pag in range(num_pages):
            subprocess.call(['pdftotext', '-f', str(pag), '-l', str(pag), str(file_path)])
            saved_file = str(file_path).replace('.pdf', '.txt')
            with open(saved_file, 'r', encoding="ISO-8859-1") as f:
                page_text = f.read()
            page_text = page_text.strip()
            remove_temp(saved_file)
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

    @classmethod
    def _write_file(cls, list_of_txt, file_path):
        with file_path.open('w') as f:
            for pag in list_of_txt:
                pag = cls._clean_text(pag)
                f.write(pag)
                f.write(' ')

    @classmethod
    def _clean_text(cls, str_text):
        str_text = cls._remove_extra_line_breaks(str_text)
        str_text = cls._remove_extra_spacing(str_text)
        return str_text

    @staticmethod
    def _remove_extra_line_breaks(str_text):
        return re.sub(r'(?<!\.)\n', ' ', str_text)

    @staticmethod
    def _remove_extra_spacing(str_text):
        str_text = re.sub(r' +', ' ', str_text)
        str_text = str_text.replace('\n ', '\n')
        str_text = str_text.replace('\x0c', '')
        return str_text
