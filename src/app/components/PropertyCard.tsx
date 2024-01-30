import Image from "next/image";
import { Chip } from "@nextui-org/react";

interface PropertyCardProps {
  feature: any;
  setSelectedProperty: (feature: any) => void;
}

function toTitleCase(str: string) {
  return str
    .toLowerCase()
    .split(" ")
    .map(function (word) {
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}

function getPriorityClass(priorityLevel: string) {
  switch (priorityLevel) {
    case "High":
      return "bg-red-500 border-red-700"; // Style for High Priority
    case "Medium":
      return "bg-yellow-500 border-yellow-700"; // Style for Medium Priority
    case "Low":
      return "bg-green-500 border-green-700"; // Style for Low Priority
    default:
      return "bg-gray-500 border-gray-700"; // Default style
  }
}

const PropertyCard = ({ feature, setSelectedProperty }: PropertyCardProps) => {
  const { address, guncrime_density, tree_canopy_gap, priority_level, OPA_ID } =
    feature.properties;

  const image = `https://storage.googleapis.com/cleanandgreenphilly/${OPA_ID}.jpg`;
  const formattedAddress = toTitleCase(address);
  const priorityClass = getPriorityClass(priority_level);

  return (
    <div
      className="max-w-sm w-full md:w-1/2 p-2 cursor-pointer"
      onClick={() => setSelectedProperty(feature)}
    >
      <div className="max-w-sm w-full p-4">
        <div className="bg-white rounded-md overflow-hidden">
          <div
            className="relative w-full rounded-lg overflow-hidden"
            style={{ height: "160px", width: "auto" }}
          >
            <Image
              src={image}
              alt={`Property at ${formattedAddress}`}
              layout="fill"
              objectFit="cover"
              unoptimized
            />
          </div>
          <div className="p-2">
            <div className="font-bold text-lg">{formattedAddress}</div>
            <div className="text-gray-700 mb">
              {guncrime_density} Gun Crime Rate
            </div>
          </div>
          <div className="px-1">
            <Chip
              classNames={{
                base: `${priorityClass} border-small border-white/50`,
                content: "text-white mb",
              }}
            >
              {priority_level + " Priority"}
            </Chip>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;
