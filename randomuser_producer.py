from kafka import KafkaProducer
import requests, json, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    try:
        res = requests.get("https://randomuser.me/api/")
        res.raise_for_status()
        user = res.json()["results"][0]
        producer.send("user-topic", value=user)
        print("Gönderildi:", user["email"])
    except Exception as e:
        print("Producer hata:", e)
    time.sleep(3)
