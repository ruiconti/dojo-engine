# 🥋 dojo
A service to receive model artefacts and training recipes to  machine learning models asynchronously 

## Project

Project architecture, motifs and goals are listed [here](docs/PROJECT.md)

## Tasks

Requirements and todo-lists are listed [here](docs/TODO.md)

## Tests

To run first delivery tests, run on project root:

``` bash
python -m test.conc
```

Test for both concurrency (through `multiprocessing` library) and feature (enqueuing and dequeuing of a file-queue)