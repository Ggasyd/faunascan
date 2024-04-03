import React, { useState, useRef, useEffect } from 'react';
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import "./CSS/Spectrogram.css";
import WaveSurfer from 'wavesurfer.js';
import SpectrogramPlugin from 'wavesurfer.js/dist/plugins/spectrogram.esm';
import axios from 'axios'; // Importez la bibliothèque axios
import Resultats from './Resultats'; // Importez votre composant Resultats

function Spectrogram() {
  const waveformRef = useRef(null);
  const wavesurfer = useRef(null);
  const [isPaused, setIsPaused] = useState(true); // Start with the assumption that it's paused
  const [showResults, setShowResults] = useState(false); // État pour contrôler la visibilité des résultats

  // Function to load the audio file and display the spectrogram
  const loadAndPlayAudio = () => {
    // Only create the Wavesurfer instance if it doesn't exist yet
    if (!wavesurfer.current) {
      wavesurfer.current = WaveSurfer.create({
  container: waveformRef.current,
  waveColor: 'green',
  progressColor: 'white',
  scrollParent: true, // Active le défilement automatique
  plugins: [
    SpectrogramPlugin.create({
      container: ".spectrogram-body",
      labels: true,
      // Assurez-vous que la couleur de fond est définie pour être transparente ou correspondre à votre choix
      waveColor: 'green',
      progressColor: 'white',
      backgroundColor: 'white' // Définissez cette option pour changer le fond
    })
  ]
});

      wavesurfer.current.load('/audio.wav'); // Adjust the path to your audio file

      wavesurfer.current.on('ready', function () {
        wavesurfer.current.play();
      });
    } else {
      wavesurfer.current.play();
    }
  };

  // Gestionnaire de clic pour basculer entre lecture et pause
  const togglePlayPause = () => {
    if (isPaused) {
      loadAndPlayAudio();
    } else {
      wavesurfer.current.pause();
    }
    setIsPaused(!isPaused);
  };

  useEffect(() => {
    // Cleanup function to destroy the Wavesurfer instance when the component unmounts
    return () => wavesurfer.current?.destroy();
  }, []);

  // Fonction pour envoyer la requête POST à FastAPI pour calculer la somme
  const calculateSum = async () => {
    try {
      const response = await axios.post('/sum', {
        a: 5, // Remplacez par la valeur de votre premier entier
        b: 10, // Remplacez par la valeur de votre deuxième entier
      });
      console.log("Résultat de la somme :", response.data.sum);
      setShowResults(true);
    } catch (error) {
      console.error("Erreur lors du calcul de la somme :", error);
    }
  };

  // Fonction pour basculer l'affichage des résultats
  const toggleResults = () => {
    if (wavesurfer.current) {
      wavesurfer.current.destroy(); // Assurez-vous de détruire l'instance de Wavesurfer
    }
    setShowResults(!showResults);
  };
  return (
    <div className="spectrogram">
      {showResults ? (
        <Resultats />
      ) : (
        <>
          <div className="spectrogram-body" ref={waveformRef}></div>
          <div className="spectrogram-controls">
            {isPaused ? (
              <FaIcons.FaPlay className="play-icon" onClick={togglePlayPause} />
            ) : (
              <AiIcons.AiOutlinePause className="pause-icon" onClick={togglePlayPause} />
            )}
          </div>
          <div className="spectrogram-actions">
          <button>Analyser</button>
            <button>Enregistrer</button>
            <button onClick={toggleResults}>Résultats</button>
            
          </div>
        </>
      )}
    </div>
  );
  
}


export default Spectrogram;
