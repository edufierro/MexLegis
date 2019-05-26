import urllib
import pandas as pd
import time
import re
from bs4 import BeautifulSoup
from utils import remove_temp


class MexLegScrapper:

    def __init__(self, legislatura, url_to_scrape):
        self.legislatura = legislatura
        self.url_to_scrape = url_to_scrape  # TODO: Get this url automatically through post method

    def get_post_url(self):
        raise NotImplemented

    @staticmethod
    def _get_page_soup(current_url, timeout=200):
        with urllib.request.urlopen(current_url, timeout=timeout) as f:
            time.sleep(2)
            page = f.read()

        soup = BeautifulSoup(page, features="lxml")

        return soup

    @classmethod
    def _get_page_table(cls, soup):

        all_tables = soup.find_all('table')
        main_table = cls._parse_html_table(all_tables[6])
        main_table.columns = main_table.iloc[0]
        main_table = main_table.iloc[2:]

        return main_table

    @staticmethod
    def _get_table_urls(soup):

        main_page_ = 'http://sil.gobernacion.gob.mx'  # TODO: clear this once get_post_url is Implemented

        all_urls = soup.find_all('a', href=True)
        onclick_urls = [x.get('onclick') for x in all_urls if x.get('onclick') is not None]
        onclick_urls = [x for x in onclick_urls if 'pp_ContenidoAsuntos' in x]

        get_url_regex = re.compile('"[^"]*"')

        onclick_urls = [get_url_regex.findall(x)[0] for x in onclick_urls]
        onclick_urls = ['{}{}'.format(main_page_, x.replace('\"', "")) for x in onclick_urls]

        return onclick_urls

    @staticmethod
    def _get_pdf_from_url(iniciativa_url, timeout=200):
        with urllib.request.urlopen(iniciativa_url, timeout=timeout) as f:
            time.sleep(0.5)
            page = f.read()

        soup_iniciativa = BeautifulSoup(page, features="lxml")
        all_urls = soup_iniciativa.find_all('a', href=True)

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




    # Scrape for the LXIII Legislatura
url = 'http://sil.gobernacion.gob.mx/Busquedas/Basica/ResultadosBusquedaBasica.php?SID=00026758073a8aec07544e9fe9074b68&Serial=173dc986d689043187bd882164410a7b&Reg=2405&Origen=BB&Paginas=15'
current_url = url
timeout = 200

main_page = 'http://sil.gobernacion.gob.mx/portal/AsuntosLegislativos/busquedaBasica'


def get_soup(my_url):
    try:
        html = urllib.request.urlopen(my_url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        return bsObj
    except AttributeError as e:
        return None