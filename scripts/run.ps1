# Start backend server
Start-Process powershell {
    Set-Location backend
    .\venv\Scripts\Activate
    uvicorn app.main:app --host 0.0.0.0 --port 8000
}

# Start frontend server
Start-Process powershell {
    Set-Location frontend
    npm start
}