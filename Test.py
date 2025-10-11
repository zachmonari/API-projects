import requests

#get a webpage
rr = requests.get('https://api.github.com/events')
#make HTTP POST request
r1=requests.post('https://httpbin.org/post', data={'key':'value'})
r2 = requests.put('https://httpbin.org/put', data={'key': 'value'})
r3 = requests.delete('https://httpbin.org/delete')
r4 = requests.head('https://httpbin.org/get')
r5 = requests.options('https://httpbin.org/get')

#Passing Parameters In URLs
payload={'key1':'value1','key2':'value2'}
r6=requests.get('https://httpbin.org/get', params=payload)
print(r1.url)
print(r1.status_code)

# passing a list of items as a value
payload={'key1':'value1','key2':['value2','value3']}
r=requests.get('https://httpbin.org/get', params=payload)
print(r.url)

r = requests.get('https://api.github.com/events', stream=True)
print(r.url)
print(r.raw)
print(r.raw.read(10))


payload = {'key1': 'value1', 'key2': 'value2'}

r = requests.post('https://httpbin.org/post', data=payload)
print(r.text)

#working with randomuser.me APIs
r = requests.get('https://randomuser.me/api')
#print(r.status_code)
#print(r.json())

gender=r.json()['results'][0]['gender']
print(gender)

title=r.json()['results'][0]['name']['title']
print(title)
first_name=r.json()['results'][0]['name']['first']
print(first_name)

last_name=r.json()['results'][0]['name']['last']
print(last_name)
print(f'{title} {first_name} {last_name}')

street=r.json()['results'][0]['location']['street']['name']
number=r.json()['results'][0]['location']['street']['number']
print(f'{street} {number}')

age=r.json()['results'][0]['dob']['age']
print(f"Age: ",age)


#working with randomfox.ca APIs
r = requests.get('https://randomfox.ca/api')

fox=r.json()
print(fox['image'])


# working with pokeApi.co APIs
base_url="https://pokeapi.co/api/v2"
def get_pokeapi_info(name):
    url=f"{base_url}/pokemon/{name}"
    response=requests.get(url)

    if response.status_code==200:
        pokemon_data=r.json()
        return pokemon_data

    else:
        print(f"Something went wrong! {response.status_code}")
        return 0

pokemon_name="Typhlosion"
pokemon_info=get_pokeapi_info(pokemon_name)

if pokemon_info:
    print(f"Name: {pokemon_info["name"].capitalize()}")
    print(f"ID: {pokemon_info["id"]}")
    print(f"Height: {pokemon_info["height"]}")
    print(f"Weight: {pokemon_info["weight"]}")
