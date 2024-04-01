--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

-- Started on 2024-03-31 14:38:41

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
-- TOC entry 217 (class 1259 OID 49229)
-- Name: resource; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.resource (
    url text NOT NULL
);


ALTER TABLE public.resource OWNER TO root;

--
-- TOC entry 216 (class 1259 OID 49222)
-- Name: rss_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rss_item (
    guid text NOT NULL,
    title text NOT NULL,
    link text NOT NULL,
    description text,
    pub_date timestamp without time zone NOT NULL,
    category text,
    resource_url text NOT NULL
);


ALTER TABLE public.rss_item OWNER TO root;

--
-- TOC entry 215 (class 1259 OID 49215)
-- Name: subscription; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscription (
    user_id bigint NOT NULL,
    resource_url text NOT NULL
);


ALTER TABLE public.subscription OWNER TO root;

--
-- TOC entry 214 (class 1259 OID 49210)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id bigint NOT NULL,
    name text
);


ALTER TABLE public."user" OWNER TO root;


--
-- TOC entry 3189 (class 2606 OID 49235)
-- Name: resource resource_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resource
    ADD CONSTRAINT resource_pkey PRIMARY KEY (url);


--
-- TOC entry 3187 (class 2606 OID 49228)
-- Name: rss_item rss_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rss_item
    ADD CONSTRAINT rss_item_pkey PRIMARY KEY (guid);


--
-- TOC entry 3185 (class 2606 OID 49214)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3192 (class 2606 OID 49246)
-- Name: rss_item rss_item_resource_url_foreign; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rss_item
    ADD CONSTRAINT rss_item_resource_url_foreign FOREIGN KEY (resource_url) REFERENCES public.resource(url);


--
-- TOC entry 3190 (class 2606 OID 49241)
-- Name: subscription user_resource_resource_url_foreign; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT user_resource_resource_url_foreign FOREIGN KEY (resource_url) REFERENCES public.resource(url);


--
-- TOC entry 3191 (class 2606 OID 49236)
-- Name: subscription user_resource_user_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT user_resource_user_id_foreign FOREIGN KEY (user_id) REFERENCES public."user"(id);


-- Completed on 2024-03-31 14:38:41

--
-- PostgreSQL database dump complete
--

