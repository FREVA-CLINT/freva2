import React, { useState, useEffect } from "react";
import TokenService from "@utils/auth/TokenService";
import request from "@utils/request";
import { AxiosError, AxiosResponse } from "axios";
import { Alert } from "react-bootstrap";
type TWorkflow = {
  name: string;
  author: string;
  cwl_version: string;
  created: string;
};

function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<TWorkflow[]>([]);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const username = TokenService.getUsername();
    if (!username) return; // this should not happen as it is a ProtectedRoute
    request
      .get(`api/${username}/workflows`)
      .then((response: AxiosResponse<TWorkflow[]>) => {
        setWorkflows(response.data);
      })
      .catch((error: AxiosError<{ detail: string }>) => {
        if (error.response) {
          setErrorMessage(error.response.data.detail);
        } else {
          setErrorMessage("Unspecified Error");
        }
      });
  }, []);

  return (
    <div>
      {errorMessage && <Alert>{errorMessage}</Alert>}
      {workflows.map((w) => (
        <li key={`${w.created}${w.name}`}>{w.name}</li>
      ))}
    </div>
  );
}

export default WorkflowsPage;
