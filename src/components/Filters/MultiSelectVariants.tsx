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
                base: ["multiSelectItem", "data-[hover=true]:gray-200"],
                value: ["text-gray-900"]
            }
        }
    },
    defaultVariants: {
        color: "gray"
    }
})

export const BlankSelectorIcon = () => (
    <svg
      aria-hidden="true"
      fill="none"
      focusable="false"
      height="1em"
      role="presentation"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="1.5"
      viewBox="0 0 24 24"
      width="1em"
    >
      {/* empty selector icon */}
    </svg>
);