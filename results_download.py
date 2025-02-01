import os
from datetime import date
from selenium.webdriver.common.by import By
from base_selenium import BaseSelenium


def results_download():
    file_creation_date = date.today()
    bot = BaseSelenium(with_interface=False)
    os.chdir(bot.save_to)
    download_folder = os.listdir()
    if download_folder:
        file_creation_date = date.fromtimestamp(os.stat(download_folder[0]).st_mtime)

    if not download_folder or file_creation_date < date.today():
        for item in download_folder:
            os.unlink(item)
        url = 'https://loterias.caixa.gov.br/Paginas/Lotofacil.aspx'
        button_download_id = 'btnResultados'
        try:
            bot.access_page(url)
            bot.click_element((By.ID, button_download_id))
            status, message = bot.check_download_status()
            print(message)
        except Exception as error:
            print(error)
        finally:
            if os.listdir() and os.listdir()[0].endswith('xlsx'):
                bot.driver.quit()
    else:
        print('Já foi feito o download do arquivo hoje')


results_download()
