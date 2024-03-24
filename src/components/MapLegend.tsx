import { ExpressionName } from "mapbox-gl";
import React, { ReactElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { FillLayer, IControl, MapboxMap, useControl } from "react-map-gl";

export class MapLegendControlClass implements IControl {
  private _map: MapboxMap | undefined;
  private _container: HTMLElement;

  constructor(options: FillLayer) {
    this._container = document.createElement("div");
    this._container.classList.add("mapboxgl-ctrl", "mapboxgl-ctrl-legend");
    this._container.innerHTML = renderToStaticMarkup(
      <MapLegend {...options} />
    );
  }

  // able to add event listeners here for interactivity
  onAdd = (map: MapboxMap) => {
    this._map = map;
    return this._container;
  };

  onRemove = () => {
    this._container.parentNode?.removeChild(this._container);
    this._map = undefined;
  };
}

export function MapLegendControl(props: FillLayer) {
  useControl(() => new MapLegendControlClass(props), {
    position: "bottom-left",
  });
  return null;
}

function parseBlocks(value: unknown) {
  if (value && Array.isArray(value) && value.length > 0) {
    const [name, ...args] = value;
    switch (name as ExpressionName) {
      case "match": {
        const [getter, ...paneLabels] = args;

        const legendItems = paneLabels.reduce(
          (accumulator, currentValue, currentIndex, array) => {
            if (currentIndex % 2 === 0) {
              accumulator.push(array.slice(currentIndex, currentIndex + 2));
            }
            return accumulator;
          },
          []
        );

        return legendItems.map(
          (label: string[]): ReactElement<any> => (
            <li style={{ "--color": label[1] } as React.CSSProperties}>
              {label[0]}
            </li>
          )
        );
      }
    }
  }
}

export function MapLegend(props: FillLayer) {
  const paneBlocks = Object.entries({ ...props.paint }).reduce(
    (acc, [attribute, value]) => {
      const blocks = parseBlocks(value);
      blocks?.forEach((block: ReactElement) => acc.push(block));
      return acc;
    },
    [] as ReactElement[]
  );

  return (
    <div className="panes" style={{ display: "block" }}>
      <details
        className={`mapboxgl-ctrl-legend-pane mapboxgl-ctrl-legend-pane--${props["source-layer"]}`}
        open
      >
        <summary id="legend-summary">Priority</summary>

        <ul className="legend-list list list--color">{paneBlocks}</ul>
      </details>
    </div>
  );
}
