import pytest

from src.scraper import Scraper, ScraperError


@pytest.mark.usefixtures("mocked_requests_get", "scraper_config_instance")
def test_scraper(mocked_requests_get, scraper_config_instance):
    scraper = Scraper(scraper_config_instance, None)
    res = scraper.get_covid_cases()
    assert res == 545


@pytest.mark.usefixtures("mocked_requests_get_invalid_response", "scraper_config_instance")
def test_scraper_invalid_response(mocked_requests_get_invalid_response, scraper_config_instance):
    scraper = Scraper(scraper_config_instance, None)
    with pytest.raises(ScraperError) as excinfo:
        scraper.get_covid_cases()
    assert (
        str(excinfo.value)
        == "Didn't managed to retrieve the number of covid cases. Response code 400"
    )


@pytest.mark.usefixtures("mocked_requests_get_content", "scraper_config_instance")
def test_scraper_invalid_content(mocked_requests_get_content, scraper_config_instance):
    scraper = Scraper(scraper_config_instance, None)
    with pytest.raises(ScraperError) as excinfo:
        scraper.get_covid_cases()
    assert (
        str(excinfo.value)
        == "Couldn't find the number of covid cases in the page retrieved. Perhaps the site has changed?"
    )
