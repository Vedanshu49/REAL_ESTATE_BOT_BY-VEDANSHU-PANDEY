# Real Estate Analysis Chatbot 🏠

A full-stack AI-powered chatbot application for real estate analysis using **React + Django + Gemini LLM**.

## 🎯 Features

- **Chat Interface**: User-friendly chat-style interface for property queries
- **AI-Powered Summaries**: Real-time summaries using Google Gemini API
- **Data Visualization**: Interactive charts showing price and demand trends
- **Data Tables**: Sortable, paginated tables with property information
- **Download Feature**: Export filtered property data as CSV
- **Location-based Filtering**: Search and analyze properties by location
- **Query History**: Keep track of all previous queries

## 🏗️ Project Structure

```
.
├── backend/                    # Django REST API
│   ├── config/                # Django settings
│   ├── api/                   # Main API app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # Data serializers
│   │   ├── services.py        # Business logic & Gemini integration
│   │   └── urls.py            # URL routing
│   ├── load_data.py           # Excel data loader
│   ├── manage.py              # Django management
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React + Vite
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.jsx            # Main app component
│   │   ├── api.js             # API client
│   │   └── main.jsx           # Entry point
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
├── Sample_data.xlsx           # Real estate data
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### 1. Clone & Setup
```bash
cd "c:\Users\VEDANSHU\Desktop\projects\intership test"
git clone <your-repo-url> .
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt

# Run migrations
cd backend
python manage.py makemigrations
python manage.py migrate

# Load sample data
python load_data.py

# Start server
python manage.py runserver
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Configure Environment Variables

**backend/.env**:
```
SECRET_KEY=your-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
ALLOWED_HOSTS=localhost,127.0.0.1
```

**frontend/.env.local**:
```
VITE_API_URL=http://localhost:8000/api
```

## 📱 Usage

1. **Start Backend**: `python manage.py runserver` (Django at http://localhost:8000)
2. **Start Frontend**: `npm run dev` (React at http://localhost:5173)
3. **Open Browser**: Navigate to http://localhost:5173
4. **Query Examples**:
   - "Analyze Wakad"
   - "Compare demand trends"
   - "Show Pune properties"

## 🔑 API Endpoints

### Queries
- `POST /api/queries/analyze/` - Analyze property data
  - Request: `{ "query": "string" }`
  - Response: `{ "summary": "string", "chartData": [...], "tableData": [...] }`

- `POST /api/queries/download_data/` - Download filtered data as CSV
  - Request: `{ "query": "string" }`
  - Response: CSV file

- `GET /api/queries/history/` - Get recent queries

### Properties
- `GET /api/properties/` - List all properties
- `GET /api/properties/by_location/?location=<name>` - Filter by location
- `GET /api/properties/locations_list/` - Get all locations

## 🤖 LLM Integration

This project uses **Google Gemini API** for natural language summaries.

### Setup Gemini API:
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create or use existing API key
3. Add to `backend/.env`: `GEMINI_API_KEY=your-key`

## 📊 Database Schema

### Property Model
- `location` (CharField)
- `property_type` (CharField: residential/commercial/industrial)
- `price` (DecimalField)
- `price_per_sqft` (DecimalField, nullable)
- `area_sqft` (DecimalField, nullable)
- `year` (IntegerField)
- `demand` (IntegerField)
- `demand_score` (FloatField)

### Query Model
- `user_query` (TextField)
- `location_filter` (CharField)
- `response_summary` (TextField)
- `chart_data` (JSONField)
- `table_data` (JSONField)
- `created_at` (DateTimeField)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Recharts, Tailwind CSS |
| Backend | Django 5.2, Django REST Framework |
| Database | SQLite (dev), PostgreSQL (prod) |
| LLM | Google Gemini API |
| Package Manager | npm, pip |

## 📦 Deployment

### Backend (Django)
**Option 1: Render**
```bash
# Create Render account and connect GitHub repo
# Set environment variables in Render dashboard
# Deploy with: python manage.py migrate && gunicorn config.wsgi
```

**Option 2: Railway**
```bash
# Similar setup with Railway dashboard
```

### Frontend (React)
**Vercel**
```bash
npm install -g vercel
vercel
# Follow prompts
```

## 🧪 Testing

```bash
# Backend tests
python manage.py test

# Frontend tests (if configured)
npm test
```

## 📝 Git Workflow

```bash
git add .
git commit -m "Feature: Add feature name"
git push origin main
```

## 🐛 Troubleshooting

### CORS Issues
- Ensure `CORS_ALLOWED_ORIGINS` in `backend/.env` matches frontend URL
- Clear browser cache and restart both servers

### Gemini API Errors
- Verify API key is correct
- Check API quota in Google Cloud Console
- Ensure Gemini API is enabled

### Data Not Loading
- Run `python load_data.py` in backend directory
- Check `Sample_data.xlsx` exists in project root
- Verify database migrations ran: `python manage.py migrate`

## 📄 License

MIT License - See LICENSE file

## 👨‍💻 Author

**Vedanshu Pandey**

## 📞 Support

For issues, please open a GitHub issue or contact the development team.

---

**Made with ❤️ using React + Django + Gemini**
