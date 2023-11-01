import React, { FC, useEffect, useState } from "react";
import {  Map as MapboxMap, VectorSource, SourceVectorLayer } from "mapbox-gl";
import { mapboxAccessToken, apiBaseUrl } from "../../config/config";
import ZoomModal from "./ZoomModal";
import { useFilter } from "@/context/FilterContext";
import LegendControl from 'mapboxgl-legend';
import 'mapboxgl-legend/dist/style.css';
import '../globals.css';
import Map, { 
  Source, 
  Layer, 
  Popup,
  NavigationControl, 
  FullscreenControl, 
  ScaleControl,
  GeolocateControl
} from 'react-map-gl';
import type { FillLayer, CustomSource, VectorSourceRaw } from 'react-map-gl';

//let popup: Popup | null = null;

const minZoom = 4;

const VectorTiles: VectorSourceRaw = {
  id: "vacant_properties",
  type: "vector",
  tiles: [`${apiBaseUrl}/api/generateTiles/{z}/{x}/{y}`],
  minzoom: minZoom,
  maxzoom: 23
}

const layerStyle: FillLayer = {
  id: "vacant_properties",
  type: "fill",
  source: "vacant_properties",
  "source-layer": "vacant_properties",
  paint: {
    "fill-color": [
      "match",
      ["get", "guncrime_density"], // get the value of the guncrime_density property
      "Bottom 50%", "#B0E57C", // Light Green
      "Top 50%", "#FFD700", // Gold
      "Top 25%", "#FF8C00", // Dark Orange
      "Top 10%", "#FF4500", // Orange Red
      "Top 5%", "#B22222", // FireBrick
      "Top 1%", "#8B0000", // Dark Rednp
      "#0000FF" // default color if none of the categories match
    ],
    "fill-opacity": 0.7
  },
  metadata: {
    name: 'Guncrime Density',
  }
};



function MapControls() {
  return (
    <>
      <GeolocateControl position="top-left" />
      <FullscreenControl position="top-left" />
      <NavigationControl position="top-left" />
      <ScaleControl />
    </>
  );
}

function MapSourceAndLayer({ onClick }) {
  return (
    <Source id="vacant_properties" {...VectorTiles}>
      <Layer {...layerStyle} onClick={onClick} />
    </Source>
  );
}


export default function PropertyMap() {
  const [isZoomModalHidden, setIsZoomModalHidden] = useState(true);
  const { filter } = useFilter();
  const [map, setMap] = useState<MapboxMap | null>(null);
  const legend = new LegendControl();
  const [popupInfo, setPopupInfo] = useState<any>(null);

  // filter function
  const updateFilter = () => {
    if (!map) return;

    const isAnyFilterEmpty = Object.values(filter).some((filterItem) => {
      if (filterItem.type === "dimension") {
        return filterItem.values.length === 0;
      } else if (filterItem.type === "measure") {
        return filterItem.min === filterItem.max;
      }
      return true;
    });

    if (isAnyFilterEmpty) {
      map.setFilter("vacant_properties", ["==", ["id"], ""]);
      return;
    }

    const mapFilter = Object.entries(filter).reduce(
      (acc, [property, filterItem]) => {
        if (filterItem.type === "dimension" && filterItem.values.length) {
          acc.push(["in", property, ...filterItem.values]);
        } else if (
          filterItem.type === "measure" &&
          filterItem.min !== filterItem.max
        ) {
          acc.push([">=", property, filterItem.min]);
          acc.push(["<=", property, filterItem.max]);
        }
        return acc;
      },
      [] as any[]
    );

    map.setFilter("vacant_properties", ["all", ...mapFilter]);
  };

  // handle map click
  const onMapClick = (event: any) => {
    console.log(event); 

    if (map) {
      const features = map.queryRenderedFeatures(event.point);
      console.log(features);

      if (features.length > 0) {
        setPopupInfo({ 
          longitude: event.lngLat.lng, 
          latitude: event.lngLat.lat, 
          feature: features[0].properties
        });
      }
    }
  };

  // handle zoom
  const onMapZoomEnd = () => {
    if (map) {
      setIsZoomModalHidden(map.getZoom() >= minZoom);
    }
  };

  useEffect(() => {
    if (map) {
      const legend = new LegendControl();
      map.addControl(legend, 'bottom-left');
    }
    updateFilter();
  }, [map, filter, updateFilter]);

  // map load
  return (
    <div className="relative h-full w-full">
    <Map
      mapboxAccessToken={mapboxAccessToken}
      mapLib={import('mapbox-gl')}
      initialViewState={{
        longitude: -75.1652,
        latitude: 39.9526,
        zoom: 13,
      }}
      mapStyle="mapbox://styles/mapbox/light-v10"
      onClick={onMapClick}
      onZoomEnd={onMapZoomEnd}
      interactiveLayerIds={["vacant_properties"]}
      onLoad={(e) => {
        setMap(e.target);
      }}
    >
      <MapControls />
      
      {popupInfo && (
        <Popup
          longitude={popupInfo.longitude}
          latitude={popupInfo.latitude}
          onClose={() => setPopupInfo(null)}
        >
          <div>
            <p>{popupInfo.feature.ADDRESS}</p>
          </div>
        </Popup>
        
      )}
      <MapSourceAndLayer onClick={onMapClick} />
    </Map>
    </div>
  );
}

