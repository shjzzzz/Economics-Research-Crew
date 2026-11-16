[CmdletBinding()]
param()
# Regression tests for the Economics Research Crew installer, hooks and lint.
# Run under each host you care about:
#   powershell -NoProfile -File tests\run.ps1   (Windows PowerShell 5.1)
#   pwsh -NoProfile -File tests\run.ps1         (PowerShell 7)
$ErrorActionPreference = "Stop"
$pkg = Split-Path -Parent $PSScriptRoot
$installer = Join-Path $pkg "Install-EconomicsResearchCrew.ps1"
$checker = Join-Path $pkg "Test-EconomicsResearchCrew.ps1"
$payload = Join-Path $pkg "payload"
$py = (Get-Command python -ErrorAction Stop).Source
$enc = [System.Text.UTF8Encoding]::new($false)
# Windows PowerShell 5.1 pipes to native programs in ASCII by default; force UTF-8 so Chinese test input survives
$OutputEncoding = $enc
$shell = (Get-Process -Id $PID).Path
$script:pass = 0; $script:fail = 0

function Get-Sha([string]$Path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $fs = [IO.File]::OpenRead($Path); try { return [BitConverter]::ToString($sha.ComputeHash($fs)).Replace("-","") } finally { $fs.Dispose() } } finally { $sha.Dispose() }
}
function Ok([bool]$cond, [string]$name) {
    if ($cond) { $script:pass++; Write-Host "  PASS $name" -ForegroundColor Green }
    else { $script:fail++; Write-Host "  FAIL $name" -ForegroundColor Red }
}
function New-Vault { $d = Join-Path ([IO.Path]::GetTempPath()) ("erc-test-" + [guid]::NewGuid().ToString("N").Substring(0,8)); New-Item -ItemType Directory $d | Out-Null; $d }
function Run-Install([string]$Vault, [string[]]$Extra = @()) {
    $ErrorActionPreference = "Continue"
    if ($Extra -notcontains "-Platform") { $Extra = @("-Platform","claude") + $Extra }
    & $shell -NoProfile -File $installer -VaultPath $Vault @Extra *> $null
    return $LASTEXITCODE
}
function Run-Check([string]$Vault) { $ErrorActionPreference = "Continue"; & $shell -NoProfile -File $checker -VaultPath $Vault *> $null; return $LASTEXITCODE }
function Snapshot([string]$Vault) {
    Get-ChildItem -LiteralPath $Vault -Recurse -File -Force | Where-Object { $_.FullName -notmatch '_erc-backups' } |
        Sort-Object FullName | ForEach-Object { $_.FullName.Substring($Vault.Length) + ":" + (Get-Sha $_.FullName) }
}
function Hook([string]$Script, [hashtable]$Data) {
    $ErrorActionPreference = "Continue"
    $json = $Data | ConvertTo-Json -Depth 5 -Compress
    $json | & $py -X utf8 (Join-Path $payload ".claude\hooks\$Script") 2>$null
    return $LASTEXITCODE
}

Write-Host "Host: $($PSVersionTable.PSVersion)  python: $(& $py --version)"

# --- 1. fresh install -------------------------------------------------------
Write-Host "[1] fresh install"
$v = New-Vault
Ok ((Run-Install $v) -eq 0) "install exit 0"
Ok ((Run-Check $v) -eq 0) "checker exit 0"
$skillCount = (Get-ChildItem (Join-Path $v ".claude\skills") -Directory).Count
$agentCount = (Get-ChildItem (Join-Path $v ".claude\agents") -Filter *.md).Count
Ok ($skillCount -eq 11) "11 skills (got $skillCount)"
Ok ($agentCount -eq 6) "6 agents (got $agentCount)"
$tpl = [IO.File]::ReadAllText((Join-Path $payload "CLAUDE.template.md")).Replace("`r`n","`n").TrimEnd()
$got = [IO.File]::ReadAllText((Join-Path $v "CLAUDE.md")).Replace("`r`n","`n").TrimEnd()
Ok ($got -eq $tpl) "root CLAUDE.md equals template (UTF-8, no mojibake)"
Ok (Test-Path (Join-Path $v "03-Literature\_sources")) "_sources dir created"

# --- 2. idempotent ----------------------------------------------------------
Write-Host "[2] idempotent"
$before = Snapshot $v
Ok ((Run-Install $v) -eq 0) "second install exit 0"
$after = Snapshot $v
Ok ((($before -join "`n") -eq ($after -join "`n"))) "no file changed on re-install"

