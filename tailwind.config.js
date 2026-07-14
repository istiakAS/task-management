/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", // templates inside root project
    "./**/templates/**/*.html",  //template inside app
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

