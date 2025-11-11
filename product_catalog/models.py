from django.db import models
from django.utils import timezone


# =======================================================
# MODEL 1: PRODUCT (Tabel Produk)
# =======================================================
class Product(models.Model):
    # Field Teks Dasar
    name = models.CharField(max_length=255, verbose_name="Nama Produk")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi Detail")

    # Field Angka (Harga)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Harga (Rp)")

    # Field Pilihan (Category)
    CATEGORY_CHOICES = [
        ('Pashmina', 'Pashmina'),
        ('Jilbab Segi Empat', 'Jilbab Segi Empat'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Kategori")

    # Field URL untuk Gambar
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL Gambar")

    # Status dan Tag
    is_new_arrival = models.BooleanField(default=False, verbose_name="Produk Baru?")
    tag = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tag (Contoh: Sale, Best Seller)")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Dibuat")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Produk"
        verbose_name_plural = "Produk"

    def __str__(self):
        return self.name


# =======================================================
# MODEL 2: PROMOTION (Tabel Promosi)
# =======================================================
class Promotion(models.Model):
    title = models.CharField(max_length=100, verbose_name="Judul Promo")
    tagline = models.CharField(max_length=255, verbose_name="Tagline Kecil")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi Singkat Promo")

    # Pengaturan waktu promo
    start_date = models.DateField(default=timezone.now, verbose_name="Tanggal Mulai Promo")
    end_date = models.DateField(default=timezone.now, verbose_name="Tanggal Berakhir Promo")

    is_active = models.BooleanField(default=True, verbose_name="Aktif (Tampilkan di website)")

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Promo"
        verbose_name_plural = "Promosi"

    def __str__(self):
        return self.title