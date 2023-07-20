from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from mvisuals.models import CustomUser, Product, DeliveryInformation


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'
            field.label_tag(attrs={'style': 'color: #00563FFF;'})


class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'buy'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class DeliveryInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveryInformation
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        for field_name, field in self.fields.items():
            field.initial = ''

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude=('', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'
        self.fields['availability'].widget.attrs['class'] = 'form-check-input m-1'
        self.fields['availability'].label = 'Available'  # Customize the label for the field


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'brand', 'code', 'category', 'description', 'availability', 'price', 'number_of_items', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'