param(
  [string]$KafkaBin    = 'D:\\SOFTWARE\\kafka_2.12-3.5.1\\bin\\windows',
  [string]$TopicPrefix = 'impression_',
  [datetime]$StartDate = (Get-Date '2019-06-13'),
  [int]$Days          = 22,
  [int]$Partitions    = 10,
  [int]$Replication   = 1
)

for ($i = 0; $i -lt $Days; $i++) {
    $date  = $StartDate.AddDays($i).ToString('yyyy-MM-dd')
    $topic = "$TopicPrefix$($date.Replace('-',''))"
    Write-Host "Creating topic '$topic'..."
    & "${KafkaBin}\kafka-topics.bat" `
        --create `
        --bootstrap-server localhost:9092 `
        --replication-factor $Replication `
        --partitions $Partitions `
        --topic $topic
}