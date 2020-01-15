from allauth.account import forms as allauth_forms


class MemberAddEmailForm(allauth_forms.AddEmailForm):
    def __init__(self, *args, **kwargs):
        super(MemberAddEmailForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'input'
