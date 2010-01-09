
PROGRAM RechPic;

{ Utiliser 64000 octets pour la pile }

USES
    OutPut,Lecspef2,Leceffi;
TYPE
    Painv = ^Tainv;
    Tainv =Array[1..30,1..30] of EXTENDED;
    Recpic = Record
             N_P      : Integer;   { Nø du pic }
             It       : Integer;   { Nb. d'it‚ration }
             Abscisse : Real;      { Abscisse du pic }
             Left     : Integer;   { Canal gauche zone pic }
             Pw       : Integer;   { Largeur zone pic en canaux }
             Bgnd     : Real;      { Bruit de fond }
             Fwhm     : Real;      { R‚solution en keV }
             Area     : Real;      { Aire du pic }
             Ener     : Real;      { Energie du pic }
             CtsSec   : Real;      { Coups par seconde }
             Erreur   : Real;      { Erreur en % }
             Eff      : Real;      { Efficacit‚ }
             Fit      : Real;      { Chi2 sur le fit gaussien }
             END;
Fich         =   File of Recpic;
TexFil =     Record
             I       : Integer;
             Fichier : STRING[80];
             END;
FilEnr       = File of TexFil;
VAR
   Il, K_Can, Nc_Correl, Id, Fi, I_Debut, I_Fin, Old_Fi, Jf , Nc_Deriv: INTEGER;
   Jimp , J1, J2 : INTEGER;
   A1, B1, Y1, Y2, Ro, K_Res : REAL;
   Moy_Aval, Moy_Amont : LONGINT;
   FlZdeb, FlZfin : BOOLEAN;
   Ainv    : Painv;
   f, Gf : TEXT;
   Fichier, Rep : String;
   EnrPic  : Fich;
   Penr    : Recpic;
   Adr     : FilEnr;
   Enr     : TexFil;
FUNCTION FNcanal ( I , N_fonction , N_bit : INTEGER) : LONGINT;
{
        Fonction … quadruple action selon le nø de N_fonction
                 1 - Permet d'obtenir l'octet de poids fort
                     d'un canal ( octet d'‚tat )
                 2 - Permet de masquer l'octet de poids fort
                     d'un canal et donc d'obtenir son contenu
                 3 - Permet d'activer un bit d'‚tat de l'octet
                     de poids fort selon la variable N_bit (0 … 7)
                 4 - Permet de d‚activer un bit d'‚tat de l'octet
                     de poids fort selon la variable N_bit(0 … 7)
        I = nø du canal de travail
}
TYPE
    ByteRec     = RECORD
                  FaibleB,FortB : BYTE;
                  END;
    WordRec     = RECORD
                  FaibleW,FortW : WORD;
                  END;
VAR
    Oct_Fort_Int , J  : INTEGER;
    Oct_Fort_Lint     : LONGINT;
BEGIN
     Oct_Fort_Int := ByteRec(WordRec(Contenu_Canal[I]).FortW).FortB;
     Oct_Fort_Lint := LONGINT(Oct_Fort_Int);
     CASE N_fonction OF

          1 :  { Octet de poids fort }
            FNcanal := Oct_Fort_Lint;

          2 :  {     Contenu         }
            FNcanal := Contenu_Canal[I] - (Oct_Fort_Lint*16777216);

          3 :  { Activation bit de marquage }
            BEGIN
            Oct_Fort_Lint := TRUNC(Exp(N_bit*0.6931471806)+0.5);
            Oct_Fort_Lint := Oct_Fort_Int OR WordRec(Oct_Fort_Lint).FaibleW;
            FNcanal := FNcanal(I,2,0) + (Oct_Fort_Lint*16777216);
            END;

          4 :  { D‚activation bit de marquage }
            BEGIN
            Oct_Fort_Lint := TRUNC(Exp(N_bit*0.6931471806)+0.5);
            Oct_Fort_Lint := Oct_Fort_Int AND NOT(WordRec(Oct_Fort_Lint).FaibleW);
            FNcanal := FNcanal(I,2,0) + (Oct_Fort_Lint*16777216);
            END;
     END;
END;
    { D‚termination de l'‚nergie d'un canal donn‚ }

FUNCTION Energy ( No_Can : Integer) : Real;
BEGIN
  Energy :=((No_Can)*((No_Can)*Coef_A_Cal_Ener+Coef_B_Cal_Ener)+Coef_C_Cal_Ener);
END;

    { D‚termination de la r‚solution pour une ‚nergie donn‚ }

FUNCTION Resolution ( Ener : Real) : Real;
BEGIN
  IF ((Ener < 513) AND (Ener > 509)) THEN Ener := Ener*1.8;
  Resolution := Ro + K_Res*Ener;
END;

    { Fonction recherche d‚but de zone }
FUNCTION FNzonDeb : INTEGER;
VAR
   Co : LONGINT;
BEGIN
     FOR Il := K_Can DOWNTO (K_Can - (Nc_Correl+1)*2) DO
         BEGIN
              Id := Il -1;
              IF Il < 3 THEN EXIT;
              Co := FNcanal((Il-1),2,0) + FNcanal((Il-2),2,0);
              IF (FNcanal(Il,2,0)+Co <= FNcanal(Il-3,2,0)+Co) OR (Il = (K_Can - Nc_Correl*2)) THEN
              BEGIN
                   Moy_Amont := ((FNcanal(Il,2,0)+Co) DIV 3);
                   FlZdeb := True;
                   FNzonDeb := Id;
                   EXIT;
              END;
         END;
