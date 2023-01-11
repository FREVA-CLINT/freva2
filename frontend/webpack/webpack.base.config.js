// Generated using webpack-cli https://github.com/webpack/webpack-cli

const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const LoadablePlugin = require("@loadable/webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const ESLintPlugin = require("eslint-webpack-plugin");
const TsconfigPathsPlugin = require("tsconfig-paths-webpack-plugin");
const isProduction = process.env.NODE_ENV == "production";

const ROOT_PATH = path.resolve(__dirname, "..");

const config = {
  devtool: "source-map",
  plugins: [
    new BundleTracker({
      filename: path.resolve(ROOT_PATH, "..", "webpack-stats.json"),
    }),
    new MiniCssExtractPlugin({ filename: "[name].css" }),
    new LoadablePlugin(),
    new ESLintPlugin({
      extensions: ["js", "jsx", "ts", "tsx"],
    }),
  ],
  optimization: {
    splitChunks: {},
  },
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/i,
        loader: "ts-loader",
        exclude: ["/node_modules/"],
      },
      {
        test: /\.s[ac]ss|.css$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: "css-loader",
            options: {
              importLoaders: 1,
            },
          },
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                config: ROOT_PATH + "/postcss.config.js",
              },
            },
          },
          {
            loader: "sass-loader",
            options: {
              implementation: require("sass"),
            },
          },
        ],
      },
      {
        test: /\.(eot|svg|ttf|woff|woff2|png|jpg|gif)$/i,
        type: "asset",
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".jsx", ".js"],
    plugins: [
      new TsconfigPathsPlugin({
        configFile: path.resolve(ROOT_PATH, "tsconfig.json"),
        extensions: [".ts", ".js", ".tsx"],
      }),
    ],
  },
};

module.exports = function getBaseConfig() {
  if (isProduction) {
    config.mode = "production";
  } else {
    config.mode = "development";
  }
  return config;
};
