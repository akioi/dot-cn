#Github Access Build On Github API v3 
#Deploy Code by abc1763613206
import requests
import os, yaml
import json

env_dist = os.environ
Gkey =  env_dist.get('GithubKEY')
Owner = env_dist.get('Owner')  # 当前组织名，请在TravisCI中定义
PusherAccount = env_dist.get('PusherAccount')  # 推送者参数
PusherPassword = env_dist.get('PusherPassword')
PusherEmail = env_dist.get('PusherEmail')
Webroot = env_dist.get('Webroot')  # 根域名(akioi.cn)


sess=requests.session()

headers = {
    'Accept': 'application/vnd.github.machine-man-preview+json',
    'User-Agent': 'DOT-CN Publisher/1.0',
    'Authorization': 'token %s' % (Gkey) 
}

headers_ForPagesOnly = {  
    'Accept': 'application/vnd.github.mister-fantastic-preview+json',
    'User-Agent': 'DOT-CN Publisher/1.0',
    'Authorization': 'token %s' % (Gkey) 
}


global data


def mkdir(path):
	if not os.path.exists(path):
		print('%s Not Exist ,Creating......\n' % (path)) 
		os.makedirs(path)

def read_file(path):
	# mkdir(os.path.split(path)[0])
	file = open(path, 'r+', encoding='utf8')
	text = file.read()
	file.close()
	return text

def write_file(text, path):
	#mkdir(os.path.split(path)[0])
	file = open(path, 'w+', encoding='utf8')
	file.write(text)
	file.close()

def load(text, data):
	for key, value in data.items():
		text = text.replace('{{ %s }}' % key, value)
	return text

def FromRequestsgetCloneURL(re):
	Getdata = re.json()
	CloneURL = Getdata['clone_url']
	print('Clone URL %s\n'%(CloneURL))
	return CloneURL


def RequestBuild(name):
	print('Request Buildings for %s' % (name))
	PostURL='https://api.github.com/repos/%s/%s/pages/builds' % (Owner,name)

	res=requests.post(url=PostURL,headers=headers_ForPagesOnly)
	print(res.text+'\n')



def getPagesURL(name):
	if "cname" in data:
		PagesURL=data['cname']
	else:
		PagesURL='%s.%s'%(name,Webroot)
	return PagesURL

def CreateRepo(name):
	print('Creating Repo %s'%(name))
	Postdata={'name' : str(data['name']),'description' : str(data['description']), 'homepage' : str('https://%s'%(getPagesURL(name)))}
	PostURL='https://api.github.com/orgs/%s/repos' % (Owner)

	res=requests.post(url=PostURL,data=json.dumps(Postdata),headers=headers)
	#print(res.text+'\n')
	return FromRequestsgetCloneURL(res)

def CheckIfRepoCreated(name):
	print('Checking Repo %s\n'%(name))
	# GET repo 信息 ， 检测状态码 404 为未创建
	r = requests.get(url = 'https://api.github.com/repos/%s/%s' % (Owner,name), headers = headers)
	#print (r.status_code)
	if(r.status_code==404): # Not Created
		CloneURL = CreateRepo(name)
	elif(r.status_code==200):# Created
		CloneURL = FromRequestsgetCloneURL(r)
	else:
		print('Unknown Error!\n')
		print(r.text+'\n')
	return CloneURL
		


def CloneRepo(name):
	CloneURL = CheckIfRepoCreated(name)
	print('Cloning %s \n'%(CloneURL))
	mkdir(os.getcwd() + '/html/')
	os.system("cd {path} && git clone {CURL} && sed -i 's/github.com/{username}:{password}@github.com/g' ./{Reponame}/.git/config" .format(   #Only Support Linux :(
		path = os.getcwd() + '/html/' ,
		CURL = CloneURL,
		Reponame = name,
		username = PusherAccount,
		password = PusherPassword
	))




def deploy(name):   # build pages at the moment?
	print('Deploying %s\n'%(name))
	os.system("git config --global push.default matching && cd {path} && echo {pagesURL} > ./CNAME && git config user.email '{Email}' &&  git config user.name '{Account}' && git add . && git commit -m 'update' && git checkout -b gh-pages && git push origin gh-pages --force > secret.txt ".format(
		path = os.getcwd() + '/html/%s' % name,
		Account = PusherAccount,
		Email = PusherEmail,
		pagesURL = getPagesURL(name)
	))
	RequestBuild(name)


def Cleanup():
	print('Cleaning up......\n')
	os.system("rm -rf html")

if __name__ == '__main__':
	Cleanup()
	#LoginGithub()
	for filename in os.listdir('src'):
		print('Processing %s'%(filename))
		text = read_file('src/%s' % filename)
		data = yaml.load(text)
		data['short_name'] = filename.split('.')[0]
		for filename in os.listdir('themes/%s' % data['theme']):
			CloneRepo(data['short_name'])
			text = read_file('themes/%s/%s' % (data['theme'], filename))
			write_file(load(text, data), 'html/%s/%s' % (data['short_name'], filename))
		deploy(data['short_name'])
	Cleanup()
		
#CheckIfRepoCreated(input())
