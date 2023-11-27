import React, { useState } from "react";
import { Input, Button } from "@nextui-org/react";
import { ArrowDownTrayIcon, ListBulletIcon } from "@heroicons/react/20/solid";
import {
  FunnelIcon,
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

  return (
    <div className="flex items-center space-x-2 bg-white p-2 h-12">
      <Button className="bg-white" onClick={toggleDetailView}>
        {currentView === "detail" ? (
          <ListBulletIcon className="h-6 w-6" />
        ) : (
          <TableCellsIcon className="h-6 w-6" />
        )}
      </Button>
      <Input
        value={searchTerm}
        onValueChange={setSearchTerm}
        placeholder="Search..."
        startContent={<MagnifyingGlassIcon className="h-6 w-6" />}
        className="w-1/2"
      />
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
    </div>
  );
};

export default SearchBarComponent;
