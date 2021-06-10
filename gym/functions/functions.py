def handle_uploaded_file(f):
    with open('gym/static/GymUser.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

