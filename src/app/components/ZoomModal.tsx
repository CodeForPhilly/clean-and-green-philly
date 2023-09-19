import React from "react";

type ZoomModalProps = {
  isHidden: boolean;
};

const ZoomModal: React.FC<ZoomModalProps> = ({ isHidden }) => {
  const visibilityClass = isHidden ? "hidden" : "block";
  return (
    <div
      className={`${visibilityClass} absolute top-2 left-2 p-2 bg-white text-black z-50`}
    >
      Zoom in to see properties.
    </div>
  );
};

export default ZoomModal;
