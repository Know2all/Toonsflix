from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.contrib.auth import login,logout,authenticate
from .serializer import *
from django.db.models import Q
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import time
import instaloader

loader = instaloader.Instaloader()

def chat(request):
    return render(request,template_name="api/chat.html")

def event_stream():
    """Generator function that yields JSON data for SSE."""
    while True:
        # Example JSON data - Replace this with your live data fetching logic
        data = {
            "message": "Current time",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Serialize data to JSON
        json_data = json.dumps(data)
        
        # Yield data in SSE format
        yield f"data: {json_data}\n\n"
        
        time.sleep(2)  # Adjust the interval as needed

def sse_view(request):
    """View that streams live JSON data to the client using SSE."""
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response

def home(request):

    page_number = request.GET.get('page', 1)
    searchQuery = request.GET.get('query',"")
    allmovies = Video.objects.filter(status=True,title__icontains=searchQuery)
    
    paginator = Paginator(allmovies, 10)
    
    page_obj = paginator.get_page(page_number)

    print(f"Page : {page_number} \nData : {page_obj} \nHas Next:{page_obj.has_next()}")
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        movies = list(page_obj.object_list.values())
        return JsonResponse({'movies': movies, 'has_next': page_obj.has_next()})
    

    return render(request,template_name='api/home.html')

def watch(request,id):
    movie = Video.objects.get(pk = id)
    if request.method == "POST":
        id = request.POST.get('id')
        video = Video.objects.get(pk = id)
        return JsonResponse({'video':video.videoUrl})
    context = {
        'movie':movie
    }
    return render(request,template_name="api/watch.html",context=context)


def authUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponse("Login Success",status=200)
            else:
                return HttpResponse("Invalid Credentials",status=500)
        except Exception as e:
            return HttpResponse(f"Error : {str(e)}",status=500)
    return render(request,template_name="api/Screens/login.html")

def logoutUser(request):
    logout(request)
    return redirect("login")

def thumbnailConverter(link):
    try:
        file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', link).group(1)
        if file_id:
            new_link = f" https://drive.google.com/thumbnail?id={file_id}"
            return new_link
    except Exception as e:
        return link

def videoConverter(link):
    try:
        file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', link).group(1)
        if file_id:
            new_link = f"https://drive.google.com/file/d/{file_id}/preview"
            return new_link
    except Exception as e:
        return link

def link_converter(request):
    return render(request,template_name="api/index.html")

def imageExtract(request):
    link = request.POST.get('image_link')
    file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', link).group(1)
    new_link = f" https://drive.google.com/thumbnail?id={file_id}"
    result = f"<a href='{new_link}'>{new_link}"
    return HttpResponse(result)

def videoExtract(request):
    link = request.POST.get('video_link')
    file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', link).group(1)
    new_link = f"https://drive.google.com/file/d/{file_id}/preview"
    result = f"<a href='{new_link}'>{new_link}"
    return HttpResponse(result)

@api_view(['GET'])
def getCategorys(request):
    allcategorys = CategorySerializer(Category.objects.filter(status=True),many=True).data
    return Response({'status':'ok','data':allcategorys})

@api_view(['GET'])
def getCartoons(request):
    allcartoons = CartoonSerializer(Cartoon.objects.filter(status=True,category__status=True),many=True).data
    return Response({'status':'ok','data':allcartoons})

@api_view(['GET'])
def getLatestVideos(request):

    videos = Video.objects.all()

    page_number = int(request.GET.get('page'))

    paginator = Paginator(videos, 10)

    try:
        videos_page = paginator.page(page_number)
    except PageNotAnInteger:
        videos_page = paginator.page(1)
    except EmptyPage:
        videos_page = paginator.page(paginator.num_pages)

    data = VideoSerializer(videos_page,many=True).data

    response = {
        'data': data,
        'has_next': videos_page.has_next(),
        'has_previous': videos_page.has_previous(),
        'page_number': videos_page.number,
        'num_pages': paginator.num_pages,
    }

    return JsonResponse(response)

@api_view(['GET'])
def search(request,searchQuery):
    results =VideoSerializer(Video.objects.filter(status=True,title__icontains=searchQuery),many=True).data
    return Response({'status':'ok','data':results})


@api_view(['GET'])
def filter_by_category(request):
    category = int(request.GET.get('id'))
    data = CartoonSerializer(Cartoon.objects.filter(status=True,category__id=category),many=True).data
    return Response({'status':'ok','data':data})

@api_view(['GET'])
def filter_by_cartoon(request):

    videos = Video.objects.filter(status=True,cartoon__id=int(request.GET.get('id')))

    page_number = int(request.GET.get('page'))

    paginator = Paginator(videos, 10)

    try:
        videos_page = paginator.page(page_number)
    except PageNotAnInteger:
        videos_page = paginator.page(1)
    except EmptyPage:
        videos_page = paginator.page(paginator.num_pages)

    data = VideoSerializer(videos_page,many=True).data
    

    response = {
        'status':'ok',
        'data': data,
        'has_next': videos_page.has_next(),
        'has_previous': videos_page.has_previous(),
        'page_number': videos_page.number,
        'num_pages': paginator.num_pages,
    }

    return Response(response)

def catgoryView(request):
    
    if request.method == 'POST':
        search = request.POST.get('search[value]')
        categorys = Category.objects.all()
        
        if search:
            categorys = Category.objects.filter(
                Q(name__icontains=search)
            )

        paginator = Paginator(categorys, request.POST.get('length', 10))
        page_number = int(request.POST.get('start', 0)) / int(request.POST.get('length')) + 1
        categorys = paginator.get_page(page_number)

        responseData = []

        for i,item in enumerate(categorys):
            row = {
                "sno":i+1,
                "title":item.name,
                "thumbnail":f"<a href='#' data-img='{item.image}' class='preview'  data-bs-toggle='modal' data-bs-target='.bs-example-modal-center' >{item.image}</a>",
                "action":f"""<a class='btn btn-sm btn-primary' hx-boost='true' href='category-edit?id={item.id}'>
                                <i class='fa fa-edit'></i>
                            </a>
                            <form class='d-inline delete' data-id='{item.id}' data-action='category-delete' >
                                <button  class='btn btn-danger btn-sm' type='submit'>
                                    <i class='fa fa-trash'></i>
                                </button>
                            </form>
                            """
            }
            responseData.append(row)

        data = {
            'draw': int(request.POST.get('draw', 1)),
            'recordsTotal': categorys.paginator.count,
            'recordsFiltered': categorys.paginator.count,
            'data': responseData
        }

        return JsonResponse(data)
    return render(request,template_name="api/Screens/category/view.html")

def categoryAdd(request):
    if request.method == "POST":
        data = request.POST
        status = True if data['status'] == "show" else False
        try:
            category = Category.objects.create(name=data['category'],image=thumbnailConverter(data['image']),status=status)
            return HttpResponse("Category Added Success",status=200)
        except Exception as e:
            return HttpResponse({'message':str(e)},status=500)
    return render(request,template_name="api/Screens/category/add.html")

def categoryEdit(request):
    if request.method == "GET":
        id = request.GET.get('id')
        category = Category.objects.get(pk=id)
        context = {
            'category':category
        }
        return render(request,template_name="api/Screens/category/edit.html",context=context)
    elif request.method == "POST":
        id = request.POST.get('id')
        try:
            category = Category.objects.get(pk=id)
            category.name = request.POST.get('category')
            category.image = thumbnailConverter(request.POST.get('image'))
            category.status = True if request.POST.get('status') == "show" else False
            category.save()
            return HttpResponse("Category Edited",status=200)
        except Exception as e:
            return HttpResponse(f"Error : {str(e)}",status=500)

def categoryDelete(request):
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            category = get_object_or_404(Category, pk=id)
            category.delete()
            return HttpResponse("Deleted",status=200)
        except Exception as e:
            return HttpResponse(f"Error :{str(e)} ",status=500)
    else:
        return HttpResponse("Invalid Request",status=400)

def cartoonAdd(request):
    categorys = Category.objects.filter(status=True)
    context = {
        'categorys':categorys
    }
    if request.method == "POST":
        data = request.POST
        status = True if data['status'] == "show" else False
        try:
            category = Category.objects.get(pk=data['category'])
            cartoon = Cartoon.objects.create(category=category,title=data['title'],image=thumbnailConverter(data['image']),status=status)
            return HttpResponse("Cartoon Added Success",status=200)
        except Exception as e:
            return HttpResponse(str(e),status=500)
    return render(request,template_name="api/Screens/cartoon/add.html",context=context)

def cartoonView(request):
    
    cartoons = Cartoon.objects.all()

    if request.method == 'POST':
        search = request.POST.get('search[value]')
        cartoons = Cartoon.objects.all()
        
        if search:
            cartoons = Cartoon.objects.filter(
                Q(title__icontains=search)
            )

        paginator = Paginator(cartoons, request.POST.get('length', 10))
        page_number = int(request.POST.get('start', 0)) / int(request.POST.get('length')) + 1
        cartoons = paginator.get_page(page_number)

        responseData = []

        for i,item in enumerate(cartoons):
            row = {
                "sno":i+1,
                "title":item.title,
                "thumbnail":f"<a href='#' data-img='{item.image}' class='preview'  data-bs-toggle='modal' data-bs-target='.bs-example-modal-center' >{item.image}</a>",
                "action":f"""<a class='btn btn-sm btn-primary' hx-boost='true' href='cartoon-edit?id={item.id}'>
                                <i class='fa fa-edit'></i>
                            </a>
                            <form class='d-inline delete' data-action='cartoon-delete' data-id='{item.id}'>
                                <button  class='btn btn-danger btn-sm' type='submit'>
                                    <i class='fa fa-trash'></i>
                                </button>
                            </form>
                            <a href='video-add?cartoon={item.id}' class='btn btn-sm btn-success'>
                                <i class='fa fa-upload'></i>
                            </a>
                            """
            }
            responseData.append(row)

        data = {
            'draw': int(request.POST.get('draw', 1)),
            'recordsTotal': cartoons.paginator.count,
            'recordsFiltered': cartoons.paginator.count,
            'data': responseData
        }

        return JsonResponse(data)
    context = {
        'cartoons':cartoons
    }
    return render(request,template_name="api/Screens/cartoon/view.html",context=context)

def cartoonEdit(request):
    if request.method == "GET":
        id = request.GET.get('id')
        cartoon = Cartoon.objects.get(pk=id)
        categorys = Category.objects.filter(status=True)
        context = {
            'cartoon':cartoon,
            'categorys':categorys
        }
        return render(request,template_name="api/Screens/cartoon/edit.html",context=context)
    elif request.method == "POST":
        id = request.POST.get('id')
        try:
            cartoon = Cartoon.objects.get(pk=id)
            category = Category.objects.get(pk=request.POST.get('category'))
            cartoon.category = category
            cartoon.title = request.POST.get('title')
            cartoon.image = thumbnailConverter(request.POST.get('image'))
            cartoon.status = True if request.POST.get('status') == "show" else False
            cartoon.save()
            return HttpResponse("Cartoon Edited",status=200)
        except Exception as e:
            return HttpResponse(f"Error : {str(e)}",status=500)
        
def cartoonDelete(request):
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            cartoon = get_object_or_404(Cartoon, pk=id)
            cartoon.delete()
            return HttpResponse("Deleted",status=200)
        except Exception as e:
            return HttpResponse(f"Error :{str(e)} ",status=500)
    else:
        return HttpResponse("Invalid Request",status=400)
    
def videoAdd(request):
    
    cartoon = request.GET.get('cartoon')
    context = {
        'cartoon':cartoon
    }
    if request.method == "POST":
        data = request.POST
        status = True if data['status'] == "show" else False
        cartoon = Cartoon.objects.get(pk=request.POST.get('cartoon'))
        try:
            video = Video.objects.create(
                cartoon=cartoon,
                title=data['title'],
                thumbnail=thumbnailConverter(data['image']),
                videoUrl=videoConverter(link=data['video']),
                status = status
            )
            return HttpResponse("Video Addedd",status=200)
        except Exception as e:
            return HttpResponse(str(e),status=500)
    return render(request,template_name="api/Screens/video/add.html",context=context)

def videoView(request):
    
    cols = ['id','cartoon','title','thumbnail']

    if request.method == 'POST':
        col = request.POST.get('order[0][column]')
        sortBy = "-" if request.POST.get('order[0][dir]') == "desc" else ""
        search = request.POST.get('search[value]')
        videos = Video.objects.all().order_by(f"{sortBy}{cols[int(col)]}")
        
        if search:
            videos = Video.objects.filter(
                Q(title__icontains=search) | Q(cartoon__title__icontains=search)
            ).order_by(f"{sortBy}{cols[int(col)]}")
            

        paginator = Paginator(videos, request.POST.get('length', 10))
        page_number = int(request.POST.get('start', 0)) / int(request.POST.get('length')) + 1
        videos = paginator.get_page(page_number)

        responseData = []

        for i,item in enumerate(videos):
            row = {
                "sno":i+1,
                "cartoon":item.cartoon.title,
                "title":item.title,
                "thumbnail":f"<a href='#' data-img='{item.thumbnail}' class='preview'  data-bs-toggle='modal' data-bs-target='.bs-example-modal-center' >{item.thumbnail}</a>",
                "action":f"""<a class='btn btn-sm btn-primary' hx-boost='true' href='video-edit?id={item.id}'>
                                <i class='fa fa-edit'></i>
                            </a>
                            <form class='d-inline delete' data-id='{item.id}'>
                                <button  class='btn btn-danger btn-sm' type='submit'>
                                    <i class='fa fa-trash'></i>
                                </button>
                            </form>
                            """
            }
            responseData.append(row)

        data = {
            'draw': int(request.POST.get('draw', 1)),
            'recordsTotal': videos.paginator.count,
            'recordsFiltered': videos.paginator.count,
            'data': responseData
        }

        return JsonResponse(data)

    return render(request,template_name="api/Screens/video/view.html")

def videoEdit(request):
    if request.method == "GET":
        id = request.GET.get('id')
        try:
            video = Video.objects.get(pk=id)
            tags = Tag.objects.all()
            cartoons = Cartoon.objects.all()
        except Exception as e:
            print(str(e))
        context = {
            'video':video,
            'tags':tags,
            'cartoons':cartoons
        }
    if request.method == "POST":
        data = request.POST
        id = request.POST.get('id')
        try:
            video = Video.objects.get(pk=id)
            video.title = data.get('title')
            video.thumbnail = thumbnailConverter(data.get('image'))
            video.videoUrl = videoConverter(data.get('video'))
            video.status = True if data.get('status') == "show" else False
            
            video.tags.clear()
            tags = [int(tag) for tag in data.getlist('tags')]
            
            for tag in tags:
                video.tags.add(tag)

            video.save()
            return HttpResponse("Success",status=200)
        except Exception as e:
           return HttpResponse(f"Error:{str(e)}",status=500)
    return render(request,template_name="api/Screens/video/edit.html",context=context)

def videoDelete(request):
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            video = get_object_or_404(Video, pk=id)
            video.delete()
            return HttpResponse("Deleted",status=200)
        except Exception as e:
            return HttpResponse(f"Error :{str(e)} ",status=500)
    else:
        return HttpResponse("Invalid Request",status=400)
    
def dashboard(request):
    return render(request,template_name="api/Screens/home.html")

def get_insta_post(request,code):
    try:
        post = IGCommerce.objects.get(shortcode = code)
        response = {
            'thumbnail':post.thumbnail,
            'video_src':post.video,
            'likes':post.likes,
            'comments':post.comments,
            'shortcode':post.shortcode,
            'mediaid':post.media_id,
        }
    except Exception as e:
        return JsonResponse({'error':str(e)},status=500)
    return JsonResponse(response,status=200)