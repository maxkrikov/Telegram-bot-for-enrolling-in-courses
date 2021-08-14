import math
import telebot
import config
import random
from telebot import types
import sqlite3

global numerkursr1
global numerkursr2
global numerkursr3
global numk2
numerkursr1 = 0
numerkursr2 = 0
numerkursr3 = 0
numk2 = 0

bot = telebot.TeleBot(config.TOKEN)

def p():
	global db
	global sql
	db = sqlite3.connect('server.db')
	sql = db.cursor()

def ctus():
	p()

	sql.execute("""CREATE TABLE IF NOT EXISTS user (
		users INTEGER,
		fiogg TEXT,
		nomer INTEGER,
		adm INTEGER,
		prosmkurs INTEGER,
		prosmkurs2 INTEGER,
		vibran INTEGER
	)""")

	db.commit()

def ctkurs():
	p()

	sql.execute("""CREATE TABLE IF NOT EXISTS kurs (
		numerkurs INTEGER,
		predm TEXT,
		fiouch TEXT,
		stoimost INTEGER,
		vremyo TEXT,
		kartina INTEGER
	)""")

	db.commit()

def ctspisok():
	p()

	sql.execute("""CREATE TABLE IF NOT EXISTS spisok (
		numerkurs INTEGER,
		fioc TEXT,
		nomerk INTEGER
	)""")


def addkurs(message):
	numkurs = bot.send_message(message.chat.id, "Введите номер курса.")
	bot.register_next_step_handler(numkurs, addkurs2)


def addkurs2(message):
	p()

	
	if message.text.isdigit():
		
		numk = int(message.text)
		global numk2
		numk2 = numk
		sql.execute(f"SELECT numerkurs FROM kurs WHERE numerkurs = {numk}")
		data = sql.fetchone()
		if data is None:
			sql.execute(f"INSERT INTO kurs VALUES ({numk}, 'None', 'None', '0', 'None', '0');")
			db.commit()
		for c in sql.execute(f"SELECT numerkurs FROM kurs WHERE numerkurs = {numk}"):
			global numerkurser
			numerkurser = c[0]
		numkurs = bot.send_message(message.chat.id, "Введите ФИО преподователя.")
		bot.register_next_step_handler(numkurs, addkurs3)
	else:
		menu(message)



def addkurs3(message):
	p()
	global numerkurser
	if message.text.isdigit():
		menu(message)
	else:
		prepod = str(message.text)
		sql.execute(f'UPDATE kurs SET fiouch = "{prepod}" WHERE numerkurs = {numerkurser}')
		db.commit()
		numkurs = bot.send_message(message.chat.id, "Введите cтоимость курса.")
		bot.register_next_step_handler(numkurs, addkurs4)
def addkurs4(message):
	p()
	global numerkurser
	
	if message.text.isdigit():
		stoimostk = int(message.text)
		sql.execute(f'UPDATE kurs SET stoimost = {stoimostk} WHERE numerkurs = {numerkurser}')
		db.commit()
		predmkurs = bot.send_message(message.chat.id, "Введите название курса.")
		bot.register_next_step_handler(predmkurs, addkurs5)
	else:
		menu(message)
def addkurs5(message):
	p()
	global numerkurser
	if message.text.isdigit():
		menu(message)
	else:
		predmet = str(message.text)
		sql.execute(f'UPDATE kurs SET predm = "{predmet}" WHERE numerkurs = {numerkurser}')
		db.commit()
		vremy = bot.send_message(message.chat.id, "Введите время проведения курса.")
		bot.register_next_step_handler(vremy, addkurs6)

def addkurs6(message):
	p()
	global numerkurser
	if message.text.isdigit():
		menu(message)
	else:
		vvod = str(message.text)
		sql.execute(f'UPDATE kurs SET vremyo = "{vvod}" WHERE numerkurs = {numerkurser}')
		db.commit()
		
		kursi = types.InlineKeyboardMarkup(row_width=5)
		mi1 = types.InlineKeyboardButton('Да', callback_data='dat1')
		mi2 = types.InlineKeyboardButton('Нет', callback_data='net1')
		kursi.add(mi1, mi2)
		bot.send_message(message.chat.id, "Добавить ли картинку в подробную информацию курса?", reply_markup=kursi)

		

