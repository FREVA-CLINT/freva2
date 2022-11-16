module.exports = {
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint", "react", "import"],
  parserOptions: {
    sourceType: "module",
    requireConfigFile: false,
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: {
      pragma: "React", // Pragma to use, default to "React"
      version: "18.2", // React version, default to the latest React stable release
    },
    "import/resolver": {
      node: {
        extensions: [".js", ".jsx"],
      },
      typescript: {
        alwaysTryTypes: true,
      },
    },
  },
  env: {
    browser: true,
    es6: true,
    node: true,
  },
  ignorePatterns: ["**/*/*.d.ts", "*.d.ts"],
  overrides: [
    {
      files: ["**/*.{ts,tsx}"],
      extends: [
        "plugin:@typescript-eslint/recommended",
        "plugin:@typescript-eslint/recommended-requiring-type-checking",
      ],
      parser: "@typescript-eslint/parser",
      parserOptions: {
        project: "tsconfig.json",
        tsconfigRootDir: __dirname,
      },
      rules: {
        "@typescript-eslint/no-misused-promises": [
          "error",
          {
            checksVoidReturn: false,
          },
        ],
        "@typescript-eslint/no-unused-vars": "error",
        "no-undef": "off",
      },
    },
  ],
  extends: [
    "eslint:recommended",
    "plugin:import/errors",
    "plugin:import/warnings",
    "plugin:react/recommended",
    "prettier",
  ],
};
