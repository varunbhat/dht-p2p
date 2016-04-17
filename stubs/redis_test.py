import redis,json

r = redis.Redis(host='redis.varunbhat.in',
                port=6379)
#
# p = r.pubsub()
#
# p.subscribe('join')
#
# def hello(*args,**kwargs):
#     print args, kwargs
#
# p.subscribe(**{'join':hello})
#
# thread = p.run_in_thread(sleep_time=0.001)

r.publish('SERVER_GLOBAL_COMMANDS',json.dumps({'command':'restart_boostrap'}))

# keyss = {
#     'OUTGOING', 2,
#     'INCOMING', 1
# }
#
# keyss.update()
#
# print keyss.OUTGOING
