# 🍽️ Wahat Al Jazzat Cafeteria - AI Receptionist System

An intelligent restaurant management system with AI-powered ordering and real-time kitchen display.

![Wahat Al Jazzat](https://img.shields.io/badge/Restaurant-Bahraini-red) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![n8n](https://img.shields.io/badge/n8n-Automation-orange)

## ✨ Features

### 🤖 AI Receptionist
- Natural language chat interface
- Automatic order detection
- Menu recommendations
- Multi-language support (Arabic/English)

### 📱 Customer Dashboard
- Beautiful menu browsing
- One-click ordering
- Real-time order tracking
- Conversation history

### 👨‍🍳 Kitchen Display System
- Real-time order display via WebSocket
- One-click status updates
- Order filtering and sorting
- Urgent order indicators
- Desktop notifications

### 🔗 System Integration
- n8n workflow automation
- MySQL database
- FastAPI backend
- Responsive design

## 🚀 Quick Start

### Windows
```bash
# Run the startup script
start_wahat_system.bat
```

### macOS/Linux
```bash
# Make script executable (first time only)
chmod +x start_wahat_system.sh

# Run the startup script
./start_wahat_system.sh
```

### Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements_wahat.txt
   npm install -g n8n
   ```

2. **Setup database**
   ```bash
   mysql -u root -p < execution/database/schema.sql
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Start n8n**
   ```bash
   n8n start
   # Open http://localhost:5678 and import the workflow
   ```

5. **Start API server**
   ```bash
   cd execution/api
   python server.py
   ```

6. **Open dashboards**
   - Customer: `frontend/customer/index.html`
   - Kitchen: `frontend/kitchen/index.html`

## 📁 Project Structure

```
.
├── execution/
│   ├── api/
│   │   └── server.py              # FastAPI backend
│   └── database/
│       └── schema.sql             # Database schema
├── frontend/
│   ├── customer/
│   │   └── index.html             # Customer chat dashboard
│   └── kitchen/
│       └── index.html             # Kitchen display system
├── workflows/
│   └── ai_receptionist_workflow.json  # n8n workflow
├── directives/
│   └── wahat_receptionist.md      # Complete documentation
├── requirements_wahat.txt         # Python dependencies
├── start_wahat_system.bat        # Windows startup script
└── start_wahat_system.sh          # macOS/Linux startup script
```

## 🎨 Design

The system features a warm, elegant design inspired by traditional Bahraini aesthetics:

- **Colors**: Red (#C8102E), Orange (#FF6B35), Gold (#D4AF37), Cream (#FFF8E7)
- **Fonts**: Playfair Display (headings), Inter (body)
- **Patterns**: Subtle Arabic geometric patterns
- **Responsiveness**: Mobile-first design

## 🔧 Configuration

### Environment Variables (.env)

```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=wahat_al_jazzat

# n8n
N8N_BASE_URL=http://localhost:5678
ANTHROPIC_API_KEY=your_anthropic_key

# API
API_HOST=0.0.0.0
API_PORT=8000
```

### Customizing the Menu

Edit `execution/database/schema.sql`:

```sql
INSERT INTO menu_items (item_name, category, description, price, preparation_time)
VALUES ('New Dish', 'MAIN_DISHES', 'Delicious description', 5.000, 25);
```

## 📊 API Endpoints

### Customer
- `GET /menu` - Get menu items
- `POST /chat` - Send message to AI
- `GET /orders` - Get orders
- `GET /orders/{id}` - Get specific order

### Kitchen
- `GET /orders?status=pending` - Filter orders
- `PUT /orders/{id}/status` - Update status
- `WS /ws/kitchen` - Real-time updates

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Automation**: n8n
- **AI**: Anthropic Claude (via n8n)
- **Real-time**: WebSocket

## 📖 Documentation

For complete documentation, see:
- [Directives/Documentation](directives/wahat_receptionist.md)
- [n8n Workflow](workflows/ai_receptionist_workflow.json)
- [Database Schema](execution/database/schema.sql)

## 🔐 Security Notes

This is a development system. For production:

1. Add API authentication (JWT/API keys)
2. Enable HTTPS
3. Implement rate limiting
4. Use environment variables for secrets
5. Set up proper database permissions
6. Add input validation and sanitization

## 🐛 Troubleshooting

### Database connection fails
- Check MySQL is running: `sudo systemctl status mysql`
- Verify credentials in `.env`
- Test connection: `mysql -u root -p`

### n8n workflow not running
- Open http://localhost:5678
- Verify workflow is active (green icon)
- Check credentials are configured
- View execution logs

### Frontend can't connect to API
- Check API is running: http://localhost:8000/health
- Verify CORS configuration
- Check browser console for errors

## 🤝 Contributing

To improve the system:

1. Update menu items in `schema.sql`
2. Modify AI behavior in n8n workflow
3. Customize styling in HTML files
4. Add new API endpoints in `server.py`

## 📄 License

This project is for Wahat Al Jazzat Cafeteria.

## 📞 Support

For issues or questions:
1. Check the [documentation](directives/wahat_receptionist.md)
2. Review error logs
3. Test database queries
4. Verify API endpoints

---

Built with ❤️ for Wahat Al Jazzat Cafeteria

**Traditional Bahraini Cuisine | AI-Powered Service**
