import argparse
from .script import fetch_okx_announcements


def main():
    parser = argparse.ArgumentParser(description="OKX Announcements Scraper")
    parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format")
    parser.add_argument("folder", type=str, help="Folder path to save output")

    args = parser.parse_args()

    fetch_okx_announcements(args.start_date, args.end_date, args.folder)


if __name__ == "__main__":
    main()
