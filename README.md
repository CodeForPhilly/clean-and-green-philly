# vacant-lots-proj

Gun crime x vacant lots mapping tool layer

# Setup Instructions

1. Install [pyenv](https://github.com/pyenv/pyenv) (or [pyenv-win](https://github.com/pyenv-win/pyenv-win) for Windows) for Python version management
2. Install the latest Python 3.11: `pyenv install 3.11.4`
3. Install [pipenv](https://github.com/pypa/pipenv) for environment management
4. Install project requirements: `pipenv install`

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

# awkde

We are using the [awkde package](https://github.com/mennthor/awkde) to create the Adaptive Width KDE. It is not available through pip. Install directly in the `src` folder using their instructions.

# Usage Instructions

1. Activate the pipenv shell: `pipenv shell`
2. Move the to src folder `cd src`
3. Run the main script `python script.py`

# Contribution Instructions

1. Create a fork of this repository and work from branches within your fork. When those changes are ready for review, create a pull request from fork:branch to upstream:main
2. Before committing changes, format your code to maintain a consistent codebase:
   ```
   pipenv shell
   black .
   ```
