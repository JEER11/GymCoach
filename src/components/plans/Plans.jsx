import React from 'react'
import './Plans.css'

const Plans = () => {
  return (
    <div className="plans-container">
        <div className="blur plans-blur-1"></div>
        <div className="blur plans-blur-2"></div>
        <div 
            className="programs-header"
            style={{gap: '2rem'}}
        >
            <span className="stroke-text">Training Plans Removed</span>
            <span>Webcam-based ML evaluation enabled</span>
        </div>
    </div>
  )
}

export default Plans