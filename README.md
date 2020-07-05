## Overview
Goal of this repo is to beautiful soup + statsroyale.com to do some analytics for clash royale.

### Structure 
```
Royale-Scrape/
├── README.md
└── notebooks
    ├── Royale\ Scrape\ I\ -\ Carter.ipynb
    ├── Royale\ Scrape\ II\ -\ Carter.ipynb
    ├── clash_royale.xlsx
    └── clash_royale2020-07-05.xlsx
```
- Notebooks
	- Royale Scrape II
		- Tracking card popularity (potentially as a metric for trading #TODO)
	- Royale Scrape I
		- Scraping user data from keys
		- Built Joint DataFrame (as a way to suggest trades between 2 players)
	- clash\_royale.xlsx
		- Excel dataframe to hold all individual dataframe
		- Note Royale Scrape I, these are time sensitive
