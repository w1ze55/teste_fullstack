import React, { useState } from 'react';
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Pagination,
  CircularProgress,
  Alert,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button
} from '@mui/material';
import {
  MoreVert as MoreVertIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  LocationOn as LocationIcon,
  ElectricBolt as ElectricBoltIcon,
  LocalParking as LocalParkingIcon
} from '@mui/icons-material';

function StationListItem({ station, isSelected, onSelect, onEdit, onDelete }) {
  const [anchorEl, setAnchorEl] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const handleMenuClick = (event) => {
    event.stopPropagation();
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleEdit = () => {
    handleMenuClose();
    onEdit(station);
  };

  const handleDeleteClick = () => {
    handleMenuClose();
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = () => {
    setDeleteDialogOpen(false);
    onDelete(station.id);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'OPERATIONAL':
        return 'success';
      case 'MAINTENANCE':
        return 'warning';
      case 'INACTIVE':
        return 'error';
      default:
        return 'default';
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

  const getTypeColor = (type) => {
    switch (type) {
      case 'AC':
        return 'primary';
      case 'DC':
        return 'secondary';
      case 'BOTH':
        return 'info';
      default:
        return 'default';
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
    <>
      <ListItem
        disablePadding
        sx={{
          backgroundColor: isSelected ? 'action.selected' : 'transparent',
          '&:hover': {
            backgroundColor: 'action.hover'
          }
        }}
      >
        <ListItemButton onClick={() => onSelect(station)} sx={{ px: 2, py: 1.5 }}>
          <ListItemText
            primary={
              <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                  {station.name}
                </Typography>
                <IconButton
                  size="small"
                  onClick={handleMenuClick}
                  sx={{ ml: 1, mt: -0.5 }}
                >
                  <MoreVertIcon fontSize="small" />
                </IconButton>
              </Box>
            }
            secondary={
              <Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <LocationIcon sx={{ fontSize: 14, mr: 0.5, color: 'text.secondary' }} />
                  <Typography variant="caption" color="text.secondary">
                    {station.city}, {station.state}
                  </Typography>
                </Box>
                
                <Box sx={{ display: 'flex', gap: 0.5, mb: 1, flexWrap: 'wrap' }}>
                  <Chip
                    label={getStatusText(station.status)}
                    color={getStatusColor(station.status)}
                    size="small"
                    variant="filled"
                  />
                  <Chip
                    label={getTypeText(station.charger_type)}
                    color={getTypeColor(station.charger_type)}
                    size="small"
                    variant="outlined"
                  />
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <ElectricBoltIcon sx={{ fontSize: 14, mr: 0.5, color: 'text.secondary' }} />
                    <Typography variant="caption" color="text.secondary">
                      {station.power_kw} kW
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <LocalParkingIcon sx={{ fontSize: 14, mr: 0.5, color: 'text.secondary' }} />
                    <Typography variant="caption" color="text.secondary">
                      {station.num_spots} vagas
                    </Typography>
                  </Box>
                </Box>
              </Box>
            }
          />
        </ListItemButton>
      </ListItem>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        onClick={(e) => e.stopPropagation()}
      >
        <MenuItem onClick={handleEdit}>
          <EditIcon sx={{ mr: 1, fontSize: 18 }} />
          Editar
        </MenuItem>
        <MenuItem onClick={handleDeleteClick} sx={{ color: 'error.main' }}>
          <DeleteIcon sx={{ mr: 1, fontSize: 18 }} />
          Excluir
        </MenuItem>
      </Menu>

      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Confirmar Exclusão</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza que deseja excluir a estação "{station.name}"?
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Esta ação não pode ser desfeita.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>
            Cancelar
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Excluir
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default function StationList({
  stations,
  loading,
  error,
  selectedStation,
  onStationSelect,
  onStationEdit,
  onStationDelete,
  pagination,
  onPageChange
}) {
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 2 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!stations || stations.length === 0) {
    return (
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          Nenhuma estação encontrada
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Tente ajustar os filtros ou adicionar uma nova estação
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="body2" color="text.secondary">
          {pagination.total} estações encontradas
        </Typography>
        {pagination.totalPages > 1 && (
          <Typography variant="caption" color="text.secondary">
            Página {pagination.page} de {pagination.totalPages}
          </Typography>
        )}
      </Box>

      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <List sx={{ p: 0 }}>
          {stations.map((station, index) => (
            <React.Fragment key={station.id}>
              <StationListItem
                station={station}
                isSelected={selectedStation?.id === station.id}
                onSelect={onStationSelect}
                onEdit={onStationEdit}
                onDelete={onStationDelete}
              />
              {index < stations.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </Box>

      {pagination.totalPages > 1 && (
        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <Pagination
            count={pagination.totalPages}
            page={pagination.page}
            onChange={(event, page) => onPageChange(page)}
            color="primary"
            size="small"
            sx={{
              display: 'flex',
              justifyContent: 'center'
            }}
          />
        </Box>
      )}
    </Box>
  );
}