def reg(message):
	pid = message.chat.id
	sql.execute(f"SELECT users FROM user WHERE users = {pid}")
	data = sql.fetchone()
	if data is None:
		sql.execute(f"INSERT INTO user VALUES ({pid}, 'None', '0', '0', '0', '0', '0');")
		db.commit()

def dan(message):
	pid = message.chat.id
	for b in sql.execute(f"SELECT fiogg FROM user WHERE users = {pid}"):
		global FIOPOL
		FIOPOL = b[0]

def danad(message):
	p()
	pid = message.chat.id
	for b in sql.execute(f"SELECT adm FROM user WHERE users = {pid}"):
		global adm
		adm = b[0]

def prosmotorkurs(message):
	pid = message.chat.id
	for b in sql.execute(f"SELECT prosmkurs FROM user WHERE users = {pid}"):
		global prosmotr
		prosmotr = b[0]

def prosmotorkurs2(message):
	pid = message.chat.id
	for b in sql.execute(f"SELECT prosmkurs2 FROM user WHERE users = {pid}"):
		global prosmotr2
		prosmotr2 = b[0]

def infag(message):
	p()
	prosmotorkurs(message)
	for ab in sql.execute(f"SELECT numerkurs FROM kurs WHERE numerkurs = {prosmotr}"):
		global numerkursr1
		numerkursr1 = ab[0]

	for ca in sql.execute(f"SELECT numerkurs FROM kurs WHERE numerkurs = {prosmotr + 1}"):
		global numerkursr2
		numerkursr2 = ca[0]

	for bc in sql.execute(f"SELECT numerkurs FROM kurs WHERE numerkurs = {prosmotr + 2}"):
		global numerkursr3
		numerkursr3 = bc[0]

