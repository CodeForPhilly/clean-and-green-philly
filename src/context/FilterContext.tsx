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

interface FilterState {
  active: { [property: string]: DimensionFilter };
  staged: { [property: string]: DimensionFilter };
}

interface FilterContextProps {
  appFilter: FilterState;
  dispatch: React.Dispatch<FilterAction>;
}

type FilterAction =
  | {
      type: "SET_STAGED_DIMENSIONS";
      property: string;
      dimensions: string[];
    }
  | {
      type: "PROMOTE_STAGED_DIMENSIONS";
    }
  | {
      type: "CLEAR_STAGED_DIMENSIONS";
    };

const filterReducer = (
  state: FilterState,
  action: FilterAction
): FilterState => {
  switch (action.type) {
    case "SET_STAGED_DIMENSIONS":
      return {
        ...state,
        staged: {
          ...state.active,
          [action.property]: {
            type: "dimension",
            values: action.dimensions,
          },
        },
      };
    case "PROMOTE_STAGED_DIMENSIONS":
      return {
        ...state,
        active: state.staged,
      };
    case "CLEAR_STAGED_DIMENSIONS":
      return {
        ...state,
        staged: {},
      };
    default:
      throw new Error("Unhandled action type");
  }
};

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
  const initialState: FilterState = {
    active: {},
    staged: {},
  };
  const [appFilter, dispatch] = useReducer(filterReducer, initialState);

  return (
    <FilterContext.Provider value={{ appFilter, dispatch }}>
      {children}
    </FilterContext.Provider>
  );
};
