##############     状态B         #################
		elif currentState == 'B':
			if(ch == '_' or ch in __letterSet__ or ch in __digitSet__):
				buf = buf+ch
				currentState = 'B'
				return
			else:#可接受状态
				
				buf = ""
				currentState = 'A'
				continue

		##############     状态C         #################

		elif currentState == 'C':
			if(ch in __digitSet__):
				buf = buf + ch
				currentState = 'C'
				return
			elif(ch=='.'):
				buf = buf+ch
				currentState = 'P'
				return
			else:#可接受状态
				console_msg = console_msg + '('+ buf + u' , 整数常量)\n'
				result.append('INUM')
				buf = ""
				currentState = 'A'
				continue

		##############     状态D         #################
		elif currentState == 'D':
			if(ch!='\'' and ch!='\\'):
				buf = buf+ch
				currentState = 'E'
				return
			elif (ch!='\'' and ch=='\\'):
				buf = buf+ch
				currentState = 'F'
				return
			else:
				compilerFail(u'空白或无效的字符')
				return

		##############     状态E        #################
		elif currentState == 'E':
			if(ch=='\''):
				buf = buf+ch
				currentState = 'H'
				continue
			else:
				compilerFail(u'字符常量长度大于一')
				return

		##############     状态H        #################
		elif currentState == 'H':
			console_msg = console_msg + '(' + buf+ u' ,字符常量)\n'
			result.append['CH']
			buf = ""
			currentState = 'A'
			return

		##############     状态F         #################
		elif currentState == 'F':
			if(ch in __switchCharSet__):
				buf = buf + ch
				currentState = 'E'
				return
			else:
				compilerFail(u'无效的转义字符')		
				return	

		##############     状态G         #################
		elif currentState == 'G':
			if(ch!='\"' and ch!='\\'):
				buf = buf+ch
				currentState = 'G'
				return
			elif (ch!='\'' and ch=='\\'):
				buf = buf+ch
				currentState = 'I'
				return
			elif(ch=='\"'):
				buf = buf+ch
				currentState = 'J'

		##############     状态I         #################
		elif currentState == 'I':
			if(ch in __switchCharSet__):
				buf = buf+ch
				currentState = 'G'
				return
			else:
				compilerFail(u'无效的转义字符')	
				return

		##############     状态J         #################
		elif currentState == 'J':
			console_msg = console_msg + '(' + buf+ u' ,字符串常量)\n'
			result.append('STR')
			buf = ""
			currentState = 'A'
			return

		##############     状态K         #################
		elif currentState == 'K':
			if(ch=='*'):
				buf = buf[0:len(buf)-1]  #是注释，退去上一个/
				currentState = 'L'
				return
			elif(ch=='/'):#单行注释
				buf = buf[0:len(buf)-1]  #是注释，退去上一个/
				currentState = 'O'
				return
			elif(ch=='='):
				buf = buf+ch
				currentState = 'B='
				return
			else:
				console_msg = console_msg+'('+buf+u' ,运算符)\n'
				result.append(buf)
				buf = ""
				currentState = 'A'
				continue

		##############     状态L         #################
		elif currentState == 'L':
			if(ch != '*'):
				currentState = 'L'
				return
			elif(ch=='*'):
				currentState = 'M'
				return
		##############     状态M         #################
		elif currentState=='M':
			if(ch=='/'):
				currentState = 'N'
				return
			else:
				currentState='L'

		##############     状态N         #################
		elif currentState=='N':
			currentState = 'A'
			return

		##############     状态O         #################
		elif currentState=='O':
			if(ch=='\n'):
				currentState = 'A'
				return
			else:
				currentState='O'
				return

		##############     状态P         #################
		elif currentState=='P':
			if(ch in __digitSet__):
				buf = buf+ch
				currentState = 'Q'
				return
			else:
				compilerFail(u'无效的浮点数')
				return

		##############     状态Q         #################
		elif currentState=='Q':
			if(ch in __digitSet__):
				buf = buf+ch
				currentState='Q'
				return
			else:
				console_msg = console_msg+'('+buf+u' , 浮点数常量)\n'
				result.append('FNUM')
				buf=""
				currentState='A'
				continue

		##############     状态A+         #################
		elif currentState=='A+':
			if(ch=='+' or ch=='='):
				buf = buf+ch
				currentState='B+'
				return
			else:
				console_msg = console_msg+'('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B+         #################
		elif currentState=='B+':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A-         #################
		elif currentState=='A-':
			if(ch=='-' or ch=='='):
				buf = buf+ch
				currentState='B-'
				return
			else:
				console_msg = console_msg+'('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B-         #################
		elif currentState=='B-':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A*         #################
		elif currentState=='A*':
			if(ch=='*' or ch=='='):
				buf = buf+ch
				currentState='B*'
				return
			else:
				console_msg = console_msg+'('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B*         #################
		elif currentState=='B(':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A&         #################
		elif currentState=='A&':
			if(ch=='&' or ch=='='):
				buf = buf+ch
				currentState='B&'
				return
			else:
				console_msg = console_msg+'('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B&         #################
		elif currentState=='B&':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A^         #################
		elif currentState=='A^':
			if(ch=='^' or ch=='='):
				buf = buf+ch
				currentState='B^'
				return
			else:
				console_msg = console_msg+ '('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B^         #################
		elif currentState=='B^':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A|         #################
		elif currentState=='A|':
			if(ch=='|' or ch=='='):
				buf = buf+ch
				currentState='B|'
				return
			else:
				console_msg = console_msg+ '('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B|         #################
		elif currentState=='B|':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A=         #################
		elif currentState=='A=':
			if(ch=='='):
				buf = buf+ch
				currentState='B='
				return
			else:
				console_msg = console_msg+ '('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B=         #################
		elif currentState=='B=':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A!         #################
		elif currentState=='A!':
			if(ch=='='):
				buf = buf+ch
				currentState='B!'
				return
			else:
				console_msg = console_msg+ '('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B!         #################
		elif currentState=='B!':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A>         #################
		elif currentState=='A>':
			if(ch=='='):
				buf = buf+ch
				currentState='B>'
				return
			else:
				console_msg = console_msg+ '('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B>         #################
		elif currentState=='B!':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue

		##############     状态A<         #################
		elif currentState=='A<':
			if(ch=='='):
				buf = buf+ch
				currentState='B<'
				return
			else:
				console_msg = console_msg+ '('+buf+u' ,操作符)\n'
				result.append(buf)
				buf=""
				currentState = 'A'
				continue

		##############     状态B<         #################
		elif currentState=='B!':
			console_msg = console_msg+'('+buf+u' ,操作符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			continue
		
		##############     状态$         #################
		elif currentState=='$':
			console_msg = console_msg+'('+buf+u' ,终结符)\n'
			result.append(buf)
			buf = ""
			currentState = 'A'
			return
		