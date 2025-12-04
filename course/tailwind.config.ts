import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "bom-black": "#0C0C0C",
        "warm-white": "#FAF9F7",
        "paper-white": "#FFFFFF",
        "slate-grey": "#2E2E2E",
        "steel-grey": "#5A5A5A",
        "silver-mist": "#E8E6E3",
        "stone-blue": "#6B8EA3",
        "sage": "#9BA88A",
      },
      fontFamily: {
        heading: ["Michroma", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
