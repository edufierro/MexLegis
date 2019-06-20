# -*- coding: utf-8 -*-

import click
from scrapper.pdfs_download import MexLegScrapper
from utils.file_utils import check_create_output_folder, \
    check_create_file_path

@click.command()
@click.option(u'--sil-url', u'-url', type=str, required=True,
              help='URL to sil search web page. Example: '
                   'http://sil.gobernacion.gob.mx/Busquedas/Basica/ResultadosBusquedaBasica.php?SID=bc5018f4636aa88b40174fb6164460db&Origen=BB&Serial=f10e3813e027399d13ac9aa8fc7ce535&Reg=2472&Paginas=15') # NOQA
@click.option(u'--data-path', u'-data', type=click.Path(), required=True,
              help=u'Path to data folder')
@click.option(u'--pdfs-folder', u'-pdfs', type=str, required=True, default='pdfs',
              help=u'PDFs folder name. Will be created inside data path')
@click.option(u'--txt-folder', u'-txt', type=str, required=True, default='txts',
              help=u'TXT folder name. Will be created inside data path')
@click.option(u'--main-data-file', u'-main', type=str, required=True, default='MainTable.csv',
              help=u'Main table filename. Will be created')
def scrape_bills(sil_url, data_path, pdfs_folder, txt_folder, main_data_file):

    main_data_file = check_create_file_path(data_path,main_data_file)
    out_pdfs_folder_path = check_create_output_folder(data_path, pdfs_folder)
    out_txts_folder_path = check_create_output_folder(data_path, txt_folder)

    bills_scrapper = MexLegScrapper(sil_url, out_pdfs_folder_path, main_data_file)
    bills_scrapper.create_main_table()
    bills_scrapper.download_pdfs(tsleep=0.5)


