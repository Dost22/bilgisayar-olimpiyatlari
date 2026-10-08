# Denetim Raporu (otomatik — doğrulanmadan UYGULANMAZ)

Toplam bulgu: 82 — critical: 1, major: 31, medium: 1, minor: 49

## [CRITICAL] 17_invaryant_ve_monovaryant.tex:222 — logic_gap (güven: high)
- **Alıntı:** Sistem için alttan sınırlı bir potansiyel fonksiyonu tanımlanabilir:
\[
\Phi = \sum_{1 \le i < j \le n} |x_i - x_j| \quad \text{veya} \quad \sum_{i=1}^n \left( \sum_{j=1}^{n-1} j \cdot x_{i+j} \right)^2
\]
Negatif bir sayının pozitife dönmesi durum uzayında ters sıralanmış çiftlerin (inversiyonların) azalmasını sağlar. Durum uzayı sonlu sayıda permütasyonla ilişkili olduğundan süreç sonlu adımda durmak zorundadır.
- **Sorun:** Reel sayılar üzerinde tanımlı bu süreçte (klasik IMO 1986 Soru 3 türevi) sunulan sözde ispat tamamen temelsizdir. Verilen birinci potansiyel fonksiyon (mutlak farklar toplamı) monovaryant değildir. Ayrıca reel sayılar her adımda değiştiğinden durum uzayı permütasyonlarla sonlu bir kümede kalmaz; karesel potansiyelin her adımda kesin azaldığı veya durum uzayının neden sonlu olduğu gösterilmemiştir.
- **Öneri:** Problemin karesel monovaryantı (örneğin $\Phi(x) = \sum_{i=1}^n (s_i)^2$ şeklinde uygun tanımlanmış kısmi toplamlar veya $E = \sum (x_i - x_{i+1})^2$ formu) açıkça seçilip hamle altındaki farkı $\Delta \Phi < 0$ olarak tam ispatlanmalı veya daha temel/açıkça gösterilebilen bir monovaryant örneği ile değiştirilmelidir.

## [MAJOR] 11_bolunebilme.tex:331 — logic_gap (güven: high)
- **Alıntı:** N = \overline{a_k a_{k-1} \dots a_2 a_1 a_1 a_2 \dots a_{k-1} a_k}
- **Sorun:** Palindrom sayının basamakları $N = \overline{a_k \dots a_1 a_1 \dots a_k}$ olarak tanımlandığında birler basamağı $d_0 = a_k$ olur. Ancak takip eden çözümde $a_m$'nin sağ yarıdaki basamak indeksi $m-1$ (dolayısıyla $m=1$ için $d_0 = a_1$) olarak kabul edilmiş ve 'Sağ yarıda sondan m'nci basamak olarak yer alır; indeksi m-1 olduğundan...' denmiştir. Sayının basamak dizilimi ile ispatta kullanılan basamak indeksleri birbiriyle çelişmektedir.
- **Öneri:** Sayı $N = \overline{a_1 a_2 \dots a_k a_k \dots a_2 a_1}$ şeklinde tanımlanmalı veya $a_m$ rakamının sağ yarıdaki indisi $k-m$, sol yarıdaki indisi $k-1+m$ olarak güncellenmelidir.

## [MAJOR] 11_bolunebilme.tex:427 — bad_reference (güven: high)
- **Alıntı:** Bu ispat, Bölüm 1'de ele aldığımız İyi Sıralama İlkesi'nin (negatif olmayan tam sayılardan oluşan boş olmayan her kümenin en küçük bir elemanı vardır) doğrudan bir uygulamasıdır.
- **Sorun:** Bölüm 1'de ('Matematiğin Dili') İyi Sıralama İlkesi yer almamaktadır. Kitap izlencesinde İyi Sıralılık İlkesi Bölüm 18'de ('Uç Değer ve Tersine Çalışma') ele alınmaktadır.
- **Öneri:** 'Bu ispat, Bölüm 18'de ayrıntılı ele alacağımız İyi Sıralılık İlkesi'nin (negatif olmayan tam sayılardan oluşan boş olmayan her kümenin en küçük bir elemanı vardır) doğrudan bir uygulamasıdır.' şeklinde düzeltilmelidir.

## [MAJOR] 11_bolunebilme.tex:535 — duplicated_example (güven: high)
- **Alıntı:** $n > 1$ bir tam sayı olsun. $2^n - 1$ sayısının $n$ ile tam bölünemeyeceğini kanıtlayınız.
- **Sorun:** Bu problem, Bölüm 33'te (33_alistirmalar_sayilar_teknikler.tex) '[Zorluk: Olimpiyat] n > 1 bir tamsayı olsun. n | 2^n - 1 koşulunu sağlayan hiçbir n > 1 tamsayısının bulunmadığını ispatlayınız.' başlığıyla alıştırma sorusu olarak verilmiştir. Ayrıca bu çözüm, henüz Bölüm 11 düzeyinde tanımlanmamış olan modüler aritmetik, mertebe (order) ve Fermat'nın Küçük Teoremi gibi ileri düzey araçları gerektirmektedir.
- **Öneri:** Bu örnek Bölüm 11'den çıkarılmalı veya Bölüm 11'in müfredatına uygun (yalnızca bölme algoritması ve temel bölünebilme özelliklerini kullanan) temel bir örnek ile değiştirilmelidir.

## [MAJOR] 12_asal_sayilar.tex:223 — duplicated_example (güven: high)
- **Alıntı:** \begin{example}[IMO 1959]
Her $n$ pozitif tamsayısı için
\[ \frac{21n + 4}{14n + 3} \]
kesrinin sadeleştirilemez olduğunu gösteriniz.
\end{example}
- **Sorun:** Bu örnek (IMO 1959 Soru 1: (21n+4)/(14n+3) kesrinin indirgenemezliği), Bölüm 13'te (13_ebob_ve_ekok.tex) '[1959 Uluslararası Matematik Olimpiyatı - Soru 1]' başlığı altında birebir aynı problem olarak çözülmektedir.
- **Öneri:** Bu örnek Bölüm 13'e (Öklid Algoritması) daha uygundur. Bölüm 12'deki bu örnek yerine aralarında asallığı pekiştiren farklı bir olimpiyat örneği (örneğin $\gcd(2n+1, 3n+2) = 1$ veya $\gcd(a, b)=1 \implies \gcd(a+b, a^2-ab+b^2) \in \{1, 3\}$) eklenmelidir.

## [MAJOR] 13_ebob_ve_ekok.tex:277 — duplicated_example (güven: high)
- **Alıntı:** \begin{example}[1959 Uluslararası Matematik Olimpiyatı - Soru 1]
Her $n$ pozitif tamsayısı için $\frac{21n + 4}{14n + 3}$ kesrinin sadeleştirilemez (indirgenemez) olduğunu kanıtlayınız.
\end{example}
- **Sorun:** Bu örnek (IMO 1959, Soru 1: $(21n+4)/(14n+3)$ kesrinin sadeleştirilemezliği) Bölüm 12'de (12_asal_sayilar.tex) zaten birebir aynı soru ve yöntemle çözülmüştür.
- **Öneri:** Örneği Öklid algoritmasını pekiştiren farklı bir problemle değiştiriniz (örneğin $\gcd(2n+1, 3n+2)$ veya $\gcd(n!+1, (n+1)!+1)$ gibi bir olimpiyat sorusu).

