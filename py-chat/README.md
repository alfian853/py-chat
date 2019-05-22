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
- create [nama grup]-> membuat grup baru
- get -> mendapatkan daftar grup yang telah tergabung
- join [kode grup] -> bergabung ke dalam grup
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
1. GROUP-CREATE *[nama_grup]* : Digunakan untuk membuat grup obrolan baru
2. GROUP-GET : Digunakan untuk mendapatkan daftar grup yang telah bergabung
3. GROUP-JOIN *[kode_grup]* : Digunakan untuk bergabung pada grup obrolan
4. GROUP-EXIT *[kode_grup]* : Digunakan untuk keluar dari grup obrolan.
5. GROUP-INVITE *[kode_grup]* *[nama_teman 1..N]* : Digunakan untuk mengundang pengguna lain untuk masuk kedalam grup. Pengguna yang menggunakan fitur ini harus terotorisasi sebagai admin grup untuk mengundang pengguna lain

6. CHAT-PRIVATE-SEND *[id_penggunateman* *[pesan]* : Digunakan untuk melakukan chat pada pengguna lain
7. CHAT-GROUP-SEND *[group_id]* *[pesan]* : Digunakan untuk melakukan chat pada grup obrolan. Obrolan hanya bisa dikirim di grup dimana pengguna merupakan member dari grup.
8. CHAT-PRIVATE-GET *[id_penggunateman]* : Digunakan untuk menampilkan isi inbox dari obrolan yang belum difetch
9. CHAT-GROUP-GET *[group_id]* : Digunakan untuk menampilkan isi inbox dari obrolan grupp yang belum difetch. Obrolan hanya bisa diambil di grup dimana pengguna merupakan member dari grup.
10. FILE-SEND-PRIVATE [id_penggunateman] [path_file] [ukuran_file] : Digunakan untuk bertukar file dengan pengguna lain
11. FILE-SEND-GROUP [group_id] [path_file] [ukuran_file] : Digunakan untuk mengirim file dalam grup
12. FILE-GET-PRIVATE [id_penggunateman] [kode_file] : Digunakan untuk melakukan retrieve pada file yang dikirim oleh pengguna lain. 
13. FILE-GET-GROUP [id_group] [kode_file] : Digunakan untuk melakukan retrieve pada file yg dikirim di grup
14. CONTACT-ADD *[nama_pengguna]* : Digunakan untuk menjadikan pengguna lain sebagai teman
15. CONTACT-GET : Digunakan untuk mendapatkan daftar teman
16. CONTACT-DELETE *[nama_pengguna]* : Digunakan untuk menghapus pengguna lain sebagai teman
17. NOTIF-GET : Digunakan untuk menampilkan pesan-pesan yang belum di retrieve