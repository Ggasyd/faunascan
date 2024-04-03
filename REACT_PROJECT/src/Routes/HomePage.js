import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import './CSS/HomePage.css';
import Spectrogram from "../Components/Spectrogram";
import Navbar from "../Components/Navbar";
import { SidebarData } from "../Components/SidebarData";

export default function HomePage() {
    const [showSpectrogram, setShowSpectrogram] = useState(false);

   

    const handleGetStartedClick = () => {
        setShowSpectrogram(true);
    };

    const resetToHomePage = () => {
        setShowSpectrogram(false);
    };
    return (
        <div className="container">
            <Navbar onHomeClick={resetToHomePage} />
            {!showSpectrogram && (
                <div className="content">
                    <img src="chat.png" className="bg-image" alt="Chat" />
                    <h1>Discover animals with their sounds</h1>
                    <p>Play with it to discover animals you never knew existed!</p>
                    <button onClick={handleGetStartedClick} id="getStarted" className="rounded-button">Get Started</button>
                </div>
            )}
            
            {showSpectrogram && <Spectrogram />}
        </div>
    );
}

