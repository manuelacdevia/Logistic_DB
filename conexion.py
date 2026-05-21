from supabase import create_client

url = "https://hexlzmqtkahdmxsmwexq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhleGx6bXF0a2FoZG14c213ZXhxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg0NTcxNTMsImV4cCI6MjA5NDAzMzE1M30.nHH6WTrlYbyB7kJd8hyAwSgUvQ6JaEpIpaOsMtC9UpY"

supabase = create_client(url, key)

print("Conexión exitosa")