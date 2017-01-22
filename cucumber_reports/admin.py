from django.contrib import admin

from .models import *

admin.site.register(BuildRun)
admin.site.register(Feature)
admin.site.register(StepRun)
admin.site.register(StepDefinition)
admin.site.register(ScenarioDefinition)
admin.site.register(ScenarioRun)