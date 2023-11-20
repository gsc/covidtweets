from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from pandas import DataFrame
from requests import Response

from src.models.scraper_config import ScraperConfig

SCRAPER_PATH = "src.scraper"


@pytest.fixture(scope="session")
def scraper_config_instance() -> Generator[ScraperConfig, None, None]:
    yield ScraperConfig(url="http://localhost")


@pytest.fixture(scope="session")
def raw_tweets_df() -> DataFrame:
    return DataFrame.from_dict(
        {
            "value": {
                0: "RT: One morning, when # Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin.",
                1: '"What\'s happened to me?" he thought. http://www.ultimate.ai\n',
                2: "RT: Checkout this page: http://www.google.com",
                3: "### 123123 ###",
                4: "RT: # http://www.google.com #",
                5: "As https://as.com",
                6: "http://maven.com a https://as.com s http://aso.com ",
            }
        }
    )


@pytest.fixture(scope="session")
def clean_tweets_df() -> DataFrame:
    return DataFrame.from_dict(
        {
            "value": {
                0: "One morning, when  Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin.",
                1: '"What\'s happened to me?" he thought.',
                2: "Checkout this page:",
                3: "123123",
                4: "",
                5: "As",
                6: "a  s",
            }
        }
    )


@pytest.fixture(scope="function")
def mocked_requests_get_content() -> Generator[MagicMock, None, None]:
    with patch(f"{SCRAPER_PATH}.requests.get") as mocked_get:
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b"<div> a random text sequence </div>"
        mocked_get.return_value = mock_response
        yield mocked_get


@pytest.fixture(scope="function")
def mocked_requests_get() -> Generator[MagicMock, None, None]:
    with patch(f"{SCRAPER_PATH}.requests.get") as mocked_get:
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b"<div class='maincounter-number'><span> 545 </span></div>"
        mocked_get.return_value = mock_response
        yield mocked_get


@pytest.fixture(scope="function")
def mocked_requests_get_invalid_response() -> Generator[MagicMock, None, None]:
    with patch(f"{SCRAPER_PATH}.requests.get") as mocked_get:
        mock_response = Response()
        mock_response.status_code = 400
        mock_response._content = b"<div><span> a random text sequence </span></div>"
        mocked_get.return_value = mock_response
        yield mocked_get
