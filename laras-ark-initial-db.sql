PGDMP                          z            IE172-database    14.2    14.2 I    y           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            z           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            {           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            |           1262    16386    IE172-database    DATABASE     e   CREATE DATABASE "IE172-database" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';
     DROP DATABASE "IE172-database";
                postgres    false            ?            1259    16387    administrator    TABLE     ?  CREATE TABLE public.administrator (
    admin_n integer NOT NULL,
    admin_pass character varying(25) NOT NULL,
    admin_m character varying(250) NOT NULL,
    admin_a integer NOT NULL,
    admin_s character varying(1) NOT NULL,
    admin_l character varying(250) NOT NULL,
    admin_no character varying(11) NOT NULL,
    admin_del_ind boolean,
    shelter_n integer,
    CONSTRAINT admin_no CHECK (((admin_no)::text ~ similar_escape('[0-9]{11}'::text, NULL::text))),
    CONSTRAINT administrator_admin_a_check CHECK (((admin_a >= 0) AND (admin_a <= 100))),
    CONSTRAINT administrator_admin_s_check CHECK (((admin_s)::text = ANY (ARRAY[('M'::character varying)::text, ('F'::character varying)::text])))
);
 !   DROP TABLE public.administrator;
       public         heap    postgres    false            ?            1259    16395    administrator_admin_n_seq    SEQUENCE     ?   CREATE SEQUENCE public.administrator_admin_n_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.administrator_admin_n_seq;
       public          postgres    false    209            }           0    0    administrator_admin_n_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.administrator_admin_n_seq OWNED BY public.administrator.admin_n;
          public          postgres    false    210            ?            1259    16396    adopter    TABLE     ?  CREATE TABLE public.adopter (
    adopter_n integer NOT NULL,
    adopter_m character varying(250) NOT NULL,
    adopter_s character varying(1) NOT NULL,
    adopter_no character varying(11) NOT NULL,
    adopter_l character varying(250) NOT NULL,
    adopter_del_ind boolean NOT NULL,
    adopter_a integer,
    adopter_transid integer NOT NULL,
    adopter_occ character varying(250),
    adopter_date_entr date,
    CONSTRAINT adopter_adopter_a_check CHECK ((adopter_a >= 5)),
    CONSTRAINT adopter_adopter_no_check CHECK (((adopter_no)::text !~~ '%[^0-9]%'::text)),
    CONSTRAINT adopter_adopter_s_check CHECK (((adopter_s)::text = ANY (ARRAY[('M'::character varying)::text, ('F'::character varying)::text])))
);
    DROP TABLE public.adopter;
       public         heap    postgres    false            ?            1259    16404    adoption    TABLE     ?  CREATE TABLE public.adoption (
    adopt_order_n integer NOT NULL,
    adopt_order_c numeric(6,2),
    adopt_order_r character varying(1),
    adopt_order_del_ind boolean NOT NULL,
    adopter_n integer,
    shelter_n integer NOT NULL,
    adopt_order_inq_n integer NOT NULL,
    pet_n integer NOT NULL,
    adopt_order_trans_date date,
    CONSTRAINT adopt_order_r CHECK (((adopt_order_r)::text = ANY (ARRAY[('Y'::character varying)::text, ('P'::character varying)::text, ('F'::character varying)::text])))
);
    DROP TABLE public.adoption;
       public         heap    postgres    false            ?            1259    16408    adoptioninquiry    TABLE     ?   CREATE TABLE public.adoptioninquiry (
    adopt_order_inq_n integer NOT NULL,
    adopt_order_inq_a integer,
    adopt_order_inq_b text,
    adopt_order_inq_c text,
    adopt_order_inq_d text,
    adopt_order_inq_e text
);
 #   DROP TABLE public.adoptioninquiry;
       public         heap    postgres    false            ?            1259    16413    event    TABLE     ?  CREATE TABLE public.event (
    event_n integer NOT NULL,
    admin_n integer NOT NULL,
    event_del_ind boolean NOT NULL,
    event_m character varying(250) NOT NULL,
    event_r character varying(250),
    event_type_n integer NOT NULL,
    CONSTRAINT event_event_r_check CHECK (((event_r)::text = ANY (ARRAY[('Success'::character varying)::text, ('Pending'::character varying)::text, ('Postponed'::character varying)::text, ('Cancelled'::character varying)::text])))
);
    DROP TABLE public.event;
       public         heap    postgres    false            ?            1259    16419    event_admin_n_seq    SEQUENCE     ?   CREATE SEQUENCE public.event_admin_n_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.event_admin_n_seq;
       public          postgres    false    214            ~           0    0    event_admin_n_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.event_admin_n_seq OWNED BY public.event.admin_n;
          public          postgres    false    215            ?            1259    16420    eventcheckup    TABLE     ?   CREATE TABLE public.eventcheckup (
    check_up_n integer NOT NULL,
    event_n integer NOT NULL,
    vet_n integer NOT NULL,
    pet_n integer NOT NULL,
    check_up_del_ind boolean NOT NULL
);
     DROP TABLE public.eventcheckup;
       public         heap    postgres    false            ?            1259    16423    eventinterview    TABLE     ?   CREATE TABLE public.eventinterview (
    interview_n integer NOT NULL,
    event_n integer NOT NULL,
    adopter_n integer NOT NULL,
    interview_del_ind boolean NOT NULL
);
 "   DROP TABLE public.eventinterview;
       public         heap    postgres    false            ?            1259    16426    eventsituationer    TABLE     ?   CREATE TABLE public.eventsituationer (
    situationer_n integer NOT NULL,
    event_n integer NOT NULL,
    situationer_anml_rsc integer NOT NULL,
    situationer_l character varying(250) NOT NULL,
    situationer_del_ind boolean NOT NULL
);
 $   DROP TABLE public.eventsituationer;
       public         heap    postgres    false            ?            1259    16429 	   eventtype    TABLE     t   CREATE TABLE public.eventtype (
    event_type_n integer NOT NULL,
    event_type character varying(80) NOT NULL
);
    DROP TABLE public.eventtype;
       public         heap    postgres    false            ?            1259    16432    medicine    TABLE     ?  CREATE TABLE public.medicine (
    med_n integer NOT NULL,
    med_cn integer NOT NULL,
    med_type character varying(250) NOT NULL,
    med_del_ind boolean NOT NULL,
    med_m character varying(250) NOT NULL,
    med_c numeric(11,2),
    med_tc numeric,
    shelter_n integer,
    med_date_entr date NOT NULL,
    CONSTRAINT medicine_check CHECK ((med_tc = ((med_cn)::numeric * med_c)))
);
    DROP TABLE public.medicine;
       public         heap    postgres    false            ?            1259    16438    pet    TABLE     |  CREATE TABLE public.pet (
    pet_n integer NOT NULL,
    pet_m character varying(250) NOT NULL,
    pet_b character varying(250) NOT NULL,
    pet_s character varying(1) NOT NULL,
    pet_rs text NOT NULL,
    pet_rd date NOT NULL,
    pet_a real,
    pet_mr text,
    pet_delete_ind boolean,
    shelter_n integer,
    pet_date_entr date NOT NULL,
    pet_adpt_stat boolean NOT NULL,
    CONSTRAINT pet_pet_a_check CHECK (((pet_a >= (0)::double precision) AND (pet_a <= (100)::double precision))),
    CONSTRAINT pet_pet_s_check CHECK (((pet_s)::text = ANY (ARRAY[('M'::character varying)::text, ('F'::character varying)::text])))
);
    DROP TABLE public.pet;
       public         heap    postgres    false            ?            1259    16445    schedule    TABLE     ?   CREATE TABLE public.schedule (
    schedule_n integer NOT NULL,
    event_n integer NOT NULL,
    schedule_d date NOT NULL,
    schedule_del_ind boolean NOT NULL
);
    DROP TABLE public.schedule;
       public         heap    postgres    false            ?            1259    16448    shelter    TABLE     ?   CREATE TABLE public.shelter (
    shelter_n integer NOT NULL,
    shelter_br character varying(250) NOT NULL,
    shelter_l character varying(250) NOT NULL
);
    DROP TABLE public.shelter;
       public         heap    postgres    false            ?            1259    16453    veterinarian    TABLE     ?  CREATE TABLE public.veterinarian (
    vet_n integer NOT NULL,
    vet_m character varying(250) NOT NULL,
    vet_a integer NOT NULL,
    vet_no character varying(11) NOT NULL,
    vet_s character varying(1) NOT NULL,
    vet_l character varying(250) NOT NULL,
    vet_del_ind boolean,
    shelter_n integer,
    vet_sal real,
    vet_spec character varying(250) NOT NULL,
    vet_date_entr date,
    CONSTRAINT veterinarian_vet_a_check CHECK (((vet_a >= 0) AND (vet_a <= 100))),
    CONSTRAINT veterinarian_vet_no_check CHECK (((vet_no)::text !~~ '%[0-9]%'::text)),
    CONSTRAINT veterinarian_vet_s_check CHECK (((vet_s)::text = ANY (ARRAY[('M'::character varying)::text, ('F'::character varying)::text])))
);
     DROP TABLE public.veterinarian;
       public         heap    postgres    false            ?           2604    16461    administrator admin_n    DEFAULT     ~   ALTER TABLE ONLY public.administrator ALTER COLUMN admin_n SET DEFAULT nextval('public.administrator_admin_n_seq'::regclass);
 D   ALTER TABLE public.administrator ALTER COLUMN admin_n DROP DEFAULT;
       public          postgres    false    210    209            ?           2604    16462    event admin_n    DEFAULT     n   ALTER TABLE ONLY public.event ALTER COLUMN admin_n SET DEFAULT nextval('public.event_admin_n_seq'::regclass);
 <   ALTER TABLE public.event ALTER COLUMN admin_n DROP DEFAULT;
       public          postgres    false    215    214            g          0    16387    administrator 
   TABLE DATA           ?   COPY public.administrator (admin_n, admin_pass, admin_m, admin_a, admin_s, admin_l, admin_no, admin_del_ind, shelter_n) FROM stdin;
    public          postgres    false    209   h       i          0    16396    adopter 
   TABLE DATA           ?   COPY public.adopter (adopter_n, adopter_m, adopter_s, adopter_no, adopter_l, adopter_del_ind, adopter_a, adopter_transid, adopter_occ, adopter_date_entr) FROM stdin;
    public          postgres    false    211   hh       j          0    16404    adoption 
   TABLE DATA           ?   COPY public.adoption (adopt_order_n, adopt_order_c, adopt_order_r, adopt_order_del_ind, adopter_n, shelter_n, adopt_order_inq_n, pet_n, adopt_order_trans_date) FROM stdin;
    public          postgres    false    212   ?m       k          0    16408    adoptioninquiry 
   TABLE DATA           ?   COPY public.adoptioninquiry (adopt_order_inq_n, adopt_order_inq_a, adopt_order_inq_b, adopt_order_inq_c, adopt_order_inq_d, adopt_order_inq_e) FROM stdin;
    public          postgres    false    213   n       l          0    16413    event 
   TABLE DATA           `   COPY public.event (event_n, admin_n, event_del_ind, event_m, event_r, event_type_n) FROM stdin;
    public          postgres    false    214   qo       n          0    16420    eventcheckup 
   TABLE DATA           [   COPY public.eventcheckup (check_up_n, event_n, vet_n, pet_n, check_up_del_ind) FROM stdin;
    public          postgres    false    216   ?o       o          0    16423    eventinterview 
   TABLE DATA           \   COPY public.eventinterview (interview_n, event_n, adopter_n, interview_del_ind) FROM stdin;
    public          postgres    false    217   p       p          0    16426    eventsituationer 
   TABLE DATA           |   COPY public.eventsituationer (situationer_n, event_n, situationer_anml_rsc, situationer_l, situationer_del_ind) FROM stdin;
    public          postgres    false    218   Mp       q          0    16429 	   eventtype 
   TABLE DATA           =   COPY public.eventtype (event_type_n, event_type) FROM stdin;
    public          postgres    false    219   ?p       r          0    16432    medicine 
   TABLE DATA           x   COPY public.medicine (med_n, med_cn, med_type, med_del_ind, med_m, med_c, med_tc, shelter_n, med_date_entr) FROM stdin;
    public          postgres    false    220   ?p       s          0    16438    pet 
   TABLE DATA           ?   COPY public.pet (pet_n, pet_m, pet_b, pet_s, pet_rs, pet_rd, pet_a, pet_mr, pet_delete_ind, shelter_n, pet_date_entr, pet_adpt_stat) FROM stdin;
    public          postgres    false    221   #r       t          0    16445    schedule 
   TABLE DATA           U   COPY public.schedule (schedule_n, event_n, schedule_d, schedule_del_ind) FROM stdin;
    public          postgres    false    222   ?v       u          0    16448    shelter 
   TABLE DATA           C   COPY public.shelter (shelter_n, shelter_br, shelter_l) FROM stdin;
    public          postgres    false    223   =w       v          0    16453    veterinarian 
   TABLE DATA           ?   COPY public.veterinarian (vet_n, vet_m, vet_a, vet_no, vet_s, vet_l, vet_del_ind, shelter_n, vet_sal, vet_spec, vet_date_entr) FROM stdin;
    public          postgres    false    224   ?w                  0    0    administrator_admin_n_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.administrator_admin_n_seq', 3, true);
          public          postgres    false    210            ?           0    0    event_admin_n_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.event_admin_n_seq', 1, false);
          public          postgres    false    215            ?           2606    16464 !   administrator admin_n_primary_key 
   CONSTRAINT     d   ALTER TABLE ONLY public.administrator
    ADD CONSTRAINT admin_n_primary_key PRIMARY KEY (admin_n);
 K   ALTER TABLE ONLY public.administrator DROP CONSTRAINT admin_n_primary_key;
       public            postgres    false    209            ?           2606    16466    administrator admin_n_unique 
   CONSTRAINT     Z   ALTER TABLE ONLY public.administrator
    ADD CONSTRAINT admin_n_unique UNIQUE (admin_n);
 F   ALTER TABLE ONLY public.administrator DROP CONSTRAINT admin_n_unique;
       public            postgres    false    209            ?           2606    16468    adopter adopter_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.adopter
    ADD CONSTRAINT adopter_pkey PRIMARY KEY (adopter_n);
 >   ALTER TABLE ONLY public.adopter DROP CONSTRAINT adopter_pkey;
       public            postgres    false    211            ?           2606    16470    adoption adoption_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.adoption
    ADD CONSTRAINT adoption_pkey PRIMARY KEY (adopt_order_n);
 @   ALTER TABLE ONLY public.adoption DROP CONSTRAINT adoption_pkey;
       public            postgres    false    212            ?           2606    16472 $   adoptioninquiry adoptioninquiry_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public.adoptioninquiry
    ADD CONSTRAINT adoptioninquiry_pkey PRIMARY KEY (adopt_order_inq_n);
 N   ALTER TABLE ONLY public.adoptioninquiry DROP CONSTRAINT adoptioninquiry_pkey;
       public            postgres    false    213            ?           2606    16474    event event_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (event_n);
 :   ALTER TABLE ONLY public.event DROP CONSTRAINT event_pkey;
       public            postgres    false    214            ?           2606    16476    eventcheckup eventcheckup_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.eventcheckup
    ADD CONSTRAINT eventcheckup_pkey PRIMARY KEY (check_up_n);
 H   ALTER TABLE ONLY public.eventcheckup DROP CONSTRAINT eventcheckup_pkey;
       public            postgres    false    216            ?           2606    16478 "   eventinterview eventinterview_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.eventinterview
    ADD CONSTRAINT eventinterview_pkey PRIMARY KEY (interview_n);
 L   ALTER TABLE ONLY public.eventinterview DROP CONSTRAINT eventinterview_pkey;
       public            postgres    false    217            ?           2606    16480 &   eventsituationer eventsituationer_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.eventsituationer
    ADD CONSTRAINT eventsituationer_pkey PRIMARY KEY (situationer_n);
 P   ALTER TABLE ONLY public.eventsituationer DROP CONSTRAINT eventsituationer_pkey;
       public            postgres    false    218            ?           2606    16482    eventtype eventtype_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.eventtype
    ADD CONSTRAINT eventtype_pkey PRIMARY KEY (event_type_n);
 B   ALTER TABLE ONLY public.eventtype DROP CONSTRAINT eventtype_pkey;
       public            postgres    false    219            ?           2606    16484    medicine medicine_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.medicine
    ADD CONSTRAINT medicine_pkey PRIMARY KEY (med_n);
 @   ALTER TABLE ONLY public.medicine DROP CONSTRAINT medicine_pkey;
       public            postgres    false    220            ?           2606    16486    pet pet_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY public.pet
    ADD CONSTRAINT pet_pkey PRIMARY KEY (pet_n);
 6   ALTER TABLE ONLY public.pet DROP CONSTRAINT pet_pkey;
       public            postgres    false    221            ?           2606    16488    schedule schedule_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_pkey PRIMARY KEY (schedule_n);
 @   ALTER TABLE ONLY public.schedule DROP CONSTRAINT schedule_pkey;
       public            postgres    false    222            ?           2606    16490    shelter shelter_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.shelter
    ADD CONSTRAINT shelter_pkey PRIMARY KEY (shelter_n);
 >   ALTER TABLE ONLY public.shelter DROP CONSTRAINT shelter_pkey;
       public            postgres    false    223            ?           2606    16492    veterinarian veterinarian_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.veterinarian
    ADD CONSTRAINT veterinarian_pkey PRIMARY KEY (vet_n);
 H   ALTER TABLE ONLY public.veterinarian DROP CONSTRAINT veterinarian_pkey;
       public            postgres    false    224            ?           2606    16493 *   administrator administrator_shelter_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.administrator
    ADD CONSTRAINT administrator_shelter_n_fkey FOREIGN KEY (shelter_n) REFERENCES public.shelter(shelter_n);
 T   ALTER TABLE ONLY public.administrator DROP CONSTRAINT administrator_shelter_n_fkey;
       public          postgres    false    223    3527    209            ?           2606    16498 (   adoption adoption_adopt_order_inq_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.adoption
    ADD CONSTRAINT adoption_adopt_order_inq_n_fkey FOREIGN KEY (adopt_order_inq_n) REFERENCES public.adoptioninquiry(adopt_order_inq_n);
 R   ALTER TABLE ONLY public.adoption DROP CONSTRAINT adoption_adopt_order_inq_n_fkey;
       public          postgres    false    213    212    3509            ?           2606    16503     adoption adoption_adopter_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.adoption
    ADD CONSTRAINT adoption_adopter_n_fkey FOREIGN KEY (adopter_n) REFERENCES public.adopter(adopter_n);
 J   ALTER TABLE ONLY public.adoption DROP CONSTRAINT adoption_adopter_n_fkey;
       public          postgres    false    212    211    3505            ?           2606    16508    adoption adoption_pet_n_fkey    FK CONSTRAINT     z   ALTER TABLE ONLY public.adoption
    ADD CONSTRAINT adoption_pet_n_fkey FOREIGN KEY (pet_n) REFERENCES public.pet(pet_n);
 F   ALTER TABLE ONLY public.adoption DROP CONSTRAINT adoption_pet_n_fkey;
       public          postgres    false    221    3523    212            ?           2606    16513     adoption adoption_shelter_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.adoption
    ADD CONSTRAINT adoption_shelter_n_fkey FOREIGN KEY (shelter_n) REFERENCES public.shelter(shelter_n);
 J   ALTER TABLE ONLY public.adoption DROP CONSTRAINT adoption_shelter_n_fkey;
       public          postgres    false    223    212    3527            ?           2606    16518    event event_admin_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_admin_n_fkey FOREIGN KEY (admin_n) REFERENCES public.administrator(admin_n);
 B   ALTER TABLE ONLY public.event DROP CONSTRAINT event_admin_n_fkey;
       public          postgres    false    209    3501    214            ?           2606    16523    event event_event_type_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_event_type_n_fkey FOREIGN KEY (event_type_n) REFERENCES public.eventtype(event_type_n);
 G   ALTER TABLE ONLY public.event DROP CONSTRAINT event_event_type_n_fkey;
       public          postgres    false    219    3519    214            ?           2606    16528 &   eventcheckup eventcheckup_event_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.eventcheckup
    ADD CONSTRAINT eventcheckup_event_n_fkey FOREIGN KEY (event_n) REFERENCES public.event(event_n);
 P   ALTER TABLE ONLY public.eventcheckup DROP CONSTRAINT eventcheckup_event_n_fkey;
       public          postgres    false    3511    216    214            ?           2606    16533 $   eventcheckup eventcheckup_pet_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.eventcheckup
    ADD CONSTRAINT eventcheckup_pet_n_fkey FOREIGN KEY (pet_n) REFERENCES public.pet(pet_n);
 N   ALTER TABLE ONLY public.eventcheckup DROP CONSTRAINT eventcheckup_pet_n_fkey;
       public          postgres    false    221    3523    216            ?           2606    16538 $   eventcheckup eventcheckup_vet_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.eventcheckup
    ADD CONSTRAINT eventcheckup_vet_n_fkey FOREIGN KEY (vet_n) REFERENCES public.veterinarian(vet_n);
 N   ALTER TABLE ONLY public.eventcheckup DROP CONSTRAINT eventcheckup_vet_n_fkey;
       public          postgres    false    216    3529    224            ?           2606    16543 ,   eventinterview eventinterview_adopter_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.eventinterview
    ADD CONSTRAINT eventinterview_adopter_n_fkey FOREIGN KEY (adopter_n) REFERENCES public.adopter(adopter_n);
 V   ALTER TABLE ONLY public.eventinterview DROP CONSTRAINT eventinterview_adopter_n_fkey;
       public          postgres    false    211    3505    217            ?           2606    16548 *   eventinterview eventinterview_event_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.eventinterview
    ADD CONSTRAINT eventinterview_event_n_fkey FOREIGN KEY (event_n) REFERENCES public.event(event_n);
 T   ALTER TABLE ONLY public.eventinterview DROP CONSTRAINT eventinterview_event_n_fkey;
       public          postgres    false    217    214    3511            ?           2606    16553 .   eventsituationer eventsituationer_event_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.eventsituationer
    ADD CONSTRAINT eventsituationer_event_n_fkey FOREIGN KEY (event_n) REFERENCES public.event(event_n);
 X   ALTER TABLE ONLY public.eventsituationer DROP CONSTRAINT eventsituationer_event_n_fkey;
       public          postgres    false    3511    218    214            ?           2606    16558     medicine medicine_shelter_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.medicine
    ADD CONSTRAINT medicine_shelter_n_fkey FOREIGN KEY (shelter_n) REFERENCES public.shelter(shelter_n);
 J   ALTER TABLE ONLY public.medicine DROP CONSTRAINT medicine_shelter_n_fkey;
       public          postgres    false    223    220    3527            ?           2606    16563    pet pet_shelter_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.pet
    ADD CONSTRAINT pet_shelter_n_fkey FOREIGN KEY (shelter_n) REFERENCES public.shelter(shelter_n);
 @   ALTER TABLE ONLY public.pet DROP CONSTRAINT pet_shelter_n_fkey;
       public          postgres    false    3527    221    223            ?           2606    16568    schedule schedule_event_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_event_n_fkey FOREIGN KEY (event_n) REFERENCES public.event(event_n);
 H   ALTER TABLE ONLY public.schedule DROP CONSTRAINT schedule_event_n_fkey;
       public          postgres    false    222    3511    214            ?           2606    16573    shelter shelter_shelter_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.shelter
    ADD CONSTRAINT shelter_shelter_n_fkey FOREIGN KEY (shelter_n) REFERENCES public.shelter(shelter_n);
 H   ALTER TABLE ONLY public.shelter DROP CONSTRAINT shelter_shelter_n_fkey;
       public          postgres    false    223    3527    223            ?           2606    16578 (   veterinarian veterinarian_shelter_n_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.veterinarian
    ADD CONSTRAINT veterinarian_shelter_n_fkey FOREIGN KEY (shelter_n) REFERENCES public.shelter(shelter_n);
 R   ALTER TABLE ONLY public.veterinarian DROP CONSTRAINT veterinarian_shelter_n_fkey;
       public          postgres    false    223    224    3527            g   T   x?3?,H,..?/J?LL???3?42??????M?4?4?463?051?L?4?2??5?(6?42?t?)645233?40*6?????? ?9c      i     x?uUQv?6??N??y@????Dv?u?$??ϊD$D???]?V9C.?I?t???=????????L??l[m???j?ي͊?Py?dR?$?kr??6??u?n????|A????m[G?+?i?]7d?:09??l6??%9gk:??o=??z?????N???Ɗ??ҹ?+?)2~c??/Ls??NCnK5J??솞N?T??e'~?C???_?g?й?g
?H2O?<????(a?&??N??v??G?Z=??n??Lx4?)??3?Z???~ή?4_hg?+*??X??C0?5?fK6??J3????[g<?j?)??ձ?8p,??J?4???urv??\???U?T"͕?U"???ҷ?'k??'???|??G?fL???P???? -?D6??Я?R????'~E?c?3A?9??[??j2?n???۪Hr)?J?Y?Krq$l	??f?k~?%?d>?P'X???!??r?2?炉4??2?8?,X??h?4??`7'?H???>^?,O%#??a?W/???t2??4?f?"?b?]|?=????:????M??2???g???B?Y2??o?4???.?o?l??EX?3V?nhؑ???B4ci????(?]d?G
?V?JÐ?j~?#?`Dt??????qh??J]a`????O@??f(?r???f??M??P?B?vS?GS?????t????K???3?K?O?d?m??'??B??X(?10M????????Ƈ?F?????8?d???3Gl???=+?TE.gP5????N?Ӟ???d???uCoX?΂?????l??;??|???[????V?}?(9?b3_s@2?
??&1??k?Ӱ??????;???ԋ??x]CE??=@Y?=5?Y]??OX??ħ????#?S???hH??7???;oa??????2???]jf?Eb?#EQGD㝕?Q?֍ҪoJ?T4??	Rl?z????Wb䩋? ?6tzAH??')G?ǈ[?????+a?u??<???/\7?4??']?+?|??`?K齃?o??t:r(?U?<D?????V?͇q9l߃?ov?;H?&y???0??h??\??F`????akb?$?+??z????ߍ???I?>X??v??A???i&?s??\?,c??܏?SM?B+S?(^??L??!)?x??????s??M??u??"?؃?ը)?V?.??????`n??"??Fb??H,??T?aB????mM?L?l??[ל?U?*d?)P
?񋖪@???O$???å?9??dyoj\?
??m<??O1g?????djt??[F?L?"fL0%?????'Og???M&? r???      j   p   x?U???0D??.2?7??K?Tg??????{w<A0o̸??$?N???8?t?[8J????w?[?c;????a?3?V?/T?????k??i???>??GH
???KH_????%M      k   K  x?mQ;O1??_??E????Ca????^|Mt???GO??8?	)S?????)??c?"??PΘ&??\h??l"0p (??ު?Z9ZJc?U??!6??G`???ګ#?s&?</է??D.?k"??b???#3_E6Z(]?D?#G?PsP?΅+6ә??\K?h?P????p?s??b?!?ĶB?C?	X0	*???Q????|???M??H??x?8??I,?H"??u?+%ah?)^ب?T/"?(?O8c?????`nͼyq-^$?0P??^?E??D?g?pA???{C???,?M??O4ԫpL?v#W??2Z?o{`??      l   [   x?3?4?L?K-I-??K,?Tp?HM?.-?H?K??K?4?2"???$8??4?$3?/?.g?e?SΘ???3?	;??і????qqq KW?      n   -   x?3?4B#?4.# i?ids?s?r?&?? &????? ??]      o   $   x?3?4?44?L?2?4???Ɯ??&@F? I#?      p   2   x?3?4B?Ģ??̼D??̲?"?4.#N3 H,J?K?Q?I%b???? ??+      q   A   x?3??,)M,???K-?2?K-I-??K,?L?S?,?,?2?tL?/ 
+x?ɲ??r?=... u?      r   3  x?m?AN?0EדS?????˪? Uj?l??!?]??n$h	???????)?Rص?cZ???0@۳??9'?D?
$H?d?F?q?p??? ??׵3?w?	??r???.?ft/?F?A_y????Q??Y??_????T??I??;S?(3T?G??%????:Ep7U?w:?*f???+ׄ'?/a??[??F?\??9??S??@1B??6z???;?9U??DO???˨`???4??~??8d >+Y?LI㟧=?.5o~?1`lF%???a??e?ٵ?? T???sK?9??yγ,?ڐ??      s   ?  x??VMS?8=+?B{߸b?8ð$P?ݪ??ұ?XE?H2?????gS?*??~?z???c6'+5?;+t???R??l؜ݙRg\jN|CvE?S?,$??`؏c3m?`k??դ??????^??i????ح???
??	?,??	??t?yV???H??????sW? ?\??	????Le?،?ܡDvw??U???????r?1b???sr|eK????H??u??J?=/裛y?^L??lL??Ό&?C?*?s???J(%x]yi?&?A?.?"Cfc?????7??Re|#<_	??n?	[?M?#?ͨLh?"???ˬ?m?LFh?ۢەK??t?g??J??{????ܡ?f{|bݻ.?7?z񓝑
?H??u?O.و??w??{????u??=g˂v?Mc??J7????B????D(??!UM?g5e??#?ş?Vh74??mG?	:4??I? /???i?I?;d??+?7a,?vMv?D?1R"G??g??0
+ޥ)7}?J???ϹT?($2?$?"?Yy?I?E?䗝?????n?{	]
L?р?	?D?]aS?EKF.????7?췍??1;n?{?6/
qzPh?t?}>}???ˢ????:??읕??(WP))?1{?????????SԄ??5??]L)gS?????A@?Q?6d3kLQE]Ĥ??-????A??V??1[Ǖ?
???L?B7?!?_?????8???k]????g?????	nb?5MG?x ?ڋ????*(?????.?޶?f?F?N?>|m?	\;'t?Ύ.Q؎?(|M;??6?q4?ZdӲ?c9??T˧"?QŷF?0??ܐ???A?B????m?z@?Қ?q4?Xï?? ?= _?o?e~??}???~?q0? tYp???)[??ށ:?T!?h??z?dM?dq]??B?B???
??":?wj?;???Ԃh???/?9{(??"??Pz{??3??[ÈsAY?֒?]?i???????\:??D??5?>?X	???????]?BV?=t?A%???q??2x???x&.?rY|B???VY0?%???
??JDQ?>͐-???+?<?_|=Wݏ???t콊?Gn?Nnl]???????kU???OY??O?B?U?q??#|&??v??M???}??h????c?.??H_4??
{?;?W??SG??f|?-??z??R?3      t   V   x?U???0???"?ॗ??	Œ??ӌBab??,???X???BQ?,?????%??Y,abn?Z?I?/"z5?h      u   {   x?M?A
?0EיS?B?B????-B?n&8DaL`?Y??? ???????,E???RY??????Z??z<kjN???e?_?/Tw???͔$?JN?T8??Dj??^?;yC8??U??_Bp ?$?/?      v   0  x?]?AN?0EדS? ?c;?????R*D??t3$???q@pz?T,Zy7???,`;?<{?@?P7?6BpU?Ђf?_n,|? ԜsX???d'@?b??
e??w=k(8:???e)װ?֎>G?/!3??x??к?ekK?΀?V
e-R!??v	??1XA?9????eT?M'?ێ>]i?<KU?h*?A?F???iw??1P?.?:?{?????\???0??Ě0??V7??f;
?.?dv????]Q???^?J?**o?????%Z?#???w??ZHc0m?+??!??T?????ɡ?}QJ?w[     