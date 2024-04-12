import { FC } from "react";
import DimensionFilter from "./Filters/DimensionFilter";
import { PiX } from "react-icons/pi";
import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import { ThemeButton } from "./ThemeButton";
import { rcos, neighborhoods } from "./Filters/Options";


const filters = [
  {
    property: "priority_level",
    display: "Priority Level",
    options: ["Low", "Medium", "High"],
    tooltip: "For information on how this is calculated, see the About page",
  },
  {
    property: "parcel_type",
    display: "Parcel Type",
    options: ["Land", "Building"],
    tooltip: "Parcel type from City of Philadelphia data",
  },
  {
    property: "access_process",
    display: "Access Process",
    options: ["Buy Property", "Land Bank", "Private Land Use Agreement"],
    tooltip: "For information on what these mean, see the Get Access page",
  },
  {
    property: "neighborhood",
    display: "Neighborhoods",
    options: neighborhoods,
    tooltip: "",
  },
  {
    property: "rco_info",
    display: "Community Organizations",
    options: rcos,
    tooltip: "",
  },
  {
    property: "tactical_urbanism",
    display: "Tactical Urbanism",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
  },
  {
    property: "conservatorship",
    display: "Conservatorship Eligible",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
  },
  {
    property: "side_yard_eligible",
    display: "Side Yard Eligible",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
  },
  {
    property: "llc_owner",
    display: "LLC Owner",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
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
      {filters.map(({ property, display, options, tooltip }) => (
        <DimensionFilter
          key={property}
          property={property}
          options={options}
          display={display}
          tooltip={tooltip}
        />
      ))}
    </div>
  );
};

export default FilterView;
