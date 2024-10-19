import { FC } from 'react';
import DimensionFilter from './Filters/DimensionFilter';
import { PiX } from 'react-icons/pi';
import { BarClickOptions } from '@/app/find-properties/[[...opa_id]]/page';
import { ThemeButton } from './ThemeButton';
import { rcos, neighborhoods, zoning } from './Filters/filterOptions';

const filters = [
  {
    property: 'priority_level',
    display: 'Suggested Priority',
    options: ['Low', 'Medium', 'High'],
    type: 'buttonGroup',
  },
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
  {
    property: 'neighborhood',
    display: 'Neighborhoods',
    options: neighborhoods,
    type: 'multiSelect',
  },
  {
    property: 'rco_names',
    display: 'Community Organizations',
    options: rcos,
    type: 'multiSelect',
    useIndexOfFilter: true,
  },
  {
    property: 'zoning_base_district',
    display: 'Zoning',
    options: zoning,
    type: 'multiSelect',
  },
  {
    property: 'parcel_type',
    display: 'Property Type',
    options: ['Land', 'Building'],
    type: 'buttonGroup',
  },
];

interface FilterViewProps {
  updateCurrentView: (view: BarClickOptions) => void;
}

const FilterView: FC<FilterViewProps> = ({ updateCurrentView }) => {
  return (
    <div className="relative p-6">
      <ThemeButton
        color="secondary"
        className="right-4 lg:right-[24px] absolute top-8 min-w-[3rem]"
        aria-label="Close filter panel"
        startContent={<PiX />}
        onPress={() => updateCurrentView('filter')}
      />
      {filters.map((attr) => (
        <DimensionFilter key={attr.property} {...attr} />
      ))}
    </div>
  );
};

export default FilterView;
