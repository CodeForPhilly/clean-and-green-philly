import React, { useState } from "react";
import { Input, Button, ButtonGroup } from "@nextui-org/react";
import {
  ListBulletIcon,
  MagnifyingGlassIcon,
  AdjustmentsHorizontalIcon,
  ArrowDownTrayIcon,
  BookmarkSquareIcon,
  // Import an icon for the default view button if available
} from "@heroicons/react/20/solid";
import { BarClickOptions } from "@/app/map/page";

type MapControlBarProps = {
  setCurrentView: (view: BarClickOptions) => void;
  currentView: BarClickOptions;
};

const MapControlBar: React.FC<MapControlBarProps> = ({
  setCurrentView,
  currentView,
}) => {
  const [searchTerm, setSearchTerm] = useState<string>("");

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
        startContent={<MagnifyingGlassIcon className="w-5 h-5" />} 
      />

      <ButtonGroup fullWidth className="w-1/2">
        <Button
          className={getButtonClassName("detail")}
          onClick={() => setCurrentView("detail")}

          startContent={<ListBulletIcon className="w-5 h-5" />} 
        >
          Default
        </Button>
        <Button
          className={getButtonClassName("filter")}
          onClick={() => setCurrentView("filter")}
          startContent={<AdjustmentsHorizontalIcon className="w-5 h-5" />}
        >
          Filter
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

export default MapControlBar;
