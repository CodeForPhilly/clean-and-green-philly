import { ExpressionName } from "mapbox-gl";
import React, { ReactElement, Dispatch, SetStateAction } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { FillLayerSpecification } from "maplibre-gl";
import { IControl, MapboxMap } from "react-map-gl";


import "../../app/mapLegend.css";

interface LayerStyleMetadata {
  name: string;
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
 * @param {FillLayerSpecification} layerStyle - data for legend
 * @returns - JSX of legend UI to be rendered in markup
 */
function MapLegend(layerStyle: FillLayerSpecification) {
  // generate label panes for legend
  const paneBlocks = Object.entries({ ...layerStyle.paint }).reduce(
    (acc, [attribute, value]) => {
      const blocks = parseBlocks(attribute, value);
      blocks?.forEach((block: ReactElement) => acc.push(block));
      return acc;
    },
    [] as ReactElement[]
  );

  return (
    <>
      <div className="panes" style={{ display: "block" }}  onClick={() => console.log('hit') }>
        <details
          className={`mapboxgl-ctrl-legend-pane mapboxgl-ctrl-legend-pane--${layerStyle.source}`}
          open
        >
          <summary id="legend-summary">
            {(layerStyle.metadata as LayerStyleMetadata).name}
          </summary>
          <ul className="legend-list list list--color">{paneBlocks}</ul>
        </details>
      </div>
    </>
  );
}

export class MapLegendControlClass implements IControl {
  private _map: MapboxMap | undefined;
  private _container: HTMLElement;
  private handler: () => void;

  constructor(layerStyle: FillLayerSpecification, setSmallScreenToggle: Dispatch<SetStateAction<boolean>>) {
    this._container = document.createElement("div");
    this._container.classList.add("mapboxgl-ctrl", "mapboxgl-ctrl-legend");
    // render legend as static markup so it can be rendered with map
    this.handler = () => setSmallScreenToggle(s => !s);
    this._container.innerHTML = renderToStaticMarkup(
      <MapLegend {...layerStyle} />
    );
  }

  // able to add event listeners here for interactivity with layer
  onAdd = (map: MapboxMap) => {
    this._map = map;
    this._container.addEventListener("click", this.handler);
    return this._container;
  };

  onRemove = () => {
     this._container.removeEventListener("click", this.handler);
    this._container.parentNode?.removeChild(this._container);
    this._map = undefined;
  };
}
