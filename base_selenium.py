import os
from sys import stdout
from time import sleep
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.expected_conditions import url_to_be, element_to_be_clickable

class BaseSelenium:
    """
    Class to organize functions to Generate SLA report in Reserve and save in a folder for BI to consume. The file
    that call this is bots_reserve/management/commands/report_gerador.py
    """
    def __init__(self, with_interface=False):
        """
        Base for Reserve's settings that contains some methods to facilitate
        :param download_path: folder path to save download
        :param with_interface: if True run with interface
        """
        self.with_interface = with_interface
        self.url = 'https://loterias.caixa.gov.br/Paginas/Lotofacil.aspx'
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.save_to = f'{BASE_DIR}/files'
        self.driver = self.config_selenium()
        self.wdw = WebDriverWait(self.driver, 40, poll_frequency=10)

    def config_selenium(self):
        """
        Selenium settings
        :return: None
        """
        print('Config selenium...')
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('prefs', {'download.default_directory': self.save_to})

        if not self.with_interface:
            options.add_argument('--headless=new')

        chrome_install = ChromeDriverManager().install()
        folder = os.path.dirname(chrome_install)
        chromedriver_path = os.path.join(folder, "chromedriver")
        os.system(f'chmod 750 {chromedriver_path}')
        service = ChromeService(chromedriver_path)
        self.driver = Chrome(service=service, options=options)
        return self.driver

    def access_page(self, url):
        """
        Access the page according to the URL and wait for it to be ready
        :param url: page url
        :return: None
        """
        print(f'accessing the page {url}')
        self.driver.get(url)
        self.wdw.until(url_to_be(url))

    def click_element(self, element):
        """
        Click on the element
        :param element: tuple type locator containing ex: (By.ID, 'number_id')
        :return: None
        """
        print(f'Downloading...')
        sleep(2)
        self.wdw.until(element_to_be_clickable(element)).click()

    def check_download_status(self) -> tuple:
        """
        Check status download
        :return: True if completed the download successfully or False if an error occurred
        """
        print('checking download status')
        sleep(3)
        count = 0
        while True:
            if not os.listdir(self.save_to) and count < 31:
                stdout.write(f'\rWaiting for download to start: {count}s')
                stdout.flush()
                sleep(1)
                count += 1
            elif count == 31:
                msg = 'ERROR: Download has not started'
                stdout.write(f'\r{msg}\n')
                stdout.flush()
                return False, msg
            else:
                stdout.write('\rStarting download')
                stdout.flush()
                break

        count = 0
        while True:
            if os.listdir(self.save_to)[0].endswith(".crdownload"):
                sleep(1)
                count += 1
                stdout.write(f'\rDownload in progress')
                stdout.flush()
            elif os.listdir(self.save_to)[0].endswith(".xlsx"):
                msg = '\rDownload completed successfully'
                return True, msg
            else:
                msg = '\rDownload failed!'
                return False, msg