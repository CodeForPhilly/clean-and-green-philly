import React, { FC, useEffect, useState } from "react";
import { Popup, Map as MapboxMap } from "mapbox-gl";
import { mapboxAccessToken, apiBaseUrl } from "../config/config";
import ZoomModal from "./ZoomModal";

let popup: Popup | null = null;

interface PropertyMapProps {
  setFeaturesInView: (features: any[]) => void;
}

const PropertyMap: FC<PropertyMapProps> = ({ setFeaturesInView }) => {
  const [isZoomModalHidden, setIsZoomModalHidden] = useState(true);

  useEffect(() => {
    const map = new MapboxMap({
      container: "mapContainer",
      style: "mapbox://styles/mapbox/streets-v9",
      center: [-75.1652, 39.9526],
      zoom: 13,
      accessToken: mapboxAccessToken,
    });

    map.on("load", async () => {
      const minZoom = 13;

      map.on("zoomend", () => {
        setIsZoomModalHidden(map.getZoom() >= minZoom);
      });

      map.addSource("vacant_properties", {
        type: "vector",
        tiles: [`${apiBaseUrl}/api/generateTiles/{z}/{x}/{y}`],
        minzoom: minZoom,
        maxzoom: 23,
      });

      map.addLayer({
        id: "vacant_properties",
        type: "fill",
        source: "vacant_properties",
        "source-layer": "vacant_properties",
        paint: {
          "fill-color": "#0000FF",
          "fill-opacity": 0.2,
        },
      });

      map.on("moveend", () => {
        let features = map.queryRenderedFeatures();
        features = features.filter(
          (feature) => feature.layer.id === "vacant_properties"
        );
        setFeaturesInView(features);
      });

      map.on("click", "vacant_properties", (e) => {
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
            .addTo(map);
        }
      });

      map.on("mouseenter", "vacant_properties", () => {
        map.getCanvas().style.cursor = "pointer";
      });

      map.on("mouseleave", "vacant_properties", () => {
        map.getCanvas().style.cursor = "";
      });
    });
  }, []);

  return (
    <div className="relative h-full w-full">
      <div id="mapContainer" className="h-full w-full"></div>
      <ZoomModal isHidden={isZoomModalHidden} />
    </div>
  );
};

export default PropertyMap;
