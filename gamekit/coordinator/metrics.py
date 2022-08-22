


from prometheus_client import Summary, Info

s = Summary('request_latency_seconds', 'Description of summary')

info = Info('mm', 'Matchmaker info')
info.info({
    'version': '1.2.3',
    'buildhost': 'foo@bar'
})

