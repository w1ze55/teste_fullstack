import React, { useState, useEffect } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Button,
  Drawer,
  IconButton,
  useTheme
} from '@mui/material';
import {
  Menu as MenuIcon,
  Logout as LogoutIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import MapComponent from './MapComponent';
import StationList from './StationList';
import StationForm from './StationForm';
import FilterPanel from './FilterPanel';
import axios from 'axios';

const DRAWER_WIDTH = 400;

export default function Dashboard() {
  const [, setStations] = useState([]);
  const [filteredStations, setFilteredStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedStation, setSelectedStation] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingStation, setEditingStation] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [filters, setFilters] = useState({
    type: '',
    status: '',
    state: ''
  });
  const [pagination, setPagination] = useState({
    page: 1,
    totalPages: 1,
    total: 0
  });

  const { user, logout } = useAuth();
  const theme = useTheme();
  useEffect(() => {
    fetchStations();
  }, [filters, pagination.page]); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchStations = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        page: pagination.page,
        per_page: 50
      });

      if (filters.type) params.append('type', filters.type);
      if (filters.status) params.append('status', filters.status);
      if (filters.state) params.append('state', filters.state);

      const response = await axios.get(`http://localhost:5000/cargas?${params}`);
      const data = response.data;
      
      setStations(data.stations);
      setFilteredStations(data.stations);
      setPagination({
        page: data.current_page,
        totalPages: data.pages,
        total: data.total
      });
    } catch (err) {
      setError('Failed to fetch charging stations');
      console.error('Error fetching stations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStationSave = async (stationData) => {
    try {
      if (editingStation) {
        await axios.put(`http://localhost:5000/cargas/${editingStation.id}`, stationData);
      } else {
        await axios.post('http://localhost:5000/cargas', stationData);
      }
      
      await fetchStations();
      setShowForm(false);
      setEditingStation(null);
    } catch (err) {
      console.error('Error saving station:', err);
      throw new Error(err.response?.data?.message || 'Failed to save station');
    }
  };

  const handleStationDelete = async (stationId) => {
    try {
      await axios.delete(`http://localhost:5000/cargas/${stationId}`);
      await fetchStations();
    } catch (err) {
      console.error('Error deleting station:', err);
      setError('Failed to delete station');
    }
  };

  const handleStationEdit = (station) => {
    setEditingStation(station);
    setShowForm(true);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    logout();
  };

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h6" gutterBottom>
          Charging Stations
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          fullWidth
          onClick={() => {
            setEditingStation(null);
            setShowForm(true);
          }}
          sx={{ mb: 2 }}
        >
          Add Station
        </Button>
        <FilterPanel filters={filters} onFilterChange={handleFilterChange} />
      </Box>
      
      <Box sx={{ flex: 1, overflow: 'hidden' }}>
        <StationList
          stations={filteredStations}
          loading={loading}
          error={error}
          selectedStation={selectedStation}
          onStationSelect={setSelectedStation}
          onStationEdit={handleStationEdit}
          onStationDelete={handleStationDelete}
          pagination={pagination}
          onPageChange={(page) => setPagination(prev => ({ ...prev, page }))}
        />
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${DRAWER_WIDTH}px)` },
          ml: { md: `${DRAWER_WIDTH}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            ⚡ EV Charging Stations Dashboard
          </Typography>
          <Typography variant="body2" sx={{ mr: 2 }}>
            Welcome, {user?.username}
          </Typography>
          <Button color="inherit" onClick={handleLogout} startIcon={<LogoutIcon />}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { md: DRAWER_WIDTH }, flexShrink: { md: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DRAWER_WIDTH },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DRAWER_WIDTH },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: { md: `calc(100% - ${DRAWER_WIDTH}px)` },
          height: '100vh',
          overflow: 'hidden'
        }}
      >
        <Toolbar />
        <Box sx={{ height: 'calc(100vh - 64px)' }}>
          <MapComponent
            stations={filteredStations}
            selectedStation={selectedStation}
            onStationSelect={setSelectedStation}
          />
        </Box>
      </Box>

      <StationForm
        open={showForm}
        onClose={() => {
          setShowForm(false);
          setEditingStation(null);
        }}
        onSave={handleStationSave}
        station={editingStation}
      />
    </Box>
  );
}
