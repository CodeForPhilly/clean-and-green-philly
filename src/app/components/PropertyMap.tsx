"use client";

import React, {
  FC,
  useEffect,
  useState,
  useRef,
  Dispatch,
  SetStateAction,
} from "react";
import { Polygon } from "geojson";
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
} from "react-map-gl";
import { FillLayer, CircleLayer } from "react-map-gl";
import maplibregl, {
  PointLike,
  Map as MaplibreMap,
  MapGeoJSONFeature,
} from "maplibre-gl";
import mapboxgl, { Expression } from "mapbox-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Protocol } from "pmtiles";

import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import "@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css";
import { Coordinates } from "../types";

const MIN_MAP_ZOOM = 10;
const MAX_MAP_ZOOM = 20;
const POINT_POLYGON_THRESHOLD = 14;
const MAX_TILE_ZOOM = 16;

const colorScheme: Expression = [
  "match",
  ["get", "priority_level"], // get the value of the guncrime_density property
  "High",
  "#FF4500", // Orange Red
  "Medium",
  "#FFD700", // Gold
  "Low",
  "#B0E57C", // Light Green
  "#D3D3D3", // default color if none of the categories match
];

const layerStylePolygon: FillLayer = {
  id: "vacant_properties_tiles_polygons",
  type: "fill",
  "source-layer": "vacant_properties_tiles_polygons",
  paint: {
    "fill-color": colorScheme,
    "fill-opacity": 0.7,
  },
  metadata: {
    name: "Priority",
  },
};

const layerStylePoints: CircleLayer = {
  id: "vacant_properties_tiles_points",
  type: "circle",
  "source-layer": "vacant_properties_tiles_points",
  paint: {
    "circle-color": colorScheme,
    "circle-opacity": 0.7,
    "circle-radius": 3,
  },
  metadata: {
    name: "Priority",
  },
};

const MapControls = () => (
  <>
    <GeolocateControl position="bottom-right" />
    <FullscreenControl position="bottom-right" />
    <NavigationControl showCompass={false} position="bottom-right" />
    <ScaleControl />
  </>
);

