import React, { FC, useState } from "react";
import { Button, Tooltip } from "@nextui-org/react";
import { BarClickOptions } from "@/app/map/page";
import {
  DownloadSimple,
  ListBullets,
  Funnel,
  Table,
}
from "@phosphor-icons/react"


type SidePanelControlBarProps = {
  currentView: BarClickOptions;
  setCurrentView: (view: BarClickOptions) => void;
  featuresInView: any[]; // Add this line
};

const SearchBarComponent: React.FC<SidePanelControlBarProps> = ({
  currentView,
  setCurrentView,
  featuresInView,
}) => {
  const handleClick = (view: BarClickOptions) => {
    if (view === currentView) {
      setCurrentView("detail");
    } else {
      setCurrentView(view);
    }
  };

  const toggleDetailView = () => {
    setCurrentView(currentView === "detail" ? "list" : "detail");
  };

  return (
    <div className="flex justify-between items-center bg-white p-2 h-12">
      {/* Left-aligned content: Total Properties in View */}
      <div className="px-4 py-2">
        <p className="text-md">
          <span className="font-bold">{featuresInView.length.toLocaleString()}</span> Properties in View 
        </p>
      </div>
  
      {/* Right-aligned content: Buttons */}
      <div className="flex items-center space-x-2">

         <Button
          onClick={() => handleClick("filter")}
          startContent={<Funnel className="h-6 w-6" />}
          className="bg-white"
        >
          Filter
        </Button>

        <Tooltip content="View" showArrow color="primary">
        <Button
          onClick={() => handleClick("detail")}
          startContent={<Table className="h-6 w-6" />}
          className="bg-white"
        >
        </Button>
        </Tooltip>

        <Tooltip content="Download" showArrow color="primary">
          <Button
            onClick={() => handleClick("download")}
            startContent={<DownloadSimple className="h-6 w-6" />}
            className="bg-white"
          >
          </Button>
        </Tooltip>

      </div>
    </div>
  );
  
};

export default SearchBarComponent;
