# Project Technologies

## Overview

This document is mean to summarize all of the various technologies and tools used across the Clean & Green Philly project, encompassing both
frontend, backend, ETL pipeline, devops/infrastructure, and miscellaneous tools. The following will include a brief description of each technology
as well as its function within our project as well as links to external resource to help new contributors familiarize themselves.

## Frontend

### Next.js

Our frontend web app is built with the Next.js framework, which is a React-based framework with additional, opinionated solutions for how to accomplish
common web application tasks including routing, data fetching, optimizations for serving media files, and a range of other features. The best place to learn more about Next.js is directly on their [docs](https://nextjs.org/docs).

### React

React is the frontend, Javascript library that Next.js itself is built around. It is built around the philosophy of separating portions of a web application's visual design and functionality into separate chunks known as **components**, which can combined and reuse in modular ways across the application. You can read more about React on its [docs](https://react.dev/reference/react).

### Tailwind

We use Tailwind as our CSS framework, which is an increasing popular for styling in modern web applications. You can read more on their [docs](https://v3.tailwindcss.com/docs/installation). Clean & Green Philly currently uses Tailwind v3 as opposed to the most recently released v4, which includes some major design differences, so be sure you are referencing the correct portion of the docs.

### Eslint and Prettier

For linting and formatting, we use the standard solutions of ESLint and Prettier.

ESLint - https://eslint.org/docs/latest/

Prettier - https://prettier.io/docs/

Because the overlap in roles for linting and formatters can be quite close, be sure to reference the integration docs about the interaction between the two technologies [here](https://prettier.io/docs/integrating-with-linters).

### Maplibre

The primary functionality of our web application is the interactive map to view vacant properties across Philadelphia. We achieve that using the Maplibre GL library, which is an open source Typescript library for rendering maps based on vector tile information in the browser environment. We supply the library with the primary feature information for visualization from our data pipeline and Maplibre GL creates an interactive map with zoom, panning, selection, and other capabilities.

There are two documentation sources to note - the original library which includes all of the original Typescript classes and objects for interacting with the map and `react-map-gl`, a library of React component that wrap that functionality and allow them to be included in React-based applications with declarative style.

Maplibre GL - https://maplibre.org/maplibre-gl-js/docs/

React Maplibre - https://visgl.github.io/react-map-gl/docs/api-reference/maplibre/map

## ETL Pipeline

### Python

All our data sourcing and pipeline code is written in Python. It's likely already installed on any particular contributors computer, but you can find documentation for installation and other resources on the main site [here](https://www.python.org/doc/). Keep in mind we use specific Python versioning within the project that you will need to adhere to using other tooling mentioned later in this document and the setup details.

You can find a lightweight refresher of basic syntax and concetps across the language at [w3schools](https://www.w3schools.com/python/) or more in-depth and comprehensive discussion on the main [docs](https://docs.python.org/3/).

### Geopandas

As we are working with geospatial data and sourcing and transforming it in various ways, we use the main Python-based, open source library for working with such data - `geopandas`. It is an extension on the popular `pandas` framework that allwos you to organize data into flexible `DataFrame` objects for easy manipulation and transformation as well as adding additional support for geographic objects in the `GeoSeries` and `GeoDataFrame` types. The documentation is available [here](https://geopandas.org/en/stable/docs.html).

### File Formatting - Geoparquet, PMTiles, tippiecanoe

We use a variety of file types for storage of the end dataset constructed by the ETL pipeline. The most common format for encoding geospatial data is GeoJSON, which stores the geometry and other information in a familiar JSON format. However, because this is inefficient for loading and fetching client-side in our web application, we convert to several other file formats for better performance.

The first are PMtiles, which is a single-file vector tile format for geospatial data. It's main benefit is that it, as a single file, encompasses all vector tiles are each zoom level for our data, and so it can be hosted in our Google Cloud Bucket and simply fetched from by Maplibre rather than needing a more complex backend or querying solution as an intermediary. More information can be found [here](https://docs.protomaps.com/pmtiles/).

The second are GeoParquet files, which are a geospatial addition to Apache Parquet files. Their benefit is they are a highly performant way to compress and store columnar data, and they have useful mechanisms for self-describing and partitioning the data within the file itself for faster retrieval and querying in the future. We are in the process of shifting the majority of our storage into this format and phasing out the Postgres-based service we have previously been using, which is mentioned below. You can find out more.

### Python version and dependency management - Pipenv - Pyenv

We manage our Python dependencies using `pipenv` which mantains them through the `Pipfile` and `Pipfile.lock`. Our Python versioning is managed through Docker when running the main script, but if you were interested in doing local development, you can also pin your python version to 3.11.4 using `pyenv`.

`pipenv` - https://pipenv.pypa.io/en/latest/

`pyenv` - https://github.com/pyenv/pyenv

### Postgres - Postgis - Timescale (SOON DEPRECATED)

### Vulture

###

## Devops - CI/CD - Infrastructure

### Docker - Docker Compose

Docker is a container tool that is used for creating an isolated and controllable environment to run our code that is replicable across different machines. Our ETL pipeline runs inside what is referred to as a **container** in Docker, which manages the versioning and dependencies of everything we use in our repo as well as ensuring it interfaces with a standardized operating system within the container's virtualized environment.

You can read more about in the Docker docs [here](https://docs.docker.com/), and the easiest way to get setup with using Docker is Docker Desktop with installation instructions [here](https://docs.docker.com/desktop/).

### Google Cloud

All of the data produced by our pipeline needs to be stored somewhere for access from our web application, and we do so with a Google Cloud bucket that holds the geospatial data as well as street view images to be served up request from the site. In addition, we have a Google Cloud Compute Engine (VM) setup to run our pipeline on a regularly scheduled interval to update our data.

Google Cloud is a broad platform and subject with a lot of details, but those interested in learning more or taking on any infrastructure tasks that crop up in the future can learn more on their [docs](https://cloud.google.com/docs).

### Github Actions

For our CI/CD, we use Github Action for a number of workflows to manage incoming pull requests, labelling issues and assigning reviews, and generating automated releases. Some of those workflows need additional correction and revision in their current form, which we are getting to, but they can be found in the `.github` directory of the repo.

Documentation for possible tasks accomplished by Github actions and writing them is [here](https://docs.github.com/en/actions).
