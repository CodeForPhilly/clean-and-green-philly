import React, { useEffect, useState, useMemo } from "react";
import {
  Chip,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Button,
} from "@nextui-org/react";
import { apiBaseUrl } from "../../../config/config";
import { useFilter } from "@/context/FilterContext";

type DimensionFilterProps = {
  property: string;
  display: string;
};

const DimensionFilter: React.FC<DimensionFilterProps> = ({
  property,
  display,
}) => {
  const [dimensions, setDimensions] = useState<any[]>([]);
  const { filter, dispatch } = useFilter();
  const [selectedKeys, setSelectedKeys] = useState<string[]>(
    filter[property] || []
  );

  const selectedValue = useMemo(
    () => Array.from(selectedKeys).join(", "),
    [selectedKeys]
  );

  useEffect(() => {
    const fetchDimensions = async () => {
      const response = await fetch(
        `${apiBaseUrl}/api/getUniqueDimensionValues?p=${property}`
      );
      const data = await response.json();
      setDimensions(data);
      dispatch({ type: "SET_DIMENSIONS", property, dimensions: data });
      setSelectedKeys(data);
    };

    fetchDimensions();
  }, []);

  const toggleDimension = (dimension: string) => {
    dispatch({ type: "TOGGLE_DIMENSION", property, dimension });
  };

  const handleSelectionChange = (newSelectedKeys: any) => {
    const selectedKeysArray = Array.from(newSelectedKeys as Set<string>);
    setSelectedKeys(selectedKeysArray);
    dispatch({
      type: "SET_DIMENSIONS",
      property,
      dimensions: selectedKeysArray,
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
        {dimensions.length > 10 && (
          <Button
            variant="bordered"
            size="sm"
            className="text-xs"
            onClick={toggleAllDimensions}
          >
            Select All
          </Button>
        )}
      </div>
      <div className="space-x-2">
        {dimensions.length > 10 ? (
          <>
            <Dropdown>
              <DropdownTrigger>
                <Button variant="bordered" className="capitalize">
                  {selectedValue.length > 5 ? "Multiple" : selectedValue}
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                aria-label="Multiple selection example"
                variant="flat"
                closeOnSelect={false}
                disallowEmptySelection
                selectionMode="multiple"
                selectedKeys={selectedKeys}
                onSelectionChange={handleSelectionChange}
                className="max-h-[200px] overflow-y-auto"
              >
                {dimensions.map((dimension) => (
                  <DropdownItem key={dimension}>{dimension}</DropdownItem>
                ))}
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
                filter[property]?.includes(dimension) ? "success" : "default"
              }
              className="cursor-pointer"
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
