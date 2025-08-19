import React, { useState, useEffect } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Button,
  Drawer,
  IconButton,
  useTheme,
  Snackbar,
  Alert,
  LinearProgress
} from '@mui/material';
import {
  Menu as MenuIcon,
  Logout as LogoutIcon,
  Add as AddIcon
} from '@mui/icons-material';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { API_ENDPOINTS } from '../config/api';
import MapComponent from './MapComponent';
import StationList from './StationList';
import StationForm from './StationForm';
import FilterPanel from './FilterPanel';

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
  const [toast, setToast] = useState({
    open: false,
    message: '',
    severity: 'info',
    progress: 0
  });
  const [userPermissions, setUserPermissions] = useState({
    can_manage_stations: false,
    is_admin: false
  });

  const { user, logout } = useAuth();
  const theme = useTheme();
  
  useEffect(() => {
    fetchStations();
    fetchUserPermissions();
  }, [filters, pagination.page]);

  const fetchUserPermissions = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await axios.get(API_ENDPOINTS.PERMISSIONS, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setUserPermissions(response.data.permissions);
      }
    } catch (err) {
      console.error('Error fetching permissions:', err);
    }
  };

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

      const response = await axios.get(`${API_ENDPOINTS.STATIONS}?${params}`);
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
    if (!userPermissions.can_manage_stations) {
      showToast(
        '🚫 Acesso negado! Apenas administradores podem criar/editar estações.',
        'error',
        5000
      );
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      if (editingStation) {
        await axios.put(API_ENDPOINTS.STATION_BY_ID(editingStation.id), stationData, { headers });
        showToast('✅ Estação atualizada com sucesso!', 'success', 3000);
      } else {
        await axios.post(API_ENDPOINTS.STATIONS, stationData, { headers });
        showToast('✅ Estação criada com sucesso!', 'success', 3000);
      }
      
      await fetchStations();
      setShowForm(false);
      setEditingStation(null);
    } catch (err) {
      console.error('Error saving station:', err);
      if (err.response?.status === 403) {
        showToast(
          '🚫 Acesso negado! Apenas administradores podem gerenciar estações.',
          'error',
          5000
        );
      } else {
        throw new Error(err.response?.data?.message || 'Failed to save station');
      }
    }
  };

  const showToast = (message, severity = 'info', duration = 5000) => {
    setToast({
      open: true,
      message,
      severity,
      progress: 0
    });

    // Animar barra de progresso
    let progress = 0;
    const interval = setInterval(() => {
      progress += (100 / duration) * 100; // Atualiza a cada 100ms
      setToast(prev => ({ ...prev, progress }));
      
      if (progress >= 100) {
        clearInterval(interval);
        setToast(prev => ({ ...prev, open: false }));
      }
    }, 100);
  };

  const handleStationDelete = async (stationId) => {
    // Verificar se o usuário tem permissão para deletar
    if (!userPermissions.can_manage_stations) {
      showToast(
        '🚫 Acesso negado! Apenas administradores podem excluir estações de carregamento.',
        'error',
        5000
      );
      return;
    }

    try {
      await axios.delete(API_ENDPOINTS.STATION_BY_ID(stationId), {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      await fetchStations();
      showToast('✅ Estação excluída com sucesso!', 'success', 3000);
    } catch (err) {
      console.error('Error deleting station:', err);
      if (err.response?.status === 403) {
        showToast(
          '🚫 Acesso negado! Apenas administradores podem excluir estações.',
          'error',
          5000
        );
      } else {
        showToast('❌ Erro ao excluir estação. Tente novamente.', 'error', 4000);
      }
    }
  };

  const handleStationEdit = (station) => {
    if (!userPermissions.can_manage_stations) {
      showToast(
        '🚫 Acesso negado! Apenas administradores podem editar estações.',
        'error',
        5000
      );
      return;
    }
    setEditingStation(station);
    setShowForm(true);
  };

  const handleAddStation = () => {
    if (!userPermissions.can_manage_stations) {
      showToast(
        '🚫 Acesso negado! Apenas administradores podem adicionar estações.',
        'error',
        5000
      );
      return;
    }
    setEditingStation(null);
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
          onClick={handleAddStation}
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
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', mr: 2 }}>
            <Typography variant="body2">
              Welcome, {user?.username}
            </Typography>
            {user?.role && (
              <Typography variant="caption" sx={{ 
                color: user.role === 'admin' ? '#ffeb3b' : '#90caf9',
                fontWeight: 'bold',
                textTransform: 'uppercase'
              }}>
                {user.role === 'admin' ? '👑 Admin' : '👤 User'}
              </Typography>
            )}
          </Box>
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

      {/* Toast com temporizador */}
      <Snackbar
        open={toast.open}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        sx={{ 
          '& .MuiSnackbarContent-root': {
            minWidth: '400px',
            maxWidth: '600px'
          }
        }}
      >
        <Alert 
          severity={toast.severity}
          variant="filled"
          sx={{
            width: '100%',
            fontSize: '1rem',
            '& .MuiAlert-message': {
              width: '100%'
            }
          }}
        >
          <Box>
            <Typography variant="body1" sx={{ mb: 1 }}>
              {toast.message}
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={toast.progress}
              sx={{
                backgroundColor: 'rgba(255, 255, 255, 0.3)',
                '& .MuiLinearProgress-bar': {
                  backgroundColor: 'rgba(255, 255, 255, 0.8)'
                }
              }}
            />
          </Box>
        </Alert>
      </Snackbar>
    </Box>
  );
}
