"use client";

import React, {
  useEffect,
  useState,
  useRef
} from "react";
import mapboxgl, { Map as MapboxMap } from "mapbox-gl";
import { mapboxAccessToken } from "../../config/config";
import { useFilter } from "@/context/FilterContext";
import LegendControl from "mapboxgl-legend";
import "mapboxgl-legend/dist/style.css";
import "../globals.css";
import Map, {
  Source,
  Layer,
  Popup,
  NavigationControl,
  FullscreenControl,
  ScaleControl,
  GeolocateControl,
  AttributionControl,
} from "react-map-gl";
import type { FillLayer, VectorSourceRaw } from "react-map-gl";
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import "@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css";
import { BookmarkSquareIcon } from "@heroicons/react/24/outline";

const minZoom = 4;
const getFeaturesZoom = 14;

const layerStyle: FillLayer = {
  id: "vacant_properties",
  type: "fill",
  source: "vacant_properties",
  "source-layer": "vacant_properties",
  paint: {
    "fill-color": [
      "match",
      ["get", "guncrime_density"], // get the value of the guncrime_density property
      "Bottom 50%",
      "#B0E57C", // Light Green
      "Top 50%",
      "#FFD700", // Gold
      "Top 25%",
      "#FF8C00", // Dark Orange
      "Top 10%",
      "#FF4500", // Orange Red
      "Top 5%",
      "#B22222", // FireBrick
      "Top 1%",
      "#8B0000", // Dark Rednp
      "#0000FF", // default color if none of the categories match
    ],
    "fill-opacity": 0.7,
  },
  metadata: {
    name: "Guncrime Density",
  },
};

const MapControls = () => (
  <>
    <GeolocateControl position="top-left" />
    <FullscreenControl position="top-left" />
    <NavigationControl position="top-left" />
    <ScaleControl />
    <AttributionControl />
  </>
);

interface PropertyMapProps {
  setFeaturesInView: (features: any[]) => void;
  setZoom: (zoom: number) => void;
  setLoading: (loading: boolean) => void;
  handleSaveProperty: (property: any) => void;
}

