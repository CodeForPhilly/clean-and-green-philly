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
} from "./components";

export type BarClickOptions = "filter" | "download" | "detail" | "list" | "saved"; // Added 'saved'

const propertyMapZoom = 14;

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");
  const [zoom, setZoom] = useState<number>(propertyMapZoom);
  const [loading, setLoading] = useState(false);
  const [savedStatus, setSavedStatus] = useState<{ [key: string]: boolean }>({});
  const [savedProperties, setSavedProperties] = useState<any[]>([]);

  const handleSaveProperty = (property: any) => {
    setSavedProperties(prevProperties => {
      const isSaved = prevProperties.some(savedProperty => savedProperty.properties.OPA_ID === property.properties.OPA_ID);
      return isSaved ? prevProperties.filter(savedProperty => savedProperty.properties.OPA_ID !== property.properties.OPA_ID) : [...prevProperties, property];
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
                setZoom={setZoom}
                setLoading={setLoading}
                setSavedProperties={handleSaveProperty}
                savedProperties={savedProperties}
                savedStatus={savedStatus}
              />
            </div>
            <SidePanel>
              <MapControlBar
                currentView={currentView}
                setCurrentView={setCurrentView}
              />
              {currentView === "filter" && <FilterView />}
              {["detail", "list", "saved"].includes(currentView) && (
                <PropertyDetailSection
                  featuresInView={currentView === "saved" ? savedProperties : featuresInView}
                  display={currentView === "list" ? "list" : "detail"}
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
