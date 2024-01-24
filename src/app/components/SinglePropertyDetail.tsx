import React from "react";
import { Button } from "@nextui-org/react";
import { MapboxGeoJSONFeature } from "mapbox-gl";
import Image from "next/image";
import { ArrowSquareOut, Broom, HandWaving, Handshake, Money, PottedPlant, Tree } from "@phosphor-icons/react";
import SinglePropertyInfoCard from "./SinglePropertyInfoCard";

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
    parcel_type,
    priority_level,
    total_due,
    tree_canopy_gap,
    zipcode,
    OPA_ID,
  } = properties;
  const image = `https://storage.googleapis.com/cleanandgreenphilly/${OPA_ID}.jpg`;
  const atlasUrl = `https://atlas.phila.gov/${address}`;

  const priorityBgClassName = priority_level.includes('High') ? 'bg-priority-high'
    : priority_level.includes('Medium') ? 'bg-priority-medium'
    : priority_level.includes('Low') ? 'bg-priority-low' : '';

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
          <div>
            <a
              href={atlasUrl}
              target="_blank"
              rel="noopener noreferrer"
              color="primary"
              className="flex p-2 items-center gap-1"
            >
              Atlas Link
              <ArrowSquareOut className="inline h-6 w-6" aria-hidden="true" />
            </a>
          </div>
        </div>
      </div>

      <table className="w-full mb-3">
        <tbody>
          <tr>
            <th scope="row" className="table-cell w-3/12">
              Suggested Priority
            </th>
            <td className="table-cell">
              <div className="flex gap-1 items-center">
                <span className={`inline-block w-4 h-4 ${priorityBgClassName}`} />
                {priority_level}
              </div>
            </td>
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
        </tbody>
      </table>

      <table className="w-full mb-4">
        <tbody>
          <tr>
            <th scope="row" className="table-cell w-3/12">
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
              Parcel Type
            </th>
            <td className="table-cell">
              <p>{parcel_type}</p>
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
              RCO
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
              Tax Delinquency
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

      <h3 className="font-bold mb-2 py-2 text-xl">Ways to transform the lot</h3>
      <p className="mb-4">
        How do you envision transforming the lot?  The type of change you want to make will guide the access you need.  Here are a couple of possible options for this lot.  Learn more.&nbsp;
        <a href="/transform-property"><Tree className="inline h-6 w-6" aria-hidden="true" />Transform a Property</a>
      </p>

      <div className="flex mb-4 px-2 gap-4">
        <SinglePropertyInfoCard
          title="Lot Cleanup"
          body="In a day, clean up with a street crew and PHS!"
          icon={<Broom className="h-12 w-12" aria-hidden="true" />}
        />
        <SinglePropertyInfoCard
          title="Community Garden"
          body="Set up a longer term, sustainable green space."
          icon={<PottedPlant className="h-12 w-12" aria-hidden="true" />}
        />
      </div>

      <h3 className="font-bold mb-2 py-2 text-xl">Getting Access</h3>
      <p className="mb-4">
        Based on the information about this property we'd recommend these actions.  Learn more at <a href="/get-access"><HandWaving className="inline h-6 w-6" aria-hidden="true" />Gain Access</a>
      </p>

      <div className="flex mb-4 px-2 gap-4">
        <SinglePropertyInfoCard
          title="Private Use Agreement"
          body="Make an agreement with the property owner."
          icon={<Handshake className="h-12 w-12" aria-hidden="true" />}
        />
        <SinglePropertyInfoCard
          title="Buying a Property"
          body="Buying a property outright can be the simplest way."
          icon={<Money className="h-12 w-12" aria-hidden="true" />}
        />
      </div>

      <h3 className="font-bold mb-2 py-2 text-xl">Remove This Property</h3>
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