def spiskurs_bot(message):
	p()
	for b in sql.execute("SELECT Count(*) FROM kurs"):
		numkur = b[0]


	if numkur == 0:
		bot.send_message(message.chat.id, "Курсы не найдены")
	else:
		pid = message.chat.id
		prosmotorkurs2(message)
		



		gdjgn = numkur / 3
		opop = math.ceil(gdjgn)
		opopop = int(gdjgn)
		jojojo = gdjgn - opopop

		jojojo2 = round(jojojo, 2)

		gdjgn1 = round(gdjgn, 2)


		if gdjgn1 == 0.67:
			prosmotorkurs(message)
			predmet1 = 0
			predmet2 = 0
			predmet3 = 0

			for a in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr}"):
				predmet1 = a[0]
			for b in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr + 1}"):
				predmet2 = b[0]
			

			infag(message)
			kursi = types.InlineKeyboardMarkup(row_width=5)
			mi1 = types.InlineKeyboardButton(predmet1, callback_data=numerkursr1)
			mi2 = types.InlineKeyboardButton(predmet2, callback_data=numerkursr2)
			mi10 = types.InlineKeyboardButton('Вернуться в меню', callback_data='men')
			kursi.add(mi1)
			kursi.add(mi2)
			kursi.add(mi10)


			
		
			bot.send_message(message.chat.id, "Доступные курсы:", reply_markup=kursi)
			bot.send_message(message.chat.id, "Нажмите на название курса для просмотра подробной информации", reply_markup=types.ReplyKeyboardRemove())
		
		elif gdjgn1 == 0.33:
			prosmotorkurs(message)
			predmet1 = 0
			predmet2 = 0
	
			for a in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr}"):
				predmet1 = a[0]


			infag(message)
			kursi = types.InlineKeyboardMarkup(row_width=5)
			mi1 = types.InlineKeyboardButton(predmet1, callback_data=numerkursr1)
			mi10 = types.InlineKeyboardButton('Вернуться в меню', callback_data='men')

			kursi.add(mi1)
			kursi.add(mi10)



			

		
			bot.send_message(message.chat.id, "Доступные курсы:", reply_markup=kursi)
			bot.send_message(message.chat.id, "Нажмите на название курса для просмотра подробной информации", reply_markup=types.ReplyKeyboardRemove())

		else:
			if prosmotr2 >= opop:
				predmet1 = 0
				predmet2 = 0
				predmet3 = 0
			
				prosmotorkurs(message)
				if jojojo2 == 0.33:
					for a in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr}"):
						predmet1 = a[0]

				elif jojojo2 == 0.67:
			

					for a in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr}"):
						predmet1 = a[0]
					for b in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr + 1}"):
						predmet2 = b[0]
				else:
					for a in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr}"):
						predmet1 = a[0]
					for b in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr + 1}"):
						predmet2 = b[0]
					for c in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr + 2}"):
						predmet3 = c[0]

		
				infag(message)
				kursi = types.InlineKeyboardMarkup(row_width=5)
				mi1 = types.InlineKeyboardButton(predmet1, callback_data=numerkursr1)
				mi2 = types.InlineKeyboardButton(predmet2, callback_data=numerkursr2)
				mi3 = types.InlineKeyboardButton(predmet3, callback_data=numerkursr3)
				mi4 = types.InlineKeyboardButton("Назад", callback_data='naz')
				mi10 = types.InlineKeyboardButton('Вернуться в меню', callback_data='men')

				if jojojo2 == 0.33:
					kursi.add(mi1)
				elif jojojo2 == 0.67:
					kursi.add(mi1)
					kursi.add(mi2)
				else:
					kursi.add(mi1)
					kursi.add(mi2)
					kursi.add(mi3)


				kursi.add(mi4)
				kursi.add(mi10)
			
			
				bot.send_message(message.chat.id, "Доступные курсы:", reply_markup=kursi)
				bot.send_message(message.chat.id, "Нажмите на название курса для просмотра подробной информации", reply_markup=types.ReplyKeyboardRemove())

				
			elif prosmotr2 == 1:
				predmet1 = 0
				predmet2 = 0
				predmet3 = 0
		
				prosmotorkurs(message)
				
				for a in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr}"):
					predmet1 = a[0]
				for b in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr + 1}"):
					predmet2 = b[0]
				for c in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr + 2}"):
					predmet3 = c[0]


				infag(message)
				kursi = types.InlineKeyboardMarkup(row_width=5)
				mi1 = types.InlineKeyboardButton(predmet1, callback_data=numerkursr1)
				mi2 = types.InlineKeyboardButton(predmet2, callback_data=numerkursr2)
				mi3 = types.InlineKeyboardButton(predmet3, callback_data=numerkursr3)
				mi4 = types.InlineKeyboardButton("Вперёд", callback_data='vper')
				mi10 = types.InlineKeyboardButton('Вернуться в меню', callback_data='men')

				
				
				kursi.add(mi1)
				kursi.add(mi2)
				kursi.add(mi3)
				kursi.add(mi4)
				kursi.add(mi10)
		
			
				bot.send_message(message.chat.id, "Доступные курсы:", reply_markup=kursi)
				bot.send_message(message.chat.id, "Нажмите на название курса для просмотра подробной информации", reply_markup=types.ReplyKeyboardRemove())

			else:
				prosmotorkurs(message)
				for a in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr}"):
					predmet1 = a[0]
				for b in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr + 1}"):
					predmet2 = b[0]
				for c in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {prosmotr + 2}"):
					predmet3 = c[0]

				infag(message)
				kursi = types.InlineKeyboardMarkup(row_width=5)
				mi1 = types.InlineKeyboardButton(predmet1, callback_data=numerkursr1)
				mi2 = types.InlineKeyboardButton(predmet2, callback_data=numerkursr2)
				mi3 = types.InlineKeyboardButton(predmet3, callback_data=numerkursr3)
				mi5 = types.InlineKeyboardButton("Вперёд", callback_data='vper')
				mi4 = types.InlineKeyboardButton("Назад", callback_data='naz')
				mi10 = types.InlineKeyboardButton('Вернуться в меню', callback_data='men')

				kursi.add(mi1)
				kursi.add(mi2)
				kursi.add(mi3)
				kursi.add(mi4, mi5)
				kursi.add(mi10)



				bot.send_message(message.chat.id, "Доступные курсы:", reply_markup=kursi)
				bot.send_message(message.chat.id, "Нажмите на название курса для просмотра подробной информации", reply_markup=types.ReplyKeyboardRemove())
		infag(message)
		print()
		



