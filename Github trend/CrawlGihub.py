import requests
from bs4 import BeautifulSoup
import pandas as pd

developer, repoName, descr, language, total_stars, forks, stars_today = [], [], [], [], [], [], []

page = requests.get("https://github.com/trending")
content = BeautifulSoup(page.text, "html.parser")

repos = content.find_all(class_="Box-row")

for repo in repos:
    # Lấy thông tin developer và repo name
    developer_and_repo = repo.find("h2", class_="h3 lh-condensed").text.strip()
    slash_index = developer_and_repo.find('/')
    developer.append(developer_and_repo[:slash_index].strip())
    repoName.append(developer_and_repo[slash_index+1:].strip())

    # Lấy mô tả của repo
    description_tag = repo.find("p", class_="col-9 color-fg-muted my-1 pr-4")
    descr.append(description_tag.text.strip() if description_tag else "No description")

    # Lấy ngôn ngữ sử dụng trong repo
    language_tag = repo.find(attrs={"itemprop": "programmingLanguage"})
    language.append(language_tag.text.strip() if language_tag else "Unknown")
    
    # Lấy số sao tổng cộng
    total_stars_tag = repo.find(lambda tag: tag.name == "a" and "stargazers" in tag.get("href", ""))
    total_stars.append(total_stars_tag.text.strip().split()[0] if total_stars_tag else "0")
    
    # Lấy số forks
    forks_tag = repo.find(lambda tag: tag.name == "a" and "forks" in tag.get("href", ""))
    forks.append(forks_tag.text.strip().split()[0] if forks_tag else "0")
    
    # Lấy số sao hôm nay
    stars_today_tag = repo.find("span", class_="d-inline-block float-sm-right")
    stars_today.append(stars_today_tag.text.strip().split()[0] if stars_today_tag else "0")
    
df = pd.DataFrame({
    "Developer": developer,
    "Repo name": repoName,
    "Description": descr,
    "Language": language,
    "Total stars": total_stars,
    "Forks": forks,
    "Stars today": stars_today
}).to_csv("github_trending.csv", index=False)
