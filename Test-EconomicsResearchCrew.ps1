[CmdletBinding()]
param([string]$VaultPath = "D:\TaxWiki")
$ErrorActionPreference = "Stop"
$VaultPath = [System.IO.Path]::GetFullPath($VaultPath)
$agents = "literature-agent","theory-agent","tax-policy-agent","econometrics-agent","causal-inference-agent","academic-reviewer"
$skills = "research-question","literature-review","theory-modeling","tax-policy-analysis","causal-inference-audit","econometric-analysis","academic-review"
$errors = @()
function Get-Front([string]$Path) {
    $t = Get-Content -LiteralPath $Path -Raw
    if ($t -notmatch '(?s)^---\r?\n(.*?)\r?\n---') { return $null }
    $h = @{}
    foreach ($l in $Matches[1] -split '\r?\n') { if ($l -match '^([\w-]+):\s*(.*)$') { $h[$Matches[1]] = $Matches[2].Trim('"') } }
    $h
}
foreach ($a in $agents) {
    $p = Join-Path $VaultPath ".claude\agents\$a.md"
    if (-not (Test-Path $p)) { $errors += "缺少 agent: $a"; continue }
    $f = Get-Front $p
    if (-not $f -or $f.name -ne $a -or -not $f.description) { $errors += "agent frontmatter 无效: $a" }
}
foreach ($s in $skills) {
    $p = Join-Path $VaultPath ".claude\skills\$s\SKILL.md"
    if (-not (Test-Path $p)) { $errors += "缺少 skill: $s"; continue }
    $f = Get-Front $p
    if (-not $f -or $f.name -ne $s -or -not $f.description) { $errors += "skill frontmatter 无效: $s" }
}
foreach ($m in ".claude\ECONOMICS-RESEARCH.md","Meta\vault-map.md","Meta\research-standards.md","Meta\source-registry.md","Meta\research-log.md") {
    if (-not (Test-Path (Join-Path $VaultPath $m))) { $errors += "缺少文件: $m" }
}
$rc = Join-Path $VaultPath "CLAUDE.md"
if (-not (Test-Path $rc) -or (Get-Content $rc -Raw) -notmatch [regex]::Escape("@.claude/ECONOMICS-RESEARCH.md")) { $errors += "根 CLAUDE.md 未 import ECONOMICS-RESEARCH.md" }
foreach ($d in "06-Data\raw","06-Data\processed","07-Code") { if (-not (Test-Path (Join-Path $VaultPath $d))) { $errors += "缺少目录: $d" } }
if ($errors.Count -gt 0) { $errors | ForEach-Object { Write-Host " x $_" -ForegroundColor Red }; exit 1 }
Write-Host "结构检查通过（$($agents.Count) agents, $($skills.Count) skills）。仍需在 Claude Code 中用 /agents、/skills 确认可识别。" -ForegroundColor Green
