import React, { FC, useState } from "react";

interface SidePanelProps {
  children?: React.ReactNode;
  isVisible: string;
}

const SidePanel: FC<SidePanelProps> = ({ children, isVisible }) => {
  const [expanded, setExpanded] = useState(true);

  return (
    <div
      role="region"
      aria-label="results sidepanel"
      className={`h-full transition-all duration-300 ${
        expanded ? "w-5/12" : "w-0"
      } bg-white overflow-auto max-sm:w-full ${isVisible}`}
    >
      {children}
    </div>
  );
};

export default SidePanel;
