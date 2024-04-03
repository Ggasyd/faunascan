import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Enregistrement des composants nécessaires pour Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Resultats() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [{
      label: 'Pourcentage',
      data: [], // Nous remplirons ces données avec l'effet ci-dessous
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
      ],
      borderWidth: 1,
    }],
  });

  useEffect(() => {
    fetch('/data.json')
      .then(response => response.json())
      .then(data => {
        setChartData({
          labels: Object.keys(data),
          datasets: [{
            ...chartData.datasets[0],
            data: Object.values(data),
          }],
        });
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, []);

  return (
    <div className="resultat">
      <div className="resultat-body">
        <p>Résultats </p>
        <div style={{ width: '800px', height: '600px' }}>
          <Bar data={chartData} options={{ scales: { y: { beginAtZero: true } } }} />
        </div>
      </div>
    </div>
  );
}

export default Resultats;
