# HTTP Server

### Perbandingan performa Server dengan menggunakan Load Balancer
![tabel](https://user-images.githubusercontent.com/32873349/58160163-20e8fa00-7ca8-11e9-85b8-c3426100e00e.png)

Tabel diatas merupakan waktu yang diperlukan untuk merespon server dengan jumlah request dan konkurensi yang berbeda-beda. Dari tabel diatas dapat dilihat bahwa semakin banyak request yang dikirimkan, maka waktu yang diperlukan server untuk merespon akan semakin lama. Selain itu waktu yang diperlukan oleh server Asynchronous untuk merespon jauh lebih cepat dibandingkan dengan waktu respon server Synchronous. 

Load Balancer, digunakan agar beban server dalam menangani request dibagi agar server menjadi lebih cepat dalam merespon request. Dari tabel diatas, dapat dilihat bahwa penggunaan Load Balancer pada server Asynchronous, membuat waktu yang diperlukan untuk merespon request menjadi lebih cepat. Hal ini terutama sangat terlihat jelas dengan penggunaan konkurensi yang lebih besar, perbedaan waktu yang diperlukan terlihat signifikan.

Sedangkan pada server Synchronous, waktu yang diperlukan untuk merespon request cenderung stabil berapapun konkurensi yang digunakan dan berapapun request yang dikirimkan.
  
    
### gambar hasil perbandingan dengan menggunakan Apache Benchmark dapat dilihat di file .pdf
