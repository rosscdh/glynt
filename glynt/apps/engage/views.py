from django.views.generic import FormView
from forms import EngageWriteMessageForm


class EngageWriteMessageView(FormView):
    form_class = EngageWriteMessageForm
    template_name = 'engage/write-message-form.html'

    def get_success_url(self):
        pass

    def get_context_data(self, **kwargs):
        context = super(EngageWriteMessageView, self).get_context_data(**kwargs)
        context.update({

        })
        return context

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request}) # add the request to the form

        user = self.request.user
        #target_user = self.request.

        kwargs.update({'initial': {
            'user': user,
        }})
        return form_class(**kwargs)

    def form_valid(self, form):
        pass
        #form.save()
        #return super(LawyerProfileSetupView, self).form_valid(form=form)