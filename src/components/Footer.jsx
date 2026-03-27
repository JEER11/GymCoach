import React from 'react'
import '../App.css'
import Github from '../assets/github.png';
// Instagram and LinkedIn removed per design

const Footer = () => {
  return (
    <div className="Footer-container">
        <hr/>
        <div className="footer">
            <div className="social-links">
              <img src={Github} alt=""/>
            </div>
        </div>
        <div className="blur blur-f-1"></div>
        <div className="blur blur-f-2"></div>
    </div>
  )
}

export default Footer
