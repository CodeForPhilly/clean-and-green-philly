import React from "react";

interface StreetViewProps {
  lat: string;
  lng: string;
  yaw: string;
  pitch: string;
  fov: string;
}

/**
 * Takes a lng/lat and generates an embed-able google street view url.
 *
 * Warning: This is manually crafted and not linked to any API,
 *          so if Google decided to change how they craft their
 *          Embedding URL structure, this would break.
 *
 * @param lat - The latitude of the location.
 * @param lng - The longitude of the location.
 * @param yaw - The yaw angle of the street view.
 * @param pitch - The pitch angle of the street view.
 * @param fov - The field of view of the street view.
 * @returns The rendered street view component.
 */
const StreetView: React.FC<StreetViewProps> = ({
  lat,
  lng,
  yaw,
  pitch,
  fov,
}) => {
  const generateStreetViewURL = (
    lat: string,
    lng: string,
    yaw: string,
    pitch: string,
    fov: string
  ) => {
    const base_url =
      "https://www.google.com/maps/embed?pb=!4v[TIMESTAMP]!6m8!1m7![PANO_ID]";
    const orientation = `!2m2!1d${lat}!2d${lng}!3f${yaw}!4f${pitch}!5f${fov}`;
    return base_url + orientation;
  };

  const streetViewURL = generateStreetViewURL(lat, lng, yaw, pitch, fov);

  return (
    <iframe
      src={streetViewURL}
      width="100%"
      height="100%"
      style={{ border: 0 }}
      allowFullScreen={false}
      loading="lazy"
    ></iframe>
  );
};

export default StreetView;
