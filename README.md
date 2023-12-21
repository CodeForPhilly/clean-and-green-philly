# Clean & Green Philly

Philadelphia has a gun violence problem. This dashboard aims to help solve it by empowering community groups to carry out cleaning and greening interventions in the vacant properties where they can have the biggest impact.

# Motivation

Philadelphia has a gun violence problem. Homicides have been on the rise since 2013. The past three years—2020, 2021, and 2022—have been the deadliest on record, with a high of 562 homicides in 2021. Community members need solutions, but many city-run initiatives are frustratingly slow or inadequate. Nearly 80% of the city’s anti-violence spending focuses on long-term violence reduction without any clear, immediate impact.

Research shows that greening and cleaning vacant and abandoned parcels is one of the most impactful, cost-effective interventions available to reduce gun violence in a neighborhood. Drs. Eugenia South and Charles Branas have led several studies that [demonstrate that greening vacant lots in Philadelphia reduced gun violence by as much as 29% in the surrounding area](https://www.pnas.org/doi/10.1073/pnas.1718503115). Similarly, cleaning and lightly repairing vacant houses led a 13% drop in gun assaults compared to nearby blocks. These “greening and cleaning” interventions not only reduce gun violence but also provide other benefits, such as reducing the urban heat island effect, lowering residents’ stress levels, and contributing to lower levels of depression among residents.

There are roughly 40,000 vaccant properties in Philadelphia. Identifying the highest-priority vacant properties will allow community groups to invest their limited resources where they will have the biggest impact. Combining various public data, this dashboard helps users identify the properties that are ideal for them to intervene in. It also offers additional information about each property to facilitate interventions and indicates the best possible route to cleaning up the property.

# Current Draft

You can view [the current build of the website here](https://vacant-lots-proj.vercel.app/). We are building based off of a prototype which looks like this:

![User prototype landing page](https://github.com/CodeForPhilly/vacant-lots-proj/assets/111617674/0776acde-9fe0-42a5-b8ab-6680525a31d7)

![User prototype map](https://github.com/CodeForPhilly/vacant-lots-proj/assets/111617674/8cbf0b06-b299-49cd-8f9f-bbb714e55b44)

An older proptotype is also [available here](https://nlebovits.github.io/dashboard_demo_website/more_info.html), although it is now significantly out of date. 

Likewise, you can view the [very first iteration as an ArcGIS Storymap here](https://storymaps.arcgis.com/stories/551f77d85a584705b97c41db7711ba1b).


# Project Updates

**Nov. 15, 2023:** The Center for Philadelphia's Urban Future has officially voted to be a fiscal sponsor for our project and maintain it long-term. We are working with them to assemble a steering committee that will help inform future development of the web tool.

**Oct. 2, 2023:** Met with the Philadelphia District Attorney's Office data analytics team. They are very excited about the dashboard and are connecting us with folks in the Managing Director's Office and the Civic Coalition to Save Lives.

**Sept. 29, 2023** Got our first funding from a donor! He's writing us a check to cover costs associated with user testing, hosting, domain name, etc., and will connet us with other folks who may be willing to give us more.

**Sept. 27, 2023** Nissim spoke with a reporter from WHYY who may be including our project in a longer piece about Philadelphians working on solutions to the gun violence crisis.

# Current Tasks

At the moment, we are working on:

- User testing with the prototype
- Finishing the Python script that creates the underlying dataset
- Building out the UI using Next.js and mapbox-gl in React
- Research and writing content for our Recommended Actions and About sections

Current tasks for the are visible under the Issues section.

# Looking For

- Front end engineer w/mapping experience
- Python data engineer
- Non-technical support with research and writing
- Ditigal design support creating additional website graphics
- Support for project documentation

# Languages/Frameworks

- React
- Next.js
- Tailwind CSS
- Python (data engineering)

# Codebase

This is a monorepo for both the nextjs app and the scripts which ETL and analyze the data.

# Contribution

Please see [`CONTRIBUTING.md`](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/CONTRIBUTING.md) for instructions on how to contribute, and [`SETUP.md`](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/SETUP.md) for instructions on how to install and work on the code.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nlebovits"><img src="https://avatars.githubusercontent.com/u/111617674?v=4?s=100" width="100px;" alt="Nissim Lebovits"/><br /><sub><b>Nissim Lebovits</b></sub></a><br /><a href="#doc-nlebovits" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

# License

MIT © Code for Philly