/*
interface PropertyMapProps {
  setFeaturesInView: (features: any[]) => void;
}

const PropertyMap: FC<PropertyMapProps> = ({ setFeaturesInView }) => {
  const [isZoomModalHidden, setIsZoomModalHidden] = useState(true);
  const { filter } = useFilter();
  const [map, setMap] = useState<MapboxMap | null>(null);

  const updateFilter = () => {
    if (!map) return;

    const isAnyFilterEmpty = Object.values(filter).some((filterItem) => {
      if (filterItem.type === "dimension") {
        return filterItem.values.length === 0;
      } else if (filterItem.type === "measure") {
        return filterItem.min === filterItem.max;
      }
      return true;
    });

    if (isAnyFilterEmpty) {
      map.setFilter("vacant_properties", ["==", ["id"], ""]);
      return;
    }

    const mapFilter = Object.entries(filter).reduce(
      (acc, [property, filterItem]) => {
        if (filterItem.type === "dimension" && filterItem.values.length) {
          acc.push(["in", property, ...filterItem.values]);
        } else if (
          filterItem.type === "measure" &&
          filterItem.min !== filterItem.max
        ) {
          acc.push([">=", property, filterItem.min]);
          acc.push(["<=", property, filterItem.max]);
        }
        return acc;
      },
      [] as any[]
    );

    map.setFilter("vacant_properties", ["all", ...mapFilter]);
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
      const minZoom = 4;

      mapInstance.on("zoomend", () => {
        setIsZoomModalHidden(mapInstance.getZoom() >= minZoom);
      });

      mapInstance.addControl(new NavigationControl(), 'top-left');
      mapInstance.addControl(new FullscreenControl(), 'top-left');

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
          "fill-color": [
            "match",
            ["get", "guncrime_density"], // get the value of the guncrime_density property
            "Bottom 50%", "#B0E57C", // Light Green
            "Top 50%", "#FFD700", // Gold
            "Top 25%", "#FF8C00", // Dark Orange
            "Top 10%", "#FF4500", // Orange Red
            "Top 5%", "#B22222", // FireBrick
            "Top 1%", "#8B0000", // Dark Rednp
            "#0000FF" // default color if none of the categories match
          ],
          "fill-opacity": 0.7
        },
        metadata: {
          name: 'Guncrime Density',
        }
      });
      
      updateFilter();

      const legend = new LegendControl();
      mapInstance.addControl(legend, 'bottom-left');

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

*/