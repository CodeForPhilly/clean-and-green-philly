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
