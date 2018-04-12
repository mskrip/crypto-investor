# crypto-investor

Project for course Extreme programming

## Installation and usage

### Local usage (not recommended)

First create virtual environment with

```sh
$ make venv
python -m venv .venv/
```

Activate it

```sh
user@local crypto-investor/ $ source .venv/bin/activate
(.venv) user@local crypto-investor/ $
```

Install dependencies

```sh
$ make install
Successfully installed crypto-investor
```

And run with

```sh
$ python cryptoinvestor/main.py -c <link to config>
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

To see configuration documentation check [here](docs/configuration.md)

Now you can access the site on [http://localhost:5000](http://localhost:5000)

### Docker usage (recommended)

Create sdist tarball

```sh
$ make sdist
...
Creating tar archive
removing 'crypto-investor-1.0.0' (and everything under it)
```

Build the docker image or pull the built image from registry (`registry.heroku.com/extreme-crypto-investor/web`).

```sh
$ docker build . -t web
...
Successfully built e3ca28da1492
Successfully tagged web:latest
```

```sh
$ docker pull registry.heroku.com/extreme-crypto-investor/web
...
Status: Downloaded newer image for registry.heroku.com/extreme-crypto-investor/web:latest
```

And run it

```sh
$ docker run -p 5000:5000 \
             --name crypto-investor \
             -e PORT=5000 \
             -e COINAPI_KEY='<your coinapi key>' \
             -e LOCAL_CURRENCY=EUR \
             registry.heroku.com/extreme-crypto-investor/web:latest
```

Now you can access the site on [http://localhost:5000](http://localhost:5000)

## Authors

- Tomas Slama
- Matej Vilk
- Samuel Wendl
- Marian Skrip
