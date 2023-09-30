import React, { FC, useState } from "react";
import DimensionFilter from "./Filters/DimensionFilter";

interface SidePanelProps {
  children?: React.ReactNode;
}

const FilterView: FC = () => {
  return (
    <>
      <DimensionFilter
        property="guncrime_density"
        display="Gun Crime Density"
      />
    </>
  );
};

export default FilterView;
