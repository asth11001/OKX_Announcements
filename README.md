# OKX Announcements Scraper

## Overview
This Python script scrapes the latest announcements from the OKX exchange's help section and saves them in a structured CSV file within a specified date range. The script utilizes web scraping with `BeautifulSoup` and handles pagination dynamically to ensure all relevant announcements are retrieved.

## Features
- Scrapes OKX announcements from the official website
- Filters announcements based on a given date range
- Saves data into a CSV file for easy processing
- Includes timeout handling to prevent indefinite requests

## Requirements
Make sure you have Python installed (recommended version 3.9 or later). Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Installation
To install the scraper as a package, navigate to the project directory and run:

```bash
pip install .
```

## Usage
Run the script with the following command:

```bash
python script.py <start_date> <end_date> <folder>
```

For example, to scrape announcements from January 1, 2025, to February 1, 2025, and save them in the `./data` directory:

```bash
python script.py 2025-01-01 2025-02-01 ./data
```

Alternatively, if installed as a package:

```bash
okx_scraper 2025-01-01 2025-02-01 ./data
```

## Running in Docker
To containerize and run the scraper in a Docker environment:

1. Build the Docker image:
   ```bash
   docker build -t okx_scraper .
   ```
2. Run the container:
   ```bash
   docker run okx_scraper 2025-01-01 2025-02-01 ./data
   ```

## Known Issues & Considerations
- The scraper relies on the current HTML structure of the OKX website. If the structure changes, the script may need updates.
- Some remote servers may block repeated scraping attempts. Consider using proxies or rate-limiting requests.
- Ensure that the output folder has appropriate permissions for saving files.

## License
This project is licensed under the MIT License.

## Contact
For issues or feature requests, please create an issue in the project repository or reach out via email.
