CREATE SCHEMA IF NOT EXISTS "public";

CREATE  TABLE "public".attribute ( 
	attribute_id         integer  NOT NULL  ,
	name                 varchar(50)  NOT NULL  ,
	CONSTRAINT pk_attribute PRIMARY KEY ( attribute_id )
 );

CREATE  TABLE "public".champion ( 
	champion_id          integer  NOT NULL  ,
	title                varchar    ,
	release_date         date    ,
	price_be             integer    ,
	price_rp             integer    ,
	resource             varchar    ,
	health               integer    ,
	hp_lvl               integer    ,
	hp_display           integer    ,
	hp_lvl_display       integer    ,
	hp_regen             integer    ,
	hp_regen_lvl         integer    ,
	mana                 integer    ,
	mana_lvl             integer    ,
	mana_regen_lvl       integer    ,
	energy               integer    ,
	energy_regen         integer    ,
	move_speed           integer    ,
	attack_damage        integer    ,
	ad_lvl               integer    ,
	attack_speed         integer    ,
	as_lvl               integer    ,
	attack_range         integer    ,
	armor                integer    ,
	armor_lvl            integer    ,
	magic_resist         integer    ,
	magic_resist_lvl     integer    ,
	pronoun              varchar    ,
	key_integer          integer    ,
	overview_page        varchar    ,
	CONSTRAINT unq_champion_champion_id UNIQUE ( champion_id ) ,
	CONSTRAINT pk_champion PRIMARY KEY ( champion_id )
 );

CREATE  TABLE "public".champion_attributes ( 
	champion_id          integer  NOT NULL  ,
	attribute_id         integer    ,
	CONSTRAINT fk_attribute FOREIGN KEY ( attribute_id ) REFERENCES "public".attribute( attribute_id )   ,
	CONSTRAINT fk_champion_attributes FOREIGN KEY ( champion_id ) REFERENCES "public".champion( champion_id )   
 );

CREATE  TABLE "public".socials ( 
 );

CREATE  TABLE "public".team ( 
	team_id              integer  NOT NULL  ,
	name                 varchar    ,
	short_name           varchar(10)    ,
	location             varchar    ,
	region               varchar    ,
	roster_photo         varchar    ,
	is_disbanded         boolean    ,
	image                varchar    ,
	overview_page        varchar    ,
	CONSTRAINT pk_team PRIMARY KEY ( team_id )
 );

CREATE  TABLE "public".team_socials ( 
	team_id              integer  NOT NULL  ,
	social_name          varchar  NOT NULL  ,
	social_link          varchar    ,
	CONSTRAINT fk_team_socials_team FOREIGN KEY ( team_id ) REFERENCES "public".team( team_id )   
 );

CREATE  TABLE "public".player ( 
	player_id            integer  NOT NULL  ,
	overview_page        varchar    ,
	username             varchar    ,
	real_name            varchar    ,
	full_name            varchar    ,
	image                varchar    ,
	country              varchar    ,
	age                  integer    ,
	birthdate            date    ,
	residency            varchar    ,
	"role"               varchar    ,
	contract_end         date    ,
	is_retired           boolean DEFAULT 0   ,
	is_substitute        boolean DEFAULT 0   ,
	team_id              integer    ,
	CONSTRAINT pk_player PRIMARY KEY ( player_id ),
	CONSTRAINT fk_player_team FOREIGN KEY ( team_id ) REFERENCES "public".team( team_id )   
 );

CREATE  TABLE "public".favorite_champions ( 
	player_id            integer  NOT NULL  ,
	champion_id          integer  NOT NULL  ,
	CONSTRAINT fk_favorite_champions_champion FOREIGN KEY ( champion_id ) REFERENCES "public".champion( champion_id )   ,
	CONSTRAINT fk_favorite_champions_player FOREIGN KEY ( player_id ) REFERENCES "public".player( player_id )   
 );

COMMENT ON COLUMN "public".team.region IS 'fk';

