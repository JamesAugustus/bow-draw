# Bow Draw

Bow Draw, Pascal üçgeni üzerine bir sayma sorusudur. Her k satırı için ⌊k/2⌋ ile ⌈k/2⌉ yarıları bir b tabanında toplanır ve eldeler sayılır. Kaç satırdan sonra toplam elde sayısı satır sayısına eşit olur? Cevap, b³'ün hemen ötesinde, yalnız b'nin 6'ya göre kalanına bağlı bir formülle verilen kesin bir n(b) noktasıdır. p asal tabanında bu toplam, c(1)·c(2)···c(n) merkez binom katsayıları çarpımında p'nin üssüdür; yani n(p), bu çarpımın p^n'ye bölünmeye başladığı tam noktadır.

[English](README.md)

> **Sürüm 1.0 (23 Kasım 2026).** Henüz başkaları tarafından incelenmedi. b ≥ 4 çift tabanlarda teklik ölçülmüştür, kanıtlanmamıştır.

## Sonuç ve örnek

Eldelerle satırlar arasındaki fark önce iner, b³ civarında en dibe varır ve sonra n(b) noktasında sıfırı keser. Bu nokta yalnız b'nin 6'ya göre kalanına bağlıdır:

```text
b çift:          n(b) = b³ + b² + b − 2
b ≡ 1 (mod 6):   n(b) = b³ + (2b² + 2b − 7) / 3
b ≡ 3 (mod 6):   n(b) = b³ + (2b² + 2b − 6) / 3
b ≡ 5 (mod 6):   n(b) = b³ + (4b² + 5b − 11) / 6
```

7 tabanında 1'den 378'e kadar satırların eldeleri toplamı tam 378'dir ve 378 = 7³ + 35'tir.

```text
b      2    3     5     7     11     13     17     19
n(b)   12   33   144   378   1419   2316   5118   7110
```

Makalelerde n(b)'nin her b ≥ 2 tabanında bir çözüm olduğunu kanıtlıyorum. Her tek tabanda ve 2 tabanında yazılı bir kanıt, n(b)'nin bir çözüm ve tek çözüm olduğunu gösteriyor; bu yüzden asal tabanlarda bilgisayar gerekmez. Öteki çift tabanlarda varlık kanıtı bilgisayar desteklidir. b ≥ 4 çift tabanlarda tekliği b < 2000 olan her tabanda sayarak denetledim, kanıtlamadım. Sonuç bir asallık testi veya çarpanlara ayırma yöntemi değildir.

## FactorX: içinde doğduğu dil

Bow Draw, FactorX'in içinden çıktı. FactorX sayıları üç durumla anlatır: hiçlik (0), varlık (1) ve düallik (iki varlığın yan yana gelmesi, `11`). Bir tabanın yazı dünyasına evren diyorum. Bir hane tabandan büyük bir sayıyı da tutabilir; buna geniş hane diyorum. Bu dilde her n ≥ 2 sayısı, tabanı n − 1 olan evrenin ilk çifti `[1][1]`'dir ve τ(n) − 1 evrende görünür. Burada τ(n) bölen sayısıdır. Asal sayı, yalnız tek bir evrende görünen sayıdır. Örneğin 12 beş evrende görünür: `[1][1]_11`, `[2][2]_5`, `[3][3]_3`, `[4][4]_2` ve `[6][6]_1`. 17 asalı yalnız `[1][1]_16` olarak görünür. Bu dil sonuçlarının içeriği klasiktir (FactorX, Bölüm 3.6); dil onlara tek bir resim verir.

## Okuma sırası

1. Bow Draw, hakemler için makale: [paper/BOW_DRAW_TR.pdf](paper/BOW_DRAW_TR.pdf) (Markdown: [paper/BOW_DRAW_TR.md](paper/BOW_DRAW_TR.md)). Tanımlar, teoremler ve kanıtları, problemin nereden çıktığı, bütün denetimler ve Ek A'da denetlenen 51 Mersenne asalının tam listesi.
2. FactorX, tam metin: [full/FACTORX_TR.pdf](full/FACTORX_TR.pdf) (Markdown: [full/FACTORX_TR.md](full/FACTORX_TR.md)). Bölüm 2 dilin sözlüğüdür, Bölüm 3 dilin üç teoremini verir. Bölüm 4 ile 7 Bow Draw'dır. Bölüm 4 tanımları, Bölüm 6.1 ifadeleri, Bölüm 7 işlenmiş örnekleri verir. Bölüm 8 ve 9 denetimleri ve sınırları verir.
3. Test kaydı: [tests/RESULTS.md](tests/RESULTS.md). Komutlar ve ham çıktıları İngilizcedir.
4. Programların hepsi [tests/](tests/) içindedir: Python `tests/` altında, C taramaları [tests/c/](tests/c/), ekran kartı taraması [tests/gpu/](tests/gpu/) altında.
5. Öğretim için bir gösteri: [demo/bow_draw_demo.html](demo/bow_draw_demo.html). Türkçe ve İngilizce tek bir HTML dosyası. İndirip tarayıcıda açmak yeter; kurulum ve internet gerekmez. Bir b tabanı seçilir, yay o tabanın eldeleriyle gerilir ve ok tam sayılarla hesaplanan n(b)'ye düşer. `bow_draw_demo.html?selftest=1` kendi denetimini yazar ve bir özet satırıyla biter.