## [MAJOR] 16_parite_ve_simetri.tex:282 — logic_gap (güven: high)
- **Alıntı:** Bu durum beyaz karelerin kullanımında yerel bir tıkanıklığa yol açar. Nitekim ayrıntılı bir graf analizi, $(1, 1)$'den $(5, 5)$'e giden bir Hamilton yolunun bulunmadığını gösterir.
- **Sorun:** Yazar, atın renk değiştirme kuralının bu problemde tek başına çelişki vermediğini belirttikten sonra köşe karelerinin komşuluk kısıtlarına değinmiş, fakat ispatı tamamlamayıp 'ayrıntılı bir graf analizi Hamilton yolunun bulunmadığını gösterir' diyerek tamamlanmamış bir argümanla sonlandırmıştır. Bu durum belirgin bir ispat boşluğudur (logic gap). Ayrıca 'At Gezintisi ve Renk Değişimi' başlığı altında pariteyle doğrudan çelişki veren bir soru (örneğin 25 karelik tahtada kapalı bir turun imkânsızlığı veya beyaz kareden başlayan bir açık turun imkânsızlığı) yerine pariteyle çözülemeyen bir sorunun yarım bırakılması pedagojik açıdan da hatalıdır.
- **Öneri:** Örnek, renklendirme ve parite kuralının doğrudan ve eksiksiz çelişki ürettiği bir problemle değiştirilmelidir; örneğin: '5x5'lik tahtada atın başladığı kareye dönen kapalı bir tur (Hamilton çevrimi) yapmasının imkânsız olduğunu gösteriniz' (25 adım tek olduğundan at başladığı renkte olamaz) veya 'Bir atın beyaz bir kareden başlayarak 25 karenin tamamını tam bir kez ziyaret etmesi mümkün müdür?' (13 siyah, 12 beyaz kare olduğundan beyazdan başlayan tur en fazla 12 siyah kare gezebilir).

## [MAJOR] 17_invaryant_ve_monovaryant.tex:105 — duplicated_example (güven: high)
- **Alıntı:** $8 \times 8$ boyutundaki standart bir satranç tahtasının karşılıklı iki çapraz köşesi (örneğin sol alt $a1$ ve sağ üst $h8$) kesilip atılıyor. Kalan 62 karelik alanı, her biri $1 \times 2$ boyutunda olan 31 adet domino taşı ile eksiksiz örtmek mümkün müdür?
- **Sorun:** Bu problem ve çözümü, bir önceki bölüm olan Bölüm 16'da (16_parite_ve_simetri.tex) neredeyse birebir aynı metinle çözümlü örnek olarak zaten işlenmiştir.
- **Öneri:** Örnek yerine invaryant konusunu pekiştiren farklı bir klasik problem (örneğin ızgara köşegenlerindeki işaret değişimleri, 15-bulmacası permütasyon paritesi veya tahtada $a, b \to a+b-1$ işlemi) eklenmeli ya da Bölüm 16'daki örneğe kısa bir atıfla geçilmelidir.

## [MAJOR] 17_invaryant_ve_monovaryant.tex:235 — logic_gap (güven: high)
- **Alıntı:** Bir satranç tahtasında bazı karelere taşlar konmuştur. Her saniye, en az 3 boş komşusu (ortak kenara sahip) olan bir taştan bir tanesi tahtadan kaldırılmaktadır. Başlangıçta tahtada kaç taş olursa olsun, bu sürecin sonlu adımda duracağını kanıtlayınız.
- **Sorun:** Örnek sorusunda sorulan problem taş eksiltmenin sonlanmasıdır (ki çözümde tek satırda taş sayısı azalır denerek geçilmiştir). Ancak çözümün geri kalan büyük kısmında soru metninde hiç sorulmayan 'virüs yayılımı / çevre monovaryantı' problemi çözülmektedir. Soru metni ile çözüm birbiriyle uyumsuzdur.
- **Öneri:** Örnek metni doğrudan virüs yayılımı problemine çevrilmelidir: 'Bir $8 \times 8$ satranç tahtasında başlangıçta bazı kareler enfektedir. Her adımda en az iki enfekte komşusu olan sağlıklı bir kare de enfekte olmaktadır. Tüm tahtanın enfekte olabilmesi için başlangıçta en az kaç enfekte kare bulunmalıdır?'

## [MAJOR] 21_diziler_ve_temel_teknikler.tex:118 — notation_violation (güven: high)
- **Alıntı:** \section{Kümülatif Toplamlar (Prefix Sums)}
- **Sorun:** Terminoloji sözleşmesinde (Tablo A) 'prefix sum(s)' teriminin İngilizce korunacağı ve Türkçe karşılığı olan 'kümülatif toplam(lar)' ifadesinin kesinlikle kullanılmayacağı belirtilmiştir. Başlıkta ve metin genelinde (örn. tanım başlığı, alt başlıklar ve özet maddesi) 'kümülatif toplam' kullanımı sözleşmeyi ihlal etmektedir.
- **Öneri:** Bölüm başlığı '\section{Prefix Sums}' yapılmalı; metin içindeki 'Kümülatif Toplam Dizisi' ve 'kümülatif toplam' ifadeleri 'prefix sum' terimiyle değiştirilmelidir.

## [MAJOR] 21_diziler_ve_temel_teknikler.tex:233 — notation_violation (güven: high)
- **Alıntı:** \section{İki İşaretçi (Two Pointers)}
- **Sorun:** Terminoloji sözleşmesinde (Tablo A) 'two pointers' teriminin İngilizce korunacağı ve Türkçe 'iki işaretçi' karşılığının kullanılmayacağı belirtilmiştir.
- **Öneri:** Başlık '\section{Two Pointers}' olarak güncellenmeli; teknik adı olarak geçen 'İki İşaretçi ile İki Toplam' ve benzeri kullanımlar 'Two Pointers' olarak revize edilmelidir (tekil 'işaretçi' kullanımı Tablo B gereği geçerlidir).

## [MAJOR] 24_temel_veri_yapilari.tex:55 — bad_reference (güven: high)
- **Alıntı:** Bölüm 19'da gördüğümüz fonksiyon çağrıları bellekte tam olarak bir yığın gibi saklanır
- **Sorun:** Bölüm 19'da (Algoritma Nedir) fonksiyonlar veya fonksiyon çağrıları (call stack) işlenmemektedir. Fonksiyonlar ve çağrı yığını Bölüm 29'da (Döngüler ve Fonksiyonlar), rekürsiyon ise Bölüm 25'te anlatılmaktadır.
- **Öneri:** Atıf Bölüm 29'a (veya Bölüm 25'e) yönlendirilmeli ya da "ilerleyen bölümlerde göreceğimiz fonksiyon çağrıları" şeklinde düzeltilmelidir.

## [MAJOR] 24_temel_veri_yapilari.tex:18 — notation_violation (güven: high)
- **Alıntı:** \section{Stack (Yığın)}
- **Sorun:** Terminoloji sözleşmesi Kategori A'da "stack", "queue", "set / map" terimlerinin İngilizce korunması ve Türkçe karşılıklarının ("yığın", "kuyruk", "küme (set) / eşlem (map)") kullanılmaması açıkça belirtilmiştir. Bölüm başlıklarında ve gövde metninde bu Türkçe karşılıklar birincil terim olarak kullanılmıştır.
- **Öneri:** Başlıklar ve metin boyunca "yığın" yerine "stack", "kuyruk" yerine "queue", "eşlem/sözlük" yerine "map" terimleri kullanılmalıdır.

## [MAJOR] 26_greedy_yaklasimi.tex:61 — notation_violation (güven: high)
- **Alıntı:** \begin{definition}[Açgözlü Seçim Özelliği / Greedy Choice Property]
- **Sorun:** Terminoloji sözleşmesine göre 'greedy' terimi İngilizce olarak korunmalıdır; 'açgözlü' Türkçe karşılığı kesinlikle kullanılmamalıdır.
- **Öneri:** \begin{definition}[Greedy Seçim Özelliği / Greedy Choice Property] olarak güncellenmelidir.

