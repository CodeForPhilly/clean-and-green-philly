import { Accordion, AccordionItem } from "@nextui-org/react";
import Image from "next/image";
import beforeAfter from "@/images/beforeAfter.png";
import cleanup from "@/images/lot-cleanup.png";
import plant from "@/images/plant-trees.jpeg";
import maintain from "@/images/maintain.jpeg";
import fence from "@/images/fence.png";
import pollinators from "@/images/flowers.png";
import garden from "@/images/community-garden.jpeg";
import meadow from "@/images/meadow.jpeg";
import bikeracks from "@/images/bike-rack.jpeg";
import stormwater from "@/images/stormwater.png";
import restaurant from "@/images/restaurant.jpeg";
import housing from "@/images/housing.png";
import park from "@/images/install-a-park.jpeg";
import ContentCard from "../../../components/ContentCard";

export default function TransformPropertyPage() {
  return (
    <>
      <h1 className="heading-3xl font-bold mb-6">Transform a Property</h1>

      <p className="body-lg">
        After gaining access to the property, you can transform a property to
        improve the quality of life in the neighborhood.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-1 gap-6 md:gap-10">
        <Image
          src={beforeAfter}
          alt={
            "A Philadelphia lot before a clean up and the same lot, filled with trees and greenery after a clean up."
          }
          placeholder="blur"
          className="w-full mt-6 overflow-hidden rounded-[20px] aspect-video md:aspect-auto object-cover object-center"
        />
      </div>

      <h2 className="heading-2xl font-bold mt-8">Basic Interventions</h2>
      <p className="body-md">
        The original research that Clean & Green Philly is based on promotes
        “cleaning and greening.” This includes removing trash, grading the land,
        planting trees, installing low fences, and maintaining the property.
        These are low-cost interventions and have been proven to be highly
        effective; even something as simple as cleaning up trash can have a big
        impact.
      </p>
      <div className="grid grid-cols-1 lg:grid-cols-3 md:grid-cols-2 gap-6 py-6">
        <ContentCard
          image={cleanup}
          alt=""
          title="Clean Garbage & Debris"
          body="Organizing a community clean-up or hiring a waste removal service to clean a lot, enhances its appearance, lifts mental health, and eliminates potential hazards."
          details={[
            {
              label: "Cost:",
              data: "Low",
            },
            {
              label: "Upkeep:",
              data: "None",
            },
          ]}
          links={[
            {
              url: "https://nkcdc.org/community/cleaning-greening/community-cleanup-resources/",
              text: "Resources on NKCDC",
            },
          ]}
        />

        <ContentCard
          image={plant}
          alt=""
          title="Plant Trees"
          body="Planting trees not only adds beauty and shade to the lot but also contributes to urban cooling, air purification, and habitat for wildlife."
          details={[
            {
              label: "Cost:",
              data: "Low",
            },
            {
              label: "Upkeep:",
              data: "Low",
            },
          ]}
          links={[
            {
              url: "https://treephilly.org/yard-trees-2/",
              text: "Help on Tree Philly",
            },
          ]}
        />

        <ContentCard
          image={maintain}
          alt=""
          title="Maintain regularly"
          body="Mowing grass, raking leaves, and clearing trash regularly ensures the lot remains clean, safe, and attractive, promoting community pride and deterring illegal activities."
          details={[
            {
              label: "Cost:",
              data: "Low",
            },
            {
              label: "Upkeep:",
              data: "Low",
            },
          ]}
        />

        <ContentCard
          image={fence}
          alt=""
          title="Install Low Fences"
          body="Hiring a contractor to install low fences defines boundaries, enhances safety, and improves aesthetics while allowing for easy access and integration with the neighborhood."
          details={[
            {
              label: "Cost:",
              data: "Medium",
            },
            {
              label: "Upkeep:",
              data: "Low",
            },
          ]}
        />
      </div>

      <h2 className="heading-2xl font-bold mt-8">Advanced Interventions</h2>
      <p className="body-md">
        Different properties have different opportunities and different
        challenges. Some properties might be a great spot for a rain garden but
        not for a playground. Likewise, you wouldn't want to start a community
        garden in a vacant lot that doesn't get any sun. To better understand
        what your options are for a specific property, try filling out the{" "}
        <a
          href="https://detroitfuturecity.com/whatwedo/land-use/DFC-lots/"
          className="link"
        >
          Detroit Future City vacant property quiz
        </a>{" "}
        (the recommendations work for Philadelphia too!). It's meant to help
        users understand the best options for their specific properties. Also,
        remember to think about other constraints, like how much funding you
        have, and how much maintenance you're willing or able to do. There are
        many ways to imagine transforming a vacant property if you want to work
        with funding and community support. Check out our{" "}
        <a href="/resources" className="link">
          Resources Page
        </a>{" "}
        to explore more like these:
      </p>
      <div className="grid grid-cols-1 lg:grid-cols-3 md:grid-cols-2 gap-6 py-6">
        <ContentCard
          image={pollinators}
          alt=""
          title="Plant Pollinator Garden"
          body="Creating a pollinator garden promotes biodiversity, supports local ecosystems, and beautifies the lot with colorful flowers."
          links={[
            {
              url: "https://phsonline.org/uploads/attachments/ckacmpaca1evpj7rasp7ty5aq-pollinator-gardens-infosheet.pdf",
              text: "Help from PHS",
            },
          ]}
        />

        <ContentCard
          image={garden}
          alt=""
          title="Establish a Community Garden"
          body="Establishing a community garden provides fresh produce, promotes social interaction, and transforms the lot into a productive and vibrant space for residents."
          links={[
            {
              url: "https://groundedinphilly.org/",
              text: "Resources from Grounded in Philly",
            },
          ]}
        />

        <ContentCard
          image={meadow}
          alt=""
          title="Plant a Meadow"
          body="Planting native wildflowers and grasses brings natural beauty, supports local wildlife, and requires less maintenance than traditional landscaping."
          links={[
            {
              url: "https://extension.psu.edu/meadows-and-prairies-wildlife-friendly-alternatives-to-lawn",
              text: "Instructions from Penn State",
            },
          ]}
        />

        <ContentCard
          image={bikeracks}
          alt=""
          title="Install Bike Parking"
          body="Installing bike parking encourages sustainable transportation, reduces congestion, and supports a healthier lifestyle for community members."
          links={[
            {
              url: "https://streetboxphl.com/",
              text: "Help from StreetBoxPHL",
            },
            {
              url: "https://www.phila.gov/media/20211109093815/OTIS-bike-corral-application.pdf",
              text: "Guidelines from City of Phila",
            },
          ]}
        />

        <ContentCard
          image={stormwater}
          alt=""
          title="Install Green Stormwater Infrastructure"
          body="Rain gardens and other infrastructure reduces stormwater runoff, prevents flooding, and improves water quality while adding greenery to the urban landscape."
          links={[
            {
              url: "https://groundedinphilly.org/",
              text: "Help from Phila Water Department",
            },
          ]}
        />

        <ContentCard
          image={restaurant}
          alt=""
          title="Offer Outdoor Restaurant Space"
          body="Providing seating and shade to local  restaurants attracts businesses, creates a lively atmosphere, and encourages community gathering and economic growth. "
          links={[
            {
              url: "https://streetboxphl.com/",
              text: "Help from StreetBoxPHL",
            },
            {
              url: "https://www.phila.gov/services/permits-violations-licenses/get-a-license/business-licenses/food-businesses/get-a-streetery-license/",
              text: "Guidelines from City of Phila",
            },
          ]}
        />

        <ContentCard
          image={housing}
          alt=""
          title="Affordable Housing"
          body="Developing affordable housing addresses housing needs, promotes diversity, and helps revitalize the neighborhood while providing homes for residents."
          links={[
            {
              url: "https://phdcphila.org/land/buy-land/propose-affordable-housing-project/",
              text: "Help from PHDC",
            },
            {
              url: "https://www.habitatphiladelphia.org/homeownership-program/",
              text: "Help from Habitat from Humanity",
            },
            {
              url: "https://www.lisc.org/philly/our-priorities/affordable-housing/",
              text: "Help from LISC",
            },
          ]}
        />

        <ContentCard
          image={park}
          alt=""
          title="Install a Park"
          body="Providing seating, green spaces, and walking paths offers recreational space, improves public health, and enhances quality of life."
          links={[
            {
              url: "https://www.jefferson.edu/academics/colleges-schools-institutes/architecture-and-the-built-environment/programs/landscape-architecture/park-in-a-truck.html",
              text: "Help from Park in a Truck",
            },
          ]}
        />
      </div>

      <h2 className="heading-2xl font-bold mt-8">Where can I get help?</h2>
      <p className="body-md">
        Many organizations in Philadelphia offer support transforming vacant
        properties.
      </p>
      <h3 className="heading-xl font-bold mt-8 mb-4">
        Community Groups and Local Representatives
      </h3>
      <p className="body-md">
        For help with greening projects, reach out to local Neighborhood
        Advisory Committees, Community Development Corporations, or Registered
        Community Organizations. They can guide you through the planning process
        and help with local rules. Local representatives can also support you,
        especially if you're facing red tape. Bring them a solid plan and show
        how your project can improve the community.
      </p>

      <h3 className="heading-xl font-bold mt-8 mb-4">
        Garden Justice Legal Initiative
      </h3>
      <p className="body-md">
        The{" "}
        <a
          href="https://pubintlaw.org/cases-and-projects/garden-justice-legal-initiative-gjli/"
          className="link"
        >
          Garden Justice Legal Initiative
        </a>{" "}
        supports community gardens and urban farms, offering free legal help,
        policy research, and community education. They work with coalitions like{" "}
        <a href="https://soilgeneration.org/" className="link">
          Soil Generation
        </a>{" "}
        to empower residents to use vacant land for gardens and farming,
        providing tools and information through training sessions and their
        online resource,{" "}
        <a href="https://groundedinphilly.org/" className="link">
          Grounded in Philly
        </a>
        .
      </p>

      <h3 className="heading-xl font-bold mt-8 mb-4">StreetBoxPHL</h3>
      <p className="body-md">
        <a href="https://streetboxphl.com/" className="link">
          StreetBoxPHL
        </a>{" "}
        helps community groups revitalize urban spaces by making parklets,
        pedestrian plazas, and bike corrals. Their tools can quickly transform
        underused spaces into vibrant, green areas that benefit the whole
        community. They offer technical support, a street furniture library, and
        help with insurance requirements.
      </p>

      <h3 className="heading-xl font-bold mt-8 mb-4">Park in a Truck</h3>
      <p className="body-md">
        <a
          href="https://www.jefferson.edu/academics/colleges-schools-institutes/architecture-and-the-built-environment/programs/landscape-architecture/park-in-a-truck.html"
          className="link"
        >
          Park in a Truck
        </a>{" "}
        supports community residents in quickly building custom parks. They've
        developed{" "}
        <a
          href="https://www.jefferson.edu/content/dam/academic/cabe/landscape-architecture/park-in-a-truck/toolkit/PiaT-toolkit-2022.pdf"
          className="link"
        >
          a toolkit
        </a>{" "}
        that helps community groups design and build parks that fit their needs.
        They also offer training and technical support to help communities
        create and maintain their parks.
      </p>

      <h2 className="heading-2xl font-bold mt-8">
        What else should I think about?
      </h2>

      <div className="body-md">
        <Accordion variant="light" selectionMode="multiple">
          <AccordionItem
            key="1"
            aria-label="Maintenance"
            title="Maintenance"
            subtitle="Click to expand"
            className="font-bold text-large"
          >
            <div className="text-base font-normal">
              It's also key to make sure that the improvements you make can keep
              going for a long time. Getting people in the area to care about
              and look after these spaces can really help. Choose projects that
              don't cost much but still have a big impact, so they're easier for
              the community to maintain. Be smart about legal stuff, especially
              with private property, and work with local authorities to make
              sure everything is okay there.
            </div>
          </AccordionItem>

          <AccordionItem
            key="2"
            aria-label="Funding"
            title="Funding"
            subtitle="Click to expand"
            className="font-bold text-large"
          >
            <div className="text-base font-normal">
              When it comes to funding, try to connect with local businesses and
              community groups. Small grants and donations might be easier to
              get for groups like yours. And don't forget about raising money
              right in the community through events or online campaigns.
            </div>
          </AccordionItem>

          <AccordionItem
            key="3"
            aria-label="Gentrification"
            title="Gentrification"
            subtitle="Click to expand"
            className="font-bold text-large"
          >
            <div className="text-base font-normal">
              Remember, your projects shouldn't push out the current residents.
              Keep them at the heart of what you do, and keep an eye on how
              things change in the neighborhood. Work together with other local
              groups, schools, and businesses - it's a great way to get more
              resources and ideas. Have regular meetings with people in the
              community to keep them in the loop and involved in decisions.
            </div>
          </AccordionItem>
        </Accordion>
      </div>
    </>
  );
}
