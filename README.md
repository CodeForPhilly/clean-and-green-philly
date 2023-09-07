# Clean & Green Philly

Philadelphia has a gun violence problem. This dashboard aims to help solve it by empowering community groups to carry out cleaning and greening interventions in the vacant properties where they can have the biggest impact.

# Motivation

Philadelphia has a gun violence problem. Homicides have been on the rise since 2013. The past three years—2020, 2021, and 2022—have been the deadliest on record, with a high of 562 homicides in 2021. Community members need solutions, but many city-run initiatives are frustratingly slow or inadequate. Nearly 80% of the city’s anti-violence spending focuses on long-term violence reduction without any clear, immediate impact.

Research shows that greening and cleaning vacant and abandoned parcels is one of the most impactful, cost-effective interventions available to reduce gun violence in a neighborhood. Drs. Eugenia South and Charles Branas have led several studies that [demonstrate that greening vacant lots in Philadelphia reduced gun violence by as much as 29% in the surrounding area](https://www.pnas.org/doi/10.1073/pnas.1718503115). Similarly, cleaning and lightly repairing vacant houses led a 13% drop in gun assaults compared to nearby blocks. These “greening and cleaning” interventions not only reduce gun violence but also provide other benefits, such as reducing the urban heat island effect, lowering residents’ stress levels, and contributing to lower levels of depression among residents.

There are roughly 40,000 vaccant properties in Philadelphia. Identifying the highest-priority vacant properties will allow community groups to invest their limited resources where they will have the biggest impact. Combining various public data, this dashboard helps users identify the properties that are ideal for them to intervene in. It also offers additional information about each property to facilitate interventions and indicates the best possible route to cleaning up the property.

# Current Draft

You can view the [most recent prototype of the website and dashboard](https://nlebovits.github.io/dashboard_demo_website/more_info.html), which was created in Quarto.

Currently we are in the process of user testing a newer prototype, which looks like this:

![User prototype landing page](https://github.com/CodeForPhilly/vacant-lots-proj/assets/111617674/0776acde-9fe0-42a5-b8ab-6680525a31d7)

![User prototype map](https://github.com/CodeForPhilly/vacant-lots-proj/assets/111617674/8cbf0b06-b299-49cd-8f9f-bbb714e55b44)

# Current Tasks

At the moment, we are working on:

- User testing with the prototype
- Finishing the Python script that creates the underlying dataset

Current tasks for the Python script are visible under the Issues section.

In September, we hope to begin turning our attention to building the dashboard and website, which will be built in React JS.

# Looking For

- Front end engineer w/mapping experience
- Python data engineer

# Languages/Frameworks

- React
- Nextjs
- Tailwind
- Python (data engineering)

### Codebase

This is a monorepo for both the nextjs app and the scripts which ETL and analyze the data.

## Data Scripts

All of the data scripting is in python and lives in the `data` folder. Everything below should be run in that folder.

# Setup Instructions

1. Install [pyenv](https://github.com/pyenv/pyenv) (or [pyenv-win](https://github.com/pyenv-win/pyenv-win) for Windows) for Python version management
  * [troubleshooting for `pyenv_win` downloadn and script permissions](https://www.sharepointdiary.com/2014/03/fix-for-powershell-script-cannot-be-loaded-because-running-scripts-is-disabled-on-this-system.html)
2. Install the latest Python 3.11: `pyenv install 3.11.4`
3. Install [pipenv](https://github.com/pypa/pipenv) for environment management
4. Install project requirements: `pipenv install`
   * *Note*: run this from the following directory: `[whever you have this repo locally]\vacant-lots-proj\data` 
   * A virtual environment will be created in this directory and the packages from the Pipfile will be installed.

# Database

1. Make sure postgres and postgis are installed
   TODO: Add instructions here
2. Create a new databse
   `createdb vacantlotdb`
3. Connect to the db
   `psql vacantlotdb`
4. Enable postgis
   `CREATE EXTENSION postgis;`
5. Set your database connection string to an environment variable `VACANT_LOTS_DB`

Optionally, in `/config/config`, set `FORCE_RELOAD` = `False` to read "cached" data in postgres instead of downloading new data.

# awkde

We are using the [awkde package](https://github.com/mennthor/awkde) to create the Adaptive Width KDE. It is not available through pip. To install, navigate to `src` and run

```
pip install -e ./awkde
```

# Usage Instructions

1. Activate the pipenv shell: `pipenv shell`
2. Move the to src folder `cd src`
3. Run the main script `python script.py`

# Mapbox

To upload to Mapbox through the API you'll need a key with `upload` write access, saved to the environment variable `CFP_MAPBOX_TOKEN_UPLOADER`

## Nextjs App

Install dependencies with:

```bash
npm i --legacy-peer-deps
```

First, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Contribution Instructions

1. Create a fork of this repository and work from branches within your fork. When those changes are ready for review, create a pull request from fork:branch to upstream:main
2. Before committing changes, format your code to maintain a consistent codebase:
   ```
   pipenv shell
   black .
   ```

# License

MIT © Code for Philly
