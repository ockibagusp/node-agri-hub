from models.credentials import Credentials
from utils.http import AgriHubAPI

"""
Credentials Model -> pass
"""
creds = Credentials()
print "Credentials Model Test"
print "======================"
print "Set expired token"
creds.set(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWJzcGVyZGF5IjoyMCwiaWQiOjEsImV4cCI6MTQ3ODA2NTQwNiwibGFiZWwiOiJGSUxLT01fMSJ9."
    "GV0JQ2Ii0hfipLMo7r1t-T3Sy1rE_1yujB9c75zFqDc",
    20
)
print "Get credentials data"
creds.get()

"""
Http lib -> pass
"""
print "\nHttp lib Test"
print "======================"
api = AgriHubAPI()
print "Subs sensor data"
api.subscribe()
print "Auth test"
api.auth()
