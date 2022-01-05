import requests
import logging
import os

from aiogram import Bot, Dispatcher, types

# log
logging.basicConfig(level=logging.INFO)

# handlers
async def starting(message: types.Message):
	try:
#		await message.reply('Привет, {0}!'.format(message.from_user.first_name))
		await message.answer('Write me the name of the pokemon (ang) or its sequence number from 1 to 898\n'
							'Напишите мне имя покемона (ang) или его порядковый номер от 1 до 898')
	except Exception:
		await message.answer('Error try again\nПопробуйте ещё раз')

async def pokemon_information(message: types.Message):
	try:
		pokemon_name = message.text.lower()
		api_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
		res = requests.get(api_url)
		#    print(res.status_code)

		if res.status_code == 200:
			res_json = res.json()
			ID = 0
			if res_json['id'] < 10:
				ID = 'ID: ' + '00' + str(res_json['id']) + '\n'
			if 10 < res_json['id'] < 100:
				ID = 'ID: ' + '0' + str(res_json['id']) + '\n'
			if res_json['id'] > 100:
				ID = 'ID: ' + str(res_json['id']) + '\n'
			name = 'Name/ Имя: ' + res_json['name'] + '\n'
			if res_json['height'] < 10:
				height = 'Height/ Рост: 0.' + str(res_json['height']) + ' m\n'
			else:
				height = 'Height/ Рост: ' + str(res_json['height'])[:1] + '.' + str(res_json['height'])[1:] + ' m\n'
			if res_json['weight'] < 100:
				weight = 'Weight/ Вес: ' + str(res_json['weight'])[:1] + '.' + str(res_json['weight'])[1:] + ' kg\n'
			else:
				weight = 'Weight/ Вес: ' + str(res_json['weight'])[:2] + '.' + str(res_json['weight'])[2:] + ' kg\n'
			base_experience = 'Base experience/ Начальный опыт: ' + str(res_json['base_experience']) + '\n'
			abilities = 'Abilities/ Способности: '
			for i in res_json['abilities']:
				abilities += i['ability']['name'] + ', '
			abilities = abilities[:-2]
			pokemon_total_info = ID + name + height + weight + base_experience + abilities
			photo_url = f'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{ID[-4:-1]}.png'
			await message.answer_photo(photo_url, caption=pokemon_total_info)

		else:
			await message.answer('Invalid pokemon name or id, please try again!\n'
								'Неверное имя покемона или id, попробуйте ещё раз!')
	except Exception:
		await message.answer('Error try again\nПопробуйте ещё раз')
# Selectel Lambda funcs
async def register_handlers(dp: Dispatcher):

	dp.register_message_handler(starting, commands=["start"])
	dp.register_message_handler(pokemon_information)

async def process_event(update, dp: Dispatcher):

	Bot.set_current(dp.bot)
	await dp.process_update(update)

# Selectel serverless entry point
async def main(**kwargs):
	bot = Bot(os.environ.get("TOKEN"))
	dp = Dispatcher(bot)

	await register_handlers(dp)

	update = types.Update.to_object(kwargs)
	await process_event(update, dp)

	return 'ok'