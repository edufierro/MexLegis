# -*- coding: utf-8 -*-

import click
import os

@click.command()
@click.option(u'--sil-url', u'-url', type=str, required=True,
              help=u'URL to sil search web page')
@click.option(u'--data-path', u'-data', type=click.Path(), required=True,
              help=u'Path to data folder')
@click.option(u'--pdfs-folder', u'-pdfs', type=str, required=True,
              help=u'PDFs folder name. Will be created inside data path')
@click.option(u'--txt-folder', u'-txt', type=str, required=True,
              help=u'TXT folder name. Will be created inside data path')
def scrape_bills(sil_url, data_path, pdfs_folder, txt_folder):
    raise NotImplementedError
