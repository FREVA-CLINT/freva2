import React from "react";
import { Container, Nav, Navbar, NavLink } from "react-bootstrap";
import { Link, useLocation } from "react-router-dom";

import LoginButton from "../Login/LoginButton";
import "./Header.scss";

type TMenuElement = {
  title: string;
  url: string;
};

export default function Header(): JSX.Element {
  const location = useLocation();

  function getMenu() {
    const menuText = document.getElementById("freva_menu")?.textContent;
    if (!menuText) {
      return [];
    }
    const menuElements = JSON.parse(menuText) as TMenuElement[];
    return menuElements;
  }

  const menuElements = getMenu();

  return (
    <header className="shadow">
      <Container className="logo-header d-flex justify-content-between py-2">
        <div>
          <img
            className="logo-left"
            src="/static/img/logo.png"
            alt="project logo"
          />
        </div>
        <div className="d-none d-sm-block">
          <img
            className="logo-right"
            src="/static/img/by_freva_transparent.png"
            alt="by freva"
          />
        </div>
      </Container>
      <Navbar bg="primary" expand="lg">
        <Container className="d-flex justify-content-start">
          <Navbar.Toggle className="ms-2" />
          <Navbar.Collapse>
            <Nav activeKey={location.pathname}>
              {menuElements.map((item) => (
                <NavLink
                  key={item.title}
                  as={Link}
                  eventKey={item.url}
                  to={item.url}
                >
                  {item.title}
                </NavLink>
              ))}
            </Nav>
          </Navbar.Collapse>
          <LoginButton />
        </Container>
      </Navbar>
    </header>
  );
}
