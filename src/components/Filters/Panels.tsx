"use client";

import React, { FC } from "react";
import { Button, Card, Chip } from "@nextui-org/react";
import { Check } from "@phosphor-icons/react";

import { access_options, PropertyAccess, PropertyAccessOption } from "@/config/propertyAccessOptions";

type PanelsProps = {
    options: string[] | PropertyAccess[];
    selectedPanelKeys: {[property: string]: string[]};
    toggleDimensionForPanel: (dimension: string, property: string) => void;
}

const Panels: FC<PanelsProps> = ({
    options,
    selectedPanelKeys,
    toggleDimensionForPanel,
}) => {

    const optionPanels = options.map((option) => {
        const panel = access_options[option]
        const Icon = panel.icon;

        return (
            <Button
                className={`flex flex-row items-center rounded-md p-3 space-x-3 bg-gray-100 text-gray-900`}
                onClick={(e) => {
                    toggleDimensionForPanel(panel.dimension, panel.property)
                }}
            >
                <div >
                    <Icon aria-hidden={true} className="size-8" />
                </div>
                <div className="flex flex-row items-center sm:items-start sm:flex-col lg:flex-row lg:items-center">
                    <div className="flex flex-col flex-0">
                    <div className="heading-md">{panel.header}</div>
                    <div className="body-sm">{panel.alt_description}</div>
                    </div>
                </div>
                {/* <div className="flex-1">
                    <PiCaretRight
                    aria-hidden={true}
                    className={clsx("size-6", {
                        ["invisible"]: !option.slug,
                    })}
                    />
                </div> */}
            </Button>
        )
    })

    return (
        <div className="flex flex-col space-y-2">
            {optionPanels}
        </div>
    )
}

export default Panels