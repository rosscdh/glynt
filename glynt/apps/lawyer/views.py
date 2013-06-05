# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import FormView, DetailView
from django.views.generic.edit import FormMixin
from endless_pagination.views import AjaxListView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from haystack.query import SQ, SearchQuerySet
from haystack.inputs import Exact, Clean

from glynt.apps.lawyer.services import EnsureLawyerService
from glynt.apps.utils import get_query

from models import Lawyer
from forms import LawyerProfileSetupForm, LawyerSearchForm

import urlparse

import logging
logger = logging.getLogger('django.request')



class LawyerProfileView(DetailView):
    model = Lawyer
    slug_field = 'user__username'

    def get_queryset(self):
        return self.model._default_manager.prefetch_related('user').all()

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(LawyerProfileView, self).get_context_data(**kwargs)

        context.update({
            'firm': self.object.primary_firm
        })
        return context


class LawyerProfileSetupView(FormView):
    form_class = LawyerProfileSetupForm
    template_name = 'lawyer/profile-form.html'

    def get_success_url(self):
        return reverse('lawyer:profile',kwargs={'slug':self.lawyer.user.username})

    def get_context_data(self, **kwargs):
        context = super(LawyerProfileSetupView, self).get_context_data(**kwargs)
        context.update({
            'lawyer': self.lawyer,
        })
        return context

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request}) # add the request to the form

        user = self.request.user
        lawyer_service = EnsureLawyerService(user=user)
        lawyer_service.process()
        lawyer = self.lawyer = lawyer_service.lawyer
        firm = lawyer_service.firm

        startups_advised = lawyer.data.get('startups_advised', [])

        kwargs.update({'initial': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,

            'position': lawyer.role,
            'phone': lawyer.phone if lawyer.phone not in [None,'None'] else '',

            'firm_name': getattr(firm, 'name', None),
            'practice_location_1': lawyer.data.get('practice_location_1', None),
            'practice_location_2': lawyer.data.get('practice_location_2', None),

            'years_practiced': lawyer.years_practiced,
            'summary': lawyer.summary,
            'bio': lawyer.bio,
            'if_i_wasnt_a_lawyer': lawyer.data.get('if_i_wasnt_a_lawyer', None),
            'startups_advised': json.dumps(startups_advised),

            'photo': lawyer.photo,
            'twitter': lawyer.data.get('twitter',''),

            'agree_tandc': lawyer.data.get('agree_tandc', None),
        }})
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'You successfully updated your profile')
        form.delete_cookies()
        return super(LawyerProfileSetupView, self).form_valid(form=form)


class LawyerListView(AjaxListView, FormMixin):
    """ Provide the means to search for lawyers based on keywords, and location
    use elastic search or a basic search depending on settings
    """
    template_name = 'lawyer/lawyer_list.html'
    page_template = 'lawyer/partials/lawyer_list_default.html'
    paginate_by = 10
    model = Lawyer
    form_class = LawyerSearchForm

    def get_queryset(self):
        """ return the approved lawyers 
        if we have a query string then use that to filter """
        logger.info('Using ElasticSearch')
        sq = SQ()
        for value in [value for key,value in self.request.GET.items() if key in ['q','location']]:
            if value:
                term = Clean(urlparse.unquote(value))
                sq.add(SQ(content=term), SQ.AND)
                sq.add(SQ(practice_locations=term), SQ.OR)

        return SearchQuerySet().filter(sq)


    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs.update({
            'request': self.request
            ,'initial': { 'q': urlparse.unquote(self.request.GET.get('q')) if self.request.GET.get('q') else None,
                          'location': urlparse.unquote(self.request.GET.get('location')) if 'location' in self.request.GET or self.request.GET.get('location') else None}
            }) # add the request to the form

        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(LawyerListView, self).get_context_data(**kwargs)

        kwargs.update({
            'form': self.get_form(self.get_form_class())
        })

        return kwargs