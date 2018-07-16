
# coding: utf-8


import os
import numpy as np
import Tkinter as tk
import tkMessageBox
from tkFileDialog import askdirectory as diag

import matplotlib
if matplotlib.get_backend() == u'agg':
	try:
		matplotlib.use('qt5agg')
		import matplotlib.pyplot as plt
	except ImportError:
		matplotlib.use('qt4agg')
		import matplotlib.pyplot as plt
else:
	import matplotlib.pyplot as plt

class menu:
	def __init__(self):
		root=tk.Tk()
		root.title('S-BT-Vis')
		frame01=tk.Frame(root)
		frame03=tk.Frame(root)
		frame03a=tk.Frame(frame03)
		frame03b=tk.Frame(frame03)
		frame04=tk.Frame(root)
		frame04a=tk.Frame(frame04)
		frame04b=tk.Frame(frame04)
		frame05=tk.Frame(root)
		frame01.pack(side=tk.TOP)
		frame03.pack(side=tk.TOP)
		frame04.pack(side=tk.TOP)
		frame04a.pack(side=tk.TOP)
		frame04b.pack(side=tk.TOP)
		frame05.pack(side=tk.TOP)

		self.ele    = tk.StringVar()
		self.xcolumn  = tk.IntVar()
		self.slb01  = tk.StringVar()
		self.intval_sc01  = tk.IntVar()
		self.doubleval_sc01  = tk.DoubleVar()
		self.doubleval_sc02  = tk.DoubleVar()
		self.nk     = tk.IntVar()
		self.ycolumn = tk.IntVar()
		
		self.ele.set('Si')
		self.intval_sc01.set(0)
		self.nk.set(30)
		self.ycolumn.set(4)
		
		self.xcolumn.set(0)
		self.slb01.set('Temperature')

		tk.Label(frame01,text='BoltzTraP Foltders').pack(side=tk.TOP)
		frame01a=tk.Frame(frame01)
		self.dir01 = tk.StringVar()
		self.dir02 = tk.StringVar()
		self.nt01,self.nt02 = 0,0
		self.req2plot = {'trace01':False,
										 'trace02':False,
										 'intrans01':False,
										 'intrans02':False,
								}
		
		tk.Entry(frame01a,textvariable=self.dir01,state='readonly').grid(column=2,row=1)
		tk.Entry(frame01a,textvariable=self.dir02,state='readonly').grid(column=2,row=2)
		
		tk.Button(frame01a, text='Browse',command=self.__diag_def01).grid(column=1,row=1)
		tk.Button(frame01a, text='Browse',command=self.__diag_def02).grid(column=1,row=2)
		
		frame01a.pack(side=tk.TOP)
		
		tk.Label(frame03,text='x-axis').pack(side=tk.TOP)
		frame03a.pack(side=tk.TOP)
		frame03b.pack(side=tk.TOP)
		
		tk.Radiobutton(frame03a,text='Fermi Energy'   ,command=self.sel_xcolumn,variable=self.xcolumn,value=0).pack(side=tk.LEFT)
		tk.Radiobutton(frame03a,text='Temperature',command=self.sel_xcolumn,variable=self.xcolumn,value=1).pack(side=tk.LEFT)
		self.lb01=tk.Label(frame03b,textvariable=self.slb01)
		self.sc01=tk.Scale(frame03b,
											 orient=tk.HORIZONTAL,
											 to=0,
											 variable=self.intval_sc01,
											 command=self.sel_scale,
											 showvalue=False,
											 length=200)
		self.lb01.pack(side=tk.TOP)
		self.sc01.pack(side=tk.TOP)
		tk.Label(frame03b,textvariable=self.doubleval_sc01).pack(side=tk.TOP)
	  
		tk.Label(frame04a,text='y-axis').pack(side=tk.TOP)
		tk.Radiobutton(frame04a,text='N'      ,variable=self.ycolumn,value=2).pack(side=tk.LEFT)
		tk.Radiobutton(frame04a,text='DOS'    ,variable=self.ycolumn,value=3).pack(side=tk.LEFT)
		tk.Radiobutton(frame04a,text='Seebeck',variable=self.ycolumn,value=4).pack(side=tk.LEFT)
		tk.Radiobutton(frame04a,text='s/t'    ,variable=self.ycolumn,value=5).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='R_H'    ,variable=self.ycolumn,value=6).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='kappa0' ,variable=self.ycolumn,value=7).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='c'      ,variable=self.ycolumn,value=8).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='chi'    ,variable=self.ycolumn,value=9).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='ZT'    ,variable=self.ycolumn,value=10).pack(side=tk.LEFT)
	  
		self.btplot=tk.Button(frame05,text='Plot',command=self.plot,width=27,height=3,state=tk.DISABLED)
		self.btplot.pack(side=tk.TOP)
	  
		root.mainloop()
		
	def __diag_def01(self,path=None):
		self.dir01.set(diag() if not path else path)
		fintrans = self.dir01.get() + '/' + self.dir01.get().split('/')[-1] + '.intrans'
		ftrace   = self.dir01.get() + '/' + self.dir01.get().split('/')[-1] + '.trace'
		
		# verifing validity of self.dir01
		if not os.path.exists(ftrace) :
			tkMessageBox.showwarning('Warning',ftrace+' file not found')
			self.req2plot['trace01']=False
			self.btplot['state']=tk.DISABLED
			return
		self.req2plot['trace01']=True
		if not os.path.exists(fintrans):
			tkMessageBox.showwarning('Warning',fintrans+' file not found')
			self.req2plot['intrans01']=False
			self.btplot['state']=tk.DISABLED
			return
		self.req2plot['intrans01']=True
		
		# temperature
		self.tmax01,self.dt01=map(eval,open(fintrans,'r').readlines()[7].split()[:2])
		self.nt01=int(self.tmax01/self.dt01)
		
		# fermi energy 
		self.data01=np.loadtxt(ftrace)
		self.ef01   = eval(open(fintrans,'r').readlines()[2].split()[0])
		self.data01[:,0] = self.data01[:,0] - self.ef01
		self.mine01 = min(self.data01[:,0])
		self.maxe01 = max(self.data01[:,0])
		self.de01   = self.maxe01 - self.mine01
		self.ne01   = int(self.de01/eval(open(fintrans,'r').readlines()[2].split()[1]) + 1)
		#self.dde01  = min(data01[0:-1,0]-data01[1:,0])
		
		self.sel_xcolumn()
		
	def __diag_def02(self,path=None):
		self.dir02.set(diag() if not path else path)
		fintrans = self.dir02.get() + '/' + self.dir02.get().split('/')[-1] + '.intrans'
		ftrace   = self.dir02.get() + '/' + self.dir02.get().split('/')[-1] + '.trace'
		
		# verifing validity of self.dir02
		if not os.path.exists(ftrace ) :
			tkMessageBox.showwarning('Warning',ftrace +' file not found')
			self.req2plot['trace02']=False
			self.btplot['state']=tk.DISABLED
			return
		self.req2plot['trace02']=True
		if not os.path.exists(fintrans):
			tkMessageBox.showwarning('Warning',fintrans+' file not found')
			self.req2plot['intrans02']=False
			self.btplot['state']=tk.DISABLED
			return
		self.req2plot['intrans02']=True
		
		# temperature
		self.tmax02,self.dt02=map(eval,open(fintrans,'r').readlines()[7].split()[:2])
		self.nt02=int(self.tmax02/self.dt02)
		
		# fermi energy
		self.data02=np.loadtxt(ftrace)
		self.ef02   = eval(open(fintrans,'r').readlines()[2].split()[0])
		self.data02[:,0] = self.data02[:,0] - self.ef02
		self.mine02 = min(self.data02[:,0])
		self.maxe02 = max(self.data02[:,0])
		self.de02   = self.maxe02 - self.mine02
		self.ne02   = int(self.de02/eval(open(fintrans,'r').readlines()[2].split()[1]) + 1)
		#self.dde02  = min(data02[0:-1,0]-data02[1:,0])
		
		self.sel_xcolumn()
		
	def sel_xcolumn(self):
		self.slb01.set('Fermi Energy' if self.xcolumn.get() else 'Temperature')
		if not self.dir01.get() == '' and not self.dir02.get() == '':
			# selecting which to use
			if not self.xcolumn.get():
				self.xgrid01=self.data01[self.data01[:,0]==self.data01[0,0]][:,1]
				self.xgrid02=self.data02[self.data02[:,0]==self.data02[0,0]][:,1]
				if self.nt01 < self.nt02:
					self.sc01['to']=self.nt01-1
					#self.mindelta=min(self.data01[1:,1] - self.data01[:-1,1])
				else:
					self.sc01['to']=self.nt02-1
					#self.mindelta=min(self.data02[1:,1] - self.data02[:-1,1])
			else:
				self.xgrid01=self.data01[self.data01[:,1]==self.data01[0,1]][:,0]
				self.xgrid02=self.data02[self.data01[:,1]==self.data02[0,1]][:,0]
				if self.ne01 < self.ne02:
					self.sc01['to']=self.ne01-1
					#self.mindelta=min(self.data01[1:,0] - self.data01[:-1,0])
				else:
					self.sc01['to']=self.ne02-1
					#self.mindelta=min(self.data02[1:,0] - self.data02[:-1,0])

			#	setting plot button to bee clickable
			if all(self.req2plot.values()): self.btplot['state']=tk.NORMAL
		
	def sel_scale(self,val):
		self.doubleval_sc01.set(list(self.xgrid01)[self.intval_sc01.get()])
		self.doubleval_sc02.set(list(self.xgrid02)[self.intval_sc01.get()])
		pass
		
	def plot(self):
		data01=self.data01
		data02=self.data02
		
		var1     = self.doubleval_sc01.get()
		var2     = self.doubleval_sc02.get()
		xcolumn = self.xcolumn.get()
		ycolumn = self.ycolumn.get()
		
		xlabel = 'Temperature (K)' if xcolumn else 'Fermi Energy (eV)'
		ylabel = {2:'N (e/uc)',
		          3:'n (mu) (e/uc)',
		          4:'S (V/K)',
		          5:'sig/tau [(ommega m s)^-1]',
		          6:'R_h (m^3/C)',
		          7:'kappa0',
		          8:'c',
		          9:'X',
		          10:'ZT'}[ycolumn]

		x01=data01[data01[:,int(not xcolumn)]==var1][:,xcolumn]
		x02=data02[data02[:,int(not xcolumn)]==var2][:,xcolumn]
		
		if ycolumn == 10:
			y01=data01[data01[:,int(not xcolumn)]==var1][:,4]**2 * data01[data01[:,int(not xcolumn)]==var1][:,5] * var1 / data01[data01[:,int(not xcolumn)]==var1][:,7]
			y02=data02[data02[:,int(not xcolumn)]==var2][:,4]**2 * data02[data02[:,int(not xcolumn)]==var2][:,5] * var2 / data02[data02[:,int(not xcolumn)]==var2][:,7]
		else:
			y01=data01[data01[:,int(not xcolumn)]==var1][:,ycolumn]
			y02=data02[data02[:,int(not xcolumn)]==var2][:,ycolumn]
	
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.grid(True)
		
		plt.plot(x01,y01,x02,y02)
		
		plt.legend(['first','second'])
		
		plt.show()

menu()
