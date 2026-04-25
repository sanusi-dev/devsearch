/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './projects/templates/**/*.html',
    './users/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        main: '#5aa5b9',
        'main-light': '#e6faff',
        sub: '#2d2d39',
        'sub-light': '#51546e',
        'sub-lighter': '#ededfd',
        text: '#737373',
        gray: '#8b8b8b',
        light: '#e5e7eb',
        'light-gray': '#767676',
        bg: '#f8fafd',
        white: '#fffefd',
        'white-light': '#f3f3f3',
        success: '#359e64',
        'success-bg': '#def8e8',
        error: '#fc4b0b',
        'error-bg': '#fff2ee',
      },
      fontFamily: {
        sans: ['Poppins', 'arial', 'helvetica', 'Segoe UI', 'roboto', 'ubuntu', 'sans-serif'],
        mono: ['Fira Code', 'Courier New', 'courier', 'monospace'],
      }
    },
  },
  plugins: [],
}

