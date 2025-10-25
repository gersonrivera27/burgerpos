#  Burger POS System

Point of Sale (POS) system for a burger restaurant using a Docker container architecture.

# Architecture

- **Frontend**: .NET 8.0 with Blazor
- **Backend**: Python FastAPI
- **Database**: PostgreSQL 15
- **Containerization**: Docker Compose

##  Initial Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd burguer
```

### 2. Configure environment variables

Copy the example file and add your credentials:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your Google Maps API key:

```
GOOGLE_MAPS_API_KEY=your_real_api_key_here
```

### 3. Start the containers

```bash
docker-compose up -d
```

### 4. Access the application

- **Frontend**: http://localhost:5001
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5433

## 🌟 Current Features

- ✅ Customer registration (name + phone)
- ✅ Google Maps API integration for coordinates and addresses
- ✅ Docker container system
- ✅ PostgreSQL database

## 📝 Development

### Project Structure

```
burguer/
├── frontend/          # .NET Blazor Application
├── backend/           # FastAPI API
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       └── routers/
├── docker-compose.yml
└── .env.example
```

### Useful Commands

```bash
# View container logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop everything
docker-compose down
```

## 🔐 Security

**IMPORTANT**: Never upload `.env` files to GitHub.
API keys and credentials must be managed locally.

## 📊 Upcoming Features

- [ ] Order system
- [ ] Product menu
- [ ] Administration panel
- [ ] Sales reports