def menu(message):
	p()
	dan(message)
	pid = message.chat.id
	if FIOPOL == 'None':
		FIO1 = bot.send_message(message.chat.id, "Привет, я бот для записи на курсы введите своё ФИО.")
		bot.register_next_step_handler(FIO1, dann)
	else:
		danad(message)
		menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Доступные курсы")
		item2 = types.KeyboardButton("Мои курсы")
		item3 = types.KeyboardButton("Админ меню")
		menu.add(item2, item1)
		if adm == 1:
			menu.add(item3)
		bot.send_message(message.chat.id, "Выбирите одну из функций:", reply_markup=menu)
def dann(message):
	p()
	global fiopg
	fiopg = str(message.text)
	pid = message.chat.id
	sql.execute(f'UPDATE user SET fiogg = "{fiopg}" WHERE users = {pid}')
	db.commit()
	num = bot.send_message(message.chat.id, "Введите свой номер телефона.")
	bot.register_next_step_handler(num, number)
def number(message):
	p()
	if message.text.isdigit():
		nomerok = int(message.text)
		pid = message.chat.id
		sql.execute(f'UPDATE user SET nomer = {nomerok} WHERE users = {pid}')
		db.commit()
		menu(message)
	else:
		menu(message)

def fioforspisq(message):
	p()
	pid = message.chat.id
	for b in sql.execute(f"SELECT fiogg FROM user WHERE users = {pid}"):
		global fioforspis
		fioforspis = b[0]

def nomerforspisq(message):
	p()
	pid = message.chat.id
	for b in sql.execute(f"SELECT nomer FROM user WHERE users = {pid}"):
		global nomerforspis
		nomerforspis = b[0]



def delet_kurs(message):
	
	delkurs = bot.send_message(message.chat.id, "Введите номер курса для удаления.")
	bot.register_next_step_handler(delkurs, del_kurs)
	

def del_kurs(message):
	p()
	if message.text.isdigit():
		chislo = int(message.text)
		sql.execute(f"SELECT numerkurs FROM kurs WHERE numerkurs = {chislo}")
		data = sql.fetchone()
		if data is None:
			bot.send_message(message.chat.id, f"Курс под номером {chislo} не найден!")
		else:
			sql.execute(f'DELETE FROM kurs WHERE numerkurs = {chislo}')
			db.commit()
			bot.send_message(message.chat.id, "Курс успешно удалён!")
	else:
		menu(message)

def spiszapis(message):
	p()
	i = 1

	for b in sql.execute("SELECT Count(*) FROM kurs"):
		numkur = b[0]

	
	if numkur == 0:
		bot.send_message(message.chat.id, "Курсы не найдены")
	else:
		for a in range(numkur):
			for c in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {i}"):
				numkure = c[0]
			for c in sql.execute(f"SELECT numerkurs FROM kurs WHERE numerkurs = {i}"):
				numkurfe = c[0]	
			i = i + 1
			print(numkure)

			sql.execute(f"SELECT fioc FROM spisok WHERE numerkurs = {numkurfe}")
			data = sql.fetchall()
			for row in data:
				sql.execute(f"SELECT nomerk FROM spisok WHERE fioc = '{row[0]}'")
				data2 = sql.fetchall()
				bot.send_message(message.chat.id, f"{row[0]}({data2[0][0]}) записан на {numkure}")
			
		
