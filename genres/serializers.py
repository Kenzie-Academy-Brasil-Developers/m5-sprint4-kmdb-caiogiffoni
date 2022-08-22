from rest_framework import serializers


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=127)

    def __repr__(self) -> str:
        return f"<Genre {self.id} - {self.name}>"