# --- 3. existing Chinese CLAUDE.md preserved ---------------------------------
Write-Host "[3] existing CLAUDE.md preserved"
$v3 = New-Vault
$orig = "# 我的 CLAUDE`n中文内容：税收遵从`n"
[IO.File]::WriteAllText((Join-Path $v3 "CLAUDE.md"), $orig, $enc)
Ok ((Run-Install $v3) -eq 0) "install exit 0"
$c = [IO.File]::ReadAllText((Join-Path $v3 "CLAUDE.md"), $enc).Replace("`r`n","`n")
Ok ($c.StartsWith($orig)) "original Chinese content preserved byte-for-byte"
Ok (([regex]::Matches($c, [regex]::Escape("@.claude/ECONOMICS-RESEARCH.md"))).Count -eq 1) "import appended once"
Run-Install $v3 | Out-Null
$c2 = [IO.File]::ReadAllText((Join-Path $v3 "CLAUDE.md"), $enc).Replace("`r`n","`n")
Ok ($c2 -eq $c) "re-run does not duplicate import"
Ok ((Get-ChildItem (Join-Path $v3 "_erc-backups") -Recurse -Filter CLAUDE.md).Count -ge 1) "backup of CLAUDE.md written"

# --- 4. -WhatIf writes nothing ------------------------------------------------
Write-Host "[4] -WhatIf"
$v4 = New-Vault
Ok ((Run-Install $v4 @("-WhatIf")) -eq 0) "WhatIf exit 0"
Ok ((Get-ChildItem -LiteralPath $v4 -Force).Count -eq 0) "WhatIf left vault empty"

# --- 5. -Update writes .new, never overwrites -------------------------------
Write-Host "[5] -Update"
$skill = Join-Path $v ".claude\skills\research-question\SKILL.md"
[IO.File]::AppendAllText($skill, "`nLOCAL EDIT`n", $enc)
$edited = (Get-Sha $skill)
Ok ((Run-Install $v @("-Update")) -eq 0) "update exit 0"
Ok ((Get-Sha $skill) -eq $edited) "edited file not overwritten"
Ok (Test-Path "$skill.new") ".new copy created for differing file"
$newCount = (Get-ChildItem $v -Recurse -Filter *.new -Force | Where-Object { $_.Name -ne "CLAUDE.md.new" }).Count
Ok ($newCount -eq 1) "only the differing file got a .new (got $newCount)"
Ok (-not (Test-Path (Join-Path $v "CLAUDE.md.new"))) "no CLAUDE.md.new when root CLAUDE.md equals template"
$v5 = New-Vault
[IO.File]::WriteAllText((Join-Path $v5 "CLAUDE.md"), "# old`n@.claude/ECONOMICS-RESEARCH.md`n", $enc)
Run-Install $v5 @("-Update") | Out-Null
Ok ((Test-Path (Join-Path $v5 "CLAUDE.md.new")) -and ([IO.File]::ReadAllText((Join-Path $v5 "CLAUDE.md"), $enc)).StartsWith("# old")) "-Update writes CLAUDE.md.new, keeps CLAUDE.md"

