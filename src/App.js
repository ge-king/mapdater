import { NextUIProvider, Navbar,NavbarBrand, NavbarContent, NavbarItem, Link, Button, Spacer } from '@nextui-org/react';
import {Card, CardBody} from "@nextui-org/react";
import './App.css'
import React, {useRef, useState, useEffect } from 'react';
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax

mapboxgl.accessToken = 'pk.eyJ1IjoiZ2VvcnoiLCJhIjoiY2xwMGJ4cDhiMDl2dzJwbmxsMG81bWFlYyJ9.KBGCIDamvcpo74WyGU3NVQ'; 


const App = () => {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [lng, setLng] = useState(-70.9);
  const [lat, setLat] = useState(42.35);
  const [zoom, setZoom] = useState(9);
  const headerRef = useRef(null);
  const footerRef = useRef(null);


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
    if (map.current) return; // initialize map only once
    map.current = new mapboxgl.Map({
    container: mapContainer.current,
    style: 'mapbox://styles/georz/clp0d043500i201qjfixs7wyu',
    center: [lng, lat],
    projection: 'globe',
    zoom: 1.5
    });
    });


    return (
      <NextUIProvider>
        <div className="container">
        <header className="header">
          <h1>MAPDATE</h1>
        </header>
          <div ref={mapContainer} className="map-container" />
          <Card className="centered-card" isBlurred='true'>
          <CardBody className="card-body">
            <p className="card-text">Welcome to MapDate. Are you ready to answer some questions to figure out exactly when your map was made?</p>
            <Spacer y={5} />
            <Button fullWidth='false' variant="ghost" color="success" className="button-go">Go</Button>
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
