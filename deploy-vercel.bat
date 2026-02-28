@echo off
REM Vercel Deployment Script for Wahat Al Jazzat AI Receptionist

echo ========================================
echo Wahat Al Jazzat - Vercel Deployment
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo [1/5] Initializing Git repository...
    git init
    if errorlevel 1 (
        echo [ERROR] Failed to initialize git
        pause
        exit /b 1
    )
    echo [+] Git repository initialized
    echo.
) else (
    echo [1/5] Git repository already exists
    echo.
)

REM Check if .env.local exists
if not exist .env.local (
    echo [!] .env.local file not found
    echo [!] Creating template .env.local file...
    (
        echo # Database Configuration
        echo DB_HOST=your-db-host.com
        echo DB_USER=your-db-user
        echo DB_PASSWORD=your-db-password
        echo DB_NAME=wahat_al_jazzat
        echo.
        echo # n8n Configuration
        echo N8N_BASE_URL=https://your-n8n-instance.com
        echo ANTHROPIC_API_KEY=sk-ant-your-key-here
    ) > .env.local
    echo [+] Created .env.local template
    echo.
    echo [!] IMPORTANT: Edit .env.local with your actual credentials
    echo [!] Then run this script again
    echo.
    pause
    exit /b 0
)

REM Check if Vercel CLI is installed
where vercel >nul 2>&1
if errorlevel 1 (
    echo [2/5] Installing Vercel CLI...
    npm install -g vercel
    if errorlevel 1 (
        echo [ERROR] Failed to install Vercel CLI
        pause
        exit /b 1
    )
    echo [+] Vercel CLI installed
    echo.
) else (
    echo [2/5] Vercel CLI already installed
    echo.
)

REM Check if logged in
vercel whoami >nul 2>&1
if errorlevel 1 (
    echo [!] You are not logged in to Vercel
    echo [!] Please login:
    vercel login
    if errorlevel 1 (
        echo [ERROR] Failed to login to Vercel
        pause
        exit /b 1
    )
    echo [+] Logged in to Vercel
    echo.
) else (
    echo [3/5] Already logged in to Vercel
    echo.
)

REM Add and commit files
echo [4/5] Preparing files for deployment...
git add .
git commit -m "Deploy to Vercel - Wahat Al Jazzat AI Receptionist"
if errorlevel 1 (
    echo [!] No changes to commit or git error
    echo [!] Continuing with deployment...
) else (
    echo [+] Files committed
)
echo.

REM Deploy to Vercel
echo [5/5] Deploying to Vercel...
echo.
echo This will:
echo 1. Create a new Vercel project (if needed)
echo 2. Detect and use vercel.json configuration
echo 3. Deploy your website
echo 4. Provide you with the deployment URL
echo.
echo Press any key to continue...
pause >nul
echo.

vercel

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Setup your MySQL database:
echo    - Use PlanetScale (recommended): https://planetscale.com
echo    - Or any MySQL provider
echo    - Run: execution/database/schema.sql
echo.
echo 2. Deploy n8n workflow:
echo    - Use n8n Cloud: https://n8n.io/cloud/
echo    - Or self-host n8n
echo    - Import: workflows/ai_receptionist_workflow.json
echo.
echo 3. Configure environment variables:
echo    - Go to Vercel project settings
echo    - Add all variables from .env.local
echo.
echo 4. Test your deployment:
echo    - Customer: https://your-project.vercel.app/customer
echo    - Kitchen: https://your-project.vercel.app/kitchen
echo.
echo For detailed instructions, see: VERCEL_DEPLOYMENT.md
echo.
echo ========================================
pause