END;
     { Fonction recherche fin de zone }
FUNCTION FNzonFin : INTEGER;
VAR
   Co : LONGINT;
BEGIN
     FOR Il := K_Can TO (K_Can+(Nc_Correl+1)*3) DO
     BEGIN
          Fi := Il + 1;
          Co := FNcanal(Il+1,2,0) + FNcanal(Il+2,2,0);
          IF ((FNcanal(Il,2,0) <= Moy_Amont)
           AND (FNcanal(Il,2,0) + Co <= FNcanal(Il+3,2,0) + Co))
           OR (Il = (K_Can+(Nc_Correl + 1)*3)) THEN
          BEGIN
               Moy_Aval := ((FNcanal(Il,2,0)+Co) DIV 3);
               FlZfin := True;
               FNzonFin := Fi;
               EXIT;
          END;
     END;
END;

{ D‚termination de la pente d'une droite  }

FUNCTION Pente ( I : Integer ) : Real; { I = nø du premier canal }
VAR
   XM,YM,XX,XY,RI,pente1  : Real;
   J               : Integer;
BEGIN
   XM := 0;
   YM := 0;
   XX := 0;
   XY := 0;
   RI := I;
   FOR J := I TO (I+Nc_Deriv-1) DO
   BEGIN
       XM := XM + RI;
       YM := YM + FNcanal(J,2,0);
       XX := XX + RI*RI;
       XY := XY + RI*FNcanal(J,2,0);
       RI := RI + 1;
   END;
   XM := XM/Nc_Deriv;
   YM := YM/Nc_Deriv;
   XX := XX/Nc_Deriv;
   XY := XY/Nc_Deriv;
   Pente := (XY - XM*YM)/(XX - XM*XM);
END;

    { Recherhe de pics automatique }
PROCEDURE  Rech_Pics_Auto ;
VAR
   Res_Correl, Barre1, Barre, Contenu_Centre, Contenu_Ailes, Som_Correl, Som  : REAL;
   Old_Canal_Correl, Canal_Correl, Energie, Lmh, Som_Can : REAL;
   Rapport, Som_Nette, Trapeze, Sy, Syg : REAL;
   I, J, I_pic, K_Sommet, Ipic, N_Canaux, K_Max, Old_Id, I_Saut , K ,Demi_Res_Cx, J_fin : INTEGER;
   Marquage_Pic , Can_Sommet , Inflexion : Boolean;

BEGIN
     { D‚termination du canal d‚but et du canal fin de recherche de pics }
     I_Debut := TRUNC((E_Deb_Rpic - Coef_C_Cal_Ener)/Coef_B_Cal_Ener);
     I_Fin := TRUNC((E_Fin_Rpic - Coef_C_Cal_Ener)/Coef_B_Cal_Ener);

     { D‚termination des paramŠtres de la courbe de r‚solution
       selon la formule : Res = Ro + K_Res*Energie  }
     K_Res := (Res_Flanc_Droite - Res_Flanc_Gauche)/(E_Fin_Rpic - E_Deb_Rpic);
     Ro := Res_Flanc_Droite - K_Res*E_Fin_Rpic;

             { Barre = Niveau de d‚tection des pics }
     Barre1 := SensibiliteRp / 6 ;

             { Energy = (Canal milieu }
     Res_Correl := Resolution(Energy(Taille_Spectre -1));
     Nc_Correl := TRUNC(Res_Correl/Coef_B_Cal_Ener);
     IF I_Fin > Taille_Spectre - Nc_Correl*4 THEN I_Fin := Taille_spectre - Nc_Correl*4;
     IF I_debut < 10 THEN I_debut := 10;
     FOR I := I_Debut TO I_Fin DO
         BEGIN
              Contenu_Canal[I] := FNcanal(I,4,0);
              Contenu_Canal[I] := FNcanal(I,4,1);
         END;
     I := I_debut ;
     Contenu_Centre := 0;
     FlZdeb := False ;
     FlZfin := False ;
     Som_Correl := 0;
     I_pic := 0;
     Old_Canal_Correl := 0;

           { D‚but de la boucle de transcorr‚lation }

     K_Can := (I + Nc_Correl*3 ) ;
     J_fin := I_fin - Nc_Correl*4;
     FOR J := I_debut TO J_fin DO
         BEGIN
              Res_Correl := Resolution(Energy(J-1));
              Nc_Correl := ROUND(Res_Correl/Coef_B_Cal_Ener);
              IF Nc_Correl > 1 THEN Nc_Correl := Nc_Correl - 1;
              K_Can := (J + Nc_Correl * 2 ) - 1 ;
              Contenu_Ailes := 0;
              FOR J1 := J to J + (Nc_Correl * 4) - 1 DO
              Contenu_Ailes := Contenu_Ailes + (FNcanal(J1,2,0));
              J2 := J + Nc_Correl ;
              Contenu_Centre := 0;
              FOR J1 := J2 to ( J2 + Nc_Correl*2 - 1) DO
              Contenu_Centre := Contenu_Centre + (FNcanal(J1,2,0));
              Contenu_Ailes := Contenu_Ailes - Contenu_Centre;
              Barre := SQRT(Contenu_Ailes) * Barre1;
              IF Barre < Barre1 then Barre := Barre1;
              Canal_Correl := Contenu_Centre - Contenu_Ailes ;      { Contenu canal corr‚l‚ }
              IF ((Canal_Correl > Barre) AND NOT(FlZdeb)) THEN  Id := FNzonDeb ; { Id = d‚but zone pic }
              IF FlZdeb THEN Som_Correl := Som_Correl + Canal_Correl;

              { D‚termination des sommets de pic }

              IF FlZdeb AND (Canal_Correl > Old_Canal_Correl) THEN
                 BEGIN
                      Contenu_Canal[K_Can -1] := FNcanal(K_Can-1,4,1);
                      Contenu_Canal[K_Can] := FNcanal(K_Can,3,1);
                 END;
              IF (Canal_Correl < Barre) AND NOT(FlZfin) AND FlZdeb THEN  Fi := FNzonFin ; { Fin de zone pic }
              IF FlZdeb AND FlZfin THEN
                 BEGIN
                      { Controle du debut de zone pic }
                      Il := Id - 1;
                      REPEAT
                            Inc(Il);
                            K_Sommet := Il;
                      UNTIL (FNcanal(Il,1,1) AND 2 = 2) OR (Il = Fi);
                      Lmh := Resolution(Energy(K_Sommet))/Coef_B_Cal_Ener;
                      IF Id < Old_Fi THEN Inc(Old_Fi);
                      IF (K_Sommet - Id + 1) > TRUNC(3*Lmh) THEN Id := K_Sommet - TRUNC(3*Lmh);
         { Controle de la fin de la zone pic }
                      Il := Fi + 1;
                      REPEAT
                            Dec(Il);
                            K_Sommet := Il;
                      UNTIL (FNcanal(Il,1,1) AND 2 = 2) OR (Il = Id);
                      Lmh := Resolution(Energy(K_Sommet))/Coef_B_Cal_Ener;
                      IF (Fi - K_Sommet + 1) > TRUNC(3*Lmh) THEN Fi := K_Sommet + TRUNC(3*Lmh);
                      IF (Fi - Id ) > Nc_Correl/2 THEN
                      BEGIN
                           Som_Can := 0;
                           Som := 0;
                           Inc(Ipic);
         { Mise en surbrillance des zones pic }
                           FOR Il := Id TO Fi DO
                           BEGIN
                                Contenu_Canal[Il] := FNcanal(Il,3,0);
                                Som_Can := Som_Can + SQRT(FNcanal(Il,2,0));
                                Som := Som + FNcanal(Il,2,0);
                           END;
                           Old_Fi := Fi;
                           Som_Can := Som_Can - ((SQRT(Moy_Amont+Moy_Aval))/2)*(Fi-Id+1);
         { Test pour ‚liminer les fronts Compton }
                           Rapport := Som_Can/Som_Correl;
         { Si test positif , on efface la surbrillance de la zone }
                           IF Rapport > 2 THEN
                           BEGIN
                                Som_Nette := Som - ((Moy_Amont+Moy_Aval)/2)*(Fi-Id+1);
                                Trapeze := Som - Som_Nette;
                                Sy := (200*SQRT(Som_Nette + 2*Trapeze))/Som_Nette;
                                IF (Sy < 0) OR (Sy > 100) OR (Rapport > 5) OR (Ipic = 1) THEN
                                     FOR Il := Id TO Fi DO
                                     BEGIN
                                          Contenu_Canal[Il] := FNcanal(Il,4,0);
                                          Contenu_Canal[Il] := FNcanal(Il,4,1);
                                     END;
                           END;
                      END
                      ELSE
                           FOR Il := Id TO Fi DO  Contenu_Canal[Il] := FNcanal(Il,4,1);
                      FlZdeb := False;
                      FlZfin := False;
                      Som_Correl := 0;
              END;
         Old_Canal_Correl := Canal_Correl;
     END;
     FlZdeb := False;
     FlZfin := False;
     { Boucle de marquage des pics sommet seconde maniŠre }
     FOR J := (I_Debut + Nc_Correl*2) TO (I_Fin - Nc_Correl*2) DO
     BEGIN
          IF ((( FNcanal(J,1,0) AND 1) = 1) AND NOT(FlZdeb)) THEN
          BEGIN
               FlZdeb := True;
               Id := J;
          END;
          IF ((( FNcanal(J,1,0) AND 1) = 0) AND FlZdeb) THEN
          BEGIN
               FlZfin := True;
               Fi := J - 1;
          END;
          IF FlZdeb AND FlZfin AND (FI > Id) THEN
          BEGIN
     { Effacement des marquages de pic pr‚c‚dents}
               FOR K_Can := Id TO Fi DO
               BEGIN
                    IF (FNcanal(K_Can,1,1) AND 2) =2 THEN
                          Contenu_Canal[K_Can] := FNcanal(K_Can,4,1);
               END;

     { D‚termination des paramŠtres pour le bruit de fond }

               Y1 :=(FNcanal((Id-1),2,0)+FNcanal(Id,2,0)+FNcanal((Id+1),2,0))/3;
               Y2 :=(FNcanal((Fi-1),2,0)+FNcanal(Fi,2,0)+FNcanal((Fi+1),2,0))/3;
               A1 := (Y1-Y2)/(Id-Fi);
               B1 := Y1 - A1*Id;

     { Marquage des sommets de pic }
               K_Can := Fi - ((Fi - Id) DIV 2);
               { Energy = (Energie du canal milieu de zone}
               Nc_Deriv := TRUNC(Resolution(Energy(K_Can))/Coef_B_Cal_Ener) + 1 ;
               IF Nc_Deriv < 2 THEN Nc_Deriv := 2;
               Marquage_Pic := False;
               Can_Sommet   := False;
               Inflexion    := False;
               I_Saut := Id -2;
               FOR K_Can := Id TO (Fi-Nc_Deriv) DO
               BEGIN
                 IF K_Can > I_Saut THEN
                 BEGIN

                       { Si sommet de pic }
                   IF ((Pente(K_Can) > 0) AND (Pente(K_Can+1) <= 0)) THEN
                   BEGIN
                     Marquage_Pic := True;
                     Can_Sommet   := True;
                   END;

                      { Si point d'inflexion pente montante }
                   IF (Pente(K_Can) > 0) AND (Pente(K_Can+1) > 0) THEN
                     IF (Pente(K_Can) > Pente(K_Can+1)) THEN
                       BEGIN
                         Marquage_Pic := True;
                       END;

                      { Si point d'inflexion pente descendante }
                   IF (Pente(K_Can) < 0) AND (Pente(K_Can+1) < 0) THEN
                     IF (Abs(Pente(K_Can)) < Abs(Pente(K_Can+1))) THEN
                       BEGIN
                         Marquage_Pic := True;
                       END;
                   IF Marquage_Pic THEN
                   BEGIN

                   { Marquage d'un point d'inflexion s'il n'en existe pas d‚j…
                    un sur ce cot‚ du pic .
                    Pas de marquage si on est dans la vall‚e entre deux pics}

                     IF NOT(Inflexion) AND NOT(Can_Sommet) THEN
                       IF NOT((Pente(K_Can - Nc_Deriv) < 0) AND (Pente(K_Can) > 0)
                       OR (Pente(K_Can - 1 - Nc_Deriv) < 0) AND (Pente(K_Can-1) > 0)
                       OR (Pente(K_Can + 1 - Nc_Deriv) < 0) AND (Pente(K_Can+1) > 0)) THEN
                       BEGIN
                       { Si pic sommet < 2 fois la racine carr‚e du BdF , pas de marquage }
                         IF (FNcanal(K_Can + Nc_Deriv DIV 2,2,0) -
                          (K_Can + Nc_Deriv DIV 2)*A1 - B1) >
                          (2*Trunc(Sqrt( FNcanal(K_Can + Nc_Deriv DIV 2,2,0)))) THEN
                          BEGIN
                            Contenu_Canal[K_Can + Nc_Deriv DIV 2] := FNcanal(K_Can+ Nc_Deriv DIV 2,3,1);
                            Inflexion := True;
                          END;
                       END;

                     { Marquage d'un sommet de pic et interdiction d'avoir un
                     canal marqu‚ sur 2/3 r‚solution de chaque cot‚ du pic }

                     IF Can_Sommet THEN
                     BEGIN
                       IF( K_Can < (Id + Nc_Deriv DIV 2 -1 )) THEN EXIT; { si sommet trop prŠs du d‚but de zone, on ‚limine }
                       IF( K_Can > (Fi - Nc_Deriv DIV 2 +1 )) THEN EXIT; { si sommet trop prŠs de la fin de zone, on ‚limine }
                       Energie := Energy(K_Can+(Nc_Deriv DIV 2));
                       Demi_Res_Cx := ROUND(Resolution(Energie)/(Coef_B_Cal_Ener*1.5));
                       
                       FOR K := 1 TO Demi_Res_Cx DO 
                       IF((FNcanal(K_Can+(Nc_Deriv DIV 2)-K,1,1) AND 2) =2) THEN
                         Contenu_Canal[K_Can+(Nc_Deriv DIV 2)-K] := FNcanal(K_Can+(Nc_Deriv DIV 2)-K,4,1);

                       { Si pic sommet < 2 fois la racine carr‚e du BdF , pas de marquage }
                         IF (FNcanal(K_Can + Nc_Deriv DIV 2,2,0) -
                          (K_Can + Nc_Deriv DIV 2)*A1 - B1) >
                          (2*Trunc(Sqrt( FNcanal(K_Can + Nc_Deriv DIV 2,2,0)))) THEN
                          BEGIN
                            Contenu_Canal[K_Can+ Nc_Deriv DIV 2] := FNcanal(K_Can+ Nc_Deriv DIV 2,3,1);
                            Inflexion := False;
                            Can_Sommet := False;
                            I_Saut := K_Can + Demi_Res_Cx;
                          END;
                     END;
                     Marquage_Pic := False;
                   END;
                 END;
               END;
          FlZdeb := False;
          FlZfin := False;
          END;
     END;
     FlZdeb := False;
     FlZfin := False;
END;

    { Int‚gration d'une zone }

PROCEDURE Int_Zone ( Mode : Integer);
VAR
   Sum    : REAL;
   I, S   : INTEGER;
BEGIN
     Sum := 0;
     FOR I := Id TO Fi DO
              Sum := Sum + FNcanal(I,2,0);
     S := Fi - Id + 1;
     CASE Mode OF
          0 :
            BEGIN
            Penr.Bgnd:=FNcanal(Id,2,0)+FNcanal(Id+1,2,0)+FNcanal(Id-1,2,0);
            Penr.Bgnd := Penr.Bgnd + FNcanal(Fi,2,0)+FNcanal(Fi+1,2,0)+FNcanal(Fi-1,2,0);
            Penr.Bgnd := (Penr.Bgnd/6)*S;
            END;
          1 :
            Penr.Bgnd := (Y1+Y2)*S/2;
     END;
     Penr.Area := Sum - Penr.Bgnd;
END;

    { Fonction pour d‚terminer le canal sommet exact }

FUNCTION FNcanexact ( Fm : Real) : REAL;
VAR
   Ap, Aq : REAL;
   I      : INTEGER;
BEGIN
     Aq := 0;
     I := Id -1;
     WHILE Aq < Penr.Area*Fm DO
     BEGIN
          Inc(I);
          Aq := Aq + FNcanal(I,2,0) - (A1*I+B1);
     END;
     Ap := Aq - ( FNcanal(I,2,0) - (A1*I+B1));
     FNcanexact := (I-1) + (Penr.Area*Fm - Ap)/(Aq - Ap) + 0.5;
END;

    { D‚termination de l'abscisse exacte et de la r‚solution d'un pic }

PROCEDURE Res_Absi_Pic ( Mode : Integer );
BEGIN
     IF Mode = 0 THEN
     BEGIN
                { D‚termination de la pente du bruit de fond }
          Y1 := (FNcanal(Id-1,2,0) + FNcanal(Id,2,0) + FNcanal(Id+1,2,0))/3;
          Y2 := (FNcanal(Fi-1,2,0) + FNcanal(Fi,2,0) + FNcanal(Fi+1,2,0))/3;
     END;
     A1 := (Y1-Y2)/(Id-Fi);
     B1 := Y1 - A1*Id;
     Int_Zone ( Mode );
     Penr.Abscisse := FNcanexact( 0.5 );
     Penr.Fwhm := (FNcanexact( 0.75 ) - FNcanexact( 0.25 ))*Coef_B_Cal_Ener*1.74;
END;

    { Impression des r‚sultats }

PROCEDURE Imp_Res;
BEGIN
     Inc(Penr.N_P);
     Penr.Left := Id;
     Penr.Pw   := Fi - Id + 1;
     Penr.Ener :=(Penr.Abscisse*(Penr.Abscisse*Coef_A_Cal_Ener+Coef_B_Cal_Ener)+Coef_C_Cal_Ener);
     Penr.CtsSec := Penr.Area/Temps_Actif_ecoule;
     Penr.Eff  := Eff_Ener(Penr.Ener);
     IF Penr.Area > 0  THEN
       Write(EnrPic,Penr)
     ELSE
       Dec(Penr.N_P);
END;

    { Traitement des pics simples }

PROCEDURE Trai_Pic_Simple;
BEGIN
     Int_Zone (1);
     IF Penr.Area < 1 THEN Exit;
     Penr.Erreur := SQRT(Penr.Bgnd*2 + Penr.Area)*100*Nb_Sigma/Penr.Area;
     Res_Absi_Pic(1);
     Penr.It := 0;
     Penr.Fit := 0;
     Imp_Res;
END;

    { Proc‚dure d'invertion de matrice }

PROCEDURE InvMd ( N : Integer);
VAR
   AB, BB : Array[1..30,1..60] of EXTENDED;
   I, J, K, Ideb, Ifin   : INTEGER;
BEGIN
     FOR I := 1 TO N DO
     BEGIN
          FOR J := 1 TO N DO AB[I,J] := Ainv^[I,J];
     END;
     Ideb := N + 1;
     Ifin := N*2;
     FOR I := 1 TO N DO
     BEGIN
          FOR J := Ideb TO Ifin DO AB[I,J] := 0;
     END;
     FOR I := 1 TO N DO
     BEGIN
          J := I + N;
          AB[I,J] := 1;
     END;
     FOR K := 1 TO N DO
     BEGIN
          FOR J := 1 TO Ifin DO BB[K,J] := AB[K,J]/AB[K,K];
          FOR I := 1 TO N DO
          BEGIN
               IF I <> K THEN
               BEGIN
                    FOR J := 1 TO Ifin DO BB[I,J] := AB[I,J] - AB[I,K]*BB[K,J];
               END;
          END;
          FOR I := 1 TO N DO
          BEGIN
               FOR J := 1 TO Ifin DO AB[I,J] := BB[I,J];
          END;
     END;
     FOR I := 1 TO N DO
     BEGIN
          FOR J := 1 TO N DO
          BEGIN
               K := J + N;
               Ainv^[I,J] := AB[I,K];
          END;
     END;
END;

    { Proc‚dure de d‚convolution des multiplets }

PROCEDURE Multiplet;
TYPE
    Pmat1 = ^Tmat1;
    Tmat1 = Array[1..200,1..30] of REAL;
    Pmat2 = ^Tmat2;
    Tmat2 = Array[1..30,1..200] of REAL;
VAR
   Absi, Dlmh, Alp, Azo, OldAbsi, OldAlp, Sur, Sigm : Array[1..10] of REAL;
   C, B, W, Yt, Res                                 : Array[1..200] of REAL;
   V, T                                             : Array[1..30] of REAL;
   A               : Pmat1;
   Yg              : Pmat2;
   Nc, Np, Jv, I, J, K, L, Nx, Sortie, Jtest, Xndl : INTEGER;
   Ener, Yzot, CalInt, Yzo, Dif1, Dif2, Dif3, Socare : REAL;
   Vazo, Valp, Decal : REAL;
BEGIN
     New(A);
     New(Yg);
        { D‚termination du nb. de pics et du nb. de canaux de la zone }
     Nc := 0;
     Np := 0;
     Jv := 3;
     FOR J := Id TO Fi DO
     BEGIN
          Inc(Nc);
          IF(( FNcanal(J,1,1) AND 2) = 2) THEN
          BEGIN
               Inc(Np);
               Absi[Np] := J;
               OldAbsi[Np] := Absi[Np];
               Ener := Energy(J);
               Dlmh[Np] := Resolution(Ener)/(Coef_B_Cal_Ener*2);
               Alp[Np] := 0.69315/SQR(Dlmh[Np]);
               OldAlp[Np] := Alp[Np];
               Azo[Np] := FNcanal(J,2,0) -(J*A1+B1);
          END;
     END;
     Nx := Jv*Np;
     Penr.It := 0;
     Sortie := 0;
     Jtest := 0;
           { D‚but de la boucle de convergence }
     WHILE (Jtest <> Np) AND (Penr.It < 20 ) DO
     BEGIN
                { Formation des matrices A,B et W }
          L := 0;
          FOR I := Id TO Fi DO
          BEGIN
               Inc(L);
               C[L] := FNcanal(I,2,0) - (I*A1+B1);
               IF C[L] <= 1 THEN C[L] := 1;
               W[L] := 1/C[L];
               Yzot := 0;
               FOR J := 1 TO Np DO
               BEGIN
                    CalInt := -Alp[J]*SQR(I-Absi[J]);
                    IF CalInt < -81 THEN Yzo := 0 ELSE Yzo := Azo[J]*EXP(CalInt);
                    Yzot := Yzot + Yzo;
                    B[L] := C[L] - Yzot;
                    K := 1 + Jv*(J-1);
                    A^[L,K] := Yzo/Azo[J];
                    A^[L,K+1] := 2*Yzo*Alp[J]*(I-Absi[J]);
                    IF Jv = 3 THEN A^[L,K+2] := -Yzo*SQR(I-Absi[J]);
               END;
          END;
              { Formation de la matrice Ainv }
          FOR J := 1 TO Nx DO
          BEGIN
               FOR K := 1 TO Nx DO
               BEGIN
                    Ainv^[J,K] := 0;
                    FOR I := 1 TO Nc DO Ainv^[J,K] := Ainv^[J,K] + A^[I,J]*W[I]*A^[I,K];
               END;
          END;
              { Inversion de la matrice }
          InvMd( Nx );
              { Formation de la matrice V }
          FOR J := 1 TO Nx DO
          BEGIN
               V[J] := 0;
               FOR I := 1 TO Nc DO V[J] := V[J] + A^[I,J]*W[I]*B[I];
          END;
              { Solution }
          FOR I := 1 TO Nx DO
          BEGIN
               T[I] := 0;
               FOR J := 1 TO Nx DO T[I] := T[I] + Ainv^[I,J]*V[J];
          END;
              { Test de convergence }
          Jtest := 0;
          FOR J := 1 TO Np DO
          BEGIN
               Dif3 := 0;
               K := 1 + Jv*(J-1);
               Azo[J] := Azo[J] + T[K];
               IF Azo[J] > 0 THEN Dif1 := ABS(T[K]/Azo[J]) ELSE Inc(Sortie);
               Absi[J] := Absi[J] + T[K+1];
               IF (Absi[J] < (Id+2)) OR (Absi[J] > (Fi-2)) THEN
               BEGIN
                 Absi[J] := OldAbsi[J];
                 Alp[J] := OldAlp[J];
               END;
               IF Absi[J] > 0 THEN Dif2 := ABS(T[K+1]/Absi[J]) ELSE Inc(Sortie);
               IF Jv = 3 THEN
               BEGIN
                    Alp[J] := Alp[J] + T[K+2];
                    IF Alp[J] > 0 THEN Dif3 := ABS(T[K+2]/Alp[J]) ELSE Inc(Sortie);
               END;
               IF Sortie = 0 THEN
               BEGIN
                    IF (Dif1 < 0.01) AND (Dif2 < 0.01) AND (Dif3 < 0.01) THEN Inc(Jtest);
                    IF ((Jv = 3) AND (Penr.It > 1) AND (Dif1 > 0.5)) THEN Inc(Sortie);
                    IF ((Jv = 3) AND (Penr.It > 1) AND (Dif2 > 0.5)) THEN Inc(Sortie);
                    IF ((Jv = 3) AND (Penr.It > 1) AND (Dif3 > 0.5)) THEN Inc(Sortie);
                    IF ((Jv = 3) AND (Penr.It < 2) AND (Dif1 > 10)) THEN Inc(Sortie);
                    IF ((Jv = 3) AND (Penr.It < 2) AND (Dif2 > 10)) THEN Inc(Sortie);
                    IF ((Jv = 3) AND (Penr.It < 2) AND (Dif3 > 10)) THEN Inc(Sortie);
               END;
          END;
          Inc(Penr.It);

              { Si non convergence, on impose la r‚solution }

          IF ((Jv = 3) AND (Penr.It < 21) AND (Sortie > 0)) THEN
          
          BEGIN
               FOR J := 1 TO Np DO
               BEGIN
                    Absi[J] := OldAbsi[J];
                    Alp[J] := OldAlp[J];
                    Azo[J] := FNcanal(TRUNC(Absi[J]),2,0) - (Absi[J]*A1+B1);
               END;
               Sortie := 0;
               Jv := 2;
               Nx := Jv*Np;
               Penr.It := 0;
          END;
     END;
     IF Sortie = 0 THEN
         { Calcul statistique et sortie correcte }
     BEGIN
          Socare := 0;
          Penr.Fit := 0;
          FOR I := 1 TO Nc DO
          BEGIN
               Res[I] := 0;
               Yt[I] := 0;
               FOR J := 1 TO Np DO Yg^[J,I] := 0;
          END;
          I := 0;
          FOR K := Id TO Fi DO
          BEGIN
               Inc(I);
               FOR J := 1 TO Np DO
               BEGIN
                    Yg^[J,I] := Azo[J]*EXP(-Alp[J]*SQR(K-Absi[J]));
                    Yt[I] := Yt[I] + Yg^[J,I];
               END;
               Res[I] := FNcanal(K,2,0) - (K*A1+B1) - Yt[I];
               Socare := Socare + Res[I]*Res[I]*W[I];
               IF FNcanal(K,2,0) <> 0 THEN Res[I] := Res[I]*Res[I]/FNcanal(K,2,0);
               Penr.Fit := Penr.Fit + Res[I];
          END;
          Xndl := Nc - Nx;
          Penr.Fit := Penr.Fit/Xndl;
          FOR J := 1 TO Np DO
          BEGIN
               Sur[J] := 1.773*Azo[J]/SQRT(Alp[J]);
               K := 1 + Jv*(J-1);
               Vazo := Socare*Ainv^[K,K]/Xndl;
               Valp := Socare*Ainv^[K+1,K+1]/Xndl;
               Sigm[J] := SQR(Azo[J])/Alp[J]*(Vazo/SQR(Azo[J]) + 0.25*Valp/SQR(Alp[J]));
               Sigm[J] := ABS(Sigm[J]);
               Sigm[J] := SQRT(Sigm[J])*200/Sur[J];
               Penr.Fwhm := 2*Coef_B_Cal_Ener*SQRT(0.69315/Alp[J]);
               Decal := Penr.Fwhm*1.5/Coef_B_Cal_Ener;
               Penr.Bgnd := (((Absi[J]-Decal)*A1+B1)+((Absi[J]+Decal)*A1+B1))*Decal;
               Penr.Abscisse := Absi[J];
               Penr.Area := Sur[J];
               Penr.Erreur := Nb_Sigma*100*SQRT(2*Penr.Bgnd+Sur[J])/Sur[J];
               Jimp := J;
               Imp_Res;
          END;
     END
     ELSE
         BEGIN
           Trai_Pic_Simple
          { Writeln(Gf,'Echec de la d‚convolution du multiplet aux ‚nergies');
           FOR J := 1 TO Np DO
           BEGIN
             Ener :=(OldAbsi[J]*(J*Coef_A_Cal_Ener+Coef_B_Cal_Ener)+Coef_C_Cal_Ener);
             Writeln(Gf,Ener:6:2);
           END;
           Writeln(Gf,'  Canal  Contenu');
           FOR I := 1 TO Nc DO Writeln(Gf,(Id+I-1):6,C[I]:9:0); }
         END;
     Dispose(A);
     Dispose(Yg);
END;

PROCEDURE Trai_Pics;
VAR
   Flag : BOOLEAN;
   Sum, Cont_Vallee, C_Max : LONGINT;
   Nb_Sommets, N_Pic, K, J, I_Vallee, No_Pic : INTEGER;
   Ecart, Rac_Som1, Rac_Som2, Old_Y2 : REAL;
   I_Sommet : Array[1..30] of INTEGER;
BEGIN
     Flag := False;
     Penr.N_P := 0;
     Sum := 0;
     C_Max := 0;
     Nb_Sommets := 0;
     No_Pic := 0;
     FOR IL := I_Debut TO I_Fin DO
     BEGIN
          IF ((FNcanal(Il,1,0) AND 1) = 0 ) THEN
          WHILE Flag DO
          BEGIN
               { D‚termination de la pente de bruit de fond }
               Fi := Il - 1;
               Y1 :=(FNcanal((Id-1),2,0)+FNcanal(Id,2,0)+FNcanal((Id+1),2,0))/3;
               Y2 :=(FNcanal((Fi-1),2,0)+FNcanal(Fi,2,0)+FNcanal((Fi+1),2,0))/3;
               Old_Y2 := Y2;
               A1 := (Y1-Y2)/(Id-Fi);
               B1 := Y1 - A1*Id;
               Old_Fi := Fi;
               IF Nb_Sommets <= 1 THEN
                    Trai_Pic_Simple
               ELSE
               BEGIN
                    N_Pic := 1;
                    FOR K := 1 TO (Nb_Sommets-1) DO
                    BEGIN
                         Cont_Vallee := 1677216; { 2^24 }
                         FOR J := I_Sommet[K] TO I_Sommet[K+1] DO
                         BEGIN
                              IF FNcanal(J,2,0) < Cont_Vallee THEN
                              BEGIN
                                   Cont_Vallee := FNcanal(J,2,0);
                                   I_Vallee := J;
                              END;
                         END;
                         Ecart := Cont_Vallee - (I_Vallee*A1+B1);

               { Si la vall‚e entre deux pics redescend suffisament, on r‚duit la zone pic }

                         IF (FNcanal(I_Sommet[K],2,0)-(I_Sommet[K]*A1+B1)) > 0 THEN
                           Rac_Som1 :=SQRT(FNcanal(I_Sommet[K],2,0)-(I_Sommet[K]*A1+B1))
                         ELSE
                           Rac_Som1 := 0;
                         IF (FNcanal(I_Sommet[K+1],2,0)-(I_Sommet[K+1]*A1+B1)) > 0 THEN
                           Rac_Som2 :=SQRT(FNcanal(I_Sommet[K+1],2,0)-(I_Sommet[K+1]*A1+B1))
                         ELSE
                           Rac_Som2 := 0;

                         IF ((Ecart < Rac_Som1) AND (Ecart < Rac_Som2))

              { Idem si l'‚cart entre deux sommets de pic est sup‚rieur … trois r‚solutions }

                          OR ((Energy(I_Sommet[K+1]) - Energy(I_Sommet[K]))
                           > Resolution(Energy(I_Vallee))*3) THEN
                         BEGIN
                              Y1 := Id*A1+B1;
                              Y2 := Cont_Vallee;
                              IF (Cont_Vallee - (I_Vallee*A1+B1) < 0) THEN
                              BEGIN
                                   A1 := (Y1 -Y2)/(Id -I_Vallee);
                                   B1 := Y1 - A1*Id;
                              END;
                              Fi := I_Vallee;
                              IF N_Pic > 1 THEN
                                   Multiplet
                              ELSE
                                   Trai_Pic_Simple;
                              N_Pic := 1;
                              Id := Fi;
                              Fi := Old_Fi;
                              Y1 := Cont_Vallee;
                              Y2 := Old_Y2;
                              A1 := (Y1-Y2)/(Id-Fi);
                              B1 := Y1 - A1*Id;
                         END
                         ELSE
                              Inc(N_Pic);
                    END;
                    Fi := Old_Fi;
                    Y1 := Id*A1 + B1;
                    Y2 := Old_Y2;
                    A1 := (Y1-Y2)/(Id-Fi);
                    B1 := Y1 - A1*Id;
                    IF N_Pic > 1  THEN
                         Multiplet
                    ELSE
                         Trai_Pic_Simple;
               END;
               Flag := False;
               Sum := 0;
               C_Max := 0;
               Nb_Sommets := 0;
          END
          ELSE IF ((FNcanal(Il,1,0) AND 1) = 1 ) THEN
          BEGIN
               IF NOT(Flag) THEN Id := IL;
               Flag := True;
               Sum := Sum + FNcanal(Il,2,0);
               IF ((FNcanal(Il,1,1) AND 2) = 2) THEN
               BEGIN
                    Inc(Nb_Sommets);
                    I_Sommet[Nb_Sommets] := Il;
               END;
               IF (FNcanal(Il,2,0) > C_Max) THEN C_Max := FNcanal(Il,2,0);
          END;
     END;
END;
BEGIN
     New (Ainv);
     GetDir(3,Rep);
     Assign(Adr,Rep +'\genrl.fil');
     Reset(Adr);
     REPEAT
           Read(Adr,Enr);
           CASE Enr.I of
                1  : { Attribution du nom du fichier r‚sultat }
                BEGIN
                     Assign(EnrPic,Enr.Fichier);
                     Rewrite(EnrPic);
                END;
                { Lecture du nom du fichier spectre … traiter }
                10 :
                BEGIN
                     Assign(Gf,Enr.Fichier);
                     Append(Gf);
                END;
                11 : LecSpe(Enr.Fichier);
                { Lecture du nom de fichier efficacit‚ }
                12 : Lec_Eff(Enr.Fichier);
           END;
     UNTIL Eof(Adr);
     Close(Adr);
     Rech_Pics_Auto ;
     Trai_Pics;
     Close(EnrPic);
     Close(Gf);
     Dispose(Ainv);
END.



