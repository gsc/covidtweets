import pytest
from pandas import DataFrame


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
