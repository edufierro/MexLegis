# -*- coding: utf-8 -*-

from scrapper.pdfs_download import MexLegScrapper


class URLDiscoverySIL:

    def __init__(self):

        self.url_to_scrape = None
        self.search_url = 'http://sil.gobernacion.gob.mx/portal/AsuntosLegislativos/busquedaBasica'

        # TODO: This is reall ugly. Need to refactor somehow.
        self.main_soup = MexLegScrapper.get_page_soup(self.search_url)

    def _get_tipo_asuntos(self):
        raise NotImplementedError
