class ServerConfigTemplate:
    def __init__(self):
        root = "/var/www/domain/public_html"
        index = "index.html"
        server_name = "example.com"
        access_log = f"/var/log/nginx/{self.domain}.access.log"
        error_log = f"/var/log/nginx/{self.domain}.error.log"
        ports = ['80']