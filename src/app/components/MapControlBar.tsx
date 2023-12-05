import React, { useState } from "react";
import { Input, Button } from "@nextui-org/react";
import { ArrowDownTrayIcon, ListBulletIcon } from "@heroicons/react/20/solid";
import {
  FunnelIcon,
  BookmarkSquareIcon,
  MagnifyingGlassIcon,
  TableCellsIcon,
} from "@heroicons/react/24/outline";
import { BarClickOptions } from "@/app/map/page";


type MapControlBarProps = {
  currentView: BarClickOptions;
  setCurrentView: (view: BarClickOptions) => void;
};

const SearchBarComponent: React.FC<MapControlBarProps> = ({
  currentView,
  setCurrentView,
}) => {
  const [searchTerm, setSearchTerm] = useState<string>("");

  const handleClick = (view: BarClickOptions) => {
    setCurrentView(view);
  };

  const toggleDetailView = () => {
    setCurrentView(currentView === "detail" ? "list" : "detail");
  };

  const getButtonClassName = (view: BarClickOptions) => {
    return currentView === view ? "bg-green-60" : "";
  };

  return (
    <div className="flex items-center space-x-2 bg-white p-2 h-12">
      <Button className="bg-white" onClick={toggleDetailView}>
        {currentView === "detail" ? (
          <ListBulletIcon className="h-5 w-5" />
        ) : (
          <TableCellsIcon className="h-5 w-5" />
        )}
      </Button>
      <Input
        value={searchTerm}
        onValueChange={setSearchTerm}
        placeholder="Search..."
        startContent={<MagnifyingGlassIcon className="w-5 h-5" />}
        width="40%"
      />

        <Button
          className={getButtonClassName("filter")}
          onClick={() => handleClick("filter")}
          startContent={<FunnelIcon className="w-5 h-5" />}
        >
          Filter
        </Button>
        <Button
          className={getButtonClassName("download")}
          onClick={() => handleClick("download")}
          startContent={<ArrowDownTrayIcon className="w-5 h-5" />}
        >
          Download
        </Button>
        <Button
          className={getButtonClassName("saved")}
          onClick={() => setCurrentView("saved")}
          startContent={<BookmarkSquareIcon className="w-5 h-5" />}
        >
          Saved
        </Button>
    </div>
  );
  
};

export default SearchBarComponent;
