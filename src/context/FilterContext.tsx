import React, {
  FC,
  useReducer,
  createContext,
  useContext,
  ReactNode,
} from 'react';

export interface DimensionFilter {
  type: 'dimension';
  values?: string[];
  rangedValues?: {
    max: string | React.ChangeEvent<HTMLSelectElement>;
    min: string | React.ChangeEvent<HTMLSelectElement>;
  };
  useIndexOfFilter?: boolean;
  limitType?: string | boolean;
}

interface FilterState {
  [property: string]: DimensionFilter;
}

interface FilterContextProps {
  appFilter: FilterState;
  dispatch: React.Dispatch<FilterAction>;
}

type FilterAction = {
  type: 'SET_DIMENSIONS' | 'CLEAR_DIMENSIONS';
  property: string;
  dimensions:
    | string[]
    | {
        max: string | React.ChangeEvent<HTMLSelectElement>;
        min: string | React.ChangeEvent<HTMLSelectElement>;
      };
  useIndexOfFilter?: boolean;
  limitType?: string | boolean;
};

const filterReducer = (
  state: FilterState,
  action: FilterAction
): FilterState => {
  switch (action.type) {
    case 'SET_DIMENSIONS':
      if (Array.isArray(action.dimensions)) {
        if (action.dimensions.length === 0) {
          const { [action.property]: _, ...rest } = state;
          return rest;
        }
        return {
          ...state,
          [action.property]: {
            type: 'dimension',
            values: action.dimensions,
            useIndexOfFilter: action.useIndexOfFilter || false,
          },
        };
      } else {
        return {
          ...state,
          [action.property]: {
            type: 'dimension',
            rangedValues: action.dimensions,
            useIndexOfFilter: action.useIndexOfFilter || false,
            limitType: action.limitType,
          },
        };
      }

    case 'CLEAR_DIMENSIONS':
      return {};
    default:
      throw new Error('Unhandled action type');
  }
};

export const FilterContext = createContext<FilterContextProps | undefined>(
  undefined
);

export const useFilter = () => {
  const context = useContext(FilterContext);
  if (!context) {
    throw new Error('useFilter must be used within a FilterProvider');
  }
  return context;
};

interface FilterProviderProps {
  children: ReactNode;
}

export const FilterProvider: FC<FilterProviderProps> = ({ children }) => {
  const [appFilter, dispatch] = useReducer(filterReducer, {});

  return (
    <FilterContext.Provider value={{ appFilter, dispatch }}>
      {children}
    </FilterContext.Provider>
  );
};
