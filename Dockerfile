FROM python:3.12-alpine

WORKDIR /app

COPY server.py ./
COPY index.html about.html services.html gallery.html contact.html 404.html ./
COPY services ./services
COPY css ./css
COPY js ./js
COPY img ./img
COPY favicon.ico favicon.svg site.webmanifest robots.txt sitemap.xml ./

ENV PORT=8080
EXPOSE 8080

CMD ["python", "server.py"]
