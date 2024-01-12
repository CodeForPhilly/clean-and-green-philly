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

  const { access_process, address, tree_canopy_gap, neighborhood, owner_1, owner_2, priority_level, guncrime_density, zipcode, OPA_ID } = properties;
  const image = `https://storage.googleapis.com/cleanandgreenphilly/${OPA_ID}.jpg`;

  return (
    <div className="w-full p-4">
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
          <h2 className="font-bold text-2xl">{address}</h2>
        </div>
        <div className="flex">
          <div className="p-2">
            <table>
            <tbody>
              <tr>
                <th className="text-left font-normal">Neighborhood</th>
                <td>{neighborhood}</td>
              </tr>
              <tr>
                <th className="text-left font-normal">Gun Crime Rate</th>
                <td>{guncrime_density}</td>
              </tr>
              <tr>
                <th className="text-left font-normal">Drug Crime</th>
                <td>???</td>
              </tr>
              <tr>
                <th className="text-left font-normal">Tree Canopy Gap</th>
                <td>{tree_canopy_gap}</td>
              </tr>
              <tr>
                <th className="text-left font-normal">Suggested Priority</th>
                <td>{priority_level}</td>
              </tr>
              <tr>
                <th className="text-left font-normal">L&I Violations</th>
                <td>???</td>
              </tr>
              <tr>
                <th className="text-left font-normal">Tax delinquency</th>
                <td>???</td>
              </tr>
              <tr>
                <th className="text-left font-normal">Acquisition Process</th>
                <td>{access_process}</td>
              </tr>
              <tr>
                <th className="text-left font-normal">Zip Code</th>
                <td>{zipcode}</td>
              </tr>
            </tbody>
            </table>
          </div>
          <div className="p-2">
            <h3 className="pb-1 font-bold text-lg">Owner</h3>
            <div className="pb-2">
              <p>{owner_1}</p>
              <p>{owner_2}</p>
            </div>
            <h3 className="pb-1 font-bold text-lg">Relevant Info</h3>
            <p className="pb-2">weeeee</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SinglePropertyDetail;