# --- 6. -WithHooks merge ------------------------------------------------------
Write-Host "[6] -WithHooks"
$v6 = New-Vault
New-Item -ItemType Directory (Join-Path $v6 ".claude") | Out-Null
$sj = Join-Path $v6 ".claude\settings.json"
[IO.File]::WriteAllText($sj, '{"permissions":{"allow":["Bash(ls)"]}}', $enc)
Ok ((Run-Install $v6 @("-WithHooks")) -eq 0) "install -WithHooks exit 0"
$st = [IO.File]::ReadAllText($sj, $enc) | ConvertFrom-Json
Ok ($st.permissions.allow[0] -eq "Bash(ls)") "existing permissions preserved"
Ok ($null -ne $st.hooks.PreToolUse -and $null -ne $st.hooks.PostToolUse) "hooks present"
$h1 = (Get-Sha $sj)
Run-Install $v6 @("-WithHooks") | Out-Null
Ok ((Get-Sha $sj) -eq $h1) "second merge is idempotent"
Ok ((Run-Check $v6) -eq 0) "checker exit 0 with hooks"
Ok ($st.hooks.PreToolUse[0].matcher -match "PowerShell") "PreToolUse matcher covers PowerShell tool"
# upgrade path: an old install whose matcher lacks PowerShell gets widened, not duplicated
$old = '{"hooks":{"PreToolUse":[{"matcher":"Write|Edit|Bash","hooks":[{"type":"command","command":"python x/protect_raw.py"}]}]}}'
[IO.File]::WriteAllText($sj, $old, $enc)
Run-Install $v6 @("-WithHooks") | Out-Null
$st2 = [IO.File]::ReadAllText($sj, $enc) | ConvertFrom-Json
Ok (@($st2.hooks.PreToolUse).Count -eq 1 -and $st2.hooks.PreToolUse[0].matcher -match "PowerShell") "old matcher widened without duplicating hook"
# without -WithHooks, settings.json is never touched
$v6b = New-Vault
New-Item -ItemType Directory (Join-Path $v6b ".claude") | Out-Null
$sjb = Join-Path $v6b ".claude\settings.json"
[IO.File]::WriteAllText($sjb, '{"a":1}', $enc)
Run-Install $v6b | Out-Null
Ok (([IO.File]::ReadAllText($sjb, $enc)) -eq '{"a":1}') "settings.json untouched without -WithHooks"
# invalid JSON is refused and left untouched
$v6c = New-Vault
New-Item -ItemType Directory (Join-Path $v6c ".claude") | Out-Null
$sjc = Join-Path $v6c ".claude\settings.json"
[IO.File]::WriteAllText($sjc, '{not json', $enc)
$rc = Run-Install $v6c @("-WithHooks")
Ok ($rc -ne 0 -and ([IO.File]::ReadAllText($sjc, $enc)) -eq '{not json') "invalid settings.json refused, untouched"

# --- 7. protect_raw hook ------------------------------------------------------
Write-Host "[7] protect_raw hook"
$rawDir = Join-Path $v "06-Data\raw"
$existing = Join-Path $rawDir "a.csv"
[IO.File]::WriteAllText($existing, "x,y`n1,2`n", $enc)
$proc = Join-Path $v "06-Data\processed\out.csv"
Ok ((Hook "protect_raw.py" @{tool_name="Write"; cwd=$v; tool_input=@{file_path=(Join-Path $rawDir "new.csv")}}) -eq 0) "Write NEW raw file allowed"
Ok ((Hook "protect_raw.py" @{tool_name="Write"; cwd=$v; tool_input=@{file_path=$existing}}) -eq 2) "Write EXISTING raw file blocked"
Ok ((Hook "protect_raw.py" @{tool_name="Edit"; cwd=$v; tool_input=@{file_path=$existing}}) -eq 2) "Edit raw file blocked"
Ok ((Hook "protect_raw.py" @{tool_name="Edit"; cwd=$v; tool_input=@{file_path="06-Data/raw/a.csv"}}) -eq 2) "Edit via relative path blocked"
Ok ((Hook "protect_raw.py" @{tool_name="Write"; cwd=$v; tool_input=@{file_path="03-Literature/_sources/p.pdf"}}) -eq 0) "Write NEW source allowed"
Ok ((Hook "protect_raw.py" @{tool_name="Write"; cwd=$v; tool_input=@{file_path=$proc}}) -eq 0) "Write processed allowed"
Ok ((Hook "protect_raw.py" @{tool_name="Bash"; cwd=$v; tool_input=@{command="rm 06-Data/raw/a.csv"}}) -eq 2) "Bash rm raw blocked"
Ok ((Hook "protect_raw.py" @{tool_name="Bash"; cwd=$v; tool_input=@{command="Remove-Item .\06-Data\raw\a.csv"}}) -eq 2) "PowerShell Remove-Item raw blocked"
Ok ((Hook "protect_raw.py" @{tool_name="Bash"; cwd=$v; tool_input=@{command="echo x > 06-Data/raw/a.csv"}}) -eq 2) "Bash redirect into raw blocked"
Ok ((Hook "protect_raw.py" @{tool_name="Bash"; cwd=$v; tool_input=@{command="cp /tmp/x.csv 06-Data/raw/"}}) -eq 2) "Bash cp into raw blocked"
Ok ((Hook "protect_raw.py" @{tool_name="Bash"; cwd=$v; tool_input=@{command="head -3 06-Data/raw/a.csv"}}) -eq 0) "Bash read of raw allowed"
Ok ((Hook "protect_raw.py" @{tool_name="Bash"; cwd=$v; tool_input=@{command="cp 06-Data/raw/a.csv 06-Data/processed/a.csv"}}) -eq 0) "Bash copy FROM raw allowed"
Ok ((Hook "protect_raw.py" @{tool_name="Bash"; cwd=$v; tool_input=@{command="rm tmp.txt"}}) -eq 0) "unrelated rm allowed"
Ok ((Hook "protect_raw.py" @{tool_name="PowerShell"; cwd=$v; tool_input=@{command="Remove-Item .\06-Data\raw\a.csv"}}) -eq 2) "PowerShell TOOL Remove-Item raw blocked"
Ok ((Hook "protect_raw.py" @{tool_name="PowerShell"; cwd=$v; tool_input=@{command="Get-Content .\06-Data\raw\a.csv"}}) -eq 0) "PowerShell TOOL read raw allowed"
"not json" | & $py -X utf8 (Join-Path $payload ".claude\hooks\protect_raw.py") 2>$null
Ok ($LASTEXITCODE -eq 0) "malformed input fails open"

