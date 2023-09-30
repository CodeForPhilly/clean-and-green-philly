import React, {
  FC,
  useState,
  createContext,
  useContext,
  ReactNode,
} from "react";

export interface FilterContextProps {
  filter: Record<string, string[]>;
  setFilter: React.Dispatch<React.SetStateAction<Record<string, string[]>>>;
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
  const [filter, setFilter] = useState<Record<string, string[]>>({});

  return (
    <FilterContext.Provider value={{ filter, setFilter }}>
      {children}
    </FilterContext.Provider>
  );
};
