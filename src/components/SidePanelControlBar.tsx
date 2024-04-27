"use client";

import React, { FC, useRef } from "react";
import { Button } from "@nextui-org/react";
import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import {
  DownloadSimple,
  Funnel,
  GlobeHemisphereWest,
  SquaresFour,
} from "@phosphor-icons/react";
import { ThemeButton } from "./ThemeButton";
import { useFilter } from "@/context/FilterContext";

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
  const filterRef = useRef<HTMLButtonElement | null>(null);
  const { appFilter } = useFilter();
  const filterCount = Object.keys(appFilter).length;

  return loading ? (
    <div>{/* Keep empty while loading */}</div>
  ) : (
    <>
      <div className="flex justify-between -mx-6 px-12 top-0 py-4 z-10 bg-white">
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
            label={
              <div className="lg:space-x-1 body-md">
                <span className="max-lg:hidden">Filter</span>
                {filterCount !== 0 && <span>({filterCount})</span>}
              </div>
            }
            onPress={() => {
              if (filterRef.current && currentView === "filter") {
                filterRef.current.blur();
              }

              updateCurrentView("filter");
            }}
            isSelected={currentView === "filter" || filterCount !== 0}
            startContent={<Funnel />}
            className="max-lg:min-w-[4rem]"
            data-hover={false}
            ref={filterRef}
          />

          <ThemeButton
            color="tertiary"
            aria-label="Download"
            onPress={() => updateCurrentView("download")}
            startContent={<DownloadSimple />}
            label={<span className="body-md max-lg:hidden">Download</span>}
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
