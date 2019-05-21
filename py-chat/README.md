# py-chat
Final Project Progjar

Nama Kelompok 
1. Bagus Dharma Iswara - 05111540000028
2. Modista Garsia - 05111640000031
3. Alfian - 05111640000073
4. Natasha Valentina Santoso - 05111640000183

### Basic Operation
Pertama-tama, server membuka layanan chat dengan cara mendengar (listening) pada port TCP 8000. Ketika klien ingin menggunakan layanan, klien akan melakukan koneksi TCP dengan server pada port tersebut. Begitu klien terkoneksi dengan server, server akan mengirim string sambutan. Klien dan server akan terus bertukar pesan (request dan response) hingga koneksi putus atau diakhiri.

Klien harus terotorisasi sebagai pengguna sebelum bisa melanjutkan proses lainnya. Apabila klien belum terdaftar sebagai pengguna, maka server akan meminta klien untuk mendaftarkan diri sebagai pengguna.

Setiap perintahnya terdiri dari sebuah kata kunci yang diikuti dengan satu atau lebih argumen lalu klien menekan Enter untuk mengirimkan request ke serber. Kata kunci dan argumen dipisahkan oleh sebuah spasi. Masing-masing argumen tidak boleh melebihi 100 karakter.

Server akan mengirimkan respon berupa status request dan messagenya. status request terbagi menjadi 2, yaitu "failed"  diikuti dengan isi message berupa penyebab request dari klien gagal di proses dan "success"

Server harus merespon semua request klien yang tidak valid dengan status "failed". Server juga harus merespon request pada sesi yang tidak valid secara sesi, sintaks, argumen, dan sebagainya.

## Sisi Activity Client
1. Menu autorisasi
- login [username] [password]
- register [username] [password] [retyped-password]
- logout

2. Menu Utama
- contact -> menuju menu kontak
- group -> menuju menu grup
- list -> menuju inbox
- back -> kembali ke menu utama

3. Menu Kontak
- get -> menampilkan daftar kontak teman
- add [username] -> menambahkan teman ke kontak
- del [username] -> menghapus teman dari kontak
- chat [username] -> membuka personal chat dengan teman
- back -> kembali ke menu utama

4. Menu Grup
- create [group-name] [group-code (optional)]-> membuat grup baru
- get -> mendapatkan daftar grup yang telah tergabung
- chat [nomor-group dalam daftar] -> masuk ke group chat
- back -> kembali ke menu utama

### Sesi Autorisasi
Kata kunci "AUTH-xxx". Pada sesi otorisasi dibagi menjadi 3 yaitu
1. AUTH-REGISTER : Untuk mendaftarkan klien sebagai pengguna
2. AUTH-LOGIN : otorisasi klien sebagai pengguna
3. AUTH-LOGOUT : menghapus sesi

Argumen-argumen yang dibutuhkan untuk masing-masing kata kunci antara lain,
1. AUTH-REGISTER [nama_pengguna] [password_pengguna] [ulangi_password] (contoh : AUTH-REGISTER modis passmodis passmodis)
2. AUTH-LOGIN [nama_pengguna] [password_pengguna] (contoh : AUTH-LOGIN modis passmodis)
3. AUTH-LOGOUT

### Sesi Transaksi
Pengguna dapat bertukar pesan (chat) terhadap sesama klien yang sama-sama sudah terotorisasi di waktu yang sama. Selain itu pengguna juga dapat bergabung kedalam group untuk bertukar pesan ke banyak pengguna lain yang tergabung pada group yang sama. Selain itu, pengguna juga dapat mengirimkan file berupa gambar pada saat bertukar pesan.

Kata kunci yang digunakan antara lain,
1. GROUP-CREATE : Digunakan untuk membuat grup obrolan baru
2. GROUP-DELETE : Digunakan untuk menghapus grup obrolan. Pengguna yang menggunakan fitur ini harus terotorisasi sebagai admin dalam grup yang ingin dihapus
3. GROUP-JOIN : Digunakan untuk bergabung pada grup obrolan
4. GROUP-LIST : Digunakan untuk melihat daftar grup yang ada. Grup yang masuk dalam list adalah Open grup. Respon server berupa nama grup dan kode yang dapat digunakan untuk bergabung kedalam grup.
5. GROUP-EXIT : Digunakan untuk keluar dari grup obrolan.
6. GROUP-INVITE : Digunakan untuk mengundang pengguna lain untuk masuk kedalam grup. Pengguna yang menggunakan fitur ini harus terotorisasi sebagai admin grup untuk mengundang pengguna lain
7. CHAT-SEND-PRIVATE : Digunakan untuk melakukan chat pada pengguna lain
8. CHAT-SEND-GROUP : Digunakan untuk melakukan chat pada grup obrolan. Obrolan hanya bisa dikirim di grup dimana pengguna merupakan member dari grup.
9. CHAT-GET-PRIVATE : Digunakan untuk menampilkan isi inbox dari obrolan yang belum difetch
10. CHAT-GET-GROUP : Digunakan untuk menampilkan isi inbox dari obrolan grupp yang belum difetch. Obrolan hanya bisa diambil di grup dimana pengguna merupakan member dari grup.
11. FILE-SEND-PRIVATE : Digunakan untuk bertukar file dengan pengguna lain
12. FILE-SEND-GROUP : Digunakan untuk mengirim file dalam grup
13. FILE-GET-PRIVATE : Digunakan untuk melakukan retrieve pada file yang dikirim oleh pengguna lain. 
14. FILE-GET-GROUP : Digunakan untuk melakukan retrieve pada file yg dikirim di grup
13. FRIEND-ADD : Digunakan untuk menjadikan pengguna lain sebagai teman
14. FRIEND-DELETE : Digunakan untuk menghapus pengguna lain sebagai teman
15. NOTIF-GET : Digunakan untuk menampilkan pesan-pesan yang belum di retrieve 
16. PERSONAL : Digunakan untuk menampilkan id dari pengguna

Argumen-argumen yang dibutuhkan untuk masing-masing kata kunci antara lain,
1. GROUP-CREATE [nama_grup] [tipe_grup(optional,default=open, option=open/close)] 
2. GROUP-DELETE [group_id]
3. GROUP-JOIN [kode_grup]
4. GROUP-EXIT [group_id] 
5. GROUP-INVITE [id_penggunateman] [group_id]
6. CHAT-PRIVATE-SEND [id_penggunateman] [pesan]
7. CHAT-PRIVATE-GET [id_penggunateman]
8. CHAT-GROUP-GET [group_id]
9. CHAT-GROUP-SEND [group_id] [pesan]
10. FILE-PRIVATE-SEND [id_penggunateman] [path_file] [ukuran_file]
11. FILE-GROUP-SEND [group_id] [path_file] [ukuran_file]
12. FILE-PRIVATE-GET [id_penggunateman] [kode_file]
13. FILE-GROUP-GET [id_group] [kode_file]
14. FRIEND-ADD [nama_pengguna]
15. FRIEND-DELETE [nama_pengguna]
