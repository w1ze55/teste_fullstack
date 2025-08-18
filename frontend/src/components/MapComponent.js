import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons for different charger types
const createCustomIcon = (type, status) => {
  let color;
  let iconSymbol;

  // Set color based on status
  switch (status) {
    case 'OPERATIONAL':
      color = '#4caf50'; // Green
      break;
    case 'MAINTENANCE':
      color = '#ff9800'; // Orange
      break;
    case 'INACTIVE':
      color = '#f44336'; // Red
      break;
    default:
      color = '#9e9e9e'; // Gray
  }

  // Set icon symbol based on type
  switch (type) {
    case 'AC':
      iconSymbol = '~';
      break;
    case 'DC':
      iconSymbol = '=';
      break;
    case 'BOTH':
      iconSymbol = '≈';
      break;
    default:
      iconSymbol = '⚡';
  }

  return L.divIcon({
    className: 'custom-div-icon',
    html: `
      <div style="
        background-color: ${color};
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 14px;
      ">${iconSymbol}</div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -15]
  });
};

// Component to handle map updates
function MapUpdater({ stations, selectedStation }) {
  const map = useMap();

  useEffect(() => {
    if (selectedStation) {
      map.setView([selectedStation.latitude, selectedStation.longitude], 15);
    } else if (stations.length > 0) {
      const bounds = L.latLngBounds(
        stations.map(station => [station.latitude, station.longitude])
      );
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  }, [map, stations, selectedStation]);

  return null;
}

// Status badge component
function StatusBadge({ status }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'OPERATIONAL':
        return '#4caf50';
      case 'MAINTENANCE':
        return '#ff9800';
      case 'INACTIVE':
        return '#f44336';
      default:
        return '#9e9e9e';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'OPERATIONAL':
        return 'Operacional';
      case 'MAINTENANCE':
        return 'Manutenção';
      case 'INACTIVE':
        return 'Inativo';
      default:
        return status;
    }
  };

  return (
    <span
      style={{
        backgroundColor: getStatusColor(status),
        color: 'white',
        padding: '2px 8px',
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: 'bold'
      }}
    >
      {getStatusText(status)}
    </span>
  );
}

// Type badge component
function TypeBadge({ type }) {
  const getTypeColor = (type) => {
    switch (type) {
      case 'AC':
        return '#2196f3';
      case 'DC':
        return '#9c27b0';
      case 'BOTH':
        return '#ff5722';
      default:
        return '#9e9e9e';
    }
  };

  const getTypeText = (type) => {
    switch (type) {
      case 'AC':
        return 'AC';
      case 'DC':
        return 'DC';
      case 'BOTH':
        return 'AC/DC';
      default:
        return type;
    }
  };

  return (
    <span
      style={{
        backgroundColor: getTypeColor(type),
        color: 'white',
        padding: '2px 8px',
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        marginLeft: '5px'
      }}
    >
      {getTypeText(type)}
    </span>
  );
}

export default function MapComponent({ stations, selectedStation, onStationSelect }) {
  // Center on Brazil
  const center = [-14.235, -51.9253];
  const zoom = 4;

  return (
    <div style={{ height: '100%', width: '100%' }}>
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapUpdater stations={stations} selectedStation={selectedStation} />
        
        {stations.map((station) => (
          <Marker
            key={station.id}
            position={[station.latitude, station.longitude]}
            icon={createCustomIcon(station.charger_type, station.status)}
            eventHandlers={{
              click: () => onStationSelect(station),
            }}
          >
            <Popup>
              <div style={{ minWidth: '250px' }}>
                <h3 style={{ margin: '0 0 10px 0', color: '#1976d2' }}>
                  {station.name}
                </h3>
                
                <div style={{ marginBottom: '8px' }}>
                  <StatusBadge status={station.status} />
                  <TypeBadge type={station.charger_type} />
                </div>
                
                <div style={{ fontSize: '14px', lineHeight: '1.5' }}>
                  <div><strong>📍 Localização:</strong> {station.city}, {station.state}</div>
                  <div><strong>⚡ Potência:</strong> {station.power_kw} kW</div>
                  <div><strong>🚗 Vagas:</strong> {station.num_spots}</div>
                  <div style={{ fontSize: '12px', color: '#666', marginTop: '8px' }}>
                    Lat: {station.latitude.toFixed(4)}, Lng: {station.longitude.toFixed(4)}
                  </div>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      
      {/* Legend */}
      <div
        style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          backgroundColor: 'white',
          padding: '15px',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
          zIndex: 1000,
          fontSize: '12px'
        }}
      >
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>Legenda</div>
        
        <div style={{ marginBottom: '8px' }}>
          <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Status:</div>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2px' }}>
            <div style={{ width: '12px', height: '12px', backgroundColor: '#4caf50', borderRadius: '50%', marginRight: '6px' }}></div>
            Operacional
          </div>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2px' }}>
            <div style={{ width: '12px', height: '12px', backgroundColor: '#ff9800', borderRadius: '50%', marginRight: '6px' }}></div>
            Manutenção
          </div>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2px' }}>
            <div style={{ width: '12px', height: '12px', backgroundColor: '#f44336', borderRadius: '50%', marginRight: '6px' }}></div>
            Inativo
          </div>
        </div>
        
        <div>
          <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Tipo:</div>
          <div style={{ marginBottom: '2px' }}>~ AC</div>
          <div style={{ marginBottom: '2px' }}>= DC</div>
          <div style={{ marginBottom: '2px' }}>≈ AC/DC</div>
        </div>
      </div>
    </div>
  );
}
