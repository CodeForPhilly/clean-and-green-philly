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

  const { access_process, address, tree_canopy_gap, market_value, neighborhood, open_violations_past_year, owner_1, owner_2, priority_level, guncrime_density, total_due, zipcode, OPA_ID } = properties;
  const image = `https://storage.googleapis.com/cleanandgreenphilly/${OPA_ID}.jpg`;
  const atlasUrl = `https://atlas.phila.gov/${address}`;

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
        <div className="py-4 px-2">
          <h2 className="font-bold text-2xl">{address}</h2>
          <a href={atlasUrl} target="_blank" rel="noopener noreferrer">Atlas Info</a>
        </div>
        <div className="flex">
          <div className="p-2 flex-grow">
            <table>
              <tbody>
                <tr>
                  <th scope="row" className="table-cell">Neighborhood</th>
                  <td className="table-cell">{neighborhood}</td>
                </tr>
                <tr>
                  <th scope="row" className="table-cell">Gun Crime Rate</th>
                  <td className="table-cell">{guncrime_density}</td>
                </tr>
                <tr>
                  <th scope="row" className="table-cell">Tree Canopy Gap</th>
                  <td className="table-cell">{Math.round(tree_canopy_gap * 100)}%</td>
                </tr>
                <tr>
                  <th scope="row" className="table-cell">Suggested Priority</th>
                  <td className="table-cell">{priority_level}</td>
                </tr>
                <tr>
                  <th scope="row" className="table-cell">L&I Violations</th>
                  <td className="table-cell">{open_violations_past_year}</td>
                </tr>
                <tr>
                  <th scope="row" className="table-cell">Tax delinquency</th>
                  <td className="table-cell">{total_due ? 'Yes' : 'No'}</td>
                </tr>
                <tr>
                  <th scope="row" className="table-cell">Access Process</th>
                  <td className="table-cell">{access_process}</td>
                </tr>
                <tr>
                  <th scope="row" className="table-cell">Zip Code</th>
                  <td className="table-cell">{zipcode}</td>
                </tr>
                <tr>
                  <th scope="row" className="table-cell">Market Value</th>
                  <td className="table-cell">${market_value.toLocaleString()}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="p-2 flex-grow">
            <h3 className="pb-1 font-bold text-lg">Owner</h3>
            <div className="pb-3">
              <p>{owner_1}</p>
              <p>{owner_2}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SinglePropertyDetail;
