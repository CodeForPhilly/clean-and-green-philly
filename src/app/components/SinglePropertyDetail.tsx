import React from "react";
import { Button } from "@nextui-org/react";
import { MapboxGeoJSONFeature } from "mapbox-gl";
import Image from "next/image";

interface PropertyDetailProps {
  property: MapboxGeoJSONFeature | null;
  setSelectedProperty: (property: MapboxGeoJSONFeature | null) => void;
}

const SinglePropertyDetail = ({
  property,
  setSelectedProperty,
}: PropertyDetailProps) => {
  if (!property) return null;
  const { properties } = property;
  if (!properties) return null;

  const { address, priority_level, guncrime_density, OPA_ID } = properties;
  const image = `https://storage.googleapis.com/cleanandgreenphilly/${OPA_ID}.jpg`;

  return (
    <div className="max-w-sm w-full md:w-1/2 p-4">
      <Button onClick={() => setSelectedProperty(null)}> Back </Button>
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
          <div className="text-gray-700 mb">{`Guncrime Density: ${guncrime_density}`}</div>
        </div>
        <div className="px-4 pb-2">
          <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
            {priority_level}
          </span>
        </div>
      </div>
    </div>
  );
};

export default SinglePropertyDetail;
