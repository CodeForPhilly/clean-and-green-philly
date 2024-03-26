import { FC } from "react";
import DimensionFilter from "./Filters/DimensionFilter";
import { Button } from "@nextui-org/react";
import { PiX, PiCheck } from "react-icons/pi";
import { BarClickOptions } from "@/app/map/page";

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
        <Button
          className="bg-gray-100 right-2 text-gray-900 absolute px-2 top-8 min-w-[3rem]"
          onPress={() => updateCurrentView("detail")}
        >
          <PiX className="h-6 w-6" />
        </Button>
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
