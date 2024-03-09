from multiprocessing import Process, Manager
import re

def kelime_say(start, end, dosya_adi, sonuc_sozlugu, toplam_kelimeler_listesi):
    kelimeler = {}
    toplam_kelimeler = 0
    with open(dosya_adi, 'r') as dosya:
        dosya.seek(start)
        parcacik = dosya.read(end - start)
        for kelime in re.findall(r'\w+', parcacik):#liste
            kelimeler[kelime] = kelimeler.get(kelime, 0) + 1
            toplam_kelimeler += 1
    sonuc_sozlugu.update(kelimeler)#sözlüğe sözlük ekler
    toplam_kelimeler_listesi.append(toplam_kelimeler)

def ana(dosya_adi, n_islemler):
    dosya_boyutu = 0
    with open(dosya_adi, 'r') as dosya:
        dosya.seek(0, 2)
        dosya_boyutu = dosya.tell()

    parcacik_boyutu = dosya_boyutu // n_islemler
    islemler = []
    yonetici = Manager()
    sonuc_sozlugu = yonetici.dict()
    toplam_kelimeler_listesi = yonetici.list()

    for i in range(n_islemler):
        baslangic = i * parcacik_boyutu
        son = baslangic + parcacik_boyutu
        if i == n_islemler - 1:
            son = dosya_boyutu
        islem = Process(target=kelime_say, args=(baslangic, son, dosya_adi, sonuc_sozlugu, toplam_kelimeler_listesi))
        islemler.append(islem)
        islem.start()

    for islem in islemler:
        islem.join()

    toplam_kelimeler = sum(toplam_kelimeler_listesi)

    # Sonuçları yazdır
    print("Her işlem tarafından okunan toplam kelime sayısı:")
    for i, sayi in enumerate(toplam_kelimeler_listesi):
        print(f"İşlem {i+1}: {sayi}")
    print("Tüm işlemler tarafından okunan toplam kelime sayısı:", toplam_kelimeler)

if __name__ == "__main__":
    dosya_adi = "oku.txt"  # Dosya adını buraya girin
    n_islemler = 3  # İşlem sayısını buraya girin
    ana(dosya_adi, n_islemler)
