# Créé par tydeb, le 20/05/2018
from random import randint
from tkinter import *

fenn=Tk()
fenn.title('accueil jeu')
fenn.configure(bg='green')

#bg=PhotoImage(file='fond_puyo - Copie.gif',master=fenn)
can=Canvas(fenn,width=807,height=615)
can.pack()
#can.create_image(408,307,image=bg)

#definition des valeurs par défaut
#1 - creation des puyos
x1=0 #numero du puyo
dhorizon=3
dparcourue=0
Xpuyo,Ypuyo=109,5
couleurpuyo=0
#2 - destruction des puyo
A=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#pair=couleur    impair=numero du puyo
B=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#ensemble des cases sur chacunes des 6 colonnes
C=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
D=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
E=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
F=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
num_col=[A,B,C,D,E,F]
detruire=[]
faut_detruire=0#savoir si la fonction detruire doit se lancer
#3 - chute des puyo
distance1,distance2,distance3,distance4,distance5,distance6=11,11,11,11,11,11
distance_au_sol=[distance1,distance2,distance3,distance4,distance5,distance6]
tour1,tour2,tour3,tour4,tour5,tour6=0,0,0,0,0,0
tour=[tour1,tour2,tour3,tour4,tour5,tour6]

def credit():
    creditfen=Tk()
    creditfen.title('Crédits')
    creditfen.configure(bg='black')
    textcredit=Label(creditfen,text='REALISE PAR :\nTanguy de Bettignies, TS2\n Thomas Verhille, TS2\n\nRemerciement à M.Crabbé et M.Pajonk pour leurs conseils et leur soutien',bg='white').pack()


#creation de la grille
def grille1():
    global grille
    a,b=56,56
    while a!=316:
        grille.create_line(a,0,a,628)
        a=a+52
    while b!=628:
        grille.create_line(0,b,316,b)
        b=b+52
    grille.create_rectangle(3,3,317,629,width=3)
    grille.create_line(116,12,152,48,fill='red',width=8)
    grille.create_line(152,12,116,48,fill='red',width=8)
    grille.create_line(3,3,3,3,fill='white')
    grille.grid(row=2,column=1)

#mise en place de la gravité
s,g=0,0 #passer de commencer a stop.
def vitesse_chute():
    global g,tour,fen
    if g==0:
        fen.after(30,puyo)
    elif g==1:
        fen.after_cancel(puyo)
    elif tour[2]==12:
        puyo()

def marche_arret(event):
    global s,g
    if s==0:
        s,g=1,0
        vitesse_chute()
    elif s==1:
        g=1
        vitesse_chute()
        s=0

def puyo():
    global Xpuyo,Ypuyo,dparcourue,couleur,puyo1color,g,dhorizon,tour,distance_au_sol,puyo1,couleurpuyo,x1,nextcolor1,nextcolor2,couleursuivante,couleurapres,perdue,col,fen,grille
    if dparcourue==0 and dhorizon==3:
        x1=x1+1
        couleur=['yellow','red','green','blue']
        puyo1color=nextcolor1
        nextcolor1=nextcolor2
        nextcolor2=couleur[randint(0,3)]
        col.configure(bg=nextcolor1)
        couleursuivante.configure(bg=nextcolor1)
        couleurapres.configure(bg=nextcolor2)
        #donne un chiffre en fonction de la couleur
        if puyo1color=='yellow':
            couleurpuyo=1
        if puyo1color=='blue':
            couleurpuyo=2
        if puyo1color=='green':
            couleurpuyo=3
        if puyo1color=='red':
            couleurpuyo=4
        puyo1=grille.create_oval(Xpuyo,Ypuyo,Xpuyo+50,Ypuyo+50,fill=puyo1color)
        grille.coords(puyo1,Xpuyo,Ypuyo,Xpuyo+50,Ypuyo+50)
    if tour[2]==11:
        g=1
        perdue.configure(bg="red",text="Game Over",pady=50)
    if g==0:
        Ypuyo=Ypuyo+13
        dparcourue=dparcourue+0.25
        grille.coords(puyo1,Xpuyo,Ypuyo,Xpuyo+50,Ypuyo+50)
        fen.after(30,puyo)
    if distance_au_sol[dhorizon-1]-dparcourue==0:
        fin_chute()

