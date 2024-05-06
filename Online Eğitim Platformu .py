import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QMessageBox, QGroupBox, QDialog

# Kurs sınıfı: Bir eğitim kursunu temsil eder
class Kurs:
    def __init__(self, kurs_adi, egitmen, icerik):
        # Kurs özelliklerini başlatır
        self.kurs_adi = kurs_adi
        self.egitmen = egitmen
        self.icerik = icerik
        self.kayitli_ogrenciler = []  # Kursa kayıtlı öğrencilerin listesi

    # Öğrenciyi kursa kaydeder
    def ogrenci_kaydet(self, ogrenci):
        self.kayitli_ogrenciler.append(ogrenci)
        print(f"{ogrenci.isim}, {self.kurs_adi} kursuna kaydedildi.")  # Konsola kayıt mesajı yazdırır

# Eğitmen sınıfı: Bir eğitmeni temsil eder
class Egitmen:
    def __init__(self, isim, uzmanlik_alani):
        # Eğitmen özelliklerini başlatır
        self.isim = isim
        self.uzmanlik_alani = uzmanlik_alani

# Öğrenci sınıfı: Bir öğrenciyi temsil eder
class Ogrenci:
    def __init__(self, isim, email):
        # Öğrenci özelliklerini başlatır
        self.isim = isim
        self.email = email

