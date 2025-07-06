# Clean & Green Philly

[Contributor Guide](/docs/CONTRIBUTING.md) | [Code of Conduct](/docs/CODE_OF_CONDUCT.md) | [Setup Instructions](/docs/SETUP/) | [Roadmap](/docs/ROADMAP.md)

🚨 Project Status

_Note: Clean & Green Philly ceased active development and maintainence in July of 2025. For more information, please see our [letter to stakeholders](/docs/PROJECT_BACKGROUND/C&GP%20Shutdown%20Letter,%20June%205,%202025.pdf) from July 2025. The website is still available at [cleanandgreenphilly.org](https://www.cleanandgreenphilly.org/) and the site, codebase, and data will remain available and open source for the foreseeable future._

Philadelphia has a gun violence problem. This dashboard aims to help solve it by empowering community groups to carry out cleaning and greening interventions in the vacant properties where they can have the biggest impact.

For more information on the research and data behind the project, please see the background information in [our docs](docs/).

## Data Access

All of our final output data, including final backups of the last reasonably valid vacant properties data, are available in [our `data` subdirectory](/data/backup_data/). There, you will find the backup vacant properties data, along with a GeoParquet file containing our last data outputs from July 2025 and a PMtiles dataset that we use for visualizing the vacant properties on the website. A README in the folder gives more context on the data.

Anyone interested in generating new data can simply install the codebase and run the pipeline via Docker, provided they bear in mind that everything _but_ the vacant properties data will be up to date.

## Project History

### 2025

**July 2025:** Clean & Green Philly ceases active development due to a lack of available data on vacant properties in Philadelphia.

**July 2025:** Clean & Green Philly publisheds v2.0, which incorporates data on all ~580,000 properties in Philadelphia.

**June 25, 2025:** Nissim and Amanda publish an op ed in _The Philadelphia Inquirer_ highlighting [the lack of official vacancy data](www.inquirer.com/opinion/commentary/mayor-parker-housing-plan-missing-data-20250625.html) and encourage the City to resume data collection.

### 2024

**October 22, 2024:** Nissim and Amanda publish an op ed in _The Philadelphia Citizen_ encouraging the City to [adopt our approach to strategically targeting vacant properties](https://thephiladelphiacitizen.org/guest-commentary-clean-and-green-philly-where-its-most-needed/).

**September 20, 2024:** Clean & Green Philly wins [HopePHL's "Great Idea" pitch competition](https://www.instagram.com/p/DAJg9SZprim/).

**June 2024:** The City of Philadelphia ceases to provide accurate vacancy data via the public API.

**May 1, 2024:** Clean & Green Philly won second place in the [36th annual NJ DEP Mapping Contest's](https://dep.nj.gov/gis/36th-mapping-contest/) Dashboard category!

**April 26, 2024:** On behalf of Clean & Green Philly, Nissim gave testimony to a Philadelphia City Council hearing on the uses of data and tech to reduce gun violence through place-based interventions. His statement is [available here](/docs/PROJECT_BACKGROUND/City%20Council%20Testimony%20Final,%20April%2026,%202024.pdf).

**April 21, 2024:** We have officially launched v1.0.0! The website is now live at [www.cleanandgreenphilly.org](https://www.cleanandgreenphilly.org/).

**Feb. 1, 2024:** We have soft launched a minimum viable product! The website is functional at [www.cleanandgreenphilly.org](https://www.cleanandgreenphilly.org/).

### 2023

**Nov. 15, 2023:** The Center for Philadelphia's Urban Future becomes our fiscal sponsor.

**June 2023:** Clean & Green Philly is launched as a Code for Philly project.

## License

MIT © Code for Philly

---

_This project was developed to address gun violence in Philadelphia through data-driven community interventions. While no longer actively maintained, we hope the code and data continue to benefit researchers and community organizations working on similar initiatives._
