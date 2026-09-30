from django.shortcuts import render, redirect
import json
from .forms import MovieForm, ImportForm
from django.conf import settings
from django.contrib import messages
import os
from django.http import FileResponse


def index(request):
    context = {
        "movies": load_json(get_path_main_json()),
        "movie_form": MovieForm(),
        "import_form": ImportForm(),
    }
    response = render(request, "movies/index.html", context)
    return response


def render_index(request, context):
    response = render(request, "movies/index.html", context)
    return response


def add_movies(request):
    if request.method != "POST":
        return redirect("index")
    form = MovieForm(request.POST)
    path = get_path_main_json()
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
    if request.method != "POST":
        return redirect("index")

    form = ImportForm(request.POST, request.FILES)
    file_path = get_path_main_json()

    if not form.is_valid():
        return render_index(
            request,
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
        data = json.loads(content)
    except UnicodeDecodeError:
        messages.error(request, "Не удалось прочитать файл кодировка должна быть utf-8")
        return redirect("index")
    except json.JSONDecodeError:
        messages.error(request, "Файл не является валидным JSON")
        return redirect("index")

    if not isinstance(data, list):
        messages.error(request, "Ожидается массив фильмов")
        return redirect("index")

    required = {"title", "year", "director", "genre", "rating"}
    cleaned_movies = []

    for i, movie in enumerate(data, 1):
        if not isinstance(movie, dict):
            messages.error(request, f"Элемент {i} не является объектом")
            return redirect("index")
        extra = movie.keys() - required
        if extra:
            messages.error(request, f"В элементе {i} лишние поля {', '.join(extra)}")
            return redirect("index")
        form_movie = MovieForm({key: str(val) for key, val in movie.items()})
        if not form_movie.is_valid():
            messages.error(request, f"Элемент {i}: {form_movie.errors.as_text()}")
            return redirect("index")
        cd = form_movie.cleaned_data
        cleaned_movies.append(
            {
                "title": cd["title"],
                "year": cd["year"],
                "director": cd["director"],
                "genre": cd["genre"],
                "rating": cd["rating"],
            }
        )

    existing = load_json(file_path)
    existing.extend(cleaned_movies)
    write_json(file_path, existing)
    messages.success(request, f"Импортировано фильмов {len(cleaned_movies)}")
    return redirect("index")


def get_path_main_json():
    return os.path.join(settings.MEDIA_ROOT, "movies.json")


def export_json(request):
    file_path = get_path_main_json()
    if not os.path.isfile(file_path):
        messages.error(request, "Файл еще не создан")
        return redirect("index")

    try:
        file = open(file_path, "rb")
    except OSError:
        messages.error(request, "Не удалось открыть файл")
        return redirect("index")

    return FileResponse(file, as_attachment=True, filename="movies.json")


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
