
# coding: utf-8


import os
import difflib
import Tkinter as tk
from tkFileDialog import askdirectory as diag


def get_data(orig):
        traces=set()
        for p,n,f in os.walk(orig):
            trace_file = p.split('/')[-1]+'.trace'
            if len(f) is not 0 and trace_file in f:
                traces.add(p+'/'+trace_file)
        
        ele={p.split('/')[1] for p in traces}
        val = []
        for e in ele:
            r = set()
            s = set()
            for i in traces:
                if i.split('/')[1] != e:
                    continue
                if i.split('/')[2] == 'ref':
                    r.add(i.split('/')[3])
                if i.split('/')[2] == 'siesta':
                    s.add(i.split('/')[3])
            val.append([e,list(r.intersection(s))])
        return dict(val)

class menu:
	def __init__(self,data):
		root=tk.Tk()
		root.title('S-BT-Vis')
		frame01=tk.Frame(root)
		frame02=tk.Frame(root)
		frame03=tk.Frame(root)
		frame03a=tk.Frame(frame03)
		frame03b=tk.Frame(frame03)
		frame04=tk.Frame(root)
		frame04a=tk.Frame(frame04)
		frame04b=tk.Frame(frame04)
		frame01.pack(side=tk.TOP)
		frame02.pack(side=tk.TOP)
		frame03.pack(side=tk.TOP)
		frame04.pack(side=tk.TOP)
		frame04a.pack(side=tk.TOP)
		frame04b.pack(side=tk.TOP)

		self.data   = data
		self.ele    = tk.StringVar()
		self.xlabel = tk.StringVar()
		self.slb01  = tk.StringVar()
		self.vsc01  = tk.IntVar()
		self.nk     = tk.IntVar()
		self.column = tk.IntVar()
		
		self.ele.set('Si')
		self.xlabel.set('E. Fermi')
		self.vsc01.set(0)
		self.nk.set(30)
		self.column.set(5)
		
