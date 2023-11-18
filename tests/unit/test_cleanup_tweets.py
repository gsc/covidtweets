import pytest
from pandas.testing import assert_frame_equal

from src.source.cleanup_tweets import cleanup_tweets


@pytest.mark.usefixtures("raw_tweets_df", "clean_tweets_df")
def test_cleanup_tweets(raw_tweets_df, clean_tweets_df):
    res = cleanup_tweets(raw_tweets_df)
    assert_frame_equal(res, clean_tweets_df)
