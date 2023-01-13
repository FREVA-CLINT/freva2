import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import LoginView from "./Login/LoginView";
import { useAppSelector } from "@utils/hooks";

export const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const username = useAppSelector((state) => state.user.username);
  const [open, setOpen] = useState(true);
  const handleClose = () => {
    setOpen(false);
  };

  if (!open && !username) {
    return <Navigate to="/" />;
  }
  if (!username) {
    return <LoginView handleClose={handleClose} isOpen={open} />;
  }

  return children;
};
