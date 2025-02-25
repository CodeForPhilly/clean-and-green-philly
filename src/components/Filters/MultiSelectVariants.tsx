import {
  extendVariants,
  Chip,
  Autocomplete,
  AutocompleteItem,
  AutocompleteProps,
} from '@nextui-org/react';

export const SelectFilter = ({
  children,
  classNames,
  inputProps,
  ...props
}: AutocompleteProps) => {
  return (
    <Autocomplete
      classNames={{
        clearButton: 'hidden',
        selectorButton: 'hidden',
        ...classNames,
      }}
      inputProps={{
        classNames: {
          inputWrapper: [
            'multiSelect',
            'data-[hover=true]:bg-gray-100',
            'group-data-[focus=true]:bg-gray-100',
          ],
          input: ['text-gray-900', 'placeholder:text-gray-900'],
        },
        ...inputProps,
      }}
      {...props}
    >
      {children}
    </Autocomplete>
  );
};

export const SelectFilterItem = extendVariants(AutocompleteItem, {
  variants: {
    color: {
      gray: {
        base: ['multiSelectItem'],
        title: ['text-gray-900'],
      },
    },
    size: {
      md: {
        wrapper: 'm-12',
      },
    },
  },
  defaultVariants: {
    color: 'gray',
    size: 'md',
  },
});

export const SelectFilterChip = extendVariants(Chip, {
  variants: {
    color: {
      gray: {
        content: ['text-blue-800', , 'text-[hover=true]:blue-800'],
        closeButton: ['text-blue-800', , 'text-[hover=true]:blue-800'],
      },
    },
    size: {
      md: {
        base: 'h-6 mr-2 pl-2 py-0.5',
        content: 'pl-0 pr-1 text-sm',
      },
    },
  },
  defaultVariants: {
    color: 'gray',
    size: 'md',
  },
});

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
