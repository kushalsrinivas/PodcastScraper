# podcastScraper Documentation

## Introduction

`podcastScraper` is a Python script designed to scrape data from podcasts hosted on Spotify and store relevant information in a Supabase database. This script extracts details such as episode number, name, description, and links from the specified podcast. The scraped data is then uploaded to a Supabase database for further analysis or use.

## Prerequisites

Before using the `podcastScraper`, make sure you have the following prerequisites installed:

- Python 3.x
- Requests library (`pip install requests`)
- Base64 library (included in Python standard library)
- JSON library (included in Python standard library)
- Urlextract library (`pip install urlextract`)
- Supabase Python client (`pip install supabase-py`)
- BeautifulSoup library (`pip install beautifulsoup4`)

## Configuration

To use the script, you need to provide your Spotify API client ID and client secret, as well as Supabase credentials. Make sure to replace the placeholder strings in the code with your actual values.

```python
clietn_id = "YOUR_SPOTIFY_CLIENT_ID"
client_secret = "YOUR_SPOTIFY_CLIENT_SECRET"
supabase: Client = create_client("YOUR_SUPABASE_URL", "YOUR_SUPABASE_KEY")
```

## Getting Spotify API Token

The script uses the Spotify API to fetch podcast details. To obtain an API token, you need to authenticate with your Spotify client ID and secret. The `get_token()` function retrieves the token, and the `get_authHeaders(token)` function generates the necessary authorization headers.

## Usage

1. Run the script in a Python environment.

```bash
python podcastScraper.py
```

2. Enter the show ID when prompted.

3. The script will fetch episode details from the specified Spotify podcast and print progress updates.

4. Once the scraping is complete, the data will be uploaded to the Supabase database.

## Script Details

### Functions

- `get_token()`: Retrieves the Spotify API token for authentication.
- `get_authHeaders(token)`: Generates authorization headers using the obtained token.
- `getLinks(htmlText)`: Extracts links from HTML text using BeautifulSoup.

### Main Workflow

1. Fetches the total number of episodes for the specified show.
2. Iteratively retrieves episode details in batches of 50 episodes until all episodes are fetched.
3. Extracts episode number, name, description, and links from each batch.
4. Uploads the scraped data to the Supabase database.

## Conclusion

`podcastScraper` simplifies the process of collecting podcast data from Spotify and storing it in a Supabase database. Feel free to customize the script for your specific use case or integrate additional functionalities.
