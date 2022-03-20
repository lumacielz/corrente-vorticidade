
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:12:50 2022

@author: luiza.maciel
"""


import numpy as np
import meshio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.tri as tri

#leitura da malha
mesh = meshio.read('cilindro_aq.msh')
X = mesh.points[:,0]
Y = mesh.points[:,1]

IEN = mesh.cells['triangle']
IENbound = mesh.cells['line']
IENboundTypeElem = list(mesh.cell_data['line']['gmsh:physical'] - 1)
boundNames = list(mesh.field_data.keys())
IENboundElem = [boundNames[elem] for elem in IENboundTypeElem]

# Cria lista de nos do contorno
cc = IENbound.reshape(IENbound.size) # lista de nos do contorno
ccName = [[] for i in range(len(cc))]  # lista com os nomes das cc's


npoints = len(X)
ne = IEN.shape[0]


#cc1 = cc[24:125]
#cc2 = cc[125:157]
#cc3 = cc[157:258]
#cc4 = cc[259:290]
#cc5 = cc[:24]

cc1 = cc[235:404]
cc2 = cc[203:234]
cc3 = cc[33:202]
cc4 = cc[2:32]
cc5 = cc[404:]

#parametros
ni = 0.025
alpha = ni
rho = 1.0
cp = 1.0
q = 0.0
dt = 0.01
niter = 140

#inicializacao das matrizes
K = np.zeros( (npoints,npoints),dtype='float' )
M = np.zeros( (npoints,npoints),dtype='float' )
Gx = np.zeros( (npoints,npoints),dtype='float' )
Gy = np.zeros( (npoints,npoints),dtype='float' )

#montagem das matrizes
for e in range(0,ne):
    [v1,v2,v3] = IEN[e]
    ai = X[v2]*Y[v3]-X[v3]*Y[v2]
    aj = X[v3]*Y[v1]-X[v1]*Y[v3]
    ak = X[v1]*Y[v2]-X[v2]*Y[v1]
    area = 0.5*(ai+aj+ak)
    
    bi = Y[v2] - Y[v3]
    bj = Y[v3] - Y[v1]
    bk = Y[v1] - Y[v2]
    
    ci = X[v3] - X[v2]
    cj = X[v1] - X[v3]
    ck = X[v2] - X[v1]
    
    kxelem = (1.0/(4*area))*np.array([ [bi*bi,bi*bj,bi*bk],[bj*bi,bj*bj,bj*bk],[bk*bi,bk*bj,bk*bk]])
    kyelem = (1.0/(4*area))*np.array([ [ci*ci,ci*cj,ci*ck],[cj*ci,cj*cj,cj*ck],[ck*ci,ck*cj,ck*ck]])
    kelem = kxelem + kyelem
    
    gxelem = (1.0/6)* np.array([[bi,bj,bk],[bi,bj,bk],[bi,bj,bk]])
    gyelem = (1.0/6)* np.array([[ci,cj,ck],[ci,cj,ck],[ci,cj,ck]])
    
    melem = (area/12.0)*np.array([[2.0,1.0,1.0],[1.0,2.0,1.0],[1.0,1.0,2.0]])

    
    for ilocal,jlocal in zip(range(0,3),range(0,3)):
        iglobal = int(IEN[e,ilocal])
        for jlocal in range(0, 3):
            jglobal = int(IEN[e,jlocal])
            K[iglobal,jglobal] += kelem[ilocal,jlocal]
            M[iglobal,jglobal] += melem[ilocal,jlocal]
            Gx[iglobal,jglobal] += gxelem[ilocal,jlocal]
            Gy[iglobal,jglobal] += gyelem[ilocal,jlocal]

#condicoes iniciais
vx = np.zeros(npoints, dtype = 'float')
vy = np.zeros(npoints, dtype = 'float')
corr = np.zeros(npoints, dtype = 'float')
wz = np.zeros(npoints, dtype = 'float')
T = np.zeros(npoints, dtype = 'float')

#aplicando condicoes de contorno da velocidade antes de calcular wzc e A na primeira iteração
for c in cc3: #paredeinf
    vx[c] = 0.0
    vy[c] = 0.0
    
#    if ccName[c] == 'out': # sem cc
#        vx[c] = 0.0
#        vy[c] = 0.0
        
for c in cc1: #paredesup
    vx[c] = 0.0
    vy[c] = 0.0
     
for c in cc4:#entrada
    vx[c] = 1.0
    vy[c] = 0.0

for c in cc5:#circulo
    vx[c] = 0.0
    vy[c] = 0.0


Minv = np.linalg.inv(M.copy())

#matriz A da funcao corrente- não muda no tempo
Ac = K.copy()  
#matriz da funcao velocidade - fixa no tempo
Av = M.copy() 

#diagonais para condicoes de contorno
for c in cc3:
    Ac[c,:] = 0.0
    Ac[c,c] = 1.0
    Av[c,:] = 0.0
    Av[c,c] = 1.0
    
#    if ccName[c] == 'direita': #neuman
#        Ac[c,:] = 0.0
#        Ac[c,c] = 1
#        Av[c,:] = 0.0
#        Av[c,c] = 1
        
for c in cc1:
    Ac[c,:] = 0.0
    Ac[c,c] = 1.0
    Av[c,:] = 0.0
    Av[c,c] = 1.0
 
for c in cc4:
    Ac[c,:] = 0.0
    Ac[c,c] = 1.0
    Av[c,:] = 0.0
    Av[c,c] = 1.0

for c in cc5:
    Ac[c,:] = 0.0
    Ac[c,c] = 1.0
    Av[c,:] = 0.0
    Av[c,c] = 1.0


#loop temporal
for i in range(0, niter):
    #define condicoes de contorno em wz usando as condicoes de contorno em vx,vy
    wzc = Minv @  (Gx @ vy - Gy @vx) 
    A = (M/dt) + ni * K + (np.diag(vx)@Gx + np.diag(vy)@Gy)
    b = (M/dt)@wz
    
    #impor cc para A e b de wz pois variam com vx vy e wz a cada passo
    for c in cc3:
        A[c,:] = 0.0
        A[c,c] = 1.0
        b[c] = wzc[c]
    
    for c in cc2:
        A[c,:] = 0.0
        A[c,c] = 1.0
        b[c] = wzc[c]
        
    for c in cc1:
        A[c,:] = 0.0
        A[c,c] = 1.0
        b[c] = wzc[c]
        
    for c in cc4:
        A[c,:] = 0.0
        A[c,c] = 1.0
        b[c] = wzc[c]
        
    for c in cc5:
        A[c,:] = 0.0
        A[c,c] = 1.0
        b[c] = wzc[c]
       
    #solucao da vorticidade
    wz = np.linalg.solve(A,b)
    
    #funcao corrente - b varia com o tempo
    bc = M@wz
    
    for c in cc3:
        bc[c] = 0.0
    for c in cc1:
        bc[c] = 1.0
    for c in cc4:
        bc[c] =  Y[c] 
    for c in cc5:
        bc[c] = 0.5

    #solucao da funcao corrente
    corr = np.linalg.solve(Ac,bc)
    
    #lado direito da equacao varia com o tempo
    bvx = Gy@corr
    bvy = -Gx@corr
    
    for c in cc3:
        bvx[c] = 0.0
        bvy[c] = 0.0
    
#        if ccName[c] == 'out': #neuman nulo
#            bvx[c] = 0.0
#            bvy[c] = 0.0
        
    for c in cc1:
        bvx[c] = 0.0
        bvy[c] = 0.0
     
    for c in cc4:
        bvx[c] = 1.0
        bvy[c] = 0.0
    
    for c in cc5:
        bvx[c] = 0.0
        bvy[c] = 0.0
 
    vx = np.linalg.solve(Av,bvx) 
    vy = np.linalg.solve(Av,bvy)
    
    At = M/dt + alpha * K + (np.diag(vx)@Gx + np.diag(vy)@Gy)
    bt = M/dt@T
    for c in cc3:
        At[c,:] = 0.0
        At[c,c] = 1
        bt[c] = 0.0
 
    for c in cc1:
        At[c,:] = 0.0
        At[c,c] = 1
        bt[c] = 0.0
    
    for c in cc5:
        At[c,:] = 0.0
        At[c,c] = 1
        bt[c] = 300.0
        
    for c in cc4:
        At[c,:] = 0.0
        At[c,c] = 1
        bt[c] = 0.0
    
    T = np.linalg.solve(At,bt)

#plots de resultados
#plt.figure(1)    
#fig, ax = plt.subplots(2,2, figsize=(15,5))
triangulation = tri.Triangulation(X,Y,IEN)
#ax[0][0].set_aspect('equal')
#ax[0][0].triplot(X,Y,IEN, linewidth=0.5)
##ax[0][0].plot(X[cc],Y[cc],'bo')
#corrp = ax[0][0].tricontourf(triangulation, corr, cmap='coolwarm')
#ax[0][0].set_title('Função Corrente (Ψ)')
#fig.colorbar(corrp,ax = ax[0][0], shrink=1.0)
#
#ax[1][0].set_aspect('equal')
#ax[1][0].triplot(X,Y,IEN, linewidth=0.5)
##ax[1][0].plot(X[cc],Y[cc],'bo')
#wzp = ax[1][0].tricontourf(triangulation, wz, cmap='coolwarm')
#ax[1][0].set_title('Vorticidade (Wz)')
#fig.colorbar(wzp,ax = ax[1][0], shrink=1.0)
#
#ax[0][1].set_aspect('equal')
#ax[0][1].triplot(X,Y,IEN, linewidth=0.5)
##ax[0][1].plot(X[cc],Y[cc],'bo')
#vyp = ax[0][1].tricontourf(triangulation, vy, cmap='coolwarm')
#ax[0][1].set_title('Velocidade em y')
#fig.colorbar(vyp,ax = ax[0][1], shrink=1.0)
#
#ax[1][1].set_aspect('equal')
#ax[1][1].triplot(X,Y,IEN, linewidth=0.5)
##ax[1][1].plot(X[cc5],Y[cc5],'bo')
#vxp = ax[1][1].tricontourf(triangulation, vx, cmap='coolwarm')
#ax[1][1].set_title('Velocidade em x')
#fig.colorbar(vxp,ax = ax[1][1], shrink=1.0)
#for i in range(len(niter)):
#    point_data = {'x' : X}
#    data_vy = {'y' : Y}
#    data_psi = { 'corrente' : corr}
#    point_data.update(data_vy)
#    point_data.update(data_psi)
#    meshio.write_points_cells('solucao-'+str(i)+'.vtk', mesh.points, mesh.cells, point_data=point_data)
plt.figure(2,figsize=(10,8))
ax = plt.axes()
ax.set_aspect('equal')
ax.triplot(X,Y,IEN, linewidth=0.5)
#ax.plot(X[cc],Y[cc],'bo')
temp = ax.tricontourf(triangulation, T, cmap='coolwarm')
ax.set_title('Temperatura')
plt.colorbar(temp, shrink=0.5)
#
plt.show()



