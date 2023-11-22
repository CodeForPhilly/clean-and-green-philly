import React from "react";

const PropertyDetail = () => {
  return (
    <div className="max-w-sm w-full md:w-1/2 p-4">
      <div className="bg-white rounded-lg overflow-hidden">
        <div className="relative h-48 w-full rounded-lg overflow-hidden">
          <img
            src="https://images.unsplash.com/photo-1612839905599-2b3f8f3e3d2a?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cHJvcGVydGllcyUyMHRvJTIwYmFjayUyMHN0YXRpb25zJTIwYW5kJTIwY2FuYXBpJTIwZ2FtZXN8ZW58MHx8MHx8&ixlib=rb-1.2.1&w=1000&q=80"
            alt="Property at 123 Main St"
            className="absolute h-full w-full object-cover"
          />
        </div>
        <div className="p-4">
          <div className="font-bold text-xl">123 Main St</div>
          <div className="text-gray-700 mb">0.5 Crime Rate, 0% Canopy Gap</div>
        </div>
        <div className="px-4 pb-2">
          <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
            High Priority
          </span>
        </div>
      </div>
    </div>
  );
};

export default PropertyDetail;
