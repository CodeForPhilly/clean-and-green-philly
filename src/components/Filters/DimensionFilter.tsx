'use client';

import React, { useMemo, useState, FC } from 'react';
import { useFilter } from '@/context/FilterContext';
import ButtonGroup from './ButtonGroup';
import MultiSelect from './MultiSelect';
import Panels from './Panels';
import RangedInputs from './RangedInputs';

type DimensionFilterProps = {
  property: string;
  display: string;
  options: string[];
  type: string;
  useIndexOfFilter?: boolean;
};

type OptionDisplayMapping = {
  [key: string]: { [key: string]: string };
};

const optionsDisplayMapping: OptionDisplayMapping = {
  llc_owner: {
    Yes: 'Business',
    No: 'Individual',
  },
};

const DimensionFilter: FC<DimensionFilterProps> = ({
  property,
  display,
  options,
  type,
  useIndexOfFilter,
}) => {
  const { dispatch, appFilter } = useFilter();
  const [selectedKeys, setSelectedKeys] = useState<string[]>(
    appFilter[property]?.values || []
  );
  const [selectedRanges, setSelectedRanges] = useState<{
    min: string | React.ChangeEvent<HTMLSelectElement>;
    max: string | React.ChangeEvent<HTMLSelectElement>;
  }>({
    min: appFilter[property]?.rangedValues?.min as string,
    max: appFilter[property]?.rangedValues?.max as string,
  });
  const initialSelectedPanelKeys = () => {
    const panelKeyObj: { [key: string]: string[] } = {};
    for (const key in appFilter) {
      panelKeyObj[key] = appFilter[key].values || [];
    }
    return panelKeyObj;
  };
  const [selectedPanelKeys, setSelectedPanelkeys] = useState<{
    [property: string]: string[];
  }>(initialSelectedPanelKeys());

  const filterLabelID = display.replace(/\s/g, '');

  const toggleDimensionForPanel = (
    dimension: string,
    panel_property: string
  ) => {
    let newSelectedPanelKeys;
    if (selectedPanelKeys[panel_property]) {
      newSelectedPanelKeys = selectedPanelKeys[panel_property].includes(
        dimension
      )
        ? selectedPanelKeys[panel_property].filter((key) => key !== dimension)
        : [...selectedPanelKeys[panel_property], dimension];
    } else {
      newSelectedPanelKeys = [dimension];
    }
    setSelectedPanelkeys({
      ...selectedPanelKeys,
      [panel_property]: newSelectedPanelKeys,
    });
    dispatch({
      type: 'SET_DIMENSIONS',
      property: panel_property,
      dimensions: newSelectedPanelKeys,
    });
  };

  const toggleDimension = (dimension: string) => {
    const newSelectedKeys = selectedKeys.includes(dimension)
      ? selectedKeys.filter((key) => key !== dimension)
      : [...selectedKeys, dimension];
    setSelectedKeys(newSelectedKeys);
    dispatch({
      type: 'SET_DIMENSIONS',
      property,
      dimensions: newSelectedKeys,
    });
  };

  const handleSelectionChange = (
    selection: React.ChangeEvent<HTMLSelectElement> | string,
    limitType?: string
  ) => {
    let newMultiSelect: string[] = [];
    const newRangeValues = { ...selectedRanges };

    if (limitType) {
      if (limitType === 'min') {
        newRangeValues.min = selection;
      } else if (limitType === 'max') {
        newRangeValues.max = selection;
      }
    }

    if (typeof selection === 'string') {
      newMultiSelect = selectedKeys.includes(selection)
        ? selectedKeys.filter((key) => key !== selection)
        : [...selectedKeys, selection];
    } else {
      if (selection.target.value !== '') {
        newMultiSelect = selection.target.value.split(',');
      }
    }
    if (limitType) {
      dispatch({
        type: 'SET_DIMENSIONS',
        property,
        limitType,
        dimensions: newRangeValues,
        useIndexOfFilter,
      });
    } else {
      setSelectedKeys(newMultiSelect);
      dispatch({
        type: 'SET_DIMENSIONS',
        property,
        dimensions: newMultiSelect,
        useIndexOfFilter,
      });
    }
  };

  const filter = useMemo(() => {
    if (type === 'buttonGroup') {
      return (
        <ButtonGroup
          options={options}
          selectedKeys={selectedKeys}
          toggleDimension={toggleDimension}
          displayOptions={optionsDisplayMapping[property]}
          aria_describedby_label={filterLabelID}
        />
      );
    } else if (type === 'panels') {
      return (
        /* the filterLabelID is pulled from the form field header text and uses aria-describedby to tie each component to the form header label using a unique ID applied to the form area header
         */
        <Panels
          options={options}
          selectedPanelKeys={selectedPanelKeys}
          toggleDimensionForPanel={toggleDimensionForPanel}
          aria_describedby_label={filterLabelID}
        />
      );
    } else if (type === 'range') {
      return (
        <RangedInputs
          display={display}
          options={options}
          selectedRanges={appFilter[property]?.rangedValues}
          setSelectedRanges={setSelectedRanges}
          handleSelectionChange={handleSelectionChange}
          aria_describedby_label={filterLabelID}
        />
      );
    } else {
      return (
        <MultiSelect
          display={display}
          options={options}
          selectedKeys={selectedKeys}
          toggleDimension={toggleDimension}
          handleSelectionChange={handleSelectionChange as any}
          aria_describedby_label={filterLabelID}
        />
      );
    }
  }, [selectedKeys, selectedPanelKeys]);

  const filterDescription =
    property === 'priority_level'
      ? {
          desc: 'Find properties based on how much they can reduce gun violence considering the gun violence, cleanliness, and tree canopy nearby. ',
          linkFragment: 'priority-method',
        }
      : property === 'market_value'
        ? {
            desc: 'Find properties based on their market value (USD). ',
            linkFragment: 'access-method',
          }
        : {
            desc: 'Find properties based on what we think is the easiest method to get legal access to them, based on the data available to us. ',
            linkFragment: 'access-method',
          };

  // text-gray-500, 600 ? or #586266 (figma)?
  return (
    <div className="pt-3 pb-6">
      <div className="flex flex-col mb-2">
        <h2 className="heading-lg" id={filterLabelID}>
          {display}
        </h2>
        {(property === 'get_access' ||
          property === 'priority_level' ||
          property === 'market_value') && (
          <p className="body-sm text-gray-500 w-[90%] my-1">
            {filterDescription.desc}
            {(property === 'get_access' || property === 'priority_level') && (
              <a
                href={`/methodology/#${filterDescription.linkFragment}`}
                className="link"
                aria-label={`Learn more about ${
                  property === 'priority_level'
                    ? 'priority level'
                    : 'access process'
                } from our Methodology Page`}
              >
                Learn more{' '}
              </a>
            )}
          </p>
        )}
      </div>
      <div>{filter}</div>
    </div>
  );
};

export default DimensionFilter;
