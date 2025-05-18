/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: "class",
    content: [
      "./app/**/*.{js,ts,jsx,tsx}",
      "./pages/**/*.{js,ts,jsx,tsx}",
      "./components/**/*.{js,ts,jsx,tsx}"
    ],
    theme: {
      extend: {
        colors: {
          surface: "#121212",
          "surface-light": "#1E1E1E",
          primary: "#9D50BB",
          secondary: "#39FF14",
          accent: "#F59E0B",
          "on-surface": "#E0E0E0",
        },
        fontFamily: {
          sans: ["Roboto", "sans-serif"],
          display: ["Cinzel", "serif"]
        },
      },
    },
    plugins: [],
  };