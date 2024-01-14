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
import { isEmpty } from "lodash";

type DimensionFilterProps = {
  property: string;
  display: string;
  options: string[];
};

const DimensionFilter: React.FC<DimensionFilterProps> = ({
  property,
  display,
  options,
}) => {
  const { filter, dispatch } = useFilter();
  const [selectedKeys, setSelectedKeys] = useState<string[]>([]);

  const filterValue = filter[property];

  useEffect(() => {
    if (!isEmpty(filterValue)) return;
    dispatch({ type: "SET_DIMENSIONS", property, dimensions: options });
    setSelectedKeys(options);
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
    if (selectedKeys.length === options.length) {
      setSelectedKeys([]);
      dispatch({ type: "SET_DIMENSIONS", property, dimensions: [] });
    } else {
      setSelectedKeys(options);
      dispatch({
        type: "SET_DIMENSIONS",
        property,
        dimensions: options,
      });
    }
  };

  return (
    <div className="pb-6">
      <div className="flex items-center justify-between mb-2">
        <div className="text-md">{display}</div>
      </div>
      <div className="space-x-2">
        {options.length > 10 ? (
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
                  {options.map((option) => (
                    <DropdownItem key={option}>{option}</DropdownItem>
                  ))}
                </DropdownSection>
              </DropdownMenu>
            </Dropdown>
          </>
        ) : (
          options.map((options, index) => (
            <Chip
              key={index}
              onClick={() => toggleDimension(options)}
              size="sm"
              color={
                filterValue?.values.includes(options) ? "success" : "default"
              }
              className="cursor-pointer mb-2 p-2"
            >
              {options}
            </Chip>
          ))
        )}
      </div>
    </div>
  );
};

export default DimensionFilter;
