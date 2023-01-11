import React from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import { Provider } from "react-redux";

import "./styles/base.scss";

import Header from "./components/Header/Header";
import { Container } from "react-bootstrap";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { store } from "./utils/store";
import WorkflowsPage from "pages/workflows/Workflows";

const App = () => {
  return (
    <Provider store={store}>
      <Header />
      <Container>
        <Outlet />
      </Container>
    </Provider>
  );
};

const router = createBrowserRouter([
  {
    element: <App />,
    path: "/",
    errorElement: <div>Error page</div>,
    children: [
      {
        index: true,
        element: <div>TODO: Content</div>,
      },
      {
        path: "workflows",
        element: (
          <ProtectedRoute>
            <WorkflowsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: "*",
        element: <div>404 not found</div>,
      },
    ],
  },
]);

// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const root = createRoot(document.getElementById("root")!);
root.render(<RouterProvider router={router} />);
