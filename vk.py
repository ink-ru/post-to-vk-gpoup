#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
https://github.com/python273/vk_api
'''

def main():

	import sys, os, pickle

	try:
		import vk_api 
	except ImportError:
		print("vk_api module havn't been found. Use - pip3 install vk_api")

	old_posts = {}

	if os.path.isfile('data.pickle') and os.stat('data.pickle').st_size != 0:
		try:
			with open('data.pickle', 'rb') as f:
				old_posts = pickle.load(f)
		except pickle.UnpicklingError as e:
			# normal, somewhat expected
			pass
		except (AttributeError,  EOFError, ImportError, IndexError) as e:
			# secondary errors
			print(traceback.format_exc(e))
			pass
		except Exception as e:
			# everything else, possibly fatal
			print(traceback.format_exc(e))
			return
	
	vk_session = vk_api.VkApi(token = 'c61e61b21016b5aca557f1224be364feeca669f4569fdd89839f43e', app_id = '6104766', client_secret = '8ycPU2gaIzGkQmimoZoZ')

	try:
		vk = vk_session.get_api()
	except vk_api.AuthError as error_msg:
		print(error_msg)
		vk_session = vk_api.VkApi(login = '+79001234567', password = 'YouPassword')
		vk_session.auth()
		vk = vk_session.get_api()
	# finally:
		# sys.exit(os.EX_NOPERM)


	remote_wall = vk.wall.get(count=1, owner_id='-140852373')  # Используем метод wall.get

	if 'remote_wall' in locals() and remote_wall['items']:
		if remote_wall['items'][0]['id'] in old_posts:
			print('old post')
		else:
			print(remote_wall['items'][0]['id'])
			old_posts[remote_wall['items'][0]['id']] = remote_wall['items'][0]['date']

			# for attachment in remote_wall['items'][0]['attachments']:
			# 	print(remote_wall['items'][0]['attachments'][0]['type'])

			if remote_wall['items'][0]['attachments'][0]['type'] == 'photo':
				ph = remote_wall['items'][0]['attachments'][0]['type']+str(remote_wall['items'][0]['attachments'][0]['photo']['owner_id'])+'_'+str(remote_wall['items'][0]['attachments'][0]['photo']['id'])
				print(vk.wall.post(message=remote_wall['items'][0]['text'], attachments=ph, owner_id='-145559733', from_group='1'))
	else:
		print('empty response')


	with open('data.pickle', 'wb') as f:
		pickle.dump(old_posts, f)

	sys.exit(os.EX_OK) # code 0, all ok

if __name__ == '__main__':
	main()
else:
	sys.exit(os.EX_USAGE) # https://docs.python.org/2/library/os.html
