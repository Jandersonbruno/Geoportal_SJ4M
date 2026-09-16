<#
.SYNOPSIS
  Publica as alteracoes do Geoportal no GitHub (e, por consequencia, no GitHub Pages).

.EXAMPLE
  .\publicar.ps1 "Ajusta cor da camada de lotes"
#>
param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$Mensagem
)

$ErrorActionPreference = "Stop"

Write-Host "==> Verificando alteracoes..." -ForegroundColor Cyan
git status --short

$resposta = Read-Host "`nConfirma o envio dessas alteracoes para o GitHub? (s/n)"
if ($resposta -ne "s") {
  Write-Host "Cancelado." -ForegroundColor Yellow
  exit 0
}

git add -A
git commit -m $Mensagem
git push

Write-Host "`n==> Publicado! O GitHub Pages atualiza em ate ~1 minuto:" -ForegroundColor Green
Write-Host "    https://jandersonbruno.github.io/Geoportal_SJ4M/" -ForegroundColor Green
