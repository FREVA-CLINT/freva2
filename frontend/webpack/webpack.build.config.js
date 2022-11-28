const path = require("path");

const ROOT_PATH = path.resolve(__dirname, "..");
const PUBLIC_PATH = "/static/frontend/";

const entry = path.resolve(ROOT_PATH, "index.tsx");

const output = {
  filename: "[name].bundle.js",
  chunkFilename: "[id].app.[contenthash].js",
  // The folder where we collect our frontend-related stuff
  path: path.resolve(ROOT_PATH, "..", "dist", "frontend"),
  // The route where we expect our stuff on the webserver
  publicPath: PUBLIC_PATH,
};

module.exports = function getProdConfig() {
  return {
    entry,
    output,
  };
};
