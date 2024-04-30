# Clean & Green Philly Summer 2024 Roadmap

## 🗓 Roadmap Overview

Welcome to the project roadmap for Clean & Green Philly! After launching v1.0.0 in spring of 2024, we will spend the summer shifting our focus from frontend tasks to building out a more robust data pipeline and a project CI/CD workflow. We will still continue to work on front end stuff, but will have a more balanced distribution across all parts of the project, while also gathering input through user research.

## Front End

### 🌐 Relevant Organizations Page

- **Goal:** Create a page listing organizations actively working on related initiatives.
- **Key Actions:**
  - Research and compile a list of relevant organizations.
  - Design and develop the webpage to display this information in an accessible format.

### 📝 Grant Writing Opportunities

- **Goal:** Provide a comprehensive list of grant writing opportunities for local organizations.
- **Key Actions:**
  - Identify and list potential grant sources.
  - Connect users to detailed grant writing resources and guides.

## Dataset Enhancements

### 🔢 Development Risk Indicator

- **Goal:** Add a development risk metric based on building permits per census block.
- **Key Actions:**
  - Calculate a z-scored count of building permits issued in the past year per census block.
  - Scale the data from high to low, noting the approximation to avoid a false appearance of precision.

### 📊 Tangled Titles Model

- **Goal:** Develop a model to identify properties with tangled titles.
- **Key Actions:**
  - Reach out to Pew about getting their dataste on tangled titles.
  - Build and implement a predictive model to identify potential tangled titles in our dataset dataset.

### 🏗 Negligent Developers Data

- **Goal:** Include data on negligent developers in our dataset.
- **Key Actions:**
  - Define what constitutes negligent development.
  - Implement a workflow to identify likely cases of negligent developers in our dataset.

## Back-End

### 📦 Containerization

- **Goal:** Containerize the entire backend setup to improve deployment efficiency and allow for migration to Google Cloud Services (GCS).
- **Key Actions:**
  - Build out a Dockerfile to run the entire ETL pipeline in the cloud.
  - Deploy the container to GCS.

### ☁️ Porting to Google Cloud

- **Goal:** Migrate our pipeline to Google Cloud.
- **Key Actions:**
  - Automate data updates with scheduled cloud functions to refresh our dataset monthly.
  - Document migration steps and best practices for future reference.

### 🧪 Implementing Data Quality Tests

- **Goal:** Implement data quality assurance measures using tools like `dbt`.
- **Key Actions:**
  - Define data quality metrics and tests.
  - Integrate `dbt` into our data processing pipelines.
  - Schedule and monitor data quality checks to ensure continuous data integrity.

### 🔄 Setting Up CI/CD

- **Goal:** Establish a Continuous Integration/Continuous Deployment (CI/CD) workflow to streamline development and deployment.
- **Key Actions:**
  - Develop CI/CD pipelines using GitHub Actions including automated testing, building, and deployment.

### 📧 Automated Stakeholder Communication

- **Goal:** Automate the process of sending targeted email updates to stakeholders such as Habitat for Humanity about new, eligible properties.
- **Key Actions:**
  - Set up email triggers in our system to send out monthly updates.
  - Customize email content based on stakeholder interest and relevance.
