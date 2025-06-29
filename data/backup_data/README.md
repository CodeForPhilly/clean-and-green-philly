## Backup Data

This folder contains 1) backup vacant properties data from June 2024, the last time these data were reasonably accurate; and 2) the final outputs of our pipeline before project shutdown in July of 2025.

### Vacancy Data

The land backup file contains vacant land data sent to us by the Department of Licenses and Inspections, corresponding to the last reasonably complete dataset on vacant land prior to the City [no longer collecting vacany data](https://www.inquirer.com/opinion/commentary/mayor-parker-housing-plan-missing-data-20250625.html).

The buildings backup are data that we collected ourselves in June of 2024. They are likely missing about a thousand or more buildings, as we hadn't realized at the time that the buildings dataset was corrupted, too, but they are the best data we have available under the circumstances.

Combined, these represent about 34,000 properties. The pipeline is configured to run using these backup data unless the City's APIs suddenly start returning data above the expected threshold again.

### Pipeline Outputs

As it's currently confiured, the pipeline will return new data for everything _except_ the vacant properties themselves, for which it uses our June of 2024 backups. This means that all associated data are the currently-available numbers from their corresponding services, but we have no way to update the vacant properties data themselves. We have stored these here in both GeoParquet format (representing all 580,000+ properties in Philadelphia) and the PMtiles that we use to visualize vacant properties on the website (representing ~34,000 vacant properties from June of 2024, with the rest of the data from July of 2025).
