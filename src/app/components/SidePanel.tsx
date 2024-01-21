import React, { FC, useState } from "react";

interface SidePanelProps {
  children?: React.ReactNode;
}

const SidePanel: FC<SidePanelProps> = ({ children }) => {
  const [expanded, setExpanded] = useState(true);

  return (
    <div
      className={`h-full transition-all duration-300 ${
        expanded ? "w-5/12" : "w-0"
      } bg-white overflow-auto`}
    >
      {children}
    </div>
  );
};

export default SidePanel;
