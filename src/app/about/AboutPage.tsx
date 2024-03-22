import {
  Modal,
  ModalContent,
  ModalBody,
  useDisclosure,
  Image,
  Tooltip,
  Button,
  Link,
} from "@nextui-org/react";

import { PiArrowRight } from "react-icons/pi";

export default function AboutPage() {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-grow grid grid-cols-1 md:grid-cols-1 gap-4 py-8 px-4 md:px-6 lg:px-24">
        <div className="container mx-auto px-4 md:px-8">
          <h1 className="heading-3xl font-bold mb-6">About This Project</h1>
          <p className="body-md mb-4">
            Philadelphia has a gun violence problem. Clean & Green Philly
            empowers Philadelphians to take action to solve it.
          </p>
          <br></br>
          <div className="flex grid grid-cols-2 mb-2">
            <div className=" flex flex-col justify-center pr-3">
              <h2 className="heading-2xl font-semibold mb-4">
                The Gun Violence Problem
              </h2>
              <p className="body-md mb-4">
                With homicides trending up since 2013, and a record high of 562
                gun deaths in 2021, community members need concrete solutions.
                Many solutions focus on long-term impact, including nearly 80%
                of the City of Philadelphia’s anti-violence spending. But
                immediate, actionable approaches are also needed. 
              </p>
            </div>
            <div className="m-4 flex items-center justify-center">
              <Image
                src="/Graphic-Map-Shootings.png"
                alt="A map of gun crime density in Philadelphia in March of 2023"
              />
            </div>
          </div>
          <div className="flex grid grid-cols-2 my-2">
            <div className=" flex flex-col justify-center pr-3">
              <h2 className="heading-2xl font-semibold mb-4">The Research</h2>
              <p className="body-md mb-4">
                Research shows that greening and cleaning vacant properties is
                one of the most impactful, cost-effective interventions
                available to reduce gun violence in a neighborhood. For example,
                Dr. Eugenia South and her team have demonstrated that greening
                vacant lots in Philadelphia reduced gun violence by as much as
                29% in the surrounding area.
              </p>
            </div>
            <div className="m-4 flex items-center justify-center overflow-hidden">
              <Image
                src="/Graphic-Research.png"
                alt="Excerpts from research on reducing gun violence with vacant lot interventions"
                className="border-1"
              />
            </div>
          </div>
          <div className="flex grid grid-cols-2 my-2">
            <div className=" flex flex-col justify-center pr-3">
              <h2 className="heading-2xl font-semibold mb-4">The Challenge</h2>
              <p className="body-md mb-4">
                Transforming Philadelphia’s vacant lots should be a key strategy
                to combating gun violence here. But in a city with nearly 40,000
                vacant properties, the main obstacle is figuring out which
                properties to prioritize and how to get access to them.
              </p>
            </div>
            <div className="m-4 flex items-center justify-center overflow-hidden">
              <Image
                src="/Graphic-Lots-Streets.png"
                alt="A zoomed in map showing an example of the lots in the interactive map"
              />
            </div>
          </div>
          <div className="flex grid grid-cols-2 my-2">
            <div className=" flex flex-col justify-center pr-3">
              <h2 className="heading-2xl font-semibold mb-4">Our Vision</h2>
              <p className="body-md mb-4">
                Our vision was to empower local residents, non-profit
                organizations, and government stakeholders to find and
                prioritize vacant properties for interventions, understand how
                to transform the properties they’ve identified, and connect
                users to resources that can support them.
              </p>
            </div>
            <div className="m-4 flex items-center justify-center overflow-hidden">
              <Image
                src="/Graphic-Skills.png"
                alt="A graphic of a cluster of green circles with icons representing aspects of the project"
              />
            </div>
          </div>
          <div className="flex grid grid-cols-2 mt-2 mb-6">
            <div className=" flex flex-col justify-center pr-3">
              <h2 className="heading-2xl font-semibold mb-4">
                Our Methodology
              </h2>
              <p className="body-md mb-4">
                We created a dataset based on the original research conducted by
                Dr. Eugenia South and her colleagues, as well as many
                conversations with stakeholders, including community residents,
                CDCs, City government offices, academic researchers, and more.
                We analyzed and combined many data sets on crime, green-space,
                and properties.
              </p>
              <div className="flex items-center">
                <Button
                  href="/methodology"
                  as={Link}
                  className="bg-gray-200 iconLink"
                >
                  <span className="body-md">Learn More</span>
                  <PiArrowRight className="w-5 h-5" />
                </Button>
              </div>
            </div>
            <div className="m-4 flex items-center justify-center overflow-hidden">
              <Image
                src="/Graphic-Merge-Data.png"
                alt="A graphic of a green circle with a grid symbol surrounded by other grid symbols with arrows pointing back to the circle."
              />
            </div>
          </div>
          <div>
            <div className="my-8">
              <h2 className="heading-2xl font-semibold mb-4">Contributors</h2>
              <p className="body-md mb-4">
                Clean & Green Philly was built by a team of Code for Philly
                volunteers. The project was created and led by{" "}
                <a
                  href="https://www.nlebovits.github.io"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link"
                >
                  Nissim Lebovits
                </a>
                .{" "}
                <a
                  href="https://www.willonabike.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link"
                >
                  Will Budreau
                </a>{" "}
                was responsible for user testing and research,{" "}
                <a
                  href="https://www.brandonfcohen.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link"
                >
                  Brandon Cohen
                </a>{" "}
                was the lead developer, and{" "}
                <a
                  href="https://www.nathanielsidwell.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link"
                >
                  {" "}
                  Nathaniel Sidwell
                </a>{" "}
                led the UX team. Thanks, too, to the many other contributors
                along the way.
              </p>
              <p className="body-md mb-4">
                Our efforts have been informed and advanced by local residents,
                community leaders, City staff, faculty at the University of
                Pennsylvania, Temple University, and Thomas Jefferson
                University; and many others. Special thanks are due to the Code
                for Philly leadership, Jon Geeting, Dante Leonard, Mjumbe Poe,
                and Vicky Tam.
              </p>
              <p className="body-md">
                Lastly, we are grateful to Dr. Eugenia South and her colleagues,
                whose work this project depends on.
              </p>
            </div>
            <div className="my-6">
              <h2 className="heading-2xl font-semibold mb-4">Feedback</h2>
              <p className="body-md mb-4">
                If you find issues in this website or would like to offer us
                feedback, please reach out to us at{" "}
                <a
                  href="mailto:cleanandgreenphl@gmail.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link"
                >
                  cleanandgreenphl@gmail.com.
                </a>
                 {" "}
              </p>
            </div>
            <div className="my-6">
              <h2 className="heading-2xl font-semibold mb-4">
                Removing Properties
              </h2>
              <p className="body-md mb-4">
                If you find issues If you would like to request that we remove a
                property from the dashboard, please see our 
                <a href="/request-removal" className="link">
                  Request Removal
                </a>{" "}
                page in this website or would like to offer us feedback, please
                reach out to us at 
                <a
                  href="mailto:cleanandgreenphl@gmail.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link"
                >
                  cleanandgreenphl@gmail.com.
                </a>{" "}
                 {" "}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