def moikurs(message):
	p()
	gohome = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Меню")
	gohome.add(item1)

	i = 1

	gtg = 0
	for b in sql.execute("SELECT Count(*) FROM kurs"):
		numkur = b[0]
	fioforspisq(message)
	for lol in sql.execute(f"SELECT fioc FROM spisok WHERE fioc = '{fioforspis}'"):
		gtg = lol[0]
	for b in sql.execute(f"SELECT Count(*) FROM spisok WHERE fioc = '{gtg}'"):
		numkur23 = b[0]
	
	if numkur == 0:
		bot.send_message(message.chat.id, "Курсы не найдены.")
	else:
		if gtg == 0:
			bot.send_message(message.chat.id, "Вы не записанны на курсы.")
		else:
			for a in range(numkur):

				for c in sql.execute(f"SELECT numerkurs FROM kurs WHERE numerkurs = {i}"):
					numkurfe = c[0]	
				i = i + 1

				sql.execute(f"SELECT numerkurs FROM spisok WHERE numerkurs = {numkurfe}")
				data = sql.fetchall()
				for row in data:
					for row34 in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {row[0]}"):
						abc = row34[0]
					for row35 in sql.execute(f"SELECT fiouch FROM kurs WHERE numerkurs = {row[0]}"):
						abcd = row35[0]
					for row36 in sql.execute(f"SELECT stoimost FROM kurs WHERE numerkurs = {row[0]}"):
						abcde = row36[0]
					for row37 in sql.execute(f"SELECT vremyo FROM kurs WHERE numerkurs = {row[0]}"):
						abcdef = row37[0]
					bot.send_message(message.chat.id, f"Курс номер: {row[0]} - {abc}, у преподователя {abcd}(цена этого курса:{abcde}), он будет проходить: {abcdef}")

			otpkurs = bot.send_message(message.chat.id, "Введите номер курса что бы отписаться.", reply_markup=gohome)
			bot.register_next_step_handler(otpkurs, otpkursd)

def otpkursd(message):

	if message.text.isdigit():
		nkdo = int(message.text)
		fioforspisq(message)
		sql.execute(f'DELETE FROM spisok WHERE numerkurs = {nkdo} AND fioc = "{fioforspis}"')
		db.commit()
		bot.send_message(message.chat.id, "Вы успешно отписались от курса!")
	else:
		menu(message)
	




def infa1(message):
	p()
	infag(message)
	pid = message.chat.id
	for row34 in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {numerkursr1}"):
		abc = row34[0]
	for row35 in sql.execute(f"SELECT fiouch FROM kurs WHERE numerkurs = {numerkursr1}"):
		abcd = row35[0]
	for row36 in sql.execute(f"SELECT stoimost FROM kurs WHERE numerkurs = {numerkursr1}"):
		abcde = row36[0]
	for row37 in sql.execute(f"SELECT vremyo FROM kurs WHERE numerkurs = {numerkursr1}"):
		abcdef = row37[0]
	for row38 in sql.execute(f"SELECT kartina FROM kurs WHERE numerkurs = {numerkursr1}"):
		abcdefgh = row38[0]

	sql.execute(f'UPDATE user SET vibran = {numerkursr1} WHERE users = {pid}')
	db.commit()


	for row38 in sql.execute(f"SELECT vibran FROM user WHERE users = {pid}"):
		global vubor
		vubor = row38[0]
	if abcdefgh == 1:
		bot.send_photo(message.chat.id, open(f'{numerkursr1}.png', 'rb'))
	bot.send_message(message.chat.id, f"Курс - {abc}(цена:{abcde}), преподователь - {abcd}, время провидения - {abcdef} ")

	vopr = types.InlineKeyboardMarkup(row_width=5)
	item1 = types.InlineKeyboardButton('Да', callback_data='dat')
	item2 = types.InlineKeyboardButton('Нет', callback_data='net')
	vopr.add(item1, item2)
	bot.send_message(message.chat.id, f"Хотите ли вы записаться на этот курс?", reply_markup=vopr)
