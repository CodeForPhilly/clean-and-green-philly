import React, {
  FC,
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
} from "react";

interface CookieContextProps {
  shouldAllowCookies: boolean;
  shouldShowBanner: boolean;
  setShouldAllowCookies: React.Dispatch<React.SetStateAction<boolean>>;
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
  const [shouldAllowCookies, setShouldAllowCookies] = useState<boolean>(() => {
    if (typeof window !== "undefined" && window.localStorage) {
      const storedPrefs = localStorage.getItem("cookiePrefs");
      return storedPrefs ? JSON.parse(storedPrefs).shouldAllowCookies : false;
    }
    return false;
  });

  const [shouldShowBanner, setShouldShowBanner] = useState<boolean>(() => {
    if (typeof window !== "undefined" && window.localStorage) {
      const storedPrefs = localStorage.getItem("cookiePrefs");
      return storedPrefs ? JSON.parse(storedPrefs).shouldShowBanner : true;
    }
    return true;
  });

  useEffect(() => {
    localStorage.setItem(
      "cookiePrefs",
      JSON.stringify({ shouldAllowCookies, shouldShowBanner })
    );
  }, [shouldAllowCookies, shouldShowBanner]);

  return (
    <CookieContext.Provider
      value={{
        shouldAllowCookies,
        shouldShowBanner,
        setShouldAllowCookies,
        setShouldShowBanner,
      }}
    >
      {children}
    </CookieContext.Provider>
  );
};
