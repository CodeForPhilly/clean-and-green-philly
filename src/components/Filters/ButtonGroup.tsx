'use client';

import React, { FC, useState } from 'react';
import { Button } from '@nextui-org/react';
import { Check } from '@phosphor-icons/react';
import { useFilter } from '@/context/FilterContext';

type ButtonGroupProps = {
  property: string;
  options: string[];
  aria_describedby_label?: string;
};

const ButtonGroup = ({
  property,
  options,
  aria_describedby_label,
}: ButtonGroupProps): JSX.Element => {
  const { dispatch, appFilter } = useFilter();
  const currentFilterKeys = appFilter[property]?.values || [];

  const toggleDimension = (dimension: string) => {
    const updatedKeys = currentFilterKeys.includes(dimension)
      ? currentFilterKeys.filter((item) => item !== dimension)
      : [...currentFilterKeys, dimension];

    dispatch({
      type: 'SET_DIMENSIONS',
      property,
      dimensions: updatedKeys,
    });
  };

  return (
    <div className="flex flex-wrap gap-x-2 min-h-[33.5px]">
      {options.map((option, index) => (
        <Button
          key={index}
          disableAnimation
          role="checkbox"
          onPress={() => toggleDimension(option)}
          size="sm"
          color={currentFilterKeys.includes(option) ? 'success' : 'default'}
          className={
            (currentFilterKeys.includes(option)
              ? 'tagSelected'
              : 'tagDefault') +
            (option === 'Private Land Use Agreement'
              ? ' max-[475px]:mt-2 sm:max-[1103px]:mt-2'
              : '')
          }
          radius="full"
          aria-checked={currentFilterKeys.includes(option)}
          aria-describedby={aria_describedby_label}
          startContent={
            currentFilterKeys.includes(option) ? (
              <Check className="w-3 max-h-6" />
            ) : undefined
          }
        >
          {option}
        </Button>
      ))}
    </div>
  );
};

export default ButtonGroup;
