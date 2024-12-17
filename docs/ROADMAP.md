## Clean & Green Philly 2025 Roadmap

### Overview

Welcome to the project roadmap for Clean & Green Philly! This is a living document that serves to outline the scope of what we intend to work on in the coming year. We intend to make quarterly updates to this document as the year progresses.

We launched v1.0.0 of [cleanandgreenphilly.org](https://www.cleanandgreenphilly.org/) in the spring of 2024. Since then, we have made substantial updates to our data pipeline, incorporating parcel-level data for every property in Philadelphia, while undertaking several months of user research and workshops to understand where we want to go next.

In 2025, we plan to begin taking advantage of our new data pipeline to pursue new analytical possibilities, and to implement the necessary updates to the website that we’ve identified through the user research process. At a high level, this will entail: 1) rebranding to more clearly articulate our aims as an organization and avoid confusion with the Mayor’s Office of Clean & Green Initiatives; 2) rewriting site content to align with the rebrand, as well as adding improved contact and donations pages; 3) focusing our front-end development on improved web and mobile accessibility for the cleanandgreenphilly.org site, 4) streamlining our data pipeline and adding improved data quality controls, 5) establishing more robust CI/CD, 6) exploring the possibility of using machine learning to identify vacant properties.

#### Organizational Rebrand 🎨

**Goal:** The Executive Director will recruit pro bono support to help Clean & Green Philly rebrand based on our strategic plan, in order to clearly articulate our aims as an organization and how we are distinct from other initiatives (especially the Mayor’s Office of Clean and Green Initiatives). This Code for Philly team will support the integration of this rebrand into the website as needed, e.g., by updating site content, graphics, colors, etc.  
**Key Actions:**

- Recruit pro bono technical support for branding, marketing, graphic design, content writing.
- Develop a branding kit with appropriate material for use in the newsletter, site, and elsewhere.
- Communicate new branding guidelines for use on the website; update the site accordingly.

#### Content Rewrite ✍️

**Goal:** Following the organizational rebrand, the Executive Director will secure support in writing new site content to ensure alignment with our rebrand and strategic plan. Additionally, new material is needed for technical documentation (e.g., a data dictionary and clearer explanations of data points like our “priority level” designation) and the “Transform” page.  
**Key Actions:**

- Identify and draft needed technical documentation (note that this will require some concerted thought based on comparable examples and best practices); mock and implement actual UI.
- Conduct user research and a comparative analysis to identify what content is missing on the website.
- Survey domain experts to identify content missing from Get Access and Transform pages.
- Recruit one or more content writers to update content for these pages.
- Coordinate with the UX team on mocking and implementation.
- Consider mocking and implementing/updating the following pages:
  - Contact
  - Donations
  - Grant opportunities for local organizations
  - A page listing organizations actively working on related initiatives

#### Improving Web and Mobile Accessibility 📱

**Goal:** In order to support less tech-saavy users, we will prioritize enhancements to web and mobile accessibility for cleanandgreenphilly.org.  
**Key Actions:**

- Build on the user journeys mapped out in the 2024 community workshop slides, adding these to the website to help guide new users.
- Create a tutorial for the “Find Properties” page using the [React Joyride guided tours package](https://github.com/gilbarbara/react-joyride).
- Implement fixes to pain points as identified by the UX team in our user workshops.
- Consider adding an “FAQ” page to the site, if needed.

#### Enhancing Data Pipeline ⚙️

**Goal:** Improve the maintainability and functionality of the data pipeline by improving code quality and adding better data quality control checks.  
**Key Actions:**

- Refactor the data pipeline to improve the maintainability of the codebase (considering using tools like `vulture` and `radon` for this purpose).
  - Relatedly:
    - https://github.com/CodeForPhilly/clean-and-green-philly/issues/717
    - https://github.com/CodeForPhilly/clean-and-green-philly/issues/706
- Add formal, consistent data quality controls using libraries like `dbt`, rather than our current ad hoc checks that exist in the pipeline.

#### Improving CI/CD 🚀

**Goal:** Improve our CI/CD process to reduce the workload on project leads and ensure the maintainability of the codebase.  
**Key Actions:**

- Add tests for key parts of the data pipeline, using a sample dataset stored on GitHub, or mocking data when necessary.
- Ensure that tests are integrated into the GitHub Actions workflows to prevent breaking code from being added to the codebase.
  - Along the way, address: https://github.com/CodeForPhilly/clean-and-green-philly/issues/830
- Eliminate redundant GitHub Actions workflows while also making sure that the remaining ones all function as intended.
- Review documentation to ensure that it is up to date and accurate.

#### Exploring ML 🧠

**Goal:** Explore the possibility of using ML with our dataset to identify vacant properties.  
**Key Actions:**

- Perform EDA to identify key features in the dataset associated with vacancy indicators.
- Explore basic modeling approaches (e.g., logit, RF) as proofs of concept to demonstrate the viability of using ML to identify vacant properties.
- Work with key stakeholders to identify scalable ways to supplant the City’s outdated vacancy by building our own model.
