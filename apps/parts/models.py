from django.db import models
from django.shortcuts import get_object_or_404
from unidecode import unidecode

# Create your models here.

class Category(models.Model):
    """
    This Category model (phân loại) is used to indicate the category of a 
    particular motorbike part

    For example:
        product: Nhớt Castrol Power ga 1 lít
                category: Nhớt
        ----------------
        product: Lốp 250 Casumina
                category: Lốp
        ----------------
        product: buri Thái
                category: Linh kiện khác
    """
    name_vn = models.CharField(verbose_name='tên', blank=False, max_length=200, default='', unique=True)
    name_en = models.CharField(verbose_name='tên tiếng anh', blank=True, max_length=200, null=False, unique=True)

    def __str__(self):
        return "{}".format(self.name_vn)
    
    def save(self, *args, **kwargs):

        self.name_vn = self.name_vn.lower() if self.name_vn else ''
        self.name_en = unidecode(self.name_en).lower() if self.name_en else ''

        if self.name_vn and not self.name_en:
            self.name_en = unidecode(self.name_vn)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Phân loại"
        verbose_name_plural = "Phân loại"



class Company(models.Model):
    """
    This Comapny model (công ty, nhà cung cấp) is used to store information about the 
    companies or manufactories where the products are produced.

    For example: product bố thắng sau Sirius hàng Katema (công ty sản xuất là Katema)
    """

    name_vn = models.CharField(verbose_name='tên', max_length=200, default='', unique=True)
    name_en = models.CharField(verbose_name='tên tiếng anh', blank=True, max_length=200, null=False, unique=True)

    def __str__(self):
        return "{}".format(self.name_vn)
    
    def save(self, *args, **kwargs):
        """
        Before saving the Company model, 2 main tasks must be accomplished:
            
            Set lower for name_vn (and name_en if blank)
            ------------------
            If the name_en is not provided, use the name_vn instead 
            (special characters removed)
        """

        self.name_vn = self.name_vn.lower() if self.name_vn else ''
        self.name_en = unidecode(self.name_en).lower() if self.name_en else ''

        if self.name_vn and not self.name_en:
            self.name_en = unidecode(self.name_vn)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Công ty"
        verbose_name_plural = "Công ty"



class MotorbikePart(models.Model):
    """
    This model stores all necessary information about a part
    """
    barcode         = models.CharField(verbose_name='mã vạch', blank=False, null=False, unique=True, max_length=50)
    name_vn         = models.CharField(verbose_name='tên sản phẩm', blank=False, null=False, max_length=200)
    name_en         = models.CharField(verbose_name='tên tiếng anh', blank=True, null=False, max_length=200)
    description     = models.TextField(verbose_name='miêu tả', blank=True, default='')
    image           = models.ImageField(verbose_name='hình ảnh', blank=True, null=True)
    price_import    = models.PositiveBigIntegerField(verbose_name='giá nhập', blank=False, default=0)
    price_customer  = models.PositiveBigIntegerField(verbose_name='giá khách', blank=True, default=0)
    price_engineer  = models.PositiveBigIntegerField(verbose_name='giá thợ', blank=True, default=0)
    price_store     = models.PositiveBigIntegerField(verbose_name='giá sỉ', blank=True, default=0)
    category        = models.ForeignKey(
        Category, 
        verbose_name=("phân loại"),
        on_delete=models.DO_NOTHING, 
        blank=True,
        null=False
    )
    company         = models.ForeignKey(
        Company, 
        verbose_name=("công ty"), 
        on_delete=models.DO_NOTHING,
        blank=True,
        null=False
    )

    def __str__(self):
        return "{} {}".format(self.name_vn, self.barcode)
    
    def save(self, *args, **kwargs):
        """
        Before saving the MotorbikePart model, 4 main tasks must be accomplished:
            
            Set lower for name_vn (and name_en if blank)
            ------------------
            If the name_en is not provided, use the name_vn instead 
            (special characters removed)
            ------------------
            If company and category are not provided, set these fields to default values
            ------------------
            If the price_store, price_engineer, and price_customer are not provided:
                price_store = price_import + 10%
                price_engineer = price_engineer + 20%
                price_customer = price_import + 30%
        """

        self.name_vn = self.name_vn.lower() if self.name_vn else ''
        self.name_en = unidecode(self.name_en).lower() if self.name_en else ''

        if self.name_vn and not self.name_en:
            self.name_en = unidecode(self.name_vn)

        if not self.company_id:
            company = Company.objects.filter(pk=1).first()
            if not company:
                raise Company.DoesNotExist("Did you forget to loaddata before running project?")
            self.company_id = company.pk
        
        if not self.category_id:
            category = Category.objects.filter(pk=1).first()
            if not category:
                raise Category.DoesNotExist("Did you forget to loaddata before running project?")
            self.category = category

        if not self.price_store:
            self.price_store = int(self.price_import * 0.1 * self.price_import)

        if not self.price_engineer:
            self.price_engineer = int(self.price_import + 0.2 * self.price_import)

        if not self.price_customer:
            self.price_customer = int(self.price_import + 0.3 * self.price_import)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Phụ tùng"
        verbose_name_plural = "Phụ tùng xe máy"

        indexes = [
            models.Index(fields=['barcode']),
            models.Index(fields=['name_vn']),
            models.Index(fields=['name_en'])
        ]

        constraints = [
            models.CheckConstraint(
                check=models.Q(price_import__lte=models.F('price_store')), 
                name='price_import_lte_price_store'
            ),
            models.CheckConstraint(
                check=models.Q(price_store__lte=models.F('price_engineer')), 
                name='price_store_lte_price_engineer'
            ),
            models.CheckConstraint(
                check=models.Q(price_engineer__lte=models.F('price_customer')), 
                name='price_engineer_lte_price_customer'
            )
        ]
