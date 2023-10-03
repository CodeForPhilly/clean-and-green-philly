import React, { useEffect, useState } from "react";
import { Chip } from "@nextui-org/react";
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
    <>
      <div className="font-semibold text-lg mb-2">{display}</div>
      <div className="space-x-2">
        {dimensions.map((dimension, index) => (
          <Chip
            key={index}
            variant={
              filter[property]?.includes(dimension) ? "solid" : "bordered"
            }
            onClick={() => toggleDimension(dimension)}
            size="sm"
            color="primary"
            className="cursor-pointer"
          >
            {dimension}
          </Chip>
        ))}
      </div>
    </>
  );
};

export default DimensionFilter;
