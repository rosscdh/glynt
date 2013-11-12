Deploy Notes
============


Nov, 10 2013 - []
----------------------------------

* ./manage.py migrate project : update to allow for null company_id as company is no longer required
* need to manualy run using shell_plus as south wont allow direct means to do it
```
for p in Project.objects.all():
...   p.save()  # will simply update the project_name in data
```
