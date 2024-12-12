import React, { Component } from "react";
import Nav from "../Navigation/Nav";
import Products from "../Products/Products";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Nav />
        <Products />
        <p>This is the HOME PAGE</p> 
      </div>
    ); 
  }
}
