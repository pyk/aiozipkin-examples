import asyncio
import aiozipkin as az


async def run():
    # setup zipkin client
    zipkin_address = "http://localhost:9411"
    endpoint = az.create_endpoint("simple_service", 
                                  ipv4="127.0.0.1", 
                                  port=8080)
    tracer = az.create(zipkin_address, endpoint, sample_rate=1.0)

    # create and setup new trace
    with tracer.new_trace(sampled=True) as span:
        # give a name for the span
        span.name("Slow SQL")
        # tag with relevant information
        span.tag("span_type", "root")
        # indicate that this is client span
        span.kind(az.CLIENT)
        # make timestamp and name it with START SQL query
        span.annotate("START SQL SELECT * FROM")
        # imitate long SQL query
        await asyncio.sleep(0.1)
        # make other timestamp and name it "END SQL"
        span.annotate("END SQL")

    await tracer.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
