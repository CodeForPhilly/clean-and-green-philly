import React, {
  FC,
  useReducer,
  createContext,
  useContext,
  ReactNode,
} from "react";

export interface FilterContextProps {
  filter: Record<string, string[]>;
  dispatch: React.Dispatch<FilterAction>;
}

type FilterAction =
  | { type: "SET_DIMENSIONS"; property: string; dimensions: string[] }
  | { type: "TOGGLE_DIMENSION"; property: string; dimension: string };

function filterReducer(
  state: Record<string, string[]>,
  action: FilterAction
): Record<string, string[]> {
  switch (action.type) {
    case "SET_DIMENSIONS":
      return { ...state, [action.property]: action.dimensions };
    case "TOGGLE_DIMENSION": {
      const prevSelectedDimensions = state[action.property] || [];
      const updatedDimensions = prevSelectedDimensions.includes(
        action.dimension
      )
        ? prevSelectedDimensions.filter((d) => d !== action.dimension)
        : [...prevSelectedDimensions, action.dimension];
      return { ...state, [action.property]: updatedDimensions };
    }
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
