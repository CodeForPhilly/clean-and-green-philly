import { ExpressionName, FillPaint } from "mapbox-gl";
import React, { ReactElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { ControlPosition, IControl, MapboxMap, useControl } from "react-map-gl";

import "../app/mapLegend.css";

interface LegendOptions {
  position: ControlPosition;
  source: string;
  paint: FillPaint;
  metadata: { [key: string]: string };
}

class MapLegendControlClass implements IControl {
  private _map: MapboxMap | undefined;
  private _container: HTMLElement;

  constructor(options: LegendOptions) {
    this._container = document.createElement("div");
    this._container.classList.add("mapboxgl-ctrl", "mapboxgl-ctrl-legend");
    // render legend as static markup so it can be rendered with map
    this._container.innerHTML = renderToStaticMarkup(
      <MapLegend {...options} />
    );
  }

  // able to add event listeners here for interactivity with layer
  onAdd = (map: MapboxMap) => {
    this._map = map;
    return this._container;
  };

  onRemove = () => {
    this._container.parentNode?.removeChild(this._container);
    this._map = undefined;
  };
}

/**
 *
 * @param {unknown} value - value in FillLayer paint field
 * @returns {ReactElement[] | undefined} - collection of React Elements made from object
 */
function parseBlocks(
  attribute: string,
  value: unknown
): ReactElement[] | undefined {
  switch (attribute) {
    // value for fill-color attribute can be single value or array
    case "fill-color": {
      if (value && Array.isArray(value) && value.length > 0) {
        const [name, ...args] = value;
        switch (name as ExpressionName) {
          case "match": {
            const [getter, ...paneLabels] = args;
            const elements: ReactElement[] = [];

            // labels and colors are in pairs in array with default being last value
            for (let i = 0; i < paneLabels.length; i += 2) {
              let label: string = paneLabels[i];
              let color: string = paneLabels[i + 1];

              // default color value
              if (label.includes("#")) {
                color = label;
                label = "Other";
              }

              elements.push(
                <li
                  key={`${label}-${color}-pane`}
                  style={{ "--color": color } as React.CSSProperties}
                >
                  {label}
                </li>
              );
            }

            return elements;
          }
          default:
            return;
        }
      }
    }
    default:
      return;
  }
}

/**
 *
 * @param {LegendOptions} props - data for legend
 * @returns - JSX of legend UI to be rendered in markup
 */
function MapLegend(props: LegendOptions) {
  const paneBlocks = Object.entries({ ...props.paint }).reduce(
    (acc, [attribute, value]) => {
      const blocks = parseBlocks(attribute, value);
      blocks?.forEach((block: ReactElement) => acc.push(block));
      return acc;
    },
    [] as ReactElement[]
  );

  return (
    <div className="panes" style={{ display: "block" }}>
      <details
        className={`mapboxgl-ctrl-legend-pane mapboxgl-ctrl-legend-pane--${props.source}`}
        open
      >
        <summary id="legend-summary">{props.metadata.name}</summary>
        <ul className="legend-list list list--color">{paneBlocks}</ul>
      </details>
    </div>
  );
}

export function MapLegendControl(props: LegendOptions) {
  useControl(() => new MapLegendControlClass(props), {
    position: props.position,
  });
  return null;
}
