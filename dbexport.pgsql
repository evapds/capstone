--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Actors; Type: TABLE; Schema: public; Owner: eva
--

CREATE TABLE public."Actors" (
    id integer NOT NULL,
    name character varying,
    age integer,
    gender character varying
);


ALTER TABLE public."Actors" OWNER TO eva;

--
-- Name: Actors_id_seq; Type: SEQUENCE; Schema: public; Owner: eva
--

CREATE SEQUENCE public."Actors_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Actors_id_seq" OWNER TO eva;

--
-- Name: Actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eva
--

ALTER SEQUENCE public."Actors_id_seq" OWNED BY public."Actors".id;


--
-- Name: Movies; Type: TABLE; Schema: public; Owner: eva
--

CREATE TABLE public."Movies" (
    id integer NOT NULL,
    title character varying,
    release_date character varying
);


ALTER TABLE public."Movies" OWNER TO eva;

--
-- Name: Movies_id_seq; Type: SEQUENCE; Schema: public; Owner: eva
--

CREATE SEQUENCE public."Movies_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Movies_id_seq" OWNER TO eva;

--
-- Name: Movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eva
--

ALTER SEQUENCE public."Movies_id_seq" OWNED BY public."Movies".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: eva
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO eva;

--
-- Name: Actors id; Type: DEFAULT; Schema: public; Owner: eva
--

ALTER TABLE ONLY public."Actors" ALTER COLUMN id SET DEFAULT nextval('public."Actors_id_seq"'::regclass);


--
-- Name: Movies id; Type: DEFAULT; Schema: public; Owner: eva
--

ALTER TABLE ONLY public."Movies" ALTER COLUMN id SET DEFAULT nextval('public."Movies_id_seq"'::regclass);


--
-- Data for Name: Actors; Type: TABLE DATA; Schema: public; Owner: eva
--

COPY public."Actors" (id, name, age, gender) FROM stdin;
4	Tom	32	male
5	Noa	27	both
6	Noa	27	both
7	Noa	27	both
8	Lena	19	female
9	Lena	19	female
10	Mike	22	male
11	Mike	22	male
12	Mike	22	male
13	Mike	22	male
14	Mike	22	male
15	Mike	22	male
16	Mike	22	male
17	Mike	22	male
18	Mike	22	male
20	Mike	22	male
19	Mike	13	male
21	Mike	22	male
1	Anna	53	female
2	Micaela	21	female
3	Sara	47	female
\.


--
-- Data for Name: Movies; Type: TABLE DATA; Schema: public; Owner: eva
--

COPY public."Movies" (id, title, release_date) FROM stdin;
2	Coolio	1987
6	Notsure	2020
8	GreatMovie	1999
9	Another movie	1999
10	Cool movie	2011
3	Notsure	2004
1	Crazy drive	2005
4	Why not	2010
5	Can this work	2011
7	Getting desparate	2012
11	Last chance	2016
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: eva
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Name: Actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eva
--

SELECT pg_catalog.setval('public."Actors_id_seq"', 21, true);


--
-- Name: Movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eva
--

SELECT pg_catalog.setval('public."Movies_id_seq"', 10, true);


--
-- Name: Actors Actors_pkey; Type: CONSTRAINT; Schema: public; Owner: eva
--

ALTER TABLE ONLY public."Actors"
    ADD CONSTRAINT "Actors_pkey" PRIMARY KEY (id);


--
-- Name: Movies Movies_pkey; Type: CONSTRAINT; Schema: public; Owner: eva
--

ALTER TABLE ONLY public."Movies"
    ADD CONSTRAINT "Movies_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: eva
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- PostgreSQL database dump complete
--

