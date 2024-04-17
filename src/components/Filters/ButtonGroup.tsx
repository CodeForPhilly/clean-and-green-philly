"use client";

import React, { FC } from "react";
import { Button } from "@nextui-org/react";
import { Check } from "@phosphor-icons/react";


type ButtonGroupProps = {
    options: string[];
    selectedKeys: string[];
    toggleDimension: (dimension: string) => void;
}

const ButtonGroup: FC<ButtonGroupProps> = ({
    options,
    selectedKeys,
    toggleDimension,
}) => {

    return (
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
    )
}

export default ButtonGroup