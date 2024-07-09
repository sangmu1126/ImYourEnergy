import requests

url = 'https://openapi.kpx.or.kr/openapi/sukub5mMaxDatetime/getSukub5mMaxDatetime'
params ={'serviceKey' : 'NpWQYBWBernbIhRAeWWRQx+Amef+hy8m+HDpfVbjbQzjZga2mjyJXKpn7C86fmyy4AaS0UlbG4BE8CPZnp+AvA==' }

response = requests.get(url, params=params)
print(response.content)