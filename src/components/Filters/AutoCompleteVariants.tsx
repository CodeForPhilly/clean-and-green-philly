import {
  Autocomplete,
  AutocompleteItem,
  extendVariants,
} from '@nextui-org/react';

export const AutocompleteFilterItem = extendVariants(AutocompleteItem, {
  variants: {
    color: {
      gray: {
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

export const AutocompleteFilter = extendVariants(Autocomplete, {
  variants: {
    color: {
      gray: {
        base: 'text-gray-900',
      },
    },
    size: {
      md: {
        base: 'py-2',
      },
    },
  },
  defaultVariants: {
    color: 'gray',
    size: 'md',
  },
});
