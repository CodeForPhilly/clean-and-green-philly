import React, { useEffect, useState } from "react";
import { Chip, Tooltip } from "@nextui-org/react";
import { useFilter } from "@/context/FilterContext";
import { InformationCircleIcon } from "@heroicons/react/24/outline";

type DimensionFilterProps = {
  property: string;
  display: string;
  options: string[];
  tooltip: string;
};

const DimensionFilter: React.FC<DimensionFilterProps> = ({
  property,
  display,
  options,
  tooltip
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
      <div className="flex items-center mb-2">
        <div className="text-md flex items-center">
          {display}
          <Tooltip content={tooltip} placement="top" showArrow color="primary">
            <InformationCircleIcon className="h-5 w-5 text-gray-500 ml-2 cursor-pointer" />
          </Tooltip>
        </div>
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
