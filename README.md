This repo houses and deploys my personal website.

It lives at [swain.codes](https://swain.codes).

## Writing a New Post

```sh
./new.py <slug>
./start.py
```

## Developing Locally

Install dependencies:

```sh
poetry install
```

Start the server locally with:

```sh
./start.py
```

Whenever your changes are finished, be sure to run a build:

```sh
./build.py
```

### Updating Code Highlighting

The code highlighting styles were generated using pygmentize, like so:

```sh
poetry run pygmentize -S default -f html -a .codehilite > src/styles/codehilite.css
```

Customize as you'd like!