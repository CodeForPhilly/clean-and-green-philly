"use client";

import React, { FC, useState } from "react";
import { NextUIProvider, Button } from "@nextui-org/react";
import { FilterProvider } from "@/context/FilterContext";
import {
  Header,
  PropertyMap,
  PropertyDetailSection,
  SidePanel,
  MapControlBar,
  FilterView,
} from "./components";

export type BarClickOptions = "filter" | "download" | "detail" | "list";

const propertyMapZoom = 14;

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");
  const [zoom, setZoom] = useState<number>(propertyMapZoom);
  const [loading, setLoading] = useState(false);

  return (
    <FilterProvider>
      <NextUIProvider>
        <div className="h-screen overflow-hidden">
          <Header />
          <div className="flex h-full relative">
            <div className="flex-grow h-full">
              <PropertyMap
                setFeaturesInView={setFeaturesInView}
                setZoom={setZoom}
                setLoading={setLoading}
              />
            </div>
            <SidePanel>
              <MapControlBar
                currentView={currentView}
                setCurrentView={setCurrentView}
              />
              {currentView === "filter" && <FilterView />}
              {["detail", "list"].includes(currentView) && (
                <PropertyDetailSection
                  featuresInView={featuresInView}
                  display={currentView as "detail" | "list"}
                  loading={loading}
                  propertyMapZoom={propertyMapZoom}
                  zoom={zoom}
                />
              )}
            </SidePanel>
          </div>
        </div>
      </NextUIProvider>
    </FilterProvider>
  );
};

export default Page;
