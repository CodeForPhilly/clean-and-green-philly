"use client";

import React, { FC } from "react";
import { X } from "@phosphor-icons/react";
import {
  SelectFilter,
  SelectFilterItem,
  SelectFilterChip,
  BlankSelectorIcon,
} from "./MultiSelectVariants";

type MultiSelectProps = {
  display: string;
  options: string[];
  selectedKeys: string[];
  toggleDimension: (dimension: string) => void;
  handleSelectionChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
};

const MultiSelect: FC<MultiSelectProps> = ({
  display,
  options,
  selectedKeys,
  toggleDimension,
  handleSelectionChange,
}) => {
  const multiSelectOptions = options.filter((option) => {
    if (!selectedKeys.includes(option)) {
      return option;
    }
  });

  return (
    <div className="space-x-2 min-h-[33.5px]">
      <SelectFilter
        aria-label={display}
        items={options}
        variant="flat"
        size="md"
        radius="md"
        isMultiline={true}
        selectionMode="multiple"
        placeholder="Select options..."
        selectorIcon={<BlankSelectorIcon />}
        selectedKeys={selectedKeys}
        renderValue={() => {
          return (
            <div className="flex flex-wrap gap-y-2">
              {selectedKeys.map((option, index) => (
                <SelectFilterChip
                  key={index}
                  classNames={{ base: "multiSelectChip" }}
                  endContent={<X />}
                  onClose={() => toggleDimension(option)}
                >
                  {option}
                </SelectFilterChip>
              ))}
            </div>
          );
        }}
        onChange={handleSelectionChange}
      >
        {multiSelectOptions.map((option) => (
          <SelectFilterItem
            key={option}
            value={option}
            classNames={{ base: "multiSelectItem" }}
            shouldHighlightOnFocus={false}
          >
            {option}
          </SelectFilterItem>
        ))}
      </SelectFilter>
    </div>
  );
};

export default MultiSelect;
