import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

year, pos,driver,nationality, car, pts = [], [], [], [], [], []

for i in range (datetime.datetime.now().year,1949,-1):
    page = requests.get(f"https://www.formula1.com/en/results.html/{i}/drivers.html")
    content = BeautifulSoup(page.text, "html.parser")
    table = content.find("table", class_="resultsarchive-table")
    rows = table.find_all("tr")
    
    for row in rows:
        columns = row.find_all("td")
        if columns:
            year.append(i)
            pos.append(columns[1].text.strip())
            driver_ = columns[2].text.strip().split("\n")
            driver.append(' '.join(driver_[:-1]))
            nationality.append(columns[3].text.strip())
            car.append(columns[4].text.strip())
            pts.append(columns[5].text.strip())
df = pd.DataFrame({
    "Position": pos,
    "Driver": driver,
    "Nationality": nationality,
    "Car": car,
    "Points": pts,
    "Year": year
}).to_csv(r"C:\Users\Admin\Desktop\python\Crawl data\F1\F1.csv", index=False)