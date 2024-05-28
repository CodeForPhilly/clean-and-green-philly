import React, {
  FC,
  createContext,
  useContext,
  useState,
  ReactNode,
} from "react";

interface CookieContextProps {
  shouldShowBanner: boolean;
  setShouldShowBanner: React.Dispatch<React.SetStateAction<boolean>>;
}

interface CookieProviderProps {
  children: ReactNode;
}

export const CookieContext = createContext<CookieContextProps | undefined>(
  undefined
);

export const useCookieContext = () => {
  const context = useContext(CookieContext);
  if (!context) {
    throw new Error("useCookieContext must be used within a CookieProvider");
  }
  return context;
};

export const CookieProvider: FC<CookieProviderProps> = ({ children }) => {
  const [shouldShowBanner, setShouldShowBanner] = useState(true);

  return (
    <CookieContext.Provider value={{ shouldShowBanner, setShouldShowBanner }}>
      {children}
    </CookieContext.Provider>
  );
};