interface PropertyMapProps {
  setFeaturesInView: Dispatch<SetStateAction<any[]>>;
  setLoading: Dispatch<SetStateAction<boolean>>;
  selectedProperty: MapGeoJSONFeature | null;
  setSelectedProperty: (property: MapGeoJSONFeature | null) => void;
  setFeatureCount: Dispatch<SetStateAction<number>>;
  setCoordinates: Dispatch<SetStateAction<Coordinates>>;
}
const PropertyMap: FC<PropertyMapProps> = ({
  setFeaturesInView,
  setLoading,
  selectedProperty,
  setSelectedProperty,
  setFeatureCount,
  setCoordinates,
}) => {
  const { appFilter } = useFilter();
  const [popupInfo, setPopupInfo] = useState<any | null>(null);
  const [map, setMap] = useState<MaplibreMap | null>(null);
  const [zoom, setZoom] = useState<number>(13);
  const legendRef = useRef<LegendControl | null>(null);
  const geocoderRef = useRef<MapboxGeocoder | null>(null);

  useEffect(() => {
    let protocol = new Protocol();
    maplibregl.addProtocol("pmtiles", protocol.tile);
    return () => {
      maplibregl.removeProtocol("pmtiles");
    };
  }, []);

  // filter function
  const updateFilter = () => {
    if (!map) return;

    const isAnyFilterEmpty = Object.values(appFilter).some((filterItem) => {
      return filterItem.values.length === 0;
    });

    if (isAnyFilterEmpty) {
      map.setFilter("vacant_properties_tiles", ["==", ["id"], ""]);
      return;
    }

    const mapFilter = Object.entries(appFilter).reduce(
      (acc, [property, filterItem]) => {
        if (filterItem.values.length) {
          acc.push(["in", property, ...filterItem.values]);
        }

        return acc;
      },
      [] as any[]
    );

    map.setFilter("vacant_properties_tiles", ["all", ...mapFilter]);
  };

  const onMapClick = (event: any) => {
    if (map) {
      const features = map.queryRenderedFeatures(event.point, {
        layers: ["vacant_properties_tiles"],
      });

      if (features.length > 0) {
        setSelectedProperty(features[0]);
        setCoordinates({
          lng: event.lngLat.lng,
          lat: event.lngLat.lat,
        });
        setPopupInfo({
          longitude: event.lngLat.lng,
          latitude: event.lngLat.lat,
          feature: features[0].properties,
        });
      } else {
        setSelectedProperty(null);
        setPopupInfo(null);
      }
    }
  };

  const handleSetFeatures = (event: any) => {
    if (!["moveend", "sourcedata"].includes(event.type)) return;
    if (!map) return;
    setLoading(true);

    const zoom_ = map.getZoom();
    setZoom(zoom_);

    let bbox: [PointLike, PointLike] | undefined = undefined;

    const features = map.queryRenderedFeatures(bbox, {
      layers: [
        "vacant_properties_tiles_polygons",
        "vacant_properties_tiles_points",
      ],
    });

    console.log(features);

    setFeatureCount(features.length);

    const priorities: { [key: string]: number } = {
      High: 1,
      Medium: 2,
      Low: 3,
    };

    const sortedFeatures = features
      .sort((a, b) => {
        return (
          priorities[a?.properties?.priority_level || ""] -
          priorities[b?.properties?.priority_level || ""]
        );
      })
      .slice(0, 100);

    // only set the first 100 properties in state
    setFeaturesInView(sortedFeatures);
    setLoading(false);
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
            zoom: MAX_TILE_ZOOM,
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
  }, [map, appFilter]);

  const id = selectedProperty?.properties?.OPA_ID ?? null;
  useEffect(() => {
    /** Ticket #87 - focus on map when a property is selected */
    if (id && map != null) {
      const features = map.queryRenderedFeatures(undefined, {
        layers: [
          "vacant_properties_tiles_polygons",
          "vacant_properties_tiles_points",
        ],
      });
      const mapItem = features.find(
        (feature) => feature.properties?.OPA_ID === id
      );

      if (mapItem != null) {
        const coordinates = (mapItem.geometry as Polygon).coordinates[0];

        if (coordinates.length > 0) {
          // Filter out coordinates that are not available
          const validCoordinates = coordinates.filter(
            ([x, y]) => !isNaN(x) && !isNaN(y)
          );

          if (validCoordinates.length > 0) {
            const totalPoint = validCoordinates.reduce(
              (prevSum, position) => [
                prevSum[0] + position[0],
                prevSum[1] + position[1],
              ],
              [0, 0]
            );

            let finalPoint = [
              totalPoint[0] / validCoordinates.length,
              totalPoint[1] / validCoordinates.length,
            ];

            // Check if the finalPoint is valid
            if (isNaN(finalPoint[0]) || isNaN(finalPoint[1])) {
              // Fallback to first coordinate of the polygon if finalPoint is invalid
              finalPoint = validCoordinates[0];
            }

            const pointForMap = { lng: finalPoint[0], lat: finalPoint[1] };

            map.flyTo({
              center: pointForMap,
            });

            setCoordinates({
              lng: finalPoint[0].toString(),
              lat: finalPoint[1].toString(),
            });

            setPopupInfo({
              longitude: finalPoint[0],
              latitude: finalPoint[1],
              feature: selectedProperty?.properties,
            });
          }
        }
      }
    }
  }, [id]);

  useEffect(() => {
    if (id == null) {
      setPopupInfo(null);
    }
  }, [id]);

  const changeCursor = (e: any, cursorType: "pointer" | "default") => {
    e.target.getCanvas().style.cursor = cursorType;
  };

  // map load
  return (
    <div className="customized-map relative h-full w-full">
      <Map
        mapboxAccessToken={mapboxAccessToken}
        mapLib={maplibregl as any}
        initialViewState={{
          longitude: -75.15975924194129,
          latitude: 39.9910071520824,
          zoom,
        }}
        mapStyle="https://api.maptiler.com/maps/dataviz/style.json?key=dIagszPpXO3RgO1NNgzm"
        onMouseEnter={(e) => changeCursor(e, "pointer")}
        onMouseLeave={(e) => changeCursor(e, "default")}
        onClick={onMapClick}
        interactiveLayerIds={[
          "vacant_properties_tiles_polygons",
          "vacant_properties_tiles_points",
        ]}
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
            onClose={() => setPopupInfo(null)}
          >
            <div>
              <p className="font-semibold body-md p-1">
                {popupInfo.feature.address}
              </p>
            </div>
          </Popup>
        )}
        <Source
          type="vector"
          url="pmtiles://https://storage.googleapis.com/cleanandgreenphilly/vacant_properties_tiles.pmtiles"
          id="vacant_properties_tiles"
        >
          <Layer {...layerStylePoints} />
          <Layer {...layerStylePolygon} />
        </Source>
      </Map>
    </div>
  );
};
export default PropertyMap;
