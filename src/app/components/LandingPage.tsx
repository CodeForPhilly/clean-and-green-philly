import imageCleaning from "@/images/cleaningLot.jpg";
import imageGunCrimes from "@/images/graphic-guncrimes.png";
import imageResearch from "@/images/graphic-research.png";
import imageGreened from "@/images/greenedLot.jpg";
import imageStep1 from "@/images/landing-step-1.png";
import imageStep2 from "@/images/landing-step-2.png";
import imageStep3 from "@/images/landing-step-3.png";
import { ArrowDownIcon } from "@heroicons/react/20/solid";
import { Button, Image, Link } from "@nextui-org/react";
import { ArrowRight, Binoculars, Key, Tree } from "@phosphor-icons/react";
import { InfoGraphicSection } from "./InfoGraphicSection";
import { NumberedIconCard } from "./NumberedIconCard";

const images = [
  {
    src: "/dirtyLot.jpg",
    alt: "Dirty lot in Philadelphia",
  },
  {
    src: "/cleaningLot.jpg",
    alt: "Cleaning lot in Philadelphia",
  },
  {
    src: "/greenedLot.jpg",
    alt: "Greened lot in Philadelphia",
  },
];

const LandingPage = () => (
  <div className="container mx-auto px-4">
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center my-10">
      <div className="text-left pr-9">
        <h1 className="heading-3xl font-extrabold leading-tight md:leading-[3rem] text-pretty">
          <span className="block">
            Cleaning and greening vacant properties can{" "}
            <span className="text-green-600 font-extrabold">
              reduce gun violence
            </span>{" "}
            by as much as 29%.
          </span>
        </h1>
      </div>
      <div className="flex flex-col justify-between items-start">
        <div className="text-gray-700 mb-4">
          {/* Responsive paragraphs */}
          <p className="hidden md:block body-lg text-balance">
            This tool can empower community groups and organizations trying to
            clean and green vacant properties to reduce gun violence.
          </p>
        </div>
        <Button
          href="#guncrimes"
          as={Link}
          size="lg"
          className="bg-gray-100 text-black gap-1"
        >
          <ArrowDownIcon className="w-5 h-5" />
          <span className="body-md">Learn How</span>
        </Button>
      </div>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-10">
      {images.map(({ src, alt }) => (
        <Image
          key={src}
          src={src}
          alt={alt}
          width="100%"
          height="auto"
          className="rounded-[8px] aspect-video md:aspect-auto object-cover object-center"
        />
      ))}
    </div>

    <div id={"guncrimes"} className="my-20">
      <InfoGraphicSection
        header={"Philadelphia has a gun violence problem."}
        body={
          "With homicides trending up since 2013, and a record high of 562 gun deaths in 2021, community members need concrete solutions. Many solutions focus on long-term impact, including nearly 80% of the City of Philadelphia's anti-violence spending, but immediate, actionable approaches are also needed."
        }
        image={{
          data: imageGunCrimes,
          alt: "Diagram of Annual Shootings in Philadelphia",
        }}
      />
    </div>

    <div id={"research"} className="my-20">
      <InfoGraphicSection
        header={"Cleaning and greening reduces violence by 29%."}
        body={
          "Research shows that greening and cleaning vacant properties is one of the most impactful, cost-effective interventions available to reduce gun violence in a neighborhood. Dr. Eugenia South and her team have demonstrated that greening vacant lots in Philadelphia reduced gun violence by as much as 29% in the surrounding area."
        }
        image={{
          data: imageResearch,
          alt: "Academic research papers",
          className: "aspect-[4/3] object-cover object-center",
        }}
      />
    </div>

    <div id={"community"} className="my-20">
      <InfoGraphicSection
        header={"Community groups and organizations are taking action."}
        body={
          "Community groups have been cleaning up lots in their own neighborhoods for decades. Large organizations like the Pennsylvania Horticulture Society have cleaned, greened and now maintain thousands of lots. Their efforts have been instrumental in proving this works."
        }
        image={{
          data: imageCleaning,
          alt: "Two people cleaning a lot",
          className: "aspect-video object-cover object-center",
        }}
      />
    </div>

    <div id={"actions"} className="my-20">
      <InfoGraphicSection
        header={"We are building the ultimate toolkit to help them."}
        body={
          "We are a passionate group of volunteers with a vision to empower citizens, groups, and organizations to do impactful data-driven environmental interventions in Philadelphia."
        }
        component={
          <div className="grid grid-cols-3 gap-5 w-full lg:w-[550px]">
            <NumberedIconCard
              icon={Binoculars}
              num={1}
              body={"Find a Vacant Property"}
            />
            <NumberedIconCard
              icon={Key}
              num={2}
              body={"Get Access to the Property"}
            />
            <NumberedIconCard
              icon={Tree}
              num={3}
              body={"Transform the Property"}
            />
          </div>
        }
      />
    </div>

    <div id={"step-1"} className="my-20">
      <InfoGraphicSection
        header={
          <ol start={1} className="list-outside list-decimal pl-7 md:pl-10">
            <li>Find vacant properties that match your goals.</li>
          </ol>
        }
        body={
          "You can search and find vacant properties that match your goals. Understand the data around that property and the surrounding neighborhoods."
        }
        image={{
          data: imageStep1,
          alt: "Placeholder graphic",
        }}
        link={{
          icon: Binoculars,
          label: "Find Properties",
          href: "/map",
        }}
      />
    </div>

    <div id={"step-2"} className="my-20">
      <InfoGraphicSection
        header={
          <ol start={2} className="list-outside list-decimal pl-7 md:pl-10">
            <li>Get data-driven suggestions on how to legally get access.</li>
          </ol>
        }
        body={
          "How do you actually get access to the property legally? This is often confusing and baffling to people. We use the property data to suggest the most convenient options and provide guidance on the process."
        }
        image={{
          data: imageStep2,
          alt: "Placeholder graphic",
        }}
        link={{
          icon: Key,
          label: "Get Access",
          href: "/get-access",
        }}
      />
    </div>

    <div id={"step-3"} className="my-20">
      <InfoGraphicSection
        header={
          <ol start={3} className="list-outside list-decimal pl-7 md:pl-10">
            <li>See all the ways you can transform properties.</li>
          </ol>
        }
        body={
          "We guide you through the most common, convenient and affordable ways to transform properties and resources on how to do it."
        }
        image={{
          data: imageStep3,
          alt: "Placeholder graphic",
        }}
        link={{
          icon: Tree,
          label: "Transform",
          href: "/transform-property",
        }}
      />
    </div>

    <div id={"get-started"} className="my-20">
      <InfoGraphicSection
        header={"Let's Do This!"}
        body={
          "There's groups and organizations throughout Philadelphia taking action and seeing impacts in their community and you can too."
        }
        image={{
          data: imageGreened,
          alt: "A beautifully transformed community lot",
          className: "aspect-video object-cover object-center",
        }}
        link={{
          icon: ArrowRight,
          label: "Get Started",
          href: "/map",
        }}
      />
    </div>
  </div>
);

export default LandingPage;
