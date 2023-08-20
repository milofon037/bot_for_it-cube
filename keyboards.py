from aiogram import types

menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu.add(types.KeyboardButton('Узнать о направлениях🎓'))
menu.add(types.KeyboardButton('Поступить в IT-куб!'))
menu.add(types.KeyboardButton('Отмена❌'))

fields = types.InlineKeyboardMarkup(row_width=2)
fields.row(types.InlineKeyboardButton('Системное\nадминистрирование', callback_data='f_sa'),
           types.InlineKeyboardButton('Программирование\nна Python', callback_data='f_py'))
fields.row(types.InlineKeyboardButton('Разработка VR/AR\nприложений', callback_data='f_vr'),
           types.InlineKeyboardButton('Основы алгоритмики\nи логики', callback_data='f_al'))
fields.row(types.InlineKeyboardButton('Мобильная\nразработка', callback_data='f_it'),
           types.InlineKeyboardButton('Программирование\nроботов', callback_data='f_pr'))
fields.add(types.InlineKeyboardButton('Кибергигиена и работа с большими данными', callback_data='f_cb'))


sis_ad = types.InlineKeyboardMarkup(row_width=2)
sis_ad.row(types.InlineKeyboardButton('Навигатор',
                                      url='https://р26.навигатор.дети/program/14021-sistemnoe-administrirovanie'),
           types.InlineKeyboardButton('Расписание',
                                      callback_data='r_/sistemnoe-administrirovanie/'))
python = types.InlineKeyboardMarkup(row_width=2)
python.row(types.InlineKeyboardButton('Навигатор',
                                      url='https://р26.навигатор.дети/program/14062-programmirovanie-na-python'),
           types.InlineKeyboardButton('Расписание',
                                      callback_data='r_/programmirovanie-na-python-litsey-akademii-yandeksa/'))
vr_ar = types.InlineKeyboardMarkup(row_width=2)
vr_ar.row(types.InlineKeyboardButton('Навигатор',
                                     url='https://р26.навигатор.дети/program/14061-razrabotka-vrar-prilozhenii'),
          types.InlineKeyboardButton('Расписание',
                                     callback_data='r_/programmirovanie-na-python-litsey-akademii-yandeksa/'))
alg_log = types.InlineKeyboardMarkup(row_width=2)
alg_log.row(types.InlineKeyboardButton('Навигатор',
                                       url='https://р26.навигатор.дети/program/14071-osnovy-algoritmiki-i-logiki'))
cyber = types.InlineKeyboardMarkup(row_width=2)
cyber.row(types.InlineKeyboardButton('Навигатор',
                                     url='https://р26.навигатор.дети/program/14074-kibergigiena-i-rabota-s-bolshimi-dannymi'))

podacha = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Подать заявление!', callback_data='zayava1'))

napravlenie = types.InlineKeyboardMarkup()
napravlenie.row(types.InlineKeyboardButton('Системное\nадминистрирование',
                                           switch_inline_query_current_chat='системное администрирование'),
                types.InlineKeyboardButton('Python',
                                           switch_inline_query_current_chat='программирование на Python'))
napravlenie.row(types.InlineKeyboardButton('VR/AR',
                                           switch_inline_query_current_chat='VR/AR'),
                types.InlineKeyboardButton('Алгоритмика и логика',
                                           switch_inline_query_current_chat='алгоритмика и логика'))
napravlenie.add(types.InlineKeyboardButton('Кибергигиена и работа с большими данными',
                                           switch_inline_query_current_chat='Кибергигиена и работа с большими данными'))
