"use client";

import React, { FC, useEffect, useState } from "react";
import { NextUIProvider } from "@nextui-org/react";
import { FilterProvider } from "@/context/FilterContext";
import {
  Header,
  PropertyMap,
  PropertyDetailSection,
  SidePanel,
  MapControlBar,
  FilterView
} from "../components";

export type BarClickOptions = "filter" | "download" | "detail" | "list" | "saved";

const propertyMapZoom = 14;

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");
  const [zoom, setZoom] = useState<number>(propertyMapZoom);
  const [loading, setLoading] = useState(false);
  const [savedPropertiesList, setSavedPropertiesList] = useState([]);
  useEffect(() => {
    // Load saved properties from local storage when component mounts
    const savedProperties = localStorage.getItem('savedProperties');
    if (savedProperties) {
      setSavedPropertiesList(JSON.parse(savedProperties));
    }
  }, []);
  const handleSaveProperty = (property) => {
    if (!property || !property.OPA_ID) {
      console.error("Property or property.OPA_ID is undefined", property);
      return;
    }
  
    // Use the state instead of reading from local storage again
    const propertyIndex = savedPropertiesList.findIndex(savedProperty => 
      savedProperty.OPA_ID === property.OPA_ID);
  
    const updatedSavedProperties = [...savedPropertiesList];
    if (propertyIndex > -1) {
      updatedSavedProperties.splice(propertyIndex, 1);
    } else {
      updatedSavedProperties.push(property);
    }
  
    // Update both local storage and state
    localStorage.setItem('savedProperties', JSON.stringify(updatedSavedProperties));
    setSavedPropertiesList(updatedSavedProperties);
  };
  
  // Debugging statement
  if (currentView === "saved") {
    console.log('Saved properties:', savedPropertiesList);
  }
  
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
                handleSaveProperty={handleSaveProperty}
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
                    featuresInView={featuresInView}  // Use the properties in view
                    display={currentView}
                    loading={loading}
                    propertyMapZoom={propertyMapZoom}
                    zoom={zoom}
                  />
                )}
                {currentView === "saved" && (
                  <PropertyDetailSection
                    featuresInView={savedPropertiesList.map(property => ({
                      ...property,
                      key: property.OPA_ID // Ensure each property has a unique key
                    }))}
                    display="detail" // or whichever format you wish to display saved properties
                    loading={false}
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