# --- 8. validate_frontmatter hook ---------------------------------------------
Write-Host "[8] validate_frontmatter hook"
$good = Join-Path $v "08-Research-Notes\good.md"
$bad = Join-Path $v "08-Research-Notes\bad.md"
$tab = Join-Path $v "08-Research-Notes\tab.md"
New-Item -ItemType Directory (Split-Path $good) -Force | Out-Null
[IO.File]::WriteAllText($good, "---`ntype: query`n---`n# ok`n", $enc)
[IO.File]::WriteAllText($bad, "---`ntype: query`n# no closing`n", $enc)
[IO.File]::WriteAllText($tab, "---`ntype: query`n`tx: 1`n---`n", $enc)
Ok ((Hook "validate_frontmatter.py" @{tool_name="Write"; cwd=$v; tool_input=@{file_path=$good}}) -eq 0) "valid frontmatter passes"
Ok ((Hook "validate_frontmatter.py" @{tool_name="Write"; cwd=$v; tool_input=@{file_path=$bad}}) -eq 2) "missing closing --- reported"
Ok ((Hook "validate_frontmatter.py" @{tool_name="Write"; cwd=$v; tool_input=@{file_path=$tab}}) -eq 2) "tab in frontmatter reported"

Remove-Item -LiteralPath $good,$bad,$tab -Force

# --- 8b. routing_hint hook (offline) ----------------------------------------
Write-Host "[8b] routing_hint hook"
function Hint([string]$Prompt) {
    $ErrorActionPreference = "Continue"
    $json = @{prompt=$Prompt} | ConvertTo-Json -Compress
    $out = $json | & $py -X utf8 (Join-Path $payload ".claude\hooks\routing_hint.py") 2>$null
    return ($out -join " ")
}
Ok ((Hint "帮我梳理税收遵从的国内外文献，找出研究缺口") -match "/literature-review") "literature intent -> /literature-review"
Ok ((Hint "我的 DID 平行趋势成立吗") -match "/causal-inference-audit") "DID intent -> /causal-inference-audit"
Ok ((Hint "我想完整做一个研究并推进") -match "/research-pipeline") "project intent -> /research-pipeline"
Ok ((Hint "固定效应和随机效应的核心区别是什么") -eq "") "conceptual question -> no hint"
Ok ((Hint "/literature-review 税收遵从") -eq "") "explicit slash command -> no hint"
# Hosts run hooks as plain `python script.py` (no -X utf8). On Chinese Windows python would decode
# stdin as GBK and no Chinese trigger would ever match; the scripts must read UTF-8 bytes themselves.
function HintPlain([string]$Json) {
    $ErrorActionPreference = "Continue"
    $out = $Json | & $py (Join-Path $payload ".claude\hooks\routing_hint.py") 2>$null
    return ($out -join " ")
}
Ok ((HintPlain (@{prompt="帮我梳理税收遵从的国内外文献"} | ConvertTo-Json -Compress)) -match "/literature-review") "Chinese prompt matches without -X utf8 (Claude host)"
Ok ((HintPlain (@{hookEventName="PreInvocation"; invocationNum=0; lastUserInput="我的 DID 平行趋势成立吗"} | ConvertTo-Json -Compress)) -match "causal-inference-audit") "Chinese prompt matches without -X utf8 (agy host)"

