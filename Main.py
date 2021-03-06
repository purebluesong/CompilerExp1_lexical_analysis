#coding:utf-8
buf = ""
ch = ''
mLine = 1
mRow = 0
currentState = 'A'
__letterSet__  = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m',
				'n','o','p','q','r','s','t','u','v','w','x','y','z',
				'A','B','C','D','E','F','G','H','I','J','K','L','M',
				'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',]
__digitSet__ = ['0','1','2','3','4','5','6','7','8','9']
__blankCharSet__ = [' ', '\n', '\t']
__switchCharSet__ = ['b', 'n', 't', '\'', '\"','\\']
# 由ANSI标准定义的C语言关键字共32个：
__keywordSet__ = ['auto','double','int','struct','break','else','long','switch','case','enum',
				'register','typedef','char','extern','return','union','const','float','short','unsigned',
				'continue','for','signed','void','default','goto','sizeof','volatile','do','if',
				'while','static'
				]
__boardSet__ = [';',',', '(', ')', '.', '{', '}','[',']']
console_msg=""
result=[]
__TOKENIZE_SUCCESS__ = 0
__TOKEN_ERROR__ = 1





def compilerFail(status):
	global mLine
	global mRow
	global buf
	global console_msg
	global currentState

	console_msg = console_msg + u"编译于第 "+str(mRow)+u" 行, 第 "+str(mLine)+u" 列失败,因为:"+status+'\n'
	currentState='A'
	buf = ""



def buffadd():
	global buf,ch
	buf += ch

def buffclr():
	global buf
	buf = ''

def make_consol_msg(flag):
	global console_msg,ch
	console_msg += '(\t' + ch + '\t\t, '+flag+'\t\t)\n' 

def make_consol_msg_buf(flag):
	global console_msg,buf
	console_msg += '(\t' + buf + '\t\t, '+flag+'\t)\n' 

def resultadd():
	global result,ch
	result.append(ch)

def resultaddString(res):
	global result
	result.append(res)

def endA_board():
	make_consol_msg(u'界符')

def defaultA():
	compilerFail(u'不可识别的字符')

def defaultB():
	global buf,result
	if (buf in __keywordSet__):
		make_consol_msg_buf(u'关键字')
		result.append(buf)
	else:
		make_consol_msg_buf(u'标识符')
		result.append('IDN')

def defaultC():
	global result
	make_consol_msg_buf(u'整数常量')
	result.append('INUM')

def defaultD():
	compilerFail(u'空白或无效的字符')

def defaultE():
	compilerFail(u'字符常量长度大于一')

def defaultF():
	compilerFail(u'无效的转义字符')

def endH_A():
	global result
	make_consol_msg_buf(u'字符常量')
	resultaddString('CH')

def defaultI():
	compilerFail(u'无效的转义字符')

def endJ_A():
	make_consol_msg_buf(u'字符串常量')
	resultaddString('STR')

def annotation():
	global buf
	buf = buf[:-1]

def defaultK():
	global buf
	make_consol_msg_buf(u'运算符')
	resultaddString(buf)

def defaultP():
	compilerFail(u'无效的浮点数')

def defaultQ():
	make_consol_msg_buf(u'浮点数常量')
	resultaddString('FNUM')

def defaultAA():
	global buf
	make_consol_msg_buf(u'操作符')
	resultaddString(buf)

def defaultBB():
	global buf
	make_consol_msg_buf(u'操作符')
	resultaddString(buf)

def defaultEnd():
	global buf
	make_consol_msg_buf(u'终结符')
	resultaddString(buf)

