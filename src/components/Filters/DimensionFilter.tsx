"use client";

import React, { useState, FC } from "react";
import { Tooltip } from "@nextui-org/react";
import { useFilter } from "@/context/FilterContext";
import { Info } from "@phosphor-icons/react";
import ButtonGroup from "./ButtonGroup";
import MultiSelect from "./MultiSelect";

type DimensionFilterProps = {
  property: string;
  display: string;
  options: string[];
  tooltip: string;
  type: string;
  multipleMatches?: boolean;
};

const DimensionFilter: FC<DimensionFilterProps> = ({
  property,
  display,
  options,
  tooltip,
  type,
  multipleMatches,
}) => {
  const { dispatch, appFilter } = useFilter();
  const [selectedKeys, setSelectedKeys] = useState<string[]>(
    appFilter[property]?.values || []
  );

  const toggleDimension = (dimension: string) => {
    const newSelectedKeys = selectedKeys.includes(dimension)
      ? selectedKeys.filter((key) => key !== dimension)
      : [...selectedKeys, dimension];
    setSelectedKeys(newSelectedKeys);
    dispatch({
      type: "SET_DIMENSIONS",
      property,
      dimensions: newSelectedKeys,
    });
  };

  const handleSelectionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newMultiSelect: string[] = e.target.value.split(",");
    setSelectedKeys(newMultiSelect);
    dispatch({
      type: "SET_DIMENSIONS",
      property,
      dimensions: newMultiSelect,
      multipleMatches,
    });
  };

  const filter = () => {
    if (type === "buttonGroup") {
      return (
        <ButtonGroup
          options={options}
          selectedKeys={selectedKeys}
          toggleDimension={toggleDimension}
        />
      );
    } else {
      return (
        <MultiSelect
          display={display}
          options={options}
          selectedKeys={selectedKeys}
          toggleDimension={toggleDimension}
          handleSelectionChange={handleSelectionChange}
        />
      );
    }
  };

  return (
    <div className="pb-6">
      <div className="flex items-center mb-2">
        <div className="flex items-center">
          <h2 className="heading-lg">{display}</h2>
          <Tooltip content={tooltip} placement="top" showArrow color="primary">
            <Info
              alt="More Info"
              className="h-5 w-9 text-gray-500 pl-2 pr-2 cursor-pointer"
              tabIndex={0}
            />
          </Tooltip>
        </div>
      </div>
      {filter()}
    </div>
  );
};

export default DimensionFilter;
