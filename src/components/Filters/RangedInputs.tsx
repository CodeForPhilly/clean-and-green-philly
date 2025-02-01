'use client';

import React, { FC } from 'react';
import Autocomplete from './AutoComplete';

type RangedInputsProps = {
  display: string;
  options: string[];
  selectedRanges:
    | {
        min: string | React.ChangeEvent<HTMLSelectElement>;
        max: string | React.ChangeEvent<HTMLSelectElement>;
      }
    | undefined;
  setSelectedRanges: (prev: any) => void;
  aria_describedby_label?: string;
  handleSelectionChange: (selection: string) => void;
};

const RangedInputs: FC<RangedInputsProps> = ({
  display,
  options,
  selectedRanges,
  setSelectedRanges,
  aria_describedby_label,
  handleSelectionChange,
}) => {
  return (
    <div className="flex items-center  min-h-[40px]">
      <div className="flex flex-col">
        <label
          htmlFor="max"
          className="body-sm font-medium text-gray-700"
          aria-describedby={aria_describedby_label}
        >
          Min
        </label>
        <Autocomplete
          display={display}
          limitType={'min'}
          selectedRange={selectedRanges?.min ?? ''}
          setSelectedRange={setSelectedRanges}
          options={options}
          aria_describedby_label=""
          handleSelectionChange={handleSelectionChange}
        />
      </div>
      <div className="flex items-center justify-center mt-6 h-0.5 w-5 bg-gray-400"></div>
      <div className="flex flex-col">
        <label
          htmlFor="max"
          className="body-sm font-medium text-gray-700"
          aria-describedby={aria_describedby_label}
        >
          Max
        </label>
        <Autocomplete
          display={display}
          limitType={'max'}
          selectedRange={selectedRanges?.max ?? ''}
          setSelectedRange={setSelectedRanges}
          options={options}
          aria_describedby_label=""
          handleSelectionChange={handleSelectionChange}
        />
      </div>
    </div>
  );
};

export default RangedInputs;
