import { render } from "@testing-library/react";
import React, { useState, useEffect } from "react";
import "./styles/Nav.css";
import "./styles/Styles.css";

function Nav() {
  return (
    <div className="Nav">
      <div className="title">
        <h1>🍻 Beer Predictor</h1>
      </div>
      <div className="nav-links">
        <ul>
          <li>
            <a href="/">Predictor</a>
          </li>
          <li>
            <a href="/info">Graphs & Info</a>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default Nav;
