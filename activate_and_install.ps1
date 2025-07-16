# PowerShell script to activate virtual environment and install dependencies

Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Installing dependencies from requirements.txt..."
python -m pip install -r requirements.txt

Write-Host "Done."
