"use client";

import { FC, useState } from "react";
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
import Hotjar from "../components/Hotjar";
import { MapboxGeoJSONFeature } from "mapbox-gl";

export type BarClickOptions = "filter" | "download" | "detail" | "list";

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  const [featureCount, setFeatureCount] = useState<number>(0);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");
  const [loading, setLoading] = useState(false);
  const [selectedProperty, setSelectedProperty] =
    useState<MapboxGeoJSONFeature | null>(null);

  return (
    <FilterProvider>
      <NextUIProvider>
      <a href="#main" tabIndex={0}>Skip to maiMAPt</a>
        <div className="flex flex-col h-screen">
          <Header />
          <main className="flex flex-grow overflow-hidden" id="main">
            <div className="flex-grow overflow-auto">
              <PropertyMap
                setFeaturesInView={setFeaturesInView}
                setLoading={setLoading}
                selectedProperty={selectedProperty}
                setSelectedProperty={setSelectedProperty}
                setFeatureCount={setFeatureCount}
              />
            </div>
            <SidePanel>
              {currentView === "filter" ? (
                <FilterView setCurrentView={setCurrentView} />
              ) : (
                <>
                  {!selectedProperty && (
                    <div className="pt-2 sticky top-0 z-10">
                      <SidePanelControlBar
                        currentView={currentView}
                        setCurrentView={setCurrentView}
                        featureCount={featureCount}
                      />
                    </div>
                  )}
                  {currentView === "download" ? (
                    <div className="p-4 mt-8 text-center">
                      <h2 className="text-2xl font-bold mb-4">
                        Access Our Data
                      </h2>
                      <p>
                        If you are interested in accessing the data behind this
                        dashboard, please reach out to us at
                        <a
                          href="mailto:cleanandgreenphl@gmail.com"
                          className="text-blue-600 hover:text-blue-800 underline"
                        >
                          {" "}
                          cleanandgreenphl@gmail.com
                        </a>
                        . Let us know who you are and why you want the data. We
                        are happy to share the data with anyone with
                        community-oriented interests.
                      </p>
                    </div>
                  ) : (
                    <PropertyDetailSection
                      featuresInView={featuresInView}
                      display={currentView as "detail" | "list"}
                      loading={loading}
                      selectedProperty={selectedProperty}
                      setSelectedProperty={setSelectedProperty}
                    />
                  )}
                </>
              )}
            </SidePanel>
          </main>
          <Hotjar />
        </div>
      </NextUIProvider>
    </FilterProvider>
  );
};

export default Page;
