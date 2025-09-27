/** @type      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
          50: 'oklch(97.1% 0.013 17.38)',
          100: 'oklch(93.6% 0.032 17.717)', 
          200: 'oklch(88.5% 0.062 18.334)',
          300: 'oklch(80.8% 0.114 19.571)',
          400: 'oklch(70.4% 0.191 22.216)',
          500: 'oklch(62.3% 0.214 259.815)',
          600: 'oklch(54.6% 0.245 262.881)',
          700: 'oklch(48.8% 0.243 264.376)',
          800: 'oklch(42.4% 0.199 265.638)',
          900: 'oklch(37.9% 0.146 265.522)',
          950: 'oklch(28.2% 0.091 267.935)',
        },
        secondary: {indcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: 'oklch(97.1% 0.013 17.38)',
          100: 'oklch(93.6% 0.032 17.717)',
          200: 'oklch(88.5% 0.062 18.334)',
          300: 'oklch(80.8% 0.114 19.571)',
          400: 'oklch(70.4% 0.191 22.216)',
          500: 'oklch(62.3% 0.214 259.815)',
          600: 'oklch(54.6% 0.245 262.881)',
          700: 'oklch(48.8% 0.243 264.376)',
          800: 'oklch(42.4% 0.199 265.638)',
          900: 'oklch(37.9% 0.146 265.522)',
          950: 'oklch(28.2% 0.091 267.935)',
        },
        secondary: {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15',
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
        },
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
      },
      borderColor: {
        DEFAULT: "hsl(var(--border))",
        border: "hsl(var(--border))",
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        '2xl': '1rem',
      },
      boxShadow: {
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
      },
      gridTemplateColumns: {
        '12': 'repeat(12, minmax(0, 1fr))',
      },
      maxWidth: {
        '1440': '1440px',
      },
    },
  },
  plugins: [],
}
