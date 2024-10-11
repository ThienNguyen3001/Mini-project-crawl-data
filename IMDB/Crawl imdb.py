from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()

url = "https://www.imdb.com/chart/top/"
driver.get(url)

titles = []
publish_years = []
times = []
movie_types = []
ratings = []
vote_counts = []

# Tìm tất cả các mục phim
movie_repo = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item__tc')

for movie in movie_repo:
    title = movie.find_element(By.CLASS_NAME, 'ipc-title__text').text.strip()
    metadata_items = movie.find_elements(By.CLASS_NAME, 'sc-ab348ad5-8.cSWcJI.cli-title-metadata-item')
    publish_year = metadata_items[0].text.strip() if len(metadata_items) > 0 else None
    time = metadata_items[1].text.strip() if len(metadata_items) > 1 else None
    movie_type = metadata_items[2].text.strip() if len(metadata_items) > 2 else None
    rating = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--rating').text.strip()
    vote_count = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--voteCount').text.strip()

    titles.append(title)
    publish_years.append(publish_year)
    times.append(time)
    movie_types.append(movie_type)
    ratings.append(rating)
    vote_counts.append(vote_count)

driver.quit()

df = pd.DataFrame({
    "Title": titles,
    "Publish year": publish_years,
    "Time": times,
    "Movie type": movie_types,
    "Rating": ratings,
    "Vote count": vote_counts
}).to_csv("IMDB\IMDB_top_chart.csv", index=False)

print('Crawl done')
