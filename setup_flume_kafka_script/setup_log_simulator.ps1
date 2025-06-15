param(
    [string]$BaseDir = "D:\\SOFTWARE\\apache-flume-1.11.0-bin\\data\\log_stream",
    [datetime]$StartDate = (Get-Date "2019-06-13"),
    [int]$Days = 22,
    [string]$FlumeConfDir = "D:\\SOFTWARE\\apache-flume-1.11.0-bin\\conf\\agents"
)

for ($i = 0; $i -lt $Days; $i++) {
    $date = $StartDate.AddDays($i).ToString('yyyy-MM-dd')
    $folder = Join-Path $BaseDir $date
    $folder = $folder.Replace('\\', '\')
    $folder = $folder.Replace('\', '\\')
    New-Item -ItemType Directory -Path $folder -Force | Out-Null

    $agentName = "agent_$($date.Replace('-',''))"
    $confFile = Join-Path $FlumeConfDir "flume-$date.conf"
    $topic = "impression_$($date.Replace('-',''))"

    $content = @"
# Flume config for date $date
$agentName.sources = spoolSrc
$agentName.sinks = kafkaSink
$agentName.channels = memChannel

# Source
$agentName.sources.spoolSrc.type = spooldir
$agentName.sources.spoolSrc.spoolDir = $folder
$agentName.sources.spoolSrc.fileHeader = true

# Channel
$agentName.channels.memChannel.type = memory
$agentName.channels.memChannel.capacity = 10000
$agentName.channels.memChannel.transactionCapacity = 1000

# Sink
$agentName.sinks.kafkaSink.type = org.apache.flume.sink.kafka.KafkaSink
$agentName.sinks.kafkaSink.topic = $topic
$agentName.sinks.kafkaSink.brokerList = localhost:9092

# Bindings
$agentName.sources.spoolSrc.channels = memChannel
$agentName.sinks.kafkaSink.channel = memChannel
"@  

    $content | Out-File -FilePath $confFile -Encoding utf8
}

Pause