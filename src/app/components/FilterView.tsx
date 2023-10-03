import React, { FC, useState } from "react";
import DimensionFilter from "./Filters/DimensionFilter";

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
    <>
      {filters.map(({ property, display }) => (
        <DimensionFilter key={property} property={property} display={display} />
      ))}
    </>
  );
};

export default FilterView;
