from django.urls import path

from .views import home,add_contact,delete_contact, update_contact
urlpatterns = [
    path("",home,name="home"),
    path("add/",add_contact,name="add-contact"),
    path("<int:id>/delete/",delete_contact,name="delete-contact"),
    # path("<int:id>/update/",update_contact,name="update-contact"),
]
