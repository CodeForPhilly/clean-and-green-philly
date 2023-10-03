import React, { useState } from "react";
import { Input, Button, ButtonGroup } from "@nextui-org/react";
import {
  BookmarkIcon,
  FunnelIcon,
  ArrowDownTrayIcon,
} from "@heroicons/react/20/solid";

type MapControlBarProps = {
  currentView: string;
  setCurrentView: (view: string) => void;
};

const SearchBarComponent: React.FC<MapControlBarProps> = ({
  currentView,
  setCurrentView,
}) => {
  const [searchTerm, setSearchTerm] = useState<string>("");

  const handleClick = (view: string) => {
    setCurrentView(view);
  };

  return (
    <div className="flex items-center">
      <Input
        value={searchTerm}
        onValueChange={setSearchTerm}
        placeholder="Search..."
        startContent={<BookmarkIcon className="w-5 h-5" />}
        width="50%"
      />

      <ButtonGroup fullWidth className="w-1/2">
        <Button
          onClick={() => handleClick("saved")}
          startContent={<BookmarkIcon className="w-5 h-5" />}
        >
          Saved
        </Button>
        <Button
          onClick={() => handleClick("filter")}
          startContent={<FunnelIcon className="w-5 h-5" />}
        >
          Filter
        </Button>
        <Button
          onClick={() => handleClick("download")}
          startContent={<ArrowDownTrayIcon className="w-5 h-5" />}
        >
          Download
        </Button>
      </ButtonGroup>
    </div>
  );
};

export default SearchBarComponent;