# --- 9. wiki_lint ---------------------------------------------------------------
Write-Host "[9] wiki_lint"
$lint = Join-Path $v ".claude\scripts\wiki_lint.py"
$lit = Join-Path $v "03-Literature"
[IO.File]::WriteAllText((Join-Path $lit "_sources\a.pdf"), "pdf", $enc)
[IO.File]::WriteAllText((Join-Path $lit "good.md"), "---`ntype: literature`nsources: [03-Literature/_sources/a.pdf]`nverification: verified`n---`nsee [[other]]`n", $enc)
[IO.File]::WriteAllText((Join-Path $lit "other.md"), "---`ntype: literature`nsources: [https://doi.org/10.1/x]`nverification: unverified`n---`nback to [[good]]`n", $enc)
[IO.File]::WriteAllText((Join-Path $v "Meta\index.md"), "---`ntype: index`n---`n[[good]] [[other]]`n", $enc)
& $py -X utf8 $lint lint --vault $v *> $null
Ok ($LASTEXITCODE -eq 0) "clean wiki exit 0"
[IO.File]::WriteAllText((Join-Path $lit "broken.md"), "---`ntype: literature`nsources: [03-Literature/_sources/missing.pdf]`nverification: verified`n---`n[[nonexistent]]`n", $enc)
[IO.File]::WriteAllText((Join-Path $lit "nofm.md"), "---`ntype: literature`n# no closing`n", $enc)
$out = (& $py -X utf8 $lint lint --vault $v --json) -join "`n"
Ok ($LASTEXITCODE -eq 1) "defects give exit 1"
$j = $out | ConvertFrom-Json
Ok (@($j.findings | Where-Object { $_.check -eq "link" }).Count -ge 1) "broken wikilink found"
Ok (@($j.findings | Where-Object { $_.check -eq "sources" -and $_.level -eq "error" }).Count -ge 1) "unresolvable source found"
Ok (@($j.findings | Where-Object { $_.check -eq "frontmatter" -and $_.level -eq "error" }).Count -ge 1) "unclosed frontmatter found"
Ok (@($j.findings | Where-Object { $_.check -eq "orphan" }).Count -ge 1) "orphan page found"
Ok (@($j.findings | Where-Object { $_.check -eq "orphan" -and $_.file -match "good|other" }).Count -eq 0) "pages linked from index/notes are not orphans"
Ok (@($j.findings | Where-Object { $_.file -match "nofm" -and $_.check -eq "frontmatter" -and $_.level -eq "warning" }).Count -eq 0) "no follow-on warnings after frontmatter error"
$legacy = Join-Path $v "旧税法笔记.md"
[IO.File]::WriteAllText($legacy, "[[ghost]] no frontmatter", $enc)
$out2 = (& $py -X utf8 $lint lint --vault $v --json) -join "`n"
Ok (-not ($out2 -match "旧税法笔记")) "legacy notes outside scope are not scanned"
$h = & $py -X utf8 $lint hash (Join-Path $lit "_sources\a.pdf") --vault $v
Ok ($LASTEXITCODE -eq 0 -and ($h -join " ") -match "sha256: [0-9a-f]{64}") "hash prints sha256 for new source"
$hex = ((($h -join " ") -replace '.*sha256: ([0-9a-f]{64}).*','$1'))
Add-Content -LiteralPath (Join-Path $v "Meta\source-registry.md") -Value "| SRC-X | a.pdf | | | | $hex | |" -Encoding UTF8
& $py -X utf8 $lint hash (Join-Path $lit "_sources\a.pdf") --vault $v *> $null
Ok ($LASTEXITCODE -eq 10) "registered source detected (exit 10)"

