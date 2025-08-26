from rest_framework import serializers
from ..models.trasladosModel import Traslado, TrasladoItem


class TrasladoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrasladoItem
        exclude = ['traslado']


class TrasladoSerializer(serializers.ModelSerializer):
    items = TrasladoItemSerializer(many=True, required=False)

    class Meta:
        model = Traslado
        fields = '__all__'
        read_only_fields = (
            'id', 'created_at', 'updated_at',
            'estatus', 'fecha_envio', 'fecha_recibido',
            'enviado_por', 'recibido_por',
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        request = self.context.get('request') if self.context else None
        user = request.user if request and hasattr(request, 'user') else None
        enviado_por = None
        if user and getattr(user, 'is_authenticated', False):
            enviado_por = user.username
        elif request:
            enviado_por = request.headers.get('X-User') or None

        traslado = Traslado.objects.create(enviado_por=enviado_por, estatus='ENVIADO', **validated_data)
        for item in items_data:
            TrasladoItem.objects.create(traslado=traslado, **item)
        return traslado
