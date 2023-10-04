import { Accordion, AccordionItem, Button } from "@nextui-org/react";
import { get } from "http";

export default function App() {
  const defaultContent =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.";

    const cleaningGreeningContent = (
      <div>
        <ul className="list-disc pl-6 mb-6">
          <li>Removing trash and debris</li>
          <li>Grading the land</li>
          <li>Planting a small number of trees to create a park-like setting</li>
          <li>
            Installing low-perimeter (about 1 meter high) fences with multiple
            ungated entrances to encourage use
          </li>
          <li>Regularly maintaining the lot</li>
        </ul>
        <p>
          <a
            href="https://detroitfuturecity.com/whatwedo/land-use/DFC-lots/lot-types/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            Learn more about potential interventions in different types of lots
          </a>
        </p>
      </div>
    );

    const getHelpContent = (
      <p>
      To carry out something like this, try getting in touch with your local
      Neighborhood Advisory Committee, a nearby Community Development
      Corporation, or your local representative. Explain to them what you
      want to do and why. Show them this map to support your explanation!
      <a
          href="https://phdcphila.org/land/buy-land/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 hover:underline"
      >
      Get help purchasing properties from PHDC
      </a>
    </p>
    )
    
    const thinkAboutContent = (
      <div>
        <p>
          Be mindful of trespassing on private property. You can use the
          dashboard tool above to identify which lots are privately owned.
          Consider reaching out to a lot owner and explaining why you want
          to carry out a lot cleanup in order to get permission.
        </p>
        <p>
          Lastly, you can also use these data to convince your NAC, CDC,
          elected official, or another organization to take action. If you
          are interested in getting specific data that were used to build
          this tool, contact me and let me know how I can help.
        </p>
      </div>
    );


  return (
    <div className="container mx-auto pt-20 h-screen">
      <h1 className="text-4xl font-bold mb-8">Take Action</h1>

      <h2 className="text-2xl font-bold">What can I do?</h2>

      <Accordion variant="light">

      <AccordionItem key="1" aria-label="Cleaning and Greening" title="Cleaning and Greening" className="text-3xl font-bold">
      <div className="text-base font-normal">
        {cleaningGreeningContent}
      </div>
      </AccordionItem>

      <AccordionItem key="2" aria-label="Affordable Housing" title="Affordable Housing" className="text-3xl font-bold">
      <div className="text-base font-normal">
        {defaultContent}
      </div>
      </AccordionItem>

      <AccordionItem key="3" aria-label="Tactical Urbanism" title="Tactical Urbanism" className="text-3xl font-bold">
      <div className="text-base font-normal">
        {defaultContent}
      </div>
      </AccordionItem>

      <AccordionItem key="4" aria-label="Other Interventions" title="Other Interventions" className="text-3xl font-bold">
      <div className="text-base font-normal">
        {defaultContent}
      </div>
      </AccordionItem>

      </Accordion>

      <div className="mt-4"></div> {/* Add extra space here */}

      <h2 className="text-2xl font-bold">Where can I get help?</h2>

      <Accordion variant="light">

        <AccordionItem key="1" aria-label="PHDC" title="PHDC" className="text-3xl font-bold">
        <div className="text-base font-normal">
          {getHelpContent}
        </div>
        </AccordionItem>

        <AccordionItem key="2" aria-label="Legal Help" title="Legal Help" className="text-3xl font-bold">
        <div className="text-base font-normal">
          {defaultContent}
        </div>
        </AccordionItem>

        <AccordionItem key="3" aria-label="Financial Help" title="Financial Help" className="text-3xl font-bold">
        <div className="text-base font-normal">
          {defaultContent}
        </div>
        </AccordionItem>

        <AccordionItem key="4" aria-label="Design Help" title="Design Help" className="text-3xl font-bold">
        <div className="text-base font-normal">
          {defaultContent}
        </div>
        </AccordionItem>

      </Accordion>

      <div className="mt-4"></div> {/* Add extra space here */}

      <h2 className="text-2xl font-bold">What should I think about?</h2>

      <Accordion variant="light">
        <AccordionItem key="1" aria-label="Funding" title="Funding" className="text-3xl font-bold">
        <div className="text-base font-normal">
          {thinkAboutContent}
        </div>
        </AccordionItem>

        <AccordionItem key="2" aria-label="Maintenance" title="Maintenance" className="text-3xl font-bold">
        <div className="text-base font-normal">
          {defaultContent}
        </div>
        </AccordionItem>

        <AccordionItem key="3" aria-label="Gentrification" title="Gentrification" className="text-3xl font-bold">
        <div className="text-base font-normal">
          {defaultContent}
        </div>
        </AccordionItem>
      </Accordion>
    </div>
  );
}





