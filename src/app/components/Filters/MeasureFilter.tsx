import React, { useEffect, useState } from "react";
import {
  useFilter,
  MeasureFilter as MeasureFilterType,
} from "@/context/FilterContext";
import MultiRangeSlider from "multi-range-slider-react";

type MeasureFilterProps = {
  property: string;
  display: string;
};

//const green60 = getComputedStyle(document.documentElement).getPropertyValue('--tw-bg-green-60').trim();

const MeasureFilter: React.FC<MeasureFilterProps> = ({ property, display }) => {
  const { filter, dispatch } = useFilter();
  const filterValue = filter[property] as MeasureFilterType;

  const [dbMinValue, setDbMinValue] = useState(0);
  const [dbMaxValue, setDbMaxValue] = useState(100);
  const [userMinValue, setUserMinValue] = useState(0);
  const [userMaxValue, setUserMaxValue] = useState(100);

  useEffect(() => {
    const fetchMeasureBounds = async () => {
      const response = await fetch(
        `${window.location.origin}/api/getMeasureBounds?p=${property}`
      );
      const data = await response.json();
      setDbMinValue(data.min);
      setDbMaxValue(data.max);
      setUserMinValue(data.min);
      setUserMaxValue(data.max);
    };

    fetchMeasureBounds();
  }, [property]);

  const handleInput = (e: any) => {
    let change = false;
    const { minValue, maxValue } = e;
    if (minValue !== userMinValue) {
      setUserMinValue(minValue);
      change = true;
    }
    if (maxValue !== userMaxValue) {
      setUserMaxValue(maxValue);
      change = true;
    }
    if (change) {
      dispatch({
        type: "SET_MEASURES",
        property,
        min: minValue,
        max: maxValue,
      });
    }
  };

  return (
    <div className="pb-6">
      <div className="flex items-center justify-between mb-2">
        <div className="text-md">{display}</div>
      </div>
      <div className="space-x-2">
        <MultiRangeSlider
          min={dbMinValue}
          max={dbMaxValue}
          step={(dbMaxValue - dbMinValue) / 25}
          minValue={userMinValue}
          maxValue={userMaxValue}
          onChange={(e) => {
            handleInput(e);
          }}
          style={{
            border: "none",
            boxShadow: "none",
            padding: "15px 10px",
          }}
          ruler="false"
          //barInnerColor = {green60}
        />
      </div>
    </div>
  );
};

export default MeasureFilter;
