import React from "react";
import Image from "next/image";
import { Chip } from "@nextui-org/react";

interface PropertyCardProps {
  feature: any;
  setSelectedProperty: (feature: any) => void;
}

const PropertyCard = ({ feature, setSelectedProperty }: PropertyCardProps) => {
  // Destructuring properties directly from feature if feature.properties is not present
  const { ADDRESS, guncrime_density, tree_canopy_gap } = feature.properties || feature;
  const roundedCanopyGap = Math.round(tree_canopy_gap * 100);
  const randomImage = `/image1.jpg`;

  return (
    <div
      className="max-w-sm w-full md:w-1/2 p-4 cursor-pointer"
      onClick={() => setSelectedProperty(feature)}
    >
      <div className="max-w-sm w-full p-4">
        <div className="bg-white rounded-lg overflow-hidden">
          <div className="relative h-48 w-full rounded-lg overflow-hidden">
            <Image
              src={randomImage}
              alt={`Property at ${ADDRESS}`}
              layout="fill"
              objectFit="cover"
            />
          </div>
          <div className="p-4">
            <div className="font-bold text-xl">{ADDRESS}</div>
            <div className="text-gray-700 mb">
              {guncrime_density} Crime Rate, {roundedCanopyGap}% Canopy Gap
            </div>
          </div>
          <div className="px-4 pb-2">
            <Chip color="success" variant="solid" size="sm">
              High Priority
            </Chip>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;
