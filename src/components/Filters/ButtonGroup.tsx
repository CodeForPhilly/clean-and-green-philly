"use client";

import React, { FC } from "react";
import { Button } from "@nextui-org/react";
import { Check } from "@phosphor-icons/react";

type ButtonGroupProps = {
  options: string[];
  selectedKeys: string[];
  toggleDimension: (dimension: string) => void;
  displayOptions?: { [key: string]: string };
};

const ButtonGroup: FC<ButtonGroupProps> = ({
  options,
  selectedKeys,
  toggleDimension,
  displayOptions = {},
}) => {
  return (
    <div className="flex flex-wrap gap-x-2 min-h-[33.5px]">
      {options.map((option, index) => (
        <Button
          key={index}
          disableAnimation
          onPress={() => toggleDimension(option)}
          size="sm"
          color={selectedKeys.includes(option) ? "success" : "default"}
          className={
            (selectedKeys.includes(option) ? "tagSelected" : "tagDefault") +
            (option === "Private Land Use Agreement"
              ? " max-[475px]:mt-2 sm:max-[1103px]:mt-2"
              : "")
          }
          radius="full"
          aria-pressed={selectedKeys.includes(option)}
          startContent={
            selectedKeys.includes(option) ? (
              <Check className="w-3 w-3.5 max-h-6" />
            ) : undefined
          }
        >
          {displayOptions[option] || option}
        </Button>
      ))}
    </div>
  );
};

export default ButtonGroup;
