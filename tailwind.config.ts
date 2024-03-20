import type { Config } from "tailwindcss";
import { nextui } from "@nextui-org/react";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        body: ['"HK Grotesk"', "sans-serif"],
        display: ['"HK Grotesk"', "sans-serif"],
      },
      colors: {
        gray: {
          900: "#03141B",
          100: "#EAF3F7",
          60: "#737E6C",
          40: "#C0C7BC",
          20: "#D2D7D0",
          10: "#F2F3F2",
          0: "#FFFFFF",
        },
        blue: {
          DEFAULT: "#3867DE",
        },
        yellow: {
          800: "#443500",
          200: "#FFF0BB",
        },
        red: {
          200: "#F7C4BC",
          800: "#440900",
        },
        green: {
          800: "#094400",
          200: "#C2F5BA",
          100: "#E9FFE5",
          80: "#00A40C",
          60: "#35C03F",
          10: "#D8FFDB",
        },
        orange: {
          60: "#E56535",
          40: "#FBB57D",
          20: "#F4E4D4",
        },
        priority: {
          high: "#F9492C",
          medium: "#F1C936",
          low: "#95E089",
        },
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      borderRadius: {
        lg: "24px",
        md: "12px",
        sm: "6px",
      },
    },
  },
  darkMode: "class",
  plugins: [nextui()],
};

export default config;
