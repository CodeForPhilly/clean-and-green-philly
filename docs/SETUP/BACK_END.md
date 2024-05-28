# Setup Instructions

## Overview

If you are planning to contribute to the data wrangling and database management on this project and will need to run the Python script, follow the installation and setup instructions below.

## Installation

### Docker

Docker is a platform that allows you to containerize and run applications in isolated environments, making it easier to manage dependencies and ensure consistent deployments. Download the [latest version of Docker Desktop for your operating system](https://www.docker.com/products/docker-desktop/).

### PostgreSQL

PostgreSQL is an open-source relational database management system. We use it to store and our data. Make sure you have the latest version of PostgreSQL installed on your computer. You can download it [here](https://www.postgresql.org/download/). As part of that setup, you will also need to install PostGIS; this should be done through the setup wizard, [as detailed here](https://postgis.net/workshops/postgis-intro/installation.html).

## Setup

### Fork the Repository

1. Navigate to [our GitHub repository](https://github.com/CodeForPhilly/vacant-lots-proj).
2. Create a fork of the repository by clicking the "Fork" button in the top right corner of the page. This will create a copy of the repository in your own GitHub account.
3. Clone your fork of the repository to your local machine using `git clone`.

Note: make sure to keep your fork up to date with the original repository by following the instructions [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo#keep-your-fork-synced).

### Create a New Database

#### Windows

1. Using powershell, navigate to the directory where PostgreSQL is installed. You can do this with a command like cd `"C:\Program Files\PostgreSQL\13\bin"` (replace 13 with your PostgreSQL version). Run `./psql -U postgres`. Enter your computer password.
2. Run `CREATE DATABASE vacantlotdb;` to create a new database named `vacantlotdb`.
3. Run `\c vacantlotdb` to connect to the database.
4. Run `CREATE EXTENSION postgis;`.
5. Run `\q` to exist PostgreSQL.

### Linux

1. Ensure that PostgreSQL is installed and running on your Mac.
2. In your terminal, run `createdb vacantlotdb`. This command directly creates a new database named `vacantlotdb`.
3. Run `psql -U postgres -d vacantlotdb`. Enter the password when prompted. This command opens the PostgreSQL command line interface and connects you to the `vacantlotdb` database.
4. Run `CREATE EXTENSION postgis;`
5. Run `\q` to exit the PostgreSQL command line interface.

### macOS

1. Ensure that PostgreSQL is installed and running on your Mac.
2. In your terminal, run `createdb vacantlotdb`. This command directly creates a new database named `vacantlotdb`.
3. Run `psql -d vacantlotdb`. Note that you might need to start postgres on mac: `brew services start postgresql` before running psql If prompted, enter the password for your PostgreSQL user. This will open the PostgreSQL command line interface and connect you to the `vacantlotdb` database. You will know it’s succeeded when you see `vacantlotdb=#`
4. Run `CREATE EXTENSION postgis;`
5. To exit the PostgreSQL interface, type `\q` and press Enter.

Note for all OS: Optionally, in `/config/config`, set `FORCE_RELOAD` = `False` to read "cached" data in postgres instead of downloading new data.

### Set Environment Variables

#### Windows

Open the command prompt as an admin. Run `setx VACANT_LOTS_DB "postgresql://postgres:password@localhost/vacantlotdb"`. Make sure to replace “password” with your user password (not your postgres password). You should get a message saying something like “Success! Specified value was saved.”

#### Linux

In the terminal, open your shell's profile file, like `~/.bashrc` or `~/.bash_profile`, using a text editor. You should be able to do this by running something like `nano ~/.bashrc`. Add the following lines at the end of the file:
`export VACANT_LOTS_DB="postgresql://postgres:password@localhost/vacantlotdb"`
Replace `password` with your PostgreSQL user password. Save and close the file. Apply the changes by running `source ~/.bashrc`.

#### macOS

In the terminal, open your shell's profile file, such as `~/.zshrc` (for Zsh, which is the default shell on recent versions of macOS) or `~/.bash_profile` (for Bash), using a text editor like Nano or Vim. For instance, `nano ~/.zshrc`. Add the following lines at the end of the file
`export VACANT_LOTS_DB="postgresql://postgres:password@localhost/vacantlotdb"`
Make sure to replace `password` with your actual PostgreSQL password. Save and close the file. To apply these changes, run `source ~/.zshrc` (or the appropriate file for your shell).

Note for all OS: you can choose to write to local, remote, both, or neither in the settings in `config.py`

### Docker Build

All of the data scripting is in python and lives in the `data` folder. Everything below should be run in that folder.

For all three OS, you'll first have to go into the `data` subdirectory and open the `docker-compose.yml` file. Change the filepath under `volumes` to the location of your repository. (Currently it is hardcoded to Brandon's filepath.)
For example, if your repository is located at `user/Documents/vacant-lots-proj`, you would change the filepath to `user/Documents/vacant-lots-proj/data`. Save and close the file. Alternatively, you can run the image in Docker following the steps below. If needed, it will build (this will take a few minutes). It should only need to build if it's your first time running or if major configuation changes are made. Changes to the python script should not trigger a re-build.

#### Windows

1. Make sure Docker is running by opening the Docker Desktop app.
2. Open the command prompt. Navigate to the location of the `vacant-lots-proj` repository. Run `cd data` and then `docker-compose run vacant-lots-proj`.
3. When the script is done running, you’ll get a notification. When you’re done, to shut up off the Docker container (which uses memory), run `docker-compose down`.

#### Linux

1. In the terminal, navigate to your repository location using `cd path/to/repository`. Then run `cd data` to move into the `data` directory.
2. Run `sudo docker-compose run vacant-lots-proj`. Enter your password if requested. If you run into an error message related to "KEY_ID" or something like similar, you may have to do the following:

- Hard-code your VACANT_LOTS_DB variable in `docker-compose.yml`.
- Also in `docker-compose.yml`, add `extra_hosts: -"host.docker.internal:host-gateway"`
- In your `postgresql.conf` file, set `listen_addresses = '*'` in
- In your `pg_hba.conf` file, add the following new lines: `host all all 10.0.0.0/24 md5` and `host all postgres 172.18.0.2/32 trust`. You may have to modify these based on your own IP address.
- Finally, after restarting postgres, navigate back to the `data` subdirectory in the project and run `docker-compose --verbose up -d`. This should run successfuly; message

The backend also works on WSL Ubuntu running Docker for Linux on Windows 10.

3. When you're finished, and you want to shut down the Docker container, run `docker-compose down`.

#### macOS

In the terminal, use the `cd` command to navigate to your repository location, and then into the `data` directory. Run `docker-compose run vacant-lots-proj`. This command starts Docker Compose and sets up your environment as defined in your `docker-compose.yml` file. When you're finished and want to shut down the Docker containers, run `docker-compose down`.

#### Making code changes

Changes to our codebase should always address an [issue](https://github.com/CodeForPhilly/vacant-lots-proj/issues) and need to be requested to be merged by submitting a pull request that will be reviewed by at least the team lead or tech lead.

#### Formatting

Format all python files by running:

```
docker-compose run formatter
```

#### Google Cloud (GCP)

The map data is converted to the [pmtiles](https://docs.protomaps.com/pmtiles/) format and served from Google Cloud. For access to production credentials, contact the project lead.

You can run the tile build locally with `docker-compose run vacant-lots-proj` to create a tile file and upload it to your own GCP bucket.  First, create your own GCP account using their free trial.  You will need to create the following assets in your GCP account and configure them in the environment variables in docker-compose.yml:
- Under APIs and Services -> Credentials, create an API key and put that in the CLEAN_GREEN_GOOGLE_KEY variable
- Under APIs and Services -> Credentials, create a service account.  After you create the service account you will download the service account private key file named like encoded-keyword-ddd-xxx.json.  Copy that to ~/.config/gcloud/application_default_credentials.json.  This path is specified by default in the volumes section of the docker compose file.
- Go to Cloud storage -> Buckets and create a new bucket.  Name it logically, e.g. cleanandgreenphl-{your_initials}.  It has to be globally unique.  Grant access to at least write to the bucket to your service account.  Put your bucket name in the GOOGLE_CLOUD_BUCKET_NAME variable.  Make sure the tiles file in your bucket is publicly accessible by following Google's instructions online.

The python script loads the tiles to Google Cloud as `vacant_properties_tiles_staging.pmtiles`. You can check this tileset by changing the config setting on the frontend `useStagingTiles` to `true`. If the tiles look OK, manually change the name in Google Cloud to remove the `_staging` and archive the previous copy.

#### Google Streetview

To update streetview images, after running the full data script run:

```
docker-compose run streetview
```

The script should only load new images that aren't in the bucket already (new properties added to list).

#### Backup and difference reporting
Whenever the data load script is run in refresh mode, the old data set is backed up and a report of any differences is sent to the team via Slack.  Differences in data are calculated using the [data-diff](https://github.com/datafold/data-diff) package. See [issue 520](https://github.com/CodeForPhilly/clean-and-green-philly/issues/520) in Github.

Backups are done in PostgreSQL in the vacantlotsdb database by copying the whole public schema to a backup schema named backup_{timestamp}.  Besides the original tables, the backup schema includes a '{table_name}_diff' table with details of the differences from data-diff for each table.

Backup schemas are only kept for one year by default.  Backup schemas older than a year are deleted at the end of the load script.

When a diff is performed, an html file of the contents of the '{table_name}_diff' table is generated for each table and uploaded to the public GCP bucket so it can be viewed in a web browser.  The location of the html files is in the format: https://storage.googleapis.com/cleanandgreenphl/diff/2{backup_timestamp}/{table_name}.html  The link to the detail diff page is included in the Slack report message.

The `CAGP_SLACK_API_TOKEN` environmental variable must be set with the API key for the Slack app that can write messages to the channel as configured in the config.py `report_to_slack_channel` variable.

The report will also be emailed to any emails configured in the config.py `report_to_email` variable.
