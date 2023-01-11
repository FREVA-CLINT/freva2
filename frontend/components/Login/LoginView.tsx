import { AxiosError, AxiosResponse } from "axios";
import React, { ClipboardEvent, FormEvent, useState } from "react";

import { Button, FloatingLabel, Form, Modal } from "react-bootstrap";

import type { TToken } from "@utils/auth/Token";
import { login } from "@utils/auth/authSlice";
import request from "@utils/request";
import { useAppDispatch } from "@utils/hooks";

export default function LoginDialog({
  handleClose,
  isOpen,
}: {
  handleClose: () => void;
  isOpen: boolean;
}) {
  const dispatch = useAppDispatch();
  const [errorMessage, setErrorMessage] = useState("");

  function trimPaste(e: ClipboardEvent<HTMLInputElement>) {
    e.preventDefault();
    const text = e.clipboardData?.getData("Text");
    if (text && e.target) {
      const element = e.target as HTMLInputElement;
      element.value = text.trim();
    }
  }

  function createForm(
    fieldname: string,
    autoComplete: string,
    password = false
  ) {
    return (
      <FloatingLabel
        className="my-4 shadow-sm"
        controlId={"login-" + fieldname}
        label={fieldname}
      >
        <Form.Control
          name={fieldname}
          type={password ? "password" : "text"}
          autoComplete={"login-section " + autoComplete}
          placeholder={fieldname}
          onPaste={trimPaste}
          required
        />
      </FloatingLabel>
    );
  }

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const target = e.target as typeof e.target & {
      username: { value: string };
      password: { value: string };
    };

    request
      .post("/api/token/", {
        username: target.username.value,
        password: target.password.value,
      })
      .then((response: AxiosResponse<TToken>) => {
        dispatch(
          login({ token: response.data, username: target.username.value })
        );
        handleClose();
      })
      .catch((error: AxiosError<{ detail: string }>) => {
        if (error.response) {
          setErrorMessage(error.response.data.detail);
        } else {
          setErrorMessage("No active account found with the given credentials");
        }
      });
  }

  return (
    <>
      <Modal
        show={isOpen}
        onHide={() => {
          handleClose();
          setErrorMessage("");
        }}
        keyboard={false}
      >
        <Modal.Header closeButton>
          <Modal.Title>Sign in</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            {createForm("username", "username")}
            {createForm("password", "current-password", true)}
            <div className="my-2 text-danger">{errorMessage}&nbsp;</div>
            <Button
              className="mb-4 shadow-sm w-100 py-3 fw-bold"
              variant="success"
              type="submit"
              value="Submit"
            >
              SIGN IN
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
}
