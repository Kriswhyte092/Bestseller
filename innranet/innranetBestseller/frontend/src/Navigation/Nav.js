import React, { Component } from "react";

export default class Nav extends Component {
  constructor(props) {
  super(props);
  }
  handleMouseEnter = (event) => {
    event.target.style.color = '#777';
  };
  handleMouseLeave = (event) => {
    event.target.style.color = 'inherit'; 
  };

  render() {
    return (
      <nav style={{
        backgroundColor: '#333',
        display: 'flex',
        color: 'white',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 1rem',
      }}>
        <a href="/" style={{
          color: 'inherit',
          fontSize: '2rem',
          textDecoration: 'none',
        }}>BESTSELLER INNRANET</a>
        <ul style={{
          padding: 0,
          margin: 0,
          display: 'flex',
          gap: '1rem',
          listStyle: 'none',
        }}>
          <li style={{
            textDecoration: 'none',
          }}
          >
            <a href="/NOOS" style={{
              color: 'inherit',
              textDecoration: 'none',
            }}
              onMouseEnter = {this.handleMouseEnter}
              onMouseLeave = {this.handleMouseLeave}
            >NOOS</a>
          </li>
          <li>
            <a href="/Væntanlegt" style={{
              color: 'inherit',
              textDecoration: 'none',
            }}
              onMouseEnter = {this.handleMouseEnter}
              onMouseLeave = {this.handleMouseLeave}
            >Væntanlegt</a>
          </li>
        </ul>
      </nav>
    );
  }
}


