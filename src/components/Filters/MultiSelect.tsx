'use client';

import React, { FC } from 'react';
import { X } from '@phosphor-icons/react';
import {
  SelectFilter,
  SelectFilterItem,
  SelectFilterChip,
  BlankSelectorIcon,
} from './MultiSelectVariants';

type MultiSelectProps = {
  display: string;
  options: any[];
  selectedKeys: string[];
  aria_describedby_label?: string;
  toggleDimension: (dimension: string) => void;
  handleSelectionChange: (
    selection: React.ChangeEvent<HTMLSelectElement> | string
  ) => void;
};

const MultiSelect: FC<MultiSelectProps> = ({
  display,
  options,
  selectedKeys,
  aria_describedby_label,
  toggleDimension,
  handleSelectionChange,
}) => {
  return (
    <div className="space-x-2 min-h-[33.5px] flex flex-col">
      <SelectFilter
        aria-describedby={aria_describedby_label}
        variant="flat"
        size="md"
        radius="md"
        placeholder="Select options..."
        selectedKey={null}
      >
        {options.map((option) => (
          <SelectFilterItem
            key={option}
            value={option}
            onClick={(e) => {
              const target = e.target as HTMLSpanElement;
              handleSelectionChange(target.innerText);
            }}
            endContent={selectedKeys.includes(option) && <div>Poop</div>}
          >
            {option}
          </SelectFilterItem>
        ))}
      </SelectFilter>
      <div className="flex min-h-14 mt-2 gap-y-2 flex-wrap">
        {selectedKeys.map((option) => (
          <SelectFilterChip
            key={option}
            classNames={{ base: 'multiSelectChip' }}
            endContent={<X aria-label={`close ${option}`} />}
            onClose={() => handleSelectionChange(option)}
          >
            {option}
          </SelectFilterChip>
        ))}
      </div>
    </div>
  );
};

export default MultiSelect;
