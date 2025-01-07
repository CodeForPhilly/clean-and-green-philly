'use client';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';

interface MapStyleSwitcherProps {
  handleStyleChange: (style: string) => void;
}

const MapStyleSwitcher: React.FC<MapStyleSwitcherProps> = ({
  handleStyleChange,
}) => {
  const [activeStyle, setActiveStyle] = useState('DATAVIZ');
  const [isHovered, setIsHovered] = useState(false);

  type BaseMap = {
    name: string;
    img: string;
  };

  type BaseMaps = Record<string, BaseMap>;

  const baseMaps: BaseMaps = {
    STREETS: {
      name: 'Street',
      img: 'https://cloud.maptiler.com/static/img/maps/streets.png',
    },
    DATAVIZ: {
      name: 'DataVisualization',
      img: 'https://cloud.maptiler.com/static/img/maps/dataviz.png',
    },
    HYBRID: {
      name: 'Hybrid',
      img: 'https://cloud.maptiler.com/static/img/maps/hybrid.png',
    },
  };

  const onClick = (key: string) => {
    setActiveStyle(key);
    handleStyleChange(baseMaps[key].name);
  };

  return (
    <div
      className="relative maplibregl-ctrl maplibregl-ctrl-basemaps p-2"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Image
        src={baseMaps[activeStyle].img}
        alt={activeStyle}
        width={65}
        height={65}
        title={activeStyle.toLowerCase()}
        className="cursor-pointer w-16 h-16 rounded-md border-2 border-gray-400 z-10"
      />

      <div
        className={`absolute flex flex-row items-center pl-2 transition-transform duration-300 ${
          isHovered
            ? 'translate-x-20 opacity-100'
            : 'translate-x-0 opacity-0 pointer-events-none'
        }`}
        style={{
          left: '4rem',
          top: '50%',
          transform: 'translateY(-50%)',
        }}
      >
        {Object.keys(baseMaps)
          .filter((key) => key !== activeStyle)
          .map((key) => (
            <Image
              key={key}
              src={baseMaps[key].img}
              alt={key}
              width={65}
              height={65}
              title={key.toLowerCase()}
              onClick={() => onClick(key)}
              className={`cursor-pointer rounded-md border-2 border-transparent hover:border-gray-400`}
            />
          ))}
      </div>
    </div>
  );
};

export default MapStyleSwitcher;
