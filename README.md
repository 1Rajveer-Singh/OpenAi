# 🇮🇳 VyapaarGPT - Ultra Advanced AI Business OS for India

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/1Rajveer-Singh/OpenAi)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deploy-black)](https://vercel.com)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red)](https://fastapi.tiangolo.com)

## 🌟 Overview

VyapaarGPT is an **Ultra Advanced AI Business Operating System** specifically designed for Indian businesses, MSMEs, and startups. It combines cutting-edge AI technology with deep understanding of Indian business culture, languages, and market dynamics.

### 🚀 Key Features

- **🤖 AI Business Agents**: Intelligent assistants for different business functions
- **🎙️ Voice Interface**: Multilingual voice commands in Hindi, English, and regional languages
- **📊 Smart Analytics**: Real-time business insights and predictive analytics
- **🛒 Marketplace Integration**: Connect with major Indian platforms (Flipkart, Amazon India, etc.)
- **� Complete Business Management**: Inventory, CRM, Finance, HR, Marketing
- **🌐 Multi-language Support**: Hindi, English, Tamil, Telugu, Bengali, and more
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **🔒 Enterprise Security**: Advanced security features for business data

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLite**: Lightweight database for demo (scalable to PostgreSQL/MySQL)
- **Python 3.8+**: Modern Python with async/await support
- **Uvicorn**: Lightning-fast ASGI server

### Frontend
- **React.js**: Modern component-based UI framework
- **React Router**: Client-side routing and navigation
- **React Context**: Global state management
- **Vanilla JavaScript**: No framework dependencies for maximum performance (legacy option)
- **Chart.js**: Beautiful, responsive charts and analytics
- **GSAP**: Smooth animations and transitions
- **Font Awesome**: Comprehensive icon library
- **Responsive CSS**: Mobile-first design approach

### Deployment
- **Vercel**: Serverless deployment platform
- **GitHub**: Version control and CI/CD
- **Environment Variables**: Secure configuration management

## 🚀 Quick Start

### React Frontend + FastAPI Backend

1. **Clone the Repository**
   ```bash
   git clone https://github.com/1Rajveer-Singh/OpenAi.git
   cd OpenAi/vyapaargpt
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
   Backend will run on `http://localhost:8000`

3. **React Frontend Setup**
   ```bash
   cd react-frontend
   npm install
   npm start
   ```
   Frontend will run on `http://localhost:3000`

### Legacy Vanilla JS Frontend (Alternative)

1. **Frontend Setup (Vanilla JS)**
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   Frontend will run on `http://localhost:3000`

### 🌐 Vercel Deployment

#### Method 1: One-Click Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/1Rajveer-Singh/OpenAi)

#### Method 2: Manual Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from Project Root**
   ```bash
   vercel --prod
   ```

#### Method 3: GitHub Integration

1. **Connect GitHub to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import from GitHub: `1Rajveer-Singh/OpenAi`
   - Select the `vyapaargpt` folder as root directory

2. **Configure Build Settings**
   - Build Command: `echo "Building VyapaarGPT..."`
   - Output Directory: `frontend`
   - Install Command: `pip install -r backend/requirements.txt`

## 📁 Project Structure

```
vyapaargpt/
├── backend/
│   ├── main.py              # Serverless FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── business.db         # SQLite database (auto-created)
├── react-frontend/          # Modern React.js application
│   ├── public/
│   │   └── index.html      # React app shell
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── context/        # React context (state management)
│   │   ├── styles/         # CSS files
│   │   ├── App.js          # Main React app
│   │   └── index.js        # React entry point
│   └── package.json        # React dependencies
├── frontend/               # Legacy vanilla JS (alternative)
│   ├── index-advanced.html # Original advanced frontend
│   ├── app.js             # Vanilla JS logic
│   └── css/               # Styling
├── vercel.json            # Vercel deployment config
├── package.json           # Project metadata
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Business Configuration
BUSINESS_NAME="Your Business Name"
BUSINESS_TYPE="retail"
CURRENCY="INR"
LANGUAGE="hi"

# API Configuration
API_BASE_URL="https://your-domain.vercel.app/api"

# Feature Flags
ENABLE_VOICE_INTERFACE=true
ENABLE_MARKETPLACE_INTEGRATION=true
ENABLE_AI_INSIGHTS=true
```

## 🔌 API Endpoints

### Business Management
- `GET /api/dashboard` - Get dashboard data
- `POST /api/business/profile` - Update business profile
- `GET /api/business/analytics` - Get business analytics

### Inventory Management
- `GET /api/inventory` - List all inventory items
- `POST /api/inventory` - Add new inventory item
- `PUT /api/inventory/{id}` - Update inventory item

### Customer Management
- `GET /api/customers` - List all customers
- `POST /api/customers` - Add new customer

### AI Features
- `POST /api/ai/chat` - Chat with AI assistant
- `POST /api/ai/voice` - Process voice commands
- `GET /api/ai/insights` - Get AI business insights

## 🚨 Troubleshooting

### Common Issues

1. **Backend Not Starting**
   ```bash
   # Check Python version
   python --version  # Should be 3.8+
   
   # Install dependencies
   pip install -r backend/requirements.txt
   ```

2. **CORS Errors**
   - Ensure frontend and backend URLs are correctly configured
   - Check `API_BASE_URL` in environment variables

3. **Vercel Deployment Issues**
   ```bash
   # Check build logs
   vercel logs
   
   # Redeploy
   vercel --prod --force
   ```

## 📜 License

MIT License

## 🙏 Acknowledgments

- **Indian MSME Community**: For inspiration and feedback
- **Open Source Libraries**: FastAPI, Chart.js, GSAP, Font Awesome

---

**Made with ❤️ for Indian Businesses by [Rajveer Singh](https://github.com/1Rajveer-Singh)**

🚀 **Ready to transform your business with AI? Deploy VyapaarGPT on Vercel now!**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/1Rajveer-Singh/OpenAi)

### 🛒 Marketplace Integration
- One-click sync to ONDC, Flipkart, Amazon, Meesho
- AI-optimized product listings
- Automated pricing strategies

## 🏗️ Architecture

```
VyapaarGPT/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── agents/         # Multi-Agent AI System
│   │   ├── api/            # REST API Endpoints
│   │   ├── models/         # Database Models
│   │   ├── services/       # Business Logic
│   │   └── integrations/   # External API Integrations
├── frontend/               # React Native Mobile App
├── docs/                   # Documentation
└── deployment/            # Docker & Cloud Config
```

## 🛠️ Tech Stack

- **AI Models**: OpenAI GPT-4o, Whisper, Vision API
- **Backend**: Python FastAPI, PostgreSQL
- **Frontend**: React Native (Voice-First UI)
- **Integrations**: UPI APIs, WhatsApp Business, ONDC, Marketplace APIs
- **Security**: AES-256 encryption, Indian data compliance

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- OpenAI API Key

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npx react-native run-android  # or run-ios
```

## 🌍 Impact

- **Economic Upliftment**: Empower 60M+ MSMEs with AI
- **Inclusivity**: Local language + voice-first adoption
- **Scalability**: From kirana stores to growing startups
- **Job Creation**: AI augments human decision-making

## 🔮 Future Roadmap

- [ ] Credit Access via AI-generated profiles
- [ ] Community Commerce for bulk buying
- [ ] AR/VR Shopping experiences
- [ ] Advanced ML models for market prediction

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📧 Contact

For questions or support, reach out to the VyapaarGPT team.

---

**Built with ❤️ for Bharat's entrepreneurs**