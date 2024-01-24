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
        body: ['"HK Grotesk"', 'sans-serif'],
        display: ['"HK Grotesk"', 'sans-serif'],
      },
      colors: {
        gray: {
          100: '#173009',
          60: '#737E6C',
          40: '#C0C7BC',
          20: '#D2D7D0',
          10: '#F2F3F2',
          0: '#FFFFFF',
        },
        blue: {
          DEFAULT: '#3867DE',
        },
        green: {
          100: '#006B08',
          80: '#00A40C',
          60: '#35C03F',
          10: '#D8FFDB',
        },
        orange: {
          60: '#E56535',
          40: '#FBB57D',
          20: '#F4E4D4',
        }
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      borderRadius: {
        lg: '24px',
        md: '12px',
        sm: '6px',
      }
    },
  },
  darkMode: "class",
  plugins: [nextui()],
};

export default config;
