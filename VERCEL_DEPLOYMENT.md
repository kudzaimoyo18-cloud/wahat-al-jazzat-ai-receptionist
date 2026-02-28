# Vercel Deployment Guide - Wahat Al Jazzat AI Receptionist

## Overview

This guide will help you deploy the Wahat Al Jazzat AI Receptionist system to Vercel.

## Prerequisites

Before deploying, you need:

1. **Vercel Account** - Free at [vercel.com](https://vercel.com)
2. **GitHub Account** - For automatic deployments
3. **MySQL Database** - Use one of these options:
   - PlanetScale (recommended for Vercel)
   - Neon (PostgreSQL, modify schema accordingly)
   - AWS RDS
   - Google Cloud SQL
   - Or any MySQL database with public IP
4. **n8n Instance** - Hosted options:
   - [n8n Cloud](https://n8n.io/cloud/)
   - Self-hosted on your server
   - Railway, Render, or other hosting platforms
5. **Anthropic API Key** - From [console.anthropic.com](https://console.anthropic.com)

## Step 1: Database Setup

### Option A: PlanetScale (Recommended for Vercel)

1. Create account at [planetscale.com](https://planetscale.com)
2. Create a new database named `wahat_al_jazzat`
3. Get connection details:
   - Host
   - Username
   - Password
   - Database name

4. Run the schema:
   ```bash
   # Using PlanetScale CLI
   pscale shell wahat_al_jazzat < execution/database/schema.sql
   ```

### Option B: Other MySQL Providers

1. Create MySQL database
2. Run the schema:
   ```bash
   mysql -h <host> -u <user> -p < database_name < execution/database/schema.sql
   ```

### Important: Database Security

- Whitelist Vercel's IP ranges
- Use environment variables for credentials
- Enable SSL connections
- Set up regular backups

## Step 2: Deploy n8n

### Option A: n8n Cloud (Easiest)

1. Sign up at [n8n.io/cloud](https://n8n.io/cloud)
2. Create a new workflow
3. Import the workflow from `workflows/ai_receptionist_workflow.json`
4. Configure credentials:
   - MySQL database connection
   - Anthropic API key
5. Activate the workflow
6. Note the webhook URLs

### Option B: Self-Hosted n8n

1. Deploy n8n to your server:
   ```bash
   docker run -it --rm \
     --name n8n \
     -p 5678:5678 \
     -v ~/.n8n:/home/node/.n8n \
     n8nio/n8n
   ```

2. Set up SSL/TLS (Use Let's Encrypt or Cloudflare)
3. Import and configure workflow
4. Note the webhook URL

### n8n Workflow Updates for Production

Update these URLs in the n8n workflow:

```json
{
  "N8N_BASE_URL": "https://your-n8n-instance.com"
}
```

## Step 3: Prepare for Vercel Deployment

### 1. Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Wahat Al Jazzat AI Receptionist"

# Create GitHub repository and push
# Follow GitHub's instructions to add remote
git remote add origin https://github.com/YOUR_USERNAME/wahat-al-jazzat.git
git branch -M main
git push -u origin main
```

### 2. Install Vercel CLI

```bash
npm install -g vercel
```

### 3. Create .env.local

Create `.env.local` in project root:

```env
# Database (get from your MySQL provider)
DB_HOST=your-db-host.com
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=wahat_al_jazzat

# n8n
N8N_BASE_URL=https://your-n8n-instance.com
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

⚠️ **Never commit `.env.local` to git!**

## Step 4: Deploy to Vercel

### Method A: Using Vercel CLI (Recommended)

```bash
# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# ? Set up and deploy? Yes
# ? Which scope? Your account
# ? Link to existing project? No
# ? Project name: wahat-al-jazzat
# ? In which directory is your code? ./
# ? Want to override settings? No
```

Vercel will detect the configuration and deploy.

### Method B: Using Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: Leave empty
   - **Output Directory**: `frontend/customer`
4. Add Environment Variables:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
   - `N8N_BASE_URL`
   - `ANTHROPIC_API_KEY`
5. Click **Deploy**

### Method C: Automatic GitHub Integration

1. Go to Vercel Dashboard
2. Click **Add New Project**
3. Import from GitHub
4. Vercel will automatically deploy on every push to `main` branch

## Step 5: Configure Domain (Optional)

### Use Vercel's Default Domain

Your site will be available at:
```
https://wahat-al-jazzat.vercel.app
```

### Use Custom Domain

1. Go to project settings in Vercel
2. Click **Domains**
3. Add your domain (e.g., `restaurant.wahataljazzat.com`)
4. Follow DNS instructions

## Step 6: Update n8n Workflow

After deployment, update the n8n workflow:

1. Get your Vercel API URL: `https://your-domain.vercel.app`
2. In n8n workflow, update webhook URLs to point to your Vercel instance
3. Reactivate the workflow

## Step 7: Test the Deployment

### Customer Dashboard
```
https://your-domain.vercel.app/customer
```

### Kitchen Display
```
https://your-domain.vercel.app/kitchen
```

### API Health Check
```bash
curl https://your-domain.vercel.app/health
```

### Test Menu API
```bash
curl https://your-domain.vercel.app/menu
```

## Architecture on Vercel

```
┌─────────────────────────────────────────────────┐
│  Vercel (Frontend + Serverless Functions)     │
│  ├─ /customer → frontend/customer/index.html    │
│  ├─ /kitchen → frontend/kitchen/index.html    │
│  └─ /api/* → Vercel Serverless Functions    │
└──────────────────┬──────────────────────────────┘
                   │
                   ├──────────────┬──────────────┐
                   ↓              ↓              ↓
            ┌─────────┐   ┌──────────┐  ┌──────────┐
            │  n8n    │   │  MySQL   │  │ Anthropic│
            │ (Cloud)  │   │(PlanetScale│ │  Claude   │
            └─────────┘   └──────────┘  └──────────┘
```

## Environment Variables Reference

### Required for Vercel

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | Database host | `aws.connect.psdb.cloud` |
| `DB_USER` | Database username | `your_user` |
| `DB_PASSWORD` | Database password | `your_password` |
| `DB_NAME` | Database name | `wahat_al_jazzat` |
| `N8N_BASE_URL` | n8n instance URL | `https://your-n8n.com` |
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-xxxxx` |

### Optional for Development

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |

## Monitoring & Debugging

### Vercel Logs

```bash
# View deployment logs
vercel logs

# View specific deployment
vercel logs <deployment-url>
```

### Database Queries

```sql
-- Check active sessions
SELECT COUNT(*) FROM sessions
WHERE created_at > DATE_SUB(NOW(), INTERVAL 1 HOUR);

-- Recent orders
SELECT * FROM orders
ORDER BY created_at DESC LIMIT 10;

-- Order statistics
SELECT order_status, COUNT(*)
FROM orders
GROUP BY order_status;
```

### n8n Executions

1. Open n8n dashboard
2. Click on the workflow
3. View "Executions" tab
4. Check for errors or failed executions

## Troubleshooting

### Issue: Database Connection Failed

**Symptom**: API returns 500 errors

**Solutions**:
1. Check database is publicly accessible
2. Verify environment variables in Vercel dashboard
3. Ensure database user has correct permissions
4. Check if SSL is required

### Issue: n8n Webhook Not Reaching API

**Symptom**: Orders not created in database

**Solutions**:
1. Check n8n webhook URL is correct
2. Verify Vercel environment variables include `N8N_BASE_URL`
3. Check n8n execution logs for errors
4. Test webhook manually with curl

### Issue: CORS Errors

**Symptom**: Browser shows CORS errors in console

**Solutions**:
1. API already includes CORS headers
2. Check Vercel deployment is using HTTPS
3. Clear browser cache
4. Check if custom headers are blocking requests

### Issue: Kitchen Display Not Updating

**Symptom**: Orders not showing in kitchen display

**Solutions**:
1. Kitchen display uses polling (every 5 seconds)
2. Check browser console for errors
3. Verify API is responding: `/orders`
4. Check database has pending orders

## Performance Optimization

### Vercel Specific

1. **Enable Edge Functions** for faster response:
   ```json
   {
     "functions": {
       "api/**/*.py": {
         "runtime": "python3.9",
         "memory": 1024,
         "maxDuration": 10
       }
     }
   }
   ```

2. **Cache Menu Items** - Menu doesn't change often, add caching

3. **Use Edge Network** - Deploy closer to users

### Database Optimization

1. Add indexes (already in schema)
2. Use connection pooling
3. Enable query cache
4. Monitor slow queries

## Security Best Practices

1. **Environment Variables** - Never commit secrets
2. **HTTPS Only** - Vercel provides this automatically
3. **Rate Limiting** - Implement on API endpoints
4. **Input Validation** - Already in place
5. **SQL Injection Protection** - Using parameterized queries
6. **Regular Updates** - Keep dependencies updated

## Cost Estimate

### Vercel (Free Tier)
- 100GB bandwidth/month
- 10 serverless function invocations/month
- Perfect for testing and small restaurants

### PlanetScale (Free Tier)
- 5GB storage
- 10B reads/month
- 1B writes/month

### n8n Cloud (Free Trial)
- 5,000 workflow executions/month
- Then starts at $20/month

### Anthropic Claude
- Pay per token usage
- ~$0.003 per message
- Very affordable for restaurant use

**Total Estimated Cost**: $0 - $50/month depending on traffic

## Backup & Recovery

### Database Backups

PlanetScale provides automated backups. For other providers:

```bash
# Backup MySQL database
mysqldump -h <host> -u <user> -p <database> > backup.sql

# Restore
mysql -h <host> -u <user> -p <database> < backup.sql
```

### n8n Workflow Backup

1. Export workflow regularly
2. Save to GitHub
3. Use version control

## Support

For issues:
1. Check [Vercel Documentation](https://vercel.com/docs)
2. Review [n8n Documentation](https://docs.n8n.io)
3. Check this deployment guide
4. Review error logs

---

**Your Wahat Al Jazzat AI Receptionist is now live on Vercel!** 🎉
