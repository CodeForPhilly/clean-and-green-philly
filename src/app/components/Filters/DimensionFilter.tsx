import React, { useEffect, useState } from "react";
import { Button } from "@nextui-org/react";
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

  useEffect(() => {
    const fetchDimensions = async () => {
      const response = await fetch(
        `${apiBaseUrl}/api/getUniqueDimensionValues?p=${property}`
      );
      const data = await response.json();
      setDimensions(data);
      dispatch({ type: "SET_DIMENSIONS", property, dimensions: data });
    };

    fetchDimensions();
  }, []);

  const toggleDimension = (dimension: string) => {
    dispatch({ type: "TOGGLE_DIMENSION", property, dimension });
  };

  return (
    <div>
      <div className="font-semibold text-lg">{display}</div>
      {dimensions.map((dimension, index) => (
        <Button
          key={index}
          radius="full"
          className={
            filter[property]?.includes(dimension)
              ? "bg-blue-500 text-white"
              : "bg-gray-200 text-gray-700"
          }
          onClick={() => toggleDimension(dimension)}
        >
          {dimension}
        </Button>
      ))}
    </div>
  );
};

export default DimensionFilter;