const PropertyMap: React.FC<PropertyMapProps> = ({
  setFeaturesInView,
  setZoom,
  setLoading,
  handleSaveProperty,
}) => {
  const { filter } = useFilter();
  const [popupInfo, setPopupInfo] = useState<any | null>(null);
  const [map, setMap] = useState<MapboxMap | null>(null);
  const [propertyVectorTiles, setPropertyVectorTiles] =
    useState<VectorSourceRaw | null>(null);
  const legendRef = useRef<LegendControl | null>(null);
  const geocoderRef = useRef<MapboxGeocoder | null>(null);
  const [isCurrentPropertySaved, setIsCurrentPropertySaved] = useState(false);


  useEffect(() => {
    const vectorTiles: VectorSourceRaw = {
      id: "vacant_properties",
      type: "vector",
      tiles: [`${window.location.origin}/api/getTiles/{z}/{x}/{y}`],
      minzoom: 10,
      maxzoom: 16,
    };

    setPropertyVectorTiles(vectorTiles);
  }, []);

  const isPropertySaved = (feature) => {
    if (!feature || !feature.OPA_ID) {
      console.error("Invalid feature data", feature);
      return false;
    }
  
    const savedProperties = JSON.parse(localStorage.getItem('savedProperties') || '[]');
    return savedProperties.some(savedProperty => 
      savedProperty.OPA_ID === feature.OPA_ID);
  };
  
  const onSave = (property) => {
    if (!property || !property.OPA_ID) {
      console.error("Property or property.OPA_ID is undefined", property);
      return;
    }
  
    handleSaveProperty(property); // Call the method that handles saving a property
    setIsCurrentPropertySaved(!isCurrentPropertySaved);
  };  
  
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

  const onMapClick = (event: any) => {
    if (map) {
      const features = map.queryRenderedFeatures(event.point, {
        layers: ["vacant_properties"],
      });
  
      console.log("Queried Features:", features);
      if (features.length > 0 && features[0].properties.OPA_ID) {
        console.log("First Feature Properties:", features[0].properties);
        const property = features[0];
        setIsCurrentPropertySaved(isPropertySaved(property.properties)); // Pass the properties object
        setPopupInfo({
          longitude: event.lngLat.lng,
          latitude: event.lngLat.lat,
          feature: property,
        });
      } else {
        setPopupInfo(null);
      }
    }
  };
  

  const handleSetFeatures = (event: any) => {
    if (event.type !== "moveend") return;
    if (!map) return;
    setLoading(true);

    const zoom = map.getZoom();
    setZoom(zoom);

    if (map.getZoom() >= getFeaturesZoom) {
      // use `undefined` to get all features
      const features = map.queryRenderedFeatures(undefined, {
        layers: ["vacant_properties"],
      });

      // Remove duplicate features (which can occur because of the way the tiles are generated)
      const uniqueFeatures = features.reduce((acc: any[], feature: any) => {
        if (
          !acc.find((f) => f.properties.OPA_ID === feature.properties.OPA_ID)
        ) {
          acc.push(feature);
        }
        return acc;
      }, []);

      setFeaturesInView(uniqueFeatures);
      setLoading(false);
    } else {
      setFeaturesInView([]);
      setLoading(false);
    }
  };

  useEffect(() => {
    if (map) {
      if (!legendRef.current) {
        legendRef.current = new LegendControl();
        map.addControl(legendRef.current, "bottom-left");
      }
    }

    return () => {
      if (map && legendRef.current) {
        map.removeControl(legendRef.current);
        legendRef.current = null;
      }
    };
  }, [map]);

  useEffect(() => {
    if (map) {
      // Add Legend Control
      if (!legendRef.current) {
        legendRef.current = new LegendControl();
        map.addControl(legendRef.current, "bottom-left");
      }

      // Add Geocoder
      if (!geocoderRef.current) {
        const center = map.getCenter();
        geocoderRef.current = new MapboxGeocoder({
          accessToken: mapboxAccessToken,
          mapboxgl: mapboxgl,
          marker: false,
          proximity: {
            longitude: center.lng,
            latitude: center.lat,
          },
        });

        map.addControl(geocoderRef.current, "top-right");

        geocoderRef.current.on("result", (e) => {
          map.flyTo({
            center: e.result.center,
            zoom: 16,
          });
        });
      }
    }

    return () => {
      // Remove Legend Control
      if (map && legendRef.current) {
        map.removeControl(legendRef.current);
        legendRef.current = null;
      }

      // Remove Geocoder
      if (map && geocoderRef.current) {
        map.removeControl(geocoderRef.current);
        geocoderRef.current = null;
      }
    };
  }, [map]);

  useEffect(() => {
    if (map) {
      updateFilter();
    }
  }, [map, filter, updateFilter]);

  const changeCursor = (e: any, cursorType: "pointer" | "default") => {
    e.target.getCanvas().style.cursor = cursorType;
  };

  // map load
  return (
    <div className="relative h-full w-full">
      <Map
        mapboxAccessToken={mapboxAccessToken}
        initialViewState={{
          longitude: -75.1652,
          latitude: 39.9526,
          zoom: 13,
        }}
        mapStyle="mapbox://styles/mapbox/light-v10"
        onMouseEnter={(e) => changeCursor(e, "pointer")}
        onMouseLeave={(e) => changeCursor(e, "default")}
        onClick={onMapClick}
        interactiveLayerIds={["vacant_properties"]}
        onLoad={(e) => {
          setMap(e.target);
        }}
        onSourceData={(e) => {
          handleSetFeatures(e);
        }}
        onMoveEnd={handleSetFeatures}
      >
        <MapControls />
        {popupInfo && (
          <Popup
            longitude={popupInfo.longitude}
            latitude={popupInfo.latitude}
            closeOnClick={false}
          >
            <div>
              <p className="font-bold">{popupInfo.feature.properties.ADDRESS}</p>
              <p>Owner: {popupInfo.feature.properties.OWNER1}</p>
              <p>Gun Crime Density: {popupInfo.feature.properties.guncrime_density}</p>
              <p>Tree Canopy Gap: {popupInfo.feature.properties.tree_canopy_gap}</p>
              <button
                onClick={() => onSave(popupInfo.feature.properties)}
                className={`flex items-center justify-center p-2 mx-auto my-3 rounded-md hover:bg-gray-200 ${isCurrentPropertySaved ? 'bg-green-500' : ''}`}
              >
                <BookmarkSquareIcon className="h-5 w-5" />
                {isCurrentPropertySaved ? 'Saved!' : 'Save'}
              </button>
            </div>
          </Popup>
        )}
        {propertyVectorTiles && (
          <Source id="vacant_properties" {...propertyVectorTiles}>
            <Layer {...layerStyle} />
          </Source>
        )}
      </Map>
    </div>
  );
};
export default PropertyMap;
