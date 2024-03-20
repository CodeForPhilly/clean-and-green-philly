"use client";

import React, { FC, useState, useEffect, useRef } from "react";
import { MapboxGeoJSONFeature } from "mapbox-gl";

interface SidePanelProps {
  children?: React.ReactNode;
  isVisible: string;
  selectedProperty: MapboxGeoJSONFeature | null;
}

const SidePanel: FC<SidePanelProps> = ({ children, isVisible, selectedProperty }) => {
  const [expanded, setExpanded] = useState(true);
  const panelRef = useRef<HTMLDivElement>(null);

  /* Scrolls the selected property to the top onmount for mobile */
  useEffect(() => {
    if (panelRef.current) {
      panelRef.current.scrollTop = 0;
    }
  }, [selectedProperty])

  return (
    <div
      role="region"
      aria-label="results sidepanel"
      className={`h-full transition-all duration-300 ${
        expanded ? "w-5/12" : "w-0"
      } bg-white overflow-auto max-sm:w-full ${isVisible}`}
      ref={panelRef}
    >
      {children}
    </div>
  );
};

export default SidePanel;
