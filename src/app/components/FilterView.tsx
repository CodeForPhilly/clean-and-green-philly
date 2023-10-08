import React, { FC } from "react";
import DimensionFilter from "./Filters/DimensionFilter";
import MeasureFilter from "./Filters/MeasureFilter";

const filters = [
  {
    property: "guncrime_density",
    display: "Gun Crime Density",
    type: "dimension",
  },
  {
    property: "ZONINGBASEDISTRICT",
    display: "Zoning",
    type: "dimension",
  },
  {
    property: "COUNCILDISTRICT_left",
    display: "Council District",
    type: "dimension",
  },
  {
    property: "tree_canopy_gap",
    display: "Tree Canopy Gap",
    type: "measure",
  },
];

const FilterView: FC = () => {
  return (
    <div className="p-6">
      <div className="font-semibold text-xl mb-2">Filters</div>

      {filters.map(({ property, display, type }) => {
        if (type === "dimension") {
          return (
            <DimensionFilter
              key={property}
              property={property}
              display={display}
            />
          );
        } else if (type === "measure") {
          return (
            <MeasureFilter
              key={property}
              property={property}
              display={display}
            />
          );
        }
        return null;
      })}
    </div>
  );
};

export default FilterView;
