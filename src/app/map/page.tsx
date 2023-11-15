"use client";

import React, { FC, useEffect, useState } from "react";
import { NextUIProvider, Button } from "@nextui-org/react";
import { FilterProvider } from "@/context/FilterContext";
import {
  Header,
  PropertyMap,
  PropertyDetailSection,
  SidePanel,
  MapControlBar,
  FilterView,
} from "../components";

export type BarClickOptions = "filter" | "download" | "detail";

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");

  useEffect(() => {
    console.log(featuresInView);
  }, [featuresInView]);

  return (
    <FilterProvider>
      <NextUIProvider>
        <div className="h-screen overflow-hidden">
          <Header />
          <div className="flex h-full relative">
            <div className="flex-grow h-full">
              <PropertyMap setFeaturesInView={setFeaturesInView} />
            </div>
            <SidePanel>
              <MapControlBar setCurrentView={setCurrentView} />
              {currentView === "filter" && <FilterView />}
              {currentView === "detail" && (
                <PropertyDetailSection featuresInView={featuresInView} />
              )}
            </SidePanel>
          </div>
        </div>
      </NextUIProvider>
    </FilterProvider>
  );
};

export default Page;
