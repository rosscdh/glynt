# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import LawyerEndorsement, InvestorEndorsement


admin.site.register([LawyerEndorsement, InvestorEndorsement])
