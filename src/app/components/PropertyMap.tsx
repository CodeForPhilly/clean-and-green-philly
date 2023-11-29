import React, {
  useEffect,
  useState,
  useRef,
  Dispatch,
  SetStateAction,
} from "react";
import { BookmarkSquareIcon } from '@heroicons/react/24/outline'; // Make sure to import the correct icon
import { Map as MapboxMap, PopupOptions } from "mapbox-gl";
import { mapboxAccessToken, apiBaseUrl } from "../../config/config";
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
} from "react-map-gl";
import type { FillLayer, VectorSourceRaw } from "react-map-gl";

const minZoom = 4;

const VectorTiles: VectorSourceRaw = {
  id: "vacant_properties",
  type: "vector",
  tiles: [`${apiBaseUrl}/api/generateTiles/{z}/{x}/{y}`],
  minzoom: minZoom,
  maxzoom: 23,
};

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
  </>
);

interface PropertyMapProps {
  setFeaturesInView: Dispatch<SetStateAction<any[]>>;
  setSavedProperties: Dispatch<SetStateAction<any[]>>; // Add this line
}

const PropertyMap: React.FC<PropertyMapProps> = ({
  setFeaturesInView,
  setSavedProperties, // Add this line
}) => {
  const { filter } = useFilter();
  const [map, setMap] = useState<MapboxMap | null>(null);
  const [popupInfo, setPopupInfo] = useState<any | null>(null);
  const legendRef = useRef<LegendControl | null>(null);

  const handleSaveProperty = (feature: any) => {
    setSavedProperties(prevProperties => [...prevProperties, feature]);
  };

  // Inside your Map component
  const handlePropertyClick = (propertyData: any) => {
    // Assume propertyData is the data of the clicked property
    handlePropertyClick(propertyData); // onPropertyClick is the prop passed from SearchBarComponent
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
  
      if (features.length > 0) {
        setPopupInfo({
          longitude: event.lngLat.lng,
          latitude: event.lngLat.lat,
          feature: features[0], // Pass the entire feature object
          onSave: () => handleSaveProperty(features[0]) // Save the entire feature
        });
      } else {
        setPopupInfo(null);
      }
    } // This curly brace was missing
  };

  const setFeaturesInViewOnMove = (event: any) => {
    if (map) {
      const features = map.queryRenderedFeatures(event.point, {
        layers: ["vacant_properties"],
      });
      setFeaturesInView(features);
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

  // Filter update
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
        onMoveEnd={setFeaturesInViewOnMove}
      >
        <MapControls />

        {popupInfo && (
          <Popup
            longitude={popupInfo.longitude}
            latitude={popupInfo.latitude}
            closeOnClick={false}
          >
            <div>
            <p className="font-bold">{popupInfo.feature.ADDRESS}</p>
            <p>Owner: {popupInfo.feature.OWNER1}</p>
            <p>Gun Crime Density: {popupInfo.feature.guncrime_density}</p>
            <p>Tree Canopy Gap: {popupInfo.feature.tree_canopy_gap}</p>
            {/* Add the save button with an onClick handler */}
            <button onClick={popupInfo.onSave} className="flex items-center justify-center p-2 rounded-md hover:bg-gray-200">
              <BookmarkSquareIcon className="h-5 w-5" />
              Save
            </button>
          </div>
          </Popup>
        )}

        <Source id="vacant_properties" {...VectorTiles}>
          <Layer {...layerStyle} />
        </Source>
      </Map>
    </div>
  );
};

export default PropertyMap;
