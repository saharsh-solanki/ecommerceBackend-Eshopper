from django.forms import ModelForm

from user.models import SiteUser


class SiteUserFrom(ModelForm):
    class Meta:
        model = SiteUser
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SiteUserFrom, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def as_p(self):
        "Returns this form rendered as HTML <p>s."

        return self._html_output(
            normal_row=u'<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row=u'%s',
            row_ender='</p>',
            help_text_html=u' <span class="helptext">%s</span>',
            errors_on_separate_row=True)