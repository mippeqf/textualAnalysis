@REM # Use Snscrape, as I understand pretty much just a wrapper around Twitter's API
@REM # Goal is to predict tone or even the tone on certain topics
@REM # Using that information in turn to predict the market is only secondary (but still interesting)
@REM # SNScrape tutorial https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af

snscrape --jsonl --progress --max-results 1000 --since 2016-01-01 twitter-search "fomc" > data/twitter.json

@REM FIX ENCODING !!