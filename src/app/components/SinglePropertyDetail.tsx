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

  const {
    access_process,
    address,
    council_district,
    guncrime_density,
    market_value,
    neighborhood,
    open_violations_past_year,
    owner_1,
    owner_2,
    priority_level,
    total_due,
    tree_canopy_gap,
    zipcode,
    OPA_ID,
  } = properties;
  const image = `https://storage.googleapis.com/cleanandgreenphilly/${OPA_ID}.jpg`;
  const atlasUrl = `https://atlas.phila.gov/${address}`;

  return (
    <div className="w-full p-4">
      <div className="pb-4">
        <Button onClick={() => setSelectedProperty(null)}> Back </Button>
      </div>
      <div className="bg-white rounded-lg overflow-hidden">
        <div className="relative h-48 w-full rounded-lg overflow-hidden">
          <Image
            src={image}
            alt={`Property at ${address}`}
            layout="fill"
            objectFit="cover"
            unoptimized
          />
        </div>
      </div>
      <div className="py-4 px-2">
        <div className="flex justify-between content-center">
          <h2 className="font-bold text-2xl">{address}</h2>
        </div>
        <div style={{ textAlign: "left", marginTop: "1em" }}>
          <Button
            as="a"
            href={atlasUrl}
            target="_blank"
            rel="noopener noreferrer"
            color="primary"
          >
            View this property on Atlas
          </Button>
        </div>
      </div>
      <table className="w-full">
        <tbody>
          <tr>
            <th scope="row" className="table-cell">
              Suggested Priority
            </th>
            <td className="table-cell">{priority_level}</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Gun Crime Rate
            </th>
            <td className="table-cell">{guncrime_density}</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Tree Canopy Gap
            </th>
            <td className="table-cell">{Math.round(tree_canopy_gap * 100)}%</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Access Process
            </th>
            <td className="table-cell">{access_process}</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Owner
            </th>
            <td className="table-cell">
              <p>{owner_1}</p>
              {owner_2 && <p>{owner_2}</p>}
            </td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Zip Code
            </th>
            <td className="table-cell">{zipcode}</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Neighborhood
            </th>
            <td className="table-cell">{neighborhood}</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Council District
            </th>
            <td className="table-cell">{council_district}</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Market Value
            </th>
            <td className="table-cell">${market_value.toLocaleString()}</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              Tax delinquency
            </th>
            <td className="table-cell">{total_due ? "Yes" : "No"}</td>
          </tr>
          <tr>
            <th scope="row" className="table-cell">
              L&I Violations
            </th>
            <td className="table-cell">{open_violations_past_year}</td>
          </tr>
        </tbody>
      </table>
      <p className="font-bold mt-4 py-2">Remove This Property</p>
      <p>
        If you would like to request that we remove this property from the
        dashboard, please see our{" "}
        <a href="/request-removal" className="text-primary">
          Request Removal page
        </a>
        .
      </p>
    </div>
  );
};

export default SinglePropertyDetail;
