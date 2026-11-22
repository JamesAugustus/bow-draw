# Bow Draw

James Augustus · ORCID [0009-0002-7286-7730](https://orcid.org/0009-0002-7286-7730)

Merkez binom katsayılarında eldelerin satır sayısına yetiştiği nokta

Sürüm 1.0, 23 Kasım 2026

## Öz

b ≥ 2 bir taban olsun. Pascal üçgeninin her k ≥ 1 satırı için ⌊k/2⌋ ile ⌈k/2⌉ yarıları b tabanında toplanır ve eldeler sayılır. E_b(n), 1'den n'ye kadar satırlardaki eldelerin toplamıdır. b bir p asalı olduğunda Kummer'in teoremine göre E_p(n), c(k) = C(k, ⌊k/2⌋) merkez binom katsayılarının c(1)·c(2)···c(n) çarpımında p'nin üssüdür. E_b(n) − n farkı önce iner, b³ civarında en dibe varır, sonra yükselir ve sıfırı keser (b ≥ 4 çift tabanlarda bu biçim ölçülmüştür, kanıtlanmamıştır). Kesişme noktasına Bow Draw noktası diyorum ve onu n(b) ile gösteriyorum. Bu nokta yalnız b'nin 6'ya göre kalanına bağlı bir formülle tam olarak verilir. Örneğin her çift b için n(b) = b³ + b² + b − 2'dir ve n(7) = 378'dir.

Her b ≥ 2 tabanı için E_b(n(b)) = n(b) olduğunu polinom sertifikalarına dayanan bilgisayar destekli bir kanıtla gösteriyorum. Her tek taban ve b = 2 için ayrıca n(b)'nin bir çözüm olduğunu, tek çözüm olduğunu ve E_b(n) − n'nin işaretini yalnız orada değiştirdiğini elle kanıtlıyorum. Böylece her asal taban için sonuç bilgisayar gerektirmez. b ≥ 4 çift tabanlarda teklik kanıtlanmamış, ölçülmüştür: b < 2000 olan her tabanda 3b³ + 300'e kadar her n'yi saydım.

Programların sınaması olarak yer formülünü ayrıca tam sayı aritmetiğiyle 5 ≤ p < 10¹⁰ olan bütün asallarda (2 ve 3 tabanlarını doğrudan saydım), 20 ile 200 basamak arasındaki 12 000 rastgele asalda ve 3 ≤ e ≤ 136 279 841 aralığındaki bilinen 2^e − 1 Mersenne asallarında denetledim. Bunlar 22 Kasım 2026'da bilinen 52 Mersenne asalından (GIMPS listesi [7]) en küçüğü olan 2² − 1 = 3 dışındaki 51 tanesidir. 51'inin hepsi Ek A'da listelenmiştir. Bileşik bir m için c(1)···c(n) çarpımında m'nin üssü başka bir büyüklüktür. Karesiz m için K_m(n) = n denkleminin (Bölüm 5.7) yalnız bir çözümü vardır ve çözüm en büyük asal çarpanın noktasıdır: her asalın kendi noktası vardır, karesiz bir bileşik ise bir asalın noktasını alır.

Bölüm 2, problemin nereden çıktığını anlatır. Bütün programlar ham çıktılarıyla birlikte paketin içindedir.

## 1. Amaç ve kapsam

Soru kısaca şudur. Eldeler satır satır sayılır. Kaç satırdan sonra toplam elde sayısı satır sayısına eşit olur? Bu soruyu her b ≥ 2 tabanı için yanıtlıyorum; tekliği tek b ve b = 2 için kanıtlıyorum. Tanımları, yer formülünü, kanıtları, küçük ve büyük işlenmiş örnekleri ve her sayıyı yeniden üreten programları veriyorum. Ayrıca farklı tabanların kesişme noktalarının birbirine göre nerede durduğunu anlatıyorum.

Burada bir asallık testi, çarpanlara ayırma yöntemi veya donanım tasarımı anlatmıyorum. Bir ifade yalnız sonlu bir aralıktaki sayıma dayanıyorsa bunu aralığıyla birlikte söylüyorum.

## 2. Problem nereden çıktı

Soru bir sayımdan çıktı. Önceki çalışmamda Pascal satırlarını Mersenne tabanlarında eldesiz okuyordum (N(p) eşik formülü [8]). Oradan merkez binom katsayılarının çarpımına ve bu çarpımda her asalın üssüne geçtim. Bu üsleri satır satır izleyen bir program (Factorx), her asal için üssün satır sayısına tam bir kez yetiştiğini gösterdi: 2 için 12'de, 3 için 33'te, 5 için 144'te ve 7 için 378'de. Yer formülünü bu sayılardan geriye doğru çıkardım, sonra kanıtladım (13 Kasım 2026). 22 Kasım 2026'da sonucu her tabana genişlettim, 23 Kasım 2026'da da tek tabanlarda varlığı ve yeri elle kanıtladım.

Çıkış noktası, kendi sözlerimle:

> "Sayı her zaman son hâli kadar güçlüdür. … 6+6 = 7'dir, çünkü önceki 6'nın emeği olmadan 7 olmaz. … O 5 dakikada çözmedi, çünkü 30 yıl + 5 dakikada çözdü. … 6'dan sonra 7 gelir ama 6'dan 1 sonra olarak değil, 6'ya bir kendi varlığı geldiği için 7 gelir."

Burada "+" sıradan toplama değildir. Dolu bir sayacın taşıp bir sonrakine tek bir birim vermesi demektir: 6 tabanında 7, 11 diye yazılır. Sayı bir birikimdir ve saydığım eldeler tam olarak bu taşmalardır.

Ad, bir atışı anlatışımdan gelir:

> "Atış hareketi gibi, aldığım aim kadar gider yani. Yani ben ne kadar oku gerersem o kadar uzağa gider. Limitim oktur."

E_b(n) − n farkı önce, gerilen bir yay gibi aşağı iner, sonra sıfırı keser: ok oraya düşer. Taban büyüdükçe ok uzağa, b³'ün biraz ötesine düşer. Öteki sezgilerim, genel anlamlarıyla birlikte, eşlik eden FactorX belgesinin ekindedir [9].

## 3. Tanımlar ve gösterimler


### 3.1 Taban, haneler ve elde

Taban b ≥ 2 bir tam sayıdır. Her x ≥ 0 tam sayısının b tabanında 0 ile b − 1 arasında haneleri vardır. x ile y hane hane toplanırken bir konumdaki hane toplamı, gelen eldeyle birlikte b'ye ulaşırsa o konumda elde oluşur. Elde sayısı carries_b(x, y) ile gösterilir.

Bir i konumuna gelen elde ⌊(x + y)/b^i⌋ − ⌊x/b^i⌋ − ⌊y/b^i⌋'dir. Buradan şu eşitlik çıkar:

```text
carries_b(x, y) = Σ_{i ≥ 1} ( ⌊(x + y)/b^i⌋ − ⌊x/b^i⌋ − ⌊y/b^i⌋ )    (3.1)
                = ( s_b(x) + s_b(y) − s_b(x + y) ) / (b − 1)    (3.2)
```

Burada s_b(x), x'in b tabanındaki hanelerinin toplamıdır. İki biçim de asal veya bileşik her tabanda geçerlidir.

### 3.2 Satırlar, merkez katsayılar ve elde toplamı

Pascal satırları k = 0'dan başlayarak numaralanır. k satırında k + 1 eleman vardır. k satırının merkez katsayısı satırın en büyük elemanıdır (OEIS A001405 [3]):

```text
c(k) = C(k, ⌊k/2⌋)

k      1   2   3   4    5    6    7    8     9    10
c(k)   1   2   3   6   10   20   35   70   126   252
```

k ≥ 1 için k satırının b tabanındaki elde sayısı

```text
κ_b(k) = carries_b(⌊k/2⌋, ⌈k/2⌉)
```

ve n satırına kadarki elde toplamı

```text
E_b(n) = κ_b(1) + κ_b(2) + ... + κ_b(n)
E_b(0) = 0
D_b(n) = E_b(n) − n
```

olarak tanımlanır. D_b(n), birikmiş eldelerle satır sayısı arasındaki farktır.

### 3.3 Kummer'in teoremi

p asal ve N ≥ 1 bir tam sayı olmak üzere v_p(N), N'de p'nin üssünü, yani p^e'nin N'yi böldüğü en büyük e'yi gösterir. v_p(C(x + y, x)) üssü carries_p(x, y)'dir [1] (ayrıca Granville'in derlemesine bakın [10]). Bu yüzden κ_p(k), c(k)'da p'nin üssüdür ve E_p(n), c(1)·c(2)···c(n) çarpımında p'nin üssüdür.

p = 3 ve k = 10 örneği. İki yarı 5 ve 5'tir. 3 tabanında 5 = 12 yazılır.

```text
      1 2
    + 1 2
    -----
    2 + 2 = 4 ≥ 3            elde 1
    1 + 1 + 1 = 3 ≥ 3        elde 2
```

İki elde vardır. Gerçekten c(10) = 252 = 4 · 9 · 7'dir ve 3'ün üssü 2'dir.

Bileşik bir b tabanında E_b(n) yine iyi tanımlı bir elde sayısıdır, fakat çarpımda b'nin üssü değildir. Bileşik bir m'nin üssü başka bir fonksiyondur ve Bölüm 5.7'de K_m(n) olarak ele alınır.

### 3.4 Bow Draw noktası

(5.1) formülünün verdiği n(b) sayısına b'nin Bow Draw noktası diyorum. Teorem 1, her b ≥ 2 için E_b(n(b)) = n(b) olduğunu gösterir. Tek b ve b = 2 için başka çözüm yoktur (Teorem 2). Çift b ≥ 4 için sayılan aralıkta başka çözüm bulunmadı (Bölüm 5.1). Ad, D_b'nin biçimini anlatır. Fark önce, gerilen bir yay gibi aşağı iner. En dibe b³ civarında varır. Sonra yükselir ve sıfırı n(b)'de keser. Okun düştüğü yer burasıdır.

### 3.5 İfadelerin durumu

| Etiket | Anlamı |
|---|---|
| GEÇERLİ (kanıt) | Bu makalede yazılı bir kanıtla gösterilmiştir |
| GEÇERLİ (bilgisayar destekli kanıt) | Bu makalede kanıtlanmıştır. Bir adım, tam aritmetikle programla denetlenen sonlu sayıda polinom eşitsizliğidir |
| ÖLÇÜLDÜ | Yalnız belirtilen aralıkta programla sayılmıştır. Kanıt yoktur |
| SINANMADI | Ne kanıtlanmış ne sayılmıştır |

Programlar sonucu PASS (geçti) veya FAIL (kaldı) olarak yazar.

## 4. Yöntem

### 4.1 Doğrudan sayım

İlk yöntem tanımı izler. Program 1'den bir N sınırına kadar her n için n'nin iki yarısını b tabanında hane hane toplar ve eldeleri bir toplama ekler. D_b(n)'nin her sıfırını, ilk sıfırdan önceki ve sonraki işaretini ve en küçük değerinin yerini ve değerini kaydeder. Her yerde kullanılan sınır N = 3b³ + 300'dür. Bu, beklenen kesişme noktasının yaklaşık üç katıdır. Bu yöntem hiçbir formül kullanmaz. `tests/check_small.py` ve `tests/c/bow_draw_scan.c` içinde uygulanmıştır.

### 4.2 Kapalı biçim

İkinci yöntem, E_b(n)'yi önceki satırları gezmeden tek bir n için hesaplar. b tabanı için şunlar tanımlanır:

```text
f(m)     = Σ_{i ≥ 1} ⌊m / b^i⌋
g(n, q)  = Σ_{k=1..n} ⌊k / q⌋ = q · a(a − 1)/2 + a(r + 1)
           burada n = a·q + r, 0 ≤ r < q
S(n)     = f(1) + f(2) + ... + f(n) = Σ_{i ≥ 1} g(n, b^i)
```

(3.1)'den κ_b(k) = f(k) − f(⌊k/2⌋) − f(⌈k/2⌉) olur. k üzerinden toplanınca

```text
E_b(n)  = S(n) − T(n)
T(2m)   = 4·S(m) − f(m)
T(2m+1) = T(2m) + f(m) + f(m + 1)    (4.1)
```

elde edilir. T(n), k = 1'den n'ye f(⌊k/2⌋) + f(⌈k/2⌉) toplamıdır. n = 2m için k = 2j çift satırları j = 1'den m'ye 2f(j) katar. k = 2j + 1 tek satırları j = 0'dan m − 1'e f(j) + f(j + 1) katar. Toplam 2S(m) + (S(m) − f(m)) + S(m) = 4S(m) − f(m)'dir. Tek durum 2m + 1 satırını ekler.

g formülü ⌊k/q⌋ = j olan k'leri sayar. 1 ≤ j < a için bunlardan q tane, j = a için r + 1 tane vardır. E_b(n)'nin her değeri, n büyüklüğündeki tam sayılarla O(log_b n) işlemle hesaplanır. p asalı için f(m), m!'de p'nin üssüdür (Legendre formülü [2]).

b = 7 ve n = 378, yani m = 189 örneği: S(378) = 11 388, S(189) = 2760, f(189) = 30, T(378) = 4 · 2760 − 30 = 11 010 ve E_7(378) = 11 388 − 11 010 = 378.

### 4.3 Ekran kartında blok taraması

Üçüncü yöntem, doğrudan sayımı bağımsız bir uygulama olarak Vulkan hesap gölgelendiricileriyle ekran kartında yineler. Kart ⌊n/2⌋ ve ⌈n/2⌉ değerlerini b tabanında hane dizileri olarak tutar. n'den n + 1'e geçerken iki yarıdan yalnız biri bir artar. Bu yüzden bölme gerekmez. Kart aralığı 256 ardışık n'lik bloklara böler. Her blok için κ_b(n) − 1 toplamını ve blok içindeki en küçük ve en büyük kısmi toplamı döndürür. İşlemci blokları sırayla toplar ve böylece D_b'yi her blok sınırında bilir. Sonra sıfırın düşebileceği her bloğu ve en küçük değeri içeren bloğu işlemcide yeniden sayar. Program `tests/gpu/bow_draw_gpu.c`, gölgelendirici `tests/gpu/bow_draw_block64.comp` dosyasındadır. 64 bit tam sayılar kullanılır.

### 4.4 Polinom sertifikaları

Dördüncü yöntem varlığı kanıtlar. r, 0 ile 11 arasında olmak üzere b = 12t + r yazılır. On iki sınıfın her birinde (5.1)'deki n(b), t'nin rasyonel katsayılı bir polinomudur. (4.1) kapalı biçimindeki her ⌊x(t)/q(t)⌋ tam kısmında pay x(t) bir polinomdur, payda q(t) ise b, b² veya b³'tür. Program her tam kısım için interpolasyonla aday bir F(t) polinomu bulur. Sonra her t ≥ t₀ için 0 ≤ x(t) − q(t)F(t) ≤ q(t) − 1 olduğunu gösterir. Bunun için t yerine t + t₀ konur ve iki polinomun bütün katsayılarının negatif olmadığı denetlenir. Her tam kısım sertifikalı polinomuyla değiştirilince E_b(n(b)) − n(b), t'nin bir polinomu olur. Program bunun sıfır polinom olduğunu denetler. t₀'ın altındaki tabanlar doğrudan denetlenir. Bütün aritmetik tamdır. Sertifikayı üç olgu kanıt yapar. Birincisi, F(t) altı ardışık tam sayıda tam sayı değerlerinden geçer ve derecesi en çok 5'tir; bu yüzden bütün ileri farkları tam sayıdır ve F(t) her tam sayı t için bir tam sayıdır. İkincisi, x(t) sınıfın her b'si için bir tam sayıdır: n(b), t'nin tam sayı değerli bir kübik polinomudur ve paritesi sınıf içinde sabittir (tam sayı değerli bir kübiğin paritesi 4'ü bölen bir dönemle tekrar eder; program 60 ardışık değeri denetler). F ve x tam sayı değerli olunca 0 ≤ x − qF ≤ q − 1 tam olarak F = ⌊x/q⌋ demektir. Üçüncüsü, program b³ ≤ n(b) < b⁴ ve m + 1 < b³ eşitsizliklerini de sertifikalar; böylece kapalı biçimin terim sayısı bütün sınıfta sabittir (Bölüm 5.3). Program `tests/check_certificates.py` dosyasındadır.

## 5. Matematiksel ilişki

### 5.1 Ana sonuçlar

**Teorem 1 (varlık).** Her b ≥ 2 tam sayısı için E_b(n(b)) = n(b)'dir. Burada

```text
b çift:              n(b) = b³ + b² + b − 2
b ≡ 1 (mod 6):       n(b) = b³ + (2b² + 2b − 7) / 3
b ≡ 3 (mod 6):       n(b) = b³ + (2b² + 2b − 6) / 3
b ≡ 5 (mod 6):       n(b) = b³ + (4b² + 5b − 11) / 6    (5.1)
```

**Teorem 2 (teklik ve işaret).** b tek veya b = 2 olsun. O zaman E_b(n) = n eşitliğini sağlayan tek n ≥ 1 sayısı n(b)'dir. Ayrıca 1 ≤ n < n(b) için D_b(n) < 0 ve n > n(b) için D_b(n) > 0'dır.

**Teorem 3 (derinlik).** Tek b için D_b(n)'nin bütün n ≥ 1 üzerindeki en küçük değeri −(b − 1)(b + 2)'dir. Bu değer n = b³ − 1'de alınır.

| İfade | Durum |
|---|---|
| Teorem 1, her b ≥ 2 | GEÇERLİ (bilgisayar destekli kanıt), Bölüm 5.3 |
| Teorem 1, tek b ve b = 2 | GEÇERLİ (kanıt), Bölüm 5.4 ve 5.5 |
| Teorem 2, tek b ve b = 2 | GEÇERLİ (kanıt), Bölüm 5.4 ve 5.5 |
| Teorem 3, tek b | GEÇERLİ (kanıt), Bölüm 5.4 |
| Teorem 4, karesiz m | GEÇERLİ (kanıt), Bölüm 5.7 |
| En uzak asal kuvvet çarpanı kuralı, bileşik m | ÖLÇÜLDÜ: 2 ≤ m ≤ 1000, üç istisna (72, 360, 544) |
| b ≥ 4 çift tabanlarda teklik ve işaret düzeni | ÖLÇÜLDÜ: 4 ≤ b < 2000 olan her çift b'de her n ≤ 3b³ + 300 |
| b ≥ 4 çift tabanlarda en küçük değer −(b² − 2); ilk kez n = b³ − b² − 1'de alınır ve n = b³ − b² + b − 1'e kadar sürer | ÖLÇÜLDÜ: 4 ≤ b < 600 olan her çift b |
| b ≥ 4 çift tabanlarda sayılan aralığın ötesinde teklik | SINANMADI |

p ≥ 5 asalları için (5.1) formülünün tek satırlık bir biçimi vardır. ε = p mod 3 (1 veya 2) ile

```text
n(p) = p³ + (4p² + (3 + ε)·p + 3ε − 17) / 6    (5.2)
```

En küçük iki asal (5.1) kapsamındadır: n(2) = 12 ve n(3) = 33.

```text
b      2    3    4     5     6     7     8     9
n(b)   12   33   82   144   256   378   582   787

b      10     11     12     13     14     15     16
n(b)   1108   1419   1882   2316   2952   3533   4366
```

n(b)'nin paritesi b'nin 12'ye göre kalanına bağlıdır. n(b) tam olarak b ≡ 3, 9 veya 11 (mod 12) olduğunda tektir, diğer durumlarda çifttir. Değer, b'nin 6'ya göre kalanına bağlıdır. Sınıfların doğrusal terimleri farklı olduğu için bütün tek tabanları kapsayan tek bir polinom yoktur.

Kendi b tabanında n(b) ve m = ⌊n(b)/2⌋ sabit hanelerle yazılır, en büyük basamak önce (GEÇERLİ, kanıt):

| Sınıf | b tabanında n(b) | b tabanında m = ⌊n(b)/2⌋ |
|---|---|---|
| b çift | (1, 1, 0, b−2) | (b/2, b/2, b/2−1) |
| b ≡ 1 (mod 6) | (1, 0, (2b+1)/3, (b−7)/3) | ((b−1)/2, (5b+1)/6, (b−7)/6) |
| b ≡ 3 (mod 6) | (1, 0, 2b/3, (2b−6)/3) | ((b−1)/2, (5b−3)/6, (5b−9)/6) |
| b ≡ 5 (mod 12) | (1, 0, (2b+2)/3, (b−11)/6) | ((b−1)/2, (5b−1)/6, (7b−11)/12) |
| b ≡ 11 (mod 12) | (1, 0, (2b+2)/3, (b−11)/6) | ((b−1)/2, (5b−1)/6, (7b−17)/12) |

n(b)'nin her satırı, (5.1)'de n(b) − b³ = c·b + d (0 ≤ c, d < b) yazılarak çıkar; m'nin satırları ikiye bölerek bulunur. b ≡ 5 (mod 12) satırı n(b) için b ≥ 17 ister; b = 5'te n(5) = 144, 5 tabanında (1, 0, 3, 4)'tür. Örneğin n(10) = 1108, 10 tabanında (1, 1, 0, 8)'dir; n(7) = 378 ise 7 tabanında (1, 0, 5, 0)'dır ve m = 189 = (3, 6, 0)'dır. Tek b için m'nin haneleri Bölüm 5.4'teki Adım 6'nınkilerdir: m = (r, r + 1 + k, y). n(b) tam olarak b ≡ 3 (mod 6) ve b ≡ 11 (mod 12) satırlarında tektir. Bunlar, G'nin o adımda sıfırın üstünden atladığı satırların ta kendisidir; yukarıdaki parite kuralını bu açıklar.

### 5.2 Büyüklük

(5.1)'den

```text
b tek:    n(b) = b³ + (2/3)·b² + O(b)
b çift:   n(b) = b³ + b² + O(b)
```

Ok, tabanın küpünün biraz ötesine düşer. Küpün ötesindeki uzaklık b² biriminde ölçülünce tek tabanlarda 2/3'e, çift tabanlarda 1'e yaklaşır.

### 5.3 Teorem 1'in kanıtı

Yöntem Bölüm 4.4'te anlatılmıştır. Her sınıfta kapalı biçimdeki terim sayısı sabittir. Program b³ ≤ n(b) < b⁴ ve ⌊n(b)/2⌋ + 1 < b³ eşitsizliklerini polinom eşitsizlikleri olarak sertifikalar. Böylece S(n)'nin üç terimi, S(m) ve f(m)'nin iki terimi vardır.

| Sınıf | n(b) | Sertifika | Geçerli | Doğrudan denetlenen |
|---|---|---|---|---|
| b = 12t | çift | 9 | b ≥ 12 | yok |
| b = 12t + 1 | çift | 9 | b ≥ 13 | yok |
| b = 12t + 2 | çift | 9 | b ≥ 14 | b = 2 |
| b = 12t + 3 | tek | 7 | b ≥ 3 | yok |
| b = 12t + 4 | çift | 9 | b ≥ 4 | yok |
| b = 12t + 5 | çift | 9 | b ≥ 17 | b = 5 |
| b = 12t + 6 | çift | 9 | b ≥ 6 | yok |
| b = 12t + 7 | çift | 9 | b ≥ 19 | b = 7 |
| b = 12t + 8 | çift | 9 | b ≥ 8 | yok |
| b = 12t + 9 | tek | 7 | b ≥ 9 | yok |
| b = 12t + 10 | çift | 9 | b ≥ 10 | yok |
| b = 12t + 11 | tek | 7 | b ≥ 11 | yok |

Sertifika sütunu, programın sertifikalı polinomlarla değiştirdiği tam kısım (⌊x/q⌋) sayısıdır. Çift n'de program T = 2S(m − 1) + f(m) + 2S(m) yazar: 3 + 2 + 2 + 2 = 9 tam kısım (S(n) üç, öteki terimler ikişer ister). Tek n'de T = 4S(m) + f(m + 1) yazar: 3 + 2 + 2 = 7 tam kısım. S(m) − S(m − 1) = f(m) olduğundan iki biçim de (4.1) ile aynıdır.

On iki sınıfın hepsinde E_b(n(b)) − n(b) sıfır polinomdur. Sınıflarının sertifikalı aralığının altında kalan 2, 5 ve 7 tabanları doğrudan hesapla E_b(n(b)) = n(b) eşitliğini sağlar. On iki sınıf bütün b ≥ 2 tabanlarını kapsar. ∎

Sertifika yalnız tam kısımları ve b'nin kuvvetlerini kullanır. Asallık kullanmaz. Bu yüzden Teorem 1 bileşik tabanlarda da geçerlidir.

### 5.4 Teorem 1 ile 3'ün tek b için kanıtı

b ≥ 3 tek ve r = (b − 1)/2 olsun. κ(h) = carries_b(h, h), h + h toplamındaki elde sayısıdır. h'nin bir d hanesi, gelen c ∈ {0, 1} eldesiyle birlikte tam olarak 2d + c ≥ b olduğunda elde verir. Bu d > r iken her zaman, d < r iken hiçbir zaman, d = r iken yalnız c = 1 ise olur.

**Lemma 1 (tek satırlar).** Tek b ve h ≥ 0 için carries_b(h, h + 1) = κ(h + 1).

*Kanıt.* t(x), x'in b − 1'e eşit sondaki hanelerinin sayısı olsun. x'e bir eklemek bu haneleri 0 yapar ve sonraki haneyi bir artırır. Bu yüzden s_b(x + 1) = s_b(x) + 1 − (b − 1)·t(x)'tir. (3.2)'den

```text
carries_b(h, h + 1) − carries_b(h + 1, h + 1)
    = ( s_b(h) − s_b(h + 1) − s_b(2h + 1) + s_b(2h + 2) ) / (b − 1)
    = t(h) − t(2h + 1).
```

Geriye t(2h + 1) = t(h) olduğunu göstermek kalır. 2h + 1 hane hane hesaplanır. Eklenen 1, 0. konuma gelen elde olarak alınır. h'nin en alttaki t(h) hanesinin her biri b − 1'dir ve 1 elde alır. Sonuç 2(b − 1) + 1 = 2b − 1'dir. Çıkan hane b − 1 olur ve 1 elde ileri gider. h'nin sonraki d hanesi b − 1 değildir ve o da 1 elde alır. Çıkan hane 2d + 1 veya 2d + 1 − b'dir. İlki tektir, b − 1 ise çifttir, dolayısıyla ilki b − 1 olamaz. İkincisi ancak d = b − 1 ise b − 1'e eşittir ve bu durum dışlanmıştır. O hâlde t(2h + 1) = t(h). ∎

Böylece κ_b(2h) = κ(h) ve κ_b(2h + 1) = κ(h + 1) olur. Lemma 1 çift tabanlarda bozulur (Bölüm 6.3).

**Lemma 2.** G(m) = Σ_{h=1..m} (κ(h) − 1) ve G(0) = 0 olsun. O zaman

```text
E_b(2m) − 2m              = 2·G(m)
E_b(2m + 1) − (2m + 1)    = G(m) + G(m + 1)
```

*Kanıt.* Lemma 1'e göre h = 1'den m'ye 2h çift satırları ve 2h − 1 tek satırları ayrı ayrı κ(h) katar. Bu yüzden E_b(2m) = 2(κ(1) + ... + κ(m)). 2m + 1 satırı κ(m + 1) ekler. ∎

Demek ki D_b'nin işareti G'nin işaretinden çıkar.

**Lemma 3 (blok kuralı).** 0 ≤ x < b^J ve 1 ≤ d ≤ b − 1 olmak üzere h = d·b^J + x olsun. O zaman

```text
d < r :   κ(h) = κ(x)
d = r :   x > (b^J − 1)/2 ise κ(h) = κ(x) + 1,   aksi hâlde κ(h) = κ(x)
d > r :   κ(h) = κ(x) + 1
```

*Kanıt.* Alttaki J hane, h + h ve x + x toplamlarında aynı eldeleri verir. Bunlardan tam olarak 2x ≥ b^J olduğunda dışarı elde çıkar. Üst d hanesi bundan sonra yukarıdaki hane kuralına göre elde verir. d'nin üstündeki bütün haneler 0'dır, bu yüzden d'den çıkan bir elde yeni bir elde doğurmaz. ∎

Kanıt G'yi önce m'nin ilk b³ değeri boyunca, sonra ötesinde izler.

**Adım 0. 1 ≤ m ≤ b² − 1 için G(m) < 0, G((b² − 1)/2) = −r² − 2r ve G(b² − 1) = −r.** Tek haneli h için h > r ise κ(h) = 1, değilse 0'dır. Bu yüzden G, h = 1'den r'ye birer iner, b − 1'e kadar düz kalır ve G(b − 1) = −r olur. x = 0 dahil, b değerlik tam bir blokta κ(x) − 1 toplamı −(r + 1)'dir. İki haneli h = d·b + x için Lemma 3 (J = 1) üç durum verir. d < r blokları bu deseni yineler ve her biri G'yi r + 1 düşürür. d = r bloğunda κ(h) − 1, x ≤ r için −1, x > r için +1'dir. d > r bloklarında κ(h) − 1 = κ(x) ≥ 0'dır ve her biri G'yi r artırır. d = r bloğunun ortasına kadar G hiç yükselmez. Orta nokta h = r·b + r = (b² − 1)/2'dir ve orada

```text
G((b² − 1)/2) = −r − (r − 1)(r + 1) − (r + 1) = −r² − 2r.
```

Sonrasında G hiç inmez ve G(b² − 1) = −r² − r + r·r = −r < 0 değerinde biter. Yani G bütün aralıkta eksidir. 0'dan b² − 1'e bütün x'ler üzerinden κ(x) − 1 toplamı G(b² − 1) − 1 = −(r + 1)'dir.

**Adım 1. 1 ≤ m ≤ (b³ − 1)/2 için G(m) < 0 ve G'nin 1 ≤ m ≤ b³ − 1 üzerindeki en küçük değeri μ = G((b³ − 1)/2) = −2r² − 3r'dir.** Üç haneli h = d·b² + x alınır. B_d = G(d·b² − 1), d bloğundan önceki değer olsun. B_1 = −r'dir ve d < r olan her blok G'yi r + 1 düşürür. Bu yüzden B_d = −r − (d − 1)(r + 1). Böyle bir blokta G(d·b² + x) = B_d − 1 + G(x)'tir. Adım 0'a göre bu değer eksidir ve en az B_{r−1} − 1 − r² − 2r = −2r² − 2r + 1 > μ'dür. d = r bloğunun alt yarısında (x ≤ (b² − 1)/2) Lemma 3 yine κ(h) = κ(x) verir. Bu yüzden G = B_r − 1 + G(x) = −r² − r + G(x) olur ve en küçük değeri x = (b² − 1)/2'dedir. r·b² + (b² − 1)/2 = (b³ − 1)/2 olduğundan

```text
μ = G((b³ − 1)/2) = −r² − r − r² − 2r = −2r² − 3r.
```

Adım 2 ile 4, G'nin b³ − 1'e kadar kalan m'lerde μ'nün üstünde kaldığını gösterir.

**Adım 2. (b³ − 1)/2 ≤ m < (r + 1)·b² − 1 aralığında G her adımda en az 1 artar.** d = r bloğunun üst yarısında x > (b² − 1)/2'dir. Bu yüzden x + x en üst hanesinden dışarı elde verir, κ(x) ≥ 1 olur ve Lemma 3, κ(h) = κ(x) + 1 ≥ 2 verir.

**Adım 3. G((r + 1)·b² − 1) = r² > 0.** d = r bloğu B_r = −r² − r + 1 değerine −(r + 1) + (b² − 1)/2 ekler. (b² − 1)/2 = 2r² + 2r ile toplam r²'dir.

**Adım 4. (r + 1)·b² − 1 ≤ m ≤ b³ − 1 aralığında G hiç inmez ve G(b³ − 1) = r·(b² − 1).** d > r için κ(h) − 1 = κ(x) ≥ 0'dır. r bloğun her biri b² − (r + 1) ekler ve r² + r(b² − r − 1) = r(b² − 1)'dir.

**Adım 5. m ≥ b³ için G(m) ≥ 4r³ + 2r² − 3r − 1 ≥ 2.** b^J ≤ m < b^(J+1) olacak biçimde J ≥ 3 alınır ve y < b^J ile m = d·b^J + y yazılır. Lemma 3'e göre her d' üst hanesi için κ(d'·b^J + x) ≥ κ(x)'tir. Bu yüzden b^J uzunluğundaki her tam blok en az G(b^J − 1) − 1 ekler. Son yarım blok en az G(y) − 1 ekler. Buradan

```text
G(m) ≥ G(b^J − 1) + (d − 1)·(G(b^J − 1) − 1) + G(y) − 1.
```

J üzerinden tümevarım uygulanır. Varsayım, G(b^J − 1) ≥ r(b² − 1) ve 1 ≤ y < b^J için G(y) ≥ μ olmasıdır. J = 3 için bu Adım 1 ile 4'tür. Eşitsizlik bu durumda G(m) ≥ r(b² − 1) + μ − 1 = 4r³ + 2r² − 3r − 1 > μ verir. Bu değer r = 1 için 2'dir ve r ile artar. Ayrıca G(b^(J+1) − 1) ≥ b·G(b^J − 1) − (b − 1) ≥ r(b² − 1) olur. Yani varsayım J + 1 için de geçerlidir. ∎

**Adım 6 (varlık ve yer). D_b'nin bir sıfırı vardır ve bu sıfır (5.1)'deki n(b)'dir.** d = r bloğunun üst yarısında iki haneli kısmı x = (r + 1 + k)·b + y biçiminde yazalım (0 ≤ k ≤ r − 1, 0 ≤ y ≤ 2r). J = 2 ile Lemma 3'ten G(r·b² + x) = B_r − 1 + G(x) + (x − (b² − 1)/2) çıkar. Adım 0'a göre G((r + 1)·b − 1) = −r² − r'dir ve d > r olan her iki haneli blok r ekler. Bu yüzden G(x) = −r² − r + k·r + max(0, y − r)'dir ve

```text
G(r·b² + x) = −2r² − r + 1 + k·(3r + 1) + φ(y),    φ(y) = y + max(0, y − r).
```

x = r·b + y ve y > r için aynı hesap G ≤ −2r² − r < 0 verir. Demek ki G, k·(3r + 1) + φ(y) = 2r² + r − 1 eşitliğini sağlayan k ve y'de işaret değiştirir. Bir blok içinde φ, y ≤ r iken birer, y > r iken ikişer artar; bir bloktan ötekine G bir artar. r = 3s + t ve t ∈ {0, 1, 2} ile:

| r | k | y | D_b'nin sıfırı |
|---|---|---|---|
| 3s (b ≡ 1 mod 6) | 2s | s − 1 | G(m₀) = 0, n = 2m₀ |
| 3s + 1 (b ≡ 3 mod 6) | 2s | 5s + 1 | G(m₁) = −1, G(m₁ + 1) = 1, n = 2m₁ + 1 |
| 3s + 2, s çift (b ≡ 5 mod 12) | 2s + 1 | (7s + 4)/2 | G(m₀) = 0, n = 2m₀ |
| 3s + 2, s tek (b ≡ 11 mod 12) | 2s + 1 | (7s + 3)/2 | G(m₁) = −1, G(m₁ + 1) = 1, n = 2m₁ + 1 |

Burada m = r·b² + (r + 1 + k)·b + y'dir. Her satırda n, (5.1)'e eşittir. Örneğin b = 6s + 1 için 2m₀ = 6s·b² + (10s + 2)·b + 2s − 2 = b³ + (2b² + 2b − 7)/3'tür. İkinci ve dördüncü satırlarda φ gereken değeri 2'lik bir adımla geçer. Bu yüzden G, −1'den 1'e geçer ve Lemma 2'ye göre D_b(2m₁ + 1) = G(m₁) + G(m₁ + 1) = 0 olur. Yani tek b için sıfır vardır ve n(b)'dedir; bilgisayar adımına gerek yoktur. Bu adımın her değerini 3'ten 401'e kadar her tek b için sayısal olarak da denetledim (`tests/check_odd_existence.py`).

**Örnek.** İki tür sıfırı üç taban gösterir.

| b | r, s, t | k, y | m | m çevresinde G (sayıldı) | D_b'nin sıfırı |
|---|---|---|---|---|---|
| 7 | 3, 1, 0 | 2, 0 | m₀ = 3·49 + 6·7 + 0 = 189 | G(188) = −1, G(189) = 0, G(190) = 1 | n = 2·189 = 378 = n(7) |
| 3 | 1, 0, 1 | 0, 1 | m₁ = 1·9 + 2·3 + 1 = 16 | G(16) = −1, G(17) = 1 | n = 2·16 + 1 = 33 = n(3) |
| 11 | 5, 1, 2 | 3, 5 | m₁ = 5·121 + 9·11 + 5 = 709 | G(709) = −1, G(710) = 1 | n = 2·709 + 1 = 1419 = n(11) |

b = 7 için formül G(189) = −2·9 − 3 + 1 + 2·10 + φ(0) = 0 verir. G sıfırı tam vurur ve ok çift bir satıra düşer. b = 3 ve b = 11'de G sıfırın üstünden −1'den 1'e atlar ve ok iki değerin arasındaki tek satıra düşer; orada D_b = G(m₁) + G(m₁ + 1) = 0'dır.

**Sonuç.** G, 1 ≤ m ≤ (b³ − 1)/2 için eksidir. Oradan (r + 1)·b² − 1'deki r² artı değerine kadar kesin artar ve o noktadan sonra hep artıdır. Kesin artan bir dizi sıfır değerini en çok bir kez alır ve işaretini yalnız bir kez değiştirir. G(m₀) = 0 ise n = 2m₀, D_b'nin bir sıfırıdır. Bu durumda D_b(2m₀ − 1) = G(m₀ − 1) < 0 ve D_b(2m₀ + 1) = G(m₀ + 1) > 0'dır. G sıfır olmadan işaret değiştiriyorsa, yani G(m₁) < 0 < G(m₁ + 1) ise, sıfır olabilecek tek yer n = 2m₁ + 1'dir. Öteki her n'de Lemma 2'deki iki terim aynı işaretlidir. Demek ki D_b'nin en çok bir sıfırı vardır, D_b ondan önce eksi, sonra artıdır ve Adım 6'ya göre bu sıfır vardır ve n(b)'dir. Bu, Teorem 1 ile 2'yi tek b için bilgisayar adımı olmadan kanıtlar.

Teorem 3 için, D_b(2m) = 2G(m) ve D_b(2m + 1) = G(m) + G(m + 1) değerlerinin ikisi de en az 2μ'dür. Eşitlik, tek b için çift olan 2m = b³ − 1'de sağlanır. Bu yüzden D_b'nin en küçük değeri 2μ = −(4r² + 6r) = −(b − 1)(b + 2)'dir. ∎

### 5.5 Teorem 2'nin b = 2 için kanıtı

s(j), j'nin ikili yazımındaki 1'lerin sayısı olsun. (3.2)'ye göre carries_2(j, j) = s(j) ve carries_2(y, y + 1) = s(y + 1) − 1'dir. H(m) = Σ_{j=1..m} (2s(j) − 3) olsun. O zaman

```text
E_2(2m) − 2m              = H(m)
E_2(2m + 1) − (2m + 1)    = H(m) + s(m + 1) − 2
```

İlk değerler H(1), ..., H(7) = −1, −2, −1, −2, −1, 0, 3'tür. Yani n = 12 bir sıfırdır ve tek konumlardaki D_2(1), D_2(3), ..., D_2(11) değerleri −1, −2, −2, −2, −2, −1'dir. J ≥ 3 ve 0 ≤ x < 2^J ile j = 2^J + x için 2s(j) − 3 = 2s(x) − 1'dir. Bu değer x = 0'da −1, x ≥ 1'de en az 1'dir. Tam bir blok boyunca H, 2^J(J − 1) artar. Bu yüzden H(2^J − 1) ≥ H(7) = 3'tür ve blok içinde H en az H(2^J − 1) − 1 ≥ 2 kalır. O hâlde m ≥ 7 için H(m) ≥ 2 ve m ≥ 6 için D_2(2m + 1) ≥ 1'dir. Tek sıfır n = 12'dir. ∎

### 5.6 İlgili çalışmalar

Şunlar bilinir ve burada kullanılır. Bir asalın binom katsayısındaki üssü bir elde sayısına eşittir (Kummer, 1852 [1]). Bir asalın m!'deki üssü f(m)'dir (Legendre [2]). (3.1) ve (3.2) eşitlikleri standarttır.

Standart gösterimle c(2h − 1) = C(2h, h)/2'dir. Bu yüzden A(m) = C(2,1)·C(4,2)···C(2m,m) ile c(1)···c(2m) = A(m)²/2^m olur (OEIS A007685 [3]). Tek asal p için buradan E_p(2m) = 2·v_p(A(m)) çıkar ve n = 2m çift çözümü v_p(A(m)) = m demektir. Örnekler p = 5 için m = 72, p = 7 için m = 189 ve p = 13 için m = 1158'dir.

p = 2 için (3.2), s_2(2j) = s_2(j) ve s_2(2j + 1) = s_2(j) + 1 ile birlikte κ_2(k) = s_2(k + 1) − 1 verir; bu, C(k, ⌊k/2⌋)'de 2'nin üssüdür (OEIS A048881 [3]). k = 1, …, n üzerinden toplayıp s_2(1) = 1 kullanınca her n ≥ 1 için E_2(n) = A000788(n + 1) − (n + 1) = A078903(n + 1) çıkar; burada A000788(N) = s_2(0) + … + s_2(N)'dir [3]. Aynı kayıtlardan 2 tabanı için yakın bir sonuç daha çıkar. A000788(4^k − 2) = k(4^k − 2) formülü n = 4^(m+1) − 3'te E_2(n) = m(n + 1) verir. A078904 de o noktadan önceki en büyük farkı verir. m = 1 için bu E_2(13) = 14'tür, n(2) = 12'den bir satır sonra.

(3.2)'ye göre E_b(n) birikimli hane toplamlarının bir birleşimi olduğundan Delange'ın formülü [11] (b = 2 için daha önce Trollope [12]) sabit b için E_b(n) = (n/2)·log_b n + O(n) verir. n = b³ civarında O(n) terimi salınır ve ana terimle aynı büyüklüktedir. Bu yüzden bu kestirim kesişmenin yerini vermez; yeri (5.1) formülü verir.

22 Kasım 2026'da OEIS'te (terimle ve sözcükle), arXiv'de (başlık ve özet), zbMATH Open'da, Crossref'te ve genel bir web arama motorunda aradım; burada andığım çalışmalara baktım. E_b(n) = n denklemini, (5.1) formülünü, Teorem 1 ile 4'ü, Bölüm 5.7'deki en uzak asal kuvvet çarpanı kuralını, −(b − 1)(b + 2) derinliğini ve 12, 33, 82, 144, 256, … ile 12, 33, 144, 378, 1419, … dizilerini bu kaynaklarda bulamadım. Görmediğim çalışmalarda yer alıyor olabilirler. Böyle bir çalışma bildirilirse sonraki sürümde eklerim.

Bulduğum en yakın çalışma, bir satırdaki bütün binom katsayılarının çarpımını ele alıyor (OEIS A001142 [3]). Lagarias ve Mehta [4] bu çarpımın asal üslerini birikimli hane toplamlarıyla yazıyor ve aynı hane toplamı ifadesini her b ≥ 2 tabanı için tanımlıyor; bileşik b'de bu ifadenin her zaman b'nin üssü olmadığını da belirtiyor. Du ve Lagarias [13] aynı çarpımın kısmi çarpanlara ayrılışını inceliyor. Straub, Moll ve Amdeberhan [5] tek tek merkez ve k-merkez binom katsayılarını ele alıyor. Hirschhorn [14] ve Kellner [15] böyle çarpımların büyüklüğünü inceliyor, asal üslerini değil. Eldeleri rastgele bir süreç olarak inceleyen çalışmalar (Holte [16]; Diaconis ve Fulman [17]) başka bir soru soruyor.

### 5.7 Bileşik m

Bileşik bir m için doğal soru bir elde sayısını değil m'nin üssünü kullanır. q₁ < ... < q_k asallarıyla m = q₁^a₁ ··· q_k^a_k yazılır. c(1)···c(n) çarpımında m'nin üssü, yani çarpımı bölen en büyük m^e kuvvetinin e üssü,

```text
K_m(n) = min_i ⌊ E_{q_i}(n) / a_i ⌋
```

olur. m asalsa K_m = E_m'dir. m bileşikse K_m ile E_m farklı fonksiyonlardır (Bölüm 6.3).

**Teorem 4 (karesiz m)** (GEÇERLİ, kanıt). m karesiz ve en büyük asal çarpanı q_k olsun. O zaman K_m(n) = n denkleminin yalnız bir çözümü vardır: n = n(q_k).

*Kanıt.* Teorem 2'ye göre her q asalı için E_q(n) − n, n(q)'dan önce eksi, sonra artıdır. n(q) noktaları q ile artar, çünkü (5.1)'e göre her b ≥ 2 için b³ < n(b) < (b + 1)³'tür. n < n(q_k) ise E_{q_k}(n) < n olur, dolayısıyla K_m(n) < n'dir. n > n(q_k) ise her i için n > n(q_i)'dir ve bütün E_{q_i}(n) > n olur, dolayısıyla K_m(n) > n'dir. n = n(q_k)'da E_{q_k}(n) = n'dir ve öteki terimler n'den büyüktür. ∎

Genel m için yalnız ölçüm vardır. Her q^a asal kuvveti çarpanının kendi çözüm kümesi vardır. İlk çözümü q^(2a+1) civarındadır, q = 2 ise 2^(2a+2) civarındadır (Şekil 5). Ölçülen 2 ≤ m ≤ 1000 aralığında iki veya daha çok farklı asal çarpanı olan 806 sayı vardır. Bunların 803'ünde m'nin çözüm kümesi, ilk çözümü en uzağa düşen asal kuvveti çarpanının çözüm kümesine eşittir. İstisnalar 72 = 2³·3², 360 = 2³·3²·5 ve 544 = 2⁵·17'dir. Üçünde de m'nin çözüm kümesi, en uzak çarpanın kümesine başka bir çarpanın sonraki bazı çözümlerinin eklenmesiyle oluşur. En uzak çarpanın hiçbir çözümü eksik değildir. 72 ve 360'ta en uzak çarpan 9'dur ve ilk çözümü 321'dir. 8 çarpanı 323 ve 324'ü ekler. 544'te en uzak çarpan 17'nin tek çözümü 5118 = n(17)'dir. 32 çarpanı 5120, 5121 ve sonraki çözümleri ekler, toplam 13 çözüm olur (Bölüm 7).

a ≥ 2 olan 25 asal kuvveti q^a ≤ 1000 arasında yalnız sekizinin tek çözümü vardır. Bunlar 7 ≤ q ≤ 31 için q² asal kareleridir: 49'dan (çözüm 18 710) 961'e (çözüm 29 266 018) kadar. 25 = 5² karesinin iki çözümü vardır: 3668 ve 3669. Her m için, ilk çözümü en uzağa düşen q^a çarpanına göre 3q^(2a+1) + 1000'e kadar (q = 2 ise 3·2^(2a+2) + 1000'e kadar) her n sayıldı. Asal kare q² için bu sınır 3q⁵ + 1000'dir. Tek çözüm, bu aralıkta tek çözüm demektir.

## 6. Sayısal örnekler

### 6.1 Küçük örnek: taban 7

Şekil 1, 1'den 720'ye her n için D_7(n)'yi gösterir. Fark küçük salınımlarla yavaşça iner, n = 342 = 7³ − 1'de −54'e varır ve sonra dik biçimde yükselir. n = 343'ten başlayarak üç eldeli ve iki eldeli satırlar bloklar hâlinde sırayla gelir: 343'ten 348'e üç, 349'dan 356'ya iki, 357'den 362'ye üç, 363'ten 370'e iki, 371'den 376'ya üç, 377'den 384'e iki. Üç eldeli bir satır D_7'yi iki, iki eldeli bir satır bir artırır. Kesişmenin çevresi:

```text
n        372   373   374   375   376   377   378   379   380   381
D_7(n)   −10    −8    −6    −4    −2    −1     0     1     2     3
```

Kesişme, (5.1)'in verdiği gibi n(7) = 7³ + (2·49 + 14 − 7)/3 = 343 + 35 = 378'dir. Derinlik, Teorem 3'ün verdiği gibi −(7 − 1)(7 + 2) = −54'tür.

![Şekil 1. 1'den 720'ye her n için D_7(n) = E_7(n) − n. En küçük değer n = 342 = 7³ − 1'de −54'tür. Tek sıfır n(7) = 378'dedir.](../figures/fig1_bow_base7_tr.png)

### 6.2 Sınır durumları

Kesişmenin hemen öncesindeki ve sonrasındaki değerler ±1 veya ±2'dir. 2 ≤ b ≤ 16 için sayılan değerler:

```text
b               2    3    4    5    6    7    8    9
D_b(n(b) − 1)  −1   −2   −1   −1   −1   −1   −1   −2
D_b(n(b) + 1)   1    2    1    2    1    1    1    2

b              10   11   12   13   14   15   16
D_b(n(b) − 1)  −1   −2   −1   −1   −1   −2   −1
D_b(n(b) + 1)   1    2    1    1    1    2    1
```

D_b(n) − D_b(n − 1) = κ_b(n) − 1 olduğundan, n(b)'nin yanındaki 2'lik bir adım orada üç eldeli bir satır demektir. Bu, n(b) tek de çift de olsa görülür, örneğin b = 5'te n(5) = 144.

En küçük tabanlar formüllerin sınır durumlarıdır. (5.1) sınıf formülü b = 2 ve b = 3'ü kapsar: 8 + 4 + 2 − 2 = 12 ve 27 + (18 + 6 − 6)/3 = 33. (5.2) asal biçimi p ≥ 5 gerektirir (Bölüm 6.3).

### 6.3 Geçersiz ve bozulan durumlar

1. **Asal biçim p = 3'te.** ε = 0 ile (5.2), tam sayı olmayan 27 + 28/6 değerini verir. (5.2) biçimi yalnız p ≥ 5 için geçerlidir. Sınıf formülü n(3) = 33 verir.
2. **Lemma 1 çift tabanda.** 4 tabanında h = 1 için carries_4(1, 2) = 0, fakat carries_4(2, 2) = 1'dir. h < 4000 için eşitlik 4 tabanında 1334, 6 tabanında 801, 10 tabanında 444 kez bozulur. Bölüm 5.4'teki kanıtın b ≥ 4 çift tabanlara uygulanamamasının nedeni budur.
3. **Bileşik m için çözüm tek değildir.** m = 4 için K_4(n) = n denkleminin 12 çözümü vardır. İlkleri 60, 65, 66, 67 ve 68'dir. Teklik asallardan asal kuvvetlerine geçmez.
4. **Bileşik tabanda elde sayısı ile üs farklıdır.** b = 6 için E_6(256) = 256'dır, yani (5.1)'in dediği gibi n(6) = 256'dır. Fakat c(1)···c(256) çarpımında 6'nın üssü K_6(256) = min(770, 424) = 424'tür. K_6(n) = n denkleminin tek çözümü, Teorem 4'ün dediği gibi n = 33 = n(3)'tür.

### 6.4 Büyük örnekler

**39 basamaklı bir asal.** p = 2¹²⁷ − 1 alınsın. p ≡ 1 (mod 3)'tür ve n(p) 115 ondalık basamaklıdır. 49252507745493099015 ile başlar ve 71468138216236078418 ile biter. Aşağıdaki üç nokta gösterilmeyen 75 basamağın yerini tutar.

```text
n(p) = 49252507745493099015 ... 71468138216236078418          (115 basamak)
```

Kapalı biçim tam sayı aritmetiğiyle E_p(n(p)) = n(p), D_p(n(p) − 1) = −1, D_p(n(p) + 1) = 1 ve D_p(p³ − 1) = −(p − 1)(p + 2) verir.

**Bilinen en büyük Mersenne asalı.** p = 2^136279841 − 1 alınsın. p 41 024 320 basamaklıdır. Basamak sayısı ⌊136279841·log₁₀2⌋ + 1'dir, çünkü 2'nin 1'den büyük bir kuvveti 10'un kuvveti olamaz. n(p) 123 072 960 basamaklıdır. Bu, 3·136279841·log₁₀2 = 123 072 959,836 eşitliğinden ve n(p) = 2^(3e)·(1 + O(2^(−e))) olmasından çıkar. Göreli düzeltme basamak sayısını değiştiremeyecek kadar küçüktür. Baştaki 685415845289511071 haneleri aynı logaritmadan 60 basamak duyarlıkla hesaplanmıştır. Saklanmış bir değerden okunmamıştır. n(p)'nin kendisi hiç yazdırılmadı. Tam bir GMP tam sayısı olarak hesaplandı. E_p kapalı biçimle n(p)'de, n(p) ± 1'de, p³ − 1'de ve dört rastgele noktada hesaplandı. Bütün denetimler 445,6 s sürede geçti (Bölüm 7).

### 6.5 Okların düştüğü yerler

(5.1) formülü her tabanın düştüğü yeri belirler. Her maddenin durumu başlığında yazılıdır.

1. **Küpün ötesi (GEÇERLİ, kanıt).** (n(b) − b³)/b², tek b için 2/3'e, çift b için 1'e yaklaşır (Şekil 3). b = 10 001 için değer 0,66675, b = 10 002 için 1,00010'dur.
2. **Ardışık asalların okları arasındaki uzaklık (GEÇERLİ, kanıt; oran aralığı ÖLÇÜLDÜ).** 5 ≤ p < q asalları için (5.2), α_p = (3 + ε)/6 ve β_p = (3ε − 17)/6 ile n(p) = p³ + (2/3)p² + α_p·p + β_p biçiminde yazılır. O zaman

   ```text
   n(q) − n(p) = (q³ − p³) + (2/3)(q² − p²) + (α_q·q − α_p·p) + (β_q − β_p).
   ```

   Yani uzaklık 3p²·(q − p)'ye yakındır. Şekil 4, (n(q) − n(p))/3p² değerinin q − p asal boşluğunu izlediğini gösterir. Bu, n(p) ≈ p³ olmasının sonucudur ve boşluğun kendisinden fazla bilgi taşımaz. 20 000'den küçük 2259 ardışık asal çiftinde n(q) − n(p)'nin q³ − p³ + (2/3)(q² − p²)'ye oranı 0,99889 ile 1,00483 arasındadır.
3. **Parite (GEÇERLİ, kanıt).** n(b) tam olarak b ≡ 3, 9, 11 (mod 12) için tektir. p ≥ 5 asalları arasında bunlar p ≡ 11 (mod 12) asallarıdır.
4. **En dipten oka uzaklık (tek b için GEÇERLİ, kanıt; çift b için ÖLÇÜLDÜ).** Tek b için uzaklık n(b) − (b³ − 1) = (2/3)b² + O(b)'dir. Örneğin b = 7 için 36, b = 31 için 660, b = 101 için 6884'tür. Çift b için en dibe, ölçüldüğü gibi ilk kez b³ − b² − 1'de varılıyorsa uzaklık tam olarak 2b² + b − 1'dir.
5. **Her parite için tek bir biçim (ÖLÇÜLDÜ).** D_b, b²'ye bölünür ve n, b² biriminde b³ kadar kaydırılır. O zaman büyük tek tabanların eğrileri tek bir kırık çizgiye, büyük çift tabanlarınki başka bir kırık çizgiye yaklaşır (Şekil 2). Sonlu b'de eğriler onlara yakındır ama eşit değildir: gerçek sıfırlar b = 101'de x = 0,6747, b = 301'de 0,6689, b = 100'de 1,0098, b = 300'de 1,0033'tedir. Tek tabanlarda en küçük değer x = (n − b³)/b² = 0'da −1'dir. Çizgi 3/2 eğimle x = 1'de 1/2'ye çıkar, x = 2/3'te sıfırı keser ve sonra 1/2 eğimle yükselir. Çift tabanlarda en küçük değer x = −1'de −1'dir. Çizgi 1/2 eğimle yükselip x = 1'de sıfırı keser ve sonra 3/2 eğimle yükselir. b = 1001 için x = 0, 2/3, 1 ve 2'deki ölçekli değerler −1,001, −0,001, 0,499 ve 0,998'dir. b = 1000 için x = −1, 1 ve 2'deki değerler −1,000, −0,001 ve 1,4985'tir.
6. **Tabanlar boyunca üçüncü farklar (ÖLÇÜLDÜ).** Ardışık b'ler üzerinde n(b) dizisi tek bir polinom değildir. Üçüncü farkları n(b + 3) − 3n(b + 2) + 3n(b + 1) − n(b), işaret değiştirerek büyür (b = 2, 3, 4, 5, ... için −15, 37, −40, 72, ...). Düzen, n(b)'nin bir polinom olduğu her sınıfın içindedir.

![Şekil 2. Tek b = 101 (mavi çizgi) ve 301 (mavi bant), çift b = 100 (turuncu kesikli) ve 300 (turuncu bant) için (E_b(n) − n)/b² ölçekli farkı, (n − b³)/b²'ye karşı. Her paritenin eğrileri neredeyse üst üste düşer. Sıfırları b büyüdükçe tek tabanlarda 2/3'e, çift tabanlarda 1'e yaklaşır.](../figures/fig2_scaled_shape_tr.png)

![Şekil 3. 5 ≤ b ≤ 400 için okun küpün ötesindeki uzaklığı (n(b) − b³)/b², sınıfa göre, logaritmik b ekseninde. Noktalı çizgiler 2/3 ve 1'dedir.](../figures/fig3_offset_by_class_tr.png)

![Şekil 4. Sol: 5'ten başlayan ilk 400 ardışık asal çifti için q − p asal boşluğu, (n(q) − n(p))/3p²'ye karşı. Sağ: 20 000'den küçük bütün ardışık asallar için n(q) − n(p)'nin q³ − p³ + (2/3)(q² − p²)'ye oranı.](../figures/fig4_prime_arrows_tr.png)

![Şekil 5. Asal kuvvetlerinde K_{q^a}(n) = n denkleminin ilk çözümü, log_q olarak. Çizgiler 2a + 1 ve 2a + 2'dir. Her n ilk çözüme kadar sayılmıştır. q ≥ 3 noktaları örtüşmesin diye yatayda biraz kaydırıldı.](../figures/fig5_prime_powers_tr.png)

## 7. Uygulama ve doğrulama

Bütün programlar bu paketin içindedir. Python programları Python 3.8 veya sonrasını ister ve üçüncü taraf paket gerektirmez. İstisnalar `tests/check_mersenne.py` (gmpy2) ve `tests/make_figures.py`'dir (numpy ve matplotlib). C programları OpenMP destekli bir C derleyicisi ister. Ekran kartı programı 64 bit gölgelendirici tam sayılarıyla Vulkan 1.2 ve `glslc` derleyicisini ister. Bütün komutlar paket kökünden çalışır. Ham çıktılar `tests/RESULTS.md` dosyasındadır. Programların çıktısı İngilizcedir.

| Program ve komut | Yöntem | Kapsam | Sonuç |
|---|---|---|---|
| `python3 tests/check_small.py 41` | doğrudan sayım, kapalı biçimle karşılaştırma | 2 ≤ b ≤ 40, her n ≤ 3b³ + 300 | 39 taban, 0 başarısızlık, PASS |
| `python3 tests/check_certificates.py` | polinom sertifikaları | b'nin 12'ye göre 12 sınıfı | 12 sınıfın 12'si PASS |
| `python3 tests/check_proof_steps.py 151` | Bölüm 5.4'ün her lemması ve adımı | tek 3 ≤ b ≤ 149, asal ve bileşik | 74 tek taban, 0 başarısızlık, PASS |
| `python3 tests/check_odd_existence.py 401` | Bölüm 5.4'ün Adım 6'sı: varlık ve yer | tek 3 ≤ b ≤ 401 | 200 tek taban, 0 hata, PASS |
| `./bow_draw_scan 600` (`tests/c/bow_draw_scan.c`) | doğrudan sayım, bütün tabanlar | 2 ≤ b < 600, her n ≤ 3b³ + 300 | 598/598 PASS, 9,69 × 10¹⁰ satır, 127 s |
| `./bow_draw_scan 1000 primes` | doğrudan sayım, asallar | p < 1000 | 168/168 PASS, 1,10 × 10¹¹ satır, 144 s |
| `./tests/gpu/bow_draw_gpu 2000` | ekran kartında blok taraması | 2 ≤ b < 2000, her n ≤ 3b³ + 300 | 1998/1998 PASS, 1,20 × 10¹³ satır, 1603 s (kartta 747 s) |
| `python3 tests/check_primes.py 10000000000 12000` | kapalı biçim | bütün 5 ≤ p < 10¹⁰ asalları ve 20 ile 200 basamaklı 12 000 rastgele asal | 455 052 509 asal ve 12 000 rastgele asal, 0 başarısızlık, PASS, 449 s |
| `python3 tests/check_mersenne.py 136279841 132049 2` | GMP ile kapalı biçim | 3 ≤ e ≤ 136 279 841 için 51 Mersenne asalı 2^e − 1 | 51/51 PASS, 3 ≤ e ≤ 132 049 aralığındaki 29 üs Lucas-Lehmer ile doğrulandı (programın saydığı 30, e = 2'yi de içerir), 2646 s, 1,04 GB |
| `python3 tests/check_composite.py` | K_m'nin doğrudan sayımı | 2 ≤ m ≤ 40 | asal ve karesiz m PASS, en uzak çarpan kuralı 7/7 |
| `./bow_draw_composite 1000` (`tests/c/bow_draw_composite.c`) | K_m'nin doğrudan sayımı | 2 ≤ m ≤ 1000 | asallar 168/168 ve karesizler 439/439 PASS, en uzak çarpan kuralı 806'da 803, 262 s |

Her denetim, mümkün olan her yerde iki bağımsız hesabı karşılaştırır. Doğrudan sayım kapalı biçimle karşılaştırılır. İşlemci sayımı ekran kartı sayımıyla karşılaştırılır. Sertifika polinomları her sınıfta 300 sayısal değerle karşılaştırılır. Mersenne denetiminde e ≤ 132 049 üslerinin asallığı program içinde Lucas-Lehmer testiyle [6] doğrulanır. Daha büyük üsler bilinen Mersenne asalları listesinden alınır [7].

Doğrudan sayımlar hiçbir formüle bağlı değildir. Kapalı biçim denetimleri E_p'yi yalnız n(p) ve n(p) ± 1 noktalarında, p³ − 1'de ve rastgele noktalarda hesaplar. Büyük asallarda başka bir sıfır olmadığının güvencesi sayımlardan değil Teorem 2'den gelir.

## 8. Sınırlar ve açık sorular

1. **Çift tabanlar.** b ≥ 4 çift tabanlarda çözümün tekliğini ve en küçük değerin yerini kanıtlayamadım; ölçtüm. Lemma 1 çift tabanlarda bozulduğu için tek taban kanıtı aktarılamaz. Çift tabanlar için bir kanıt açık bir sorudur.
2. **Bilgisayar destekli adım.** b ≥ 4 çift tabanlarda Teorem 1, `tests/check_certificates.py` tarafından tam rasyonel aritmetikle denetlenen polinom sertifikalarına dayanır. Program kısadır ve bir saniyeden kısa sürede çalışır. Yine de okurun programa güvenmesi veya onu yeniden yazması gerekir. Tek b ve b = 2 için Bölüm 5.4 ve 5.5'teki yazılı kanıtlar ona gerek duymaz.
3. **Bağımsız okuma.** Bölüm 5.4 ve 5.5'teki yazılı kanıtları henüz bağımsız bir okura denetletmedim. İçlerindeki her ara değeri ve tekdüzelik iddiasını Bölüm 7'de listelenen tek tabanlarda sayısal olarak denetledim.
4. **Asallık testi değildir.** Teorem 1 her tabanda geçerli olduğu için E_b(n(b)) = n(b) eşitliği asalları bileşiklerden ayıramaz. Kummer'in üs yorumu yalnız asal tabanlarda geçerlidir.
5. **Çarpanlara ayırma yöntemi değildir.** Teorem 4 ve bileşik m ölçümleri m'nin çarpanlarını kullanır. Hız iddiam yok.
6. **Bileşik m.** En uzak asal kuvveti çarpanı kuralı, ölçülen aralıkta 72, 360 ve 544 olmak üzere üç istisnası olan bir gözlemdir. İstisnaları da kapsayan bir ifade ve asal kuvvetlerinin q^(2a+1) civarındaki düşme yerindeki sabit açık sorulardır.
7. **Program sınırları.** C ve ekran kartı programları 64 bit tam sayı kullanır, bu yüzden n < 2⁶³ ve E_b(n) < 2⁶³ gerektirir. Yalnız ilk koşul yetmez: b = 1 400 000'de taramanın sonu 3b³ + 300, 2⁶³'ten küçüktür ama oradaki E_b değeri değildir. b < 2000 için ikisi de 4·10¹⁰'un altında kalır. Doğrudan sayım taban başına yaklaşık 3b³ log_b(3b³) hane işlemi tutar. Kapalı biçimin sabit bir sınırı yoktur, fakat maliyeti p³'ün büyüklüğüyle artar.
8. **Literatür.** Bölüm 5.6, aranan veri tabanlarını, aramanın tarihini ve bulunanları listeler. Bu kaynaklarda olmayan bir sonuç yine de biliniyor olabilir.
9. **Programlar.** Programlar ve ham çıktıları (tests/RESULTS.md) bu makaleye eşlik eden paketin içindedir. Süreler ve ekran kartı sonuçları orada kayıtlıdır.

## 9. Sonuç

Her b ≥ 2 tabanında, merkez binom katsayılarının 1'den n'ye kadar satırlardaki eldeleri, b³'ün hemen ötesinde (5.1)'in verdiği n(b) noktasında satır sayısına yetişir. Tek tabanlarda ve 2 tabanında ikisinin eşit olduğu tek nokta budur, fark işaretini yalnız orada değiştirir ve bunların hepsi elle kanıtlıdır. b ≥ 4 çift tabanlarda teklik ölçülmüştür, kanıtlanmamıştır. Asal p için E_p(n), merkez binom katsayılarının çarpımında p'nin üssüdür. Karesiz bir m için Teorem 4, K_m(n) = n denkleminin tek çözümünü en büyük asal çarpanın noktasına yerleştirir. Düşme yerleri basit kurallara uyar. b'nin 6'ya göre kalanına bağlıdırlar ve küpün yaklaşık (2/3)b² veya b² ötesindedirler. p < q ardışık asallarının okları arasında yaklaşık 3p²(q − p) uzaklık vardır.

## Ek A. Denetlenen bütün Mersenne asalları

Tablo, `python3 tests/check_mersenne.py 136279841 132049 2` komutunun denetlediği bütün p = 2^e − 1 Mersenne asallarını verir (Bölüm 7). Bunlar 3 ≤ e ≤ 136 279 841 aralığındaki bilinen 51 Mersenne asalıdır. Bilinen 52 Mersenne asalının en küçüğü olan 3 = 2² − 1, p ≥ 5 isteyen (5.2) asal biçiminin dışındadır. Onun noktası n(3) = 33 doğrudan sayımla doğrulanmıştır (Bölüm 7).

Program her p için GMP ile tam sayı aritmetiğinde şunları denetler: E_p(n(p)) = n(p), n(p) − 1 ve n(p) + 1'deki işaretler, en küçük değer E_p(p³ − 1) − (p³ − 1) = −(p − 1)(p + 2), n(p)'nin iki yanında ikişer rastgele nokta ve p'nin bir önceki Mersenne asalıyla çarpımı (Teorem 4). e ≤ 132 049 olan 30 üs için 2^e − 1'in asal olduğunu program kendisi Lucas-Lehmer testiyle doğrular (bu sayıya e = 2 dahildir). Daha büyük üsler bilinen Mersenne asalları listesinden alınır [7]. Bütün koşu 2646 s sürdü, en çok 1,04 GB bellek kullandı. Ham çıktı `tests/RESULTS.md` dosyasının 7. bölümündedir. Aynı tablo makinece okunur biçimde `tests/mersenne.csv` dosyasındadır.

| üs e | 2^e − 1'in basamak sayısı | sonuç | süre (s) |
|---|---|---|---|
| 3 | 1 | PASS | 0,0 |
| 5 | 2 | PASS | 0,0 |
| 7 | 3 | PASS | 0,0 |
| 13 | 4 | PASS | 0,0 |
| 17 | 6 | PASS | 0,0 |
| 19 | 6 | PASS | 0,0 |
| 31 | 10 | PASS | 0,0 |
| 61 | 19 | PASS | 0,0 |
| 89 | 27 | PASS | 0,0 |
| 107 | 33 | PASS | 0,0 |
| 127 | 39 | PASS | 0,0 |
| 521 | 157 | PASS | 0,0 |
| 607 | 183 | PASS | 0,0 |
| 1 279 | 386 | PASS | 0,0 |
| 2 203 | 664 | PASS | 0,0 |
| 2 281 | 687 | PASS | 0,0 |
| 3 217 | 969 | PASS | 0,0 |
| 4 253 | 1 281 | PASS | 0,0 |
| 4 423 | 1 332 | PASS | 0,0 |
| 9 689 | 2 917 | PASS | 0,0 |
| 9 941 | 2 993 | PASS | 0,0 |
| 11 213 | 3 376 | PASS | 0,0 |
| 19 937 | 6 002 | PASS | 0,0 |
| 21 701 | 6 533 | PASS | 0,0 |
| 23 209 | 6 987 | PASS | 0,0 |
| 44 497 | 13 395 | PASS | 0,0 |
| 86 243 | 25 962 | PASS | 0,1 |
| 110 503 | 33 265 | PASS | 0,1 |
| 132 049 | 39 751 | PASS | 0,2 |
| 216 091 | 65 050 | PASS | 0,3 |
| 756 839 | 227 832 | PASS | 1,6 |
| 859 433 | 258 716 | PASS | 1,3 |
| 1 257 787 | 378 632 | PASS | 2,1 |
| 1 398 269 | 420 921 | PASS | 2,3 |
| 2 976 221 | 895 932 | PASS | 5,9 |
| 3 021 377 | 909 526 | PASS | 4,7 |
| 6 972 593 | 2 098 960 | PASS | 17,0 |
| 13 466 917 | 4 053 946 | PASS | 36,5 |
| 20 996 011 | 6 320 430 | PASS | 53,9 |
| 24 036 583 | 7 235 733 | PASS | 78,1 |
| 25 964 951 | 7 816 230 | PASS | 111,5 |
| 30 402 457 | 9 152 052 | PASS | 133,1 |
| 32 582 657 | 9 808 358 | PASS | 154,4 |
| 37 156 667 | 11 185 272 | PASS | 132,9 |
| 42 643 801 | 12 837 064 | PASS | 172,6 |
| 43 112 609 | 12 978 189 | PASS | 207,7 |
| 57 885 161 | 17 425 170 | PASS | 364,2 |
| 74 207 281 | 22 338 618 | PASS | 226,9 |
| 77 232 917 | 23 249 425 | PASS | 214,3 |
| 82 589 933 | 24 862 048 | PASS | 237,6 |
| 136 279 841 | 41 024 320 | PASS | 445,6 |

## Kaynaklar

1. E. E. Kummer, "Über die Ergänzungssätze zu den allgemeinen Reciprocitätsgesetzen", Journal für die reine und angewandte Mathematik 44 (1852), 93–146, doi:10.1515/crll.1852.44.93.
2. A.-M. Legendre, Essai sur la théorie des nombres, ikinci baskı, Courcier, Paris, 1808.
3. OEIS Foundation, The On-Line Encyclopedia of Integer Sequences, A000788, A001142, A001405, A007685, A048881, A078903 ve A078904 dizileri, https://oeis.org, erişim 22 Kasım 2026.
4. J. C. Lagarias ve H. Mehta, "Products of binomial coefficients and unreduced Farey fractions", International Journal of Number Theory 12 (2016), no. 1, 57–91, doi:10.1142/S1793042116500044, arXiv:1409.4145.
5. A. Straub, V. H. Moll ve T. Amdeberhan, "The p-adic valuation of k-central binomial coefficients", Acta Arithmetica 140 (2009), no. 1, 31–42, doi:10.4064/aa140-1-2, arXiv:0811.2028.
6. D. H. Lehmer, "An extended theory of Lucas' functions", Annals of Mathematics (2) 31 (1930), no. 3, 419–448, doi:10.2307/1968235.
7. Great Internet Mersenne Prime Search, bilinen Mersenne asalları listesi, https://www.mersenne.org/primes/, erişim 22 Kasım 2026.
8. J. Augustus, "Pascal Mersenne Rows: powers of two as carry-free Pascal rows in Mersenne bases", 2026, https://github.com/JamesAugustus/pascal-mersenne-rows.
9. J. Augustus, "FactorX: the universe language of numbers and its main example, Bow Draw", sürüm 1.0, 2026, eşlik eden belge.
10. A. Granville, "Arithmetic properties of binomial coefficients I: Binomial coefficients modulo prime powers", içinde: J. Borwein ve diğerleri (ed.), Organic Mathematics (Burnaby, BC, 1995), CMS Conference Proceedings 20, American Mathematical Society, Providence, RI, 1997, 253–276, https://dms.umontreal.ca/~andrew/Binomial/.
11. H. Delange, "Sur la fonction sommatoire de la fonction « somme des chiffres »", L'Enseignement Mathématique (2) 21 (1975), 31–47, doi:10.5169/seals-47328.
12. J. R. Trollope, "An explicit expression for binary digital sums", Mathematics Magazine 41 (1968), no. 1, 21–25, doi:10.1080/0025570X.1968.11975826.
13. L. Du ve J. C. Lagarias, "Partial factorizations of products of binomial coefficients", International Journal of Number Theory 18 (2022), no. 3, 691–728, doi:10.1142/S1793042122500373, arXiv:2006.15439.
14. M. D. Hirschhorn, "The asymptotic behavior of ∏_{k=0}^{n} C(n, k)", The Fibonacci Quarterly 51 (2013), no. 2, 163–173, doi:10.1080/00150517.2013.12427960.
15. B. C. Kellner, "Asymptotic products of binomial and multinomial coefficients revisited", Integers 24 (2024), Paper A59, doi:10.5281/zenodo.12167556, arXiv:2312.11369.
16. J. M. Holte, "Carries, combinatorics, and an amazing matrix", The American Mathematical Monthly 104 (1997), no. 2, 138–149, doi:10.1080/00029890.1997.11990612.
17. P. Diaconis ve J. Fulman, "Carries, shuffling, and an amazing matrix", The American Mathematical Monthly 116 (2009), no. 9, 788–803, doi:10.4169/000298909X474864, arXiv:0806.3583.

Bu paketteki kaynak kod MIT lisansıyla, metin, şekiller ve tablolar CC BY 4.0 lisansıyla sunulur. Telif hakkı © 2026 James Augustus.
