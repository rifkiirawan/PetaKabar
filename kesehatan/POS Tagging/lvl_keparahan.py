# Untuk keparahan meninggal || sakit || sembuh 
# Jika ada yang meninggal lebih dari 15 langsung parah
# Jika ada yang sakit lebih dari 20 langsung parah 
# 

# ------------------------
# AREA PENGETESAN

meninggal = 0
sakit = 4
sembuh = 17

# ---------------------------


# Jika nol semua
if (meninggal==0 and sakit==0 and sembuh==0):
   keparahan="Rendah"

# Kondisi langsung parah 
elif(int(meninggal)>12 or int(sakit)>20 or int(sembuh)>50):
   keparahan="Tinggi"

# Meninggal
elif(int(meninggal)<=3 and sakit==0 and sembuh==0):
   keparahan="Rendah"
elif(int(meninggal)<=7 and int(meninggal)>=6 and sakit==0 and sembuh==0):
   keparahan="Sedang"
elif(int(meninggal)>12 and sakit==0 and sembuh==0):
   keparahan="Tinggi"

# Sakit 
elif(meninggal==0 and int(sakit)<=10 and sembuh==0):
   keparahan="Rendah"
elif(meninggal==0 and int(sakit)>10 and int(sakit)<=20 and sembuh==0):
   keparahan="Sedang "
elif(meninggal==0 and int(sakit)>20 and sembuh==0):
   keparahan="Tinggi"

# Sembuh
elif(meninggal==0 and sakit==0 and int(sembuh)<=20):
   keparahan ="Rendah"
elif(meninggal==0 and sakit==0 and int(sembuh)>20 and int(sembuh)<=50):
   keparahan ="Sedang"
elif(meninggal==0 and sakit==0 and int(sembuh)>50):
   keparahan ="Tinggi"

# Campuran sedang
elif(int(meninggal)<=3 and int(sakit)<=10 and int(sembuh)<=20):
   keparahan ="Sedang"
elif(int(meninggal)<=3 and int(sakit)<=10):
   keparahan ="Sedang"
elif(int(sakit)<=10 and int(sembuh)<=20):
   keparahan ="Sedang"
elif(int(meninggal)<=3 and int(sembuh)<=20):
   keparahan ="Sedang"

#Campuran parah
elif(int(meninggal)<=7 and int(meninggal)>=6 and int(sakit)>10 and int(sakit)<=20):
   keparahan ="Tinggi"
elif(int(sakit)>10 and int(sakit)<=20 and int(sembuh)>20 and int(sembuh)<=50):
   keparahan ="Tinggi"
elif(int(meninggal)<=7 and int(meninggal)>=6 and int(sembuh)>20 and int(sembuh)<=50):
   keparahan ="Tinggi"
print(keparahan)