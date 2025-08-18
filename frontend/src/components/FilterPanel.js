import React from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
  Chip,
  Stack
} from '@mui/material';
import { FilterList as FilterIcon } from '@mui/icons-material';

const CHARGER_TYPES = [
  { value: 'AC', label: 'AC' },
  { value: 'DC', label: 'DC' },
  { value: 'BOTH', label: 'Both AC/DC' }
];

const STATION_STATUS = [
  { value: 'OPERATIONAL', label: 'Operational' },
  { value: 'MAINTENANCE', label: 'Maintenance' },
  { value: 'INACTIVE', label: 'Inactive' }
];

const BRAZILIAN_STATES = [
  { value: 'AC', label: 'Acre' },
  { value: 'AL', label: 'Alagoas' },
  { value: 'AP', label: 'Amapá' },
  { value: 'AM', label: 'Amazonas' },
  { value: 'BA', label: 'Bahia' },
  { value: 'CE', label: 'Ceará' },
  { value: 'DF', label: 'Distrito Federal' },
  { value: 'ES', label: 'Espírito Santo' },
  { value: 'GO', label: 'Goiás' },
  { value: 'MA', label: 'Maranhão' },
  { value: 'MT', label: 'Mato Grosso' },
  { value: 'MS', label: 'Mato Grosso do Sul' },
  { value: 'MG', label: 'Minas Gerais' },
  { value: 'PA', label: 'Pará' },
  { value: 'PB', label: 'Paraíba' },
  { value: 'PR', label: 'Paraná' },
  { value: 'PE', label: 'Pernambuco' },
  { value: 'PI', label: 'Piauí' },
  { value: 'RJ', label: 'Rio de Janeiro' },
  { value: 'RN', label: 'Rio Grande do Norte' },
  { value: 'RS', label: 'Rio Grande do Sul' },
  { value: 'RO', label: 'Rondônia' },
  { value: 'RR', label: 'Roraima' },
  { value: 'SC', label: 'Santa Catarina' },
  { value: 'SP', label: 'São Paulo' },
  { value: 'SE', label: 'Sergipe' },
  { value: 'TO', label: 'Tocantins' }
];

export default function FilterPanel({ filters, onFilterChange }) {
  const handleFilterChange = (filterType, value) => {
    onFilterChange({
      ...filters,
      [filterType]: value
    });
  };

  const clearAllFilters = () => {
    onFilterChange({
      type: '',
      status: '',
      state: ''
    });
  };

  const activeFiltersCount = Object.values(filters).filter(value => value !== '').length;

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <FilterIcon sx={{ mr: 1, color: 'text.secondary' }} />
        <Typography variant="subtitle2" color="text.secondary">
          Filters
        </Typography>
        {activeFiltersCount > 0 && (
          <Chip 
            label={activeFiltersCount} 
            size="small" 
            color="primary" 
            sx={{ ml: 1 }}
          />
        )}
      </Box>

      <Stack spacing={2}>
        <FormControl fullWidth size="small">
          <InputLabel>Charger Type</InputLabel>
          <Select
            value={filters.type}
            label="Charger Type"
            onChange={(e) => handleFilterChange('type', e.target.value)}
          >
            <MenuItem value="">All Types</MenuItem>
            {CHARGER_TYPES.map((type) => (
              <MenuItem key={type.value} value={type.value}>
                {type.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth size="small">
          <InputLabel>Status</InputLabel>
          <Select
            value={filters.status}
            label="Status"
            onChange={(e) => handleFilterChange('status', e.target.value)}
          >
            <MenuItem value="">All Status</MenuItem>
            {STATION_STATUS.map((status) => (
              <MenuItem key={status.value} value={status.value}>
                {status.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth size="small">
          <InputLabel>State</InputLabel>
          <Select
            value={filters.state}
            label="State"
            onChange={(e) => handleFilterChange('state', e.target.value)}
          >
            <MenuItem value="">All States</MenuItem>
            {BRAZILIAN_STATES.map((state) => (
              <MenuItem key={state.value} value={state.value}>
                {state.label} ({state.value})
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {activeFiltersCount > 0 && (
          <Box sx={{ mt: 1 }}>
            <Typography 
              variant="caption" 
              color="primary" 
              sx={{ cursor: 'pointer', textDecoration: 'underline' }}
              onClick={clearAllFilters}
            >
              Clear all filters
            </Typography>
          </Box>
        )}
      </Stack>
    </Box>
  );
}
