import { extendVariants, Select, SelectItem } from "@nextui-org/react";

export const MultiSelect = extendVariants(Select, {
    variants: {
        color: {
            gray: {
                trigger: ["multiSelect", "data-[hover=true]:bg-gray-200"],
                value: ["text-gray-900"],
            }
        }
    },
    defaultVariants: {
        color: "gray"
    }
})

export const MultiSelectItem = extendVariants(SelectItem, {
    variants: {
        color: {
            gray: {
                base: ["multiSelectItem", "data-[hover=true]:ease-in h-6 bg-gray-200"],
                value: ["text-gray-900"]
            }
        }
    },
    defaultVariants: {
        color: "gray"
    }
})