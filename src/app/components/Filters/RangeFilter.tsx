import React, { useEffect, useState } from "react";
import { Slider, Tooltip } from "@nextui-org/react";
import { useFilter } from "@/context/FilterContext";
import { Info } from "@phosphor-icons/react";

type RangeFilterProps = {
  property: string;
  display: string;
  min: number;
  max: number;
  step: number;
  tooltip: string;
};

const RangeFilter: React.FC<RangeFilterProps> = ({
  property,
  display,
  min,
  max,
  step,
  tooltip
}) => {
  const { filter, dispatch } = useFilter();
  const [rangeValue, setRangeValue] = useState<[number, number]>([min, max]);

  useEffect(() => {
    dispatch({ type: "SET_RANGE", property, min: rangeValue[0], max: rangeValue[1] });
  }, [rangeValue, dispatch, property]);

  return (
    <div className="pb-6">
      <div className="flex items-center mb-2">
        <div className="text-md flex items-center">
          {display}
          <Tooltip content={tooltip} placement="top" showArrow color="primary">
            <Info className="h-5 w-5 text-gray-500 ml-2 cursor-pointer" />
          </Tooltip>
        </div>
      </div>
      <div className="flex items-center">
        <Slider
          value={rangeValue}
          minValue={min}
          maxValue={max}
          step={step}
          onChange={(value) => setRangeValue(value as [number, number])}
        />
      </div>
    </div>
  );
};

export default RangeFilter;
