# Terminoloji ve Notasyon — Kitap Geneli Sözleşme (yaşayan belge)

Bu dosya, kitabın **tamamında** kullanılacak terim ve gösterimlerin **mevcut** kaynağıdır. Kutsal değildir; daha iyi bir terim/gösterim bulunursa değiştirilebilir.

Bir konu yazan ajan:

1. Buradaki terim ve gösterimleri **kullanmalıdır**.
2. Yeni bir terim ya da gösterim getiriyorsa, onu **aynı anda bu dosyaya da eklemelidir**.
3. Mevcut bir terimi/gösterimi değiştirmek istiyorsa: değişikliği (nedeniyle birlikte) `config/KARARLAR.md` dosyasına işlemeli ve ilgili tüm `.tex` dosyalarına yaymalıdır.

## Temel gösterimler

| Kavram | Gösterim | Not |
|---|---|---|
| Kombinasyon (binom katsayısı) | `\binom{n}{r}` | $n$ nesneden $r$ tanesini sırasız seçme |
| Permütasyon | `P(n,r)` | sıralı seçim; $P(n,r)=n!/(n-r)!$ |
| Faktöriyel | `n!` | $0! = 1$ |
| Bölme | `a \mid b` | “$a$, $b$'yi böler” |
| Bölmeme | `a \nmid b` | |
| EBOB | `\gcd(a,b)` | en büyük ortak bölen |
| EKOK | `\operatorname{lcm}(a,b)` | en küçük ortak kat |
| Kongruans | `a \equiv b \pmod m` | modüler aritmetik |
| Alt taban | `\lfloor x \rfloor` | |
| Üst tavan | `\lceil x \rceil` | |
| Küme eleman sayısı | `|A|` | kümenin boyutu |
| Karmaşıklık | `O(n)`, `O(n^2)`, `O(\log n)`, `O(1)` | Big O notasyonu |
| Sayı tabanı | `(n)_b` | “$n$ sayısı $b$ tabanında”, örn. $(101)_2 = 5$ |
| Logaritma | `\log_a x` | “$a$ tabanında $x$'in logaritması”; $a^y=x \iff y=\log_a x$ |
| Doğal logaritma | `\ln x` | yalnız $\log_e x$ kastedildiğinde kullanılır |
| İkili logaritma | `\log_2 x` | karmaşıklık/girdi boyutu bağlamında taban sıkça açık yazılır |

## Kural: Teknik terimlerin İngilizce/Türkçe kararı

Olimpiyat ve rekabetçi programlama literatüründe **oturmuş İngilizce teknik terimler olduğu gibi kalır**; zorlama Türkçeleştirme anlamı bozar. Yerleşik Türkçe matematik terimleri ise korunur. Üç kategori vardır:

### A) İngilizce korunur (Türkçe karşılığı KULLANILMAZ)

| İngilizce (asıl) | ❌ Kullanılmayacak Türkçe |
|---|---|
| MST (minimum spanning tree) | minimum yayılım ağacı |
| spanning tree | yayılım ağacı |
| two pointers | iki işaretçi |
| prefix sum(s) | kümülatif toplam(lar) |
| greedy | açgözlü |
| bitmask | bit maskesi |
| bitwise | bit düzeyinde |
| deque | iki uçlu kuyruk |
| adjacency list / matrix | komşuluk listesi / matrisi |
| priority queue | öncelikli kuyruk |
| binary heap | ikili öbek |
| hash table | karma tablosu |
| memoization | belleklenmiş arama, belleklenme |
| DFS | "derin öncelikli arama", "gezinme" — doğru kullanım: **DFS (derinlik öncelikli arama)** |
| BFS | "geniş öncelikli arama", "gezinme" — doğru kullanım: **BFS (genişlik öncelikli arama)** |
| stack | yığın → **ARTIK SERBEST** (bkz. aşağıdaki not) |
| queue | kuyruk → **ARTIK SERBEST** (bkz. aşağıdaki not) |
| set / map | küme (set) / eşlem (map) → **ARTIK SERBEST** (bkz. aşağıdaki not) |

> **NOT (D18 — kullanıcı kararı):** `stack`, `queue`, `set`, `map` terimlerinin Türkçe
> karşılıkları (`yığın`, `kuyruk`, `küme`/`eşlem`) **Türkçe bilgisayar bilimi
> literatüründe yerleşiktir**. Bu dört terim artık yasak listesinde **değildir**; her
> iki biçim de kullanılabilir. Yaygın kitap kalıbı: başlıklarda `Stack (Yığın)`,
> `Queue (Kuyruk)` gibi **çift gösterim**; metin içinde ilk geçişte çift, sonrasında
> tek biçim (tutarlı olmak kaydıyla).

