from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import scrape.scraper as scraper
from multiprocessing import Pool
import time
import openai

basicUrl = 'https://myhealthgazette.com/wp-admin/admin-ajax.php'
queryText = "Please rewrite this text in a fluent simple and fun language."
openai.api_key = "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"

@api_view(http_method_names=["POST"])
def scrapeposts(request: Request):
    weblink = request.data.get("weblink")
    postId = int(request.data.get("postId"))
    prompt = request.data.get("prompt")

    print(f"weblink: {weblink}, postId: {postId}, prompt: {prompt}")

    try:
        posts = scraper.scraper(postId, weblink)

        print('Replacing with ai')
        with Pool(1) as p:
            replacedPosts = p.starmap(scraper.worker, [(post, prompt) for post in posts])
        
        print('sending results...')

        for post in posts:
            print(post)

        for replaced_post in replacedPosts:
            print(replaced_post)

        print('All done!')

        return Response(data={"msg": "results sent succcessfully", "data": {"old": posts, "new": replacedPosts}})

    except openai.error.RateLimitError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30

        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)

        return scrapeposts(postId, weblink, query_text=queryText)
