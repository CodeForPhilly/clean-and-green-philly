import { Accordion, AccordionItem, Button, Link } from "@nextui-org/react";
import { get } from "http";

import AboutPageImage from "./AboutIPageImage";

const image=[{
  src: "/annual_guncrimes_plot.png",
  alt: "Vacant lot in Philadelphia",
},]
export default function AboutPage() {
  const defaultContent =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.";

    const motivationContent = (
    <><div className="flex">
        <p className="text-2xl mb-4">
          Philadelphia has a gun violence problem. Homicides have been on the rise since 2013.
          The past three years—2020, 2021, and 2022—have been the deadliest on record, with a high of 562 homicides in 2021.
          Community members need solutions, but many city-run initiatives are frustratingly slow or inadequate.
          Nearly 80% of the city’s anti-violence spending focuses on long-term violence reduction without any clear, immediate impact.
        </p>
      </div>
      <div className="object-center w-50 h-50">
          {image.map(({ src, alt }) => (
            <AboutPageImage
              key={src}
              src={src}
              alt={alt} />
          ))}
        </div></>
    );
   

    const researchContent = (
      <p className="text-2xl mb-4">
      Research shows that greening and cleaning vacant and abandoned parcels is one of the most impactful,
      cost-effective interventions available to reduce gun violence in a neighborhood.
      Drs. Eugenia South and Charles Branas have led several studies that demonstrate that greening vacant lots in Philadelphia reduced gun violence
      by as much as 29% in the surrounding area. Similarly, cleaning and lightly repairing vacant houses led a 13% drop in gun assaults compared to nearby blocks.
      These “greening and cleaning” interventions not only reduce gun violence but also provide other benefits, such as reducing the urban heat island effect,
      lowering residents’ stress levels, and contributing to lower levels of depression among residents.
    </p>
    );

    const methodologyContent = (
      <p className="text-2xl mb-4">
      This map combines data on vacant and abandoned properties from the Department of Licenses and Inspections
      with Philadelphia Police Department data on gun violence. Additional datasets from a variety of other sources
      provide more information about each parcel, such as what neighborhood it falls in and whether it’s in the PHS Community LandCare
      or Philadelphia LandCare programs.
      <br></br>
      The basic methodology is as follows. First, crime data were filtered to include only gun crimes (reported as “aggravated assault firearm”
      and “robbery firearm” by PPD) in the past year. This follows the research upon which the dashboard is based. These points were then used to
      calculate a <a href="https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-kernel-density-works.htm" className="text-blue-500 hover:underline">kernel density estimate</a>,
      which indicates the intensity of gun crime at any point in space. The KDE was then extracted to each vacant parcel to indicate the local level of gun violence.
      Finally, to make the gun crime rates easier to understand, each parcel was classified by the percentile into which its gun crime score falls.
      Those interested in a more in-depth understanding of how this map was produced can view the Python code behind the dataset in this GitHub repository.
    </p>
    );

    const attributionContent = (
      <p className="text-2xl mb-4">
        This dashboard was built by Nissim Lebovits. He is a master's student in city planning at the University of Pennsylvania's Weitzman School of Design,
        where he focuses on environmental planning and spatial analysis. He's interested in using data to foster civic engagement and build more sustainable,
        inclusive cities. Previously he was an AmeriCorps VISTA with the City of Philadelphia, where he worked to support residents of the West Philadelphia Promise Zone.
        For questions about this dashboard, to see more of his work, or to hire him to support your community organization's data work, please see his website.
      </p>
    );

    const acknowledgementsContent = (
      <p className="text-2xl mb-4">
        Many people helped inform this tool, including residents, CDC leaders, City staff, Penn faculty, and more. Special thanks, however,
        are due to Dante Leonard for facilitating countless valuable conversations with people throughout Philadelphia, to Mjumbe Poe
        for serving as my independent study instructor while I built the JavaScript dashboard and website, to Vicky Tam for teaching the GIS class
        in which I built the first functional version of this tool, and to Dr. Eugenia South for spearheading the original research upon which this tool is based.
      </p>
    );


  return (
    <div className="container mx-auto pt-20 h-screen">
      <h1 className="text-4xl font-bold mb-8">About</h1>

      <Accordion variant="light" defaultExpandedKeys={["1"]}>

      <AccordionItem key="1" aria-label="Motivation" title="Motivation" className="font-bold text-large">
      <div className="text-base font-normal">
        {motivationContent}
      </div>
      </AccordionItem>

      <AccordionItem key="2" aria-label="Research" title="Research" className="text-3xl font-bold mt-4">
      <div className="text-base font-normal">
        {researchContent}
      </div>
      </AccordionItem>

      <AccordionItem key="3" aria-label="Methodology" title="Methodology" className="text-3xl font-bold mt-4">
      <div className="text-base font-normal">
        {methodologyContent}
      </div>
      </AccordionItem>

      <AccordionItem key="4" aria-label="Attribution" title="Attribution" className="text-3xl font-bold mt-4">
      <div className="text-base font-normal">
        {attributionContent}
      </div>
      </AccordionItem>

      <AccordionItem key="5" aria-label="Acknowledgements" title="Acknowledgements" className="text-3xl font-bold mt-4">
      <div className="text-base font-normal">
        {acknowledgementsContent}
      </div>
      </AccordionItem>

      </Accordion>

      <div className="mt-4"></div> {/* Add extra space here */}

    </div>
  );
}


