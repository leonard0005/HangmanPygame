# PowerShell script to organize Hangman project files
# Run this script from the project root directory

Write-Host "Organizing Hangman project files..." -ForegroundColor Green

# Create a backup of the original file structure
Write-Host "Creating backup..." -ForegroundColor Yellow
if (!(Test-Path "backup")) {
    New-Item -ItemType Directory -Path "backup"
}
Copy-Item "*.png" "backup\" -ErrorAction SilentlyContinue
Copy-Item "*.mp3" "backup\" -ErrorAction SilentlyContinue
Copy-Item "*.TTF" "backup\" -ErrorAction SilentlyContinue
Copy-Item "*.txt" "backup\" -ErrorAction SilentlyContinue

# Move font files
Write-Host "Moving font files..." -ForegroundColor Cyan
Move-Item "PIXELADE.TTF" "assets\fonts\" -ErrorAction SilentlyContinue

# Move dictionary file
Write-Host "Moving dictionary file..." -ForegroundColor Cyan
Move-Item "Dictionary.txt" "data\" -ErrorAction SilentlyContinue

# Move screen images
Write-Host "Moving screen images..." -ForegroundColor Cyan
Move-Item "TitleScreen_Hangman.png" "assets\images\screens\" -ErrorAction SilentlyContinue
Move-Item "GameScreen.png" "assets\images\screens\" -ErrorAction SilentlyContinue
Move-Item "VictoryScreen.png" "assets\images\screens\" -ErrorAction SilentlyContinue
Move-Item "InstructionsBoard*.png" "assets\images\screens\" -ErrorAction SilentlyContinue

# Move hangman images
Write-Host "Moving hangman images..." -ForegroundColor Cyan
Move-Item "Error1.*.png" "assets\images\hangman\" -ErrorAction SilentlyContinue

# Move UI images
Write-Host "Moving UI images..." -ForegroundColor Cyan
Move-Item "RevealSignBoard.png" "assets\images\ui\" -ErrorAction SilentlyContinue
Move-Item "KeyboardSignBoard.png" "assets\images\ui\" -ErrorAction SilentlyContinue
Move-Item "CountDownBlackOut.png" "assets\images\ui\" -ErrorAction SilentlyContinue
Move-Item "FullWordGuessPopUp.png" "assets\images\ui\" -ErrorAction SilentlyContinue

# Move button images
Write-Host "Moving button images..." -ForegroundColor Cyan
Move-Item "Normal*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue
Move-Item "Hover*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue
Move-Item "Press*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue
Move-Item "play*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue
Move-Item "Music*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue
Move-Item "Sound*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue
Move-Item "FullWordGuessButton*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue
Move-Item "UI_Flat_Select_*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue
Move-Item "VictoryScreenButton*.png" "assets\images\buttons\" -ErrorAction SilentlyContinue

# Move music files
Write-Host "Moving music files..." -ForegroundColor Cyan
Move-Item "Indiana Jones Main Theme.mp3" "assets\audio\music\" -ErrorAction SilentlyContinue
Move-Item "Indy's Fanfare.mp3" "assets\audio\music\" -ErrorAction SilentlyContinue
Move-Item "GameplayDesperateSituation.mp3" "assets\audio\music\" -ErrorAction SilentlyContinue
Move-Item "InstructionsScreen-Map.mp3" "assets\audio\music\" -ErrorAction SilentlyContinue
Move-Item "VictoryScreen-Indy and Sophia's Kiss.mp3" "assets\audio\music\" -ErrorAction SilentlyContinue
Move-Item "LooseScreen-Ominous Feeling.mp3" "assets\audio\music\" -ErrorAction SilentlyContinue

# Move sound effect files
Write-Host "Moving sound effect files..." -ForegroundColor Cyan
Move-Item "BigButtonPressFX.mp3" "assets\audio\sfx\" -ErrorAction SilentlyContinue
Move-Item "CountDownSFX.mp3" "assets\audio\sfx\" -ErrorAction SilentlyContinue
Move-Item "LooseLifeFX.mp3" "assets\audio\sfx\" -ErrorAction SilentlyContinue
Move-Item "LightSwitchFX.mp3" "assets\audio\sfx\" -ErrorAction SilentlyContinue
Move-Item "KeyboardTypingFX.mp3" "assets\audio\sfx\" -ErrorAction SilentlyContinue
Move-Item "BlockedFX.mp3" "assets\audio\sfx\" -ErrorAction SilentlyContinue

Write-Host "File organization complete!" -ForegroundColor Green
Write-Host "Your project is now organized and ready for GitHub!" -ForegroundColor Yellow
Write-Host "You can now run: python src\main.py" -ForegroundColor Cyan
