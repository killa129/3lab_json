from django import forms


class MovieForm(forms.Form):
    title = forms.CharField(
        label="Название",
        max_length=200,
        error_messages={"required": "Введите название фильма"},
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Например: Inception",
            }
        ),
    )
    year = forms.IntegerField(
        label="Год выпуска",
        min_value=1888,
        max_value=2100,
        error_messages={
            "required": "Введите год",
            "invalid": "Год должен быть числом",
            "min_value": "Год должен быть позже 1888",
            "max_value": "Год должен быть праньше 2100",
        },
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
                "min": 1888,
                "max": 2100,
                "placeholder": "2010",
            }
        ),
    )
    director = forms.CharField(
        label="Режиссер",
        max_length=200,
        error_messages={"required": "Введите режиссера"},
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Например: Кристофер Нолан",
            }
        ),
    )
    genre = forms.ChoiceField(
        label="Жанр",
        choices=[
            ("drama", "драма"),
            ("comedy", "комедия"),
            ("action", "боевик"),
            ("thriller", "триллер"),
            ("horror", "ужасы"),
            ("sci-fi", "фантастика"),
            ("fantasy", "фэнтези"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-input",
            }
        ),
    )
    rating = forms.FloatField(
        label="Рейтинг",
        min_value=0,
        max_value=10,
        step_size=0.1,
        error_messages={
            "required": "Введите рейтинг",
            "invalid": "Рейтинг должен быть числом",
            "min_value": "Рейтинг не может быть меньше 0",
            "max_value": "Рейтинг не может быть больше 10",
        },
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
                "min": 0,
                "max": 10,
                "placeholder": "8.8",
            }
        ),
    )


class ImportForm(forms.Form):
    json_file = forms.FileField(
        label="JSON файл",
        error_messages={
            "required": "Выбери файл для загрузки",
            "invalid": "Некорректный файл",
        },
        widget=forms.FileInput(
            attrs={
                "class": "form-input",
                "accept": ".json,applicatioin/json",
            }
        ),
    )
