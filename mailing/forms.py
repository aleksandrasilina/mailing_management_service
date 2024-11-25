from django import forms

from mailing.models import Mailing, Message, Client


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('mailing_status', 'owner')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["first_send_time"].widget = DateTimeInput()
        self.fields["last_send_time"].widget = DateTimeInput()

        if not user.is_superuser:
            self.fields["message"].queryset = Message.objects.filter(owner=user)
            self.fields["clients"].queryset = Client.objects.filter(owner=user)


class MailingModeratorForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('mailing_status',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
