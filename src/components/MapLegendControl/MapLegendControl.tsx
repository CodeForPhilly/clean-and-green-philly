import { ControlPosition, FillLayerSpecification } from "maplibre-gl";
import React from "react";
import { useControl } from "react-map-gl";
import { MapLegendControlClass } from "./MapLegend";

interface LegendOptions {
  position: ControlPosition;
  layerStyle: FillLayerSpecification;
}

export default function MapLegendControl(props: LegendOptions) {
  useControl(() => new MapLegendControlClass(props.layerStyle), {
    position: props.position,
  });
  return null;
}
