# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install backend dependencies
Set-Location backend
pip install -r requirements.txt

# Install frontend dependencies
Set-Location ..\frontend
npm install

# Return to root directory
Set-Location ..