/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f8f5ff",
          100: "#f0e8ff",
          200: "#e3d4fe",
          300: "#cfb8fd",
          400: "#b294fa",
          500: "#9969f8",
          600: "#8246ed",
          700: "#7031d9",
          800: "#5e28b8",
          900: "#4d2295",
          950: "#30145e",
        },
        secondary: {
          50: "#f2f5ff",
          100: "#e6ebfe",
          200: "#d1dafc",
          300: "#b3c2fa",
          400: "#8f9ef6",
          500: "#727cf2",
          600: "#5a5ae8",
          700: "#4846d2",
          800: "#3c3aab",
          900: "#343486",
          950: "#1f1e56",
        },
        accent: {
          50: "#fef2ff",
          100: "#fde6ff",
          200: "#fbcdfe",
          300: "#f9a8fc",
          400: "#f576f5",
          500: "#e847e8",
          600: "#d31fca",
          700: "#b316a6",
          800: "#931588",
          900: "#79196f",
          950: "#500043",
        },
        text: {
          light: "#1a1a2e",
          dark: "#ffffff",
          muted: {
            light: "#4b5563",
            dark: "#d1d5db",
          },
        },
      },
      animation: {
        "pulse-wave": "pulse-wave 1.5s infinite",
        "music-pulse": "musicPulse 1s ease-in-out infinite",
        "fade-in": "fadeIn 0.5s ease-out forwards",
        "slide-in-left": "slideInLeft 0.3s ease-out forwards",
        "slide-in-right": "slideInRight 0.3s ease-out forwards",
        ping: "ping 1s cubic-bezier(0, 0, 0.2, 1) infinite",
        float: "float 3s ease-in-out infinite",
        glow: "glow 2s ease-in-out infinite",
        "appear-once": "appearOnce 0.5s ease-out forwards",
        "loading-pulse":
          "loadingPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        glow: {
          "0%, 100%": { boxShadow: "0 0 10px rgba(139, 92, 246, 0.5)" },
          "50%": { boxShadow: "0 0 20px rgba(139, 92, 246, 0.8)" },
        },
        appearOnce: {
          "0%": { opacity: 0, transform: "translateY(10px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
        fadeIn: {
          "0%": { opacity: 0, transform: "translateY(10px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
        loadingPulse: {
          "0%, 100%": { opacity: 1 },
          "50%": { opacity: 0.7 },
        },
        slideInLeft: {
          "0%": { opacity: 0, transform: "translateX(-20px)" },
          "100%": { opacity: 1, transform: "translateX(0)" },
        },
        slideInRight: {
          "0%": { opacity: 0, transform: "translateX(20px)" },
          "100%": { opacity: 1, transform: "translateX(0)" },
        },
      },
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
        inter: ["Inter", "sans-serif"],
      },
      boxShadow: {
        soft: "0 4px 10px rgba(0, 0, 0, 0.05)",
        "soft-lg": "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
        "inner-soft": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
        glow: "0 0 15px rgba(139, 92, 246, 0.5)",
        "dark-glow": "0 0 15px rgba(168, 85, 247, 0.5)",
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.5rem",
        "3xl": "2rem",
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            maxWidth: "none",
            color: theme("colors.gray.700"),
            a: {
              color: theme("colors.primary.600"),
              "&:hover": {
                color: theme("colors.primary.800"),
              },
            },
          },
        },
        dark: {
          css: {
            color: theme("colors.gray.300"),
            a: {
              color: theme("colors.primary.400"),
              "&:hover": {
                color: theme("colors.primary.300"),
              },
            },
            h1: {
              color: theme("colors.gray.100"),
            },
            h2: {
              color: theme("colors.gray.100"),
            },
            h3: {
              color: theme("colors.gray.100"),
            },
            strong: {
              color: theme("colors.gray.100"),
            },
            code: {
              color: theme("colors.gray.100"),
            },
            blockquote: {
              color: theme("colors.gray.400"),
            },
          },
        },
      }),
    },
  },
  variants: {
    extend: {
      typography: ["dark"],
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
