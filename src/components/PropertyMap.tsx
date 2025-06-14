'use client';
import { useFilter } from '@/context/FilterContext';
import { createMapLibreGlMapController } from '@maptiler/geocoding-control/maplibregl-controller';
import { GeocodingControl } from '@maptiler/geocoding-control/react';
import '@maptiler/geocoding-control/style.css';
import { Tooltip } from '@nextui-org/react';
import { Info, X } from '@phosphor-icons/react';
import { centroid } from '@turf/centroid';
import { Position } from 'geojson';
import maplibregl, {
  CircleLayerSpecification,
  ColorSpecification,
  DataDrivenPropertyValueSpecification,
  FillLayerSpecification,
  IControl,
  LngLat,
  // IControl,
  LngLatLike,
  MapGeoJSONFeature,
  Map as MaplibreMap,
  MapMouseEvent,
  PointLike,
} from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { Protocol } from 'pmtiles';
import {
  // useRef,
  Dispatch,
  FC,
  ReactElement,
  SetStateAction,
  useEffect,
  useState,
} from 'react';
import { createPortal } from 'react-dom';
import Map, {
  GeolocateControl,
  Layer,
  NavigationControl,
  Popup,
  Source,
  ViewState,
} from 'react-map-gl/maplibre';
import '../components/components-css/PropertyMap.css';
import { ThemeButton } from '../components/ThemeButton';
import {
  googleCloudBucketName,
  maptilerApiKey,
  useStagingTiles,
} from '../config/config';
import { toTitleCase } from '../utilities/toTitleCase';
import { subZoning } from './Filters/filterOptions';
import { MapLegendControl } from './MapLegendControl';
import MapStyleSwitcher from './MapStyleSwitcher';

type MapStyle = {
  url: string;
};

type MapStyles = Record<string, MapStyle>;

type SearchedProperty = {
  coordinates: [number, number];
  address: string;
};

const MIN_MAP_ZOOM = 10;
const MAX_MAP_ZOOM = 20;

const layers = [
  'vacant_properties_tiles_polygons',
  'vacant_properties_tiles_points',
];
const colorScheme: DataDrivenPropertyValueSpecification<ColorSpecification> = [
  'match',
  ['get', 'priority_level'], // get the value of the guncrime_density property
  'High',
  '#FF4500', // Orange Red
  'Medium',
  '#FFD700', // Gold
  'Low',
  '#B0E57C', // Light Green
  '#D3D3D3', // default color if none of the categories match
];

const layerStylePolygon: FillLayerSpecification = {
  id: 'vacant_properties_tiles_polygons',
  type: 'fill',
  source: 'vacant_properties_tiles',
  'source-layer': 'vacant_properties_tiles_polygons',
  paint: {
    'fill-color': colorScheme,
    'fill-opacity': 0.7,
  },
  metadata: {
    name: 'Priority',
  },
};

const layerStylePoints: CircleLayerSpecification = {
  id: 'vacant_properties_tiles_points',
  type: 'circle',
  source: 'vacant_properties_tiles',
  'source-layer': 'vacant_properties_tiles_points',
  paint: {
    'circle-color': colorScheme,
    'circle-opacity': 0.7,
    'circle-radius': 3,
  },
  metadata: {
    name: 'Priority',
  },
};

const mapStyles: MapStyles = {
  DataVisualization: {
    url: `https://api.maptiler.com/maps/dataviz/style.json?key=${maptilerApiKey}`,
  },
  Hybrid: {
    url: `https://api.maptiler.com/maps/hybrid/style.json?key=${maptilerApiKey}`,
  },
  Street: {
    url: `https://api.maptiler.com/maps/streets/style.json?key=${maptilerApiKey}`,
  },
};

// info icon in legend summary
let summaryInfo: ReactElement | null = null;

