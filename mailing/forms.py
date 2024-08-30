from django import forms

from mailing.models import Mailing


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('mailing_status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_send_time"].widget = DateTimeInput()
        self.fields["last_send_time"].widget = DateTimeInput()
