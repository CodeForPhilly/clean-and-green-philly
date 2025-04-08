'use client';

import React from 'react';
import { accessOptions } from '@/config/propertyAccessOptions';
import Panel, { PanelProps } from './Panel';

const { DO_NOTHING, ...activeOptions } = accessOptions;

const panelAccessOptions = Object.entries(activeOptions).map(([_, option]) => {
  const { property, dimension, header, secondary_description, icon } = option;

  return {
    property,
    dimension,
    header,
    secondary_description,
    icon,
  } as PanelProps;
});

const Panels = () => {
  const optionPanels = panelAccessOptions.map((option, index) => {
    const { property, dimension, header, secondary_description, icon } = option;

    return (
      <Panel
        property={property}
        dimension={dimension}
        header={header}
        secondary_description={secondary_description}
        icon={icon}
      />
    );
  });

  return <div className="flex flex-col space-y-2">{optionPanels}</div>;
};

export default Panels;
