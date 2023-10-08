import React, {
  FC,
  useReducer,
  createContext,
  useContext,
  ReactNode,
} from "react";

export interface DimensionFilter {
  type: "dimension";
  values: string[];
}

export interface MeasureFilter {
  type: "measure";
  min: number;
  max: number;
}

type FilterValue = DimensionFilter | MeasureFilter;

interface FilterState {
  [property: string]: FilterValue;
}

interface FilterContextProps {
  filter: FilterState;
  dispatch: React.Dispatch<FilterAction>;
}

type FilterAction =
  | { type: "SET_DIMENSIONS"; property: string; dimensions: string[] }
  | { type: "TOGGLE_DIMENSION"; property: string; dimension: string }
  | { type: "SET_MEASURES"; property: string; min: number; max: number };

function filterReducer(state: FilterState, action: FilterAction): FilterState {
  switch (action.type) {
    case "SET_DIMENSIONS":
      return {
        ...state,
        [action.property]: { type: "dimension", values: action.dimensions },
      };
    case "TOGGLE_DIMENSION": {
      const filterValue = state[action.property];
      if (filterValue?.type === "dimension") {
        const updatedDimensions = filterValue.values.includes(action.dimension)
          ? filterValue.values.filter((d) => d !== action.dimension)
          : [...filterValue.values, action.dimension];
        return {
          ...state,
          [action.property]: { type: "dimension", values: updatedDimensions },
        };
      }
      return state;
    }
    case "SET_MEASURES":
      return {
        ...state,
        [action.property]: {
          type: "measure",
          min: action.min,
          max: action.max,
        },
      };
    default:
      throw new Error("Unhandled action type");
  }
}

export const FilterContext = createContext<FilterContextProps | undefined>(
  undefined
);

export const useFilter = () => {
  const context = useContext(FilterContext);
  if (!context) {
    throw new Error("useFilter must be used within a FilterProvider");
  }
  return context;
};

interface FilterProviderProps {
  children: ReactNode;
}

export const FilterProvider: FC<FilterProviderProps> = ({ children }) => {
  const [filter, dispatch] = useReducer(filterReducer, {});

  return (
    <FilterContext.Provider value={{ filter, dispatch }}>
      {children}
    </FilterContext.Provider>
  );
};
