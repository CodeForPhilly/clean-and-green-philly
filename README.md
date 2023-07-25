# vacant-lots-proj
Gun crime x vacant lots mapping tool layer

# Setup Instructions
1. Install [pyenv](https://github.com/pyenv/pyenv) (or [pyenv-win](https://github.com/pyenv-win/pyenv-win) for Windows) for Python version management
2. Install the latest Python 3.11: `pyenv install 3.11.4`
3. Install [pipenv](https://github.com/pypa/pipenv) for environment management
4. Install project requirements: `pipenv install`

# Usage Instructions
1. Activate the pipenv shell: `pipenv shell`
2. Run the main script: `python process_data.py [output_filename]`

# Contribution Instructions
1. Create a fork of this repository, and work from branches in your fork. When those changes are ready for review, please create a pull request from fork:branch to upstream:main.
2. Before committing changes, format your code to maintain a consistent codebase: 
    ```
    pipenv shell
    black .
    ```
