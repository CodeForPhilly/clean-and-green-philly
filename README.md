# Clean & Green Philly

Philadelphia has a gun violence problem. This dashboard aims to help solve it by empowering community groups to carry out cleaning and greening interventions in the vacant properties where they can have the biggest impact.

## Motivation

Philadelphia has a gun violence problem. Homicides have been on the rise since 2013. The past three years—2020, 2021, and 2022—have been the deadliest on record, with a high of 562 homicides in 2021. Community members need solutions, but many city-run initiatives are frustratingly slow or inadequate. Nearly 80% of the city’s anti-violence spending focuses on long-term violence reduction without any clear, immediate impact.

Research shows that greening and cleaning vacant and abandoned parcels is one of the most impactful, cost-effective interventions available to reduce gun violence in a neighborhood. Drs. Eugenia South and Charles Branas have led several studies that [demonstrate that greening vacant lots in Philadelphia reduced gun violence by as much as 29% in the surrounding area](https://www.pnas.org/doi/10.1073/pnas.1718503115). Similarly, cleaning and lightly repairing vacant houses led a 13% drop in gun assaults compared to nearby blocks. These “greening and cleaning” interventions not only reduce gun violence but also provide other benefits, such as reducing the urban heat island effect, lowering residents’ stress levels, and contributing to lower levels of depression among residents.

There are roughly 40,000 vaccant properties in Philadelphia. Identifying the highest-priority vacant properties will allow community groups to invest their limited resources where they will have the biggest impact. Combining various public data, this dashboard helps users identify the properties that are ideal for them to intervene in. It also offers additional information about each property to facilitate interventions and indicates the best possible route to cleaning up the property.

## Current Draft

You can view [the current build of the website here](https://www.cleanandgreenphilly.org/). We are building based off of a prototype which looks like this:

![User prototype landing page](https://github.com/CodeForPhilly/vacant-lots-proj/assets/111617674/0776acde-9fe0-42a5-b8ab-6680525a31d7)

![User prototype map](https://github.com/CodeForPhilly/vacant-lots-proj/assets/111617674/8cbf0b06-b299-49cd-8f9f-bbb714e55b44)

An older proptotype is also [available here](https://nlebovits.github.io/dashboard_demo_website/more_info.html), although it is now significantly out of date.

Likewise, you can view the [very first iteration as an ArcGIS Storymap here](https://storymaps.arcgis.com/stories/551f77d85a584705b97c41db7711ba1b).

## Project Updates

**Feb. 1, 2024:** We have soft launched a minimum viable product! The website is functional at [www.cleanandgreenphilly.org](https://www.cleanandgreenphilly.org/).

**Nov. 15, 2023:** The Center for Philadelphia's Urban Future has officially voted to be a fiscal sponsor for our project and maintain it long-term. We are working with them to assemble a steering committee that will help inform future development of the web tool.

**Oct. 2, 2023:** Met with the Philadelphia District Attorney's Office data analytics team. They are very excited about the dashboard and are connecting us with folks in the Managing Director's Office and the Civic Coalition to Save Lives.

**Sept. 29, 2023** Got our first funding from a donor! He's writing us a check to cover costs associated with user testing, hosting, domain name, etc., and will connet us with other folks who may be willing to give us more.

**Sept. 27, 2023** Nissim spoke with a reporter from WHYY who may be including our project in a longer piece about Philadelphians working on solutions to the gun violence crisis.

## Current Tasks

At the moment, we are working on:

- Organizing a steering committee of stakeholders to guide future project development
- Improving the accessibility and responsiveness of our MVP
- Improving the content and design of our Take Action pages
- Laying groundwork to apply for a grant to support our work

Current tasks for the are visible under the [Issues](https://github.com/CodeForPhilly/vacant-lots-proj/issues) section.

## Looking For

- An experienced developer to lead our front-end work and coordinate with our UX team
- A graphic designer to work on content for the website
- Someone with grant-writing expertise

## Languages/Frameworks

- React
- NextJS
- Tailwind CSS
- Python (data engineering)

## Codebase

This is a single repository for both the React app and the Python pipeline to ETL the data.

## Contribution

Please see the documents in our [DOCS](/DOCS) folder for background on the project and instructions on how to contribute. At a minimum, please read:

1) The [guide to contributing](/DOCS/CONTRIBUTING.md)
2) The [code of conduct](/DOCS/CODE_OF_CONDUCT.md)
3) The appropriate installation setup instructions ([front end](/DOCS/SETUP/FRONT_END.md), [back end](/DOCS/SETUP/BACK_END.md), or [full stack](/DOCS/SETUP/FULL_SETUP.md))


### Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nlebovits"><img src="https://avatars.githubusercontent.com/u/111617674?v=4?s=100" width="100px;" alt="Nissim Lebovits"/><br /><sub><b>Nissim Lebovits</b></sub></a><br /><a href="#doc-nlebovits" title="Documentation">📖</a> <a href="#code-nlebovits" title="Code">💻</a> <a href="#content-nlebovits" title="Content">🖋</a> <a href="#data-nlebovits" title="Data">🔣</a> <a href="#fundingFinding-nlebovits" title="Funding Finding">🔍</a> <a href="#maintenance-nlebovits" title="Maintenance">🚧</a> <a href="#projectManagement-nlebovits" title="Project Management">📆</a> <a href="#research-nlebovits" title="Research">🔬</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://kedgard-cordero.netlify.app"><img src="https://avatars.githubusercontent.com/u/97119018?v=4?s=100" width="100px;" alt="Kedgard Cordero"/><br /><sub><b>Kedgard Cordero</b></sub></a><br /><a href="#code-Kenny4297" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/brandonfcohen1"><img src="https://avatars.githubusercontent.com/u/2308834?v=4?s=100" width="100px;" alt="Brandon Cohen"/><br /><sub><b>Brandon Cohen</b></sub></a><br /><a href="#code-brandonfcohen1" title="Code">💻</a> <a href="#doc-brandonfcohen1" title="Documentation">📖</a> <a href="#infra-brandonfcohen1" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jroper-scottlogic"><img src="https://avatars.githubusercontent.com/u/125047199?v=4?s=100" width="100px;" alt="Jack Roper"/><br /><sub><b>Jack Roper</b></sub></a><br /><a href="#code-jroper-scottlogic" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://coroflot.com/willonabike"><img src="https://avatars.githubusercontent.com/u/1652510?v=4?s=100" width="100px;" alt="Will"/><br /><sub><b>Will</b></sub></a><br /><a href="#research-willonabike" title="Research">🔬</a> <a href="#design-willonabike" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/thansidwell"><img src="https://avatars.githubusercontent.com/u/1965986?v=4?s=100" width="100px;" alt="Nathaniel Sidwell"/><br /><sub><b>Nathaniel Sidwell</b></sub></a><br /><a href="#design-thansidwell" title="Design">🎨</a> <a href="#research-thansidwell" title="Research">🔬</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/marvieqa"><img src="https://avatars.githubusercontent.com/u/102739972?v=4?s=100" width="100px;" alt="Marvie Mulder"/><br /><sub><b>Marvie Mulder</b></sub></a><br /><a href="#a11y-marvieqa" title="Accessibility">️️️️♿️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://markandrewgoetz.com"><img src="https://avatars.githubusercontent.com/u/4121678?v=4?s=100" width="100px;" alt="Mark Goetz"/><br /><sub><b>Mark Goetz</b></sub></a><br /><a href="#code-markgoetz" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/tracyctran/"><img src="https://avatars.githubusercontent.com/u/7329799?v=4?s=100" width="100px;" alt="Tracy Tran"/><br /><sub><b>Tracy Tran</b></sub></a><br /><a href="#a11y-bacitracin" title="Accessibility">️️️️♿️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://elizabethwalker.site"><img src="https://avatars.githubusercontent.com/u/44076192?v=4?s=100" width="100px;" alt="Elizabeth Walker"/><br /><sub><b>Elizabeth Walker</b></sub></a><br /><a href="#code-19ewalker" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://alexbyrdleitner-portfolio.netlify.app/"><img src="https://avatars.githubusercontent.com/u/111008425?v=4?s=100" width="100px;" alt="Alex Byrd-Leitner"/><br /><sub><b>Alex Byrd-Leitner</b></sub></a><br /><a href="#code-AZBL" title="Code">💻</a> <a href="#a11y-AZBL" title="Accessibility">️️️️♿️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/gturmel"><img src="https://avatars.githubusercontent.com/u/16137908?v=4?s=100" width="100px;" alt="Greg Turmel"/><br /><sub><b>Greg Turmel</b></sub></a><br /><a href="#code-gturmel" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://paulchoi.dev"><img src="https://avatars.githubusercontent.com/u/8061917?v=4?s=100" width="100px;" alt="Paul Choi"/><br /><sub><b>Paul Choi</b></sub></a><br /><a href="#code-paulhchoi" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Amberroseweeks"><img src="https://avatars.githubusercontent.com/u/61482332?v=4?s=100" width="100px;" alt="Amberroseweeks"/><br /><sub><b>Amberroseweeks</b></sub></a><br /><a href="#code-Amberroseweeks" title="Code">💻</a> <a href="#a11y-Amberroseweeks" title="Accessibility">️️️️♿️</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

MIT © Code for Philly

