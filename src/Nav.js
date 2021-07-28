import React from "react";
import "./styles/Nav.css";

function Nav() {
  return (
    <div className="Nav">
      <div className="nav-links">
        <ul>
          <li>
            <a href="/">Get Prediction</a>
          </li>
          <li>
            <a href="/info">View Graphs</a>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default Nav;
