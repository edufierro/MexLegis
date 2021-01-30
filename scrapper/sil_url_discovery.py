# -*- coding: utf-8 -*-

import os
import time

from utils.click_utlis import info, error
from selenium import webdriver


class URLDiscoverySIL:

    def __init__(self, selenium_driver=None):

        self.url_to_scrape = None
        # This is hard coded.
        self.search_url = 'http://sil.gobernacion.gob.mx/portal/AsuntosLegislativos/busquedaBasica'
        info('Searching url {}'.format(self.search_url))

        self.driver_path = os.environ.get('CHROMEPATH', selenium_driver)
        if not self.driver_path:
            error('No Selenium Driver Found. You can set it with CHROMEPATH env variable')

    def _get_soup_using_selenium(self):
        driver = webdriver.Chrome('/Users/eduardofierro/Downloads/chromedriver')
        driver.get(self.search_url)
        time.sleep(2) # Sleeping two seconds,
