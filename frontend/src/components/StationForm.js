import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Alert,
  Box,
  Typography
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';

// Brazilian states
const BRAZILIAN_STATES = [
  { code: 'AC', name: 'Acre' },
  { code: 'AL', name: 'Alagoas' },
  { code: 'AP', name: 'Amapá' },
  { code: 'AM', name: 'Amazonas' },
  { code: 'BA', name: 'Bahia' },
  { code: 'CE', name: 'Ceará' },
  { code: 'DF', name: 'Distrito Federal' },
  { code: 'ES', name: 'Espírito Santo' },
  { code: 'GO', name: 'Goiás' },
  { code: 'MA', name: 'Maranhão' },
  { code: 'MT', name: 'Mato Grosso' },
  { code: 'MS', name: 'Mato Grosso do Sul' },
  { code: 'MG', name: 'Minas Gerais' },
  { code: 'PA', name: 'Pará' },
  { code: 'PB', name: 'Paraíba' },
  { code: 'PR', name: 'Paraná' },
  { code: 'PE', name: 'Pernambuco' },
  { code: 'PI', name: 'Piauí' },
  { code: 'RJ', name: 'Rio de Janeiro' },
  { code: 'RN', name: 'Rio Grande do Norte' },
  { code: 'RS', name: 'Rio Grande do Sul' },
  { code: 'RO', name: 'Rondônia' },
  { code: 'RR', name: 'Roraima' },
  { code: 'SC', name: 'Santa Catarina' },
  { code: 'SP', name: 'São Paulo' },
  { code: 'SE', name: 'Sergipe' },
  { code: 'TO', name: 'Tocantins' }
];

