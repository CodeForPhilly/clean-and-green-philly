"use client";

import React, { useRef, useState, useEffect } from "react";
import {
  FilterView,
  PropertyDetailSection,
  PropertyMap,
  SidePanel,
  SidePanelControlBar,
} from "@/components";
import { FilterProvider } from "@/context/FilterContext";
import { NextUIProvider, Spinner } from "@nextui-org/react";
import { X, GlobeHemisphereWest, ListBullets } from "@phosphor-icons/react";
import { MapGeoJSONFeature } from "maplibre-gl";
import StreetView from "../../../components/StreetView";
import { centroid } from "@turf/centroid";
import { Position } from "geojson";
import { ThemeButton } from "../../../components/ThemeButton";
import { useRouter } from "next/navigation";
import { ViewState } from "react-map-gl";
import { PiX } from "react-icons/pi";

export type BarClickOptions = "filter" | "download" | "detail" | "list";

type MapPageProps = {
  params: {
    opa_id: string;
  };
};

const MapPage = ({ params }: MapPageProps) => {
  const [featuresInView, setFeaturesInView] = useState<MapGeoJSONFeature[]>([]);
  const [featureCount, setFeatureCount] = useState<number>(0);
  const [currentView, setCurrentView] = useState<BarClickOptions>("detail");
  const [loading, setLoading] = useState(true);
  const [selectedProperty, setSelectedProperty] =
    useState<MapGeoJSONFeature | null>(null);
  const [isStreetViewModalOpen, setIsStreetViewModalOpen] =
    useState<boolean>(false);
  const [streetViewLocation, setStreetViewLocation] = useState<Position | null>(
    null
  );
  const [smallScreenMode, setSmallScreenMode] = useState("map");
  const prevRef = useRef("map");
  const sizeRef = useRef(0);
  const prevCoordinateRef = useRef<Position | null>(null);
  const linkedPropertyRef = useRef<string | null>(null);
  const [initialViewState, setInitialViewState] = useState<ViewState>({
    longitude: -75.1628565788269,
    latitude: 39.97008211622267,
    zoom: 11,
    bearing: 0,
    pitch: 0,
    padding: { top: 0, bottom: 0, left: 0, right: 0 },
  });
  const [isLinkedPropertyParsed, setIsLinkedPropertyParsed] = useState(false);
  const [savedPropertyCount, setSavedPropertyCount] = useState(0);
  const [shouldFilterSavedProperties, setShouldFilterSavedProperties] =
    useState(false);

  const router = useRouter();

  // Handle Routing
  useEffect(() => {
    const { opa_id } = params;

    const getLinkedPropertyDetails = async () => {
      // Check if OPA ID is present in URL
      // It should be the only URL parameter and a string-like collection of numbers between 8 and 9 characters

      // Get property metadata
      try {
        const objectMetadataResponse = await fetch(
          `https://storage.googleapis.com/storage/v1/b/cleanandgreenphl/o/${linkedPropertyRef.current}.jpg`
        );
        const objectMetadata = await objectMetadataResponse.json();
        const { metadata } = objectMetadata;
        let { location } = metadata;
        location = JSON.parse(location.replace(/'/g, '"'));
        setInitialViewState({
          ...initialViewState,
          longitude: location.lng,
          latitude: location.lat,
          zoom: 18,
        });
        setIsLinkedPropertyParsed(true);
      } catch {
        router.push("/find-properties");
      }
    };

    if (!opa_id) {
      // do nothing, load map
      setIsLinkedPropertyParsed(true);
    } else if (opa_id?.length === 1 && opa_id[0].match(/^\d{8,9}$/)) {
      if (opa_id.toString() === linkedPropertyRef.current?.toString()) return;
      linkedPropertyRef.current = opa_id[0];
      getLinkedPropertyDetails();
    } else {
      // Invalid OPA ID- redirect to main map page
      router.push("/find-properties");
    }
  }, [initialViewState, params, router]);

  useEffect(() => {
    // This useEffect navigates to the linked property when it is loaded
    if (!featuresInView || !linkedPropertyRef.current) return;

    const linkedProperty = featuresInView.find(
      (feature) =>
        feature.properties.opa_id.toString() ===
        linkedPropertyRef?.current?.toString()
    );

    if (
      linkedProperty &&
      linkedProperty.properties.opa_id !== selectedProperty?.properties.opa_id
    ) {
      setSelectedProperty(linkedProperty);
      linkedPropertyRef.current = null;
    }
  }, [featuresInView, selectedProperty?.properties.opa_id]);

  useEffect(() => {
    if (!selectedProperty) return;
    const opa_id = selectedProperty.properties.opa_id;
    history.replaceState(null, "", `/find-properties/${opa_id}`);
  }, [selectedProperty]);

  const updateCurrentView = (view: BarClickOptions) => {
    setCurrentView(view === currentView ? "detail" : view);
    if (
      prevRef.current === "map" &&
      window.innerWidth < 640 &&
      (view === "filter" ||
        (Object.keys(params).length === 0 && prevCoordinateRef.current))
    ) {
      setSmallScreenMode((prev: string) =>
        prev === "map" ? "properties" : "map"
      );
    }
  };

  const updateSmallScreenMode = () =>
    setSmallScreenMode((prev: string) => {
      prevRef.current = prev === "map" ? "properties" : "map";
      setCurrentView("detail");
      return prevRef.current;
    });

  /*
      Because filter view is part of smallScreenMode = properties,
      we need to switch to properties when filtering from map.
      If filters are selected from small screen but screen is resized before applying them,
      restores original small screen mode with the filters.
     */
  useEffect(() => {
    sizeRef.current = window.innerWidth;
    const updateWindowDimensions = () => {
      if (sizeRef.current >= 640 && window.innerWidth < 640) {
        setCurrentView((c) => {
          setSmallScreenMode(c !== "detail" ? "properties" : prevRef.current);
          return c;
        });
      }
      sizeRef.current = window.innerWidth;
    };

    window.addEventListener("resize", updateWindowDimensions);

    return () => window.removeEventListener("resize", updateWindowDimensions);
  }, []);

  const controlBarProps = {
    currentView,
    featureCount,
    loading,
    savedPropertyCount,
    shouldFilterSavedProperties,
    smallScreenMode,
    setShouldFilterSavedProperties,
    updateCurrentView,
  };
  const isVisible = (mode: string) =>
    smallScreenMode === mode ? "" : "max-sm:hidden";

  useEffect(() => {
    if (!selectedProperty) return;
    const propCentroid = centroid(selectedProperty.geometry);
    setStreetViewLocation(propCentroid.geometry.coordinates);

    if (window.innerWidth < 640 && prevRef.current === "map") {
      prevCoordinateRef.current = propCentroid.geometry.coordinates;
      setSmallScreenMode("properties");
    }
  }, [selectedProperty]);

  // Get number of property IDs cached in Web browser's localStorage.
  // In the future, localStorage caching might be replaced by an HTTP call to an API or database.
  useEffect(() => {
    const opa_ids = localStorage.getItem("opa_ids");

    if (opa_ids && JSON.parse(opa_ids).count) {
      setSavedPropertyCount(JSON.parse(opa_ids).count);
    } else {
      setSavedPropertyCount(0);
    }
  }, [currentView, selectedProperty, shouldFilterSavedProperties]);

  return (
      <NextUIProvider>
        <div className="flex flex-col">
          <div className="flex flex-grow overflow-hidden">
            <StreetViewModal
              isOpen={isStreetViewModalOpen}
              onClose={() => setIsStreetViewModalOpen(false)}
            >
              <StreetView
                lat={streetViewLocation?.[1].toString() || ""}
                lng={streetViewLocation?.[0].toString() || ""}
                yaw="180"
                pitch="5"
                fov="0.7"
              />
            </StreetViewModal>
            <div className={`flex-grow ${isVisible("map")}`}>
              <div
                className={`sticky top-0 z-10 sm:hidden ${isVisible("map")}`}
              >
                <SidePanelControlBar {...controlBarProps} />
              </div>
              {isLinkedPropertyParsed ? (
                <PropertyMap
                  featuresInView={featuresInView}
                  setFeaturesInView={setFeaturesInView}
                  setLoading={setLoading}
                  selectedProperty={selectedProperty}
                  setSelectedProperty={setSelectedProperty}
                  setFeatureCount={setFeatureCount}
                  initialViewState={initialViewState}
                  prevCoordinate={prevCoordinateRef.current}
                  setPrevCoordinate={() => (prevCoordinateRef.current = null)}
                />
              ) : (
                <div className="flex w-full h-full justify-center">
                  <Spinner />
                </div>
              )}
            </div>
            <SidePanel
              isVisible={isVisible("properties")}
              selectedProperty={selectedProperty}
            >
              {!selectedProperty && (
                <div className="h-14 sticky top-0 z-10">
                  <SidePanelControlBar {...controlBarProps} />
                </div>
              )}
              {currentView === "download" ? (
                <div className="relative">
                  <ThemeButton
                    color="secondary"
                    className="right-4 lg:right-[24px] absolute top-8 min-w-[3rem]"
                    aria-label="Close download panel"
                    startContent={<PiX />}
                    onPress={() => updateCurrentView("detail")}
                  />
                  <div className="p-4 mt-8 text-center">
                    <h2 className="heading-xl font-semibold mb-4">
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
                </div>
              ) : currentView === "filter" ? (
                <FilterView updateCurrentView={updateCurrentView} />
              ) : (
                <PropertyDetailSection
                  featuresInView={featuresInView}
                  display={currentView as "detail" | "list"}
                  loading={loading}
                  selectedProperty={selectedProperty}
                  setSelectedProperty={setSelectedProperty}
                  setIsStreetViewModalOpen={setIsStreetViewModalOpen}
                  shouldFilterSavedProperties={shouldFilterSavedProperties}
                  setShouldFilterSavedProperties={
                    setShouldFilterSavedProperties
                  }
                  smallScreenMode={smallScreenMode}
                  updateCurrentView={updateCurrentView}
                />
              )}
            </SidePanel>
            <ThemeButton
              aria-label={`Change to ${smallScreenMode}`}
              label={smallScreenMode === "map" ? "List View" : "Map View"}
              className="fixed bottom-10 left-1/2 -ml-[3.5rem] rounded-2xl sm:hidden max-md:min-w-[7rem]"
              onPress={updateSmallScreenMode}
              startContent={
                smallScreenMode === "map" ? (
                  <ListBullets />
                ) : (
                  <GlobeHemisphereWest />
                )
              }
            />
          </div>
        </div>
      </NextUIProvider>
  );
};

export default MapPage;

const StreetViewModal: React.FC<{
  children: React.ReactNode;
  isOpen: boolean;
  onClose: () => void;
}> = ({ children, isOpen, onClose }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
        // return focus
        document.getElementById("outside-iframe-element")?.focus();
        const outsideElement = document.getElementById(
          "outside-iframe-element"
        );
        outsideElement?.focus();
      } else if (event.key === "Tab") {
        // Trap focus within the container
        const container = containerRef.current;
        if (container && !container.contains(document.activeElement)) {
          // If focus goes outside the container, bring it back to the first focusable element inside the container
          const focusableElements = container.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
          );
          if (focusableElements.length > 0) {
            event.preventDefault();
            (focusableElements[0] as HTMLElement).focus();
          }
        }
      }
    };

    const handleDocumentClick = (event: MouseEvent) => {
      if (
        isOpen &&
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        onClose();
        // return focus
        document.getElementById("outside-iframe-element")?.focus();
        const outsideElement = document.getElementById(
          "outside-iframe-element"
        );
        outsideElement?.focus();
      }
    };

    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      document.addEventListener("click", handleDocumentClick);
    } else {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("click", handleDocumentClick);
    }

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("click", handleDocumentClick);
    };
  }, [isOpen, onClose]);

  useEffect(() => {
    // Focus the container when it's opened
    if (isOpen && containerRef.current) {
      containerRef.current.focus();
    }
    // return focus when closed
    document.getElementById("outside-iframe-element")?.focus();
    const outsideElement = document.getElementById("outside-iframe-element");
    outsideElement?.focus();
  }, [isOpen]);

  return (
    <>
      {isOpen && (
        <div
          id="street-view-overlay"
          className="absolute inset-0 z-50 w-full h-full"
          ref={containerRef}
          tabIndex={0} // Make the container focusable
        >
          <div className="fixed w-full h-full bg-black">
            <ThemeButton
              color="tertiary"
              startContent={<X />}
              onPress={onClose}
              tabIndex={0}
              label="Close"
              aria-label="Close full screen street view map"
              className="absolute top-4 right-4"
            />
            {children}
          </div>
        </div>
      )}
    </>
  );
};
