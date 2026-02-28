# Wahat Al Jazzat Cafeteria - AI Receptionist System

## Overview

Complete AI-powered restaurant management system with:
- **Customer Chat Interface** - AI receptionist for taking orders
- **Kitchen Display System** - Real-time order management for chefs
- **n8n Integration** - AI-powered order processing
- **Database** - MySQL for orders and sessions

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CUSTOMER DASHBOARD                                        │
│  - Chat with AI receptionist                                │
│  - Browse menu                                             │
│  - Place orders                                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  FASTAPI BACKEND (execution/api/server.py)                 │
│  - Handle chat messages                                     │
│  - Manage orders                                           │
│  - WebSocket for real-time updates                         │
└──────────────┬──────────────────────────────────────────────┘
               │
               ├─────────────────────┐
               ↓                     ↓
┌──────────────────────────┐  ┌──────────────────────┐
│  n8n Workflow            │  │  MySQL Database       │
│  - AI conversation      │  │  - Orders             │
│  - Order detection       │  │  - Sessions           │
│  - Menu recommendations  │  │  - Conversation       │
└──────────────────────────┘  └──────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────────────────┐
│  KITCHEN DISPLAY SYSTEM                                     │
│  - Real-time order display                                  │
│  - Status management                                        │
│  - WebSocket updates                                        │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Database Setup

```bash
# Install MySQL
# On Ubuntu/Debian:
sudo apt-get install mysql-server

# On macOS:
brew install mysql

# On Windows:
# Download from https://dev.mysql.com/downloads/mysql/
```

Create the database and tables:

```bash
mysql -u root -p < execution/database/schema.sql
```

Or manually:

```sql
CREATE DATABASE wahat_al_jazzat;
USE wahat_al_jazzat;

-- Run the schema.sql file contents
```

### 2. Install Dependencies

```bash
# Python dependencies
pip install fastapi uvicorn mysql-connector-python python-dotenv requests

# Node.js (for n8n)
npm install -g n8n
```

### 3. Configure Environment Variables

Create `.env` file in project root:

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

### 4. Start n8n

```bash
n8n start
```

Import the workflow:
1. Open http://localhost:5678
2. Click "Import from File"
3. Select `workflows/ai_receptionist_workflow.json`
4. Configure credentials:
   - MySQL database connection
   - Anthropic API key
5. Activate the workflow

### 5. Start the API Server

```bash
cd execution/api
python server.py
```

Or with auto-reload:

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open the Dashboards

**Customer Dashboard:**
Open `frontend/customer/index.html` in your browser

**Kitchen Display:**
Open `frontend/kitchen/index.html` in your browser

## Features

### Customer Dashboard

- **AI Chat Interface** - Natural conversation with AI receptionist
- **Menu Browsing** - Interactive menu with categories
- **One-Click Ordering** - Click menu items to order
- **Order Tracking** - Real-time order status updates
- **Conversation History** - Full chat session maintained

### Kitchen Display

- **Real-Time Updates** - WebSocket-based live order display
- **Order Filtering** - Filter by status (pending/preparing/ready)
- **Status Management** - One-click status updates
- **Time Tracking** - See how long orders have been waiting
- **Priority Indicators** - Urgent orders highlighted
- **Notifications** - Desktop notifications for new orders

### n8n Workflow

- **AI-Powered Chat** - Claude AI for natural conversation
- **Order Detection** - Automatic order extraction from conversation
- **Menu Integration** - Real-time menu data for recommendations
- **Session Management** - Track customer conversations
- **Status Updates** - Automatic status logging

## API Endpoints

### Customer-Facing

```bash
GET  /menu                    # Get all menu items
POST /chat                    # Send message to AI
GET  /orders                  # Get all orders
GET  /orders/{id}             # Get specific order
GET  /sessions/{id}/orders    # Get orders for session
GET  /sessions/{id}/conversation  # Get conversation history
POST /sessions                # Create new session
```

### Kitchen-Facing

```bash
GET  /orders?status=pending   # Get filtered orders
PUT  /orders/{id}/status      # Update order status
WS   /ws/kitchen              # WebSocket for real-time updates
```

### Health & Monitoring

```bash
GET  /                        # API info
GET  /health                  # Health check
```

## Database Schema

### Tables

