import { NextUIProvider, Navbar,NavbarBrand, NavbarContent, NavbarItem, Link, Button, Spacer } from "@nextui-org/react";
import {Card, CardBody} from "@nextui-org/react";
import './App.css'
import axios from "axios";
import React, {useRef, useState, useEffect } from 'react';
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';

mapboxgl.accessToken = 'pk.eyJ1IjoiZ2VvcnoiLCJhIjoiY2xwMGJ4cDhiMDl2dzJwbmxsMG81bWFlYyJ9.KBGCIDamvcpo74WyGU3NVQ'; 


const App = () => {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [lng, setLng] = useState(-70.9);
  const [lat, setLat] = useState(42.35);
  const [zoom, setZoom] = useState(2);
  const [currentQuestionId, setCurrentQuestionId] = useState("0");
  const [questionData, setQuestionData] =useState({ text: 'Loading question...', questions: {} });
  const headerRef = useRef(null);
  const footerRef = useRef(null);
  const [darkMode, setDarkMode] = useState(false);
  const toggleSpin = () => {
    setIsSpinning(!isSpinning);
  };
  const [isSpinning, setIsSpinning] = useState(true);
  const secondsPerRevolution = 120;
  const maxSpinZoom = 5;
  const slowSpinZoom = 3;
  const darkStyle =  'mapbox://styles/georz/clp1avglo01ej01o4dwy2bzgw';
const lightStyle = 'mapbox://styles/georz/clp0d043500i201qjfixs7wyu'; // Replace with your dark mode style URL

const getQuestion = (questionId) => {
  axios.get(`https://mapdate-04c9ad419d4c.herokuapp.com/question/${questionId}`)
    .then(response => {
      setQuestionData(response.data);
      setCurrentQuestionId(questionId);
    })
    .catch(error => console.error('Error fetching data:', error));
};

const handleAnswerButtonClick = (answerKey) => {
  const nextQuestionId = questionData.questions[answerKey];
  getQuestion(nextQuestionId);
};

useEffect(() => {
  getQuestion(currentQuestionId); // Fetch initial question on component mount
}, [currentQuestionId]);


  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };


  const adjustMapHeight = () => {
    const headerHeight = headerRef.current?.offsetHeight || 0;
    const footerHeight = footerRef.current?.offsetHeight || 0;
    const windowHeight = window.innerHeight;
    const mapHeight = windowHeight - headerHeight - footerHeight;
    if (mapContainer.current) {
      mapContainer.current.style.height = `${mapHeight}px`;
    }
  };

  useEffect(() => {
    if (map.current) return; // Initialize map only once
  
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: darkMode ? darkStyle : lightStyle,
      center: [lng, lat],
      projection: 'globe',
      zoom: zoom
    });

    map.current.dragPan.disable();
  
    map.current.on('load', () => {
      const spinGlobe = () => {
        if (!isSpinning || !map.current) return;
  
        const zoom = map.current.getZoom();
        if (zoom < maxSpinZoom) {
          let distancePerSecond = 360 / secondsPerRevolution;
          if (zoom > slowSpinZoom) {
            const zoomDif = (maxSpinZoom - zoom) / (maxSpinZoom - slowSpinZoom);
            distancePerSecond *= zoomDif;
          }
          const center = map.current.getCenter();
          center.lng = (center.lng - distancePerSecond) % 360;
          map.current.easeTo({ center, duration: 1000, easing: (n) => n });
        }
      };
  
      const spinInterval = setInterval(spinGlobe, 1000);
      

      


      return () => {
        clearInterval(spinInterval);
      };
    });
  }, [isSpinning, darkMode, darkStyle, lightStyle, lng, lat, zoom]);

  useEffect(() => {
    if (map.current) {
      map.current.setStyle(darkMode ? darkStyle : lightStyle);
    }
  }, [darkMode]);

  useEffect(() => {
    axios.get(`localhost:5000/question/${currentQuestionId}`) // Ensure correct protocol and port
      .then(response => {
        setQuestionData(response.data);
  
        // Check if map is initialized and question has valid latlng data
        if (map.current && response.data.latlng && response.data.latlng.length === 2) {
          const [latitude, longitude] = response.data.latlng;
          map.current.flyTo({
            center: [longitude, latitude],
            zoom: 3
          });
        }
      })
      .catch(error => console.error('Error fetching data:', error));
  }, [currentQuestionId]); 
  


  return (
    <NextUIProvider>
      <div className={`${darkMode ? 'dark' : 'light'} container`}>
        <header className="header">
          <h1>MAPDATE</h1>
          <Button isIconOnly onClick={toggleDarkMode}>
            {darkMode ? 
              <LightModeIcon/> : // Icon for light mode
              <DarkModeIcon/>    // Icon for dark mode
            }
          </Button>
        </header>
        <div ref={mapContainer} className="map-container" />
        <Card className="centered-card" isBlurred='true'>
        <CardBody className="card-body">
          <p className="card-text">{questionData.text}</p>
          <Spacer y={5} />
          <div className="button-group">
          {questionData.questions && Object.keys(questionData.questions).map((answerKey) => (
              <Button
                key={answerKey}
                fullWidth={false}
                variant="ghost"
                color={answerKey === 'no' ? 'error' : 'success'}
                className={`button-${answerKey}`}
                onClick={() => handleAnswerButtonClick(answerKey)}
              >
                {answerKey.charAt(0).toUpperCase() + answerKey.slice(1)}
              </Button>
            ))}
          </div>
        </CardBody>
        </Card>
        <footer>
          Made by George
        </footer>
      </div>
    </NextUIProvider>
  );
  
  };

export default App;