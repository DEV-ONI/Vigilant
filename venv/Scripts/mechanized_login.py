import mechanize

# request = mechanize.Request(url='https://www.facebook.com/', method='GET')
# print(request)
mbr = mechanize.Browser()
mbr.open('https://www.facebook.com/')
mbr.form['email'] = user
mbr.form['pass'] = password



print(url)