- `menu_items` - Restaurant menu
- `sessions` - Customer chat sessions
- `orders` - Customer orders
- `order_items` - Items in each order
- `conversation_history` - Chat messages
- `order_status_log` - Status change history

## Customization

### Update Menu Items

Edit `execution/database/schema.sql` and add/update menu items:

```sql
INSERT INTO menu_items (item_name, category, description, price, preparation_time)
VALUES ('New Dish', 'MAIN_DISHES', 'Delicious description', 5.000, 25);
```

### Modify AI Behavior

Edit the system prompt in the n8n workflow:
1. Open n8n workflow
2. Find "Generate AI Response" node
3. Edit the system message in the parameters

### Change Colors/Branding

Edit CSS variables in the HTML files:

```css
:root {
    --primary-red: #C8102E;
    --primary-orange: #FF6B35;
    --gold: #D4AF37;
    --cream: #FFF8E7;
}
```

## Production Deployment

### Database

- Use a managed MySQL service (AWS RDS, Google Cloud SQL, etc.)
- Set up regular backups
- Configure connection pooling

### API Server

```bash
# Using gunicorn with uvicorn workers
pip install gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### n8n

- Use Docker: `docker run -p 5678:5678 n8nio/n8n`
- Or deploy n8n cloud: https://n8n.io/cloud/
- Configure proper authentication
- Set up workflow monitoring

### Frontend

- Serve static files with nginx
- Enable HTTPS
- Configure CORS properly
- Add analytics

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name wahat-al-jazzat.com;

    # Customer dashboard
    location / {
        root /path/to/frontend/customer;
        index index.html;
    }

    # Kitchen display
    location /kitchen {
        alias /path/to/frontend/kitchen;
        index index.html;
    }

    # API proxy
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # WebSocket proxy
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Troubleshooting

### Database Connection Issues

```bash
# Check MySQL is running
sudo systemctl status mysql

# Test connection
mysql -u root -p -h localhost

# Check credentials in .env
cat .env | grep DB_
```

### n8n Workflow Not Running

1. Check n8n is running: http://localhost:5678
2. Verify workflow is active (green icon)
3. Check credentials are configured
4. View execution logs in n8n

### Frontend Can't Connect to API

1. Check API server is running: http://localhost:8000/health
2. Check CORS configuration
3. Verify API_BASE URL in HTML files
4. Check browser console for errors

### WebSocket Connection Failing

1. Verify ws:// protocol (not https)
2. Check firewall settings
3. Ensure WebSocket endpoint is accessible
4. Review browser console for specific errors

## Security Considerations

1. **API Authentication** - Add JWT or API key authentication
2. **Input Validation** - Validate all user inputs
3. **SQL Injection** - Use parameterized queries (already implemented)
4. **HTTPS** - Use SSL/TLS in production
5. **Rate Limiting** - Implement rate limiting on API endpoints
6. **Database Access** - Restrict database user permissions

## Monitoring & Logging

### API Server Logs

```bash
# View logs
tail -f execution/api/server.log

# Enable debug logging
export LOG_LEVEL=DEBUG
```

### n8n Workflow Logs

1. Open n8n UI
2. Click on workflow
3. View "Executions" tab
4. Check individual execution logs

### Database Queries

```sql
-- View recent orders
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;

-- Check active sessions
SELECT COUNT(*) FROM sessions WHERE created_at > DATE_SUB(NOW(), INTERVAL 1 HOUR);

-- Order status distribution
SELECT order_status, COUNT(*) FROM orders GROUP BY order_status;
```

## Performance Optimization

1. **Database Indexes** - Already added in schema
2. **WebSocket Connection Pooling** - Use for multiple kitchen displays
3. **Caching** - Cache menu items and frequently accessed data
4. **Lazy Loading** - Load orders on-demand
5. **CDN** - Serve static files from CDN in production

## Support

For issues or questions:
1. Check logs and error messages
2. Review this documentation
3. Check n8n workflow execution logs
4. Test database queries directly
5. Verify API endpoints with curl/Postman

## Future Enhancements

- [ ] Mobile app for customers
- [ ] SMS notifications for order status
- [ ] Payment gateway integration
- [ ] Customer loyalty program
- [ ] Inventory management
- [ ] Analytics dashboard
- [ ] Multi-location support
- [ ] Delivery tracking
- [ ] Table reservations
- [ ] Voice ordering support
