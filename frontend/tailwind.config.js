/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f3faf7",
          100: "#d7f0e4",
          500: "#2f855a",
          700: "#276749",
          900: "#1c4532",
        },
      },
    },
  },
  plugins: [],
};

