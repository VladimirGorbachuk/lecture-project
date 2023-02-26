to run project
docker build -t my-react-app . -f ./ci-cd/frontend.Dockerfile
docker run -p 80:80 my-react-app