#		bk=button_nkp(frame02,data)
		tk.Label(frame02,text='Number of k-points').pack(side=tk.TOP)
		vals=set(w for v in self.data.values() for w in v)
		allowed=set([v for v in data[self.ele.get()]])
		self.rbt=[]
		for n,nk in enumerate(vals):
			state = tk.NORMAL if nk in allowed else tk.DISABLED
			self.rbt.append(tk.Radiobutton(frame02,text=nk,variable=self.nk,value=nk,command=self.sel_nk,state=state))
			self.rbt[n].pack(side=tk.RIGHT)

		#elm=ele_menu(frame01,data,self.ele,bk.remake)
		tk.Label(frame01,text='Select BoltzTraP Foltders').pack(side=tk.TOP)
		frame01a=tk.Frame(frame01)
		self.dir01 = tk.StringVar()
		self.dir02 = tk.StringVar()
		#self.dir01.set('/home/')
		#self.dir02.set('/home/')
		
		def diag_def01():
			self.dir01.set(diag())
		def diag_def02():
			self.dir02.set(diag())
		
		tk.Entry(frame01a,textvariable=self.dir01).grid(column=2,row=1)
		tk.Entry(frame01a,textvariable=self.dir02).grid(column=2,row=2)
		
		tk.Button(frame01a, text='Browse',command=diag_def01).grid(column=1,row=1)
		tk.Button(frame01a, text='Browse',command=diag_def02).grid(column=1,row=2)
		
		frame01a.pack(side=tk.TOP)
		
		#for el in data:
		#	tk.Radiobutton(frame01,text=el,variable=self.ele,value=el,command=self.sel_ele).pack(side=tk.LEFT)
	  
		tk.Label(frame03,text='x-axis').pack(side=tk.TOP)
		frame03a.pack(side=tk.TOP)
		frame03b.pack(side=tk.TOP)
		
		#xa=x_axis(frame03a,frame03b)
		self.xlabel.set('Temperature')
		self.slb01.set('Temperature')
		tk.Radiobutton(frame03a,text='Temperature',command=self.sel_xaxis,variable=self.xlabel,value='E. Fermi').pack(side=tk.LEFT)
		tk.Radiobutton(frame03a,text='E. Fermi',command=self.sel_xaxis,variable=self.xlabel,value='Temperature').pack(side=tk.LEFT)
		self.lb01=tk.Label(frame03b,textvariable=self.slb01)
		self.sc01=tk.Scale(frame03b,orient=tk.HORIZONTAL,to=29,variable=self.vsc01,command=self.sel_scale)
		self.lb01.pack(side=tk.TOP)
		self.sc01.pack(side=tk.TOP)
	  
		tk.Label(frame04a,text='y-axis').pack(side=tk.TOP)
		tk.Radiobutton(frame04a,text='N'      ,command=self.plot,variable=self.column,value=3).pack(side=tk.LEFT)
		tk.Radiobutton(frame04a,text='DOS'    ,command=self.plot,variable=self.column,value=4).pack(side=tk.LEFT)
		tk.Radiobutton(frame04a,text='Seebeck',command=self.plot,variable=self.column,value=5).pack(side=tk.LEFT)
		tk.Radiobutton(frame04a,text='s/t'    ,command=self.plot,variable=self.column,value=6).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='R_H'    ,command=self.plot,variable=self.column,value=7).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='kappa0' ,command=self.plot,variable=self.column,value=8).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='c'      ,command=self.plot,variable=self.column,value=9).pack(side=tk.LEFT)
		tk.Radiobutton(frame04b,text='chi'    ,command=self.plot,variable=self.column,value=10).pack(side=tk.LEFT)
	  
	  
		root.mainloop()
	
	def get_var_ele(self):
		return self.ele
		
	def sel_ele(self):
		self.remake(self.ele)
		
	def remake(self,ele):
		vals=set([v for v in data[ele.get()]])
		for rbt in self.rbt:
			rbt['state'] = tk.NORMAL if rbt['value'] in vals else tk.DISABLED
	
	def sel_nk(self):
		self.plot()
		pass
		
	def sel_xaxis(self):
		self.slb01.set(self.xlabel.get())
		self.plot()
		
	def sel_scale(self,val):
		#self.plot()
		pass
		
	def plot(self):
		ele    = self.ele.get()
		nk     = str(self.nk.get())
		column = str(self.column.get())
		vsc    = self.vsc01.get()
		xlabel = 'E. Fermi' if self.xlabel.get() == 'Temperature'  else 'Temperature'
		
		path_file_ref = './'+ele+'/ref/'+nk+'/'+ele+'/'+ele+'.trace'
		path_file_sie = './'+ele+'/siesta/'+nk+'/'+ele+'/'+ele+'.trace'
		
		fref = open(path_file_ref,'r')
		fref.readline()
		v0_ref = fref.readline().split()[0]
		fref.close()
		fsie = open(path_file_sie,'r')
		fsie.readline()
		v0_sie = fsie.readline().split()[0]
		fsie.close()
		
		if xlabel == 'Temperature':
			format = lambda x:'using 2:'+column+' every ::'+str(30*vsc)+'::'+str(30*(vsc+1)-1)
			xlabel += ' (K)'
		else:
			format = lambda x:'using (13.605698065894*(\$1 - '+x+')):'+column+' every 30::'+str(vsc)
			xlabel += ' (eV)'
		ylabel = {3:'N (e/uc)',
		          4:'n ({/Symbol m}) (e/uc)',
		          5:'S (V/K)',
		          6:'{/Symbol s}/{/Symbol t} [({/Symbol w} m s)^-1]',
		          7:'R_H (m^3/C)',
		          8:'{/Symbol k^0}',
		          9:'c',
		          10:'{/Symbol x}'}[self.column.get()]
		os.system('gnuplot -p -e "set xlabel \''+xlabel+'\'; set ylabel \''+ylabel+'\' ; plot \''+path_file_ref+'\' '+format(v0_ref)+'  w l title \'reference\', \''+path_file_sie+'\' '+format(v0_sie)+'  w l title \'siesta\'; pause mouse keypress"')

data=get_data('.')
menu(data)
