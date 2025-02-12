import os
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def process_announcement(item):
    """Extracts title, link, and date from an announcement item."""
    title_elem = item.find("div", class_="index_title__iTmos")
    date_elem = item.find("span", attrs={"data-testid": "DateDisplay"})
    link_elem = item.find("a")

    if not title_elem or not date_elem or not link_elem:
        return None

    title = title_elem.text.strip()
    link = "https://www.okx.com" + link_elem["href"]
    date_str = date_elem.text.strip().replace("Published on ", "")

    try:
        date_obj = datetime.strptime(date_str, "%b %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None

    return {"Title": title, "Link": link, "Date": formatted_date}


def fetch_okx_announcements(start_date: str, end_date: str, folder: str):
    """
    Fetch OKX announcements using web scraping within a given date range
    and save to a CSV file.

    Parameters:
    start_date (str): Start date in format YYYY-MM-DD
    end_date (str): End date in format YYYY-MM-DD
    folder (str): Folder path to save the output CSV file
    """

    announcements = []
    base_url = "https://www.okx.com/help/section/announcements-latest-announcements/page/{}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    # First request to determine max pages
    response = requests.get(base_url.format(1), headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to retrieve. HTTP Status Code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract maximum pages
    pagination_elem = soup.find("ul", class_="okui-pagination")
    max_pages = 1
    if pagination_elem:
        page_links = pagination_elem.find_all("a", attrs={"data-testid": "okd-pagination-pager"})
        page_numbers = [
            int(link.get("data-e2e-okd-pagination-pager"))
            for link in page_links
            if link.get("data-e2e-okd-pagination-pager", "").isdigit()
        ]
        if page_numbers:
            max_pages = max(page_numbers)

    # Iterate through pages
    for page in range(1, max_pages + 1):
        response = requests.get(base_url.format(page), headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed on page {page}. Status: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("li", class_="index_articleItem__d-8iK")

        if not articles:
            print("No more announcements found.")
            break

        # Process each announcement
        for item in articles:
            announcement = process_announcement(item)
            if announcement and start_date <= announcement["Date"] <= end_date:
                announcements.append(announcement)

        # Early exit if all announcements on this page are outside the date range
        if announcements and announcement["Date"] < start_date:
            break

    # Ensure folder exists
    os.makedirs(folder, exist_ok=True)
    output_path = os.path.join(folder, "okx_announcements.csv")

    # Save to CSV
    if announcements:
        df = pd.DataFrame(announcements)
        df.to_csv(output_path, index=False)
        print(f"Saved {len(announcements)} announcements to {output_path}")
    else:
        print("No announcements found within the date range.")
