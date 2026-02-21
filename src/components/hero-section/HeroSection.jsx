import React from 'react'
import Header from '../header/Header'
// hero images removed per design
import './HeroSection.css'

import {motion} from 'framer-motion'

const HeroSection = () => {

    const transition = {type: 'spring', duration: 3}
    const mobile = window.innerWidth <= 768 ? true : false;

    return (
        <div className="hero" id="home">
            <div className="blur hero-blur"></div>
            <div className="left-h">
                <Header />
                <div className="hero-text">
                    <div>
                        <span className="main-title">Gymnastics Coach</span>
                    </div>
                    <div className="hero-subtext">
                        <span>Use your webcam to start the ML-based evaluation and receive feedback.</span>
                    </div>
                </div>
                
            </div>

            <div className="right-h">
                {/* Hero images removed; keep layout minimal for ML app */}
                
            </div>
        </div>
  )
}

export default HeroSection