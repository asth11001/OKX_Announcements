from setuptools import setup, find_packages

setup(
    name="okx_news_scraper",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pandas",
        "argparse"
    ],
    entry_points={
        "console_scripts": [
            "okx_scraper=okx_news_scraper.main:main"
        ]
    },
    author="AV",
    description="A web scraper for OKX announcements",
)
