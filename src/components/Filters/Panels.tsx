'use client';

import React, { FC } from 'react';
import { Card, CardBody } from '@nextui-org/react';
import { Check } from '@phosphor-icons/react';
import {
  access_options,
  ALL_PROPERTY_ACCESS,
  PropertyAccess,
  PropertyAccessOption,
} from '@/config/propertyAccessOptions';
import { useFilter } from '@/context/FilterContext';

type PanelFilterOptions = PropertyAccessOption & {
  alt_description: string;
  dimension: string;
  property: string;
};

type PanelsProps = {
  options: string[] | PropertyAccess[];
  selectedPanelKeys: { [property: string]: string[] };
  aria_describedby_label?: string;
  toggleDimensionForPanel: (dimension: string, property: string) => void;
};

const types = [p in keyof PropertyAccessOption];

const panelAccessOptions = access_options.map((option) => Object.fromEntries(ALL_PROPERTY_ACCESS.map(access => [access, option[access]])));

const Panels = ({
  options,
  selectedPanelKeys,
  toggleDimensionForPanel,
  aria_describedby_label,
}: PanelsProps) => {
  const { dispatch, appFilter } = useFilter();

  const optionPanels = options.map((option, index) => {
    const panel = panel_access_options[option];
    const Icon = panel.icon;
    const isSelected =
      selectedPanelKeys[panel.property] &&
      selectedPanelKeys[panel.property].includes(panel.dimension)
        ? true
        : false;

    return (
      <Card
        key={index}
        role="checkbox"
        aria-describedby={aria_describedby_label}
        aria-checked={isSelected}
        className={isSelected ? 'panelSelected ' : 'panelDefault'}
        isPressable
        onPress={() => toggleDimensionForPanel(panel.dimension, panel.property)}
        shadow="none"
      >
        <CardBody className="flex flex-row justify-between p-[0px]">
          <div className="flex flex-row">
            <div className="mr-3">
              <Icon aria-hidden={true} className="size-8" />
            </div>
            <div className="flex flex-row items-center sm:items-start sm:flex-col lg:flex-row lg:items-center">
              <div className="flex flex-col flex-0">
                <div className="heading-md">{panel.header}</div>
                <div className="body-sm">{panel.alt_description}</div>
              </div>
            </div>
          </div>
          <div>
            {isSelected ? <Check className="self-end size-5" /> : undefined}
          </div>
        </CardBody>
      </Card>
    );
  });

  return <div className="flex flex-col space-y-2">{optionPanels}</div>;
};

export default Panels;
