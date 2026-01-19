import qrcode

url = "192.168.1.183:8501"
img = qrcode.make(url)
img.save("qr_fiche_incident.png")
