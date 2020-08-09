from allauth.account.forms import SignupForm
from django import forms
from users.models.estabelecimento import Estabelecimento
from users.models.profile import Profile


class MyCustomSignupForm(SignupForm):

    estabelecimento_nome = forms.CharField(required=True,
                                   min_length=3,
                                   max_length=50,
                                   widget=forms.TextInput(attrs={'placeholder': 'Estabelecimento'}))

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        #cria o estabelecimento que será usado para criar os demais objetos
        estabelecimento = Estabelecimento(dono=user, nome=self.cleaned_data['estabelecimento_nome'])
        estabelecimento.save()

        profile = Profile(user=user, estabelecimento=estabelecimento)
        profile.save()
        # You must return the original result.
        return user