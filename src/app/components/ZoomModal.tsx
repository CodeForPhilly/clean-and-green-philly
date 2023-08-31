import React from "react";

type ZoomModalProps = {
  isHidden: boolean;
};

const ZoomModal: React.FC<ZoomModalProps> = ({ isHidden }) => {
  const visibilityClass = isHidden ? "invisible" : "visible";

  return (
    <div
      className={`${visibilityClass} absolute bottom-2 left-2 p-2 bg-white text-black`}
    >
      Zoom in to see properties.
    </div>
  );
};

export default ZoomModal;
