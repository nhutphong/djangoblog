from django import forms

from .models import Article


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'picture',
            'active',
        ]


"""
    project> python3 mamange shell
    # field

    field = forms.EmailField()
    field.clean('dung@gmail.com'): True or False

    

    # form

    default_data_field = {'title': "title_one", 'description': 'da qua ma'}
    
    # new_product
    form = ProductModelForm(default_data_field or request.POST)

    if form.is_valid():
        product = form.save(commit=False)
        product.author = request.user
        product.save()

    # update
    form = ProductModelForm(request.POST, instance=product)

"""
# =============================================================================
                            # validators=[]
"""
    form.is_valid() -> call clean(self)
    clean(self) -> call to_python(self,value) va validate(self, value)
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
# validators = [ func, ...]
# dung duoc cho form field va model field

from django.core.validators import validate_email

class MultiEmailField(forms.Field):
    def to_python(self, emalis: str) -> list :
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, emails: list):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(emails)
        for email in emails:
            validate_email(email)



"""
    form = ContactForm(request.POST)

    form.is_valid() se call MultiEmailField.clean() 
    MultiEmailField.clean() se call 2 method

    thuc ra la validate(to_python(value))
"""
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()

    even_field = forms.IntegerField(validators=[validate_even])

    sender = forms.EmailField()
    recipients = MultiEmailField()
    cc_myself = forms.BooleanField(required=False)

    # def clean_<field_name>(self)
    # check one field_message: co san attr self.cleaned_data
    # khong nen co check nhieu field: def clean(self)
    def clean_message(self):
        message = self.cleaned_data['message']
        if "dung@gmail.com" not in message:
            raise ValidationError("You have forgotten about Fred!")

        return message


    # check more fields
    def clean(self):
        # run  super().clean()
        # se co attr self.cleaned_data

        cleaned_data = super().clean()

        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
    
            if "help" not in subject:

                raise ValidationError(
                    "Did not send for 'help' in the subject despite "
                    "CC'ing yourself."
                )


class DemoModelForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'picture',
            'active',
        ] # '__all__'
        # exclude = ['picture'] bo qua 'picture'