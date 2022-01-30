from django.forms import ModelForm, forms, widgets
from django.forms.models import ModelForm
from django import forms
from .models import Project , Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name','featured_image','desc','company','demo_link','source_link']

        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)
        
        for name,field in self.fields.items():
            self.fields[name].widget.attrs.update({'class':'input','placeholder':f'Add {name}'})
        # self.fields['name'].widget.attrs.update({'class':'input','placeholder':'Add Name '})
        # self.fields['desc'].widget.attrs.update({'class':'input','placeholder':'Add Desc '})
        # self.fields['company'].widget.attrs.update({'class':'input','placeholder':'Add Company '})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']

        labels = {
            'value' : 'Place your vote',
            'body' : 'Add a comment with your vote'
        }
        
    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)   

        for name,field in self.fields.items():
                field.widget.attrs.update({'class':'input'})