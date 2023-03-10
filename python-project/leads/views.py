from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.views import generic
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm

# CRUD +L - Create, Retrieve, Update and Delete + List


class SingupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")

#class based view
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

#function based view
def landing_page(request):
    return render(request, "landing.html")

#class based view
class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"


#function based view
def lead_list(request):
    #return HttpResponse("Hello World")
    #return render(request, "leads/home_page.html")
    
    leads = Lead.objects.all()
    
    context = {
        "leads" : leads
    }
    return render(request, "leads/lead_list.html", context)


#class based view
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"
    

#fucntion based view
def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead" : lead
    }
    return render(request, "leads/lead_detail.html", context)


#class based view
class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    #for sending email
    # def form_valid(self, form):
    #     send_mail(
    #         subject="A lead has been created",
    #         message="Go to the site to see the new lead",
    #         from_email="test@test.com",
    #         recipient_list=["test2@test.com"]
    #     )
    #     return super(LeadCreateView, self).form_valid(form)


#function based view
def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        print('Receiving a post request')
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
            
    context = {
        "form" : form
    }
    return render(request, "leads/lead_create.html", context)


#class based view
class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")


#function based view
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
            
    context = {
        "form" : form, "lead": lead
    }
    return render(request, "leads/lead_update.html", context)


#class based view
class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
        
    def get_success_url(self):
        return reverse("leads:lead-list")


#function based view
def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")
    
