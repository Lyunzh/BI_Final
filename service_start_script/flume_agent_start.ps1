param(
  [string]$FlumeHome    = "D:\\SOFTWARE\\apache-flume-1.11.0-bin",
  [string]$FlumeConfDir = "D:\\SOFTWARE\\apache-flume-1.11.0-bin\\conf",
  [string]$LogDir       = "D:\\SOFTWARE\\apache-flume-1.11.0-bin\\logs\\agents"
)

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }

Get-ChildItem -Path "$FlumeConfDir\\agents" -Filter "flume-*.conf" | ForEach-Object {
    $datePart  = $_.BaseName.Substring(6)
    $agentName = "agent_$($datePart.Replace('-',''))"

    $confFile = $_.FullName
    $args = @(
      "agent",
      "--conf",       $FlumeConfDir,
      "--conf-file",  $confFile,
      "--name",       $agentName
    )

    $outLog = Join-Path $LogDir "$agentName-out.log"
    $errLog = Join-Path $LogDir "$agentName-err.log"

    Start-Process -FilePath (Join-Path $FlumeHome "bin\\flume-ng.cmd") `
                  -ArgumentList $args `
                  -NoNewWindow `
                  -RedirectStandardOutput $outLog `
                  -RedirectStandardError  $errLog

    Write-Host "Started Flume agent '$agentName' with config '$confFile'"
}

Pause