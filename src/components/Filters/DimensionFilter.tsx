"use client";

import React, { useState, FC } from "react";
import { useFilter } from "@/context/FilterContext";
import { PropertyAccess } from "@/config/propertyAccessOptions";
import ButtonGroup from "./ButtonGroup";
import MultiSelect from "./MultiSelect";
import Panels from "./Panels";

type DimensionFilterProps = {
  property: string;
  display: string;
  options: string[];
  type: string;
  useIndexOfFilter?: boolean;
};

const DimensionFilter: FC<DimensionFilterProps> = ({
  property,
  display,
  options,
  type,
  useIndexOfFilter,
}) => {
  const { dispatch, appFilter } = useFilter();
  const [selectedKeys, setSelectedKeys] = useState<string[]>(
    appFilter[property]?.values || []
  );
  const [selectedPanelKeys, setSelectedPanelkeys] = useState<{[property: string]: string[]}>({})

  const toggleDimensionForPanel = (dimension: string, panel_property: string) => {
    let newSelectedPanelKeys
    if (selectedPanelKeys[panel_property]) {
      newSelectedPanelKeys = selectedPanelKeys[panel_property].includes(dimension)
        ? selectedPanelKeys[panel_property].filter((key) => key !== dimension)
        : [...selectedPanelKeys[panel_property], dimension];
    } else {
      newSelectedPanelKeys = [dimension]
    }
    setSelectedPanelkeys({...selectedPanelKeys, [panel_property]: newSelectedPanelKeys});
    dispatch({
      type: "SET_DIMENSIONS",
      property: panel_property,
      dimensions: newSelectedPanelKeys,
    });
  }

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
      useIndexOfFilter,
    });
  };

  const Filter = () => {
    if (type === "buttonGroup") {
      return (
        <ButtonGroup
          options={options}
          selectedKeys={selectedKeys}
          toggleDimension={toggleDimension}
        />
      );
    } else if (type === "panels") {
      return (
        <Panels 
          options={options}
          selectedPanelKeys={selectedPanelKeys}
          toggleDimensionForPanel={toggleDimensionForPanel}
        />
      )
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

  const filterDescription =
    property === "priority_level"
      ? {
          desc: "Find properties based on how much they can reduce gun violence considering the gun violence, cleanliness, and tree canopy nearby. ",
          linkFragment: "priority-method",
        }
      : {
          desc: "Find properties based on what we think is the easiest method to get legal access to them, based on the data available to us. ",
          linkFragment: "access-method",
        };
  // text-gray-500, 600 ? or #586266 (figma)?
  return (
    <div className="pt-3 pb-6">
      <div className="flex flex-col mb-2">
        <h2 className="heading-lg">{display}</h2>
        {(property === "access_process" || property === "priority_level") && (
          <p className="body-sm text-gray-500 w-[90%] my-1">
            {filterDescription.desc}
            <a
              href={`/methodology/#${filterDescription.linkFragment}`}
              className="link"
              aria-label={`Goes to methodology page for ${property}`}
            >
              Learn more{" "}
            </a>
          </p>
        )}
      </div>
      <Filter />
    </div>
  );
};

export default DimensionFilter;
