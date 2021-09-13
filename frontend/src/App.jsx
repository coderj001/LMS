import React from "react";
import { LoginPage, RegisterPage } from "./Pages";
import { Navbar } from "./components";

function App() {
  return (
    <div className="App">
      <Navbar />
      <LoginPage />
      <RegisterPage />
    </div>
  );
}

export default App;
