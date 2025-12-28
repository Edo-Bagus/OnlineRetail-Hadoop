# Perintah Lengkap MapReduce dengan Hadoop di Docker

## Langkah-langkah dari Awal (Fresh Start)

### 1. Build Docker Image dengan Python
```powershell
docker-compose build
```

### 2. Start Hadoop Cluster (Namenode + Datanode)
```powershell
docker-compose up -d
```

### 3. Tunggu Cluster Siap (30 detik)
```powershell
Start-Sleep -Seconds 30
docker ps
```

### 4. Verifikasi Datanode Terhubung
```powershell
docker exec namenode hdfs dfsadmin -report
```

### 5. Copy File CSV ke Namenode Container
```powershell
docker cp Online-Retail.csv namenode:/tmp/
```

### 6. Copy Mapper Script ke Container
```powershell
docker cp mapper.py namenode:/tmp/
```

### 7. Copy Reducer Script ke Container
```powershell
docker cp reducer.py namenode:/tmp/
```

### 8. Fix Line Ending (Windows ke Unix)
```powershell
docker exec namenode bash -c "sed -i 's/\r$//' /tmp/mapper.py /tmp/reducer.py"
```

### 9. Update Shebang ke Python3
```powershell
docker exec namenode bash -c "sed -i 's|#!/usr/bin/env python|#!/usr/bin/python3|' /tmp/mapper.py /tmp/reducer.py"
```

### 10. Buat Scripts Executable
```powershell
docker exec namenode bash -c "chmod +x /tmp/mapper.py /tmp/reducer.py"
```

### 11. Buat Direktori Input di HDFS
```powershell
docker exec namenode hdfs dfs -mkdir -p /input
```

### 12. Upload File CSV ke HDFS
```powershell
docker exec namenode hdfs dfs -put /tmp/Online-Retail.csv /input/
```

### 13. Verifikasi File di HDFS
```powershell
docker exec namenode hdfs dfs -ls /input/
```

### 14. Jalankan MapReduce Job
```powershell
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/mapper.py,/tmp/reducer.py -mapper /tmp/mapper.py -reducer /tmp/reducer.py -input /input/Online-Retail.csv -output /output/final_result"
```

### 15. Lihat Output Files
```powershell
docker exec namenode hdfs dfs -ls /output/final_result
```

### 16. Preview Hasil (10 baris pertama)
```powershell
docker exec namenode hdfs dfs -cat /output/final_result/part-00000 | Select-Object -First 10
```

### 17. Download Hasil dari HDFS ke Container
```powershell
docker exec namenode hdfs dfs -get /output/final_result/part-00000 /tmp/result.txt
```

### 18. Copy Hasil ke Host Windows
```powershell
docker cp namenode:/tmp/result.txt ./final_result.txt
```

---

## Command Cleanup (Untuk Mengulang dari Awal)

### Stop dan Hapus Semua Container + Volumes
```powershell
docker-compose down -v
```

### Verifikasi Tidak Ada Container
```powershell
docker ps -a
```

---

## Ringkasan Hasil

- **Input**: 541,910 records dari Online-Retail.csv
- **Map Output**: 537,113 records (stock_code + quantity)
- **Reduce Output**: 4,034 unique products dengan total quantity
- **Output File**: `/output/final_result/part-00000` di HDFS
- **Local File**: `final_result.txt` di direktori kerja

---

## Troubleshooting

### Jika Datanode Tidak Terhubung
Cek environment variable di docker-compose.yml:
```yaml
environment:
  - CORE_CONF_fs_defaultFS=hdfs://namenode:8020
```

### Jika Error "python\r: No such file"
Jalankan command fix line ending:
```powershell
docker exec namenode bash -c "sed -i 's/\r$//' /tmp/mapper.py /tmp/reducer.py"
```

### Jika Error f-string SyntaxError
Python 3.5 tidak support f-strings. Gunakan `.format()` atau `%`:
```python
# Ganti
print(f"{stock_code}\t{quantity}")
# Dengan
print("{}\t{}".format(stock_code, quantity))
```

---

## Akses Web UI

- **Namenode**: http://localhost:9870
- **Resource Manager**: http://localhost:8088

---

## Files yang Dibutuhkan

1. `Dockerfile` - Custom Hadoop image dengan Python 3
2. `docker-compose.yml` - Orchestration namenode + datanode
3. `mapper.py` - Map phase script
4. `reducer.py` - Reduce phase script
5. `Online-Retail.csv` - Input data

---

**Total Waktu Eksekusi**: ~10-15 detik untuk MapReduce job