def infa2(message):
	p()
	infag(message)
	pid = message.chat.id
	for row34 in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {numerkursr2}"):
		abc = row34[0]
	for row35 in sql.execute(f"SELECT fiouch FROM kurs WHERE numerkurs = {numerkursr2}"):
		abcd = row35[0]
	for row36 in sql.execute(f"SELECT stoimost FROM kurs WHERE numerkurs = {numerkursr2}"):
		abcde = row36[0]
	for row37 in sql.execute(f"SELECT vremyo FROM kurs WHERE numerkurs = {numerkursr2}"):
		abcdef = row37[0]
	for row38 in sql.execute(f"SELECT kartina FROM kurs WHERE numerkurs = {numerkursr2}"):
		abcdefgh = row38[0]

	sql.execute(f'UPDATE user SET vibran = {numerkursr2} WHERE users = {pid}')
	db.commit()


	for row38 in sql.execute(f"SELECT vibran FROM user WHERE users = {pid}"):
		global vubor
		vubor = row38[0]

	if abcdefgh == 1:
		bot.send_photo(message.chat.id, open(f'{numerkursr2}.png', 'rb'))

	bot.send_message(message.chat.id, f"Курс - {abc}(цена:{abcde}), преподователь - {abcd}, время провидения - {abcdef} ")
	
	vopr = types.InlineKeyboardMarkup(row_width=5)
	item1 = types.InlineKeyboardButton('Да', callback_data='dat')
	item2 = types.InlineKeyboardButton('Нет', callback_data='net')
	vopr.add(item1, item2)
	bot.send_message(message.chat.id, f"Хотите ли вы записаться на этот курс?", reply_markup=vopr)
def infa3(message):
	p()
	infag(message)
	pid = message.chat.id
	for row34 in sql.execute(f"SELECT predm FROM kurs WHERE numerkurs = {numerkursr3}"):
		abc = row34[0]
	for row35 in sql.execute(f"SELECT fiouch FROM kurs WHERE numerkurs = {numerkursr3}"):
		abcd = row35[0]
	for row36 in sql.execute(f"SELECT stoimost FROM kurs WHERE numerkurs = {numerkursr3}"):
		abcde = row36[0]
	for row37 in sql.execute(f"SELECT vremyo FROM kurs WHERE numerkurs = {numerkursr3}"):
		abcdef = row37[0]
	for row38 in sql.execute(f"SELECT kartina FROM kurs WHERE numerkurs = {numerkursr3}"):
		abcdefgh = row38[0]

	sql.execute(f'UPDATE user SET vibran = {numerkursr3} WHERE users = {pid}')
	db.commit()

	for row38 in sql.execute(f"SELECT vibran FROM user WHERE users = {pid}"):
		global vubor
		vubor = row38[0]

	if abcdefgh == 1:
		bot.send_photo(message.chat.id, open(f'{numerkursr3}.png', 'rb'))

	bot.send_message(message.chat.id, f"Курс - {abc}(цена:{abcde}), преподователь - {abcd}, время провидения - {abcdef} ")
	
	vopr = types.InlineKeyboardMarkup(row_width=5)
	item1 = types.InlineKeyboardButton('Да', callback_data='dat')
	item2 = types.InlineKeyboardButton('Нет', callback_data='net')
	vopr.add(item1, item2)
	bot.send_message(message.chat.id, f"Хотите ли вы записаться на этот курс?", reply_markup=vopr)
def proverka(message):
	p()
	pid = message.chat.id
	for b in sql.execute(f"SELECT vibran FROM user WHERE users = {pid}"):
		global vibranan
		vibranan = b[0]

def uspzapisnakurs(message):
	p()
	proverka(message)
	pid = message.chat.id
	for b in sql.execute(f"SELECT fiogg FROM user WHERE users = {pid}"):
		fiopol = b[0]
	pid = message.chat.id
	for b in sql.execute(f"SELECT nomer FROM user WHERE users = {pid}"):
		nomerc = b[0]


	sql.execute(f"SELECT numerkurs FROM spisok WHERE numerkurs = {vubor} AND fioc = '{fiopol}'")
	data = sql.fetchone()
	if data is None:
		sql.execute(f"INSERT INTO spisok VALUES ({vubor}, '{fiopol}', {nomerc});")
		db.commit()
		bot.send_message(message.chat.id, "Вы успешно записанны на курс!")
		if vibranan == 0:
			menu(message)
		else:
			pid = message.chat.id
			sql.execute(f'UPDATE user SET vibran = {0} WHERE users = {pid}')
			db.commit()

			pid = message.chat.id
			sql.execute(f'UPDATE user SET prosmkurs = {0} WHERE users = {pid}')
			db.commit()
				
			pid = message.chat.id
			sql.execute(f'UPDATE user SET prosmkurs2 = {0} WHERE users = {pid}')
			db.commit()
			menu(message)
	else:
		bot.send_message(message.chat.id, f"Вы уже записанны на этот курс.")
		menu(message)

	




