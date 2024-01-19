import React, { useEffect, useState } from "react";
import { Chip } from "@nextui-org/react";
import { useFilter } from "@/context/FilterContext";

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

  const toggleDimension = (dimension: string) => {
    const newSelectedKeys = selectedKeys.includes(dimension)
      ? selectedKeys.filter(key => key !== dimension)
      : [...selectedKeys, dimension];
    setSelectedKeys(newSelectedKeys);
    dispatch({ type: "SET_DIMENSIONS", property, dimensions: newSelectedKeys });
  };

  return (
    <div className="pb-6">
      <div className="flex items-center justify-between mb-2">
        <div className="text-md">{display}</div>
      </div>
      <div className="space-x-2">
        {options.map((option, index) => (
          <Chip
            key={index}
            onClick={() => toggleDimension(option)}
            size="sm"
            color={selectedKeys.includes(option) ? "success" : "default"}
            className="cursor-pointer mb-2 p-2"
          >
            {option}
          </Chip>
        ))}
      </div>
    </div>
  );
};

export default DimensionFilter;
