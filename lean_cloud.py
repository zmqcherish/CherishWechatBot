import leancloud
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s', level=logging.INFO, datefmt='%m-%d %H:%M:%S')
leancloud.init("")

HitoItem = leancloud.Object.extend('HitoItem')
query = leancloud.Query(HitoItem)

def except_decorative(func):
	def decorator(*args, **keyargs):
		try:
			return func(*args, **keyargs)
		except Exception as e:
			logging.error(f'handle {func.__name__} error: {e}')
	return decorator


# def create_int():
# 	obj = HitoItem()
# 	obj.set('cid', '19830330')
# 	obj.set('update', True)
# 	obj.save()


@except_decorative
def find_by_cid(cid):
	a = query.equal_to('cid', cid).find()
	if len(a) > 0:
		return a[0]


def save_val(cid, count, name):
	obj = HitoItem()
	obj.set('cid', cid)
	obj.set('count', count)
	obj.set('name', name)
	obj.save()


def update_val(cid, count):
	item = find_by_cid(cid)
	if not item:
		return
	item.set('count', count)
	where = HitoItem.query.equal_to('cid', cid)
	item.save(where=where)


def update_update(val):
	cql = 'update HitoItem set update = ? where objectId = ?'
	result = leancloud.Query.do_cloud_query(cql, val, '5c305f460b61600067656668')


if __name__ == '__main__':
	# create_int()
	# save_val('1', 123)
	update_update(False)
	# update_val('1231',213213)
	# a = find_by_cid('123')