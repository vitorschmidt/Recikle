from dataclasses import fields
from rest_framework import serializers
from materials.models import Material

class ListMaterialSerializer(serializers.ModelSerializer):
    class Meta():
        model = Material
        fields = ["id","name","dangerousness","category","infos","decomposition"]

class CreateMaterialSerializer(serializers.ModelSerializer):
    class Meta():
        model = Material
        fields=['id',"name","dangerousness","category","infos","decomposition"]