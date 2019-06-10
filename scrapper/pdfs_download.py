# -*- coding: utf-8 -*-

import urllib
import pandas as pd
import time
import re
from bs4 import BeautifulSoup
from utils.file_utils import check_create_output_folder
from utils.click_utlis import info, error, warn


class MexLegScrapper:

    def __init__(self, url_to_scrape, pdf_folder_name, txt_folder_name, table_name):

        self.url_to_scrape = url_to_scrape  # TODO: Get this url automatically through post method
        self.main_page = 'http://sil.gobernacion.gob.mx'
        self.all_iniciativas_table = table_name
        self.pdf_folder_name = check_create_output_folder(pdf_folder_name)
        self.txt_folder_name = check_create_output_folder(txt_folder_name)

        self.main_table = None

    def get_post_url(self):
        # TODO: Parse url automatically
        raise NotImplementedError

    def create_main_table(self):
        soups_generator = self._soups_generator()

        info('Beginning scrapping loop')
        for page_soup in soups_generator:
            page_table = self._get_page_table(page_soup)
            page_urls = self._get_table_urls(page_soup)
            page_table['onclicks'] = page_urls
            if page_table.shape[1] != 13:
                error('Inconsistent table lengths, exiting', fatal=True)
            self.main_table.append(page_table)

        self.main_table.to_csv(self.all_iniciativas_table)

    def _soups_generator(self):
        idx = 0
        finished_yielding = False
        while finished_yielding is False:
            idx += 1
            url_to_scrape = '{}&pagina={}'.format(self.url_to_scrape, idx)
            page_soup, should_continue = self._get_soup_and_continue_token(url_to_scrape)

            if idx % 5 == 0:
                info('Advance: {}...'.format(idx))

            if should_continue is False:
                finished_yielding = True
                warn('Finished scrapping at page {}'.format(idx))
            else:
                yield page_soup

    @classmethod
    def _get_soup_and_continue_token(cls, web_page):
        page_soup = cls._get_page_soup(web_page)
        is_bad = page_soup.find('td', {"class": "simpletextorange"})
        if is_bad.contents:
            return None, True
        else:
            return page_soup, False

    @classmethod
    def _get_page_table(cls, soup):

        all_tables = soup.find_all('table')
        main_table = cls._parse_html_table(all_tables[6])
        main_table.columns = main_table.iloc[0]
        main_table = main_table.iloc[2:]

        return main_table

    def _get_table_urls(self, soup):

        all_urls = soup.find_all('a', href=True)
        onclick_urls = [x.get('onclick') for x in all_urls if x.get('onclick') is not None]
        onclick_urls = [x for x in onclick_urls if 'pp_ContenidoAsuntos' in x]

        get_url_regex = re.compile('"[^"]*"')

        onclick_urls = [get_url_regex.findall(x)[0] for x in onclick_urls]
        onclick_urls = ['{}{}'.format(self.main_page, x.replace('\"', "")) for x in onclick_urls]

        return onclick_urls

    @classmethod
    def _download_pdf_from_table(cls, iniciativa_url):

        soup_iniciativa = cls._get_page_soup(iniciativa_url, tsleep=0.5)
        urls_iniciativa = soup_iniciativa.find_all(href=True)
        urls_iniciativa = [x.get('href') for x in urls_iniciativa]
        urls_iniciativa = [x for x in urls_iniciativa if x.split('.')[-1]=='pdf']

        if len(urls_iniciativa) > 1:
            raise AttributeError('More pdfs found in {}'.format(iniciativa_url))

        if len(urls_iniciativa) == 0:
            raise AttributeError('No pdf found in {}'.format(iniciativa_url))

        return urls_iniciativa[0]

    @staticmethod
    def _get_page_soup(current_url, timeout=200, tsleep=2.0):
        with urllib.request.urlopen(current_url, timeout=timeout) as f:
            time.sleep(tsleep)
            page = f.read()

        soup = BeautifulSoup(page, features="lxml")

        return soup

    @staticmethod
    def _parse_html_table(table):
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns,
                          index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        return df
