from pandas import DataFrame


def cleanup_tweets(df: DataFrame):
    url_regexp = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"

    df.value = df.value.str.replace(url_regexp, "", regex=True)
    df.value = df.value.str.replace("#", "")
    df.value = df.value.str.replace("RT:", "")
    df.value = df.value.str.strip()
    return df