const MapControls: React.FC<{
  handleStyleChange: (styleName: string) => void;
}> = ({ handleStyleChange }) => {
  const [smallScreenToggle, setSmallScreenToggle] = useState<boolean>(false);
  return (
    <>
      <NavigationControl showCompass={false} position="bottom-right" />
      <GeolocateControl position="bottom-right" />
      <MapStyleSwitcher handleStyleChange={handleStyleChange} />
      {smallScreenToggle || window.innerWidth > 640 ? (
        <MapLegendControl
          position="bottom-left"
          setSmallScreenToggle={setSmallScreenToggle}
          layerStyle={layerStylePolygon}
        />
      ) : (
        <div className="custom-legend-info-div maplibregl-ctrl maplibregl-ctrl-group w-[40px] h-[40px]">
          <ThemeButton
            className="custom-legend-info z-10"
            startContent={
              <span className="custom-legend-info-icon maplibregl-ctrl-icon"></span>
            }
            onPress={() => setSmallScreenToggle((s) => !s)}
          />
        </div>
      )}
    </>
  );
};

interface PropertyMapProps {
  featuresInView: MapGeoJSONFeature[];
  setFeaturesInView: Dispatch<SetStateAction<any[]>>;
  setLoading: Dispatch<SetStateAction<boolean>>;
  setHasLoadingError: Dispatch<SetStateAction<boolean>>;
  selectedProperty: MapGeoJSONFeature | null;
  setSelectedProperty: (property: MapGeoJSONFeature | null) => void;
  setFeatureCount: Dispatch<SetStateAction<number>>;
  initialViewState: ViewState;
  prevCoordinate: Position | null;
  setPrevCoordinate: () => void;
}
const PropertyMap: FC<PropertyMapProps> = ({
  featuresInView,
  setFeaturesInView,
  setLoading,
  setHasLoadingError,
  selectedProperty,
  setSelectedProperty,
  setFeatureCount,
  initialViewState,
  prevCoordinate,
  setPrevCoordinate,
}) => {
  const { appFilter } = useFilter();
  const [popupInfo, setPopupInfo] = useState<any | null>(null);
  const [map, setMap] = useState<MaplibreMap | null>(null);
  const [mapController, setMapController] = useState<IControl>();
  const [currentStyle, setCurrentStyle] = useState<string>(
    'Data Visualization View'
  );
  const [searchedProperty, setSearchedProperty] = useState<SearchedProperty>({
    coordinates: [-75.1628565788269, 39.97008211622267],
    address: '',
  });

  useEffect(() => {
    const protocol = new Protocol();
    maplibregl.addProtocol('pmtiles', protocol.tile);
    return () => {
      maplibregl.removeProtocol('pmtiles');
    };
  }, []);

  const onMapClick = (e: MapMouseEvent) => {
    handleMapClick(e.lngLat);
  };

  const handleStyleChange = (styleName: string) => {
    setCurrentStyle(styleName);
  };

  const moveMap = (targetPoint: LngLatLike) => {
    if (map) {
      map.easeTo({
        center: targetPoint,
      });
    }
  };

  const handleMapClick = (clickPoint: LngLat) => {
    if (map) {
      const features = map.queryRenderedFeatures(map.project(clickPoint), {
        layers,
      });

      setSearchedProperty({ ...searchedProperty, address: '' });
      if (features.length > 0) {
        setSelectedProperty(features[0]);
      } else {
        setSelectedProperty(null);
      }
    }
  };

  const handleSetFeatures = (event: any) => {
    if (!['moveend', 'sourcedata'].includes(event.type)) return;
    if (!map) return;
    setLoading(true);

    const bbox: [PointLike, PointLike] | undefined = undefined;

    const features = map.queryRenderedFeatures(bbox, { layers });

    //Get count of features if they are clustered
    const clusteredFeatureCount = features.reduce(
      (acc: number, feature: MapGeoJSONFeature) => {
        if (feature.properties?.clustered) {
          acc += feature.properties?.point_count || 0;
        } else {
          acc += 1;
        }
        return acc;
      },
      0
    );

    setFeatureCount(clusteredFeatureCount);

    const priorities: { [key: string]: number } = {
      High: 1,
      Medium: 2,
      Low: 3,
    };

    const sortedFeatures = features
      .sort((a: MapGeoJSONFeature, b: MapGeoJSONFeature) => {
        return (
          priorities[a?.properties?.priority_level || ''] -
          priorities[b?.properties?.priority_level || '']
        );
      })
      .slice(0, 100);

    // only set the first 100 properties in state
    setFeaturesInView(sortedFeatures);
    setLoading(false);
  };

  useEffect(() => {
    // This useEffect sets selectedProperty and map popup information after a property has been searched in the map's search form
    if (!featuresInView || selectedProperty || searchedProperty.address === '')
      return;

    if (map) {
      const features = map.queryRenderedFeatures(
        map.project(searchedProperty.coordinates),
        {
          layers,
        }
      );
      if (features.length > 0) {
        setSelectedProperty(features[0]);
        setSearchedProperty({ ...searchedProperty, address: '' });
      } else {
        setSelectedProperty(null);
        setPopupInfo({
          longitude: searchedProperty.coordinates[0],
          latitude: searchedProperty.coordinates[1],
          feature: { address: searchedProperty.address },
        });
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [featuresInView, selectedProperty]);

  useEffect(() => {
    if (map) {
      // Add info icon to legend on map load
      const legendSummary = document.getElementById('legend-summary');
      if (legendSummary) {
        const infoString: string =
          'We prioritize properties based on how much they can reduce gun violence considering the vacancy, gun violence, cleanliness, and tree canopy.';
        summaryInfo = createPortal(
          <Tooltip
            showArrow
            placement="top-start"
            color="primary"
            content={infoString}
            classNames={{
              base: ['before:-translate-x-2'],
              content: ['max-w-96 -translate-x-2'],
            }}
          >
            <Info
              alt="Priority Info"
              className="text-gray-500 cursor-pointer"
              tabIndex={0}
            />
          </Tooltip>,
          legendSummary
        );
      }

      setMapController(createMapLibreGlMapController(map, maplibregl) as any);
    }
  }, [map, setSelectedProperty]);

  useEffect(() => {
    if (!map) return;
    if (!selectedProperty) {
      setPopupInfo(null);
      if (window.innerWidth < 640 && prevCoordinate) {
        map.setCenter(prevCoordinate as LngLatLike);
        setPrevCoordinate();
      }
    } else {
      const propCentroid = centroid(selectedProperty.geometry);
      moveMap(propCentroid.geometry.coordinates as LngLatLike);
      setPopupInfo({
        longitude: propCentroid.geometry.coordinates[0],
        latitude: propCentroid.geometry.coordinates[1],
        feature: selectedProperty.properties,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedProperty]);

  useEffect(() => {
    // filter function
    // update filters on both layers for ease of switching between layers
    const updateFilter = () => {
      if (!map) return;

      const isAnyFilterEmpty = Object.values(appFilter).some((filterItem) => {
        return filterItem.values.length === 0;
      });

      if (isAnyFilterEmpty) {
        map.setFilter('vacant_properties_tiles_points', ['==', ['id'], '']);
        map.setFilter('vacant_properties_tiles_polygons', ['==', ['id'], '']);

        return;
      }

      const mapFilter = Object.entries(appFilter).reduce(
        (acc, [property, filterItem]) => {
          if (filterItem.values.length) {
            const thisFilterGroup: any = ['any'];
            filterItem.values.forEach((item) => {
              if (filterItem.useIndexOfFilter) {
                thisFilterGroup.push([
                  '>=',
                  ['index-of', item, ['get', property]],
                  0,
                ]);
              } else {
                thisFilterGroup.push(['in', ['get', property], item]);
              }
              if (Object.keys(subZoning).includes(item)) {
                subZoning[item].forEach((subZone: string) => {
                  if (filterItem) {
                    thisFilterGroup.push([
                      '>=',
                      ['index-of', subZone, ['get', property]],
                      0,
                    ]);
                  } else {
                    thisFilterGroup.push(['in', ['get', property], subZone]);
                  }
                });
              }
            });

            acc.push(thisFilterGroup);
          }
          return acc;
        },
        [] as any[]
      );

      map.setFilter('vacant_properties_tiles_points', ['all', ...mapFilter]);
      map.setFilter('vacant_properties_tiles_polygons', ['all', ...mapFilter]);
    };

    if (map) {
      updateFilter();
    }
  }, [map, appFilter, currentStyle]);

  const changeCursor = (
    e: any,
    cursorType: 'pointer' | 'grab' | 'grabbing'
  ) => {
    e.target.getCanvas().style.cursor = cursorType;
  };

  const handlePopupClose = () => {
    setSelectedProperty(null);
    setPopupInfo(null);
    history.replaceState(null, '', `/find-properties`);
  };

  // map load
  return (
    <div className="customized-map relative max-sm:min-h-[calc(100svh-100px)] max-sm:max-h-[calc(100svh-100px) h-full overflow-auto w-full">
      <Map
        mapLib={maplibregl as any}
        initialViewState={initialViewState}
        mapStyle={mapStyles[currentStyle]?.url}
        onMouseEnter={(e) => changeCursor(e, 'pointer')}
        onMouseLeave={(e) => changeCursor(e, 'grab')}
        onMouseDown={(e) => changeCursor(e, 'grabbing')}
        onMouseUp={(e) => changeCursor(e, 'grab')}
        onClick={onMapClick}
        minZoom={MIN_MAP_ZOOM}
        maxZoom={MAX_MAP_ZOOM}
        interactiveLayerIds={layers}
        onError={(e) => {
          setHasLoadingError(true);
        }}
        onLoad={(e) => {
          setMap(e.target);
          const attributionButton: HTMLElement | null = document.querySelector(
            '.maplibregl-ctrl-attrib-button'
          );
          if (attributionButton) {
            attributionButton.click();
          } else {
            console.warn('Attribution button not found.');
          }
        }}
        onSourceData={(e) => {
          handleSetFeatures(e);
        }}
        onStyleData={(e) => {
          const layerIds = e.target
            .getStyle()
            .layers.map((layer: any) => layer.id);
          const layersApplied = layers.every((layer) =>
            layerIds.includes(layer)
          );
          if (layersApplied) {
            setHasLoadingError(false);
          }
        }}
        onMoveEnd={handleSetFeatures}
      >
        <MapControls handleStyleChange={handleStyleChange} />
        <div
          className="geocoding"
          style={{
            position: 'absolute',
            top: '16px',
            right: '16px',
          }}
        >
          <GeocodingControl
            apiKey={maptilerApiKey}
            // COMMENT OUT LINE BELOW; OTHERWISE IT WILL CAUSE THE NEXTJS WEB APPLICATION TO CRASH
            // mapController={mapController}
            bbox={[-75.288283, 39.864114, -74.945063, 40.140129]} // Bounding box for Philadelphia
            markerOnSelected={false}
            filter={(feature: any) => {
              if (feature.place_type.includes('address')) {
                return feature.context.some((i: any) => {
                  return i.text.includes('Philadelphia');
                });
              }
            }}
            proximity={[
              {
                type: 'fixed',
                coordinates: [-75.1652, 39.9526], // Approximate center of Philadelphia
              },
            ]}
            onPick={({ feature }) => {
              if (feature) {
                const address = feature.place_name.split(',')[0];
                setSelectedProperty(null);
                setSearchedProperty({
                  coordinates: feature.center,
                  address: address,
                });
                map?.easeTo({
                  center: feature.center,
                  zoom: 16,
                });
              }
            }}
          />
        </div>
        {popupInfo && (
          <Popup
            className="customized-map-popup"
            longitude={popupInfo.longitude}
            latitude={popupInfo.latitude}
            closeOnClick={false}
            onClose={handlePopupClose}
          >
            <div className="flex flex-row items-center nowrap space-x-1">
              <span>{toTitleCase(popupInfo.feature.address)}</span>
              {/* keeping invisible to maintain spacing for built-in close button */}
              <X size={16} className="invisible" />
            </div>
          </Popup>
        )}
        <Source
          type="vector"
          url={`pmtiles://https://storage.googleapis.com/${googleCloudBucketName}/vacant_properties_tiles${
            useStagingTiles ? '_staging' : ''
          }.pmtiles`}
          id="vacant_properties_tiles"
        >
          <Layer {...layerStylePoints} />
          <Layer {...layerStylePolygon} />
        </Source>
      </Map>
      {summaryInfo}
    </div>
  );
};
export default PropertyMap;
