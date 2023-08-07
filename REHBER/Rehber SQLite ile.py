"""
1- SQLite üzerinde saklanacak bir telefon rehberi oluşturdum.
2- Rehber aynı kişiye ait birçok telefon numarasını saklayabilecek bir yapıdadır.
3- Programda bir menü vardır ve ilgili seçenekler seçildiğinde kayıtlar üzerinde 
arama, ekleme, silme ve güncelleme (tel numarasını değiştirme gibi) işlemleri yapar.
4- Arama yaparken iki seçenek vardır: Hem telefon numarası verilip ilgili isim getirilebilir
hem de isim verilip telefon numarası getirilebilir."""


import sqlite3

def ID_Getir(Ad, Soyad):
    cur.execute("SELECT KisiID FROM Kisiler WHERE Ad = ? AND Soyad = ?", (Ad, Soyad))
    return cur.fetchone()

def Tel_Getir(Kisi):
    cur.execute("SELECT Tür, Numara FROM Numaralar WHERE Kisi = ?", str(Kisi[0]))
    return cur.fetchall()
        
def KisiTür_Getir(Tel):
    cur.execute("SELECT Ad, Soyad, Tür FROM Kisiler, Numaralar " +
                "WHERE KisiID = Kisi AND Numara = '" + Tel + "'")
    return cur.fetchone()

con = sqlite3.connect("rehber.db", isolation_level = None) # autocommit
con.execute("CREATE TABLE IF NOT EXISTS Kisiler(KisiID INTEGER PRIMARY KEY, Ad, Soyad)")
con.execute("CREATE TABLE IF NOT EXISTS Numaralar(Kisi INTEGER, Tür, Numara)")
cur = con.cursor()

while True:
    secim = input("1) İsme Göre Arama\n" +
                  "2) Telefon Numarasına Göre Arama\n" +
                  "3) Çıkış\n")
    if secim == '1':
        Ad = input("Ad: ").title() # title(): ilk harfleri büyük harf yapar
        Soyad = input("Soyad: ").title()
        KisiID = ID_Getir(Ad, Soyad)
        if KisiID:
            KisiID = str(KisiID[0])
            print("Aradığınız kişinin numaraları:")
            for i in Tel_Getir(KisiID):
                print(i[0], i[1])

            secim2 = input("...1) İsmi Değiştir\n" +
                           "...2) Kişiyi Sil\n" +
                           "...3) Numarayı Değiştir\n" +
                           "...4) Numarayı Sil\n" +
                           "...5) Numara Ekle\n")
            if secim2 == '1':
                Ad = input("Ad: ")
                Soyad = input("Soyad: ")
                con.execute("UPDATE Kisiler SET Ad = ?, Soyad = ? WHERE KisiID = ?", (Ad, Soyad, KisiID))
            if secim2 == '2':    
                con.execute("DELETE FROM Kisiler WHERE Ad = ? AND Soyad = ?", (Ad, Soyad))
                con.execute("DELETE FROM Numaralar WHERE Kisi = ?", KisiID)
            if secim2 == '3':    
                Tür = input("Güncellenecek telefon numarasının türü: ")
                Tel = input("Yeni telefon numarası: ")
                con.execute("UPDATE Numaralar SET Numara = ? WHERE Tür = ? AND Kisi = ?", (Tel, Tür, KisiID))
            if secim2 == '4':    
                Tür = input("Silinecek telefon numarasının türü: ")
                con.execute("DELETE FROM Numaralar WHERE Tür = ? AND Kisi = ?", (Tür, KisiID))
            if secim2 == '5':
                Tel = input("Eklemek istediğiniz telefon numarası: ")
                Tür = input("Bu telefon numarasının türü: ")
                con.execute("INSERT INTO Numaralar VALUES(?,?,?)", (KisiID,Tür,Tel))

        else:
            secim2 = input("Aradığınız kişi rehberde bulunamadı.\n" +
                           "Yeni kişi olarak eklensin mi? (E/H)\n")
            if secim2 == 'E' or secim2 == 'e':
                con.execute("INSERT INTO Kisiler(Ad,Soyad) VALUES(?,?)", (Ad, Soyad))
                KisiID = ID_Getir(Ad, Soyad)
                KisiID = str(KisiID[0])
                Tel = input("Eklemek istediğiniz telefon numarası: ")
                Tür = input("Bu telefon numarasının türü: ")
                con.execute("INSERT INTO Numaralar VALUES(?,?,?)", (KisiID, Tür, Tel))
    
    if secim == '2':
        Tel = input("Tel No: ")
        KisiTür = KisiTür_Getir(Tel)
        if KisiTür:
            print(KisiTür[0] + " " + KisiTür[1], "kişisin", KisiTür[2], "numarası\n")
        else:
            print("Aradığınız numara rehberde bulunamadı\n")
        
    if secim == '3': break
