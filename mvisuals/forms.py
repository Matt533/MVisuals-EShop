from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from mvisuals.models import CustomUser, Product, DeliveryInformation, Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', )  # Exclude author field from the form

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from the kwargs
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'

    def save(self, commit=True):
        instance = super(AddPostForm, self).save(commit=False)
        if self.user:
            instance.author = self.user  # Set the author to the user who clicked the button
            instance.author_id = self.user.id  # Set the author_id explicitly
        if commit:
            instance.save()
        return instance

class PostForm(forms.ModelForm):
            class Meta:
                model = Post
                fields = ['title', 'content', 'display', 'image1', 'image2', 'image3',
                          'image4']

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.visible_fields():
                    field.field.widget.attrs['class'] = 'form-control mb-3'

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