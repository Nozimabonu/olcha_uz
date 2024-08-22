from django.urls import path
from olcha.views.category import c_views as c_views
from olcha.views.group import g_views as g_views
from olcha.views.product import p_views as p_views
from olcha.views.auth import views as auth_views

urlpatterns = [
    # category urls
    path('category/', c_views.CategoryListApiView.as_view(), name='category-list'),
    path('category/<slug:slug>/detail/', c_views.CategoryDetailApiView.as_view(), name='category-detail'),
    path('category/create/', c_views.CategoryCreateApiView.as_view(), name='create-category'),
    path('category/<slug:slug>/edit/', c_views.CategoryUpdateApiView.as_view()),
    path('category/<slug:slug>/delete/', c_views.CategoryDeleteApiView.as_view()),

    # Group urls
    path('group/create/', g_views.GroupCreateApiView.as_view(), name='group-create'),
    path('category/<slug:slug>/', g_views.GroupListApiView.as_view(), name='group-list'),
    path('group/<slug:slug>/detail/', g_views.GroupDetailApiView.as_view()),

    # Product urls
    path('category/<slug:category_slug>/<slug:group_slug>/', p_views.ProductListCreateApiView.as_view()),
    path('product/view/<slug:slug>/', p_views.ProductDetailView.as_view()),

    # Login View
    path('login-page/', auth_views.LoginApiView.as_view()),
    path('logout-page/', auth_views.LogoutApiView.as_view()),
    path('register-page/', auth_views.RegisterAPiVIew.as_view()),

]
