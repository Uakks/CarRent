from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field= "django.db.models.BigAutoField"   #Если в модели не указан свой номер, Django сам добавляет колонку id с номерами 1, 2, 3…
    name = 'apps.cars'  #Адрес приложения: где оно лежит
    verbose_name= "Cars"
