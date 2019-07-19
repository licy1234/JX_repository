# __author:"zonglr"
# date:2018/7/10
#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from jpype import *
import os.path,sys,requests,demjson

class TestLogin():
	#root_dir = os.path.dirname(os.path.dirname(__file__))    #os.path.dirname(__file__)返回脚本的路径
	root_dir=os.path.join(os.path.abspath('.'),'C:/Users/luwb/Desktop/Python/test_data')   #os.path.join(path1[, path2[, ...]]) 将目录和文件名合成一个路径       # os.path.abspath(path)  返回绝对路径
	print(os.path.abspath('.'))  
	
	print(root_dir)
	filepath = root_dir+'/tpcommon.jar'
	#filepath = root_dir+'/'+'test_data/tpcommon.jar'
	#print(filepath)
	jvmpath = getDefaultJVMPath()       # 默认的JVM路径
	# 启动jvm服务
	startJVM(jvmpath, "-ea","-Djava.class.path=%s" % (filepath))
	JDClass = JClass('com.zc.travel.common.utils.rsa.DESede')
	JDClass2 = JClass('com.zc.travel.common.utils.rsa.Base64')

    
	'''通过请求getsecretkey接口获取secretkey和uuid'''
	payload = {
				'method': 'getSecretKey.do'}
	r = requests.post('http://u.test.8atour.com/api/getSecretKey', data=payload)
	json = r.json()
	#print('json列表:',json)
	secretkey = json['data']['data']['secretKey']
	#print('secretkey值:',secretkey)
	#print('secretkey类型:',type(secretkey))
	uuid = json['data']['data']['uuid']
	#print('uuid值：%s'%uuid)

	phonenumber = "15622340169"
	logintype = "1"

	'''加密key由phonenumber+secretkey+logintype拼接，拼接后的长度不足24补0，最后转成字节数组'''
	init_key = ''.join([phonenumber,secretkey,logintype])
	#print("init_key类型:",type(init_key))
	#print('init_key值:',init_key)

	while len(init_key) < 24:
		print('init_key小于24位时:',init_key)
		init_key = init_key + '0'
		
	'''将init_key转成字节数组作为加密key'''
	key = bytearray(init_key,encoding = 'utf-8')
	print('key值：',key)

	'''将密码转成字节数组作为加密date'''
	psw = 'aa1234'
	date = bytearray(psw,encoding = 'utf-8')

	# 调用jar中的方法,先3DES加密再base64加密
	init_result = JDClass.encrypt(date,key)
	result = JDClass2.encode(init_result)
	print("加密后的密码：",result)

	'''开始登录'''
	put = {
				'userName': phonenumber,
				'password': result,
				'loginType': logintype,
				'isVerify': '2',
				'isDefaultLogin': '2',
				'method': 'login.do',
				'uuid': uuid
	}
	#print("put类型",type(put))

	r = requests.post('http://u.test.8atour.com/api/login', data=put)
	json=r.json()
	assert json['data']['msg'] == '请求成功'

	shutdownJVM()



'''

	root_dir=os.path.join(os.path.abspath('.'),'C:/Users/luwb/Desktop/Python/test_data')   #os.path.join(path1[, path2[, ...]]) 将目录和文件名合成一个路径       # os.path.abspath(path)  返回绝对路径
	#print(os.path.abspath('.'))  
	filepath = root_dir+'/tpcommon.jar'

'''