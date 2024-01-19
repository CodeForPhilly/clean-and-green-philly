import React, { FC } from "react";
import DimensionFilter from "./Filters/DimensionFilter";

const filters = [
  {
    property: "priority_level",
    display: "Priority Level",
    options: ["Low Priority", "Medium Priority", "High Priority"],
  },
  {
    property: "parcel_type",
    display: "Parcel Type",
    options: ["Land", "Building"],
  },
  {
    property: "access_process",
    display: "Access Process",
    options: [
      "Buy Property",
      "Land Bank",
      "Private Land Use Agreement",
      "Conservatorship",
    ],
  },
  {
    property: "tactical_urbanism",
    display: "Tactical Urbanism",
    options: ["Y", "N"],
  },
];

const FilterView: FC = () => {
  return (
    <div className="p-6">
      <div className="font-semibold text-xl mb-2">Filters</div>

      {filters.map(({ property, display, options }) => (
        <DimensionFilter
          key={property}
          property={property}
          options={options}
          display={display}
        />
      ))}
    </div>
  );
};

export default FilterView;
