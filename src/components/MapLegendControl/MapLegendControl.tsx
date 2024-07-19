import { ControlPosition, FillLayerSpecification } from 'maplibre-gl';
import React, { Dispatch, SetStateAction } from 'react';
import { useControl } from 'react-map-gl';
import { MapLegendControlClass } from './MapLegend';

interface LegendOptions {
  position: ControlPosition;
  layerStyle: FillLayerSpecification;
  setSmallScreenToggle: Dispatch<SetStateAction<boolean>>;
}

export default function MapLegendControl(props: LegendOptions) {
  useControl(
    () =>
      new MapLegendControlClass(props.layerStyle, props.setSmallScreenToggle),
    {
      position: props.position,
    }
  );
  return null;
}
