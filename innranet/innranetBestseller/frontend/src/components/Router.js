import React, { Component } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import NOOS from "./NOOS";
import Bonus from "./bonus";
import HomePage from "./HomePage";


export default class RouterComponent extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Router>
        <Routes>
          <Route exact path="/" element={<HomePage /> } />
          <Route path="/NOOS" element={<NOOS />} />
          <Route path="/bonus" element={<Bonus />} />
        </Routes>
      </Router>
    );
  }
}

  
