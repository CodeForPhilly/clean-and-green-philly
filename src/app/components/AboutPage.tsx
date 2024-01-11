import { Accordion, AccordionItem, Button, Link, Image } from "@nextui-org/react";
import { get } from "http";


export default function AboutPage() {
  return (
    <div className="grid grid-cols-2 gap-4 py-8 px-24">
      <div className="container mx-auto">
        <h2 className="text-3xl font-semibold mb-4">What is this?</h2>
        <p className="text-lg mb-4">
        Philadelphia has a gun violence problem. Clean & Green Philly empowers Philadelphians to take action to solve it.
        </p>
        <p className="text-lg">
          Our dashboard helps local residents, non-profit organizations, and government stakeholders identify and prioritize vacant properties for interventions, understand how to transform the properties they’ve identified, and connect with resources that will help them do so.
        </p>
        <br></br>
        <h2 className="text-3xl font-semibold mb-4">Why make this?</h2>
        <p className="text-lg mb-4">
        Clean & Green Philly was built to respond to Philadelphia’s historic gun violence problem. With homicides trending up since 2013, and a record high of 562 gun deaths in 2021, community members need concrete solutions.
        </p>
        <div className="mt-1 flex items-center justify-center">
          <Image src="/annual_guncrimes_plot.png" alt="A graph of gun crimes in Philadelphia since 2013" width={600} height={400} />
        </div>
        <p className="text-lg mb-4">
          Many solutions focus on long-term impact, including <a href="https://controller.phila.gov/philadelphia-audits/fy23-anti-violence-budget/#/" target="_blank" rel="noopener noreferrer" className="text-primary">nearly 80% of the City of Philadelphia’s anti-violence spending</a>. But immediate, actionable approaches are also needed. Clean & Green Philly helps to fill that gap by promoting interventions in vacant properties. Our goal is to make it as easy as possible for everyday Philadelphians to take action to reduce gun violence in our city.
        </p>
        <p className="text-lg mb-4">
        Research shows that greening and cleaning vacant properties is one of the most impactful, cost-effective interventions available to reduce gun violence in a neighborhood. For example, Dr. Eugenia South and her team have demonstrated that  
        <a href="https://www.pnas.org/doi/10.1073/pnas.1718503115" target="_blank" rel="noopener noreferrer" className="text-primary"> greening vacant lots</a> in Philadelphia reduced gun violence by as much as 29% in the surrounding area.
        </p>
        <div className="mt-4 flex items-center justify-center">
          <Image src="/main_article_summary.png" alt="Excerpts from research on reducing gun violence with vacant lot interventions" width={600} height={400} />
        </div>
        <p className="text-lg">
          Transforming Philadelphia’s vacant lots should be a key strategy to combating gun violence here. But in a city with nearly 40,000 vacant properties, the main obstacle is figuring out which properties to prioritize and how to get access to them. Clean & Green Philly helps solve this problem by using public data to identify high-priority properties, filter them based on the possible ways of intervening, and connect users to resources that can support these interventions.
        </p>
        <div className="mt-4 flex items-center justify-center">
          <Image src="/transformed_lots.png" alt="Examples of transformed lots" width={600} height={400} />
        </div>
      </div>
      <div className="container mx-auto">
        <h2 className="text-3xl font-semibold mb-4">How was this built?</h2>
        <p className="text-lg mb-4">
        Clean & Green Philly combines several public datasets in order to categorize Philadelphia’s vacant properties based on how important it is that someone intervene there and what the easiest way to do that is.
        </p>
        <p className="text-lg mb-4">
          We created the dataset based on the original research conducted by Dr. Eugenia South and her colleagues, as well as many conversations with stakeholders, including community residents, CDCs, City government offices, academic researchers, and more.
        </p>
        <p className="text-lg">
          All of the code used to build this tool is <a href="https://github.com/CodeForPhilly/vacant-lots-proj" target="_blank" rel="noopener noreferrer" className="text-primary">available on our GitHub repository</a>. We hope to add data documentation in the near future. For further questions about our methods, feel free to reach out to us at <a href="mailto:cleangreenphilly@gmail.com" className="text-primary">cleangreenphilly@gmail.com</a>.
        </p>
        <br></br>
        <h2 className="text-3xl font-semibold mb-4">Who built this?</h2>
        <p className="text-lg mb-4">
        Clean & Green Philly was built by a team of Code for Philly volunteers. The project was created and led by Nissim Lebovits. Will Budreau was responsible for user testing and research, Brandon Cohen was the lead developer, and Nathaniel Sidwell led the UX team. Thanks, too, to the many other contributors along the way.
        </p>
        <p className="text-lg mb-4">
          Our efforts have been informed and advanced by local residents, community leaders, City staff, faculty at the University of Pennsylvania, Temple University, and Thomas Jefferson University; and many others. Special thanks are due to the Code for Philly leadership, Jon Geeting, Dante Leonard, Mjumbe Poe, and Vicky Tam.
        </p>
        <p className="text-lg">
          Lastly, we are grateful to Dr. Eugenia South and her colleagues, whose work this project depends on.
        </p>
        <br></br>
        <h2 className="text-3xl font-semibold mb-4">Feedback</h2>
        <p className="text-lg mb-4">
        If you find issues in this website or would like to offer us feedback, please reach out to us at <a href="mailto:cleangreenphilly@gmail.com" className="text-primary">cleangreenphilly@gmail.com</a>.
        </p>
      </div>
    </div>
  );
}





/*
import AboutPageImage from "./AboutPageImage";

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

      <div className="mt-4"></div>

    </div>
  );
}
*/
