import React from "react";
import Image from "next/image";
import { Chip } from "@nextui-org/react";

interface PropertyCardProps {
  feature: any;
  setSelectedProperty: (feature: any) => void;
}

const PropertyCard = ({ feature, setSelectedProperty }: PropertyCardProps) => {
  const { address, guncrime_density, tree_canopy_gap, priority_level, OPA_ID } =
    feature.properties;

  const roundedCanopyGap = Math.round(tree_canopy_gap * 100);
  const image = `https://storage.googleapis.com/cleanandgreenphilly/${OPA_ID}.jpg`;
  const atlasUrl = `https://atlas.phila.gov/${address}`;

  return (
    <div
      className="max-w-sm w-full md:w-1/2 p-4 cursor-pointer"
      onClick={() => setSelectedProperty(feature)}
    >
      <div className="max-w-sm w-full p-4">
        <div className="bg-white rounded-lg overflow-hidden">
          <div className="relative h-48 w-full rounded-lg overflow-hidden">
            <Image
              src={image}
              alt={`Property at ${address}`}
              layout="fill"
              objectFit="cover"
            />
          </div>
          <div className="p-4">
            <div className="font-bold text-xl">{address}</div>
            <div className="text-gray-700 mb">
              {guncrime_density} Crime Rate, {roundedCanopyGap}% Canopy Gap
            </div>
            <a href={atlasUrl} target="_blank" rel="noopener noreferrer">
              Click here for Atlas Info
            </a>
          </div>
          <div className="px-4 pb-2">
            <Chip color="success" variant="solid" size="sm">
              {priority_level}
            </Chip>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;
