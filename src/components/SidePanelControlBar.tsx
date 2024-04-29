"use client";

import React, { FC, useRef } from "react";
import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import {
  BookmarkSimple,
  DownloadSimple,
  Funnel,
  GlobeHemisphereWest,
  SquaresFour,
} from "@phosphor-icons/react";
import { ThemeButton } from "./ThemeButton";
import { useFilter } from "@/context/FilterContext";
import { getPropertyIdsFromLocalStorage } from "@/utilities/localStorage";

type SidePanelControlBarProps = {
  currentView: string;
  featureCount: number;
  loading: boolean;
  savedPropertyCount: number;
  shouldFilterSavedProperties: boolean;
  smallScreenMode: string;
  setShouldFilterSavedProperties: (shouldFilter: boolean) => void;
  updateCurrentView: (view: BarClickOptions) => void;
  updateSmallScreenMode: () => void;
};

const SearchBarComponent: FC<SidePanelControlBarProps> = ({
  currentView,
  featureCount,
  loading,
  savedPropertyCount,
  shouldFilterSavedProperties,
  smallScreenMode,
  setShouldFilterSavedProperties,
  updateCurrentView,
  updateSmallScreenMode,
}) => {
  const filterRef = useRef<HTMLButtonElement | null>(null);
  const savedRef = useRef<HTMLButtonElement | null>(null);
  const { dispatch, appFilter } = useFilter();

  const filterCount = Object.keys(appFilter).length;

  const onClickSavedButton = () => {
    let propertyIds = getPropertyIdsFromLocalStorage();

    if (shouldFilterSavedProperties) {
      setShouldFilterSavedProperties(false);
      dispatch({
        type: "SET_DIMENSIONS",
        property: "OPA_ID",
        dimensions: [],
      });
    } else {
      setShouldFilterSavedProperties(true);
      dispatch({
        type: "SET_DIMENSIONS",
        property: "OPA_ID",
        dimensions: [...propertyIds],
      });
    }
  };

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
          {savedPropertyCount > 0 ? (
            <ThemeButton
              color="tertiary"
              label={
                <div className="lg:space-x-1 body-md">
                  <span className="max-lg:hidden">Saved</span>
                </div>
              }
              onPress={onClickSavedButton}
              isSelected={shouldFilterSavedProperties}
              startContent={<BookmarkSimple />}
              className={`max-lg:min-w-[4rem] ${
                smallScreenMode === "map" ? "max-sm:hidden" : ""
              }`}
              ref={savedRef}
            />
          ) : (
            <></>
          )}
          <ThemeButton
            color="tertiary"
            aria-label="Filter"
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
