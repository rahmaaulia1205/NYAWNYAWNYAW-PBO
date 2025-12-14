# NYAWNYAWNYAW – Cat Run

Proyek Ujian Akhir Semester  
Mata Kuliah : Pemrograman Berorientasi Objek  
Program Studi : D4 Manajemen Informatika  
Universitas Negeri Surabaya  

---

## Deskripsi Aplikasi
NYAWNYAWNYAW – Cat Run merupakan game arcade sederhana berbasis Python
yang dikembangkan menggunakan library **Pygame**.  
Pada game ini, pemain mengendalikan karakter kucing untuk menghindari musuh
berupa anjing, mengumpulkan power-up, dan bertahan selama mungkin untuk
mendapatkan skor tertinggi.

Aplikasi ini dibuat sebagai implementasi konsep **Object-Oriented Programming (OOP)**.

---

## Fitur Utama
- Kontrol pergerakan karakter menggunakan keyboard
- Musuh bergerak dengan kecepatan acak
- Sistem nyawa (health)
- Power-up untuk menambah nyawa
- Sistem skor berbasis waktu
- Penyimpanan highscore menggunakan file JSON
- Menu utama, pause, dan game over

---

## Konsep OOP yang Digunakan
- **Encapsulation**  
  Penggunaan atribut private pada class Player untuk mengelola nyawa pemain.

- **Inheritance**  
  Class `Player`, `Dog`, dan `PowerUp` mewarisi class `Entity`.

- **Polymorphism**  
  Method `update()` dan `draw()` memiliki implementasi berbeda pada setiap class turunan.

---

## Teknologi yang Digunakan
- Python 3
- Pygame
- JSON (penyimpanan highscore)

---

## Cara Menjalankan Aplikasi
1. Pastikan Python sudah terinstal
2. Install pygame dengan perintah: pip install pygame 
3. Jalankan game dengan perintah: python main.py


