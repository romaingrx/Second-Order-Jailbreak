/** @type {import('tailwindcss').Config} */
import { nextui } from "@nextui-org/react";
module.exports = {
  content: [
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        "pastel-0": '#BAABDA',
        "pastel-1": '#D6E5FA',
        "pastel-2": '#FFF9F9',
      },
    },
  },
  plugins: [nextui()]
}
