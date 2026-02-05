# Frontend is served via Nginx from the backend FastAPI app
# This Dockerfile is a reference implementation
# In the current setup, the frontend is served from the backend container

FROM nginx:alpine

# Copy static files to nginx
COPY static/ /usr/share/nginx/html/static/
COPY templates/ /usr/share/nginx/html/templates/

# Copy nginx configuration
COPY ../deploy/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
