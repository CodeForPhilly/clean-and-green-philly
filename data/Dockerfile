# Use an official Python 3.11 runtime as a parent image
FROM python:3.11.4

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies for GDAL
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV GDAL_VERSION=3.2.1
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Install Pipenv
RUN pip install pipenv

# Copy the content of the local src directory to the working directory
COPY src/ .

# Install the dependencies from Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Install awkde within the Pipenv environment
# Assuming awkde is located in /usr/src/app/awkde
WORKDIR /usr/src/app/awkde
RUN pipenv run pip install .

# Change back to the original working directory
WORKDIR /usr/src/app

# Use Pipenv to run the script
# Adjust the path to your main Python script if needed
CMD ["pipenv", "run", "python", "./script.py"]