export default function StationForm({ open, onClose, onSave, station }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm({
    defaultValues: {
      name: '',
      latitude: '',
      longitude: '',
      charger_type: '',
      power_kw: '',
      num_spots: '',
      status: '',
      state: '',
      city: ''
    }
  });

  useEffect(() => {
    if (station) {
      reset({
        name: station.name || '',
        latitude: station.latitude || '',
        longitude: station.longitude || '',
        charger_type: station.charger_type || '',
        power_kw: station.power_kw || '',
        num_spots: station.num_spots || '',
        status: station.status || '',
        state: station.state || '',
        city: station.city || ''
      });
    } else {
      reset({
        name: '',
        latitude: '',
        longitude: '',
        charger_type: '',
        power_kw: '',
        num_spots: '',
        status: 'OPERATIONAL',
        state: '',
        city: ''
      });
    }
  }, [station, reset]);

  const onSubmit = async (data) => {
    try {
      setLoading(true);
      setError('');
      
      // Convert numeric fields
      const formattedData = {
        ...data,
        latitude: parseFloat(data.latitude),
        longitude: parseFloat(data.longitude),
        power_kw: parseFloat(data.power_kw),
        num_spots: parseInt(data.num_spots, 10)
      };

      await onSave(formattedData);
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to save station');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    reset();
    setError('');
    onClose();
  };

  return (
    <Dialog 
      open={open} 
      onClose={handleClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: { minHeight: '600px' }
      }}
    >
      <DialogTitle>
        <Typography variant="h6">
          {station ? 'Editar Estação' : 'Nova Estação de Carregamento'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {station ? 'Atualize os dados da estação' : 'Cadastre uma nova estação de carregamento elétrico'}
        </Typography>
      </DialogTitle>

      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Controller
                name="name"
                control={control}
                rules={{ required: 'Nome é obrigatório' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Nome da Estação *"
                    error={!!errors.name}
                    helperText={errors.name?.message}
                    placeholder="Ex: Estação São Paulo - Centro"
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="latitude"
                control={control}
                rules={{
                  required: 'Latitude é obrigatória',
                  validate: (value) => {
                    const num = parseFloat(value);
                    if (isNaN(num)) return 'Deve ser um número válido';
                    if (num < -90 || num > 90) return 'Deve estar entre -90 e 90';
                    return true;
                  }
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Latitude *"
                    type="number"
                    inputProps={{ step: 'any' }}
                    error={!!errors.latitude}
                    helperText={errors.latitude?.message || 'Entre -90 e 90'}
                    placeholder="-23.5505"
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="longitude"
                control={control}
                rules={{
                  required: 'Longitude é obrigatória',
                  validate: (value) => {
                    const num = parseFloat(value);
                    if (isNaN(num)) return 'Deve ser um número válido';
                    if (num < -180 || num > 180) return 'Deve estar entre -180 e 180';
                    return true;
                  }
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Longitude *"
                    type="number"
                    inputProps={{ step: 'any' }}
                    error={!!errors.longitude}
                    helperText={errors.longitude?.message || 'Entre -180 e 180'}
                    placeholder="-46.6333"
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="charger_type"
                control={control}
                rules={{ required: 'Tipo de carregador é obrigatório' }}
                render={({ field }) => (
                  <FormControl fullWidth error={!!errors.charger_type}>
                    <InputLabel>Tipo de Carregador *</InputLabel>
                    <Select {...field} label="Tipo de Carregador *">
                      <MenuItem value="AC">AC (Corrente Alternada)</MenuItem>
                      <MenuItem value="DC">DC (Corrente Contínua)</MenuItem>
                      <MenuItem value="BOTH">AC/DC (Ambos)</MenuItem>
                    </Select>
                    {errors.charger_type && (
                      <Typography variant="caption" color="error" sx={{ mt: 1, ml: 2 }}>
                        {errors.charger_type.message}
                      </Typography>
                    )}
                  </FormControl>
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="power_kw"
                control={control}
                rules={{
                  required: 'Potência é obrigatória',
                  validate: (value) => {
                    const num = parseFloat(value);
                    if (isNaN(num) || num <= 0) return 'Deve ser um número positivo';
                    return true;
                  }
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Potência (kW) *"
                    type="number"
                    inputProps={{ step: 'any', min: 0 }}
                    error={!!errors.power_kw}
                    helperText={errors.power_kw?.message || 'Ex: 22, 50, 150'}
                    placeholder="150"
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="num_spots"
                control={control}
                rules={{
                  required: 'Número de vagas é obrigatório',
                  validate: (value) => {
                    const num = parseInt(value, 10);
                    if (isNaN(num) || num <= 0) return 'Deve ser um número inteiro positivo';
                    return true;
                  }
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Número de Vagas *"
                    type="number"
                    inputProps={{ min: 1, step: 1 }}
                    error={!!errors.num_spots}
                    helperText={errors.num_spots?.message}
                    placeholder="4"
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="status"
                control={control}
                rules={{ required: 'Status é obrigatório' }}
                render={({ field }) => (
                  <FormControl fullWidth error={!!errors.status}>
                    <InputLabel>Status *</InputLabel>
                    <Select {...field} label="Status *">
                      <MenuItem value="OPERATIONAL">Operacional</MenuItem>
                      <MenuItem value="MAINTENANCE">Em Manutenção</MenuItem>
                      <MenuItem value="INACTIVE">Inativo</MenuItem>
                    </Select>
                    {errors.status && (
                      <Typography variant="caption" color="error" sx={{ mt: 1, ml: 2 }}>
                        {errors.status.message}
                      </Typography>
                    )}
                  </FormControl>
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="state"
                control={control}
                rules={{ required: 'Estado é obrigatório' }}
                render={({ field }) => (
                  <FormControl fullWidth error={!!errors.state}>
                    <InputLabel>Estado (UF) *</InputLabel>
                    <Select {...field} label="Estado (UF) *">
                      {BRAZILIAN_STATES.map((state) => (
                        <MenuItem key={state.code} value={state.code}>
                          {state.code} - {state.name}
                        </MenuItem>
                      ))}
                    </Select>
                    {errors.state && (
                      <Typography variant="caption" color="error" sx={{ mt: 1, ml: 2 }}>
                        {errors.state.message}
                      </Typography>
                    )}
                  </FormControl>
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="city"
                control={control}
                rules={{ required: 'Cidade é obrigatória' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Cidade *"
                    error={!!errors.city}
                    helperText={errors.city?.message}
                    placeholder="São Paulo"
                  />
                )}
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 3, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Dica:</strong> Use ferramentas como Google Maps para obter as coordenadas exatas da localização da estação.
            </Typography>
          </Box>
        </DialogContent>

        <DialogActions sx={{ p: 3 }}>
          <Button onClick={handleClose} disabled={loading}>
            Cancelar
          </Button>
          <Button
            type="submit"
            variant="contained"
            disabled={loading}
          >
            {loading ? 'Salvando...' : (station ? 'Atualizar' : 'Cadastrar')}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}

