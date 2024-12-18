from django.urls import path
from .import views
urlpatterns = [

    path('category-add',views.categoryAdd,name="category-add"),
    path('category-edit',views.categoryEdit,name="category-edit"),
    path('category-view',views.catgoryView,name="category-view"),
    path('category-delete',views.categoryDelete,name="category-delete"),

    path('cartoon-add',views.cartoonAdd,name="cartoon-add"),
    path('cartoon-view',views.cartoonView,name="cartoon-view"),
    path('cartoon-edit',views.cartoonEdit,name="cartoon-edit"),
    path('cartoon-delete',views.cartoonDelete,name="cartoon-delete"),

    path('video-add',views.videoAdd,name="video-add"),
    path('video-edit',views.videoEdit,name="video-edit"),
    path('video-view',views.videoView,name="video-view"),
    path('video-delete',views.videoDelete,name="video-delete"),

    path('dashboard',views.dashboard,name="dashboard"),
    path('',views.dashboard,name="dashboard"),
    path('login',views.authUser,name="login"),
    path('logout',views.logoutUser,name="logout"),

    path('categorys',views.getCategorys,name="categorys"),
    path('cartoons',views.getCartoons,name="cartoons"),
    path('getlatestvideos',views.getLatestVideos,name="Latest Videos"),
    path('search/<str:searchQuery>',views.search,name="search"),
    path('help',views.link_converter,name='help'),
    path('image_extract',views.imageExtract,name="image_extract"),
    path('video_extract',views.videoExtract,name="video_extract"),
    path('filter_by_category',views.filter_by_category,name='filter_by_category'),
    path('filter_by_cartoon',views.filter_by_cartoon,name='filter_by_cartoon'),


    path('get_insta_post/<str:code>',views.get_insta_post,name='get_insta_post'),

    path('event/chats',views.sse_view,name='chats'),
]