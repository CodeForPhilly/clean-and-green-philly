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
  const { filter, setFilter } = useFilter();

  useEffect(() => {
    const fetchDimensions = async () => {
      const response = await fetch(
        `${apiBaseUrl}/api/getUniqueDimensionValues?p=${property}`
      );
      const data = await response.json();
      console.log(data);
      setDimensions(data);
      const newFilter = { ...filter, [property]: data };
      setFilter(newFilter);
    };

    fetchDimensions();
  }, []);

  const toggleDimension = (dimension: string) => {
    setFilter((prevFilter) => {
      const prevSelectedDimensions = prevFilter[property] || [];
      const updatedDimensions = prevSelectedDimensions.includes(dimension)
        ? prevSelectedDimensions.filter((d) => d !== dimension)
        : [...prevSelectedDimensions, dimension];
      return { ...prevFilter, [property]: updatedDimensions };
    });
  };

  return (
    <div>
      <div className="font-semibold text-lg">{display}</div>
      {dimensions.map((dimension, index) => (
        <Button
          key={index}
          radius="full"
          className={
            filter[property].includes(dimension)
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
