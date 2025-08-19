# 🚀 Deploy Guide - Render

Este guia contém as instruções para fazer deploy da aplicação EV Charging Stations no Render.

## ✅ Arquivos Preparados

Os seguintes arquivos foram criados/atualizados para o deploy:

- ✅ `render.yaml` - Configuração automática do Render
- ✅ `backend/config.py` - Configurações de produção
- ✅ `backend/run.py` - Script de inicialização atualizado
- ✅ `backend/build.sh` - Script de build do backend
- ✅ `backend/app/__init__.py` - CORS configurado para produção
- ✅ `frontend/src/config/api.js` - Configuração centralizada da API
- ✅ `frontend/src/contexts/AuthContext.js` - URLs atualizadas
- ✅ `frontend/src/components/Dashboard.js` - URLs atualizadas

## 🌐 Passo a Passo no Render

### 1. Preparar Repositório
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy Automático (Recomendado)
1. Acesse [render.com](https://render.com)
2. Faça login com GitHub
3. Clique em **"New +"** → **"Blueprint"**
4. Conecte seu repositório
5. O Render detectará o `render.yaml` automaticamente
6. Clique em **"Deploy"**

### 3. Deploy Manual (Alternativo)

#### Backend:
1. **New +** → **Web Service**
2. **Configurações:**
   - Name: `ev-charging-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
   - Root Directory: `backend`

#### Frontend:
1. **New +** → **Static Site**
2. **Configurações:**
   - Name: `ev-charging-frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `build`
   - Root Directory: `frontend`

#### Banco de Dados:
1. **New +** → **PostgreSQL**
2. **Name:** `ev-charging-db`
3. **Plan:** Free

## ⚙️ Variáveis de Ambiente

### Backend:
- `FLASK_ENV=production`
- `SECRET_KEY` (gerado automaticamente pelo Render)
- `DATABASE_URL` (conectado automaticamente ao PostgreSQL)

### Frontend:
- `REACT_APP_API_URL` (conectado automaticamente ao backend)

## 🔄 Após o Deploy

1. **Aguarde** todos os serviços ficarem online (pode levar alguns minutos)
2. **Teste** a aplicação:
   - Acesse o frontend
   - Faça login com: `admin` / `admin123`
   - Verifique se as estações carregam corretamente
3. **Configure domínio personalizado** (opcional)

## 🐛 Solução de Problemas

### Backend não inicia:
- Verifique os logs do serviço
- Confirme se `DATABASE_URL` está configurado
- Verifique se todas as dependências estão no `requirements.txt`

### Frontend não carrega dados:
- Verifique se `REACT_APP_API_URL` aponta para o backend correto
- Confirme se o CORS está configurado corretamente
- Verifique os logs do browser (F12)

### Banco de dados vazio:
- O `seed_data.py` é executado automaticamente
- Usuário admin padrão: `admin` / `admin123`

## 📝 URLs Finais

Após o deploy, suas URLs serão:
- **Frontend:** `https://ev-charging-frontend.onrender.com`
- **Backend API:** `https://ev-charging-backend.onrender.com`
- **Database:** Interno (não acessível externamente)

## 🔒 Segurança

- ✅ Senhas não são expostas nos logs
- ✅ CORS configurado apenas para domínios autorizados
- ✅ SECRET_KEY gerado automaticamente
- ✅ Banco PostgreSQL com SSL

## 📊 Monitoramento

O Render fornece:
- Logs em tempo real
- Métricas de performance
- Health checks automáticos
- Alertas por email

---

**🎉 Sua aplicação está pronta para produção!**
