import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import { Chip, Tooltip, Link } from "@nextui-org/react";
import {
  ArrowLeft,
  ArrowSquareOut,
  ArrowsOut,
  Share,
} from "@phosphor-icons/react";
import { MapGeoJSONFeature } from "maplibre-gl";
import Image from "next/image";
import { Dispatch, SetStateAction, useState } from "react";
import PropertyAccessOptionContainer from "./PropertyAccessOptionContainer";
import { ThemeButton, ThemeButtonLink } from "./ThemeButton";
import ContentCard from "./ContentCard";
import cleanup from "@/images/transform-a-property.png";

interface PropertyDetailProps {
  property: MapGeoJSONFeature | null;
  setSelectedProperty: (property: MapGeoJSONFeature | null) => void;
  setIsStreetViewModalOpen: Dispatch<SetStateAction<boolean>>;
  updateCurrentView: (view: BarClickOptions) => void;
}

function getPriorityClass(priorityLevel: string) {
  switch (priorityLevel) {
    case "High":
      return "bg-red-200 text-red-800"; // Style for High Priority
    case "Medium":
      return "bg-yellow-200 text-yellow-800"; // Style for Medium Priority
    case "Low":
      return "bg-green-200 text-green-800"; // Style for Low Priority
    default:
      return "bg-gray-500 border-gray-700"; // Default style
  }
}

