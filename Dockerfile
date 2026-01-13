# Resonance School - Woodborne Festival Portal
# Multi-stage build for optimized production image

FROM nginx:alpine

# Metadata
LABEL maintainer="Hannes Mitterer <resonance@woodborne.festival>"
LABEL description="Resonance School Woodborne Festival Portal"
LABEL version="1.0.0"

# Copy HTML files to nginx web root
COPY index.html /usr/share/nginx/html/
COPY LICENSE /usr/share/nginx/html/
COPY README.md /usr/share/nginx/html/
COPY README_PARTNERS.md /usr/share/nginx/html/

# Create a custom nginx configuration
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    \
    # Enable CORS for API calls \
    location ~* \.(html|css|js)$ { \
        add_header Access-Control-Allow-Origin "*"; \
        add_header Cache-Control "public, max-age=3600"; \
    } \
    \
    # Security headers \
    add_header X-Frame-Options "SAMEORIGIN" always; \
    add_header X-Content-Type-Options "nosniff" always; \
    add_header X-XSS-Protection "1; mode=block" always; \
}' > /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
