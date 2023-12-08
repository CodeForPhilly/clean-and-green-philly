import React, { useEffect, useState } from "react";
import {
  Chip,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Button,
  DropdownSection,
} from "@nextui-org/react";
import { useFilter } from "@/context/FilterContext";

type DimensionFilterProps = {
  property: string;
  display: string;
};

const DimensionFilter: React.FC<DimensionFilterProps> = ({
  property,
  display,
}) => {
  const [dimensions, setDimensions] = useState<string[]>([]);
  const { filter, dispatch } = useFilter();
  const filterValue = filter[property];
  const isDimensionFilter = filterValue?.type === "dimension";
  const [selectedKeys, setSelectedKeys] = useState<string[]>(
    isDimensionFilter ? filterValue.values : []
  );

  useEffect(() => {
    const fetchDimensions = async () => {
      const response = await fetch(
        `${window.location.origin}/api/getUniqueDimensionValues?p=${property}`
      );
      const data = await response.json();
      setDimensions(data);
      dispatch({ type: "SET_DIMENSIONS", property, dimensions: data });
      setSelectedKeys(data);
    };

    fetchDimensions();
  }, [property, dispatch]);

  const toggleDimension = (dimension: string) => {
    dispatch({ type: "TOGGLE_DIMENSION", property, dimension });
  };

  const handleSelectionChange = (newSelectedKeys: Set<string>) => {
    let filteredKeys = Array.from(newSelectedKeys);
    if (filteredKeys.length > 1) {
      filteredKeys = filteredKeys.filter(
        (currentKey: string) => currentKey !== "selectAll"
      );
    }
    setSelectedKeys(filteredKeys);
    dispatch({
      type: "SET_DIMENSIONS",
      property,
      dimensions: filteredKeys,
    });
  };

  const toggleAllDimensions = () => {
    if (selectedKeys.length === dimensions.length) {
      setSelectedKeys([]);
      dispatch({ type: "SET_DIMENSIONS", property, dimensions: [] });
    } else {
      setSelectedKeys(dimensions);
      dispatch({
        type: "SET_DIMENSIONS",
        property,
        dimensions: dimensions,
      });
    }
  };

  return (
    <div className="pb-6">
      <div className="flex items-center justify-between mb-2">
        <div className="text-md">{display}</div>
      </div>
      <div className="space-x-2">
        {dimensions.length > 10 ? (
          <>
            <Dropdown>
              <DropdownTrigger>
                <Button variant="bordered" className="capitalize">
                  {selectedKeys.length > 5
                    ? "Multiple"
                    : selectedKeys.join(", ")}
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                aria-label="Multiple selection example"
                variant="flat"
                closeOnSelect={false}
                disallowEmptySelection
                selectionMode="multiple"
                selectedKeys={selectedKeys}
                onSelectionChange={(keys) => {
                  handleSelectionChange(keys as Set<string>);
                }}
                className="max-h-[200px] overflow-y-auto"
              >
                <DropdownSection>
                  <DropdownItem onClick={toggleAllDimensions} key="selectAll">
                    Select All
                  </DropdownItem>
                </DropdownSection>
                <DropdownSection>
                  {dimensions.map((dimension) => (
                    <DropdownItem key={dimension}>{dimension}</DropdownItem>
                  ))}
                </DropdownSection>
              </DropdownMenu>
            </Dropdown>
          </>
        ) : (
          dimensions.map((dimension, index) => (
            <Chip
              key={index}
              onClick={() => toggleDimension(dimension)}
              size="sm"
              color={
                isDimensionFilter && filterValue.values.includes(dimension)
                  ? "success"
                  : "default"
              }
              className="cursor-pointer mb-2 p-2"
            >
              {dimension}
            </Chip>
          ))
        )}
      </div>
    </div>
  );
};

export default DimensionFilter;
