# Full Restart Script
# Restart cluster dan jalankan semua analisis dari awal

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  FULL RESTART - HADOOP CLUSTER" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

# Step 1: Stop existing containers
Write-Host "Step 1: Stopping existing containers..." -ForegroundColor Yellow
docker-compose down 2>$null
Start-Sleep -Seconds 3
Write-Host "   Containers stopped`n" -ForegroundColor Green

# Step 2: Start cluster
Write-Host "Step 2: Starting Hadoop cluster..." -ForegroundColor Yellow
docker-compose up -d
Write-Host "   Waiting for cluster to initialize (30 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 30
Write-Host "   Cluster started`n" -ForegroundColor Green

# Step 3: Verify cluster
Write-Host "Step 3: Verifying cluster..." -ForegroundColor Yellow
$report = docker exec namenode hdfs dfsadmin -report 2>&1 | Select-String "Live datanodes"
if ($report) {
    Write-Host "   Cluster is healthy`n" -ForegroundColor Green
} else {
    Write-Host "   Cluster may need more time..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
}

# Step 4: Leave safe mode
Write-Host "Step 4: Leaving safe mode..." -ForegroundColor Yellow
docker exec namenode bash -c "hdfs dfsadmin -safemode leave" | Out-Null
Write-Host "   Safe mode off`n" -ForegroundColor Green

# Step 5: Upload data and scripts
Write-Host "Step 5: Uploading data and scripts..." -ForegroundColor Yellow

# Check if data exists in HDFS
$dataExists = docker exec namenode hdfs dfs -ls /input/Online-Retail.csv 2>$null
if (-not $dataExists) {
    Write-Host "   Uploading CSV data..." -ForegroundColor Gray
    docker cp Online-Retail.csv namenode:/tmp/ | Out-Null
    docker exec namenode hdfs dfs -mkdir -p /input | Out-Null
    docker exec namenode hdfs dfs -put /tmp/Online-Retail.csv /input/ | Out-Null
    Write-Host "   Data uploaded to HDFS" -ForegroundColor Green
} else {
    Write-Host "   Data already exists in HDFS" -ForegroundColor Cyan
}

Write-Host "   Copying MapReduce scripts..." -ForegroundColor Gray
docker cp mapreduce_scripts/product_sales_mapper.py namenode:/tmp/ | Out-Null
docker cp mapreduce_scripts/product_sales_reducer.py namenode:/tmp/ | Out-Null
docker cp mapreduce_scripts/customer_pattern_mapper.py namenode:/tmp/ | Out-Null
docker cp mapreduce_scripts/customer_pattern_reducer.py namenode:/tmp/ | Out-Null
docker cp mapreduce_scripts/time_distribution_mapper.py namenode:/tmp/ | Out-Null
docker cp mapreduce_scripts/time_distribution_reducer.py namenode:/tmp/ | Out-Null

docker exec namenode bash -c "sed -i 's/\r$//' /tmp/*.py && chmod +x /tmp/*.py" | Out-Null
Write-Host "   Scripts uploaded and configured`n" -ForegroundColor Green

# Step 6: Run all analyses
Write-Host "Step 6: Running all MapReduce analyses...`n" -ForegroundColor Yellow

Write-Host "   [1/3] Product Sales Analysis..." -ForegroundColor Cyan
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/product_sales_mapper.py,/tmp/product_sales_reducer.py -mapper 'python3 /tmp/product_sales_mapper.py' -reducer 'python3 /tmp/product_sales_reducer.py' -input /input/Online-Retail.csv -output /output/product_sales" 2>&1 | Out-Null
Write-Host "         Completed" -ForegroundColor Green

Write-Host "   [2/3] Customer Patterns Analysis..." -ForegroundColor Cyan
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/customer_pattern_mapper.py,/tmp/customer_pattern_reducer.py -mapper 'python3 /tmp/customer_pattern_mapper.py' -reducer 'python3 /tmp/customer_pattern_reducer.py' -input /input/Online-Retail.csv -output /output/customer_patterns" 2>&1 | Out-Null
Write-Host "         Completed" -ForegroundColor Green

Write-Host "   [3/3] Time Distribution Analysis..." -ForegroundColor Cyan
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/time_distribution_mapper.py,/tmp/time_distribution_reducer.py -mapper 'python3 /tmp/time_distribution_mapper.py' -reducer 'python3 /tmp/time_distribution_reducer.py' -input /input/Online-Retail.csv -output /output/time_distribution" 2>&1 | Out-Null
Write-Host "         Completed`n" -ForegroundColor Green

# Step 7: Download and convert results
Write-Host "Step 7: Downloading and converting results..." -ForegroundColor Yellow
docker exec namenode hdfs dfs -get /output/product_sales/part-00000 /tmp/product_sales.txt 2>$null
docker exec namenode hdfs dfs -get /output/customer_patterns/part-00000 /tmp/customer_patterns.txt 2>$null
docker exec namenode hdfs dfs -get /output/time_distribution/part-00000 /tmp/time_distribution.txt 2>$null

docker cp namenode:/tmp/product_sales.txt results/product_sales_result.txt 2>$null
docker cp namenode:/tmp/customer_patterns.txt results/customer_patterns_result.txt 2>$null
docker cp namenode:/tmp/time_distribution.txt results/time_distribution_result.txt 2>$null

Push-Location results
python ../mapreduce_scripts/convert_to_csv.py | Out-Null
Pop-Location
Write-Host "   Results ready`n" -ForegroundColor Green

# Final summary
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  FULL RESTART COMPLETED!" -ForegroundColor Green
Write-Host "=========================================`n" -ForegroundColor Green

Write-Host "Cluster Status:" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host "`nResults available at:" -ForegroundColor Cyan
Write-Host "   - results/product_sales_result.csv" -ForegroundColor White
Write-Host "   - results/customer_patterns_result.csv" -ForegroundColor White
Write-Host "   - results/time_distribution_result.csv`n" -ForegroundColor White

Write-Host "Web UI:" -ForegroundColor Cyan
Write-Host "   - Namenode: http://localhost:9870" -ForegroundColor White
Write-Host "   - Resource Manager: http://localhost:8088`n" -ForegroundColor White
