import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

function Navigaton() {
  return (
    <div>
      <Navbar bg="dark" variant="dark" expand="lg" collapseOnSelect>
        <Container>
          <LinkContainer to="/">
            <Navbar.Brand>LMS</Navbar.Brand>
          </LinkContainer>
        </Container>
      </Navbar>
    </div>
  );
}

export default Navigaton;
