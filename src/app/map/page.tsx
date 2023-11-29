"use client";

import React, { FC, useState } from "react";
import { NextUIProvider } from "@nextui-org/react";
import { FilterProvider } from "@/context/FilterContext";
import {
  Header,
  PropertyMap,
  PropertyDetailSection,
  SidePanel,
  MapControlBar,
  FilterView,
  PropertyCard, // Import PropertyCard
} from "../components";

export type BarClickOptions = "filter" | "download" | "detail" | "saved";

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");
  const [savedProperties, setSavedProperties] = useState<any[]>([]);

  return (
    <FilterProvider>
      <NextUIProvider>
        <div className="h-screen overflow-hidden">
          <Header />
          <div className="flex h-full relative">
            <div className="flex-grow h-full">
              <PropertyMap 
                setFeaturesInView={setFeaturesInView} 
                setSavedProperties={setSavedProperties}
              />
            </div>
            <SidePanel>
              <MapControlBar setCurrentView={setCurrentView} currentView={currentView} />
              {currentView === "filter" && <FilterView />}
              {currentView === "detail" && (
                <PropertyDetailSection featuresInView={featuresInView} />
              )}
              {currentView === "saved" && savedProperties.map((property, index) => (
                <PropertyCard key={index} feature={property} />
              ))}
            </SidePanel>
          </div>
        </div>
      </NextUIProvider>
    </FilterProvider>
  );
};

export default Page;
