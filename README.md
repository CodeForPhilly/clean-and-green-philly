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

# Project Updates

**Oct. 2, 2023:** Met with the Philadelphia District Attorney's Office data analytics team. They are very excited about the dashboard and are connecting us with folks in the Managing Director's Office and the Civic Coalition to Save Lives.

**Sept. 29, 2023** Got our first funding from a donor! He's writing us a check to cover costs associated with user testing, hosting, domain name, etc., and will connet us with other folks who may be willing to give us more.

**Sept. 27, 2023** Nissim spoke with a reporter from WHYY who may be including our project in a longer piece about Philadelphians working on solutions to the gun violence crisis.

# Current Tasks

At the moment, we are working on:

- User testing with the prototype
- Finishing the Python script that creates the underlying dataset
- Building out the UI using Next.js and mapbox-gl in React

Current tasks for the are visible under the Issues section.

We also need non-technical help with researching and writing content for our Recommended Actions and About sections.

# Looking For

- Front end engineer w/mapping experience
- Python data engineer
- Non-technical support with research and writing
- Ditigal design support creating additional website graphics

# Languages/Frameworks

- React
- Next.js
- Tailwind CSS
- Python (data engineering)

# Codebase

This is a monorepo for both the nextjs app and the scripts which ETL and analyze the data.

## Data Scripts

All of the data scripting is in python and lives in the `data` folder. Everything below should be run in that folder.

#### Setup Instructions

1. Download [Docker](https://www.docker.com/products/docker-desktop/)

##### Database

1. Make sure postgres and postgis are installed
   - Follow the steps here: [Introduction to PostGIS](https://postgis.net/workshops/postgis-intro/installation.html)
2. Create a new databse
   `createdb vacantlotdb`
3. Connect to the db
   `psql vacantlotdb`
4. Enable postgis
   `CREATE EXTENSION postgis;`
5. Set your database connection string to an environment variable `VACANT_LOTS_DB`

Optionally, in `/config/config`, set `FORCE_RELOAD` = `False` to read "cached" data in postgres instead of downloading new data.

##### awkde

We are using the [awkde package](https://github.com/mennthor/awkde) to create the Adaptive Width KDE. It is not available through pip, but is handled as a part of the Docker build.

#### Usage Instructions

```shell
docker-compose up
```

Run the image in Docker. If needed, it will build (this will take a few minutes). It should only need to build if it's your first time running or if major configuation changes are made. Changes to the python script should not trigger a re-build. Linux users may run into a permissions error, in which case they should use `sudo docker-compose up`.

## Environment Variables

The following environment variables must be set:
`VACANT_LOTS_DB`: The local postgres URL for your database.
`VACANT_LOTS_DB_REMOTE`: The remote postgres URL for the hosted database.

You can choose to write to local, remote, both, or neither in the settings in `config.py`

## Nextjs App

Install dependencies with:

```bash
npm i
```

First, run the development server:

```bash
npm run dev
```

# Environment Variables

The following environment variables must be set:
`VACANT_LOTS_DB`: The local postgres URL for your database.
`NEXT_PUBLIC_VACANT_LOTS_API_BASE_URL`: Set this to `http://localhost:3000`.

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Contribution Instructions

1. Create a fork of this repository and work from branches within your fork. When those changes are ready for review, create a pull request from fork:branch to upstream:main
2. ~~Before committing changes, format your code to maintain a consistent codebase:~~ TODO: Figure out how to do this with Docker.

# License

MIT © Code for Philly
