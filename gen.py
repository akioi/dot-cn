import os, yaml

def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def read_file(path):
	mkdir(os.path.split(path)[0])
	file = open(path, 'r+', encoding='utf8')
	text = file.read()
	file.close()
	return text

def write_file(text, path):
	mkdir(os.path.split(path)[0])
	file = open(path, 'w+', encoding='utf8')
	file.write(text)
	file.close()

def load(text, data):
	for key, value in data.items():
		text = text.replace('{{ %s }}' % key, value)
	return text

def depoly(name):
	os.system("cd {path} && git add . && git commit -m 'update' && git push".format(
		path = os.getcwd() + '/html/%s' % name
	))

if __name__ == '__main__':
	for filename in os.listdir('src'):
		text = read_file('src/%s' % filename)
		data = yaml.load(text)
		data['short_name'] = filename.split('.')[0]
		for filename in os.listdir('themes/%s' % data['theme']):
			text = read_file('themes/%s/%s' % (data['theme'], filename))
			write_file(load(text, data), 'html/%s/%s' % (data['short_name'], filename))
		depoly(data['short_name'])