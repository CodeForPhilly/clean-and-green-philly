"use client";

import React, { FC } from "react";
import { Tooltip } from "@nextui-org/react";
import { BarClickOptions } from "@/app/map/page";
import { DownloadSimple, Funnel, Table } from "@phosphor-icons/react";
import { ThemeButton } from "./ThemeButton";

type SidePanelControlBarProps = {
  currentView: BarClickOptions;
  setCurrentView: (view: BarClickOptions) => void;
  featureCount: number;
  loading: boolean;
};

const SearchBarComponent: FC<SidePanelControlBarProps> = ({
  currentView,
  setCurrentView,
  featureCount,
  loading,
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

  return loading ? (
    <div>{/* Keep empty while loading */}</div>
  ) : (
    <div className="flex justify-between items-center bg-white p-2 h-12">
      {/* Left-aligned content: Total Properties in View */}
      <div className="px-4 py-2">
        <h1 className="body-md">
          <span className="font-bold">{featureCount.toLocaleString()}</span>{" "}
          Properties in View
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
          label="Filter"
          onPress={() => handleClick("filter")}
          startContent={<Funnel />}
        />

        <Tooltip content="View" showArrow color="primary">
          <ThemeButton
            color="tertiary"
            aria-label="View"
            onPress={() => handleClick("detail")}
            startContent={<Table />}
          />
        </Tooltip>

        <Tooltip content="Download" showArrow color="primary">
          <ThemeButton
            color="tertiary"
            aria-label="Download"
            onPress={() => handleClick("download")}
            startContent={<DownloadSimple />}
          />
        </Tooltip>
      </div>
    </div>
  );
};

export default SearchBarComponent;