/*
const AboutPage = () => (
  <div className="container mx-auto pt-20 h-screen grid grid-cols-1 sm:grid-cols-2 gap-8">
    <div className="text-left my-10">
      <h1 className="text-3xl font-bold mb-4">About</h1>

      <h2 className="text-2xl font-bold mt-4">Motivation</h2>
      <p className="text-2xl mb-4">
        Philadelphia has a gun violence problem. Homicides have been on the rise since 2013.
        The past three years—2020, 2021, and 2022—have been the deadliest on record, with a high of 562 homicides in 2021.
        Community members need solutions, but many city-run initiatives are frustratingly slow or inadequate.
        Nearly 80% of the city’s anti-violence spending focuses on long-term violence reduction without any clear, immediate impact.
      </p>

      <h2 className="text-2xl font-bold mt-4">Research</h2>
      <p className="text-2xl mb-4">
        Research shows that greening and cleaning vacant and abandoned parcels is one of the most impactful,
        cost-effective interventions available to reduce gun violence in a neighborhood.
        Drs. Eugenia South and Charles Branas have led several studies that demonstrate that greening vacant lots in Philadelphia reduced gun violence
        by as much as 29% in the surrounding area. Similarly, cleaning and lightly repairing vacant houses led a 13% drop in gun assaults compared to nearby blocks.
        These “greening and cleaning” interventions not only reduce gun violence but also provide other benefits, such as reducing the urban heat island effect,
        lowering residents’ stress levels, and contributing to lower levels of depression among residents.
      </p>

      <h2 className="text-2xl font-bold mt-4">Methodology</h2>
      <p className="text-2xl mb-4">
        This map combines data on vacant and abandoned properties from the Department of Licenses and Inspections
        with Philadelphia Police Department data on gun violence. Additional datasets from a variety of other sources
        provide more information about each parcel, such as what neighborhood it falls in and whether it’s in the PHS Community LandCare
        or Philadelphia LandCare programs.
        <br></br>
        The basic methodology is as follows. First, crime data were filtered to include only gun crimes (reported as “aggravated assault firearm”
        and “robbery firearm” by PPD) in the past year. This follows the research upon which the dashboard is based. These points were then used to
        calculate a <a href="https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-kernel-density-works.htm" className="text-blue-500 hover:underline">kernel density estimate</a>,
        which indicates the intensity of gun crime at any point in space. The KDE was then extracted to each vacant parcel to indicate the local level of gun violence.
        Finally, to make the gun crime rates easier to understand, each parcel was classified by the percentile into which its gun crime score falls.
        Those interested in a more in-depth understanding of how this map was produced can view the Python code behind the dataset in this GitHub repository.
      </p>

    </div>
    <div className="text-left my-10">
      <h2 className="text-2xl font-bold mt-4">Attribution</h2>
      <p className="text-2xl mb-4">
        This dashboard was built by Nissim Lebovits. He is a master's student in city planning at the University of Pennsylvania's Weitzman School of Design,
        where he focuses on environmental planning and spatial analysis. He's interested in using data to foster civic engagement and build more sustainable,
        inclusive cities. Previously he was an AmeriCorps VISTA with the City of Philadelphia, where he worked to support residents of the West Philadelphia Promise Zone.
        For questions about this dashboard, to see more of his work, or to hire him to support your community organization's data work, please see his website.
      </p>

      <h2 className="text-2xl font-bold mt-4">Acknowledgements</h2>
      <p className="text-2xl mb-4">
        Many people helped inform this tool, including residents, CDC leaders, City staff, Penn faculty, and more. Special thanks, however,
        are due to Dante Leonard for facilitating countless valuable conversations with people throughout Philadelphia, to Mjumbe Poe
        for serving as my independent study instructor while I built the JavaScript dashboard and website, to Vicky Tam for teaching the GIS class
        in which I built the first functional version of this tool, and to Dr. Eugenia South for spearheading the original research upon which this tool is based.
      </p>
    </div>
    <div className="flex justify-between space-x-2.5">

    </div>
  </div>
  
);


export default AboutPage;
*/