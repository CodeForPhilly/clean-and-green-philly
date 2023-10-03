import React, { FC, useEffect, useState } from "react";
import { Popup, Map as MapboxMap } from "mapbox-gl";
import { mapboxAccessToken, apiBaseUrl } from "../../config/config";
import ZoomModal from "./ZoomModal";
import { useFilter } from "@/context/FilterContext";

let popup: Popup | null = null;

interface PropertyMapProps {
  setFeaturesInView: (features: any[]) => void;
}

const PropertyMap: FC<PropertyMapProps> = ({ setFeaturesInView }) => {
  const [isZoomModalHidden, setIsZoomModalHidden] = useState(true);
  const { filter } = useFilter();
  const [map, setMap] = useState<MapboxMap | null>(null);

  const updateFilter = () => {
    if (map) {
      const isAnyFilterEmpty = Object.values(filter).some(
        (values) => values.length === 0
      );

      if (isAnyFilterEmpty) {
        map.setFilter("vacant_properties", ["==", ["id"], ""]);
      } else {
        const mapFilter = Object.entries(filter).reduce(
          (acc, [property, values]) => {
            if (values.length) {
              acc.push(["in", property, ...values]);
            }
            return acc;
          },
          [] as any[]
        );

        map.setFilter("vacant_properties", ["all", ...mapFilter]);
      }
    }
  };

  useEffect(() => {
    const mapInstance = new MapboxMap({
      container: "mapContainer",
      style: "mapbox://styles/mapbox/light-v10",
      center: [-75.1652, 39.9526],
      zoom: 13,
      accessToken: mapboxAccessToken,
    });

    mapInstance.on("load", async () => {
      const minZoom = 13;

      mapInstance.on("zoomend", () => {
        setIsZoomModalHidden(mapInstance.getZoom() >= minZoom);
      });

      mapInstance.addSource("vacant_properties", {
        type: "vector",
        tiles: [`${apiBaseUrl}/api/generateTiles/{z}/{x}/{y}`],
        minzoom: minZoom,
        maxzoom: 23,
      });

      mapInstance.addLayer({
        id: "vacant_properties",
        type: "fill",
        source: "vacant_properties",
        "source-layer": "vacant_properties",
        paint: {
          "fill-color": "#0000FF",
          "fill-opacity": 0.2,
        },
      });

      updateFilter();

      mapInstance.on("moveend", () => {
        let features = mapInstance.queryRenderedFeatures();
        features = features.filter(
          (feature) => feature.layer.id === "vacant_properties"
        );
        setFeaturesInView(features);
      });

      mapInstance.on("click", "vacant_properties", (e) => {
        if (popup) {
          popup.remove();
        }

        if (e.features?.length) {
          const feature = e.features[0];
          const propertyHTML = feature.properties
            ? Object.keys(feature.properties)
                .map((key) => `<b>${key}</b>: ${feature.properties![key]}<br/>`)
                .join("")
            : "No properties available";

          popup = new Popup({ offset: [0, -15] })
            .setLngLat(e.lngLat)
            .setHTML(`<div style='color: black;'><p>${propertyHTML}</p></div>`)
            .addTo(mapInstance);
        }
      });

      mapInstance.on("mouseenter", "vacant_properties", () => {
        mapInstance.getCanvas().style.cursor = "pointer";
      });

      mapInstance.on("mouseleave", "vacant_properties", () => {
        mapInstance.getCanvas().style.cursor = "";
      });

      setMap(mapInstance);
    });
  }, []);

  useEffect(() => {
    updateFilter();
  }, [filter]);

  return (
    <div className="relative h-full w-full">
      <div id="mapContainer" className="h-full w-full"></div>
      <ZoomModal isHidden={isZoomModalHidden} />
    </div>
  );
};

export default PropertyMap;
