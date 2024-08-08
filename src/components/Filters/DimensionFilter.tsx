'use client';

import React, { useMemo, useState, FC } from 'react';
import { useFilter } from '@/context/FilterContext';
import ButtonGroup from './ButtonGroup';
import MultiSelect from './MultiSelect';
import Panels from './Panels';

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
  const initialSelectedPanelKeys = () => {
    const panelKeyObj: { [key: string]: string[] } = {};
    for (const key in appFilter) {
      panelKeyObj[key] = appFilter[key].values;
    }
    return panelKeyObj;
  };
  const [selectedPanelKeys, setSelectedPanelkeys] = useState<{
    [property: string]: string[];
  }>(initialSelectedPanelKeys());

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
    selection: React.ChangeEvent<HTMLSelectElement> | string
  ) => {
    let newMultiSelect: string[] = [];
    if (typeof selection === 'string') {
      newMultiSelect = selectedKeys.includes(selection)
        ? selectedKeys.filter((key) => key !== selection)
        : [...selectedKeys, selection];
    } else {
      if (selection.target.value !== '') {
        newMultiSelect = selection.target.value.split(',');
      }
    }
    setSelectedKeys(newMultiSelect);
    dispatch({
      type: 'SET_DIMENSIONS',
      property,
      dimensions: newMultiSelect,
      useIndexOfFilter,
    });
  };

  const filter = useMemo(() => {
    if (type === 'buttonGroup') {
      return (
        <ButtonGroup
          options={options}
          selectedKeys={selectedKeys}
          toggleDimension={toggleDimension}
          displayOptions={optionsDisplayMapping[property]}
        />
      );
    } else if (type === 'panels') {
      return (
        <Panels
          options={options}
          selectedPanelKeys={selectedPanelKeys}
          toggleDimensionForPanel={toggleDimensionForPanel}
        />
      );
    } else {
      return (
        <MultiSelect
          display={display}
          options={options}
          selectedKeys={selectedKeys}
          toggleDimension={toggleDimension}
          handleSelectionChange={handleSelectionChange}
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
      : {
          desc: 'Find properties based on what we think is the easiest method to get legal access to them, based on the data available to us. ',
          linkFragment: 'access-method',
        };

  // text-gray-500, 600 ? or #586266 (figma)?
  return (
    <div className="pt-3 pb-6">
      <div className="flex flex-col mb-2">
        <h2 className="heading-lg">{display}</h2>
        {(property === 'get_access' || property === 'priority_level') && (
          <p className="body-sm text-gray-500 w-[90%] my-1">
            {filterDescription.desc}
            <a
              href={`/methodology/#${filterDescription.linkFragment}`}
              className="link"
              aria-label={`Learn more about ${property === 'priority_level' ? 'priority level' : 'access process'} from our Methodology Page`}
            >
              Learn more{' '}
            </a>
          </p>
        )}
      </div>
      {filter}
    </div>
  );
};

export default DimensionFilter;
