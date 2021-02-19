from django.contrib import admin
from django.urls import path, include
import os
urlpatterns = [
    path('admin/', admin.site.urls),
]
for name in os.listdir(f"apps/"):
	if name not in [".DS_Store"] and os.path.isdir(f"apps/{name}"):
	    urlpatterns.append(
	        path('', include(f"apps.{name}.urls"))
	    )

