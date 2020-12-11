from django.db import models


class LargeCategory(models.Model):
    """大カテゴリ"""
    id = models.AutoField(verbose_name='ID', primary_key=True)
    category = models.CharField(verbose_name='大カテゴリ', max_length=30)

    def __str__(self):
        return self.category

    class Meta:
        managed = False
        db_table = 'largeCategory'
        verbose_name_plural = '大カテゴリ'


class SmallCategory(models.Model):
    """小カテゴリ"""
    id = models.AutoField(verbose_name='ID', primary_key=True)
    category = models.CharField(verbose_name='小カテゴリ', max_length=40)

    def __str__(self):
        return self.category

    class Meta:
        managed = False
        db_table = 'smallCategory'
        verbose_name_plural = '小カテゴリ'


class Crew(models.Model):
    """社員"""
    id = models.AutoField(verbose_name='社員ID', primary_key=True)
    crew_num = models.CharField(verbose_name='社員番号', max_length=6)
    name = models.CharField(verbose_name='氏名', max_length=15)
    kana = models.CharField(verbose_name='しめい', max_length=30)
    enter_date = models.DateField(verbose_name='入社日')
    position = models.CharField(verbose_name='役職', max_length=10)
    mail = models.EmailField(verbose_name='メールアドレス', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'crew'
        verbose_name_plural = '社員'


class Book(models.Model):
    """書籍"""
    id = models.AutoField(verbose_name='ID', primary_key=True)
    name = models.CharField(verbose_name='書籍名', max_length=100)
    author = models.CharField(verbose_name='著者', max_length=100, blank=True, null=True)
    issue_date = models.DateField(verbose_name='発行日')
    purchase_date = models.DateField(verbose_name='最終購入日', blank=True, null=True)
    all_stock = models.IntegerField(verbose_name='在庫', default='1')
    last_stock = models.IntegerField(verbose_name='レンタル可能数', default='1')
#    large_id = models.CharField(verbose_name='大カテゴリ', max_length=20, blank=True, null=True)
#    small_id = models.CharField(verbose_name='小カテゴリ', max_length=20, blank=True, null=True)
    large_id = models.ForeignKey(LargeCategory, verbose_name='大カテゴリ', db_column='large_id', on_delete=models.CASCADE)
    small_id = models.ForeignKey(SmallCategory, verbose_name='小カテゴリ', db_column='small_id', on_delete=models.CASCADE)
    disposal_status = models.CharField(verbose_name='廃棄',  max_length=10, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        db_table = 'book'
        verbose_name_plural = '書籍'


class Rental(models.Model):
    """レンタル"""
    id = models.AutoField(verbose_name='ID', primary_key=True)
    crew_id = models.ForeignKey(Crew, verbose_name='社員名', db_column='crew_id', on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, verbose_name='書籍名', db_column='book_id', on_delete=models.CASCADE)
    reservation_date = models.DateField(verbose_name='レンタル申請日')
    rental_date = models.DateField(verbose_name='レンタル日')
    return_date = models.DateField(verbose_name='返却日')

    class Meta:
        managed = False
        db_table = 'rental'
        verbose_name_plural = 'レンタル'


class Disposal(models.Model):
    """廃棄"""
    id = models.AutoField(verbose_name='ID', primary_key=True)
    book_id = models.ForeignKey(Book, verbose_name='本', db_column='book_id', on_delete=models.CASCADE)
    disposal_date = models.DateField(verbose_name='廃棄日', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disposal'
        verbose_name_plural = '廃棄'


class BookOrder(models.Model):
    """注文"""
    id = models.AutoField(verbose_name='ID', primary_key=True)
    crew_id = models.ForeignKey(Crew, verbose_name='社員名', db_column='crew_id', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='書籍名', max_length=100)
    author = models.CharField(verbose_name='著者', max_length=100)
    order_date = models.DateField(verbose_name='注文日')
    issue_date = models.DateField(verbose_name='発行日', blank=True, null=True)
    order_quantity = models.IntegerField(verbose_name='注文数', default='1')
    large_id = models.ForeignKey(LargeCategory, verbose_name='大カテゴリ', db_column='large_id', on_delete=models.CASCADE)
    small_id = models.ForeignKey(SmallCategory, verbose_name='小カテゴリ', db_column='small_id', on_delete=models.CASCADE)
    book_url = models.TextField(verbose_name='URL')

    class Meta:
        managed = False
        db_table = 'bookOrder'
        verbose_name_plural = '注文'


class Review(models.Model):
    """レビュー"""
    id = models.AutoField(verbose_name='ID', primary_key=True)
    crew_id = models.ForeignKey(Crew, verbose_name='社員名', db_column='crew_id', blank=True,
                                null=True, on_delete=models.SET_DEFAULT, default='')
    book_id = models.ForeignKey(Book, verbose_name='書籍名', db_column='book_id',
                                on_delete=models.CASCADE)
    evaluation = models.IntegerField(verbose_name='10段階評価')
    review = models.TextField(verbose_name='レビュー', max_length=255)

    class Meta:
        managed = False
        db_table = 'review'
        verbose_name_plural = 'レビュー'
