'use client';

import React, { FC, useEffect, useRef, useState } from 'react';
import { Check, X } from '@phosphor-icons/react';
import {
  SelectFilter,
  SelectFilterItem,
  SelectFilterChip,
} from './MultiSelectVariants';
import { useFilter } from '@/context/FilterContext';

type MultiSelectProps = {
  property: string;
  options: any[];
  aria_describedby_label?: string;
  useIndexOfFilter?: boolean;
};

const MultiSelect = ({
  property,
  options,
  aria_describedby_label,
  useIndexOfFilter,
}: MultiSelectProps): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const { dispatch, appFilter } = useFilter();

  const currentFilterKeys = appFilter[property]?.values || [];

  // Override Autocomplete design to continue focus on the input after closing the popover menu
  useEffect(() => {
    if (!isOpen) {
      inputRef.current?.blur();
    }
  }, [isOpen]);

  const handleSelectFilterKeys = (selection: string) => {
    const updatedKeys = currentFilterKeys.includes(selection)
      ? currentFilterKeys.filter((option) => option !== selection)
      : [...currentFilterKeys, selection];

    dispatch({
      type: 'SET_DIMENSIONS',
      property,
      dimensions: updatedKeys,
      useIndexOfFilter,
    });
  };

  return (
    <div className="space-x-2 min-h-[33.5px] flex flex-col">
      <SelectFilter
        aria-describedby={aria_describedby_label}
        variant="flat"
        size="md"
        radius="md"
        placeholder="Select options..."
        selectedKey={null}
        inputProps={{
          ref: inputRef,
        }}
        onOpenChange={() => setIsOpen((prev) => !prev)}
      >
        {options.map((option) => (
          <SelectFilterItem
            key={option}
            value={option}
            onClick={(e) => {
              const target = e.target as HTMLSpanElement;
              handleSelectFilterKeys(target.innerText);
            }}
            endContent={
              currentFilterKeys.includes(option) && <Check weight="bold" />
            }
          >
            {option}
          </SelectFilterItem>
        ))}
      </SelectFilter>
      <div className="flex mt-2 gap-y-2 flex-wrap">
        {currentFilterKeys.map((option) => (
          <SelectFilterChip
            key={option}
            classNames={{ base: 'multiSelectChip' }}
            endContent={<X aria-label={`close ${option}`} />}
            onClose={() => handleSelectFilterKeys(option)}
          >
            {option}
          </SelectFilterChip>
        ))}
      </div>
    </div>
  );
};

export default MultiSelect;
