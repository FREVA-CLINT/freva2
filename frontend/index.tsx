import React from "react";
import { createRoot } from "react-dom/client";
import Header from "./components/Header/Header";

const root = createRoot(document.getElementById("root")!);
root.render(
  <h1>
    <Header />
    Hello, world!
  </h1>
);
