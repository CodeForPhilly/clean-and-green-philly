import React, { useState } from "react";
import { Input, Button, ButtonGroup } from "@nextui-org/react";
import {
  BookmarkIcon, // This is the icon currently used for the "Search..." input
  FunnelIcon,
  ArrowDownTrayIcon,
  BookmarkSquareIcon, // Assuming you want to use this for the "Saved" button
} from "@heroicons/react/20/solid";
import { BarClickOptions } from "@/app/map/page";

type MapControlBarProps = {
  setCurrentView: (view: BarClickOptions) => void;
};

const MapControlBar: React.FC<MapControlBarProps> = ({
  setCurrentView,
}) => {
  const [searchTerm, setSearchTerm] = useState<string>("");

  const handleClick = (view: BarClickOptions) => {
    setCurrentView(view);
  };

  return (
    <div className="flex items-center">
      <Input
        value={searchTerm}
        onValueChange={setSearchTerm}
        placeholder="Search..."
        width="50%"
        // If you want an icon inside the search bar, it should be here
        startContent={<BookmarkIcon className="w-5 h-5" />} 
      />

      <ButtonGroup fullWidth className="w-1/2">
        <Button
          onClick={() => handleClick("filter")}
          startContent={<FunnelIcon className="w-5 h-5" />}
        >
          Filter
        </Button>
        <Button
          onClick={() => handleClick("download")}
          startContent={<ArrowDownTrayIcon className="w-5 h-5" />} // Ensure this is the correct icon for "Download"
        >
          Download
        </Button>
        <Button
          onClick={() => handleClick("saved")}
          startContent={<BookmarkSquareIcon className="w-5 h-5" />} // Use a distinct icon for "Saved"
        >
          Saved
        </Button>
      </ButtonGroup>
    </div>
  );
};

export default MapControlBar;
