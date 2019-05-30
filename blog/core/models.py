from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
# from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices
from slugify import slugify

# Create your models here.


class PostStatus(DjangoChoices):
    draft = ChoiceItem('D', _('Draft'))
    hidden = ChoiceItem('H', _('Hidden'))
    queued = ChoiceItem('Q', _('Queued'))
    rejected = ChoiceItem('R', _('Rejected'))
    published = ChoiceItem('P', _('Published'))


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    meta_description = models.TextField(max_length=160, null=True, blank=True)
    meta_keywords = models.TextField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def category_posts(self):
        return Post.objects.filter(category=self).count()


class Tags(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        tempslug = slugify(self.name)
        if self.id:
            tag = Tags.objects.get(pk=self.id)
            if tag.name != self.name:
                self.slug = slugify(tempslug)
        else:
            self.slug = slugify(tempslug)
        super(Tags, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    content = models.TextField(_("Content"))
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Created By'), on_delete=models.PROTECT)
    updated_on = models.DateTimeField(_("Updated On"), auto_now=True)
    publication_date = models.DateTimeField(_('Publication date'), db_index=True, default=timezone.now,)
    expiration_date = models.DateTimeField(_('Expiration  date'), null=True, blank=True)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    meta_description = models.TextField(_("Meta Desc"), max_length=160, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, verbose_name=_("Tags"), related_name='rel_posts')
    status = models.CharField(_("Status"), max_length=10, choices=PostStatus.choices, default='Drafted')
    keywords = models.TextField(_("Keywords"), max_length=500, blank=True)
    featured_image = models.ImageField(_("Featured Image"), upload_to='static/blog/uploads/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.title
