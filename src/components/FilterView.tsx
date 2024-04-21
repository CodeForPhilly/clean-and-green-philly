import { FC } from "react";
import DimensionFilter from "./Filters/DimensionFilter";
import { PiX } from "react-icons/pi";
import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import { ThemeButton } from "./ThemeButton";
import { rcos, neighborhoods } from "./Filters/filterOptions";

const filters = [
  {
    property: "priority_level",
    display: "Priority Level",
    options: ["Low", "Medium", "High"],
    tooltip: "For information on how this is calculated, see the About page",
    type: "buttonGroup",
  },
  {
    property: "parcel_type",
    display: "Parcel Type",
    options: ["Land", "Building"],
    tooltip: "Parcel type from City of Philadelphia data",
    type: "buttonGroup",
  },
  {
    property: "access_process",
    display: "Access Process",
    options: ["Buy Property", "Land Bank", "Private Land Use Agreement"],
    tooltip: "For information on what these mean, see the Get Access page",
    type: "buttonGroup",
  },
  {
    property: "neighborhood",
    display: "Neighborhoods",
    options: neighborhoods,
    tooltip:
      "Neighborhood mapping from OpenDataPhilly by Element 84 (formerly Azavea)",
    type: "multiSelect",
  },
  {
    property: "rco_names",
    display: "Community Organizations",
    options: rcos,
    tooltip: "RCO mapping from City of Philadelphia data",
    type: "multiSelect",
    multipleMatches: true,
  },
  {
    property: "tactical_urbanism",
    display: "Tactical Urbanism",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
    type: "buttonGroup",
  },
  {
    property: "conservatorship",
    display: "Conservatorship Eligible",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
    type: "buttonGroup",
  },
  {
    property: "side_yard_eligible",
    display: "Side Yard Eligible",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
    type: "buttonGroup",
  },
  {
    property: "llc_owner",
    display: "LLC Owner",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
    type: "buttonGroup",
  },
];

type FilterViewProps = {
  updateCurrentView: (view: BarClickOptions) => void;
};

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
      {filters.map(({ property, display, options, tooltip, type }) => (
        <DimensionFilter
          key={property}
          property={property}
          options={options}
          display={display}
          tooltip={tooltip}
          type={type}
        />
      ))}
    </div>
  );
};

export default FilterView;
