import React, { Dispatch, FC, SetStateAction } from "react";
import { Button, Tooltip } from "@nextui-org/react";
import { BarClickOptions } from "@/app/map/page";
import { DownloadSimple, Funnel, List, Table } from "@phosphor-icons/react";

type SidePanelControlBarProps = {
  currentView: BarClickOptions;
  setCurrentView: (view: BarClickOptions) => void;
  featureCount: number;
  loading: boolean;
  smallScreenMode: string;
  setSmallScreenMode: Dispatch<SetStateAction<(arg: string) => string>>;
};

const SearchBarComponent: FC<SidePanelControlBarProps> = ({
  currentView,
  setCurrentView,
  featureCount,
  loading,
  smallScreenMode,
  setSmallScreenMode
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
    <>
    <div className="flex justify-between items-center bg-white p-2 h-14">
      {/* Left-aligned content: Total Properties in View */}
      <Button
        aria-label={`Change to ${smallScreenMode}`}
        className="bg-white w-fit px-2 sm:hidden"
        onPress={() => setSmallScreenMode((prev : string) => (prev === 'map' ? 'properties' : 'map'))}
      >
        <List className="h-6 w-6" />
      </Button>
      <div className="sm:px-4 py-2">
        <h1 className="body-md">
          <span className="font-bold">{featureCount} </span> 
          Properties <span className="max-md:hidden"> in View </span>
        </h1>
      </div>

      {/* Right-aligned content: Buttons */}
      <div className="flex items-center sm:space-x-2" role="region" aria-label="controls">
        <Button
          onPress={() => handleClick("filter")}
          startContent={<Funnel className="h-6 w-6" />}
          className="bg-white max-sm:px-2"
        >
          <span className="max-sm:hidden body-md">Filter</span>
        </Button>

        <Tooltip content="View" showArrow color="primary">
          <Button
            aria-label="View"
            onPress={() => handleClick("detail")}
            startContent={<Table className="h-6 w-6" />}
            className="bg-white max-md:hidden"
          ></Button>
        </Tooltip>

        <Tooltip content="View" showArrow color="primary">
          <Button
            aria-label="Download"
            onPress={() => handleClick("download")}
            startContent={<DownloadSimple className="h-6 w-6" />}
            className="bg-white max-sm:px-2"
          ></Button>
        </Tooltip>
      </div>
    </div>
    </>
  );
};

export default SearchBarComponent;
