import React, { FC, useState } from "react";

interface PropertyDetailSectionProps {
  featuresInView: any[];
}

const PropertyDetailSection: FC<PropertyDetailSectionProps> = ({
  featuresInView,
}) => {
  const [expanded, setExpanded] = useState(true);
  const [limit, setLimit] = useState(20);

  const loadMore = () => setLimit(limit + 20);

  console.log(Math.min(limit, featuresInView.length));
  console.log(featuresInView);
  return (
    <div
      className={`h-full transition-all duration-300 ${
        expanded ? "w-1/3" : "w-0"
      } bg-white overflow-hidden`}
    >
      <div className="flex flex-wrap overflow-y-auto h-[85vh]">
        {featuresInView
          .slice(0, Math.min(limit, featuresInView.length))
          .map((feature, index) => (
            <div key={index} className="w-1/2 p-2">
              <div className="bg-gray-100 rounded-lg p-4">
                <h3 className="text-lg font-medium">
                  {feature.properties.ADDRESS}
                </h3>
                <p className="text-gray-500">{feature.properties.BLDG_DESC}</p>
              </div>
            </div>
          ))}
      </div>
      {featuresInView.length > limit && (
        <button
          onClick={loadMore}
          className="p-2 m-4 bg-blue-500 text-white rounded"
        >
          Load More
        </button>
      )}
    </div>
  );
};

export default PropertyDetailSection;
