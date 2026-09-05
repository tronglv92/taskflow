/**
 * Compile TaskFlow's Tailwind utility classes during both `npm run dev` and
 * `npm run build`. Without this Vite serves the component class attributes
 * but no corresponding CSS, leaving the Academy service tab unstyled.
 */
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
}