## Nasıl çalıştırılır?

Ana denetimler için Python 3.8 veya sonrası yeter. Üçüncü taraf paket gerekmez. Paket kökünden:

```sh
python3 tests/check_small.py
python3 tests/check_certificates.py
python3 tests/check_proof_steps.py
python3 tests/check_odd_existence.py
python3 tests/check_primes.py
python3 tests/check_composite.py
python3 tests/check_universe_language.py
```

Her program her durum için PASS (geçti) veya FAIL (kaldı) işaretli bir satır yazar ve bir özetle biter: başarısızlık sayısı ya da bütün koşu için PASS. `check_small.py`, 41'den küçük her tabanda 3b³ + 300'e kadar her n'yi sayar. `check_certificates.py`, her taban için bilgisayar destekli varlık kanıtıdır (tek tabanlarda ve 2 tabanında ayrıca yazılı bir kanıt var). `check_proof_steps.py`, teklik kanıtının her adımını tek tabanlarda denetler; `check_odd_existence.py` de tek tabanlar için yazılı varlık kanıtının Adım 6'sını denetler (varsayılan b ≤ 101; 401'e kadar tam koşu tests/RESULTS.md'de). `check_primes.py`, kapalı biçimi varsayılan olarak bir milyondan küçük bütün asallarda ve 20 ile 200 basamaklı 200 rastgele asalda kullanır; tests/RESULTS.md'deki tam koşu 10¹⁰'dan küçük bütün asalları ve 12 000 rastgele asalı kullandı. `check_universe_language.py`, Bölüm 3'ün üç teoremini denetler.

İsteğe bağlı denetimler ek yazılım ister. `tests/check_mersenne.py` gmpy2 ister. Varsayılan olarak üssü 4423'e kadar olan 19 Mersenne asalını birkaç saniyede denetler. 51'inin tamamı için `python3 tests/check_mersenne.py 136279841 132049 2` yaklaşık 45 dakika sürer (tests/RESULTS.md'de 2646 s). `tests/make_figures.py` numpy ve matplotlib ister. C programları OpenMP destekli bir C derleyicisi ister:

```sh
gcc -O3 -march=native -fopenmp tests/c/bow_draw_scan.c -o bow_draw_scan
./bow_draw_scan 400
gcc -O3 -march=native -fopenmp tests/c/bow_draw_composite.c -o bow_draw_composite
./bow_draw_composite 500
```

Ekran kartı taraması 64 bit gölgelendirici tam sayılarıyla Vulkan 1.2 ve `glslc` ister. `sh tests/gpu/build.sh` ile derlenir ve `./tests/gpu/bow_draw_gpu 1000` ile çalıştırılır.

## Dosyalar ve koşullar

- `paper/`: hakemler için Bow Draw makalesi, Türkçe (`BOW_DRAW_TR`) ve İngilizce (`BOW_DRAW_EN`), PDF ve Markdown.
- `full/`: FactorX tam metni, dil ve sezgilerimle, Türkçe (`FACTORX_TR`) ve İngilizce (`FACTORX_EN`).
- `README.md`: bu sayfanın İngilizcesi.
- `figures/`: beş şekil, İngilizce ve Türkçe (`_tr` ekli).
- `demo/`: öğretim gösterisi, tek bir HTML dosyası.
- `tests/`: programlar (Python, C `tests/c/`, Vulkan `tests/gpu/`), test kaydı `tests/RESULTS.md` ve Mersenne sonuçlarının tablosu `tests/mersenne.csv`. Program çıktıları İngilizcedir.
- Lisanslar: bütün kaynak kod, testler ve gösteri [MIT](LICENSE) kapsamındadır. İngilizce ve Türkçe metin, PDF'ler, şekiller, tablolar ve atıf bilgisi [CC BY 4.0](LICENSE-CC-BY-4.0) kapsamındadır. Telif hakkı © 2026 James Augustus. Her lisans kendi malzemesine uygulanır. Bütün dosyalar için iki lisans arasında seçim sunulmaz.
- [CITATION.cff](CITATION.cff): atıf bilgisi.

## Nasıl atıf yapılır

Bu çalışmayı bir derste, konuşmada, makalede ya da programda kullanırsanız lütfen şöyle atıf yapın:

> James Augustus, "Bow Draw: where the carries of the central binomial coefficients catch up with the number of rows", version 1.0, 2026, doi:10.5281/zenodo.24451375.

> James Augustus, "FactorX: the universe language of numbers and its main example, Bow Draw", 2026, ORCID 0009-0002-7286-7730.

Depo: https://github.com/JamesAugustus/bow-draw · DOI: [10.5281/zenodo.24451375](https://doi.org/10.5281/zenodo.24451375) (Zenodo'da arşivli). Atıf bilgisi [CITATION.cff](CITATION.cff) dosyasındadır.

Düzeltmeler ve eksik kaynaklar memnuniyetle karşılanır. Sonraki sürümde eklerim ve bildireni anarım.

James Augustus · ORCID [0009-0002-7286-7730](https://orcid.org/0009-0002-7286-7730) · jamesaugustus1313@gmail.com