## [MAJOR] 26_greedy_yaklasimi.tex:280 — logic_gap (güven: high)
- **Alıntı:** Tanım gereği $e$, kesiti kesen \textbf{en hafif} kenar olduğundan $w(e) \le w(e')$'dir. Dolayısıyla $w(T') \le w(T)$ olur. $T$ zaten minimum ağırlıklı olduğundan $w(T') < w(T)$ olamaz. Şu halde $w(T') = w(T)$ olmalıdır; yani $e$ kenarını içeren $T'$ de bir minimum kapsayan ağaçtır (kenar ağırlıkları birbirinden farklıysa $w(e) < w(e')$ olacağından doğrudan çelişki çıkar).
- **Sorun:** Teorem ifadesinde $e$'nin kesiti kesen kenarlar arasında ağırlığı 'kesin olarak en küçük' (strictly minimal) olduğu belirtilmiştir. $e' \ne e$ kesiti kesen bir başka kenar olduğundan, teorem hipotezi doğrudan $w(e) < w(e')$ olmasını gerektirir. Dolayısıyla $w(T') < w(T)$ elde edilerek doğrudan çelişkiye ulaşılır. İspattaki 'w(e) <= w(e') olduğundan w(T') = w(T) olmalıdır' ve parantez içindeki 'kenar ağırlıkları birbirinden farklıysa' açıklaması teorem hipoteziyle çelişmekte ve mantıksal bir pürüz oluşturmaktadır.
- **Öneri:** Adım doğrudan kesin eşitsizlikle ifade edilmelidir: '$e$ kesiti kesen kenarlar arasında kesin olarak en küçük ağırlığa sahip olduğundan ve $e' \ne e$ kesiti kestiğinden $w(e) < w(e')$'dir. Buradan $w(T') = w(T) - w(e') + w(e) < w(T)$ elde edilir; bu ise $T$'nin bir MST olmasıyla çelişir. Dolayısıyla her MST $e$ kenarını içermek zorundadır.'

## [MAJOR] 27_graflar_ve_arama.tex:361 — notation_violation (güven: high)
- **Alıntı:** Kruskal Algoritması (Kenar Odaklı Açgözlülük)
- **Sorun:** Terminoloji sözleşmesinde 'greedy' terimi Kategori A (İngilizce korunur, Türkçe karşılığı KULLANILMAZ) altındadır ve 'açgözlü' kullanımı açıkça yasaklanmıştır. Benzer şekilde alt başlıktaki 'Prim Algoritması (Düğüm Odaklı Açgözlülük)' ifadesinde de 'açgözlülük' kullanılmamalıdır.
- **Öneri:** Başlıklar sırasıyla 'Kruskal Algoritması (Kenar Odaklı Greedy Yaklaşım)' ve 'Prim Algoritması (Düğüm Odaklı Greedy Yaklaşım)' olarak güncellenmelidir.

## [MAJOR] 27_graflar_ve_arama.tex:221 — notation_violation (güven: high)
- **Alıntı:** Kuyruk (Queue) ile Seviye Seviye İlerleme
- **Sorun:** Terminoloji sözleşmesinde 'queue' terimi Kategori A (İngilizce korunur) altındadır ve 'kuyruk' Türkçe karşılığı kullanılmayacaklar arasında listelenmiştir.
- **Öneri:** Başlık ve metin içindeki kullanımlarda 'Queue ile Seviye Seviye İlerleme' ve 'queue' terimi tercih edilmelidir.

## [MAJOR] 27_graflar_ve_arama.tex:380 — bad_reference (güven: high)
- **Alıntı:** Bölüm 24'te gördüğümüz priority queue (min-heap) yapısı kullanılır.
- **Sorun:** Bölüm 24'te (Temel Veri Yapıları) yalnızca Stack, Queue, Set ve Map ele alınmış olup priority queue (ikili öbek / min-heap) anlatılmamıştır.
- **Öneri:** 'Bölüm 24'te gördüğümüz priority queue' atfı kaldırılarak priority queue kısaca tanıtılmalı veya veri yapısının işlevi parantez içi açıklamayla verilmelidir.

## [MAJOR] 27_graflar_ve_arama.tex:444 — bad_reference (güven: high)
- **Alıntı:** En küçük mesafeli düğüme hızla ulaşmak için Bölüm 24'te gördüğümüz priority queue (\texttt{std::priority\_queue}) kullanılır.
- **Sorun:** Bölüm 24'te priority queue (veya std::priority_queue) anlatılmamaktadır.
- **Öneri:** 'Bölüm 24'te gördüğümüz' ifadesi kaldırılmalıdır.

## [MAJOR] 28_c_ye_giris_ve_kontrol_akisi.tex:57 — factual (güven: high)
- **Alıntı:** \item \texttt{\textbackslash{}\%d} veya \texttt{\textbackslash{}\%i}: İşaretli 32-bit tam sayı (\texttt{int}).
- **Sorun:** Biçim belirteçleri metin içinde listelenirken ve açıklanırken (57-65, 144, 155, 156, 167, 169. satırlar) `\textbackslash{}\%` yazılmıştır. Bu komut PDF derlemesinde ekrana ters bölü (`\`) basarak belirteçlerin C dilindeki gerçek biçimi olan `%d`, `%u`, `%lld`, `%lf`, `%f`, `%c`, `%s` yerine `\%d`, `\%u`, `\%lld`, `\%lf` olarak görünmesine neden olmaktadır. C dilinde format belirteçleri ters bölü içermez.
- **Öneri:** `\textbackslash{}\%` yerine doğrudan `\%` kullanılmalıdır (örn. `\texttt{\%d}`, `\texttt{\%u}`, `\texttt{\%lld}`, `\texttt{\%lf}`, `\texttt{\%f}`, `\texttt{\%c}`, `\texttt{\%s}`).

## [MAJOR] 28_c_ye_giris_ve_kontrol_akisi.tex:189 — factual (güven: high)
- **Alıntı:** \text{\texttt{if (A \textbackslash{}\&\textbackslash{}\& B)}} \iff \text{\texttt{if (A) \textbackslash{}\{ if (B) \textbackslash{}\{ ... \textbackslash{}\}} \textbackslash{}\}}}
- **Sorun:** Kısa devre değerlendirmesinin denklik gösteriminde `\&` ve süslü parantezlerin önüne fazladan `\textbackslash{}` eklenmiştir. Bu durum derlenen çıktıda C dilinde bulunmayan ters bölü karakterlerinin görünmesine (`if (A \&\& B) <=> if (A) \{ if (B) \{ ... \} \}`) ve C sözdiziminin bozulmasına yol açmaktadır.
- **Öneri:** İfade şu şekilde düzeltilmelidir: `\text{\texttt{if (A \&\& B)}} \iff \text{\texttt{if (A) \{ if (B) \{ ... \} \}}}`

## [MAJOR] 29_donguler_ve_fonksiyonlar.tex:343 — prerequisite_violation (güven: high)
- **Alıntı:** typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} List;
- **Sorun:** Bölüm 29 henüz döngüler ve temel fonksiyonları işlemektedir. Kod örneğinde kullanılan 'struct' ve 'typedef' yapıları Bölüm 31'de, dinamik bellek tahsisi (malloc, realloc, free) ve detaylı işaretçi modelleri ise Bölüm 30'da anlatılmaktadır. Bu kavramlar henüz tanıtılmadan karmaşık bir dinamik dizi yapısı örnek olarak sunulmuştur.
- **Öneri:** Bu örnek yerine fonksiyonlara işaretçiyle dizi veya basit değişken aktarımını gösteren, henüz struct ve dinamik bellek (malloc/realloc) gerektirmeyen temel bir fonksiyon örneği verilmelidir.

## [MAJOR] 31_bitwise_ve_struct.tex:81 — factual (güven: high)
- **Alıntı:** \lstinline|n = n | (1 << k)|
- **Sorun:** \lstinline sınırlandırıcısı olarak '|' seçilmiştir; ancak kod parçası içinde bitwise VEYA ('|') operatörü yer aldığından listings paketi kodu ilk '|' karakterinde kapatmakta ve geri kalan kısmı (' (1 << k)|') metin modunda hatalı/bozuk karakterlerle dizmektedir.
- **Öneri:** Sınırlandırıcı olarak '/' veya '+' kullanılmalıdır: \lstinline/n = n | (1 << k)/

## [MAJOR] 31_bitwise_ve_struct.tex:147 — factual (güven: high)
- **Alıntı:** \lstinline|maskA | maskB|
- **Sorun:** \lstinline sınırlandırıcısı olarak '|' seçilmiştir; ancak kod içinde bitwise VEYA ('|') operatörü bulunduğu için listings kodu erken kapatmakta ve ' maskB|' kısmı metin modunda bozuk basılmaktadır.
- **Öneri:** Sınırlandırıcı olarak '/' kullanılmalıdır: \lstinline/maskA | maskB/

## [MAJOR] 32_alistirmalar_sayma.tex:310 — duplicated_example (güven: high)
- **Alıntı:** \begin{example}[Zor: André Yansıma İlkesi ve Köşegeni Aşmama]
Bir parçacık $(0,0)$ noktasından $(n,n)$ noktasına sağa ve yukarı birim adımlarla ilerlemektedir. Parçacığın $y = x$ doğrusunun \textbf{kesinlikle üzerine çıkmadığı} (yani her adımda $y \le x$ kaldığı) kaç farklı yol vardır?
\end{example}
- **Sorun:** Bu problem ve çözümü, kitabın Bölüm 10'unda '[André'nin Yansıma İlkesi / Catalan Sayıları Sezgisi]' başlığı altında ve Bölüm 9'unda '[Köşegeçen Sınırı — Yansıma Fikrine Giriş]' adıyla zaten aynı model ve yöntemle işlenmiştir. Alıştırma bölümünde aynı soruyu üçüncü kez çözmek yerine yansıma ilkesinin farklı bir varyantı (örneğin Bertrand Sandık Problemi / Ballot Problem ya da $y = x + 1$ yerine farklı bir sınır çizgisine çarpmayan yollar) sorulmalıdır.
- **Öneri:** Örnek, yansıma ilkesinin farklı bir uygulamasıyla değiştirilebilir: Örneğin, $A$ adayının $a$, $B$ adayının $b$ oy aldığı ($a > b$) ve sayım boyunca $A$'nın daima önde gittiği sayım sıralamalarının sayısı (Bertrand Sandık Problemi) veya $(0,0)$'dan $(n,n)$'ye $y \le x + 1$ doğrusunun üzerine çıkmayan yollar gibi özgün bir problem kurgulanabilir.

## [MAJOR] 34_alistirmalar_algoritma_c.tex:216 — notation_violation (güven: high)
- **Alıntı:** Özyineleme yığınından geri dönüşleri izleyelim.
- **Sorun:** Terminoloji sözleşmesinde 'özyineleme' terimi açıkça yasaklanmış ve 'rekürsiyon' teriminin standardize edildiği belirtilmiştir. Ayrıca 'stack' yerine tek başına 'yığın' kullanımı da A grubu yasaklı terimler arasındadır.
- **Öneri:** 'Rekürsiyon yığınından (call stack) geri dönüşleri izleyelim.' veya 'Çağrı yığınından geri dönüşleri izleyelim.' şeklinde düzeltilmelidir.

## [MAJOR] 34_alistirmalar_algoritma_c.tex:401 — notation_violation (güven: high)
- **Alıntı:** \subsection{İki İşaretçi (Two Pointers) Tekniği: Sıralı Dizide Toplam}
- **Sorun:** Terminoloji sözleşmesi A Kategorisi gereğince 'two pointers' terimi İngilizce olarak korunmalı, Türkçe karşılığı ('iki işaretçi') kullanılmamalıdır.
- **Öneri:** Başlık '\subsection{Two Pointers Tekniği: Sıralı Dizide Toplam}' olarak güncellenmelidir.

## [MAJOR] 35_karma_cozumlu_problemler.tex:0 — math_error (güven: high)
- **Alıntı:** N(\text{hiçbiri}) = \sum_{k=0}^{2n-1} (-1)^k \cdot r_k \cdot (n - k)!
- **Sorun:** Toplamın üst sınırı $2n-1$ olarak yazılmıştır; ancak $k > n$ olduğunda $(n-k)!$ ifadesi negatif bir tam sayının faktöriyeli olacağından tanımsızdır. $n \times n$'lik bir tahtada aynı satır ve sütunda bulunmayan en fazla $n$ adet yasaklı kare seçilebilir ($k > n$ için $r_k = 0$). Dolayısıyla toplamın üst sınırı $n$ olmalıdır (nitekim altındaki çözümde üst sınır doğru olarak $n$ alınmıştır).
- **Öneri:** Formüldeki toplamın üst sınırı $n$ yapılmalıdır: $N(\text{hiçbiri}) = \sum_{k=0}^n (-1)^k \cdot r_k \cdot (n - k)!$.

## [MAJOR] 35_karma_cozumlu_problemler.tex:0 — notation_violation (güven: high)
- **Alıntı:** \subsection{Problem 3: Kümülatif Toplamlar ve Güvercin Yuvası: Bölünebilir Alt Diziler}
- **Sorun:** Terminoloji sözleşmesine göre 'kümülatif toplam(lar)' ifadesi kesinlikle kullanılmamalıdır; bunun yerine 'prefix sum(s)' terimi korunmalıdır. Ayrıca metin içindeki '(a) Kümülatif toplamları sıralayalım:' ve 'Kümülatif toplam dizisiyle çalışırken...' kullanımları da bu kuralı ihlal etmektedir.
- **Öneri:** Başlık '\subsection{Problem 3: Prefix Sums ve Güvercin Yuvası: Bölünebilir Alt Diziler}' olarak güncellenmeli; metin içindeki 'Kümülatif toplamları' ve 'Kümülatif toplam dizisiyle' ifadeleri 'Prefix sums dizisini' ve 'Prefix sums dizisiyle' şeklinde düzeltilmelidir.

## [MAJOR] 36_cozumler_ve_ipuclari.tex:401 — notation_violation (güven: high)
- **Alıntı:** \subsection{Kümülatif Toplamlar (Prefix Sums) ve 2 Boyutlu Aralık Sorguları}
- **Sorun:** Terminoloji sözleşmesinde 'prefix sum(s)' teriminin İngilizce korunması gerektiği, Türkçe karşılığı olan 'kümülatif toplam(lar)' ifadesinin KULLANILMAYACAĞI açıkça belirtilmiştir. Bölüm başlığında ve altındaki şekil yazısında 'Kümülatif Toplam' kullanılmıştır.
- **Öneri:** Başlığı '\subsection{Prefix Sums ve 2 Boyutlu Aralık Sorguları}' ve şekil başlığını '\caption{2 Boyutlu Prefix Sums ve İçerme-Dışarma}' olarak güncelleyiniz.

## [MAJOR] 36_cozumler_ve_ipuclari.tex:354 — factual (güven: high)
- **Alıntı:** include <stdio.h>
- **Sorun:** C kodu listing bloklarında önişlemci (preprocessor) yönergelerinin başındaki '#' karakterleri eksiktir (`include <stdio.h>` ve `define MAXN 1005`). Bu durum kodların derlenememesine ve sözdizimi hatasına yol açar.
- **Öneri:** Listing bloklarındaki `include <stdio.h>` ifadelerini `#include <stdio.h>`, `define MAXN 1005` ifadesini ise `#define MAXN 1005` olarak düzeltiniz.

## [MAJOR] 37_ekler.tex:118 — bad_reference (güven: high)
- **Alıntı:** \item \textbf{Bézout Özdeşliği ve Genişletilmiş Öklid (Bölüm 13 ve 16):}
- **Sorun:** Bézout Özdeşliği için Bölüm 16'ya atıf yapılmıştır. Bölüm 16 'Parite ve Simetri' konusunu işlemekte olup Bézout özdeşliği veya Genişletilmiş Öklid ile ilgisi yoktur; bu konu Bölüm 13 (EBOB ve EKOK) ve Bölüm 33'te ele alınmaktadır.
- **Öneri:** '(Bölüm 13 ve 16)' ifadesi '(Bölüm 13)' veya '(Bölüm 13 ve 33)' olarak düzeltilmelidir.

## [MINOR] 02_ispat_nasil_yapilir.tex:415 — notation_violation (güven: high)
- **Alıntı:** return n * faktoriyel(n - 1); // Ozyinelemeli adim
- **Sorun:** Terminoloji sözleşmesine göre 'özyineleme' terimi yasaklanmış olup 'rekürsiyon' (rekürsif) standardize edilmiştir.
- **Öneri:** return n * faktoriyel(n - 1); // Rekursif adim (indirgeme)

## [MINOR] 03_saymanin_temel_ilkeleri.tex:272 — math_error (güven: high)
- **Alıntı:** 2 Yazı'dan az içeren bitişler 7 tanedir ($TT$, $YTT$, $TYTT$, $YYTT$, $YTYTT$, $TYYTT$, $TYTYTT$)
- **Sorun:** Parantez içinde listelenen dizilimlerden 4 tanesi ($YYTT$, $YTYTT$, $TYYTT$, $TYTYTT$) tam olarak 2 Yazı içermektedir; dolayısıyla '2 Yazı'dan az' ifadesi bu elemanlarla çelişmektedir. Kastedilen '3 Yazı'dan az' (yani en fazla 2 Yazı içeren ve $TT$ ile biten) durumlardır.
- **Öneri:** '2 Yazı'dan az içeren bitişler 7 tanedir' yerine '3 Yazı'dan az (en fazla 2 Yazı) içeren bitişler 7 tanedir' veya '$TT$ ile biten (en fazla 2 Yazı içeren) durumlar 7 tanedir' yazılmalıdır.

## [MINOR] 05_kombinasyon.tex:224 — notation_violation (güven: high)
- **Alıntı:** Pascal bağıntısı $\binom{n}{r} = \binom{n-1}{r-1} + \binom{n-1}{r}$ doğal bir rekürsiyon (rekürsiyon) yapısı sunar.
- **Sorun:** Terminoloji sözleşmesinde B kategorisinde yer alan terimler için kural 'rekürsiyon (recursion)' şeklinde ilk geçişte İngilizce karşılığının parantez içinde verilmesidir. Metinde sehven 'rekürsiyon (rekürsiyon)' yazılmıştır.
- **Öneri:** 'rekürsiyon (rekürsiyon)' ifadesini 'rekürsiyon (recursion)' olarak düzeltiniz.

## [MINOR] 05_kombinasyon.tex:232 — notation_violation (güven: high)
- **Alıntı:** // Ozyinelemeli adim: Pascal kurali
- **Sorun:** Terminoloji sözleşmesine göre 'özyineleme' terimi yasaklanmış olup yerine 'rekürsiyon' / 'rekürsif' kullanımı zorunlu kılınmıştır.
- **Öneri:** Yorum satırını '// Rekursif adim: Pascal kurali' olarak güncelleyiniz.

## [MINOR] 07_guvercin_yuvasi_ilkesi.tex:315 — factual (güven: high)
- **Alıntı:** mükerrer elemanları systematically hesaba katan
- **Sorun:** Türkçe metin içerisinde İngilizce 'systematically' kelimesi sehven bırakılmıştır.
- **Öneri:** 'mükerrer elemanları sistematik olarak hesaba katan' şeklinde düzeltilmelidir.

## [MINOR] 08_icerme_disarma.tex:39 — bad_reference (güven: high)
- **Alıntı:** (Bölüm 11 ve 12'deki bölünebilme ilkeleri uyarınca)
- **Sorun:** Bölüm 8'de bulunulmasına rağmen, daha sonra gelecek olan Bölüm 11 (Bölünebilme) ve Bölüm 12'ye (Asal Sayılar) geçmiş zaman gibi atıf yapılmıştır. Kitap sözleşmesine göre ileriye yapılan atıflar açıkça gelecek zaman kipiyle ('Bölüm ...'de göreceğimiz üzere') verilmelidir.
- **Öneri:** "(Bölüm 11 ve 12'de göreceğimiz bölünebilme ilkeleri uyarınca)" şeklinde düzeltilmelidir.

## [MINOR] 08_icerme_disarma.tex:147 — bad_reference (güven: high)
- **Alıntı:** (Bölüm 13'te ele aldığımız EKOK tanımıyla)
- **Sorun:** Bölüm 8'de bulunulmasına rağmen, henüz işlenmemiş olan Bölüm 13'e (EBOB ve EKOK) sanki daha önce anlatılmış gibi 'ele aldığımız' şeklinde atıf yapılmıştır.
- **Öneri:** "(Bölüm 13'te göreceğimiz en küçük ortak kat / lcm tanımıyla)" şeklinde ileri referans kipine dönüştürülmelidir.

## [MINOR] 08_icerme_disarma.tex:147 — notation_violation (güven: high)
- **Alıntı:** \text{EKOK}(4, 6) = 12
- **Sorun:** Terminoloji ve notasyon sözleşmesinde EKOK gösterimi için '\operatorname{lcm}(a,b)' standart olarak belirlenmiştir. Metinde '\text{EKOK}' kullanılmıştır.
- **Öneri:** "\operatorname{lcm}(4, 6) = 12" olarak güncellenmeli ve bu örnekteki diğer \text{EKOK} kullanımları da \operatorname{lcm} yapılmalıdır.

## [MINOR] 08_icerme_disarma.tex:402 — notation_violation (güven: high)
- **Alıntı:** \textbf{bitmask} (bitmask) tekniği kullanılır.
- **Sorun:** Sözleşmenin A grubundaki terimlerde (İngilizce korunur) 'bitmask' yer almakta olup Türkçe karşılığı kullanılmaz. 'bitmask (bitmask)' yazımı gereksiz bir tekrar ve hatalı şablon kullanımıdır.
- **Öneri:** "\textbf{bitmask} tekniği kullanılır." şeklinde parantez içi tekrar kaldırılmalıdır.

## [MINOR] 09_izgara_yollari_ve_yineleme_iliskileri.tex:147 — factual (güven: high)
- **Alıntı:** define MOD 1000000007
- **Sorun:** C dilinde önişlemci makro tanımları '#' karakteri ile başlamalıdır. 'define MOD' ifadesi derleme hatasına yol açar.
- **Öneri:** #define MOD 1000000007

## [MINOR] 09_izgara_yollari_ve_yineleme_iliskileri.tex:344 — factual (güven: high)
- **Alıntı:** define MOD 1000000007
- **Sorun:** C dilinde önişlemci makro tanımları '#' karakteri ile başlamalıdır. 'define MOD' ifadesi derleme hatasına yol açar.
- **Öneri:** #define MOD 1000000007

## [MINOR] 10_cifte_sayim_ve_birebir_esleme.tex:146 — bad_reference (güven: high)
- **Alıntı:** Bölüm 11'deki bölünebilme tanımını hatırlarsak, $j$'nin her pozitif böleni $i$ için bir kez ziyaret edilir.
- **Sorun:** Bölüm 11 henüz işlenmemiştir; dolayısıyla 'hatırlarsak' ifadesiyle geriye dönük bir atıf yapılması yanlıştır. Sözleşme gereği henüz işlenmemiş bölümlere ileriye dönük referans verilmelidir.
- **Öneri:** 'Bölüm 11'de ayrıntılı göreceğimiz bölünebilme tanımı gereği, $j$'nin her pozitif böleni $i$ için...' şeklinde ileri referans olarak düzeltilmelidir.

## [MINOR] 11_bolunebilme.tex:182 — factual (güven: high)
- **Alıntı:** include <stdbool.h>
- **Sorun:** C kod bloğunda önişlemci direktifinin başındaki '#' karakteri unutulmuştur; 'include <stdbool.h>' geçerli bir C sözdizimi değildir.
- **Öneri:** #include <stdbool.h>

## [MINOR] 12_asal_sayilar.tex:418 — bad_reference (güven: high)
- **Alıntı:** Bölüm 16'da ele aldığımız parite kontrolü: $(x+y) + (x-y) = 2x$ (çift) olduğundan
- **Sorun:** Bölüm 16 (Parite ve Simetri) henüz işlenmemiş sonraki bir bölümdür; metinde ise sanki daha önce işlenmiş gibi geçmiş zaman ('ele aldığımız') kullanılmıştır.
- **Öneri:** 'Bölüm 16'da ayrıntılı göreceğimiz parite (teklik-çiftlik) özelliği:' veya doğrudan 'Parite (teklik-çiftlik) kontrolü:' şeklinde düzeltilmelidir.

## [MINOR] 13_ebob_ve_ekok.tex:244 — notation_violation (güven: high)
- **Alıntı:** /* Özyinelemeli (rekürsif) yöntem */
- **Sorun:** Terminoloji sözleşmesine göre 'özyineleme' terimi yasaklanmış olup 'rekürsiyon / rekürsif' kullanımı standardize edilmiştir.
- **Öneri:** Yorum satırını '/* Rekürsif yöntem */' şeklinde güncelleyiniz.

## [MINOR] 14_moduler_aritmetik.tex:115 — factual (güven: high)
- **Alıntı:** r = -17 MOD 5
- **Sorun:** Python dilinde mod alma işleci '%' sembolüdür; 'MOD' şeklinde bir operatör veya anahtar kelime Python sözdiziminde bulunmaz ve SyntaxError üretir. Metinde de Python'daki '%' işlecinin davranışından bahsedilmektedir.
- **Öneri:** r = -17 % 5  # r degeri 3 cikar

## [MINOR] 15_taban_aritmetigi.tex:361 — notation_violation (güven: high)
- **Alıntı:** Bit Düzeyinde İşlemler (Bitwise Operators):
- **Sorun:** Terminoloji sözleşmesine göre 'bitwise' terimi İngilizce olarak korunmalı, 'bit düzeyinde' karşılığı kullanılmamalıdır (A Grubu: İngilizce korunur / ❌ Kullanılmayacak Türkçe: bit düzeyinde).
- **Öneri:** "Bit Düzeyinde İşlemler (Bitwise Operators):" yerine "Bitwise İşlemler:" veya "Bitwise Operatörler:" ifadesi kullanılmalıdır.

## [MINOR] 16_parite_ve_simetri.tex:344 — math_error (güven: high)
- **Alıntı:** simetri ekseninden dışa doğru Bölüm 21'de inceleyeceğimiz two pointers tekniğiyle kontrol eder:
- **Sorun:** Metindeki açıklama kodun işleyiş yönüyle çelişmektedir. Kod simetri ekseninden dışa doğru değil; dizginin iki ucundan merkeze doğru ('sol = 0', 'sag = n - 1', 'sol++', 'sag--') yani dıştan içe doğru çalışmaktadır.
- **Öneri:** 'simetri ekseninden dışa doğru' ifadesi 'dizginin iki ucundan merkeze doğru' olarak düzeltilmelidir.

## [MINOR] 16_parite_ve_simetri.tex:351 — notation_violation (güven: high)
- **Alıntı:** // Iki isaretci ile simetri kontrolu: O(n) zaman, O(1) ekstra alan
- **Sorun:** Terminoloji sözleşmesine göre 'two pointers' terimi İngilizce korunmalıdır; Türkçe karşılığı olan 'iki işaretçi' teriminin kullanılması Kategori A kapsamında yasaktır.
- **Öneri:** Yorum satırı '// Two pointers ile simetri kontrolu: O(n) zaman, O(1) ekstra alan' şeklinde güncellenmelidir.

## [MINOR] 19_algoritma_nedir.tex:385 — factual (güven: high)
- **Alıntı:** include <stdio.h>
- **Sorun:** C dilinde standart kütüphane başlık dosyasını dahil etmek için önişlemci yönergesi başında diyez işareti bulunmalıdır (`#include <stdio.h>`). `#` karakteri eksik bırakılmıştır.
- **Öneri:** #include <stdio.h>

## [MINOR] 20_karmasiklik_ve_bigo.tex:223 — bad_reference (güven: high)
- **Alıntı:** Bu analiz, Bölüm 12'de göreceğimiz Eratosthenes kalburunun karmaşıklık hesabının da temelini oluşturur.
- **Sorun:** Bölüm 12 (Asal Sayılar) kitabın akışında Bölüm 20'den önce yer almaktadır; bu nedenle 'göreceğimiz' ifadesi zamanlama ve referans açısından hatalıdır.
- **Öneri:** 'Bu analiz, Bölüm 12'de gördüğümüz Eratosthenes kalburunun karmaşıklık hesabının da temelini oluşturur.' şeklinde düzeltilmelidir.

## [MINOR] 20_karmasiklik_ve_bigo.tex:328 — notation_violation (güven: high)
- **Alıntı:** çağırdığınız rekürsif (rekürsif) fonksiyonlar da bellek tüketir.
- **Sorun:** Parantez içi açıklama yanlışlıkla terimin kendisini tekrarlamıştır ('rekürsif (rekürsif)'). Terminoloji sözleşmesine göre terim ya doğrudan 'rekürsif' olarak kullanılmalı ya da ilk geçişte İngilizce karşılığıyla 'rekürsif (recursive)' olarak verilmelidir.
- **Öneri:** 'çağırdığınız rekürsif fonksiyonlar da bellek tüketir.' veya 'çağırdığınız rekürsif (recursive) fonksiyonlar da bellek tüketir.' olarak düzeltilmelidir.

## [MINOR] 21_diziler_ve_temel_teknikler.tex:5 — factual (güven: high)
- **Alıntı:** \emph{prefix sums} (\emph{prefix sums}) ve \emph{two pointers} (\emph{two pointers})
- **Sorun:** Kavramlar tanıtılırken terimler parantez içinde gereksizce ötelenmeden aynen yinelenmiştir ('prefix sums (prefix sums)' ve 'two pointers (two pointers)').
- **Öneri:** Cümle '\emph{prefix sums} ve \emph{two pointers}' şeklinde sadeleştirilmelidir.

## [MINOR] 21_diziler_ve_temel_teknikler.tex:50 — bad_reference (güven: high)
- **Alıntı:** Bu işlem, Bölüm 17'de incelediğimiz \emph{yarı-değişmez} (\emph{monovariant}) mantığını taşır: $k$'ıncı adım tamamlandığında, elimizdeki değer $A[0 \dots k]$ alt dizisinin en büyük değeridir.
- **Sorun:** 'k. adımda elimizdeki değer A[0..k]'nın en büyüğüdür' ifadesi bir yarı-değişmez (monovariant) değil, döngü adımları boyunca korunan bir döngü değişmezidir (loop invariant). Döngü değişmezleri Bölüm 17'de değil, Bölüm 19'da ele alınmıştır.
- **Öneri:** İfade 'Bölüm 19'da incelediğimiz döngü değişmezi (loop invariant) mantığını taşır' olarak düzeltilmelidir.

## [MINOR] 21_diziler_ve_temel_teknikler.tex:175 — math_error (güven: high)
- **Alıntı:** kaç tane \texttt{\$1\$} olduğunu
- **Sorun:** \texttt{\$1\$} yazımı LaTeX çıktısında daktilo yazı tipinde doğrudan '$1$' (dolar simgeleri görünür biçimde) basılmasına neden olur.
- **Öneri:** '\texttt{\$1\$}' yerine '$1$' veya '\texttt{1}' yazılmalıdır.

## [MINOR] 21_diziler_ve_temel_teknikler.tex:181 — notation_violation (güven: high)
- **Alıntı:** dizinin prefix sumını aldığımızda
- **Sorun:** Terminoloji sözleşmesine göre İngilizce teknik terimlere gelen Türkçe ekler apostrofla bağlanmalıdır ('prefix sum'ın', 'prefix sums'ın'). 'prefix sumını' ve 229. satırdaki 'prefix sumı' yazımlarında ekler doğrudan yapıştırılmıştır.
- **Öneri:** 'prefix sum'ını' ve 'prefix sum'ı' şeklinde apostrof eklenmelidir.

## [MINOR] 22_siralama.tex:37 — notation_violation (güven: high)
- **Alıntı:** \textbf{Açgözlü (Greedy) Stratejiler:}
- **Sorun:** Terminoloji sözleşmesine göre 'greedy' terimi İngilizce korunmalı, Türkçe karşılığı olan 'açgözlü' kesinlikle kullanılmamalıdır (Kategori A: Türkçe karşılığı KULLANILMAZ).
- **Öneri:** \textbf{Greedy Stratejiler:}

## [MINOR] 23_ikili_arama.tex:302 — factual (güven: high)
- **Alıntı:** include <stdio.h>
- **Sorun:** C dilinde önişlemci yönergesi eksik yazılmıştır; 'include <stdio.h>' yerine '#include <stdio.h>' olmalıdır.
- **Öneri:** #include <stdio.h>

## [MINOR] 24_temel_veri_yapilari.tex:235 — math_error (güven: high)
- **Alıntı:** Her eleman toplamda en fazla 3 yığın işlemine tabi tutulur.
- **Sorun:** İki stack ile queue simülasyonunda bir eleman: 1) Y1'e push, 2) Y1'den pop, 3) Y2'ye push, 4) Y2'den pop olmak üzere toplamda en fazla 4 stack işlemine tabi tutulur. Y1'den Y2'ye aktarım tek bir işlem değil, bir pop ve bir push olmak üzere iki işlemdir.
- **Öneri:** "en fazla 3 yığın işlemine" ifadesi "en fazla 4 stack işlemine (2 push, 2 pop)" olarak düzeltilmelidir.

## [MINOR] 24_temel_veri_yapilari.tex:254 — notation_violation (güven: high)
- **Alıntı:** çift uçlu kuyruk (\texttt{deque})
- **Sorun:** Terminoloji sözleşmesi Kategori A uyarınca "deque" terimi İngilizce korunmalı, Türkçe karşılığı ("iki uçlu kuyruk" veya "çift uçlu kuyruk") kullanılmamalıdır.
- **Öneri:** "çift uçlu kuyruk (\texttt{deque})" yerine doğrudan "\texttt{deque}" kullanılmalıdır.

## [MINOR] 24_temel_veri_yapilari.tex:309 — notation_violation (güven: high)
- **Alıntı:** Karma Tablosu (Hash Table)
- **Sorun:** Terminoloji sözleşmesinde "karma tablosu" terimi Kategori A'da (Kullanılmayacak Türkçe) açıkça listelenmiştir; terimin "hash table" olarak korunması gerekmektedir.
- **Öneri:** "Karma Tablosu (Hash Table)" yerine doğrudan "Hash Table" yazılmalıdır.

## [MINOR] 25_rekursiyon_ve_dp.tex:5 — notation_violation (güven: high)
- **Alıntı:** \textbf{rekürsiyon (rekürsiyon)}
- **Sorun:** Terminoloji sözleşmesine göre rekürsiyon terimi ilk geçtiğinde İngilizce karşılığı parantez içinde verilmelidir: 'rekürsiyon (recursion)'. Metinde sehven 'rekürsiyon (rekürsiyon)' yazılmıştır.
- **Öneri:** \textbf{rekürsiyon (recursion)} olarak düzeltilmelidir.

## [MINOR] 25_rekursiyon_ve_dp.tex:5 — notation_violation (güven: high)
- **Alıntı:** \textbf{memoization (bellekleme)}
- **Sorun:** Terminoloji sözleşmesinde memoization terimi Kategori A (İngilizce korunur, Türkçe karşılığı KULLANILMAZ) altındadır. 'belleklenmiş arama, belleklenme, bellekleme' gibi Türkçe karşılıkların kullanılması yasaktır; doğrudan 'memoization' kullanılmalıdır.
- **Öneri:** '\textbf{memoization (bellekleme)}' yerine yalnızca '\textbf{memoization}' yazılmalıdır (aynı durum Tanım 2'deki tanım başlığında da düzeltilmelidir).

## [MINOR] 26_greedy_yaklasimi.tex:264 — notation_violation (güven: high)
- **Alıntı:** grafın \textbf{tüm} minimum kapsayan ağaçlarında yer almak zorundadır.
- **Sorun:** Terminoloji sözleşmesinde 'MST (minimum spanning tree)' ve 'spanning tree' terimlerinin İngilizce olarak korunması gerektiği belirtilmiştir. Metinde 'minimum kapsayan ağaç' ve 'kapsayan ağaç' terimleri kullanılmıştır.
- **Öneri:** 'minimum kapsayan ağaçlarında' yerine 'MST'lerinde' (ve ilgili yerlerde 'spanning tree' / 'MST') ifadesi kullanılmalıdır.

## [MINOR] 27_graflar_ve_arama.tex:344 — logic_gap (güven: high)
- **Alıntı:** \textbf{zorundadır}. \textbf{zorundadır}.
- **Sorun:** Teorem metninin sonunda 'zorundadır' ifadesi mükerrer basılmıştır.
- **Öneri:** Mükerrer olan ikinci '\textbf{zorundadır}.' ifadesi silinmelidir.

## [MINOR] 29_donguler_ve_fonksiyonlar.tex:338 — notation_violation (güven: high)
- **Alıntı:** \subsubsection{3. Gösterici ile Dinamik Yapıların Güncellenmesi}
- **Sorun:** Kitap terminoloji sözleşmesine göre C dilindeki bu kavram için 'işaretçi (pointer)' terimi standardize edilmiştir; 'gösterici' terimi kullanılmamalıdır.
- **Öneri:** \subsubsection{3. İşaretçi ile Dinamik Yapıların Güncellenmesi} veya doğrudan konu kapsamına uygun bir başlık ile değiştirilmelidir.

## [MINOR] 30_diziler_stringler_ve_pointer.tex:147 — factual (güven: high)
- **Alıntı:** include <stdio.h>
- **Sorun:** C programlama dilinde standart kütüphane başlık dosyaları '#include <stdio.h>' önişlemci yönergesi ile dahil edilir. Kod parçalarında başındaki '#' (diyez) karakteri eksik bırakılmıştır (kod bloklarında 'include <stdio.h>' olarak yazılmıştır).
- **Öneri:** Kod bloklarındaki 'include <stdio.h>' ifadelerini '#include <stdio.h>' olarak düzeltiniz.

## [MINOR] 31_bitwise_ve_struct.tex:218 — factual (güven: high)
- **Alıntı:** include <math.h>
- **Sorun:** C önişlemci yönergesi olan '#include' ifadesindeki '#' karakteri eksiktir; doğrudan 'include <math.h>' yazılmıştır.
- **Öneri:** #include <math.h> olarak düzeltilmelidir.

## [MINOR] 31_bitwise_ve_struct.tex:253 — factual (güven: high)
- **Alıntı:** include <stdio.h>
- **Sorun:** C önişlemci yönergesi olan '#include' ifadesindeki '#' karakteri eksiktir; doğrudan 'include <stdio.h>' yazılmıştır.
- **Öneri:** #include <stdio.h> olarak düzeltilmelidir.

## [MINOR] 31_bitwise_ve_struct.tex:293 — factual (güven: high)
- **Alıntı:** include <stdio.h>
- **Sorun:** C önişlemci yönergesi olan '#include' ifadesindeki '#' karakteri eksiktir; doğrudan 'include <stdio.h>' yazılmıştır.
- **Öneri:** #include <stdio.h> olarak düzeltilmelidir.

## [MINOR] 33_alistirmalar_sayilar_teknikler.tex:438 — factual (güven: high)
- **Alıntı:** include <stdio.h>
- **Sorun:** C kodunda önişlemci direktifi eksik yazılmıştır; başında '#' işareti olmadan 'include <stdio.h>' derleme hatasına yol açar.
- **Öneri:** #include <stdio.h>

## [MINOR] 35_karma_cozumlu_problemler.tex:0 — notation_violation (güven: high)
- **Alıntı:** Mod $n$'de aynı değere sahip iki farklı prefix sumın varlığı garanti midir?
- **Sorun:** Terminoloji sözleşmesine göre İngilizce teknik terimlere Türkçe ekler yapıştırılmamalı, apostrofla bağlanmalıdır ('prefix sums'ın'). Metindeki 'prefix sumın' ve birkaç satır sonraki 'prefix sumı' kullanımları apostrof kuralına aykırıdır.
- **Öneri:** 'prefix sumın' yerine 'prefix sums'ın' (veya 'prefix sum'ın'), 'prefix sumı' yerine 'prefix sums'ı' yazılmalıdır.

## [MINOR] 35_karma_cozumlu_problemler.tex:0 — notation_violation (güven: high)
- **Alıntı:** \emph{deranjman} (düzensiz permütasyon)
- **Sorun:** Terminoloji sözleşmesi Tablo B'de bu kavram 'düzensiz dizilim (derangement)' olarak tekleştirilmiştir. 'deranjman (düzensiz permütasyon)' kullanımı sözleşmeye uygun değildir.
- **Öneri:** 'düzensiz dizilim (derangement)' terimi kullanılmalıdır.

## [MINOR] 35_karma_cozumlu_problemler.tex:0 — logic_gap (güven: medium)
- **Alıntı:** Aranan medyan eleman, $f(X) \ge \frac{N^2 + 1}{2}$ koşulunu sağlayan en küçük $X$'tir.
- **Sorun:** Problem 7'nin girişinde medyan, 'kendisinden küçük veya eşit eleman sayısı en az $\lceil N^2 / 2 \rceil$ olan en küçük değer' olarak tanımlanmıştır. $N$ çift olduğunda $\frac{N^2+1}{2}$ bir tam sayı değildir (örneğin $N=4$ için $8.5$). Tavan/taban fonksiyonu kullanılmadan kesirli ifade bırakılması tanımsal tutarsızlığa yol açmaktadır.
- **Öneri:** İfade, problem girişindeki tanım ve C kodundaki tam sayı bölmesiyle (`(N * N + 1) / 2`) uyumlu olarak $f(X) \ge \lceil N^2 / 2 \rceil$ veya $f(X) \ge \lfloor \frac{N^2 + 1}{2} \rfloor$ şeklinde yazılmalıdır.

## [MINOR] 35_karma_cozumlu_problemler.tex:0 — factual (güven: high)
- **Alıntı:** include <stdio.h>
- **Sorun:** Problem 2, Problem 3, Problem 5 ve Problem 7'de yer alan C kod bloklarında preprocessor direktiflerinin başındaki '#' karakteri eksiktir ('include <stdio.h>', 'define INF ...'). Bu durum kodun C standartlarına göre derlenmesini engeller.
- **Öneri:** Tüm 'include <stdio.h>' satırları '#include <stdio.h>', 'include <stdlib.h>' satırları '#include <stdlib.h>' ve 'define INF ...' satırı '#define INF ...' olarak düzeltilmelidir.

## [MINOR] 36_cozumler_ve_ipuclari.tex:521 — notation_violation (güven: high)
- **Alıntı:** rekürsif (rekürsif) C fonksiyonunu yazınız.
- **Sorun:** Sözleşmeye göre terim ilk geçtiğinde İngilizce karşılığı verilir ('rekürsif (recursive)' veya 'rekürsiyon (recursion)'); burada sehven parantez içine de aynı Türkçe kelime yazılarak 'rekürsif (rekürsif)' denmiştir.
- **Öneri:** 'rekürsif (recursive) C fonksiyonunu yazınız.' veya doğrudan 'rekürsif C fonksiyonunu yazınız.' olarak düzeltiniz.

## [MINOR] 37_ekler.tex:167 — factual (güven: high)
- **Alıntı:** \item \textbf{Düzlemsel Graflar için Euler Formülü:}
- **Sorun:** Bölüm girişinde (satır 7) 'Bu eklerde yalnızca kitapta anlatılan kavramlara yer verilmiştir' denmesine karşın, düzlemsel graflar (planar graphs) ve Euler formülü ($V - E + F = 2$) kitabın Bölüm 27 dahil hiçbir bölümünde tanımlanmamış ve işlenmemiştir.
- **Öneri:** Düzlemsel graflar kitap kapsamına dahil edilmeyecekse bu madde formül listesinden çıkarılmalı veya kitapta açıklandığı bir bölüme referans verilmelidir.

## [MINOR] 37_ekler.tex:206 — notation_violation (güven: high)
- **Alıntı:** derinlik öncelikli arama & depth-first search (DFS) \\
- **Sorun:** Terminoloji sözleşmesi Kategori A uyarınca 'derin öncelikli arama' Türkçe karşılık olarak tek başına kullanılmaz; doğru standart kullanım 'DFS (derinlik öncelikli arama)' veya doğrudan 'DFS'tir. Benzer şekilde satır 213'teki 'genişlik öncelikli arama' yerine 'BFS (genişlik öncelikli arama)' esastır.
- **Öneri:** Türkçe Terim sütunundaki ilgili satırlar sözleşmedeki standart olan 'DFS (derinlik öncelikli arama)' ve 'BFS (genişlik öncelikli arama)' biçimine getirilmelidir.

## [MINOR] 37_ekler.tex:249 — factual (güven: high)
- **Alıntı:** Kitapta anlatılmayan yapılar (binary search tree, bipartite graph, LCA, monoton kuyruk, segment tree, bit manipulation, brute-force, divide and conquer, combinatorial proof, Euler totient, in-degree/out-degree, time/space complexity gibi ayrı başlıklar) bu tabloya alınmamıştır.
- **Sorun:** Parantez içinde 'kitapta anlatılmayan yapılar' olarak listelenen kavramlardan bipartite graph (Bölüm 27'de 'İki Kümeli Graf / Bipartite'), divide and conquer (Bölüm 22'de 'Böl-ve-Fethet') ve combinatorial proof (Bölüm 6 ve 10'da 'Kombinatorik İspat') kitapta doğrudan işlenmiştir. Bu kavramların anlatılmadığının iddia edilmesi olgusal hatadır.
- **Öneri:** 'bipartite graph', 'divide and conquer' ve 'combinatorial proof' terimleri kitapta anlatılmayanlar listesinden çıkarılmalıdır.

## [MEDIUM] 13_ebob_ve_ekok.tex:454 — logic_gap (güven: medium)
- **Alıntı:** Bu inceleme bize, buradaki çözümün ikilinin yalnızca yer değiştirmesi durumuna dayandığını gösterir.
- **Sorun:** Örnekte 'c'nin alabileceği değerler hakkında ne söylenebilir?' diye sorulup çözümde sadece c = b - a durumunda kümenin {a+c, b-c} = {b, a} olarak korunduğu gösterilmiştir. Başka c değerlerinin mümkün olup olmadığı tartışılmamış, ancak çözüm sanki tek durum buymuş gibi kesin bir dille genelleme yapmıştır.
- **Öneri:** Soruyu 'b > a olmak üzere c = b - a seçiminin eşitliği sağladığını gösteriniz' şeklinde netleştiriniz veya genel durumda (a+c) + (b-c) = a+b toplamı korunduğundan {a+c, b-c} = {a, b} olmasının yeterli olduğunu, ancak genel bölen çiftleri için başka çözümlerin de araştırılabileceğini belirterek mantıksal iddiayı sınırlandırınız.