### B) Türkçe kalır, İLK geçişte İngilizce eşi parantezde verilir

| Türkçe (korunur) | İlk geçişte parantezde |
|---|---|
| işaretçi | (pointer) |
| rekürsiyon | (recursion) — **"özyineleme" DEĞİL, "rekürsiyon" standardize edilir** |
| dinamik programlama | (DP) |
| düğüm | (node) |
| kenar | (edge) |
| dizi | (array) — yalnız diziler/CS bağlamında |
| topolojik sıralama | (topological sort) |
| en kısa yol | (shortest path) |
| sözde kod | (pseudocode) |
| düzensiz dizilim | (derangement) |
| graf | (graph) |

### C) Yerleşik Türkçe matematik terimi (dokunulmaz)

| İngilizce | Türkçe (kullanılır) |
|---|---|
| invariant | değişmez |
| monovariant | yarı-değişmez |
| pigeonhole principle | güvercin yuvası ilkesi |
| extremal principle | uç değer ilkesi |
| working backwards | tersine çalışma |
| parity | teklik–çiftlik (parite) |
| inclusion–exclusion | içerme-dışarma |
| binomial coefficient | binom katsayısı |
| binomial expression | binom |
| binomial expansion | binom açılımı |
| binomial theorem | binom teoremi |
| Pascal's triangle | Pascal üçgeni |
| hockey-stick identity | hokey sopası özdeşliği |
| stars and bars | ayraç yöntemi — "Yıldızlar ve Bölücüler" çevirisi KULLANILMAZ |
| Vandermonde's identity | Vandermonde özdeşliği |
| combinatorial proof / double counting | kombinatorik ispat / iki yoldan sayma |
| binary search | ikili arama |
| sorting | sıralama |
| loop | döngü |
| Handshaking Lemma | el sıkışma lemması — kitapta **"El Sıkışma Lemması"** adıyla tekleştirildi ("Tokalaşma Lemması" YANLIŞ) |
| Lucas parity theorem | Lucas parite teoremi (Bölüm 15'te "Sierpiński / Lucas Parite Teoremi" adıyla ispatlanır) |
| Fermat's Little Theorem | Fermat'nın Küçük Teoremi (Bölüm 14'te ispatlanır; Bölüm 11, 34 ve 37'de kullanılır) |
| logaritma | logaritma (`\log_a x`) — Bölüm 16; $O(\log n)$ bağlamında taban sıkça $2$'dir ama büyük $O$'da önemsizdir |

## Yazım tercihleri (terimden bağımsız)

- **`operatör`** kullanılır, **`işleç` KULLANILMAZ**. (Kullanıcı kararı, D18: "işleç"
  uydurma bir karşılıktır; yerleşik kullanım "operatör"dür.)
  Örnek: "işleç önceliği" → **"operatör önceliği"**; "aritmetik işleçlerle" →
  **"aritmetik operatörlerle"**; "mantıksal işleçler" → **"mantıksal operatörler"**.
- İngilizce bir terime Türkçe ek **apostrofla** bağlanır (bkz. Kurallar).

## Kurallar

- Aynı kavramı farklı yerlerde farklı adlandırma; yukarıdaki karşılığı kullan.
- İngilizce bir terime Türkçe ek **apostrofla** bağlanır, doğrudan yapıştırılmaz: `prefix sums'ın`, `adjacency list'ini`, `hash table'a`, `spanning tree'ye`, `MST'sinde`. Yanlış: `prefix sumsın`, `adjacency listni`, `hash tablena`, `spanning treedır`, `MST (minimum spanning tree)nda`, `bitwiseki`.
- Her terimi **ilk kullanıldığı yerde** kısaca tanımla. Örn. “değişmez (invariant), bir süreç boyunca sabit kalan niceliktir.”
- Notasyonu metin içinde her zaman açıkla: “EBOB'u $\gcd(a,b)$ ile gösterelim” gibi.
- Henüz tanıtılmamış bir kavramı bir konunun **ana aracı** olarak kullanma; kullanmak zorundaysan ileri referans ver: “(Bölüm 4'te göreceğiz).”
