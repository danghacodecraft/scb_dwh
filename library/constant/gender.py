from django.utils.translation import ugettext_lazy as _

GENDER_TYPE_MALE = 1
GENDER_TYPE_FEMALE = 2
GENDER_TYPE_OTHER = 3

GENDER_TYPE = {
    GENDER_TYPE_MALE: _('Mr'),
    GENDER_TYPE_FEMALE: _('Mrs'),
    GENDER_TYPE_OTHER: _('Other'),
}
GENDER_TYPE_CHOICE = ((k, v) for k, v in GENDER_TYPE.items())
GENDER_TYPE_LIST = [(k, v) for k, v in GENDER_TYPE.items()]
