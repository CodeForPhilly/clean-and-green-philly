'use client';

import { FC } from 'react';
import { ThemeButton } from './ThemeButton';
import { BarClickOptions } from '@/app/find-properties/[[...opa_id]]/page';
import { rcos, neighborhoods, zoning } from './Filters/filterOptions';
import FilterDescription from './Filters/FilterDescription';
import ButtonGroup from './Filters/ButtonGroup';
import MultiSelect from './Filters/MultiSelect';
import Panels from './Filters/Panels';
import { useFilter } from '@/context/FilterContext';

interface FilterViewProps {
  updateCurrentView: (view: BarClickOptions) => void;
}

const FilterView: FC<FilterViewProps> = ({ updateCurrentView }) => {
  const { dispatch } = useFilter();

  const onResetButtonPressed = () => {
    dispatch({
      type: 'CLEAR_DIMENSIONS',
      property: 'reset',
      dimensions: [],
    });
  };

  return (
    <div className="relative p-6">
      {/* Add ID to the close button */}
      <ThemeButton
        color="secondary"
        className="right-4 lg:right-[24px] absolute top-8 min-w-[3rem]"
        label={'Reset'}
        aria-label="Reset filters"
        id="close-filter-button" // Add an ID to this button
        onPress={onResetButtonPressed}
      />
      <div className="pt-3 pb-6">
        <FilterDescription
          title="Suggested Priority"
          description="Find properties based on how much they can reduce gun violence considering the gun violence, cleanliness, and tree canopy nearby. "
          link="/methodology/#priority-method"
        />
        <ButtonGroup
          property="priority_level"
          options={['Low', 'Medium', 'High']}
          aria_describedby_label="Suggested Priority"
        />
      </div>
      <div className="pt-3 pb-6">
        <FilterDescription
          title="Get Access"
          description="Find properties based on what we think the easiest method to get legal access to them is, based on the data available to us."
          link="/methodology/#access-method"
        />
        <Panels />
      </div>
      <div className="pt-3 pb-6">
        <FilterDescription title="Neighborhoods" />
        <MultiSelect
          property="neighborhood"
          options={neighborhoods}
          aria_describedby_label="Neighborhoods"
          useIndexOfFilter={false}
        />
      </div>
      <div className="pt-3 pb-6">
        <FilterDescription title="Community Organizations" />
        <MultiSelect
          property="rco_names"
          options={rcos}
          aria_describedby_label="Community_Organizations"
          useIndexOfFilter={true}
        />
      </div>

      <div className="pt-3 pb-6">
        <FilterDescription title="Zoning" />
        <MultiSelect
          property="zoning_base_district"
          options={zoning}
          aria_describedby_label="Zoning"
          useIndexOfFilter={false}
        />
      </div>
      <div className="pt-3 pb-6">
        <FilterDescription title="Property Type" />
        <ButtonGroup
          property="parcel_type"
          options={['Land', 'Building']}
          aria_describedby_label="Property_Type"
        />
      </div>
    </div>
  );
};

export default FilterView;
