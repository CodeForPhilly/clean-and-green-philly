import Image from "next/image";
import beforeAfter from "@/images/beforeAfter.png";
import { ArrowUpRight } from "@phosphor-icons/react";

export default function TransformPropertyPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flew-grow container mx-auto pt-20">
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

        <h2 className="heading-2xl font-bold mt-8 mb-6">Basic Interventions</h2>
        <p className="body-md">
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
          out the
          <a
            target="_blank"
            rel="noopener noreferrer nofollow"
            href="https://detroitfuturecity.com/whatwedo/land-use/DFC-lots/"
            className="link mx-1"
          >
            Detroit Future City vacant property quiz
          </a>
          (the recommendations work for Philadelphia too!). It’s meant to help
          users understand the best options for their specific properties. Also,
          remember to think about other constraints, like how much funding you
          have, and how much maintenance you’re willing or able to do.
        </p>
        <p className="body-md mb-4">
          There are many ways to imagine transforming a vacant property if you
          want to work with funding and community support. Check out our
          Resources Page to explore more like these:
          {/* Resources Link Needed */}
        </p>

        {/* Eight Advanced interventions green cards go here */}

        <h2 className="heading-2xl font-bold mt-8 mb-6">Get Help</h2>
        <p className="body-md">
          Many organizations in Philadelphia offer support transforming vacant
          properties. See our resources page for more information!
        </p>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mb-4">Park in a Truck</h3>
          <p className="body-md mb-4">
            Park in a Truck supports community residents in quickly building
            custom parks. They've developed a toolkit that helps community
            groups design and build parks that fit their needs. They also offer
            training and technical support to help communities create and
            maintain their parks.
          </p>
          <a
            target="_blank"
            rel="noopener noreferrer nofollow"
            href="https://www.jefferson.edu/academics/colleges-schools-institutes/architecture-and-the-built-environment/programs/landscape-architecture/park-in-a-truck.html"
            className="link inline-flex items-center leading-5"
          >
            Park in a Truck
            <ArrowUpRight className="mt-1" size={20} aria-hidden="true" />
          </a>
        </div>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mb-4">Jump Start</h3>
          <p className="body-md mb-4">
            Jump Start is a source of short term financing that guides you along
            the way, and moves quickly, to help you succeed in a competitive
            real estate market. Jumpstart Philly offers acquisition and
            construction financing for residential and mixed-use investment
            projects throughout the City of Philadelphia. We are more than a
            bank, we’re a non-traditional, community-driven lender ready to see
            you succeed.
          </p>
          <a
            target="_blank"
            rel="noopener noreferrer nofollow"
            //add hyperlink here in place of #  -> href="#"
            className="link inline-flex items-center leading-5"
          >
            Jump Start
            <ArrowUpRight className="mt-1" size={20} aria-hidden="true" />
          </a>
        </div>

        <div className="bg-gray-100 rounded-lg p-8 mt-8">
          <h3 className="heading-xl font-bold mb-4">Local Representatives</h3>
          <p className="body-md">
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
          <p className="body-md mb-4">
            Getting funding is a vital part of returning vacant properties to
            productive use. Funding can come from many sources, such as grants
            from local government and non-profit funders, public-private
            partners, and crowd-sourced fundraising. In the future, we plan to
            add a page to list common funding sources and explain how to use
            data from Clean & Green Philly to support a grant application.
          </p>
          <p className="body-md mb-4">
            Any amount of funding can be useful. Many effective interventions
            such as property cleanups can be accomplished for a few hundred
            dollars—or even for free, with volunteer support! When planning your
            property intervention, consider what level of funding you have
            access to, and how you can get the most bang for your buck.
          </p>
          <p className="body-md mb-4">
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
          <p className="body-md mb-4">
            Transforming a vacant property isn’t a one-and-done event. In fact,
            many properties that are currently vacant were transformed years
            ago—but not maintained in the decades since. In order to make sure
            that your intervention is high-impact and long-lived, make sure to
            have a maintenance plan in place.
          </p>
          <p className="body-md mb-4">
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
          <p className="body-md">
            Our goal is to help community groups reduce violence through
            cleaning and greening methods in their neighborhoods. We recognize
            that may inadvertently increase property values, increase rental
            prices and displace already-marginalized Philadelphians. We are
            working to avoid this by meeting extensively with community groups
            and responding to their concerns. Read more about this topic.
            {/* Link to gentrification page */}
          </p>
        </div>
      </div>
    </div>
  );
}
