import React, {
  useEffect,
  useState,
  useRef,
  Dispatch,
  SetStateAction,
} from "react";
import { Map as MapboxMap } from "mapbox-gl";
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
const getFeaturesZoom = 14;

const VectorTiles: VectorSourceRaw = {
  id: "vacant_properties",
  type: "vector",
  tiles: [`${apiBaseUrl}/api/getTiles/{z}/{x}/{y}`],
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
  setZoom: Dispatch<SetStateAction<number>>;
  setLoading: Dispatch<SetStateAction<boolean>>;
}
const PropertyMap: React.FC<PropertyMapProps> = ({
  setFeaturesInView,
  setZoom,
  setLoading,
}: any) => {
  const { filter } = useFilter();
  const [popupInfo, setPopupInfo] = useState<any | null>(null);
  const [map, setMap] = useState<MapboxMap | null>(null);
  const legendRef = useRef<LegendControl | null>(null);

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
          feature: features[0].properties,
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
              <p className="font-bold">{popupInfo.feature.ADDRESS}</p>
              <p>Owner: {popupInfo.feature.OWNER1}</p>
              <p>Gun Crime Density: {popupInfo.feature.guncrime_density}</p>
              <p>Tree Canopy Gap: {popupInfo.feature.tree_canopy_gap}</p>
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
