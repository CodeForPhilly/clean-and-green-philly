"use client";

import React, { FC, useState } from "react";

interface SidePanelProps {
  children?: React.ReactNode;
}

const SidePanel: FC<SidePanelProps> = ({ children }) => {
  const [expanded, setExpanded] = useState(true);

  return (
    <div
      role="region"
      aria-label="results sidepanel"
      className={`min-h-[calc(100svh-165px)] max-h-[calc(100svh-165px)] h-full overflow-y-scroll transition-all duration-300 bg-white ${
        expanded ? "w-5/12" : "w-0"
      }`}
    >
      {children}
    </div>
  );
};

export default SidePanel;
