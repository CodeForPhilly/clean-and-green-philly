'use client';

import React, { FC } from 'react';
import {
  AutocompleteFilter,
  AutocompleteFilterItem,
} from './AutoCompleteVariants';

type AutocompleteProps = {
  display: string;
  options: string[];
  limitType: string;
  selectedRange: string | React.ChangeEvent<HTMLSelectElement>;
  setSelectedRange: (prev: any) => void;
  aria_describedby_label?: string;
  handleSelectionChange: (selection: string, limitType: string) => void;
};

export const Autocomplete: FC<AutocompleteProps> = ({
  options,
  limitType,
  selectedRange,
  setSelectedRange,
  aria_describedby_label,
  handleSelectionChange,
}) => {
  const selectedKey = options.indexOf(selectedRange as string).toString();

  const onEnter = (key: string) => {
    setSelectedRange((prev: any) => ({
      ...prev,
      [limitType]: key,
    }));
    handleSelectionChange(key, limitType);
  };
  return (
    <div className="space-x-2 min-h-[33.5px]">
      <AutocompleteFilter
        aria-describedby={aria_describedby_label}
        defaultSelectedKey={selectedKey}
        variant="flat"
        size="md"
        radius="md"
        onKeyUp={(key) =>
          key.key === 'Enter' && onEnter(key.currentTarget.value)
        }
        placeholder="Select options..."
      >
        {options.map((option: string, index: number) => (
          <AutocompleteFilterItem key={index} shouldHighlightOnFocus={false}>
            {option}
          </AutocompleteFilterItem>
        ))}
      </AutocompleteFilter>
    </div>
  );
};

export default Autocomplete;