const SinglePropertyDetail = ({
  property,
  setSelectedProperty,
  setIsStreetViewModalOpen,
  updateCurrentView,
}: PropertyDetailProps) => {
  const [shareLabel, setShareLabel] = useState<boolean>(false);
  const [hover, setHover] = useState<boolean>(false);

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
    rco_names,
    zoning_base_district,
    priority_level,
    total_due,
    tree_canopy_gap,
    zipcode,
    OPA_ID,
  } = properties;
  const image = `https://storage.googleapis.com/cleanandgreenphl/${OPA_ID}.jpg`;
  const atlasUrl = `https://atlas.phila.gov/${address}`;
  const priorityClass = getPriorityClass(priority_level);

  const priorityBgClassName = priority_level.includes("High")
    ? "bg-red-200 text-red-800"
    : priority_level.includes("Medium")
    ? "bg-priority-medium"
    : priority_level.includes("Low")
    ? "bg-priority-low"
    : "";

  const Th = ({ children }: { children: React.ReactNode }) => (
    <th scope="row" className="table-cell whitespace-nowrap w-1/3">
      {children}
    </th>
  );

  return (
    <div className="w-full px-6 pb-6">
      <div className="flex justify-between sticky top-0 py-4 z-10 bg-white">
        <ThemeButton
          color="tertiary"
          label="Back"
          startContent={<ArrowLeft />}
          onPress={() => {
            setSelectedProperty(null);
            updateCurrentView("detail");
            history.replaceState(null, "", `/find-properties`);
          }}
        />
        <Tooltip
          disableAnimation
          closeDelay={100}
          placement="top"
          content={shareLabel ? "Link Copied" : "Copy Link"}
          isOpen={hover}
          classNames={{
            content: "bg-gray-900 rounded-[14px] text-white relative top-1",
          }}
        >
          <ThemeButton
            color="tertiary"
            label="Share"
            startContent={<Share />}
            onPress={() => {
              navigator.clipboard.writeText(window.location.href);
              setShareLabel(true);
            }}
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
          />
        </Tooltip>
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
          <button
            className="absolute top-4 right-4 bg-white p-[10px] rounded-md hover:bg-gray-100"
            onClick={() => setIsStreetViewModalOpen(true)}
            aria-label="Open full screen street view map"
            id="outside-iframe-element"
          >
            <ArrowsOut color="#3D3D3D" size={24} />
          </button>
        </div>
      </div>
      <div className="py-4 px-2">
        <div className="flex justify-between content-center">
          <h2
            className="font-bold heading-2xl"
            style={{
              textTransform: "capitalize",
            }}
          >
            {address.toLowerCase()}
          </h2>
          <div>
            <ThemeButtonLink
              href={atlasUrl}
              target="_blank"
              rel="noopener noreferrer"
              color="tertiary"
              label="Atlas"
              endContent={<ArrowSquareOut aria-hidden="true" />}
            />
          </div>
        </div>
      </div>

      <table aria-label="Community Impact" className="w-full mb-3">
        <tbody
          style={{
            fontSize: "16px",
          }}
        >
          <tr>
            <Th>Suggested Priority</Th>
            <td className="table-cell">
              <div className="flex gap-1 items-center">
                <Chip
                  classNames={{
                    base: `${priorityClass} border-small border-white/50`,
                    content: "body-sm",
                  }}
                >
                  {priority_level + " Priority"}
                </Chip>
              </div>
            </td>
          </tr>
          <tr>
            <Th>Gun Crime Rate</Th>
            <td className="table-cell">{guncrime_density}</td>
          </tr>
          <tr>
            <Th>Tree Canopy Gap</Th>
            <td className="table-cell">{Math.round(tree_canopy_gap * 100)}%</td>
          </tr>
        </tbody>
      </table>

      <table aria-label="Land Information" className="w-full mb-4">
        <tbody>
          <tr>
            <Th>Access Process</Th>
            <td className="table-cell">{access_process}</td>
          </tr>
          <tr>
            <Th>Owner</Th>
            <td className="table-cell">
              <p>{owner_1}</p>
              {owner_2 && <p>{owner_2}</p>}
            </td>
          </tr>
          <tr>
            <Th>Zip Code</Th>
            <td className="table-cell">{zipcode}</td>
          </tr>
          <tr>
            <Th>Neighborhood</Th>
            <td className="table-cell">{neighborhood}</td>
          </tr>
          <tr>
            <Th>RCO</Th>
            <td className="table-cell">{rco_names.split("|").join(", ")}</td>
          </tr>
          <tr>
            <Th>Zoning</Th>
            <td className="table-cell">{zoning_base_district}</td>
          </tr>
          <tr>
            <Th>Council District</Th>
            <td className="table-cell">{council_district}</td>
          </tr>
          <tr>
            <Th>Market Value</Th>
            <td className="table-cell">${market_value}</td>
          </tr>
          <tr>
            <Th>Tax Delinquency</Th>
            <td className="table-cell">{total_due ? "Yes" : "No"}</td>
          </tr>
          <tr>
            <Th>L&I Violations</Th>
            <td className="table-cell">{open_violations_past_year}</td>
          </tr>
        </tbody>
      </table>

      <h3 className="font-bold mb-2 py-2 heading-xl">Getting Access</h3>
      <p className="mb-4">
        Before you can transform this property, you need to get legal access to
        it. Here are the possible options for this property including which are
        available, not available and likely the best option.{" "}
        <Link href="/get-access" className="link">
          Learn more on Get Access.
        </Link>
      </p>

      <div className="mb-4">
        <PropertyAccessOptionContainer property={properties} />
      </div>

      <h3 className="font-bold mb-2 py-2 heading-xl">Transform a Property</h3>
      <Link
        href="/transform-property"
        color="foreground"
        className="hover:opacity-100"
      >
        <ContentCard
          image={cleanup}
          alt=""
          title="Transform a Property"
          body="We guide you through the most common, convenient and affordable ways to transform properties and resources on how to do it."
          hasArrow={true}
        />
      </Link>

      {/*
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
      */}

      <h3 className="font-bold mb-2 py-2 heading-xl">Remove This Property</h3>
      <p>
        If you would like to request that we remove this property from the
        dashboard, please see our{" "}
        <a href="/request-removal" className="link">
          Request Removal page
        </a>
        .
      </p>
    </div>
  );
};

export default SinglePropertyDetail;