def fin_chute():
    global Xpuyo,Ypuyo,dhorizon,tour,distance_au_sol,dparcourue,num_col,couleurpuyo,x1,detruire,faut_detruire,combo
    Ypuyo,Xpuyo=5,109
    tour[dhorizon-1]=tour[dhorizon-1]+1
    distance_au_sol[dhorizon-1]=11-tour[dhorizon-1]
    num_col[dhorizon-1][2*(tour[dhorizon-1]-1)]=couleurpuyo
    num_col[dhorizon-1][2*(tour[dhorizon-1]-1)+1]=x1
    combo=0
    for i in range (10):#à modifier pour avoir un truc plus précis qui s'active quand nécessaire
        faut_detruire=0
        detruire=[]
        verif_destruction_horizon()
        verif_destruction_vertical()
        if faut_detruire==1:
            destruction()
            combo=combo+1
    dhorizon=3
    dparcourue=0

def a_gauche(event):
    global Xpuyo,dhorizon,distance_au_sol,dparcourue,tour,puyo1,grille
    if distance_au_sol[dhorizon-1]-dparcourue!=0 and dparcourue+tour[dhorizon-2]<=10.75:
        if dhorizon!=1:
            Xpuyo=Xpuyo-52
            grille.coords(puyo1,Xpuyo,Ypuyo,Xpuyo+50,Ypuyo+50)
            dhorizon=dhorizon-1

def a_droite(event):
    global Xpuyo,dhorizon,distance_au_sol,dparcourue,tour,puyo1,grille
    if distance_au_sol[dhorizon-1]-dparcourue!=0 and dparcourue+tour[dhorizon]<=10.75:
        if dhorizon!=6:
            Xpuyo=Xpuyo+52
            grille.coords(puyo1,Xpuyo,Ypuyo,Xpuyo+50,Ypuyo+50)
            dhorizon=dhorizon+1

def verif_destruction_horizon():
    global num_col,detruire,tour,distance_au_sol,faut_detruire
    b=0
    while b<23:
        a=0
        while a<4:
            if num_col[a][b]==num_col[a+1][b]==num_col[a+2][b]!=0:
                detruire.append(num_col[a][b+1]+20),detruire.append(num_col[a+1][b+1]+20),detruire.append(num_col[a+2][b+1]+20)
                num_col[a][b+1],num_col[a+1][b+1],num_col[a+2][b+1]=0,0,0
                distance_au_sol[a],distance_au_sol[a+1],distance_au_sol[a+2]=distance_au_sol[a]+1,distance_au_sol[a+1]+1,distance_au_sol[a+2]+1
                tour[a],tour[a+1],tour[a+2]=tour[a]-1,tour[a+1]-1,tour[a+2]-1
                faut_detruire=1
                a=a+2
                if a<5:
                    if num_col[a][b]==num_col[a+1][b]!=0:
                        detruire.append(num_col[a+1][b+1]+20)
                        num_col[a+1][b+1]=0
                        distance_au_sol[a+1]=distance_au_sol[a+1]+1
                        tour[a+1]=tour[a+1]-1
                        a=a+1
                        if a<5:
                            if num_col[a][b]==num_col[a+1][b]!=0:
                                detruire.append(num_col[a+1][b+1]+20)
                                num_col[a+1][b+1]=0
                                distance_au_sol[a+1]=distance_au_sol[a+1]+1
                                tour[a+1]=tour[a+1]-1
                                a=a+1
                                if a<5:
                                    if num_col[a][b]==num_col[a+1][b]!=0:
                                        detruire.append(num_col[a+1][b+1]+20)
                                        num_col[a+1][b+1]=0
                                        distance_au_sol[a+1]=distance_au_sol[a+1]+1
                                        tour[a+1]=tour[a+1]-1
                                        a=a+1
            else:
                a=a+1
        b=b+2

