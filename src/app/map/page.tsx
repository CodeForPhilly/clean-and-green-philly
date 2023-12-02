"use client";

import React, { FC, useState, } from "react";
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

export type BarClickOptions = "filter" | "detail" | "saved";

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");
  const [savedProperties, setSavedProperties] = useState<any[]>([]);
  const [savedStatus, setSavedStatus] = useState<{ [key: string]: boolean }>({});

  const handleSaveProperty = (property: any) => {
    setSavedProperties(prevProperties => {
      const isSaved = prevProperties.some(savedProperty => savedProperty.properties.OPA_ID === property.properties.OPA_ID);
  
      if (isSaved) {
        return prevProperties.filter(savedProperty => savedProperty.properties.OPA_ID !== property.properties.OPA_ID);
      } else {
        return [...prevProperties, property];
      }
    });
  
    setSavedStatus(prevStatus => ({
      ...prevStatus,
      [property.properties.OPA_ID]: !(prevStatus[property.properties.OPA_ID] || false)
    }));
  };
  

  return (
    <FilterProvider>
      <NextUIProvider>
        <div className="h-screen overflow-hidden">
          <Header />
          <div className="flex h-full relative">
            <div className="flex-grow h-full">
              <PropertyMap 
                setFeaturesInView={setFeaturesInView} 
                setSavedProperties={handleSaveProperty}
                savedProperties={savedProperties} // Pass savedProperties to PropertyMap
                savedStatus={savedStatus} // Pass savedStatus to PropertyMap
              />
            </div>
            <SidePanel>
              <MapControlBar setCurrentView={setCurrentView} currentView={currentView} />
              {currentView === "filter" && <FilterView />}
              {currentView === "detail" && (
                <PropertyDetailSection featuresInView={featuresInView} />
              )}
              {currentView === "saved" && (
                <PropertyDetailSection featuresInView={savedProperties} />
              )}
            </SidePanel>
          </div>
        </div>
      </NextUIProvider>
    </FilterProvider>
  );
};

export default Page;
