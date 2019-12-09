/*==============================================================*/
/* Nom de SGBD :  MySQL 5.0                                     */
/* Date de création :  09/12/2019 11:25:40                      */
/*==============================================================*/


drop table if exists CAPTEUR;

drop table if exists MESURE;

drop table if exists SONDE;

drop table if exists UTILISATEUR;

/*==============================================================*/
/* Table : CAPTEUR                                              */
/*==============================================================*/
create table CAPTEUR
(
   ID_CAPTEUR           int not null auto_increment,
   ID_SONDE             int not null,
   CAPTEUR_MESURE       longtext,
   CAPTEUR_VALEUR       float,
   primary key (ID_CAPTEUR)
);

/*==============================================================*/
/* Table : MESURE                                               */
/*==============================================================*/
create table MESURE
(
   ID_MESURE            int not null auto_increment,
   ID_CAPTEUR           int not null,
   MESURE_DATE          datetime,
   MESURE_TEMP          float,
   MESURE_HUMIDITE      float,
   primary key (ID_MESURE)
);

/*==============================================================*/
/* Table : SONDE                                                */
/*==============================================================*/
create table SONDE
(
   ID_SONDE             int not null auto_increment,
   ID_UTILISATEUR       int not null,
   SONDE_POS_LATITUDE   double,
   SONDE_POS_LONGITUDE  double,
   SONDE_NOM            varchar(40),
   primary key (ID_SONDE)
);

/*==============================================================*/
/* Table : UTILISATEUR                                          */
/*==============================================================*/
create table UTILISATEUR
(
   ID_UTILISATEUR       int not null auto_increment,
   UTILISATEUR_PSEUDO   varchar(40),
   UTILISATEUR_EMAIL    varchar(40),
   UTILISATEUR_MDP      longtext,
   primary key (ID_UTILISATEUR)
);

alter table CAPTEUR add constraint FK_AVOIR foreign key (ID_SONDE)
      references SONDE (ID_SONDE) on delete restrict on update restrict;

alter table MESURE add constraint FK_REALISER foreign key (ID_CAPTEUR)
      references CAPTEUR (ID_CAPTEUR) on delete restrict on update restrict;

alter table SONDE add constraint FK_ASSOCIATION_3 foreign key (ID_UTILISATEUR)
      references UTILISATEUR (ID_UTILISATEUR) on delete restrict on update restrict;

