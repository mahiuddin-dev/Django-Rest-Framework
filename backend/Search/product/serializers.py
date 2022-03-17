from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validations import validate_title


class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)

    url = serializers.SerializerMethodField(read_only=True) # One way to do it is to use the get_url function

    edit_url = serializers.HyperlinkedIdentityField(view_name='product:product_update_view',lookup_field='pk') # Another way to do it

    # email = serializers.EmailField(write_only=True)

    title = serializers.CharField(validators=[validate_title])
    # name = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Product
        fields = ['url','edit_url','pk','title','name','description','price','sale_price','my_discount']

    # def validate_title(self,value):
    #     qs = Product.objects.filter(title__iexact=value)

    #     if qs.exists():
    #         raise serializers.ValidationError(f" {value} This title has already been used")
    #     return value


    # def create(self,validated_data):
    #     validated_data.pop('email')
    #     obj = super().create(validated_data)

    #     return obj

    # def update(self,instance,validated_data):
    #     email = validated_data.pop('email')
    #     instance.title = validated_data.get('title')
    #     instance.description = validated_data.get('description')
    #     instance.price = validated_data.get('price')
    #     return super().update(instance,validated_data)

    # url way to do it
    def get_url(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('product:product_view',kwargs={'pk':obj.pk},request=request)   


    def get_my_discount(self,obj):
        try:
            return obj.get_discount()
        except:
            return None