# --- 10. multi-platform (agy / Codex) -----------------------------------------
Write-Host "[10] multi-platform"
$v10 = New-Vault
Ok ((Run-Install $v10 @("-Platform","all","-WithHooks")) -eq 0) "all-platform install exit 0"
Ok ((Run-Check $v10) -eq 0) "checker passes for all platforms"
Ok ((Test-Path (Join-Path $v10 "CLAUDE.md")) -and (Test-Path (Join-Path $v10 ".claude\skills"))) "Claude files present"
$sk = @(Get-ChildItem (Join-Path $v10 ".agents\skills") -Directory)
Ok ($sk.Count -eq 11) ".agents has 11 skills (got $($sk.Count))"
$badName = @($sk | Where-Object { ([IO.File]::ReadAllText((Join-Path $_.FullName "SKILL.md"), $enc)) -notmatch ("(?m)^name:\s*" + [regex]::Escape($_.Name) + "\s*$") })
Ok ($badName.Count -eq 0) "every SKILL.md name equals its folder"
$ag = @(Get-ChildItem (Join-Path $v10 ".agents\agents") -Filter *.md)
Ok ($ag.Count -eq 6 -and @($ag | Where-Object { ([IO.File]::ReadAllText($_.FullName, $enc)) -notmatch "(?m)^subagent: true" }).Count -eq 0) "6 agy subagents with subagent: true"
$am = [IO.File]::ReadAllText((Join-Path $v10 "AGENTS.md"), $enc)
Ok ([IO.File]::ReadAllBytes((Join-Path $v10 "AGENTS.md")).Length -le 24000) "AGENTS.md within 24,000 bytes"
Ok ($am -match "ERC:BEGIN" -and $am -notmatch "(?m)^@\.claude/" -and $am -match "\.agents/scripts/wiki_lint\.py" -and $am -notmatch "Skill 工具") "AGENTS.md self-contained, paths and wording rewritten"
Ok (-not (@(Get-ChildItem (Join-Path $v10 ".agents\skills") -Recurse -Filter *.md | Where-Object { ([IO.File]::ReadAllText($_.FullName, $enc)) -match "\.claude/" }).Count)) "no .claude/ paths left in .agents skills"
$hj = [IO.File]::ReadAllText((Join-Path $v10 ".agents\hooks.json"), $enc) | ConvertFrom-Json
Ok ($null -ne $hj.'economics-research-crew'.PreToolUse -and $null -ne $hj.'economics-research-crew'.PreInvocation) "agy hooks.json has our key with PreToolUse + PreInvocation"
& $py -X utf8 (Join-Path $v10 ".agents\scripts\wiki_lint.py") lint --vault $v10 *> $null
Ok ($LASTEXITCODE -eq 0) "generated wiki_lint runs on a fresh vault (and skips .agents/)"
$before10 = Snapshot $v10
Ok ((Run-Install $v10 @("-Platform","all","-WithHooks")) -eq 0) "all-platform re-install exit 0"
Ok ((($before10 -join "`n") -eq ((Snapshot $v10) -join "`n"))) "no file changed on all-platform re-install"

# existing AGENTS.md / hooks.json are preserved
$v10b = New-Vault
New-Item -ItemType Directory (Join-Path $v10b ".agents") | Out-Null
[IO.File]::WriteAllText((Join-Path $v10b "AGENTS.md"), "# 我的规则`n保留这一行`n", $enc)
[IO.File]::WriteAllText((Join-Path $v10b ".agents\hooks.json"), '{"mine":{"Stop":[{"command":"echo hi"}]}}', $enc)
Ok ((Run-Install $v10b @("-Platform","agy","-WithHooks")) -eq 0) "agy install over existing files exit 0"
$am2 = [IO.File]::ReadAllText((Join-Path $v10b "AGENTS.md"), $enc)
Ok ($am2.StartsWith("# 我的规则`n保留这一行") -and $am2 -match "ERC:BEGIN") "existing AGENTS.md kept, block appended"
$hj2 = [IO.File]::ReadAllText((Join-Path $v10b ".agents\hooks.json"), $enc) | ConvertFrom-Json
Ok ($null -ne $hj2.mine -and $null -ne $hj2.'economics-research-crew') "existing hooks.json key kept, ours added"
Ok (-not (Test-Path (Join-Path $v10b "CLAUDE.md")) -and -not (Test-Path (Join-Path $v10b ".claude"))) "agy-only install leaves no Claude files"
Ok (@(Get-ChildItem (Join-Path $v10b "_erc-backups") -Recurse -File -Filter AGENTS.md).Count -eq 1) "existing AGENTS.md backed up"
# -Update with a stale block -> AGENTS.md.new, original untouched
[IO.File]::WriteAllText((Join-Path $v10b "AGENTS.md"), $am2.Replace("## 路由规则", "## 路由规则（旧）"), $enc)
$shaOld = Get-Sha (Join-Path $v10b "AGENTS.md")
Ok ((Run-Install $v10b @("-Platform","agy","-Update")) -eq 0) "agy -Update exit 0"
Ok ((Get-Sha (Join-Path $v10b "AGENTS.md")) -eq $shaOld -and (Test-Path (Join-Path $v10b "AGENTS.md.new"))) "stale block -> AGENTS.md.new, original untouched"
Ok (([IO.File]::ReadAllText((Join-Path $v10b "AGENTS.md.new"), $enc)).StartsWith("# 我的规则")) "AGENTS.md.new keeps user content"

