import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import { Chip, Tooltip, Link } from "@nextui-org/react";
import {
  ArrowLeft,
  BookmarkSimple,
  ArrowSquareOut,
  ArrowsOut,
  Share,
} from "@phosphor-icons/react";
import { MapGeoJSONFeature } from "maplibre-gl";
import Image from "next/image";
import { Dispatch, SetStateAction, useEffect, useState } from "react";
import PropertyAccessOptionContainer from "./PropertyAccessOptionContainer";
import { ThemeButton, ThemeButtonLink } from "./ThemeButton";
import ContentCard from "./ContentCard";
import cleanup from "@/images/transform-a-property.png";
import { PiEyeSlash } from "react-icons/pi";
import { useFilter } from "@/context/FilterContext";
import { getPropertyIdsFromLocalStorage } from "@/utilities/localStorage";

interface PropertyDetailProps {
  property: MapGeoJSONFeature | null;
  setSelectedProperty: (property: MapGeoJSONFeature | null) => void;
  setIsStreetViewModalOpen: Dispatch<SetStateAction<boolean>>;
  shouldFilterSavedProperties: boolean;
  setShouldFilterSavedProperties: (shouldFilter: boolean) => void;
  updateCurrentView: (view: BarClickOptions) => void;
}

interface PropertyIdLocalStorage {
  count: number;
  opa_ids: {
    [key: string]: any;
  };
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
  shouldFilterSavedProperties,
  setShouldFilterSavedProperties,
  updateCurrentView,
}: PropertyDetailProps) => {
  const { dispatch } = useFilter();

  const [shareLabel, setShareLabel] = useState<boolean>(false);
  const [hover, setHover] = useState<boolean>(false);
  const [isPropertySavedToLocalStorage, setIsPropertySavedToLocalStorage] =
    useState(false);

  useEffect(() => {
    if (!localStorage.getItem("opa_ids")) {
      initializeLocalStorage();
    }

    const localStorageData = localStorage.getItem("opa_ids");
    const parsedLocalStorageData = localStorageData
      ? JSON.parse(localStorageData)
      : {};

    const propertyId = parsedLocalStorageData.opa_ids[OPA_ID];
    propertyId
      ? setIsPropertySavedToLocalStorage(true)
      : setIsPropertySavedToLocalStorage(false);
  }, []);

  if (!property) return null;
  const { properties } = property;
  if (!properties) return null;

  const {
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
    phs_partner_agency,
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

  const savePropertyIdToLocalStorage = (localCache: PropertyIdLocalStorage) => {
    let newLocalCache: PropertyIdLocalStorage = {
      ...localCache,
    };
    newLocalCache.opa_ids[OPA_ID] = OPA_ID;
    newLocalCache.count++;
    localStorage.setItem("opa_ids", JSON.stringify(newLocalCache));
  };

  const removePropertyIdFromLocalStorage = (
    localStorageData: PropertyIdLocalStorage
  ) => {
    delete localStorageData.opa_ids[OPA_ID];
    localStorageData.count--;
    localStorage.setItem("opa_ids", JSON.stringify(localStorageData));
  };

  const initializeLocalStorage = () => {
    let opa_ids: PropertyIdLocalStorage = {
      count: 0,
      opa_ids: {},
    };

    localStorage.setItem("opa_ids", JSON.stringify(opa_ids));
  };

  const onClickSaveButton = () => {
    const localStorageData = localStorage.getItem("opa_ids");
    const parsedLocalStorageData = localStorageData
      ? JSON.parse(localStorageData)
      : {};

    if (parsedLocalStorageData.opa_ids[OPA_ID]) {
      removePropertyIdFromLocalStorage(parsedLocalStorageData);
      setIsPropertySavedToLocalStorage(false);

      if (parsedLocalStorageData.count === 0) {
        dispatch({
          type: "SET_DIMENSIONS",
          property: "OPA_ID",
          dimensions: [],
        });
        setShouldFilterSavedProperties(false);
      } else {
        if (shouldFilterSavedProperties) {
          let propertyIds = getPropertyIdsFromLocalStorage();
          dispatch({
            type: "SET_DIMENSIONS",
            property: "OPA_ID",
            dimensions: [...propertyIds],
          });
        }
      }
    } else {
      savePropertyIdToLocalStorage(parsedLocalStorageData);
      setIsPropertySavedToLocalStorage(true);
    }
  };

  return (
    <div className="w-full px-6 pb-6">
      <div className="flex justify-between sticky -mx-6 px-6 top-0 py-4 z-10 bg-white">
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

        {/* Right-aligned content: Buttons */}
        <div className="flex items-center">
          <ThemeButton
            color="tertiary"
            label={isPropertySavedToLocalStorage ? "Saved" : "Save"}
            startContent={<BookmarkSimple />}
            onPress={() => {
              onClickSaveButton();
            }}
            isSelected={isPropertySavedToLocalStorage}
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

      <PropertyDetailTable
        tableLabel="Community Impact"
        rows={[
          {
            label: "Gun Crime Rate",
            content: guncrime_density,
          },
          {
            label: "Tree Canopy Gap",
            content: `${Math.round(tree_canopy_gap * 100)}%`,
          },
          {
            label: "L&I Violations",
            content: open_violations_past_year,
          },
          {
            label: "PHS LandCare",
            content: phs_partner_agency,
          },
          {
            label: "Suggested Priority",
            content: (
              <Chip
                classNames={{
                  base: `${priorityClass} border-small border-white/50`,
                  content: "body-sm",
                }}
              >
                {priority_level + " Priority"}
              </Chip>
            ),
          },
        ]}
      />

      <PropertyDetailTable
        tableLabel="Land Information"
        rows={[
          {
            label: "Owner",
            content: (
              <div className="flex flex-col">
                <span>{owner_1}</span>
                {owner_2 && <span>{owner_2}</span>}
              </div>
            ),
          },
          {
            label: "Zip Code",
            content: zipcode,
          },
          {
            label: "Neighborhood",
            content: neighborhood,
          },
          {
            label: "Registered Community Orgs",
            content: rco_names.split("|").join(", "),
          },
          {
            label: "Zoning",
            content: zoning_base_district,
          },
          {
            label: "Council District",
            content: council_district,
          },
          {
            label: "Market Value",
            content: new Intl.NumberFormat("en-US", {
              style: "currency",
              currency: "USD",
              minimumFractionDigits: 0,
              maximumFractionDigits: 0,
            }).format(market_value),
          },
          {
            label: "Tax Delinquency",
            content: total_due ? "Yes" : "No",
          },
        ]}
      />

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

      <div className="flex flex-col space-y-6 mt-[72px]">
        <p>You can request that we remove this property from the dashboard.</p>
        <div className="flex">
          <ThemeButtonLink
            color="secondary"
            href="/request-removal"
            startContent={<PiEyeSlash />}
            label={"Request we hide this property"}
          />
        </div>
      </div>
    </div>
  );
};

const PropertyDetailTable = ({
  tableLabel,
  rows,
}: {
  tableLabel: string;
  rows: {
    label: string;
    tooltip?: React.ReactNode;
    content: string | React.ReactNode;
  }[];
}) => {
  return (
    <table
      aria-label={tableLabel}
      className="w-full mb-3 border-y border-gray-200"
    >
      <tbody className="body-md divide-y divide-gray-200">
        {rows.length > 0 &&
          rows.map((row, index) => (
            <tr key={index}>
              <th
                scope="row"
                className="text-left py-2 px-0 w-1/3 sm:w-1/2 lg:w-1/3 pr-4"
              >
                {row.label}
              </th>
              <td className="py-2 px-0">
                <div className="flex items-center">{row.content}</div>
              </td>
            </tr>
          ))}
      </tbody>
    </table>
  );
};

export default SinglePropertyDetail;
