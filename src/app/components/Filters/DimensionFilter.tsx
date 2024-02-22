import React, { useState, FC } from "react";
import { Chip, Tooltip } from "@nextui-org/react";
import { useFilter } from "@/context/FilterContext";
import { Info } from "@phosphor-icons/react";

type DimensionFilterProps = {
  property: string;
  display: string;
  options: string[];
  tooltip: string;
};

const DimensionFilter: FC<DimensionFilterProps> = ({
  property,
  display,
  options,
  tooltip,
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

  return (
    <div className="pb-6">
      <div className="flex items-center mb-2">
        <div className="text-md flex items-center">
          {display}
          <Tooltip content={tooltip} placement="top" showArrow color="primary">
            <Info alt="More Info" className="h-5 w-9 text-gray-500 pl-2 pr-2 cursor-pointer" tabIndex={0} />
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
