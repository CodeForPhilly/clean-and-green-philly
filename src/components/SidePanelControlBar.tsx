"use client";

import React, { Dispatch, FC, SetStateAction } from "react";
import { Button, Tooltip } from "@nextui-org/react";
import { BarClickOptions } from "@/app/map/page";
import { DownloadSimple, Funnel, GlobeHemisphereWest, SquaresFour, Table } from "@phosphor-icons/react";

type SidePanelControlBarProps = {
  featureCount: number;
  loading: boolean;
  smallScreenMode: string;
  setSmallScreenMode: Dispatch<SetStateAction<string>>;
  updateCurrentView: (view: BarClickOptions) => void;
  updateSmallScreenMode: () => void;
};

const SearchBarComponent: FC<SidePanelControlBarProps> = ({
  featureCount,
  loading,
  smallScreenMode,
  updateCurrentView,
  updateSmallScreenMode
}) => {

  return loading ? (
    <div>{/* Keep empty while loading */}</div>
  ) : (
    <>
    <div className="flex justify-between items-center bg-white p-2 h-14">
      {/* Left-aligned content: Total Properties in View */}
      <Button
        aria-label={`Change to ${smallScreenMode}`}
        className="bg-white w-fit px-2 sm:hidden hover:bg-gray-100"
        onPress={updateSmallScreenMode}
      >
        {smallScreenMode === 'map' ? <GlobeHemisphereWest className="h-6 w-6"/> : <SquaresFour className="h-6 w-6" />}
      </Button>
      <div className="sm:px-4 py-2">
        <h1 className="body-md">
          <span className="font-bold">{featureCount} </span> 
          Properties <span className="max-lg:hidden"> in View </span>
        </h1>
      </div>

      {/* Right-aligned content: Buttons */}
      <div
        className="flex items-center sm:space-x-2"
        role="region"
        aria-label="controls"
      >
        <Button
          onPress={() => updateCurrentView("filter")}
          startContent={<Funnel className="h-6 w-6" />}
          className="bg-white max-sm:px-2 hover:bg-gray-100"
        >
          <span className="max-sm:hidden body-md">Filter</span>
        </Button>
        <Button
          aria-label="View"
          onPress={() => updateCurrentView("detail")}
          startContent={<Table className="h-6 w-6" />}
          className="bg-white max-md:hidden hover:bg-gray-100"
        ></Button>
        <Button
          aria-label="Download"
          onPress={() => updateCurrentView("download")}
          startContent={<DownloadSimple className="h-6 w-6" />}
          className="bg-white max-sm:px-2 hover:bg-gray-100"
        ></Button>
      </div>
    </div>
    </>
  );
};

export default SearchBarComponent;
