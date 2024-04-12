import Image from "next/image";
import beforeAfter from "@/images/beforeAfter.png";

export default function TransformPropertyPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flew-grow container mx-auto pt-20">
        <h1 className="heading-3xl font-bold mb-6">Transform a Property</h1>
        <p>
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

        <h2 className="heading-2xl font-bold mt-8 mb-6">Basic Interventions</h2>
        <p>
          The original research that Clean & Green Philly is based on promotes
          “cleaning and greening.” This includes removing trash, grading the
          land, planting trees, installing low fences, and maintaining the
          property. These are low-cost interventions and have been proven to be
          highly effective; even something as simple as cleaning up trash can
          have a big impact.
        </p>
        {/* Four basic interventions green cards go here */}

        <h2 className="heading-2xl font-bold mt-8 mb-6">
          Advanced Interventions
        </h2>
        <p className="body-md mb-4">
          Different properties have different opportunities and different
          challenges. Some properties might be a great spot for a rain garden
          but not for a playground. Likewise, you wouldn’t want to start a
          community garden in a vacant lot that doesn’t get any sun. To better
          understand what your options are for a specific property, try filling
          out the Detroit Future City vacant property quiz (the recommendations
          work for Philadelphia too!). It’s meant to help users understand the
          best options for their specific properties. Also, remember to think
          about other constraints, like how much funding you have, and how much
          maintenance you’re willing or able to do.
        </p>
        <p className="mb-4">
          There are many ways to imagine transforming a vacant property if you
          want to work with funding and community support. Check out our
          Resources Page to explore more like these:
        </p>

        {/* Eight Advanced interventions green cards go here */}

        <h2 className="heading-2xl font-bold mt-8 mb-6">Get Help</h2>
        <p>
          Many organizations in Philadelphia offer support transforming vacant
          properties. See our resources page for more information!
        </p>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mb-4">Park in a Truck</h3>
          <p>
            Park in a Truck supports community residents in quickly building
            custom parks. They've developed a toolkit that helps community
            groups design and build parks that fit their needs. They also offer
            training and technical support to help communities create and
            maintain their parks.
          </p>
        </div>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mb-4">Jump Start</h3>
          <p>
            Jump Start is a source of short term financing that guides you along
            the way, and moves quickly, to help you succeed in a competitive
            real estate market. Jumpstart Philly offers acquisition and
            construction financing for residential and mixed-use investment
            projects throughout the City of Philadelphia. We are more than a
            bank, we’re a non-traditional, community-driven lender ready to see
            you succeed.
          </p>
        </div>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mt-8 mb-4">
            Local Representatives
          </h3>
          <p>
            Local representatives can also support you, especially if you're
            facing red tape. Bring them a solid plan and show how your project
            can improve the community.
          </p>
        </div>

        <h2 className="heading-2xl font-bold mt-8 mb-6">
          Additional Considerations
        </h2>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mb-4">Funding</h3>
          <p className="mb-4">
            Getting funding is a vital part of returning vacant properties to
            productive use. Funding can come from many sources, such as grants
            from local government and non-profit funders, public-private
            partners, and crowd-sourced fundraising. In the future, we plan to
            add a page to list common funding sources and explain how to use
            data from Clean & Green Philly to support a grant application.
          </p>
          <p className="mb-4">
            Any amount of funding can be useful. Many effective interventions
            such as property cleanups can be accomplished for a few hundred
            dollars—or even for free, with volunteer support! When planning your
            property intervention, consider what level of funding you have
            access to, and how you can get the most bang for your buck.
          </p>
          <p className="mb-4">
            Funding is needed not only for the initial property transformation,
            but also to maintain the project in the long term. When planning
            your project, consider dividing your funding into two parts: one
            part to pay for the initial intervention, and a second part—at least
            equal to the first part—to pay for maintaining your project in the
            future.
          </p>
        </div>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mb-4">Maintenance</h3>
          <p className="mb-4">
            Transforming a vacant property isn’t a one-and-done event. In fact,
            many properties that are currently vacant were transformed years
            ago—but not maintained in the decades since. In order to make sure
            that your intervention is high-impact and long-lived, make sure to
            have a maintenance plan in place.
          </p>
          <p className="mb-4">
            Consider who will be responsible for maintaining the property, what
            their tasks will be, what kind of resources they will need, and how
            you will fund this ongoing maintenance. Often, partnering with an
            established organization like a CDC can help make sure that you have
            the capacity and resources needed to ensure that your intervention
            continues to be effective for many years into the future.
          </p>
        </div>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mb-4">Gentrification </h3>
          <p>
            Our goal is to help community groups reduce violence through
            cleaning and greening methods in their neighborhoods. We recognize
            that may inadvertently increase property values, increase rental
            prices and displace already-marginalized Philadelphians. We are
            working to avoid this by meeting extensively with community groups
            and responding to their concerns. Read more about this topic.
            {/* Link to gentrification page */}
          </p>
        </div>

        {/* <p >
          These are just some of the many possibilities. Remember to be both
          creative and practical: there is no one-size-fits-all solution, and
          Philadelphia will need a variety of uses in its vacant properties,
          including green space, housing, parks, commercial space, and more.
        </p> */}

        {/* <h2 className="heading-2xl font-bold mt-8">
          What's right for my property?
        </h2> */}

        {/* <p >
          Different properties have different opportunities and different
          challenges. Some properties might be a great spot for a rain garden
          but not for a playground. Likewise, you wouldn’t want to start a
          community garden in a vacant lot that doesn’t get any sun. To better
          understand what your options are for a specific property, try filling
          out the{" "}
          <a
            href="https://detroitfuturecity.com/whatwedo/land-use/DFC-lots/"
            className="link"
          >
            Detroit Future City vacant property quiz
          </a>
          . It’s meant to help users understand the best options for their
          specific properties. Although it was built for users in Detroit, it’s
          still helpful here in Philadelphia. Also, remember to think about
          other constraints, like how much funding you have, and how much
          maintenance you’re willing or able to do.
        </p> */}
        {/* <h2 className="heading-2xl font-bold mt-8">Where can I get help?</h2>
        <p >
          Many organizations in Philadelphia offer support transforming vacant
          properties.
        </p>
        <h3 className="heading-xl font-bold mt-8 mb-4">
          Community Groups and Local Representatives
        </h3>
        <p >
          For help with greening projects, reach out to local Neighborhood
          Advisory Committees, Community Development Corporations, or Registered
          Community Organizations. They can guide you through the planning
          process and help with local rules. Local representatives can also
          support you, especially if you're facing red tape. Bring them a solid
          plan and show how your project can improve the community.
        </p>
        <h3 className="heading-xl font-bold mt-8 mb-4">
          Garden Justice Legal Initiative
        </h3>
        <p >
          The{" "}
          <a
            href="https://pubintlaw.org/cases-and-projects/garden-justice-legal-initiative-gjli/"
            className="link"
          >
            Garden Justice Legal Initiative
          </a>{" "}
          supports community gardens and urban farms, offering free legal help,
          policy research, and community education. They work with coalitions
          like{" "}
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
        <p >
          <a href="https://streetboxphl.com/" className="link">
            StreetBoxPHL
          </a>{" "}
          helps community groups revitalize urban spaces by making parklets,
          pedestrian plazas, and bike corrals. Their tools can quickly transform
          underused spaces into vibrant, green areas that benefit the whole
          community. They offer technical support, a street furniture library,
          and help with insurance requirements.
        </p>
        <h3 className="heading-xl font-bold mt-8 mb-4">Park in a Truck</h3>
        <p >
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
          that helps community groups design and build parks that fit their
          needs. They also offer training and technical support to help
          communities create and maintain their parks.
        </p>
        <h2 className="heading-2xl font-bold mt-8">
          What else should I think about?
        </h2>
        <div >
          <Accordion variant="light" selectionMode="multiple">
            <AccordionItem
              key="1"
              aria-label="Maintenance"
              title="Maintenance"
              subtitle="Click to expand"
              className="font-bold text-large"
            >
              <div className="text-base font-normal">
                It's also key to make sure that the improvements you make can
                keep going for a long time. Getting people in the area to care
                about and look after these spaces can really help. Choose
                projects that don't cost much but still have a big impact, so
                they're easier for the community to maintain. Be smart about
                legal stuff, especially with private property, and work with
                local authorities to make sure everything is okay there.
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
                When it comes to funding, try to connect with local businesses
                and community groups. Small grants and donations might be easier
                to get for groups like yours. And don't forget about raising
                money right in the community through events or online campaigns.
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
                Remember, your projects shouldn't push out the current
                residents. Keep them at the heart of what you do, and keep an
                eye on how things change in the neighborhood. Work together with
                other local groups, schools, and businesses - it's a great way
                to get more resources and ideas. Have regular meetings with
                people in the community to keep them in the loop and involved in
                decisions.
              </div>
            </AccordionItem>
          </Accordion>
        </div> */}
      </div>
    </div>
  );
}
