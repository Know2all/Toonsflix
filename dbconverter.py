import instaloader

loader = instaloader.Instaloader()

profile = instaloader.Profile.from_username(loader.context, "r_o_l_l_n_o_004")

posts_data = []

for post in profile.get_posts():
    posts_data.append({
        'caption': post.caption,
        'media_url': post.url,
        'is_video': post.is_video,
        'video_url': post.video_url if post.is_video else None,
        'likes': post.likes,
        'comments': post.comments,
        'timestamp': post.date.strftime('%Y-%m-%d %H:%M:%S')
    })

print(posts_data)