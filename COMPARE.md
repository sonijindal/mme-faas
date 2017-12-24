
Comparing few open source serverless platforms:

IronFunctions
* Import functions from AWS lambda and run it on other platforms by making it a docker image.
* Async functions using "type":"async"
* Logging support: Metrics can be used to decide upon scaling based upon the wait time.
* HTTP triggers.
* github stars: 1902

OpenFaas
* Serverless functions with docker and kubernetes
* UI portal
* Function in any language
* HTTP based
* collects Cloud Native metrics through Prometheus.
* Package any binary into a container
* Async using NATS (https://nats.io/documentation/streaming/nats-streaming-intro/)
* Triggers: HTTP, WIP for trigger event source (https://github.com/openfaas/faas/issues/400)
	http://jmkhael.io/downnotifier-site-pinger/
* github stars: 7706

Note : Easy to use.

OpenWhisk
* Plugged into Serverless framwork
* Kafka queue from ngnix to functions
* Support for event triggers like location updates, emails, HTTP call, database state change etc.
* github stars: 2243

nuclio
* For high performance events and data processing
* A single function instance can process hundreds of thousands of HTTP requests or data records per second
* pluggable event sources (http, message queue, stream)
* pluggable data services.
* sync and async event sources.
* github stars: 1073

Note: Feature rich but looks complex.

Fission
* Serverless functions with kubernetes
* Fission supports HTTP routes as triggers today, with upcoming support for other types of event triggers, such as timers and Kubernetes events.
* A trigger is something that maps an event to a function; Fission supports HTTP routes as triggers today, with upcoming support for other types of event triggers, such as timers and Kubernetes events.
* github stars: 2820

Note: It is in early alpha
