import requests
from aiogram import Bot, Dispatcher, executor, types
import logging

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def starting(message: types.Message):
    await bot.send_message(message.chat.id, 'Write me the name of the pokemon (ang) or its sequence number from 1 to 898\n'
                                            'Напишите мне имя покемона (ang) или его порядковый номер от 1 до 898')

@dp.message_handler()
async def pokemon_information(message: types.Message):
    pokemon_name = message.text.lower()
    api_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
    res = requests.get(api_url)
#    print(res.status_code)

    if res.status_code == 404:
        await bot.send_message(message.chat.id, 'Invalid pokemon name or id, please try again!\n'
                                                'Неверное имя покемона или id, попробуйте ещё раз!')
    else:
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
        await bot.send_photo(message.chat.id, photo=photo_url, caption=pokemon_total_info)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)