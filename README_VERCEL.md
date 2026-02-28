# 🚀 Wahat Al Jazzat - Vercel Deployment

Deploy your AI receptionist system to Vercel in minutes!

![Vercel](https://img.shields.io/badge/Vercel-Deploy-black?logo=vercel&style=for-the-badge) ![PlanetScale](https://img.shields.io/badge/PlanetScale-Database-blue?style=for-the-badge) ![n8n](https://img.shields.io/badge/n8n-Automation-orange?style=for-the-badge)

## 🎯 Quick Start (3 Steps)

### 1. Run Deployment Script

**Windows:**
```bash
deploy-vercel.bat
```

**macOS/Linux:**
```bash
chmod +x deploy-vercel.sh
./deploy-vercel.sh
```

### 2. Setup Database & n8n

- **Database**: Create MySQL database (PlanetScale recommended)
- **n8n**: Deploy n8n workflow (n8n Cloud or self-hosted)
- **Environment Variables**: Add credentials to Vercel

### 3. Test Your Site

Open:
- **Customer**: `https://your-project.vercel.app/customer`
- **Kitchen**: `https://your-project.vercel.app/kitchen`

## 📋 Prerequisites

| Service | What it's for | Cost | Setup Time |
|----------|---------------|-------|------------|
| **Vercel** | Hosting (frontend + API) | Free tier | 2 min |
| **PlanetScale** | MySQL database | Free tier | 5 min |
| **n8n Cloud** | AI workflow automation | Free trial then $20/mo | 10 min |
| **Anthropic API** | AI chat responses | Pay per use | 2 min |

### Total Setup Time: **~20 minutes**
### Monthly Cost: **$0 - $50** depending on traffic

## 📁 Project Structure for Vercel

```
.
├── vercel.json                  # Vercel configuration
├── api/
│   └── index.py               # Serverless API functions
├── frontend/
│   ├── customer/
│   │   └── index.html         # Customer chat interface
│   └── kitchen/
│       └── index.html         # Kitchen display
├── execution/database/
│   └── schema.sql            # Database schema
├── workflows/
│   └── ai_receptionist_workflow.json  # n8n workflow
└── .env.local                # Environment variables (NEVER commit)
```

## 🔧 Environment Variables

Add these in Vercel Dashboard → Settings → Environment Variables:

```env
# Database (get from PlanetScale or your MySQL provider)
DB_HOST=your-db-host.com
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=wahat_al_jazzat

# n8n (get from n8n deployment)
N8N_BASE_URL=https://your-n8n-instance.com

# Anthropic AI (get from console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## 🚦 Deployment Options

### Option A: One-Click Deploy (Recommended)

```bash
# Windows
deploy-vercel.bat

# macOS/Linux
./deploy-vercel.sh
```

**What it does:**
- Checks prerequisites
- Creates `.env.local` template
- Installs Vercel CLI
- Initializes Git (if needed)
- Deploys to Vercel
- Provides next steps

### Option B: Manual Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Import in Vercel Dashboard**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repo
   - Configure settings
   - Add environment variables
   - Click "Deploy"

3. **Done!** Vercel will provide your URL

### Option C: Continuous Integration

Every push to `main` branch triggers automatic deployment. Perfect for development!

## 🗄️ Database Setup

### PlanetScale (Recommended)

1. **Create account**: [planetscale.com](https://planetscale.com)
2. **Create database** named `wahat_al_jazzat`
3. **Run schema**:
   ```bash
   pscale shell wahat_al_jazzat < execution/database/schema.sql
   ```
4. **Get connection details** from PlanetScale dashboard
5. **Add to Vercel** as environment variables

### Alternative: Any MySQL Provider

```bash
# AWS RDS, Google Cloud SQL, or any MySQL
mysql -h <host> -u <user> -p <database> < execution/database/schema.sql
```

## 🤖 n8n Workflow Setup

### n8n Cloud (Easiest)

1. **Sign up**: [n8n.io/cloud](https://n8n.io/cloud)
2. **Create new workflow**
3. **Import** from `workflows/ai_receptionist_workflow.json`
4. **Configure credentials**:
   - MySQL database connection
   - Anthropic API key
5. **Activate** workflow (green icon)
6. **Note** the webhook URL

### Self-Hosted n8n

```bash
# Using Docker
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Or deploy to Railway, Render, etc.
```

## 🌐 URL Structure After Deployment

```
https://your-project.vercel.app/
├── /customer          # Customer chat dashboard
├── /kitchen          # Kitchen display system
├── /health            # API health check
├── /menu              # Get menu items
├── /chat              # AI chat endpoint
├── /orders            # Order management
└── /api/*            # All API endpoints
```

## 🎨 Custom Domain

### Use Vercel's Free Domain

Your site is automatically available at:
```
https://your-project-name.vercel.app
```

### Add Custom Domain

1. Go to Vercel Dashboard → Project → Settings → Domains
2. Add your domain (e.g., `restaurant.wahataljazzat.com`)
3. Vercel provides DNS settings
4. Update your domain's DNS records
5. SSL certificate is automatic!

## 📊 Monitoring

### Vercel Dashboard

- **Analytics**: Page views, visitors
- **Deployments**: History and logs
- **Functions**: Execution times and errors
- **Edge Network**: Global distribution

### Database Monitoring

PlanetScale dashboard shows:
- Query performance
- Connection count
- Storage usage
- Read/write operations

### n8n Monitoring

- **Execution logs**: See all AI conversations
- **Error tracking**: Debug issues
- **Performance metrics**: Response times

## 🐛 Troubleshooting

### Issue: "Database connection failed"

**Checklist:**
- [ ] Database is publicly accessible (not localhost)
- [ ] Environment variables in Vercel are correct
- [ ] Database user has proper permissions
- [ ] PlanetScale branch is deployed

**Test:**
```bash
curl https://your-project.vercel.app/health
```

### Issue: "n8n webhook not working"

**Checklist:**
- [ ] n8n workflow is active (green icon)
- [ ] `N8N_BASE_URL` is correct in Vercel
- [ ] n8n can reach Vercel (test webhook manually)
- [ ] Check n8n execution logs

**Test:**
```bash
curl -X POST https://your-n8n.com/webhook/test
```

### Issue: "Kitchen not updating"

**Note:** Kitchen display uses polling (every 5s) instead of WebSockets on Vercel.

**Checklist:**
- [ ] Wait 5 seconds for refresh
- [ ] Check browser console for errors
- [ ] Test API: `/orders`
- [ ] Verify database has orders

### Issue: "CORS errors"

**Solutions:**
1. API includes CORS headers
2. Use HTTPS (Vercel default)
3. Clear browser cache
4. Check if custom headers are blocking

## 🔒 Security Checklist

- [x] Environment variables in Vercel (not in code)
- [x] HTTPS enabled (Vercel automatic)
- [x] Parameterized SQL queries (no injection)
- [x] Input validation
- [ ] Rate limiting (add in production)
- [ ] API authentication (add for production)
- [ ] Regular database backups

## 📈 Scaling

### Handling More Traffic

**Vercel automatically scales:**
- Serverless functions scale instantly
- Edge network distributes globally
- No manual scaling needed

**Database:**
- PlanetScale handles millions of queries
- Automatic sharding
- Connection pooling

**n8n:**
- Upgrade to higher plan if needed
- Or use multiple workflow instances

## 💰 Cost Breakdown

| Service | Free Tier | Paid Options |
|----------|------------|--------------|
| **Vercel** | 100GB bandwidth, 10k invocations/mo | $20/mo starts |
| **PlanetScale** | 5GB, 10B reads, 1B writes | $39/mo starts |
| **n8n** | 5k executions/mo trial | $20/mo starts |
| **Anthropic** | Pay per token (~$0.003/chat) | - |
| **Total** | **$0 - $20/mo** | **$20 - $100/mo** |

## 🔄 Updates

### Updating the Application

```bash
# Make changes
git add .
git commit -m "Update menu items"
git push

# Vercel automatically deploys! 🎉
```

### Updating Database Schema

```bash
# Create migration file
# Apply changes
pscale shell wahat_al_jazzat < migration.sql
```

### Updating n8n Workflow

1. Edit in n8n dashboard
2. Save changes
3. Reactivate workflow
4. No code changes needed!

## 📚 Documentation

- [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) - Detailed deployment guide
- [directives/wahat_receptionist.md](directives/wahat_receptionist.md) - System documentation
- [WAHAT_README.md](WAHAT_README.md) - Original project README

## 🎓 Learning Resources

- [Vercel Docs](https://vercel.com/docs)
- [PlanetScale Docs](https://docs.planetscale.com)
- [n8n Docs](https://docs.n8n.io)
- [Anthropic Docs](https://docs.anthropic.com)

## 🆘 Support

1. Check deployment logs in Vercel dashboard
2. Review n8n execution logs
3. Test API endpoints with curl/Postman
4. Check database connectivity
5. Review [troubleshooting section](#-troubleshooting)

## ✨ Features Included

### Customer Dashboard
- ✅ AI-powered chat receptionist
- ✅ Interactive menu browsing
- ✅ One-click ordering
- ✅ Real-time order tracking
- ✅ Beautiful, responsive design

### Kitchen Display
- ✅ Real-time order display (polling)
- ✅ One-click status updates
- ✅ Order filtering
- ✅ Time tracking
- ✅ Priority indicators

### Backend
- ✅ Vercel serverless functions
- ✅ MySQL database integration
- ✅ n8n workflow automation
- ✅ Claude AI integration
- ✅ RESTful API

---

## 🎉 You're All Set!

Your Wahat Al Jazzat AI Receptionist is ready for Vercel deployment!

**Questions?** Check the detailed [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

**Ready to deploy?** Run the deployment script and follow the prompts!