def verif_destruction_vertical():
    global num_col,detruire,distance_au_sol,tour,faut_detruire
    b=0
    while b<6:
        a=0
        while a<19:
            if num_col[b][a]==num_col[b][a+2]!=0:
                a=a+2
                if num_col[b][a]==num_col[b][a+2]!=0:
                    detruire.append(num_col[b][a-1]+20),detruire.append(num_col[b][a+1]+20),detruire.append(num_col[b][a+3]+20)
                    num_col[b][a-1],num_col[b][a+1],num_col[b][a+3]=0,0,0
                    distance_au_sol[b]=distance_au_sol[b]+3
                    tour[b]=tour[b]-3
                    faut_detruire=1
                    a=a+2
                    if num_col[b][a]==num_col[b][a+2]!=0:
                        detruire.append(num_col[b][a+3]+20)
                        num_col[b][a+3]=0
                        distance_au_sol[b]=distance_au_sol[b]+1
                        tour[b]=tour[b]-1
                        a=a+2
            else:
                a=a+2
        b=b+1

def destruction(): #dans num_col, seul les numero sont reinitialisé mais pas les couleurs necessaire à la verif
    global detruire,num_col,distance_au_sol,tour,faut_detruire,score,combo,grille,scoring#il faut desormais reinitialisé les couleurs
    for i in detruire: score=score+10*(2**combo)#et faire chuter les puyos
    for i in range(3):#et mettre le score a jour
        for i in detruire: grille.delete(i)
        b=0
        while b<21:
            a=0
            while a<6:
                if num_col[a][b+1]==0 and num_col[a][b+2]!=0:
                    grille.coords(num_col[a][b+3]+20,a*52+5,572-(b/2)*52+5,a*52+55,572-(b/2)*52+55)
                if num_col[a][b+1]==0:
                    num_col[a][b],num_col[a][b+1],num_col[a][b+2],num_col[a][b+3]=num_col[a][b+2],num_col[a][b+3],0,0
                a=a+1
            b=b+2
    scoring.configure(bg="limegreen",text=score)

def game():
    global score,combo,couleur,nextcolor1,nextcolor2,scoring,couleursuivante,couleurapres,perdue,grille,col,fen
    fen=Tk()
    fen.title("ONE-Puyo")
    fen.geometry("1272x960+0+0")
    fen.configure(bg="limegreen")

    score=0
    combo=0
    couleur=['yellow','red','green','blue']
    nextcolor1=couleur[randint(0,3)]
    nextcolor2=couleur[randint(0,3)]

    #grille de jeu
    #perdue est invisible avant la défaite du joueur.
    scoring=Label(fen,bg="limegreen",text=score,pady=2)
    scoring.grid(row=1,column=1)
    couleursuivante=Label(fen,height='6',width='15',bg=nextcolor1)
    couleursuivante.grid(row=2,column=3)
    col=Label(fen,bg=nextcolor1,text='couleur suivante')
    col.grid(row=2,column=3)
    couleurapres=Label(fen,height='6',width='15',bg=nextcolor2)
    couleurapres.grid(row=2,column=4)
    perdue=Label(fen,bg="limegreen",padx=250)
    perdue.grid(row=1)
    grille=Canvas(fen,width=317,height=629,bg="white")
    grille1()
    fen.bind("<Left>",a_gauche)
    fen.bind("<Right>",a_droite)
    fen.bind("<space>",marche_arret)

    fen.mainloop()


def commandes():
    commandfen=Tk()
    commandfen.title('Commands')
    commandfen.configure(bg='black')
    textcommand=Label(commandfen,text='COMMANDS :\n\nSTART&STOP = SPACE BAR\nUSE THE DIRECTIONNALS ARROWS TO MOVE RIGHT OR LEFT\n\nTHANKS FOR PLAYING OUR GAME ;)',bg='white').pack()

menu=LabelFrame(fenn,bg='gold2',text='MENU',padx='40',pady='50',labelanchor='n')
menu.place(relx='0.6',rely='0.5',anchor='center')
lancement=Button(menu,text='PLAY',bg='red',command=game,padx='18',pady='5')
lancement.pack()
rien1=Label(menu,pady='5',text=' ',bg='gold2')
rien1.pack()
option=Button(menu,text='COMMANDS',bg='green',command=commandes,padx='10',pady='5')
option.pack()
rien2=Label(menu,pady='5',text=' ',bg='gold2')
rien2.pack()
Credit=Button(menu,text='CREDITS',bg='blue',command=credit,padx='13',pady='5')
Credit.pack()

fenn.mainloop()
