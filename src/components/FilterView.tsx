import { FC } from "react";
import DimensionFilter from "./Filters/DimensionFilter";
import { PiX } from "react-icons/pi";
import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import { ThemeButton } from "./ThemeButton";
import { rcos, neighborhoods, zoning } from "./Filters/filterOptions";
import { access_options, PropertyAccess } from "@/config/propertyAccessOptions";


const filters = [
  {
    property: "priority_level",
    display: "Suggested Priority",
    options: ["Low", "Medium", "High"],
    type: "buttonGroup",
  },
  {
    // COMBINED FILTER
    property: "access_process",
    display: "Access Process",
    options: ["Buy Property", "Land Bank", "Private Land Use Agreement"],
    type: "buttonGroup",
  },
  {
    property: "neighborhood",
    display: "Neighborhoods",
    options: neighborhoods,
    type: "multiSelect",
  },
  {
    property: "rco_names",
    display: "Community Organizations",
    options: rcos,
    type: "multiSelect",
    useIndexOfFilter: true,
  },
  {
    property: "zoning_base_district",
    display: "Zoning",
    options: zoning,
    type: "multiSelect",
  },
  {
    property: "parcel_type",
    display: "Parcel Type",
    options: ["Land", "Building"],
    type: "buttonGroup",
  },
  {
    // COMBINED FILTER
    property: "tactical_urbanism",
    display: "Tactical Urbanism",
    options: ["Yes", "No"],
    type: "buttonGroup",
  },
  {
    // COMBINED FILTER
    property: "conservatorship",
    display: "Conservatorship Eligible",
    options: ["Yes", "No"],
    type: "buttonGroup",
  },
  {
    // COMBINED FILTER
    property: "side_yard_eligible",
    display: "Side Yard Eligible",
    options: ["Yes", "No"],
    type: "buttonGroup",
  },
  {
    property: "llc_owner",
    display: "LLC Owner",
    options: ["Yes", "No"],
    type: "buttonGroup",
  },
  {
    // COMBINED FILTER --> "Get Permission from the Owner" (Private Land Use Agreement), "Buy Affordably from the Owner" (Buy Property), "Buy Through the Land Bank" (Land Bank)
    property: "get_access",
    display: "Get Access",
    options: ["TACTICAL_URBANISM", "PRIVATE_LAND_USE", "BUY_FROM_OWNER", "SIDE_YARD", "LAND_BANK", "CONSERVATORSHIP"],
    type: "panels",
  },
];

interface FilterViewProps {
  updateCurrentView: (view: BarClickOptions) => void;
}

const FilterView: FC<FilterViewProps> = ({ updateCurrentView }) => {
  return (
    <div className="relative p-6">
      <ThemeButton
        color="secondary"
        className="right-4 lg:right-[24px] absolute top-8 min-w-[3rem]"
        aria-label="Close filter panel"
        startContent={<PiX />}
        onPress={() => updateCurrentView("filter")}
      />
      {filters.map((attr) => (
        <DimensionFilter key={attr.property} {...attr} />
      ))}
    </div>
  );
};

export default FilterView;
