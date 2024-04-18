import { FC } from "react";
import DimensionFilter from "./Filters/DimensionFilter";
import { PiX } from "react-icons/pi";
import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import { ThemeButton } from "./ThemeButton";
import { rcos, neighborhoods } from "./Filters/FilterOptions";

const filters = [
  {
    property: "priority_level",
    display: "Suggested Priority",
    options: ["Low", "Medium", "High"],
    type: "buttonGroup",
  },
  {
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
  },
  {
    property: "parcel_type",
    display: "Parcel Type",
    options: ["Land", "Building"],
    type: "buttonGroup",
  },
  {
    property: "tactical_urbanism",
    display: "Tactical Urbanism",
    options: ["Yes", "No"],
    type: "buttonGroup",
  },
  {
    property: "conservatorship",
    display: "Conservatorship Eligible",
    options: ["Yes", "No"],
    type: "buttonGroup",
  },
  {
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
