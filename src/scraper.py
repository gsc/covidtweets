import requests
from bs4 import BeautifulSoup

from src.models.scraper_config import ScraperConfig


class ScraperError(Exception):
    pass


class Scraper:
    def __init__(self, scraper_config: ScraperConfig, spark_logger):
        self.url = scraper_config.url
        self.spark_logger = spark_logger

    def get_covid_cases(self) -> int:
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            total_cases_element = soup.find("div", {"class": "maincounter-number"})
            num = total_cases_element.span.text.strip().replace(",", "")
            return int(num)
        else:
            raise ScraperError(
                f"Didn't managed to retrieve the number of covid cases. Response code {response.status_code}"
            )
