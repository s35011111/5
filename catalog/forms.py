from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description','category', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter product description...'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name...'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),

        }
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'category':'Category',
            'price': 'Price',
            'image': 'Product Image',

        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        standart_attr={'style':'width: 700px', 'class':'form-field'}
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.NumberInput)):
                field.widget.attrs.update(standart_attr)

    def clean_name(self):
        name = self.cleaned_data['name']
        if self._contains_prohibited_words(name):
            raise forms.ValidationError('Product name contains prohibited words.')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if self._contains_prohibited_words(description):
            raise forms.ValidationError('Description contains prohibited words.')
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be positive.')
        return price


    def _contains_prohibited_words(self, text):
        prohibited_words = ["казино",    "криптовалюта",    "крипта",    "биржа",    "дешево",
                            "бесплатно",    "обман",    "полиция",    "радар"]
        text_lower = text.lower()
        return any(prohibited_word in text_lower for prohibited_word in prohibited_words)


class ProductModeratorForm(ProductForm):
    class Meta(ProductForm.Meta):
        fields = ProductForm.Meta.fields + ['published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['published'].label = "Publish this product"


