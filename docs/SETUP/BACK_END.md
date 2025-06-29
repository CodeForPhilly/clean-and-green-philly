# Setup Instructions

## Overview

If you plan to contribute to the data wrangling on this project and need to run the Python script, follow the installation and setup instructions below.

## Setup

### Fork and Clone

1. Navigate to [our GitHub repository](https://github.com/CodeForPhilly/clean-and-green-philly).
2. Create a fork of the repository by clicking the "Fork" button in the top right corner of the page.
3. Clone your fork of the repository to your local machine using `git clone`.

**Note:** Keep your fork up to date with the original repository by following the instructions [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo#keep-your-fork-synced).

### Install Dependencies and Pre-commit Hooks

1. Navigate to the root directory and install the virtual environment and dependencies:

   ```sh
   uv sync
   ```

2. Install pre-commit hooks for code quality and commit message validation:

   ```sh
   uv run pre-commit install
   ```

3. Copy the commit message hook file to ensure conventional commit format validation:

   **Windows Command Prompt:**

   ```cmd
   copy .github\hooks\commit-msg .git\hooks\
   ```

   **Mac/Linux/Git Bash:**

   ```bash
   cp .github/hooks/commit-msg .git/hooks/
   chmod +x .git/hooks/commit-msg
   ```

> **Note:** All commits must follow the Conventional Commits format: `<type>[optional scope]: <description>`
>
> Valid types: feat, fix, docs, style, refactor, test, chore, ci, perf, build
>
> Examples:
>
> - `fix: resolve data fetching issue`
> - `feat(FilterView): add new method for conditional filtering`
> - `docs: update the pull request template`

### Environment Variables

Copy the `data/.env.example` file to `data/.env` and fill in your actual values:

```sh
cp data/.env.example data/.env
```

Then edit `data/.env` with your specific credentials for Google Cloud Platform and Slack integration.

All environment variables will be automatically passed through to Docker containers.

### Docker Setup

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) for your operating system.

2. Build the Docker services (run from the `data/` directory):

   ```sh
   cd data
   docker compose build
   ```

3. Run the main pipeline:

   ```sh
   docker compose run vacant-lots-proj
   ```

4. When finished, shut down containers:
   ```sh
   docker compose down
   ```

**Note:** For first-time runs, set `FORCE_RELOAD=True` in `config.py` and optionally `log_level: int = logging.DEBUG` for verbose output.

## Python Development

You can develop and run the backend `script.py` and unit tests outside of Docker using your local Python environment:

1. Install the same Python version as defined in the `Dockerfile` (3.11.4)
2. Use `uv` to create a virtual environment and install dependencies from `pyproject.toml`
3. Run unit tests with `pytest`

For testing individual services:

```sh
cd data
uv run test_service.py [name_of_service]
# Example: uv run test_service.py opa_properties
```

The `config.py` file defines several log levels for testing the pipeline, including profiling, geometry debugging, and verbose output.

## Configuration

Configuration variables are defined in `data/src/config/config.py`. See the documentation in that file for each variable.

### Required Secrets

The following secrets may be shared by project leads:

- **Google Cloud credentials** for accessing the cloud platform
- **Slack API key** for posting diff reports to the project Slack

For development, you can set up your own GCP account and Slack bot for testing.

### Code Changes and Formatting

- Changes should address an [issue](https://github.com/CodeForPhilly/vacant-lots-proj/issues)
- Submit pull requests for review by team lead or tech lead
- Format Python files:
  ```sh
  docker compose run --rm vacant-lots-proj sh -c "ruff format"
  ```

## Google Cloud Platform (GCP)

The map data is converted to the [pmtiles](https://docs.protomaps.com/pmtiles/) format and served from Google Cloud. For access to production credentials, contact the project lead.

You can run the tile build locally with `docker compose run vacant-lots-proj` to create a tile file and upload it to your own GCP bucket. First, create your own GCP account using their free trial. You will need to create the following assets in your GCP account and configure them in the environment variables in the `.env` file:

1. Under APIs and Services -> Credentials, create an API key and put that in the CLEAN_GREEN_GOOGLE_KEY variable.
2. Under APIs and Services -> Credentials, create a service account. After you create the service account you will download the service account private key file named like encoded-keyword-ddd-xxx.json. Copy that to `~/.config/gcloud/application_default_credentials.json`. This path is specified by default in the volumes section of the docker compose file.
3. Go to Cloud storage -> Buckets and create a new bucket. Name it logically, e.g. cleanandgreenphl-{your_initials}. It has to be globally unique. Grant access to at least write to the bucket to your service account. Put your bucket name in the GOOGLE_CLOUD_BUCKET_NAME variable. Make sure the tiles file in your bucket is publicly accessible by following Google's instructions online.

Your `/data/.env` file should now look like this:

```sh
CLEAN_GREEN_GOOGLE_KEY=your-api-key-here
GOOGLE_CLOUD_BUCKET_NAME=your-bucket-name-here
```

The python script loads the tiles to Google Cloud as `vacant_properties_tiles_staging.pmtiles`. You can check this tileset by changing the config setting on the frontend `useStagingTiles` to `true`. If the tiles look OK, manually change the name in Google Cloud to remove the `_staging` and archive the previous copy.

##### Converting PMTiles to Vector Data

Pmtiles stored in the cloud or locally can be converted back to a vector dataset (e.g., GeoJson) by using [tippecanoe](https://github.com/mapbox/tippecanoe) in the terminal: `tippecanoe-decode -c vacant_properties_tiles.pmtiles > vacant_properties_tiles.geojson`. (Note that this can likely be done in the Docker container to avoid installing a local copy of tippecanoe, but we haven't explored this yet.)

#### Google Streetview

To update streetview images, after running the full data script run:

```sh
docker compose run streetview
```

The script should only load new images that aren't in the bucket already (new properties added to list).

#### Backup and difference reporting

Whenever the data load script is run in force reload mode, the old data set is backed up and a report of any differences is sent to the team via Slack. Differences in data are calculated using the [data-diff](https://github.com/datafold/data-diff) package. See [issue 520](https://github.com/CodeForPhilly/clean-and-green-philly/issues/520) in Github.

Backup schemas are only kept for one year by default. Backup schemas older than a year are deleted at the end of the load script.

After all runs of the back-end script, the tiles file is backed up to the backup/ directory in the GCP bucket with a timestamp. If the main tiles file ever gets corrupted, it can be rolled back to a backup file.

When a diff is performed, an html file of the contents of the '{table_name}\_diff' table is generated for each table and uploaded to the public GCP bucket so it can be viewed in a web browser. The location of the html files is in the format: https://storage.googleapis.com/cleanandgreenphl/diff/{backup_timestamp}/{table_name}.html The link to the detail diff page is included in the Slack report message.

The `CAGP_SLACK_API_TOKEN` environmental variable must be set with the API key for the Slack app that can write messages to the channel as configured in the config.py `report_to_slack_channel` variable.

The report will also be emailed to any emails configured in the config.py `report_to_email` variable.
