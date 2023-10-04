import React, { FC, useState } from "react";
import DimensionFilter from "./filters/DimensionFilter";

const filters = [
  {
    property: "guncrime_density",
    display: "Gun Crime Density",
  },
  {
    property: "ZONINGBASEDISTRICT",
    display: "Zoning",
  },
  {
    property: "COUNCILDISTRICT_left",
    display: "Council District",
  },
];

const FilterView: FC = () => {
  return (
    <div className="p-6">
      <div className="font-semibold text-xl mb-2">Filters</div>

      {filters.map(({ property, display }) => (
        <DimensionFilter key={property} property={property} display={display} />
      ))}
    </div>
  );
};

export default FilterView;
