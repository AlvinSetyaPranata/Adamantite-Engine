# DEFAULT SECTION 
MAX_BACKLOG = 20                 # Set the maximum unaccepted connection
MAX_THREAD_ALLOWED = "EACH"      # Set the maximum thread that server will use, 'each' represent to use thrad for each incoming request
MAX_BUFFER_LIMIT = 16000         # Set the maximum of buffer size
REQUEST_TIMEOUT = 0              # Set the connection timeout between server and client



COMPRESSION_PRIORITY = [
    "br",
    "gzip",
    "deflate",
    "compress",
    "chunked"
]

# br = 1
# gzip = 2
# deflate = 3
# compress = 4





# feelfree to, change the status code abreviations
STATUS_CODE_ABREVIATIONS = {
    "200" : "OK",
    "401" : "UNAUTHORIZED",
    "403" : "FORBIDDEN",
    "404" : "NOT FOUND",
    "500" : "INTERNAL SERVER ERROR",
    "400" : "BAD REQUEST"
}


