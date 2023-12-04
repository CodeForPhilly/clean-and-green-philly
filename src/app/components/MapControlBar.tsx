import React, { useState } from "react";
import { Input, Button, ButtonGroup } from "@nextui-org/react";
import {
  FunnelIcon,
  TableCellsIcon,
  MagnifyingGlassIcon,
  BookmarkSquareIcon,
  ArrowDownTrayIcon
  // Import an icon for the default view button if available
} from "@heroicons/react/20/solid";
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

  const getButtonClassName = (view: BarClickOptions) => {
    return currentView === view ? "bg-green-60" : "bg-gray-40";
  };

  return (
    <div className="flex items-center">
      <Input
        value={searchTerm}
        onValueChange={setSearchTerm}
        placeholder="Search..."
        width="50%"
        startContent={<MagnifyingGlassIcon className="h-6 w-6" />}
        className="w-1/2"
      />
      <ButtonGroup>
        <Button
          onClick={() => handleClick("filter")}
          startContent={<FunnelIcon className="h-6 w-6" />}
          className="bg-white"
        >
          Filter
        </Button>
        <Button
          onClick={() => handleClick("download")}
          startContent={<ArrowDownTrayIcon className="h-6 w-6" />}
          className="bg-white"
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
      </ButtonGroup>
    </div>
  );
  
};

export default SearchBarComponent;
