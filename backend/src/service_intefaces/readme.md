here we have abstract interfaces (ports) for our services
idea is simple:
in our web api code we use these abstractions (so neither our framework, nor service implementations "know" each other)
and we inject services by app dependency overrides