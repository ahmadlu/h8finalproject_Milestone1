-------Tugas Akhir Talent HUB------
bahan :Postman, navicat


1. import Database yang adadi folder dengan nama : milestone.db

2. Jalankan liblary flask dengan cara : 
	1. buka terminal
	2. buka fod
	3. jalankan script sebagai berikut : .\Scripts\activate 
	4. Setelah jalan env nya,jalankan script app.py
	5. clik/ copy http://127.0.0.1:5000/milestone di API POSTMAN(karena saya menggunakan API ini)

3. jalankan fungsi CRUD
	1. CREAT > ubah menjadi POST, dan http://127.0.0.1:5000/milestone
	misal : 
	{
   	 	"capaian": "Bisa membai ilmu bermanfaat ",
   		"waktu": "1 Januari 2024"
	}

		lalu send

	2. Read > ubah menjadi READ, dan http://127.0.0.1:5000/milestone
	
	3. Update > ubah menjadi PUT, dan http://127.0.0.1:5000/milestone/{id}

	4. Delete > ubah menjadi DELETE dan http://127.0.0.1:5000/milestone/{id}
	
	