from django import forms

from category.models import Category
from product.models import Product

IS_PUBLISHED_STATUS = (('', '-----'), ('0', '非公開'), ('1', '公開'))


class ProductInputForm(forms.Form):
    """ 商品登録・編集 フォーム（スタッフ）"""
    name = forms.CharField(
        label='商品名',
        max_length=255,
        required=True,
    )
    price = forms.IntegerField(
        label='販売価格',
        required=True,
    )
    category = forms.ModelChoiceField(
        label='カテゴリー',
        queryset=Category.objects.filter(is_deleted=False),
        required=True,
        empty_label='-----'
    )
    is_published = forms.IntegerField(
        label='公開ステータス',
        required=True,
    )
    image = forms.ImageField(
        label='商品画像',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id', None)
        super(ProductInputForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        name = data.get('name')
        price = data.get('price')
        category = data.get('category')
        product_id = self.product_id
        # 重複チェック
        if name and price and category and product_id:
            qs = Product.objects.filter(
                name=name,
                price=price,
                category=category,
                is_deleted=False
            ).exclude(id=product_id).exists()
            if qs:
                self.add_error('name', 'この情報は既に登録されています')
        return data


class ProductSearchForm(forms.Form):
    """ 商品一覧検索フォーム （スタッフ）"""
    name = forms.CharField(
        label='商品名',
        max_length=255,
        required=False,
    )
    price_from = forms.IntegerField(
        label='販売価格',
        min_value=0,
        required=False,
    )
    price_to = forms.IntegerField(
        label='販売価格',
        min_value=0,
        required=False,
    )
    category = forms.ModelChoiceField(
        label='カテゴリー',
        queryset=Category.objects.filter(is_deleted=False),
        empty_label='-----',
        required=False,
    )
    is_published = forms.ChoiceField(
        label='公開ステータス',
        choices=IS_PUBLISHED_STATUS,
        required=False,
    )


class QtyForm(forms.Form):
    """ ユーザの商品詳細画面で注文できる数量をチェックする"""
    qty = forms.IntegerField(
        label='数量',
        min_value=1,
        max_value=100,
        required=True,
        error_messages={'max_value': '100 以下で入力してください'}
    )
    product_id = forms.IntegerField(
        label='商品id',
        required=True
    )
    # TODO 在庫数を見て入力できる数量を制御する
    # max_value=在庫数
    # 在庫数より多い数量を入力された場合にエラーメッセージを表示する
