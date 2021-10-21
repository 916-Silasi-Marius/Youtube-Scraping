# Youtube-Scraping

This is a Python algorithm for scraping the YouTube Platform using the YouTube API. The concept is pretty simple, you provide a list o comma separated keywords in the console and the program does the job.

For each individual run of the program, you will get 50-100 new YouTube channels per keyword that are linked in any way with the keyword you provided. This script simulates a basic YouTube search, acquires the channel IDs of the channels that posted the videos that showed up and starts gathering more data about every single channel.

The data consists in: 
 * Channel ID
 * Subscriber count
 * Last published video
 * Average views per video
 * Average likes per video
 * Average comments per video
 * Relevance
 * Posting frequency
 * Country
 * Instagram
 * Topics
 * Scrape Date
 * Scrape Keyword

The averages and relevance are calculated by a special formula, not just the basic average.
After gathering all this information, using the Google Sheet API, the data is stored in a Google Sheet.
There are some filters that are applied to the results, concerning video count, average views etc. The videos that do not pass this filter are stored in a separate Google Sheet.
Both the Google Sheets are evaluated before scraping to make sure all the results that we receive are 100% new channels that have not been scraped yet, so we do not have any duplicates in our databases.

# Running the script
