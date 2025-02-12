import os
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def fetch_okx_announcements(start_date: str, end_date: str, folder: str):
    """
    Fetch OKX announcements using web scraping within a given date range
    and save to a CSV file.

    Parameters:
    start_date (str): Start date in format YYYY-MM-DD
    end_date (str): End date in format YYYY-MM-DD
    folder (str): Folder path to save the output csv file
    """

    announcements = []
    base_url = "https://www.okx.com/help/section/announcements-latest-announcements/page/{}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(base_url.format(1), headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to retrieve. HTTP Status Code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    pagination_elem = soup.find("ul",
                                class_="okui-pagination")
    if pagination_elem:
        page_links = pagination_elem.find_all("a", attrs={"data-testid": "okd-pagination-pager"})
        page_numbers = [int(link.get("data-e2e-okd-pagination-pager", "1"))
                        for link in page_links
                        if link.get("data-e2e-okd-pagination-pager") and
                        link.get("data-e2e-okd-pagination-pager").isdigit()]
        max_pages = max(page_numbers)
    else:
        max_pages = 1

    for page in range(1, max_pages):
        response = requests.get(base_url.format(page), headers=headers,
                                timeout=10)
        if response.status_code != 200:
            print(f"Failed on page {page}. Status: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("li", class_="index_articleItem__d-8iK")

        if not articles:
            print("No more announcements found.")
            break

        for item in articles:
            title_elem = item.find("div", class_="index_title__iTmos")
            date_elem = item.find("span", attrs={"data-testid": "DateDisplay"})
            link_elem = item.find("a")

            if not title_elem or not date_elem or not link_elem:
                continue

            title = title_elem.text.strip()
            link = "https://www.okx.com" + link_elem["href"]
            date_str = date_elem.text.strip()
            date_part = date_str.replace("Published on ", "")
            # Convert to datetime object and format to Y-m-d
            date_obj = datetime.strptime(date_part, "%b %d, %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            # Check if the announcement falls within the date range
            if start_date <= formatted_date <= end_date:
                announcements.append({
                    "Title": title,
                    "Link": link,
                    "Date": formatted_date
                })
    # Ensure folder exists
    os.makedirs(folder, exist_ok=True)
    output_path = os.path.join(folder, "okx_announcements.csv")
    # Save to csv
    if announcements:
        df = pd.DataFrame(announcements)
        df.to_csv(output_path, index=False)
        print(f"Saved {len(announcements)} announcements to {output_path}")
    else:
        print("No announcements found within the date range.")
