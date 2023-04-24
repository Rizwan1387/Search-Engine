from django.shortcuts import render, get_object_or_404
from .models import Counter
from django.shortcuts import render
from django.shortcuts import HttpResponse

def index(request):
	q = request.GET.get("q", None)
	try: 
		value = None 
		if(q=='apple watch series 8'):
			value = ["https://www.apple.com/apple-watch-series-8/",'https://www.apple.com/us/shop/goto/buy_watch/apple_watch_series_8','https://www.apple.com/',
			'https://www.apple.com/#footnote-1']
		elif(q=='airpods 2nd generation'):
			value = ['https://www.apple.com/airpods/','https://www.apple.com/ipad/','https://www.apple.com/ipad-10.9/','https://www.apple.com/us/shop/goto/buy_ipad/ipad']
		elif(q.strip()==''):
			value = ['NOT FOUND']
		else: 
			value = ["https://www.apple.com/",'https://www.apple.com/us/shop/goto/buy_watch/apple_watch_series_8','https://www.apple.com/#footnote-1','https://www.apple.com/iphone-14/']
		context = {'statuses':value }
		return render(request, 'counter/index.html', context)

	except: 
		return render(request, 'counter/notfound.html', context)
