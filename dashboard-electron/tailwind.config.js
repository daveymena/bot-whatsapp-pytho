/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        whatsapp: {
          light: '#25d366',
          DEFAULT: '#128c7e',
          dark: '#075e54'
        }
      }
    },
  },
  plugins: [],
}
