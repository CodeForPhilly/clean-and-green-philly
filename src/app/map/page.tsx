"use client";

import React, { FC, useState } from "react";
import { NextUIProvider } from "@nextui-org/react";
import { FilterProvider } from "@/context/FilterContext";
import {
  Header,
  PropertyMap,
  PropertyDetailSection,
  SidePanel,
  SidePanelControlBar,
  FilterView,
} from "../components";
import { MapboxGeoJSONFeature } from "mapbox-gl";

export type BarClickOptions = "filter" | "download" | "detail" | "list";

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");
  const [loading, setLoading] = useState(false);
  const [selectedProperty, setSelectedProperty] = useState<MapboxGeoJSONFeature | null>(null);

  return (
    <FilterProvider>
      <NextUIProvider>
        <div className="h-screen overflow-hidden">
          <Header />
          <div className="flex h-full relative">
            <div className="flex-grow h-full">
              <PropertyMap
                setFeaturesInView={setFeaturesInView}
                setLoading={setLoading}
                setSelectedProperty={setSelectedProperty}
              />
            </div>
            <SidePanel>
              <SidePanelControlBar
                currentView={currentView}
                setCurrentView={setCurrentView}
              />
              {currentView === "filter" && <FilterView />}
              {["detail", "list"].includes(currentView) && (
                <PropertyDetailSection
                  featuresInView={featuresInView}
                  display={currentView as "detail" | "list"}
                  loading={loading}
                  selectedProperty={selectedProperty}
                  setSelectedProperty={setSelectedProperty}
                />
              )}
              {currentView === "download" && (
                <div className="p-4 mt-8 text-center">
                  <h2 className="text-2xl font-bold mb-4">Access Our Data</h2>
                  <p>
                    If you are interested in accessing the data behind this
                    dashboard, please reach out to us at
                    <a
                      href="mailto:cleangreenphilly@gmail.com"
                      className="text-blue-600 hover:text-blue-800 underline"
                    >
                      {" "}
                      cleangreenphilly@gmail.com
                    </a>
                    . Let us know who you are and why you want the data. We are
                    happy to share the data with anyone with community-oriented
                    interests!
                  </p>
                </div>
              )}
            </SidePanel>
          </div>
        </div>
      </NextUIProvider>
    </FilterProvider>
  );
};

export default Page;
