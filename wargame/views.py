from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.expressions import F
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from registration.backends.simple.views import RegistrationView

from wargame import models
from wargame.forms import UserRegistrationForm
from wargame.models import Challenge, UserChallenge, Submission


class IndexView(TemplateView):
    template_name = 'wargame/index.html'


class ChallengesView(LoginRequiredMixin, TemplateView):
    template_name = 'wargame/challenges.html'

    def challenges(self):
        return self.request.user.get_visible_challenges()


class ScoreboardView(TemplateView):
    template_name = 'wargame/scoreboard.html'
    scores = models.User.get_top_40_by_score()


class RulesView(TemplateView):
    template_name = 'wargame/rules.html'


class AboutUsView(TemplateView):
    template_name = 'wargame/about_us.html'

    # noinspection PyMethodMayBeStatic
    def get_people(self):
        return models.StaffMember.objects.order_by(F('name')).all()


class LinksView(TemplateView):
    template_name = 'wargame/links.html'


class UserRegistrationView(RegistrationView):
    form_class = UserRegistrationForm
    template_name = 'wargame/registration.html'


class ChallengeDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'wargame/challenge_details.html'

    def challenge(self):
        return Challenge.objects.get(pk=self.kwargs['id'])

    def files(self):
        return self.challenge().files.filter(private=False).all()

    def userchallenge(self):
        return UserChallenge.get_or_create(self.request.user, self.challenge())

    def post(self, *args, **kwargs):
        userchallenge = self.userchallenge()
        if userchallenge.solved():
            return HttpResponseRedirect(self.request.path)

        submission = Submission()
        submission.user_challenge = userchallenge
        submission.value = self.request.POST.get('flag')

        if submission.value is None:
            return HttpResponseRedirect(self.request.path)

        submission.save()

        if userchallenge.solved():
            messages.success(self.request, 'Congratulations! You have successfully solved this challenge!')
        else:
            messages.error(self.request, 'Your answer was incorrect. Try again!')

        return HttpResponseRedirect(self.request.path)


@login_required()
def reveal_hint(request, challenge_id):
    challenge = Challenge.objects.get(pk=challenge_id)
    userchallenge = UserChallenge.get_or_create(request.user, challenge)
    if not userchallenge.solved():
        userchallenge.hint_used = True
        userchallenge.save()
    return HttpResponseRedirect(reverse_lazy('challenge-details', kwargs={'id': challenge_id}))
