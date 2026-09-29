from django.shortcuts import render, redirect
import json
from .forms import MovieForm, ImportForm
from django.conf import settings
from django.contrib import messages
import os
from django.http import FileResponse


def index(request):
    context = {
        "movies": load_json(os.path.join(settings.MEDIA_ROOT, "movies.json")),
        "movie_form": MovieForm(),
        "import_form": ImportForm(),
    }
    response = render(request, "movies/index.html", context)
    return response


def add_movies(request):
    if request.method != "POST":
        return redirect("index")
    form = MovieForm(request.POST)
    path = os.path.join(settings.MEDIA_ROOT, "movies.json")
    if not form.is_valid():
        return render(
            request,
            "movies/index.html",
            context={
                "movies": load_json(path),
                "movie_form": form,
                "import_form": ImportForm(),
            },
        )
    cd = form.cleaned_data
    new_movie = {
        "title": cd["title"],
        "year": cd["year"],
        "director": cd["director"],
        "genre": cd["genre"],
        "rating": cd["rating"],
    }
    append_movie(path, new_movie)
    response = redirect("index")
    return response


def import_json(request):
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)

        if not form.is_valid():
            file_path = os.path.join(settings.MEDIA_ROOT, "movies.json")
            return render(
                request,
                "movies/index.html",
                {
                    "movies": load_json(file_path),
                    "movie_form": MovieForm(),
                    "import_form": form,
                },
            )

        uploaded = form.cleaned_data["json_file"]

        if not uploaded.name.lower().endswith(".json"):
            messages.error(request, "Файл должен быть в формате .json")
            return redirect("index")
        try:
            content = uploaded.read().decode("utf-8")
            data = json.load(content)
        except UnicodeDecodeError:
            messages.error(
                request, "Не удалось прочитать файл кодировка должна быть utf-8"
            )
            return redirect("index")
        except json.JSONDecodeError:
            messages.error(request, "Файл не является валидным JSON")
            return redirect("index")

        if not isinstance(data, list):
            messages.error(request, "Ожидается массив фильмов")
            return redirect("index")

        required = {"title", "year", "director", "genre", "raiting"}
        for i, movie in enumerate(data, 1):
            if not isinstance(movie, dict):
                messages.error(request, f"Элемент {i} не является объектом")
                return redirect("index")
            missing = required - movie.keys()
            if missing:
                messages.error(
                    request, f"В элементе {i} отстутствуют поля {', '.join(missing)}"
                )
                return redirect("index")
        return render(
            request,
            "movies/index.html",
            context={
                "movies": data,
                "movie_form": MovieForm(),
                "import_form": form,
            },
        )


def export_json(request):
    file_path = load_json(os.path.join(settings.MEDIA_ROOT, "movies.json"))
    if not os.path.exists(file_path):
        messages.error(request, "Файл еще не создан")
        return redirect("index")

    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="movies.json"
    )


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_movie(path, movie):
    data = load_json(path)
    data.append(movie)
    write_json(path, data)