state_converter = {
	'A':[###################   状态A   #############
		(True, __blankCharSet__			, [],				'A'),
		(True, __letterSet__ + [' ']	, [buffadd],		'B'),
		(True, __digitSet__ 			, [buffadd],		'C'),
		(True, ['\''] 					, [buffadd],		'D'),
		(True, ['\"']					, [buffadd],		'G'),
		(True, ['/']		 			, [buffadd],		'K'),
		(True, ['+']		 			, [buffadd],		'A+'),
		(True, ['-']		 			, [buffadd],		'A-'),
		(True, ['*']		 			, [buffadd],		'A*'),
		(True, ['&']		 			, [buffadd],		'A&'),
		(True, ['^']		 			, [buffadd],		'A^'),
		(True, ['|']		 			, [buffadd],		'A|'),
		(True, ['=']		 			, [buffadd],		'A='),
		(True, ['!']		 			, [buffadd],		'A!'),
		(True, ['>']		 			, [buffadd],		'A>'),
		(True, ['<']		 			, [buffadd],		'A<'),
		(True, __boardSet__ 			, [buffclr,endA_board,resultadd],'A'),
		(True, ['$']					, [buffadd],		'$'),
		('default',[]					, [defaultA],		'A'),
		],
	'B':[###################   状态B   #############
		(True,['_']+__letterSet__+__digitSet__	,[buffadd],'B'),
		('default',[]				,[defaultB,buffclr],'_A'),
		],
	'C':[###################   状态C   #############
		(True,__digitSet__ 			,[buffadd],		'C'),
		(True,['.'] 				,[buffadd],		'P'),
		('default',[] 				,[defaultC,buffclr],'_A'),
		],
	'D':[
		(False,['\'','\\']			,[buffadd],		'E'),
		(True,['\\'] 				,[buffadd],		'F'),
		('default',[] 				,[defaultD],	'A'),
		],
	'E':[
		(True,['\''] 				,[buffadd],		'H'),
		('default',[]				,[defaultE],	'A'),
		],
	'F':[
		(True,__switchCharSet__		,[buffadd],		'E'),
		('default',[] 				,[defaultF],	'A'),
		],
	'G':[
		(False,['\\','\"'] 			,[buffadd],		'G'),
		(True,['\\'] 				,[buffadd],		'I'),
		(True,['\"'] 				,[buffadd],		'J'),
		],
	'H':[
		(False,[] 					,[endH_A,buffclr],'A'),
		],
	'I':[
		(True,__switchCharSet__		,[buffadd],		'G'),
		('default',[]				,[defaultI],	'A'),
		],
	'J':[
		(False,[] 					,[endJ_A,buffclr],'A'),
		],
	'K':[
		(True,['*'] 				,[annotation],	'L'),
		(True,['/'] 				,[annotation],	'O'),
		(True,['='] 				,[buffadd],		'B='),
		('default',[] 				,[defaultK,buffclr],'_A'),
		],
	'L':[
		(False,['*'] 				,[],			'L'),
		(True,['*'] 				,[],			'M'),
		],
	'M':[
		(True,['/'] 				,[],			'N'),
		('default',[] 				,[],			'L'),
		],
	'N':[
		('default',[] 				,[],			'A'),
		],
	'O':[
		(True,['\n'] 				,[],			'A'),
		('default',[] 				,[],			'O'),
		],
	'P':[
		(True,__digitSet__			,[buffadd],		'Q'),
		('default',[]				,[defaultP],	'A'),
		],
	'Q':[
		(True,__digitSet__			,[buffadd],		'Q'),
		('default',[]				,[defaultQ,buffclr],'_A'),
		],
}
state_converter.update({
	'A+':[
		(True,['+','=']				,[buffadd],		'B+'),
		('default',[]				,[defaultAA, buffclr],'_A'),
		],
	'B+':[
		('default',[]				,[defaultBB,buffclr],'_A')
		],
	'A-':[
		(True,['-','=']				,[buffadd],		'B-'),
		],
	'A*':[
		(True,['*','=']				,[buffadd],		'B*'),
		('default',[]				,[defaultAA,buffclr],'_A'),
		],
	'B*':[
		('default',[]				,[defaultBB,buffclr],'_A'),
		],
	'A&':[
		(True,['&','=']				,[buffadd],		'B&'),
		('default',[]				,[defaultAA,buffclr],'_A'),
		],
	'B&':[
		('default',[]				,[defaultBB,buffclr],'_A'),
		],
	'A^':[
		(True,['^','=']				,[buffadd],		'B^'),
		('default',[]				,[defaultAA,buffclr],'_A'),
		],
	'B^':[
		('default',[]				,[defaultBB,buffclr],'_A'),
		],
	'A|':[
		(True,['|','=']				,[buffadd],		'B|'),
		('default',[]				,[defaultAA,buffclr],'_A'),
		],
	'B|':[
		('default',[]				,[defaultBB,buffclr],'_A'),
		],
	'A=':[
		(True,['=']					,[buffadd],		'B='),
		('default',[]				,[defaultAA,buffclr],'_A'),
		],
	'B=':[
		('default',[]				,[defaultBB,buffclr],'_A'),
		],
	'A!':[
		(True,['=']					,[buffadd],		'B!'),
		('default',[]				,[defaultAA,buffclr],'_A'),
		],
	'B!':[
		('default',[]				,[defaultBB,buffclr],'_A'),
		],
	'A>':[
		(True,['=']					,[buffadd],		'B>'),
		('default',[]				,[defaultAA,buffclr],'_A'),
		],
	'B>':[
		('default',[]				,[defaultBB,buffclr],'_A'),
		],
	'A<':[
		(True,['|','=']				,[buffadd],		'B<'),
		('default',[]				,[defaultAA,buffclr],'_A'),
		],
	'B<':[
		('default',[]				,[defaultBB,buffclr],'_A'),
		],
	'$'	:[
		('default',[]				,[defaultEnd,buffclr],'_A'),
		],
})

def getNextState(currentState):
	global state_converter
	states_handle = state_converter[currentState] 
	# print currentState
	for state_struct in states_handle:
		if state_struct[0] == 'default':
			for method in state_struct[2]:
				method()
			return state_struct[3]
		elif state_struct[0]:
			if ch in state_struct[1]:
				for method in state_struct[2]:
					method()
				return state_struct[3]
		else:
			if ch not in state_struct[1]:
				for method in state_struct[2]:
					method()
				return state_struct[3]

def tokenizer():
	global mLine
	global mRow
	global currentState
	global __letterSet__
	global __digitSet__
	global __blankCharSet__
	global __keywordSet__
	global console_msg
	global result
	global __TOKEN_ERROR__
	global __TOKENIZE_SUCCESS__

	while True:#there could rewrite by state machine
		currentState = getNextState(currentState)
		if currentState == '$':
			return
		elif currentState[0] == '_':
			currentState = currentState[1:]
			continue
		else:
			return		

def scanner(text):
	global mLine
	global mRow
	global buf
	global console_msg
	global currentState,ch

	buf = ""
	console_msg = ""
	for i in xrange(0,len(text)):
		# console_msg=console_msg+'进入scanner\n'
		mLine = mLine+1
		ch = text[i]
		tokenizer()
		if(text[i]=='\n'):
			mRow += 1
			mLine = 0
	ch = '$'
	tokenizer()
		
			
def main():
	global result,console_msg
	fp = open('code.c','r')
	scanner(fp.read())
# 	console_msg= console_msg+'($,结束符)\n'
# 	result.append('$')
	print(console_msg)
	print(result)
	return result
	

if __name__ == '__main__':
	main()
	