@bot.message_handler(commands=['start'])
def send_welcome(message):
	p()
	ctus()
	ctkurs()
	ctspisok()
	reg(message)
	menu(message)
	pid = message.chat.id
	sql.execute(f'UPDATE user SET prosmkurs = {0} WHERE users = {pid}')
	db.commit()
		
	pid = message.chat.id
	sql.execute(f'UPDATE user SET prosmkurs2 = {0} WHERE users = {pid}')
	db.commit()

	pid = message.chat.id
	sql.execute(f'UPDATE user SET vibran = {0} WHERE users = {pid}')
	db.commit()
		


	




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

	infag(call.message)




	if call.message:

		if call.data == 'dat1':
			p()
			bot.send_message(call.message.chat.id, "Предупреждение! К этому курсу была добавлена возможность прикреплять картинку, ОБЯЗАТЕЛЬНО сейчас нужно добавить картинку в папку к скрипту бота в формате номеркурса.png")
			bot.send_message(call.message.chat.id, "Курс успешно создан!")
			sql.execute(f'UPDATE kurs SET kartina = {1} WHERE numerkurs = {numk2}')
			db.commit()


		elif call.data == 'net1':
			p()
			sql.execute(f'UPDATE kurs SET kartina = {0} WHERE numerkurs = {numk2}')
			db.commit()
			bot.send_message(call.message.chat.id, "Курс успешно создан!")

		elif call.data == 'vper':
			p()
			pid = call.message.chat.id
			
			prosmotorkurs2(call.message)
			sql.execute(f'UPDATE user SET prosmkurs2 = {prosmotr2 + 1} WHERE users = {pid}')
			db.commit()
			

			prosmotorkurs(call.message)
			sql.execute(f'UPDATE user SET prosmkurs = {prosmotr + 3} WHERE users = {pid}')
			db.commit()

			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Доступные курсы:",   reply_markup=None)
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.delete_message(call.message.chat.id, call.message.message_id+1)

			spiskurs_bot(call.message)

		elif call.data == 'naz':
			p()
			pid = call.message.chat.id
			
			prosmotorkurs2(call.message)
			sql.execute(f'UPDATE user SET prosmkurs2 = {prosmotr2 - 1} WHERE users = {pid}')
			db.commit()
			

			prosmotorkurs(call.message)
			sql.execute(f'UPDATE user SET prosmkurs = {prosmotr - 3} WHERE users = {pid}')
			db.commit()

			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Доступные курсы:",   reply_markup=None)
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.delete_message(call.message.chat.id, call.message.message_id+1)

			spiskurs_bot(call.message)

		elif call.data == str(numerkursr1):
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Доступные курсы:",   reply_markup=None)
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.delete_message(call.message.chat.id, call.message.message_id+1)
			pid = call.message.chat.id
			p()

			prosmotorkurs2(call.message)
			infa1(call.message)


			

			
		elif call.data == str(numerkursr2):
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Доступные курсы:",   reply_markup=None)
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.delete_message(call.message.chat.id, call.message.message_id+1)
			pid = call.message.chat.id
			p()

			prosmotorkurs2(call.message)
			infa2(call.message)


		elif call.data == str(numerkursr3):
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Доступные курсы:",   reply_markup=None)
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.delete_message(call.message.chat.id, call.message.message_id+1)
			pid = call.message.chat.id
			p()

			prosmotorkurs2(call.message)
			infa3(call.message)



		elif call.data == 'men':
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Доступные курсы:",   reply_markup=None)
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.delete_message(call.message.chat.id, call.message.message_id+1)
			pid = call.message.chat.id
			p()

			sql.execute(f'UPDATE user SET prosmkurs = {0} WHERE users = {pid}')
			db.commit()

			sql.execute(f'UPDATE user SET prosmkurs2 = {0} WHERE users = {pid}')
			db.commit()

			pid = call.message.chat.id
			sql.execute(f'UPDATE user SET vibran = {0} WHERE users = {pid}')
			db.commit()

			prosmotorkurs2(call.message)
			menu(call.message)
		elif call.data == 'dat':
			proverka(call.message)
			if vibranan > 0:
				uspzapisnakurs(call.message)
			else:
				bot.send_message(call.message.chat.id, "Я не знаю такой команды")
				menu(call.message)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Хотите ли вы записаться на этот курс?",   reply_markup=None)
			bot.delete_message(call.message.chat.id, call.message.message_id)
		elif call.data == 'net':
			p()
			proverka(call.message)

			if vibranan > 0:
				spiskurs_bot(call.message)
				pid = call.message.chat.id
				sql.execute(f'UPDATE user SET vibran = {0} WHERE users = {pid}')
				db.commit()
				infag(call.message)
			else:
				bot.send_message(call.message.chat.id, "Я не знаю такой команды")
				menu(call.message)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Хотите ли вы записаться на этот курс?",   reply_markup=None)
			bot.delete_message(call.message.chat.id, call.message.message_id)



