# ddcrypt v1.1 - by Gameye98/DedSecTL
# droidscript deobfuscator - note that when droidscript update, their app function code will always change
# so dont blame me if you found the function code its not match with real function code, i dont think you understand what ive said
# i dont even know what im saying, just do the experiment by yourself and you will understand what im trynna say
# ---
# license: MIT
# team: BlackHole Security
# purpose: droidscript apk deobfuscator
# ---
import os, re, sys, time
import string, struct
import subprocess, shutil

class StopDDCrypt(Exception):
	pass

def system(cmd):
	return subprocess.run(cmd,shell=True,check=True,stdout=subprocess.PIPE).stdout.decode()

if len(sys.argv) != 2:
	print(f"Usage: {sys.argv[0]} [filename.js|filename.apk]")
else:
	try:
		filepath = sys.argv[1]
		filename = filepath.split("/")[len(filepath.split("/"))-1]
		destdir = sys.argv[0][0:len(sys.argv[0])-len(sys.argv[0].split("/")[-1])]
		if os.path.exists(sys.argv[1]):
			if os.path.isfile(filepath):
				print("[ddcrypt] starting...")
				try:
					open(filepath,"r").read()
				except UnicodeDecodeError:
					stream = open(filepath,"rb").read()
					if len(stream) > 4:
						if stream[0:4] == b"PK\x03\x04":
							print("[ddcrypt] file: zip archive data [sig:PK\\x03\\x04]")
							filenoformat = filename
							if filename.endswith(".zip") or filename.endswith(".apk"):
								filenoformat = filename[0:len(filename)-4]
								destdir = destdir + filenoformat + "/"
								print("[ddcrypt] extracting raw resources...")
								shutil.unpack_archive(filepath, destdir, "zip")
								strings = ""
								try:
									androidmanifest = open(destdir + "AndroidManifest.xml","r").read()
									strings = androidmanifest
								except UnicodeDecodeError:
									androidmanifest = open(destdir + "AndroidManifest.xml","rb").read()
									for b in stream:
										if (b >= 0x41 and b < 0x5b) or (b >= 0x61 and b < 0x7b):
											signed = struct.pack("b", b).decode()
											if signed in string.ascii_letters:
												strings += signed
									userdir = destdir + "assets/user"
									if os.path.isdir(userdir):
										isfilejs = False
										for f in os.listdir(userdir):
											if f.lower().endswith(".js"):
												isfilejs = True
												break
										if not isfilejs:
											print("[ddcrypt] the app is not build with droidscript")
											print("[ddcrypt] or not supported to be decompiled")
											print("[ddcrypt] deleting raw resources...")
											system(f"rm -rf {destdir}")
											print("[ddcrypt] quitting!",end="")
											raise StopDDCrypt
										tempdir = destdir[0:len(destdir)-1] + ".bak"
										system(f"mv '{userdir}' '{tempdir}'")
										system(f"rm -rf '{destdir[0:len(destdir)-1]}'")
										system(f"mv '{tempdir}' '{destdir[0:len(destdir)-1]}'")
										for f in os.listdir(destdir[0:len(destdir)-1]):
											if f.endswith(".js"):
												fileiter = f[0:len(f)-3]
												if fileiter in strings or fileiter.lower() in strings:
													filepath = destdir + f
													filename = f
													break
									else:
										print("[ddcrypt] the app is not build with droidscript")
										print("[ddcrypt] or not supported to be decompiled")
										print("[ddcrypt] deleting raw resources...")
										system(f"rm -rf {destdir}")
										print("[ddcrypt] quitting!",end="")
										raise StopDDCrypt
				code_fix = [["),",")\n"],["(!1)","(false)"],["(1)","(true)"],[")\n",");\n\t"],["(){","() {\n\t"],[",.",",0."],["!1)","false)"],[")}function",");\n}\nfunction"],[" =  = "," == "],["case\"","case \""],["1?","true"],[")):",");} else {"],["try{","try {\n\t"],[";while",";\n\twhile"],["++}","++;\n}"],[";break;case",";break;\n\tcase"],[":app",": app"],["}function","}\nfunction"],["}catch(e){","} catch(e) {\n\t"],[")}}",");\n\t}\n}"],["\"?","\") {\n\t"],[")}",")\n}"]]
				funclst = ["_103:ShowPopup","_2():Exit()","_130:SetOrientation","_86:EnableBackKey","_126:SetOrientation","_84:EnableBackKey","_88:Alert","_264:CreateListDialog","_239:CreateButton","_244:CreateText","_245:CreateTextEdit","_248:CreateScroller","_257:CreateScroller","_158:AddLayout","_182:ReadFile","_237:CreateLayout","_254:CreateYesNoDialog"]
				print(f"[ddcrypt] read: {filepath}")
				filenew = filename.replace(".js","")+"_new.js"
				fileold = filename.replace(".js","")+"_old.js"
				bak = inx = open(filepath, "r").read()
				reg_1 = re.findall(r'\\u\d\d\d\d', inx)
				reg_2 = re.findall(r'\\u\d\d\d\w', inx)
				reg_3 = re.findall(r'\w+=\w+', inx)
				# reg_4 = re.findall(r'\w+,\w+', inx)
				reg_5 = re.findall(r'"=\w+', inx)
				reg_6 = re.findall(r'\w+="', inx)
				print(f"[{filename}] deobfuscating code (regex+unicode)")
				for item in reg_1:
					exec(f"res = u'{item}'")
					inx = inx.replace(item, res)
				for item in reg_2:
					exec(f"res = u'{item}'")
					inx = inx.replace(item, res)
				for item in reg_3:
					inx = inx.replace(item, item.replace("="," = "))
				"""
				for item in reg_4:
					inx = inx.replace(item, item.replace(",",";\n"))
				"""
				for item in reg_5:
					inx = inx.replace(item, item.replace("="," = "))
				for item in reg_6:
					inx = inx.replace(item, item.replace("="," = "))
				dd_0 = inx
				print(f"[{filename}] fix code depends on code_fix[]")
				for piece_of in code_fix:
					dd_0 = dd_0.replace(piece_of[0], piece_of[1])
				"""
				dd_1 = dd_0.replace("),",")\n")
				dd_2 = dd_1.replace("(!1)","(false)").replace("(1)","(true)")
				dd_3 = dd_2.replace(")\n",");\n\t")
				dd_4 = dd_3.replace("="," = ")
				dd_5 = dd_4.replace("(){","() {\n\t")
				dd_6 = dd_5.replace(",.",",0.").replace("!1)","false)")
				dd_7 = dd_6.replace(")}function",");\n}\nfunction")
				dd_8 = dd_7.replace(" =  = "," == ")
				dd_9 = dd_8.replace("case\"","case \"")
				dd_10 = dd_9.replace("1?","true")
				dd_11 = dd_10.replace(")):",");} else {")
				dd_12 = dd_11.replace("try{","try {\n\t")
				"""
				print(f"[{filename}] replace old function with new function")
				for function in funclst:
					dd_0 = dd_0.replace(function.split(":")[0],function.split(":")[1])
					time.sleep(0.1)
				try:
					create_layout = re.findall(r'(app._[0-9]+)',re.findall(r'app._[0-9]+\("linear"', dd_0)[0])
					dd_0 = dd_0.replace("app._"+create_layout[0],"app.CreateLayout")
					add_layout_1 = re.findall(r'([a-zA-Z0-9]+) = app.CreateLayout', dd_0)
					add_layout_2 = re.findall("(app._[0-9]+)\("+add_layout_1[0]+"\)", dd_0)
					dd_0 = dd_0.replace(add_layout_2[0],"app.AddLayout")
					write_file_1 = re.findall(r'app\..*","Append"\);', dd_0)
					write_file_2 = re.findall(r'app._([0-9]+)', write_file_1[0])
					dd_0 = dd_0.replace("app."+write_file_2,"app.WriteFile")
				except IndexError:
					pass
				open(filepath,"w").write(dd_0)
				print(f"[write] original: {filepath}")
				open(filepath[0:len(filepath)-len(filename)] + filenew,"w").write(dd_0)
				print(f"[write] backup(new): {filepath[0:len(filepath)-len(filename)]+filenew}")
				open(filepath[0:len(filepath)-len(filename)] + fileold,"w").write(bak)
				print(f"[write] backup(old): {filepath[0:len(filepath)-len(filename)]+fileold}")
				print("[ddcrypt] done .. !!")
	except (KeyboardInterrupt, EOFError):
		exit()
	except Exception as e:
		print(e)