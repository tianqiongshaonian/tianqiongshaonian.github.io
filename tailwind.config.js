/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{html,js,css}",
    "./static/**/*.js"
  ],
  safelist: [
    'max-w-[1600px]',
    'max-w-[1440px]',
    'max-w-[240px]',
    'max-w-[200px]',
    'max-w-[180px]',
    'max-w-[160px]',
    'min-w-[200px]',
    'min-w-[240px]',
    'bg-emerald-50',
    'text-emerald-700',
    'border-emerald-200',
    'border-emerald-200/80',
    'bg-emerald-500',
    'text-emerald-600',
    'bg-rose-50',
    'text-rose-600',
    'border-rose-200',
    'border-rose-200/80',
    'bg-amber-50',
    'text-amber-700',
    'border-amber-200/60',
    'text-amber-500',
    'bg-white/15',
    'bg-white/20',
    'text-amber-200',
    'pulse-dot',
    'custom-scrollbar'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    }
  },
  plugins: [],
}
