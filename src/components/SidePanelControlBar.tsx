"use client";

import React, { FC, useRef } from "react";
import { Button } from "@nextui-org/react";
import { BarClickOptions } from "@/app/find-properties/page";
import {
  DownloadSimple,
  Funnel,
  GlobeHemisphereWest,
  SquaresFour,
  Table,
} from "@phosphor-icons/react";
<<<<<<< HEAD
import { ThemeButton } from "./ThemeButton";
=======
import { useFilter } from "@/context/FilterContext";
>>>>>>> f1c5e16 (feat(457): add filter count to button)

type SidePanelControlBarProps = {
  currentView: string;
  featureCount: number;
  loading: boolean;
  smallScreenMode: string;
  updateCurrentView: (view: BarClickOptions) => void;
  updateSmallScreenMode: () => void;
};

const SearchBarComponent: FC<SidePanelControlBarProps> = ({
  currentView,
  featureCount,
  loading,
  smallScreenMode,
  updateCurrentView,
  updateSmallScreenMode,
}) => {
<<<<<<< HEAD
  const filterRef = useRef<HTMLButtonElement | null>(null);
=======
  const { appFilter } = useFilter();
  const filterCount = Object.keys(appFilter).length;
>>>>>>> f1c5e16 (feat(457): add filter count to button)

  return loading ? (
    <div>{/* Keep empty while loading */}</div>
  ) : (
    <>
      <div className="flex justify-between items-center bg-white border-b-[1px] border-[#12121215] p-2 h-14">
        {/* Left-aligned content: Total Properties in View */}
        <ThemeButton
          color="tertiary"
          aria-label={`Change to ${smallScreenMode}`}
          className="sm:hidden max-md:min-w-[4rem]"
          onPress={updateSmallScreenMode}
          startContent={
            smallScreenMode === "map" ? (
              <SquaresFour />
            ) : (
              <GlobeHemisphereWest />
            )
          }
        />
        <div className="sm:px-4 py-2">
          <h1 className="body-md">
            <span className="font-bold">{featureCount.toLocaleString()} </span>
            Properties <span className="max-xl:hidden"> in View </span>
          </h1>
        </div>

        {/* Right-aligned content: Buttons */}
        <div
          className="flex items-center space-x-2"
          role="region"
          aria-label="controls"
        >
          <ThemeButton
            color="tertiary"
            label={<span className="max-lg:hidden body-md">Filter</span>}
            onPress={() => {
              if (filterRef.current && currentView === "filter") {
                filterRef.current.blur();
              }
              
              updateCurrentView("filter");
            }}
            isSelected={currentView === "filter"}
            startContent={<Funnel />}
            className="max-lg:min-w-[4rem]"
            data-hover={false}
            ref={filterRef}
          />

          <ThemeButton
            color="tertiary"
            aria-label="View"
            onPress={() => updateCurrentView("detail")}
            startContent={<Table />}
            className={`max-lg:min-w-[4rem] ${
              smallScreenMode === "map" ? "max-sm:hidden" : ""
            }`}
          />

          <ThemeButton
            color="tertiary"
            aria-label="Download"
            onPress={() => updateCurrentView("download")}
            startContent={<DownloadSimple />}
            className={`max-md:min-w-[4rem] ${
              smallScreenMode === "map" ? "max-sm:hidden" : ""
            }`}
          />
        </div>
      </div>
    </>
  );
};

export default SearchBarComponent;
