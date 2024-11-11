# api
Alinea A.P.I

## install Redis Service (MAC)
```bash
brew install redis
```

## Start Redis Service
```
brew services start redis
```

## Start Server
```bash
daphne -p 8000 alinea.asgi:application
```
