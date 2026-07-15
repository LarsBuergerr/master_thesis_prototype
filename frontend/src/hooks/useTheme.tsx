import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  THEME_COLORS,
  getStoredTheme,
  prefersDarkScheme,
  setStoredTheme,
  type Theme,
  type ThemeColors,
} from "../lib/theme";

interface ThemeContextValue {
  theme: Theme;
  colors: ThemeColors;
  /** Whether the theme is an explicit user choice (vs. following the OS). */
  isOverride: boolean;
  toggle: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  // `null` = no explicit choice yet; CSS alone follows `prefers-color-scheme`.
  const [override, setOverride] = useState<Theme | null>(() => getStoredTheme());
  const [systemDark, setSystemDark] = useState(prefersDarkScheme);

  useEffect(() => {
    const mql = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => setSystemDark(mql.matches);
    mql.addEventListener("change", onChange);
    return () => mql.removeEventListener("change", onChange);
  }, []);

  useEffect(() => {
    if (override) document.documentElement.setAttribute("data-theme", override);
    else document.documentElement.removeAttribute("data-theme");
  }, [override]);

  const theme: Theme = override ?? (systemDark ? "dark" : "light");

  const value = useMemo<ThemeContextValue>(
    () => ({
      theme,
      colors: THEME_COLORS[theme],
      isOverride: override !== null,
      toggle: () => {
        const next: Theme = theme === "dark" ? "light" : "dark";
        setOverride(next);
        setStoredTheme(next);
      },
    }),
    [theme, override],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within a ThemeProvider");
  return ctx;
}
