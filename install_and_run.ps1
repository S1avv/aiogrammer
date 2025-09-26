Param(
  [switch]$Force
)

$ErrorActionPreference = 'Stop'

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Error "Python is required but not found in PATH. Please install Python 3.12+."
}

if (-not (Get-Command pipx -ErrorAction SilentlyContinue)) {
  Write-Host "pipx not found, installing via pip for current user..."
  python -m pip install --user --upgrade pipx
}

$pipxCmd = (Get-Command pipx -ErrorAction SilentlyContinue)
if ($null -ne $pipxCmd) {
  $PIPX = 'pipx'
} else {
  $PIPX = 'python -m pipx'
}

$installArgs = 'install', '.'
if ($Force) { $installArgs = @('install', '--force', '.') }

& $PIPX @installArgs

try {
  & aiogrammer --help | Out-Host
} catch {
  Write-Warning "aiogrammer is not on PATH yet. Running 'pipx ensurepath'..."
  & $PIPX ensurepath | Out-Host
  Write-Host "Please open a new terminal session and run: aiogrammer --help"
}