@bot.message_handler(content_types=['text'])
def read(message):
	pid = message.chat.id
	if message.text == config.ADMPASSWORD:
		p()
		sql.execute(f'UPDATE user SET adm = {1} WHERE users = {pid}')
		db.commit()
		bot.send_message(message.chat.id, "Админ права выданы")
		menu(message)
	elif message.text == 'Админ меню':
		danad(message)
		if adm == 1:
			menu5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton("Просмотр доступных курсов")
			item2 = types.KeyboardButton("Создание и редактирование курсов")
			item3 = types.KeyboardButton("Список записавшихся")
			item4 = types.KeyboardButton("Меню")
			item5 = types.KeyboardButton("Удалить курс")
			menu5.add(item2, item1, item3)
			menu5.add(item4, item5)
			bot.send_message(message.chat.id, "Выбирите одну из функций:", reply_markup=menu5)
		else:
			bot.send_message(message.chat.id, "Вы не админ")
	elif message.text == "Создание и редактирование курсов":
		danad(message)
		if adm == 1:
			ctkurs()
			addkurs(message)
		else:
			bot.send_message(message.chat.id, "Вы не админ")
	elif message.text == "Просмотр доступных курсов":
		danad(message)
		if adm == 1:
			p()

			sql.execute(f'UPDATE user SET prosmkurs = {1} WHERE users = {pid}')
			db.commit()
			sql.execute(f'UPDATE user SET prosmkurs2 = {1} WHERE users = {pid}')
			db.commit()
			spiskurs_bot(message)
			infag(message)
		else:
			bot.send_message(message.chat.id, "Вы не админ")
	elif message.text == "Удалить курс":
		danad(message)
		if adm == 1:
			delet_kurs(message)
		else:
			bot.send_message(message.chat.id, "Вы не админ")
		

	elif message.text == 'Доступные курсы':
		p()

		sql.execute(f'UPDATE user SET prosmkurs = {1} WHERE users = {pid}')
		db.commit()
		sql.execute(f'UPDATE user SET prosmkurs2 = {1} WHERE users = {pid}')
		db.commit()
		spiskurs_bot(message)
		infag(message)
	elif message.text == 'Меню':
		p()
		menu(message)
		pid = message.chat.id

		sql.execute(f'UPDATE user SET prosmkurs = {0} WHERE users = {pid}')
		db.commit()

		sql.execute(f'UPDATE user SET prosmkurs2 = {0} WHERE users = {pid}')
		db.commit()


		sql.execute(f'UPDATE user SET vibran = {0} WHERE users = {pid}')
		db.commit()
		prosmotorkurs2(message)
	elif message.text == 'Список записавшихся':
		danad(message)
		if adm == 1:
			spiszapis(message)
		else:
			bot.send_message(message.chat.id, "Вы не админ")

		
	elif message.text == 'Мои курсы':
		moikurs(message)



#запуск бота безостановки
bot.polling(none_stop=True)