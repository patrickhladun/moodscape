const gulp = require("gulp");
const sass = require("gulp-sass")(require("sass"));
const postcss = require("gulp-postcss");
const autoprefixer = require("autoprefixer");
const tailwindcss = require("tailwindcss");
const browserSync = require("browser-sync").create();

const paths = {
  styles: {
    src: "src/styles/**/*.scss", // Watch all SCSS files
    entry: "src/styles/style.scss", // Entry point for the styles
    dest: "static/css/",
  },
  html: {
    src: "./**/templates/**/*.html",
  },
  py: {
    src: "./**/*.py",
  },
};

// Compile SCSS, add Tailwind CSS and Autoprefixer, and output to the destination folder
function styles() {
  return gulp
    .src(paths.styles.entry) // Only compile the main entry SCSS file
    .pipe(sass().on("error", sass.logError))
    .pipe(postcss([tailwindcss, autoprefixer]))
    .pipe(gulp.dest(paths.styles.dest))
    .pipe(browserSync.stream()); // Stream changes to BrowserSync
}

// Initialize BrowserSync and set up the proxy server
function serve() {
  browserSync.init({
    proxy: "127.0.0.1:8000", // Proxy server to 127.0.0.1:8000
    port: 3000, // Local server will run on localhost:3000
    open: false, // Prevents BrowserSync from automatically opening the browser
  });

  gulp.watch(paths.styles.src, styles);
  gulp
    .watch(paths.py.src)
    .on("change", gulp.series(styles, browserSync.reload));
  gulp
    .watch(paths.html.src)
    .on("change", gulp.series(styles, browserSync.reload));
}
const build = gulp.series(styles, serve);

exports.styles = styles;
exports.serve = serve;
exports.build = build;
exports.default = build;
