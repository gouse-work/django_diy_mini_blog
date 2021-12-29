from django.test import TestCase
from blog.forms import CommentCreateForm
from django.utils.crypto import get_random_string

class  CommentCreateFormTest(TestCase):
    def test_description_label(self):
        form=CommentCreateForm()
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'description')

    def test_description_help_text(self):
        form=CommentCreateForm()
        self.assertEqual(form.fields['description'].help_text,'Enter comment about blog here.')

    def test_description_max_length(self):
        form=CommentCreateForm()
        self.assertEqual(form.fields['description'].max_length,1000)

    def test_description_above_max_length(self):
        description_data=get_random_string(length=1001)
        form=CommentCreateForm(data={'description':description_data})
        self.assertFalse(form.is_valid())