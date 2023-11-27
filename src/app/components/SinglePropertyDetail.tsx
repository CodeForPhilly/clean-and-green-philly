import React from "react";
import { Button } from "@nextui-org/react";
import { MapboxGeoJSONFeature } from "mapbox-gl";

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

  return (
    <div className="max-w-sm w-full md:w-1/2 p-4">
      <Button onClick={() => setSelectedProperty(null)}> Back </Button>
      <div className="bg-white rounded-lg overflow-hidden">
        <div className="relative h-48 w-full rounded-lg overflow-hidden">
          <img
            src="https://images.unsplash.com/photo-1612839905599-2b3f8f3e3d2a?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cHJvcGVydGllcyUyMHRvJTIwYmFjayUyMHN0YXRpb25zJTIwYW5kJTIwY2FuYXBpJTIwZ2FtZXN8ZW58MHx8MHx8&ixlib=rb-1.2.1&w=1000&q=80"
            alt={`Property at ${properties.ADDRESS}`}
            className="absolute h-full w-full object-cover"
          />
        </div>
        <div className="p-4">
          <div className="font-bold text-xl">{properties.ADDRESS}</div>
          <div className="text-gray-700 mb">{`Guncrime Density: ${properties.guncrime_density}`}</div>
        </div>
        <div className="px-4 pb-2">
          <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
            High Priority
          </span>
        </div>
      </div>
    </div>
  );
};

export default SinglePropertyDetail;
