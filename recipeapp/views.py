from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Recipe, Comment
from .forms import RecipeForm, CommentForm
from django.core.paginator import Paginator

@login_required
def like_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user in recipe.liked_by.all():
        recipe.liked_by.remove(request.user)
    else:
        recipe.liked_by.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def profile_view(request):
    recipes_list = Recipe.objects.filter(author=request.user).order_by('-created_at')

    for recipe in recipes_list:
        recipe.total_likes = recipe.liked_by.count()

    paginator = Paginator(recipes_list, 5)  # Show 5 recipes per page
    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)
    return render(request, 'dishes/profile.html', {'recipes': recipes})

@login_required
def delete_recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('profile')
    return render(request, 'dishes/delete.html', {'recipe': recipe})

@login_required
def edit_dishes_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'dishes/edit_dishes.html', {'form': form})


# @login_required
def home_view(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    comment_form = CommentForm()
    form = RecipeForm()

    # Recipe submission
    if request.method == 'POST':
        if 'recipe_submit' in request.POST:
            form = RecipeForm(request.POST, request.FILES)
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.save()
                return redirect('home')

        elif 'comment_submit' in request.POST:
            recipe_id = request.POST.get('recipe_id')
            recipe = get_object_or_404(Recipe, id=recipe_id)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.recipe = recipe
                comment.save()
                return redirect('home')

    else:
        form = RecipeForm()
        comment_form = CommentForm()

    return render(request, 'dishes/home.html', {
        'recipes': recipes,
        'form': form,
        'comment_form': comment_form
    })

def about(request):
    return render(request,'dishes/about.html')

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'dishes/recipe_form.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')  # After logout, send them to login page

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Replace 'home' with your homepage URL name
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
