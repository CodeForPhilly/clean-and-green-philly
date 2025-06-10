'use client';

import { useFilter } from '@/context/FilterContext';
import { FC } from 'react';
import ButtonGroup from './Filters/ButtonGroup';
import FilterDescription from './Filters/FilterDescription';
import { neighborhoods, rcos, zoning } from './Filters/filterOptions';
import MultiSelect from './Filters/MultiSelect';
import Panels from './Filters/Panels';
import { ThemeButton } from './ThemeButton';

const FilterView: FC = () => {
  const { dispatch } = useFilter();
  return (
    <div className="relative p-6">
      <ThemeButton
        color="secondary"
        className="right-4 lg:right-[24px] absolute top-8 min-w-[4rem] font-medium"
        aria-label="Close filter panel"
        label="Reset"
        id="close-filter-button"
        onPress={() =>
          dispatch({
            type: 'CLEAR_DIMENSIONS',
            property: '',
            dimensions: [],
          })
        }
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
