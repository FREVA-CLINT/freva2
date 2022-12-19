import React, { useEffect, useState } from "react";

import { Button } from "react-bootstrap";
import { logout, setUsername } from "@utils/auth/authSlice";
import { useAppDispatch, useAppSelector } from "@utils/hooks";
import TokenService from "@utils/auth/TokenService";

import LoginView from "./LoginView";

export default function LoginDialog() {
  const [show, setShow] = useState(false);
  const username = useAppSelector((state) => state.user.username);
  const dispatch = useAppDispatch();
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  // User has logged of in another tab, remove the remaining user info in this tab
  useEffect(() => {
    if (!TokenService.getUsername() && username) {
      dispatch(logout());
    } else if (TokenService.getUsername() && !username) {
      dispatch(setUsername());
    }
  });

  return (
    <>
      {username ? (
        <Button
          variant="primary"
          onClick={() => {
            dispatch(logout());
          }}
        >
          {username}
        </Button>
      ) : (
        <Button variant="primary" onClick={handleShow}>
          Login
        </Button>
      )}

      <LoginView handleClose={handleClose} isOpen={show} />
    </>
  );
}
