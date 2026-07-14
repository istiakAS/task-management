
from django import forms
from tasks.models import Task

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget, label='Due Date')
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label='Assign To')

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees', [])
        print(employees)
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]


class StyledFormMixin:
    """mixin to apply styling to form fields"""

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-400 focus:ring-rose-500"

    def applied_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                "class": f"{self.default_classes} overflow-hidden resize-none",  # added overflow-y-auto and resize-none for better UX
                "placeholder": f"Enter {field.label.lower()}",
                "rows": 5  # added to define a consistent textarea height
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-400 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"  # added space between checkboxes
                })


# Django model form 
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model  = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }

        # widgets = {
        #     'title': forms.TextInput(attrs={"class": "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-400 focus:ring-rose-500", 
        #     'placeholder': 'Enter task title'}),

        #     'description': forms.Textarea(attrs={"class": "border-2 border-gray-300 w-full p-3 rounded-lg resize-none shadow-sm focus:outline-none focus:border-rose-400 focus:ring-rose-500",
        #     'placeholder': 'Enter task description',
        #     'rows': 5, #added define a consitent textarea height
        #     }),

        #     'due_date': forms.SelectDateWidget(attrs={"class": "border-2 border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none focus:border-rose-400 focus:ring-rose-500"}),

        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={"class": "space-y-2" #added space between checkboxes
        #     }),
        # }

    """design with mixin class"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.applied_styled_widgets()
        

