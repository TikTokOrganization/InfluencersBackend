import requests, webbrowser, time

webbrowser.open("http://localhost:8080/login")

input()

client_id = "620677125812-g4634rpb7kam1r5hm8kq2mdccdhg3i5l.apps.googleusercontent.com"
r = requests.get("http://localhost:8080/getLikedShorts", params = {"client_id": client_id})