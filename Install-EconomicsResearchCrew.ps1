[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$VaultPath = "D:\TaxWiki",
    [switch]$WithUpstream,
    [string]$RepoUrl = ""
)
$ErrorActionPreference = "Stop"

function Copy-NoOverwrite([string]$Source, [string]$Destination) {
    if (-not (Test-Path $Source)) { return }
    foreach ($f in Get-ChildItem -LiteralPath $Source -Recurse -File -Force) {
        $rel = $f.FullName.Substring($Source.TrimEnd('\').Length).TrimStart('\')
        $dest = Join-Path $Destination $rel
        if (Test-Path $dest) { Write-Host "  跳过(已存在): $rel" -ForegroundColor Yellow; continue }
        if ($PSCmdlet.ShouldProcess($dest, "复制")) {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
            Copy-Item -LiteralPath $f.FullName -Destination $dest
        }
    }
}

$VaultPath = [System.IO.Path]::GetFullPath($VaultPath)
if (-not (Test-Path $VaultPath -PathType Container)) { throw "知识库目录不存在：$VaultPath" }
$packageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$payload = Join-Path $packageRoot "payload"
if (-not (Test-Path $payload)) { throw "未找到 payload 目录，请完整解压安装包。" }
$claudeDir = Join-Path $VaultPath ".claude"

# 1. 备份
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = Join-Path $VaultPath "_erc-backups\$stamp"
foreach ($rel in @("CLAUDE.md", ".mcp.json", ".claude\settings.json")) {
    $src = Join-Path $VaultPath $rel
    if (Test-Path $src -PathType Leaf) {
        $dst = Join-Path $backupDir $rel
        if ($PSCmdlet.ShouldProcess($src, "备份到 $dst")) {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
            Copy-Item -LiteralPath $src -Destination $dst
        }
    }
}

# 2. 可选：上游框架，隔离构建，只取 agents/skills/references
$importLines = @()
if ($WithUpstream) {
    if (-not $RepoUrl) { throw "-WithUpstream 需要同时指定 -RepoUrl（上游 My-Brain-Is-Full-Crew 的 Git 地址）。" }
    foreach ($c in "git","bash.exe","jq") { if (-not (Get-Command $c -ErrorAction SilentlyContinue)) { throw "缺少命令：$c" } }
    $repoPath  = Join-Path $VaultPath "_vendor\My-Brain-Is-Full-Crew"
    $stagePath = Join-Path $VaultPath "_erc-staging"
    if (Test-Path $stagePath) { throw "临时目录已存在：$stagePath，请先检查后手动移走。" }
    if (-not (Test-Path (Join-Path $repoPath ".git"))) {
        if (Test-Path $repoPath) { throw "$repoPath 已存在但不是 Git 仓库。" }
        if ($PSCmdlet.ShouldProcess($RepoUrl, "git clone")) {
            git clone --depth 1 $RepoUrl $repoPath
            if ($LASTEXITCODE -ne 0) { throw "git clone 失败" }
        }
    }
    $launch = Join-Path $repoPath "scripts\launchme.sh"
    if ((Test-Path $launch) -and $PSCmdlet.ShouldProcess($stagePath, "构建上游 Crew")) {
        Write-Host "请先人工审阅 $launch 的参数；下面的 --platform/--target 参数未经本包验证。" -ForegroundColor Yellow
        $cyg = (Get-Command cygpath.exe -ErrorAction Stop).Source
        $ru = (& $cyg -u $repoPath).Trim(); $su = (& $cyg -u $stagePath).Trim()
        & (Get-Command bash.exe).Source -lc "cd '$ru' && bash scripts/launchme.sh --platform claude-code --target '$su'"
        if ($LASTEXITCODE -ne 0) { throw "上游构建失败；知识库未被改动。" }
        foreach ($d in "agents","skills","references") {
            Copy-NoOverwrite (Join-Path $stagePath ".claude\$d") (Join-Path $claudeDir $d)
        }
        $disp = Join-Path $stagePath "CLAUDE.md"
        $dispDest = Join-Path $claudeDir "MBIFC-DISPATCHER.md"
        if ((Test-Path $disp) -and -not (Test-Path $dispDest)) {
            Copy-Item $disp $dispDest
            $importLines += "@.claude/MBIFC-DISPATCHER.md"
        }
    }
}
$importLines += "@.claude/ECONOMICS-RESEARCH.md"

# 3. 本扩展
Copy-NoOverwrite (Join-Path $payload ".claude") $claudeDir
Copy-NoOverwrite (Join-Path $payload "Meta") (Join-Path $VaultPath "Meta")
Copy-NoOverwrite (Join-Path $payload "Templates") (Join-Path $VaultPath "Templates")

# 4. 根 CLAUDE.md 仅追加缺失的 import
$rootClaude = Join-Path $VaultPath "CLAUDE.md"
$enc = [System.Text.UTF8Encoding]::new($false)
if (-not (Test-Path $rootClaude)) {
    if ($PSCmdlet.ShouldProcess($rootClaude, "新建")) {
        $tpl = Join-Path $payload "CLAUDE.template.md"
        $body = if (Test-Path $tpl) { (Get-Content -LiteralPath $tpl -Raw).TrimEnd() } else { "# TaxWiki Research Workspace" }
        $extra = @($importLines | Where-Object { $body -notmatch [regex]::Escape($_) })
        if ($extra.Count -gt 0) { $body += "`r`n`r`n" + ($extra -join "`r`n") }
        [IO.File]::WriteAllText($rootClaude, $body + "`r`n", $enc)
    }
} else {
    $existing = Get-Content -LiteralPath $rootClaude -Raw
    $missing = @($importLines | Where-Object { $existing -notmatch [regex]::Escape($_) })
    if ($missing.Count -gt 0 -and $PSCmdlet.ShouldProcess($rootClaude, "追加 import")) {
        [IO.File]::WriteAllText($rootClaude, $existing.TrimEnd() + "`r`n`r`n" + ($missing -join "`r`n") + "`r`n", $enc)
    }
}

# 5. 研究目录（仅新建，不移动现有内容）
foreach ($d in "00-Inbox","01-Research-Projects","03-Literature","04-Theories","05-Methods",
               "06-Data\raw","06-Data\processed","06-Data\metadata","07-Code\python","07-Code\R","07-Code\stata",
               "08-Research-Notes","09-Writing","10-Archive","MOC") {
    $p = Join-Path $VaultPath $d
    if (-not (Test-Path $p) -and $PSCmdlet.ShouldProcess($p, "创建目录")) { New-Item -ItemType Directory -Force -Path $p | Out-Null }
}
Write-Host "完成。备份：$backupDir 。请运行 Test-EconomicsResearchCrew.ps1。" -ForegroundColor Green
