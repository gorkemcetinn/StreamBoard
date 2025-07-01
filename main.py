import subprocess, time, webbrowser

if __name__ == "__main__":
    print("🚀 Flask API başlatılıyor...")
    flask = subprocess.Popen(["python", "app.py"])
    time.sleep(2)

    print("🚀 Kafka producer başlatılıyor...")
    prod = subprocess.Popen(["python", "randomuser_producer.py"])
    time.sleep(1)

    print("🚀 Spark streaming başlatılıyor...")
    spk = subprocess.Popen(["python", "spark_randomuser_stream.py"])
    time.sleep(3)

    print("🌐 Tarayıcı açılıyor…")
    webbrowser.open("http://127.0.0.1:5000/")
    
    # Ctrl-C ile durdurulana kadar bekler
    try:
        flask.wait()
        prod.wait()
        spk.wait()
    except KeyboardInterrupt:
        pass
