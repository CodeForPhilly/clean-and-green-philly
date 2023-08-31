"use client";

import React, { FC } from "react";
import MapboxGL from "react-mapbox-gl";
import { Popup, Map as MapboxMap } from "mapbox-gl";
import { mapboxAccessToken } from "../config/mapbox"; // Assuming this is the correct relative path
import PropertyMap from "./components/PropertyMap";

const Map = MapboxGL({
  accessToken: mapboxAccessToken,
});

let popup: Popup | null = null; // To hold the popup instance

const Page: FC = () => {
  return (
    <div style={{ height: "100vh" }}>
      <PropertyMap />
    </div>
  );
};

export default Page;
