from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup headless browser options
options = Options()
options.headless = True

max_second = 10
max_cell = 10

# Load existing data if available
if os.path.exists("NhaDatHCM_temp.csv"):
    existing_data = pd.read_csv("NhaDatHCM_temp.csv")
    district = existing_data["Quận/Huyện"].tolist()
    street = existing_data["Tên đường/Làng xã"].tolist()
    from_to = existing_data["Đoạn: Từ - Đến"].tolist()
    VT1 = existing_data["VT1"].tolist()
    VT2 = existing_data["VT2"].tolist()
    VT3 = existing_data["VT3"].tolist()
    VT4 = existing_data["VT4"].tolist()
    VT5 = existing_data["VT5"].tolist()
    loai = existing_data["Loại"].tolist()
    index = existing_data["Trang"].tolist()
    start_page = existing_data["Trang"].max() + 1 # Start from the next page
else:
    district, street, from_to = [], [], []
    VT1, VT2, VT3, VT4, VT5, loai = [], [], [], [], [], []
    start_page = 1
    index = []

# Define a function to scrape data from a single page
def scrape_page(page_number):
    browser = webdriver.Chrome(options=options)
    url = f"https://thuvienphapluat.vn/page/BangGiaDat.aspx?city=32&district=0&street=0&pricerange=0-99999&typeland=&orderby=&typeorder=1&P={page_number}"
    browser.get(url)
    
    # Wait for table to load
    WebDriverWait(browser, max_second).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table")))
    
    rows = browser.find_elements(By.XPATH, "/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/table[2]/tbody/tr")
    
    page_data = {
        "Quận/Huyện": [],
        "Tên đường/Làng xã": [],
        "Đoạn: Từ - Đến": [],
        "VT1": [],
        "VT2": [],
        "VT3": [],
        "VT4": [],
        "VT5": [],
        "Loại": [],
        "Trang": []
    }

    for row in rows[1:]:  # Skip header row
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == max_cell:
            page_data["Quận/Huyện"].append(cells[1].text)
            page_data["Tên đường/Làng xã"].append(cells[2].text)
            page_data["Đoạn: Từ - Đến"].append(cells[3].text)
            page_data["VT1"].append(cells[4].text)
            page_data["VT2"].append(cells[5].text)
            page_data["VT3"].append(cells[6].text)
            page_data["VT4"].append(cells[7].text)
            page_data["VT5"].append(cells[8].text)
            page_data["Loại"].append(cells[9].text)
            page_data["Trang"].append(page_number)

    browser.quit()
    return page_data

# Scrape pages using multithreading
num_of_pages = 117  # Total number of pages to scrape
num_of_scrape = 10  # Total number of pages to scrape
end_page = min(start_page + num_of_scrape, num_of_pages)  # Adjust this number to scrape more or fewer pages at a time

all_data = {
    "Quận/Huyện": district,
    "Tên đường/Làng xã": street,
    "Đoạn: Từ - Đến": from_to,
    "VT1": VT1,
    "VT2": VT2,
    "VT3": VT3,
    "VT4": VT4,
    "VT5": VT5,
    "Loại": loai,
    "Trang": index
}

with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers based on your system capability
    futures = [executor.submit(scrape_page, i) for i in range(start_page, end_page)]
    for future in as_completed(futures):
        page_data = future.result()
        all_data["Quận/Huyện"].extend(page_data["Quận/Huyện"])
        all_data["Tên đường/Làng xã"].extend(page_data["Tên đường/Làng xã"])
        all_data["Đoạn: Từ - Đến"].extend(page_data["Đoạn: Từ - Đến"])
        all_data["VT1"].extend(page_data["VT1"])
        all_data["VT2"].extend(page_data["VT2"])
        all_data["VT3"].extend(page_data["VT3"])
        all_data["VT4"].extend(page_data["VT4"])
        all_data["VT5"].extend(page_data["VT5"])
        all_data["Loại"].extend(page_data["Loại"])
        all_data["Trang"].extend(page_data["Trang"])
        print(f"Page {page_data['Trang'][0]} done")

# Save data to CSV
df = pd.DataFrame(all_data)
df.to_csv(r"C:\Users\Admin\Desktop\python\Crawl data\Estate pricing\NhaDatHCM_temp.csv", index=False)
