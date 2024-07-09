import requests

url = 'https://openapi.kpx.or.kr/openapi/sukub5mMaxDatetime/getSukub5mMaxDatetime'
params ={'serviceKey' : 'NpWQYBWBernbIhRAeWWRQx%2BAmef%2Bhy8m%2BHDpfVbjbQzjZga2mjyJXKpn7C86fmyy4AaS0UlbG4BE8CPZnp%2BAvA%3D%3D' }

response = requests.get(url, params=params)
print(response.content)