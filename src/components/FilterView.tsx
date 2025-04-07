'use client';

import { FC } from 'react';
import { PiX } from 'react-icons/pi';
import { ThemeButton } from './ThemeButton';
import { BarClickOptions } from '@/app/find-properties/[[...opa_id]]/page';
import { rcos, neighborhoods, zoning } from './Filters/filterOptions';
import DimensionFilter from './Filters/DimensionFilter';
import FilterDescription from './Filters/FilterDescription';
import { title } from 'process';
import ButtonGroup from './Filters/ButtonGroup';
import MultiSelect from './Filters/MultiSelect';

const filters = [
  {
    property: 'get_access',
    display: 'Get Access',
    options: [
      'TACTICAL_URBANISM',
      'PRIVATE_LAND_USE',
      'BUY_FROM_OWNER',
      'SIDE_YARD',
      'LAND_BANK',
      'CONSERVATORSHIP',
    ],
    type: 'panels',
  },
  // {
  //   property: 'neighborhood',
  //   display: 'Neighborhoods',
  //   options: neighborhoods,
  //   type: 'multiSelect',
  // },
  // {
  //   property: 'rco_names',
  //   display: 'Community Organizations',
  //   options: rcos,
  //   type: 'multiSelect',
  //   useIndexOfFilter: true,
  // },
  // {
  //   property: 'zoning_base_district',
  //   display: 'Zoning',
  //   options: zoning,
  //   type: 'multiSelect',
  // },
  // {
  //   property: 'parcel_type',
  //   display: 'Property Type',
  //   options: ['Land', 'Building'],
  //   type: 'buttonGroup',
  // },
];

// const filterDescriptions: FilterDescriptionProps[] = [
//   {
//     title: 'Suggested Priority',
//     description:
//       'Find properties based on how much they can reduce gun violence considering the gun violence, cleanliness, and tree canopy nearby.',
//     link: 'priority-method',
//   },
//   {
//     title: 'Market Value',
//     description: 'Find properties based on their market value (USD).',
//   },
//   {
//     title: 'Get Access',
//     description:
//       'Find properties based on what we think the easiest method to get legal access to them is, based on the data available to us.',
//     link: 'access-method',
//   },
//   {
//     title: 'Neighborhoods',
//   },
//   {
//     title: 'Community Organizations',
//   },
//   {
//     title: 'Zoning',
//   },
//   {
//     title: 'Property Type',
//   },
// ];

interface FilterViewProps {
  updateCurrentView: (view: BarClickOptions) => void;
}

const FilterView: FC<FilterViewProps> = ({ updateCurrentView }) => {
  return (
    <div className="relative p-6">
      {/* Add ID to the close button */}
      <ThemeButton
        color="secondary"
        className="right-4 lg:right-[24px] absolute top-8 min-w-[3rem]"
        aria-label="Close filter panel"
        startContent={<PiX />}
        id="close-filter-button" // Add an ID to this button
        onPress={() => {
          updateCurrentView('filter');
        }}
      />
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
      <FilterDescription title="Neighborhoods" />
      <MultiSelect
        property="neighborhood"
        options={neighborhoods}
        aria_describedby_label="Neighborhoods"
        useIndexOfFilter={false}
      />
      <FilterDescription title="Community Organizations" />
      <MultiSelect
        property="rco_names"
        options={rcos}
        aria_describedby_label="Community_Organizations"
        useIndexOfFilter={true}
      />
      <FilterDescription title="Zoning" />
      <MultiSelect
        property="zoning_base_district"
        options={zoning}
        aria_describedby_label="Zoning"
        useIndexOfFilter={false}
      />
      <FilterDescription title="Property Type" />
      <ButtonGroup
        property="parcel_type"
        options={['Land', 'Building']}
        aria_describedby_label="Property_Type"
      />
      {filters.map((attr) => (
        <DimensionFilter key={attr.property} {...attr} />
      ))}
    </div>
  );
};

export default FilterView;
