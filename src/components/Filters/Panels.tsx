"use client";

import React, { FC } from "react";
import { Button, Card, CardBody, Chip } from "@nextui-org/react";
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
        const panelStyle = () => {
            if (selectedPanelKeys[panel.property]) {
                if (selectedPanelKeys[panel.property].includes(panel.dimension)) {
                    return "panelSelected"
                } else {
                    return "panelDefault"
                }
            } else {
                return "panelDefault"
            }
        }
        const checkMark = () => {
            if (selectedPanelKeys[panel.property]) {
                if (selectedPanelKeys[panel.property].includes(panel.dimension)) {
                    return <Check className="w-3 w-3.5 max-h-6" />
                } else {
                    return undefined
                }
            } else {
                return undefined
            }
        }

        return (
            <Card
                className = { panelStyle() }
                isPressable
                onPress={() => toggleDimensionForPanel(panel.dimension, panel.property)}
            >
                <CardBody className="flex flex-row space-x-1 py-[0px] px-[0px]">
                    <div >
                        <Icon aria-hidden={true} className="size-8" />
                    </div>
                    <div className="flex flex-row items-center sm:items-start sm:flex-col lg:flex-row lg:items-center">
                        <div className="flex flex-col flex-0">
                        <div className="heading-md">{panel.header}</div>
                        <div className="body-sm">{panel.alt_description}</div>
                        </div>
                    </div>
                    <div >
                        {checkMark()}
                    </div>

                </CardBody>
            </Card>
        )
    })

    return (
        <div className="flex flex-col space-y-2">
            {optionPanels}
        </div>
    )
}

export default Panels