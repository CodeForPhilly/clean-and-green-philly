"use client";

import React, { useState, FC } from "react";
import { Button, Chip, Tooltip } from "@nextui-org/react";
import { useFilter } from "@/context/FilterContext";
import { Check, Info } from "@phosphor-icons/react";
import { rcos_detail } from "./FilterOptions"
import { MultiSelect, MultiSelectItem, BlankSelectorIcon } from "./MultiSelectVariants"

type DimensionFilterProps = {
  property: string;
  display: string;
  options: string[];
  tooltip: string;
};

const DimensionFilter: FC<DimensionFilterProps> = ({
  property,
  display,
  options,
  tooltip,
}) => {
  const { dispatch, appFilter } = useFilter();
  const [selectedKeys, setSelectedKeys] = useState<string[]>(
    appFilter[property]?.values || []
  );

  const toggleDimension = (dimension: string) => {
    const newSelectedKeys = selectedKeys.includes(dimension)
    ? selectedKeys.filter(key => key !== dimension)
    : [...selectedKeys, dimension];
    setSelectedKeys(newSelectedKeys);
    dispatch({
      type: "SET_DIMENSIONS",
      property,
      dimensions: newSelectedKeys,
    });
  };
  
  const handleSelectionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newMultiSelect: string[] = e.target.value.split(",")
    setSelectedKeys(newMultiSelect);
    const newDimensions = (property === 'neighborhood') ? newMultiSelect : newMultiSelect.map((rco) => {
      return rcos_detail[rco]
    })
    dispatch({
      type: "SET_DIMENSIONS",
      property,
      dimensions: newDimensions,
    });
  }

  const handleSelectionRemove = (removedOption: string | undefined) => {
    const newMultiSelect: string[] = selectedKeys.filter(option => option !== removedOption)
    setSelectedKeys(newMultiSelect)
    const newDimensions = (property === 'neighborhood') ? newMultiSelect : newMultiSelect.map((rco) => {
      return rcos_detail[rco]
    })
    dispatch({
      type: "SET_DIMENSIONS",
      property,
      dimensions: newDimensions,
    });
  }

  if (property === "neighborhood" || property === "rco_info") {
  
    const multiSelectOptions = options.filter((option) => {
      if (!selectedKeys.includes(option)) {
        return option
      }
    })

    return (
      <div className="pb-6">
        <div className="flex items-center mb-2">
          <div className="flex items-center">
            <h2 className="heading-lg">{display}</h2>
            <Tooltip content={tooltip} placement="top" showArrow color="primary">
              <Info
                alt="More Info"
                className="h-5 w-9 text-gray-500 pl-2 pr-2 cursor-pointer"
                tabIndex={0}
              />
            </Tooltip>
          </div>
        </div>
        <div className="space-x-2 min-h-[33.5px]">
          <MultiSelect
            aria-label={display}
            items={options}
            variant="flat"
            size="sm"
            radius="md"
            isMultiline={true}
            selectionMode="multiple"
            placeholder="Select options"
            selectorIcon={<BlankSelectorIcon />}
            selectedKeys={selectedKeys}
            renderValue={() => {
              return (
                <div className="flex flex-wrap gap-2">
                  {selectedKeys.map((option, index) => (
                    <Chip key={index} classNames={{base:"multiSelectChip"}} onClose={() => handleSelectionRemove(option)}>{option}</Chip>
                  ))}
                </div>
              )
            }}
            onChange={handleSelectionChange}
          >
            {multiSelectOptions.map((option) => (
              <MultiSelectItem 
                key={option} 
                value={option}
                selectedIcon={<BlankSelectorIcon />}
                shouldHighlightOnFocus={false}
              >
                {option}
              </MultiSelectItem>
            ))}
          </MultiSelect>
        </div>
        {}
      </div>
    )
  } 

  return (
    <div className="pb-6">
      <div className="flex items-center mb-2">
        <div className="flex items-center">
          <h2 className="heading-lg">{display}</h2>
          <Tooltip content={tooltip} placement="top" showArrow color="primary">
            <Info
              alt="More Info"
              className="h-5 w-9 text-gray-500 pl-2 pr-2 cursor-pointer"
              tabIndex={0}
            />
          </Tooltip>
        </div>
      </div>
      <div className="space-x-2 min-h-[33.5px]">
        {options.map((option, index) => (
          <Button
            key={index}
            disableAnimation
            onPress={() => toggleDimension(option)}
            size="sm"
            color={selectedKeys.includes(option) ? "success" : "default"}
            className={
              selectedKeys.includes(option) ? "tagSelected" : "tagDefault"
            }
            radius="full"
            aria-pressed={selectedKeys.includes(option)}
            startContent={
              selectedKeys.includes(option) ? (
                <Check className="w-3 w-3.5 max-h-6" />
              ) : undefined
            }
          >
            {option}
          </Button>
        ))}
      </div>
    </div>
  );
};

export default DimensionFilter;
