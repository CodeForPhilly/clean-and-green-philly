import React from "react";
import { Button } from "@nextui-org/react";
import { ArrowDownTrayIcon, ListBulletIcon } from "@heroicons/react/20/solid";
import { FunnelIcon, TableCellsIcon, BookmarkSquareIcon } from "@heroicons/react/24/outline";
import { BarClickOptions } from "@/app/map/page";

type MapControlBarProps = {
  currentView: BarClickOptions;
  setCurrentView: (view: BarClickOptions) => void;
};

const SearchBarComponent: React.FC<MapControlBarProps> = ({
  currentView,
  setCurrentView,
}) => {
  const handleClick = (view: BarClickOptions) => {
    setCurrentView(view);
  };

  const toggleDetailView = () => {
    setCurrentView(currentView === "detail" ? "list" : "detail");
  };

  const getButtonClassName = (view: BarClickOptions) => {
    return currentView === view ? "bg-green-60" : "bg-white";
  };

  return (
    <div className="flex items-center space-x-2 bg-white p-2 h-12">
      <Button className="bg-white" onClick={toggleDetailView}>
        {currentView === "detail" ? (
          <ListBulletIcon className="h-6 w-6" />
        ) : (
          <TableCellsIcon className="h-6 w-6" />
        )}
      </Button>
      <Button
        className={getButtonClassName("filter")}
        onClick={() => handleClick("filter")}
        startContent={<FunnelIcon className="h-6 w-6" />}
      >
        Filter
      </Button>
      <Button
        className={getButtonClassName("download")}
        onClick={() => handleClick("download")}
        startContent={<ArrowDownTrayIcon className="h-6 w-6" />}
      >
        Download
      </Button>
      <Button
          className={getButtonClassName("saved")}
          onClick={() => setCurrentView("saved")}
          startContent={<BookmarkSquareIcon className="w-6 h-6" />}
        >
          Saved
        </Button>
    </div>
  );
};

export default SearchBarComponent;