# OnlineEgitimPlatformu sınıfı: Bir online eğitim platformunu temsil eder
class OnlineEgitimPlatformu:
    def __init__(self):
        # Veritabanına bağlan
        self.conn = sqlite3.connect('online_egitim.db')
        self.cursor = self.conn.cursor()

        # Kurs, Eğitmen ve Öğrenci tablolarını oluştur
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Kurs (
                                id INTEGER PRIMARY KEY,
                                kurs_adi TEXT NOT NULL,
                                egitmen TEXT NOT NULL,
                                icerik TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Egitmen (
                                id INTEGER PRIMARY KEY,
                                isim TEXT NOT NULL,
                                uzmanlik_alani TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Ogrenci (
                                id INTEGER PRIMARY KEY,
                                isim TEXT NOT NULL,
                                email TEXT NOT NULL)''')
        self.conn.commit()

    # Bir kurs ekler
    def kurs_ekle(self, kurs_adi, egitmen_adi, uzmanlik_alani, icerik):
        self.cursor.execute("INSERT INTO Egitmen (isim, uzmanlik_alani) VALUES (?, ?)", (egitmen_adi, uzmanlik_alani))
        egitmen_id = self.cursor.lastrowid

        self.cursor.execute("INSERT INTO Kurs (kurs_adi, egitmen, icerik) VALUES (?, ?, ?)", (kurs_adi, egitmen_id, icerik))
        self.conn.commit()

    # Bir öğrenci ekler
    def ogrenci_ekle(self, isim, email):
        self.cursor.execute("INSERT INTO Ogrenci (isim, email) VALUES (?, ?)", (isim, email))
        self.conn.commit()

    # Mevcut kursları listeler
    def kurs_listele(self):
        self.cursor.execute("SELECT kurs_adi, isim FROM Kurs JOIN Egitmen ON Kurs.egitmen = Egitmen.id")
        kurslar = self.cursor.fetchall()
        kurs_listesi = "Mevcut Kurslar:\n"
        for kurs in kurslar:
            kurs_listesi += f"Kurs Adı: {kurs[0]}, Eğitmen: {kurs[1]}\n"
        return kurs_listesi

# OgrenciKayitDialog sınıfı: Öğrenci kayıt penceresini temsil eder
class OgrenciKayitDialog(QDialog):
    def __init__(self, platform):
        super().__init__()
        self.platform = platform
        self.setWindowTitle("Öğrenci Kayıt")  # Pencere başlığını ayarlar
        self.initUI()

    # Pencere arayüzünü oluşturur
    def initUI(self):
        layout = QVBoxLayout()  # Dikey bir düzen oluşturur

        self.isim_entry = QLineEdit()  # İsim giriş kutusunu oluşturur
        layout.addWidget(QLabel("İsim:"))  # "İsim:" etiketini ekler
        layout.addWidget(self.isim_entry)  # İsim giriş kutusunu ekler

        self.email_entry = QLineEdit()  # E-posta giriş kutusunu oluşturur
        layout.addWidget(QLabel("E-posta:"))  # "E-posta:" etiketini ekler
        layout.addWidget(self.email_entry)  # E-posta giriş kutusunu ekler

        kaydet_button = QPushButton("Kaydet")  # "Kaydet" düğmesini oluşturur
        kaydet_button.clicked.connect(self.kaydet)  # "Kaydet" düğmesinin tıklama olayını bağlar
        layout.addWidget(kaydet_button)  # "Kaydet" düğmesini ekler

        self.setLayout(layout)  # Pencere düzenini ayarlar

    # Öğrenciyi kaydeder
    def kaydet(self):
        isim = self.isim_entry.text()  # İsim giriş kutusundan veriyi alır
        email = self.email_entry.text()  # E-posta giriş kutusundan veriyi alır
        self.platform.ogrenci_ekle(isim, email)  # Platforma öğrenciyi ekler
        QMessageBox.information(self, "Başarılı", "Öğrenci kaydı başarıyla oluşturuldu.")  # Bilgi mesajı ile başarıyı bildirir
        self.close()  # Pencereyi kapatır

# Arayuz sınıfı: Online eğitim platformunun ana penceresini temsil eder
class Arayuz(QWidget):
    def __init__(self, platform):
        super().__init__()
        self.platform = platform
        self.setWindowTitle("ONLINE EĞİTİM PLATFORMU")  # Pencere başlığını ayarlar
        self.initUI()

    # Pencere arayüzünü oluşturur
    def initUI(self):
        self.result_label = QLabel()  # Sonuç etiketini oluşturur
        self.result_label.setStyleSheet("color: green; font-weight: bold;")  # Etiketin stilini ayarlar

        kurs_ekle_groupbox = self.create_kurs_ekle_groupbox()  # Kurs ekleme grubunu oluşturur
        kurs_listele_button = QPushButton("Mevcut Kursları Listele")  # "Mevcut Kursları Listele" düğmesini oluşturur
        kurs_listele_button.clicked.connect(self.kurslari_listele)  # "Mevcut Kursları Listele" düğmesinin tıklama olayını bağlar
        ogrenci_kayit_button = QPushButton("Öğrenci Kayıt")  # "Öğrenci Kayıt" düğmesini oluşturur
        ogrenci_kayit_button.clicked.connect(self.kayit_olustur)  # "Öğrenci Kayıt" düğmesinin tıklama olayını bağlar

        layout = QVBoxLayout()  # Dikey bir düzen oluşturur
        layout.addWidget(kurs_ekle_groupbox)  # Kurs ekleme grubunu ekler
        layout.addWidget(kurs_listele_button)  # "Mevcut Kursları Listele" düğmesini ekler
        layout.addWidget(ogrenci_kayit_button)  # "Öğrenci Kayıt" düğmesini ekler
        layout.addWidget(self.result_label)  # Sonuç etiketini ekler

        self.setLayout(layout)  # Pencere düzenini ayarlar

    # Kurs ekleme grubunu oluşturur
    def create_kurs_ekle_groupbox(self):
        groupbox = QGroupBox("Yeni Kurs Ekle")  # Grup kutusu başlığını ayarlar

        self.kurs_adi_entry = QLineEdit()  # Kurs adı giriş kutusunu oluşturur
        self.egitmen_entry = QLineEdit()  # Eğitmen giriş kutusunu oluşturur
        self.uzmanlik_entry = QLineEdit()  # Uzmanlık alanı giriş kutusunu oluşturur
        self.icerik_entry = QTextEdit()  # Kurs içeriği metin kutusunu oluşturur

        layout = QVBoxLayout()  # Dikey bir düzen oluşturur
        layout.addWidget(QLabel("Kurs Adı:"))  # "Kurs Adı:" etiketini ekler
        layout.addWidget(self.kurs_adi_entry)  # Kurs adı giriş kutusunu ekler
        layout.addWidget(QLabel("Eğitmen:"))  # "Eğitmen:" etiketini ekler
        layout.addWidget(self.egitmen_entry)  # Eğitmen giriş kutusunu ekler
        layout.addWidget(QLabel("Uzmanlık Alanı:"))  # "Uzmanlık Alanı:" etiketini ekler
        layout.addWidget(self.uzmanlik_entry)  # Uzmanlık alanı giriş kutusunu ekler
        layout.addWidget(QLabel("Kurs İçeriği:"))  # "Kurs İçeriği:" etiketini ekler
        layout.addWidget(self.icerik_entry)  # Kurs içeriği metin kutusunu ekler

        kurs_ekle_button = QPushButton("Kurs Ekle")  # "Kurs Ekle" düğmesini oluşturur
        kurs_ekle_button.clicked.connect(self.kurs_ekle)  # "Kurs Ekle" düğmesinin tıklama olayını bağlar
        layout.addWidget(kurs_ekle_button)  # "Kurs Ekle" düğmesini ekler

        groupbox.setLayout(layout)  # Grup kutusu düzenini ayarlar
        return groupbox  # Grup kutusunu döndürür

    # Bir kurs ekler
    def kurs_ekle(self):
        kurs_adi = self.kurs_adi_entry.text()  # Kurs adı giriş kutusundan veriyi alır
        egitmen_adi = self.egitmen_entry.text()  # Eğitmen adı giriş kutusundan veriyi alır
        uzmanlik_alani = self.uzmanlik_entry.text()  # Uzmanlık alanı giriş kutusundan veriyi alır
        icerik = self.icerik_entry.toPlainText()  # Kurs içeriği metin kutusundan veriyi alır
        self.platform.kurs_ekle(kurs_adi, egitmen_adi, uzmanlik_alani, icerik)  # Platforma kursu ekler
        self.result_label.setText(f"{kurs_adi} kursu başarıyla eklendi.")  # Sonuç etiketine ekleme mesajını yazar

    # Mevcut kursları listeler
    def kurslari_listele(self):
        kurs_listesi = self.platform.kurs_listele()  # Mevcut kursları alır
        QMessageBox.information(self, "Mevcut Kurslar", kurs_listesi)  # Bilgi mesajı ile mevcut kursları gösterir

    # "Öğrenci Kayıt" butonuna tıklanıldığında öğrenci kayıt penceresini açar
    def kayit_olustur(self):
        dialog = OgrenciKayitDialog(self.platform)  # Öğrenci kayıt dialogunu oluşturur
        dialog.exec_()  # Pencereyi görüntüler

if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt uygulamasını başlatır

    platform = OnlineEgitimPlatformu()  # OnlineEgitimPlatformu nesnesini oluşturur
    arayuz = Arayuz(platform)  # Arayuz nesnesini oluşturur
    arayuz.show()  # Pencereyi gösterir

    sys.exit(app.exec_())  # Uygulamayı çalıştırır
