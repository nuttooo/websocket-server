# Use an official nginx image
FROM nginx:alpine

# Copy the static files to the nginx html directory
COPY index.html /usr/share/nginx/html/
COPY login.html /usr/share/nginx/html/
COPY admin.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 to the outside world
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
