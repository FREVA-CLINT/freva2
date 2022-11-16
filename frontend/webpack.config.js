const { merge } = require("webpack-merge");

const baseConfig = require("./webpack/webpack.base.config");
const serverConfig = require("./webpack/webpack.devserver.config");
const buildConfig = require("./webpack/webpack.build.config");

let config;
if (process.env.npm_lifecycle_event === "dev") {
  config = merge(baseConfig(), serverConfig(), { node: { __dirname: true } });
} else {
  config = merge(baseConfig(), buildConfig(), { node: { __dirname: true } });
}

module.exports = config;
