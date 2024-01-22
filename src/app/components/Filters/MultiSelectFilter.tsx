import React, { useCallback, useState } from 'react';
import { Tooltip } from '@nextui-org/react';
import { useFilter } from '@/context/FilterContext';
import { InformationCircleIcon } from '@heroicons/react/24/outline';

type MultiSelectFilterProps = {
  property: string;
  display: string;
  options: string[];
  tooltip: string;
};

const MultiSelectFilter: React.FC<MultiSelectFilterProps> = ({
  property,
  display,
  options,
  tooltip,
}) => {
  const { dispatch } = useFilter();
  const [selectedKeys, setSelectedKeys] = useState<string[]>([]);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const toggleDimension = useCallback(
    (dimension: string) => {
      setSelectedKeys((prevKeys) => {
        const newKeys = prevKeys.includes(dimension)
          ? prevKeys.filter((key) => key !== dimension)
          : [...prevKeys, dimension];
        dispatch({ type: 'SET_DIMENSIONS', property, dimensions: newKeys });
        return newKeys;
      });
    },
    [dispatch, property]
  );

  return (
    <div className="pb-6 relative">
      <div className="flex items-center mb-2">
        <div className="text-md flex items-center">
          {display}
          <Tooltip content={tooltip} placement="top" showArrow color="primary">
            <InformationCircleIcon className="h-5 w-5 text-gray-500 ml-2 cursor-pointer" />
          </Tooltip>
        </div>
      </div>
      <button
        onClick={() => setDropdownOpen(!dropdownOpen)}
        className="px-4 py-2 bg-blue-500 text-white rounded focus:outline-none focus:shadow-outline"
      >
        Select Options
      </button>
      {dropdownOpen && (
        <div className="absolute z-10 bg-white border rounded shadow-lg mt-2 w-48">
          {options.map((option) => (
            <div key={option} className="flex items-center px-4 py-2 hover:bg-gray-100">
              <input
                type="checkbox"
                checked={selectedKeys.includes(option)}
                onChange={() => toggleDimension(option)}
                className="form-checkbox h-5 w-5 text-blue-600"
              />
              <label className="ml-2 text-sm">{option}</label>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MultiSelectFilter;
