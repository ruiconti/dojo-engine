
# Project

A service to support and serve machine learning engineers, running applications with pragmatic (albeit specific) issues:

1. Reduces overhead when training complex models
2. Drastically minimizes model training ETA
3. Centralized model storage enables
   1. continuous improvement (testing) pipelines,
   2. ensure reproducibility,
   3. encourages peer-review 

The context in which `dojo` is relevant on picture below:


![Dojo](Dojo.png)

## Architecture

Server looks for *messages* on a subscription-bus and, when one arrives, artefacts are properly receieved and stored. A message receieve event triggers *job* creation -- instruction for a group of workers -- which is placed on an execution queue.

Workers are constantly fetching for jobs to run and, when one arrives, retrieves artefacts required to execute said job. Workers may (not sure?) write metadata as a stream of messages, i.e. `stdout`, in a way that Server can expose training logs. 

![Dojo](Dojo&#32;Specifics.png)

## Development

An agile user-centered approach's being used. So a general common implicit mindset's *start easy, validate fast and evolve smartly*.

### Server

In order to serve many requests simultaneously, a pool of server-processes is created and each is then mapped to incoming requests on runtime. Multi-processing is chosen over multi-threaded because the latter is limited by python's GIL.

#### For now

Server won't run any real model training nor model serving. As it's a latter step, training and persisting are simulated by sleeping processes.

## Clients

#### For now

Client will start simple: simulate sending packs of commands - as requests in no specific order (for now). Simple requests are expected to inform if command was receieved successfully.