# Codex-only: shared files, no agy hooks
$v10c = New-Vault
Ok ((Run-Install $v10c @("-Platform","codex","-WithHooks")) -eq 0) "codex install exit 0"
Ok ((Run-Check $v10c) -eq 0) "checker passes for codex"
Ok ((Test-Path (Join-Path $v10c "AGENTS.md")) -and -not (Test-Path (Join-Path $v10c ".agents\hooks.json")) -and -not (Test-Path (Join-Path $v10c ".agents\hooks"))) "codex: AGENTS.md, no agy hooks"

# agy hook input shapes
function AgyHook([string]$Script, [string]$Json) {
    $ErrorActionPreference = "Continue"
    $out = $Json | & $py -X utf8 (Join-Path $payload ".claude\hooks\$Script") 2>$null
    return (($out -join " ") + "|rc=$LASTEXITCODE")
}
$rawf = Join-Path $v10 "06-Data\raw\p.csv"; [IO.File]::WriteAllText($rawf, "a", $enc)
$jp = { param($tool,$args2) (@{toolCall=@{name=$tool; args=$args2}; cwd=$v10} | ConvertTo-Json -Depth 5 -Compress) }
Ok ((AgyHook "protect_raw.py" (& $jp "edit_file" @{Path=$rawf; Target="a"; Replacement="b"})) -match '"decision": "deny".*\|rc=0') "agy edit_file on raw -> deny JSON"
Ok ((AgyHook "protect_raw.py" (& $jp "write_file" @{Path=$rawf; Content="x"})) -match '"decision": "deny"') "agy write_file overwriting raw -> deny"
Ok ((AgyHook "protect_raw.py" (& $jp "write_file" @{Path=(Join-Path $v10 "06-Data\raw\new.csv"); Content="x"})) -match '^\{"decision":"ask"\}\|rc=0') "agy write_file creating new raw file -> ask (normal flow)"
Ok ((AgyHook "protect_raw.py" (& $jp "run_command" @{CommandLine="del 06-Data\raw\p.csv"})) -match '"decision": "deny"') "agy run_command deleting raw -> deny"
Ok ((AgyHook "protect_raw.py" (& $jp "read_file" @{Path=$rawf})) -match '^\{"decision":"ask"\}') "agy read_file -> ask (never allow)"
Ok ((AgyHook "protect_raw.py" '{"toolCall":broken') -match '^\{"decision":"ask"\}\|rc=0') "agy malformed input -> neutral JSON"
$pi0 = @{hookEventName="PreInvocation"; invocationNum=0; lastUserInput="帮我梳理税收遵从的国内外文献"} | ConvertTo-Json -Compress
$pi1 = @{hookEventName="PreInvocation"; invocationNum=1; lastUserInput="帮我梳理税收遵从的国内外文献"} | ConvertTo-Json -Compress
$pi2 = @{hookEventName="PreInvocation"; invocationNum=0; lastUserInput="固定效应是什么"} | ConvertTo-Json -Compress
Ok ((AgyHook "routing_hint.py" $pi0) -match 'injectSteps.*literature-review') "agy PreInvocation first call -> injected hint"
Ok ((AgyHook "routing_hint.py" $pi1) -match '^\{\}\|rc=0') "agy later invocation in same turn -> {}"
Ok ((AgyHook "routing_hint.py" $pi2) -match '^\{\}\|rc=0') "agy conceptual question -> {}"

# --- cleanup + summary ----------------------------------------------------------
foreach ($d in $v,$v3,$v4,$v5,$v6,$v6b,$v6c,$v10,$v10b,$v10c) { if ($d -and (Test-Path $d) -and $d.StartsWith([IO.Path]::GetTempPath())) { Remove-Item -LiteralPath $d -Recurse -Force -ErrorAction SilentlyContinue } }
Write-Host ""
Write-Host "passed: $script:pass  failed: $script:fail" -ForegroundColor $(if ($script:fail) { "Red" } else { "Green" })
if ($script:fail) { exit 1 }
