const path = require("path");

const webpack = require("webpack");

const mode = "development";

const isDevServer = !!(process.env.npm_lifecycle_event === "dev");

const SERVER_HOST = "127.0.0.1";
const SERVER_PORT = 8080;

let output;
let devServer;
let plugins;
let entry;

if (isDevServer) {
  // override django's STATIC_URL for webpack bundles
  output = {
    publicPath: `http://${SERVER_HOST}:${SERVER_PORT}/assets/bundles/`,
  };

  entry = [`webpack-dev-server/client`, path.resolve("index.tsx")];

  devServer = {
    allowedHosts: "all",
    hot: true,
    client: {
      logging: "verbose",
      webSocketURL: `ws://${SERVER_HOST}:${SERVER_PORT}/ws`,
    },
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  };

  plugins = [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
  ];
}

module.exports = function getDevConfig() {
  return {
    target: "web",
    mode,
    entry,
    output,
    plugins,
    devServer,
  };
};
