"use client";

import React, { FC } from "react";
import { Card, CardBody } from "@nextui-org/react";
import { Check } from "@phosphor-icons/react";
import { access_options, PropertyAccess, PropertyAccessOption } from "@/config/propertyAccessOptions";

type PanelFilterOptions = PropertyAccessOption & {
    alt_description: string;
    dimension: string;
    property: string;
}

type PanelsProps = {
    options: string[] | PropertyAccess[];
    selectedPanelKeys: {[property: string]: string[]};
    toggleDimensionForPanel: (dimension: string, property: string) => void;
}

const panel_access_options: Record<PropertyAccess | string, PanelFilterOptions> = {
    [PropertyAccess.PRIVATE_LAND_USE]: {
        ...access_options[PropertyAccess.PRIVATE_LAND_USE],
        alt_description:
        'Properties where you could get a "private land use agreement"',
        dimension: 'Private Land Use Agreement',
        property: 'access_process',
    },
    [PropertyAccess.TACTICAL_URBANISM]: {
        ...access_options[PropertyAccess.TACTICAL_URBANISM],
        alt_description:
          'Properties likely safe to quickly clean without express permission',
        dimension: 'Yes',
        property: 'tactical_urbanism',
      },
      [PropertyAccess.BUY_FROM_OWNER]: {
        ...access_options[PropertyAccess.BUY_FROM_OWNER],
        alt_description:
          'Properties with a market value under $1,000',
        dimension: 'Buy Property',
        property: 'access_process',
      },
      [PropertyAccess.SIDE_YARD]: {
        ...access_options[PropertyAccess.SIDE_YARD],
        alt_description:
          'Properties eligible for the "Side Yard Program"',
        dimension: 'Yes',
        property: 'side_yard_eligible',
      },
      [PropertyAccess.LAND_BANK]: {
        ...access_options[PropertyAccess.LAND_BANK],
        alt_description:
          'Properties available for discount prices from the Land Bank',
        dimension: 'Land Bank',
        property: 'access_process',
      },
      [PropertyAccess.CONSERVATORSHIP]: {
        ...access_options[PropertyAccess.CONSERVATORSHIP],
        alt_description:
          'Abandoned and unsafe properties you can gain through a legal process',
        dimension: 'Yes',
        property: 'conservatorship',
      },
}

const Panels: FC<PanelsProps> = ({
    options,
    selectedPanelKeys,
    toggleDimensionForPanel,
}) => {

    const optionPanels = options.map((option, index) => {
        const panel = panel_access_options[option]
        const Icon = panel.icon;
        const isSelected = (selectedPanelKeys[panel.property] && selectedPanelKeys[panel.property].includes(panel.dimension)) ? true : false;

        return (
            <Card
                key={index}
                className = {isSelected ? "panelSelected " : "panelDefault"}
                isPressable
                isHoverable={false}
                onPress={() => toggleDimensionForPanel(panel.dimension, panel.property)}
                shadow="none"
            >
                <CardBody className="flex flex-row justify-between p-[0px]">
                    <div className="flex flex-row space-x-1">
                        <div >
                            <Icon aria-hidden={true} className="size-8" />
                        </div>
                        <div className="flex flex-row items-center sm:items-start sm:flex-col lg:flex-row lg:items-center">
                            <div className="flex flex-col flex-0">
                            <div className="heading-md">{panel.header}</div>
                            <div className="body-sm">{panel.alt_description}</div>
                            </div>
                        </div>

                    </div>
                    <div >
                        {isSelected ? <Check className="self-end size-5" /> : undefined}
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