import React, { Component } from "react";
import { createRoot } from "react-dom/client";
import RouterComponent from "./Router";
import NOOS from "./NOOS";
import Bonus from "./bonus";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <RouterComponent /> 
      </div>
    );
  }
}

const appDiv = document.getElementById('app');

const root = createRoot(appDiv);
root.render(<App />);
