import { Button } from "@nextui-org/react";
import { useState } from "react";

const RecommendedActions = () => {
  const [isExpanded, setIsExpanded] = useState({
    canDo: false,
    getHelp: false,
    thinkAbout: false,
  });

  // Function to toggle the expansion state of a section
  const toggleSection = (sectionName) => {
    setIsExpanded({
      ...isExpanded,
      [sectionName]: !isExpanded[sectionName],
    });
  };

  return (
    <div className="container mx-auto pt-20 h-screen">
      <div className="text-left text-2xl my-10">
        <h1 className="text-4xl font-bold mb-4">Take Action</h1>

        <div className="mb-4">
          <h2 className="text-2xl font-bold">
            What can I do?
            <Button
              type="ghost"
              onClick={() => toggleSection("canDo")}
              size="small"
              className={`ml-2 border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white ${
                isExpanded["canDo"] ? "bg-blue-500 text-white" : ""
              }`}
            >
              {isExpanded["canDo"] ? "Collapse" : "Expand"}
            </Button>
          </h2>
          {isExpanded["canDo"] && (
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
          )}
        </div>

        <div className="mb-4">
          <h2 className="text-2xl font-bold">
            Where can I get help?
            <Button
              type="ghost"
              onClick={() => toggleSection("getHelp")}
              size="small"
              className={`ml-2 border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white ${
                isExpanded["getHelp"] ? "bg-blue-500 text-white" : ""
              }`}
            >
              {isExpanded["getHelp"] ? "Collapse" : "Expand"}
            </Button>
          </h2>
          {isExpanded["getHelp"] && (
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
          )}
        </div>

        <div className="mb-4">
          <h2 className="text-2xl font-bold">
            What else should I think about?
            <Button
              type="ghost"
              onClick={() => toggleSection("thinkAbout")}
              size="small"
              className={`ml-2 border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white ${
                isExpanded["thinkAbout"] ? "bg-blue-500 text-white" : ""
              }`}
            >
              {isExpanded["thinkAbout"] ? "Collapse" : "Expand"}
            </Button>
          </h2>
          {isExpanded["thinkAbout"] && (
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
          )}
        </div>

        <div className="flex justify-between space-x-2.5">
          {/* Add buttons or other UI elements here */}
        </div>
      </div>
    </div>
  );
};

export default RecommendedActions;
