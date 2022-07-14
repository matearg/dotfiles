# set PowerShell to UTF-8
[console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding 

# Imported Modules
Import-Module -Name Terminal-Icons
Import-Module -Name PSReadLine
Import-Module -Name posh-git

# Alias
Set-Alias ll Get-ChildItem
Set-Alias re Rename-Item
Set-Alias g git
Set-Alias gg lazygit
Set-Alias vim nvim
Set-Alias v nvim
Set-Alias at alacritty-themes

# PSReadLine
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -EditMode Windows
Set-PSReadLineOption -PredictionViewStyle List

# Prompt
Clear-Host

# Starship
Invoke-Expression (&starship init powershell)

# Oh my Posh
# oh-my-posh --init --shell pwsh --config ~\github\dotfiles\powershell\ohmyposh-themes\mynegligible2.omp.json | Invoke-Expression
# oh-my-posh --init --shell pwsh --config ~\scoop\apps\oh-my-posh\current\themes\clean-detailed.omp.json | Invoke-Expression

# Utilities
function which ($command) {
  Get-Command -Name $command -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty Path -ErrorAction SilentlyContinue
}
