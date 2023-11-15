import React, { FC, useState } from "react";
import PropertyCard from "./PropertyCard";

interface PropertyDetailSectionProps {
  featuresInView: any[];
}

const PropertyDetailSection: FC<PropertyDetailSectionProps> = ({
  featuresInView,
}) => {
  const [limit, setLimit] = useState(20);

  const loadMore = () => setLimit(limit + 20);

  return (
    <>
      <div className="flex flex-wrap overflow-y-auto max-h-[calc(100vh-110px)]">
        {featuresInView
          .slice(0, Math.min(limit, featuresInView.length))
          .map((feature, index) => (
            <PropertyCard feature={feature} key={index} />
          ))}

        {featuresInView.length > limit && (
          <div>
            <button
              onClick={loadMore}
              className="p-2 m-4 bg-blue-500 text-white rounded"
            >
              Load More
            </button>
          </div>
        )}
      </div>
    </>
  );
};

export default PropertyDetailSection;
