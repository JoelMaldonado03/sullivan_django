git a-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-07-2025 a las 00:16:40
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sullivan`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad`
--

CREATE TABLE `actividad` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha` date NOT NULL,
  `curso_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad_estudiante`
--

CREATE TABLE `actividad_estudiante` (
  `id` bigint(20) NOT NULL,
  `entrega` tinyint(1) NOT NULL,
  `calificacion` decimal(5,2) DEFAULT NULL,
  `actividad_id` bigint(20) NOT NULL,
  `estudiante_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia`
--

CREATE TABLE `asistencia` (
  `id` bigint(20) NOT NULL,
  `estado` varchar(12) NOT NULL,
  `clase_id` bigint(20) NOT NULL,
  `estudiante_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Token', 6, 'add_token'),
(22, 'Can change Token', 6, 'change_token'),
(23, 'Can delete Token', 6, 'delete_token'),
(24, 'Can view Token', 6, 'view_token'),
(25, 'Can add Token', 7, 'add_tokenproxy'),
(26, 'Can change Token', 7, 'change_tokenproxy'),
(27, 'Can delete Token', 7, 'delete_tokenproxy'),
(28, 'Can view Token', 7, 'view_tokenproxy'),
(29, 'Can add estudiante', 8, 'add_estudiante'),
(30, 'Can change estudiante', 8, 'change_estudiante'),
(31, 'Can delete estudiante', 8, 'delete_estudiante'),
(32, 'Can view estudiante', 8, 'view_estudiante'),
(33, 'Can add curso profesor', 9, 'add_cursoprofesor'),
(34, 'Can change curso profesor', 9, 'change_cursoprofesor'),
(35, 'Can delete curso profesor', 9, 'delete_cursoprofesor'),
(36, 'Can view curso profesor', 9, 'view_cursoprofesor'),
(37, 'Can add persona', 10, 'add_persona'),
(38, 'Can change persona', 10, 'change_persona'),
(39, 'Can delete persona', 10, 'delete_persona'),
(40, 'Can view persona', 10, 'view_persona'),
(41, 'Can add persona estudiante', 11, 'add_personaestudiante'),
(42, 'Can change persona estudiante', 11, 'change_personaestudiante'),
(43, 'Can delete persona estudiante', 11, 'delete_personaestudiante'),
(44, 'Can view persona estudiante', 11, 'view_personaestudiante'),
(45, 'Can add curso', 12, 'add_curso'),
(46, 'Can change curso', 12, 'change_curso'),
(47, 'Can delete curso', 12, 'delete_curso'),
(48, 'Can view curso', 12, 'view_curso'),
(49, 'Can add materia', 13, 'add_materia'),
(50, 'Can change materia', 13, 'change_materia'),
(51, 'Can delete materia', 13, 'delete_materia'),
(52, 'Can view materia', 13, 'view_materia'),
(53, 'Can add asistencia', 14, 'add_asistencia'),
(54, 'Can change asistencia', 14, 'change_asistencia'),
(55, 'Can delete asistencia', 14, 'delete_asistencia'),
(56, 'Can view asistencia', 14, 'view_asistencia'),
(57, 'Can add clase', 15, 'add_clase'),
(58, 'Can change clase', 15, 'change_clase'),
(59, 'Can delete clase', 15, 'delete_clase'),
(60, 'Can view clase', 15, 'view_clase'),
(61, 'Can add actividad', 16, 'add_actividad'),
(62, 'Can change actividad', 16, 'change_actividad'),
(63, 'Can delete actividad', 16, 'delete_actividad'),
(64, 'Can view actividad', 16, 'view_actividad'),
(65, 'Can add actividad estudiante', 17, 'add_actividadestudiante'),
(66, 'Can change actividad estudiante', 17, 'change_actividadestudiante'),
(67, 'Can delete actividad estudiante', 17, 'delete_actividadestudiante'),
(68, 'Can view actividad estudiante', 17, 'view_actividadestudiante'),
(69, 'Can add evento', 18, 'add_evento'),
(70, 'Can change evento', 18, 'change_evento'),
(71, 'Can delete evento', 18, 'delete_evento'),
(72, 'Can view evento', 18, 'view_evento'),
(73, 'Can add usuario evento', 19, 'add_usuarioevento'),
(74, 'Can change usuario evento', 19, 'change_usuarioevento'),
(75, 'Can delete usuario evento', 19, 'delete_usuarioevento'),
(76, 'Can view usuario evento', 19, 'view_usuarioevento'),
(77, 'Can add usuario', 20, 'add_usuario'),
(78, 'Can change usuario', 20, 'change_usuario'),
(79, 'Can delete usuario', 20, 'delete_usuario'),
(80, 'Can view usuario', 20, 'view_usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clase`
--

CREATE TABLE `clase` (
  `id` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `curso_id` bigint(20) NOT NULL,
  `materia_id` bigint(20) NOT NULL,
  `profesor_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `curso`
--

CREATE TABLE `curso` (
  `id` bigint(20) NOT NULL,
  `nombre_curso` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `curso_profesor`
--

CREATE TABLE `curso_profesor` (
  `id` bigint(20) NOT NULL,
  `curso_id` bigint(20) NOT NULL,
  `persona_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(16, 'actividades', 'actividad'),
(17, 'actividades', 'actividadestudiante'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(6, 'authtoken', 'token'),
(7, 'authtoken', 'tokenproxy'),
(14, 'clases', 'asistencia'),
(15, 'clases', 'clase'),
(4, 'contenttypes', 'contenttype'),
(12, 'cursos', 'curso'),
(8, 'estudiantes', 'estudiante'),
(18, 'eventos', 'evento'),
(19, 'eventos', 'usuarioevento'),
(13, 'materias', 'materia'),
(9, 'personas', 'cursoprofesor'),
(10, 'personas', 'persona'),
(11, 'personas', 'personaestudiante'),
(5, 'sessions', 'session'),
(20, 'usuarios', 'usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'cursos', '0001_initial', '2025-07-03 20:40:26.807912'),
(2, 'estudiantes', '0001_initial', '2025-07-03 20:40:26.872016'),
(3, 'actividades', '0001_initial', '2025-07-03 20:40:27.067617'),
(4, 'contenttypes', '0001_initial', '2025-07-03 20:40:27.101870'),
(5, 'contenttypes', '0002_remove_content_type_name', '2025-07-03 20:40:27.158705'),
(6, 'auth', '0001_initial', '2025-07-03 20:40:27.352440'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-07-03 20:40:27.400566'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-07-03 20:40:27.407561'),
(9, 'auth', '0004_alter_user_username_opts', '2025-07-03 20:40:27.414563'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-07-03 20:40:27.421620'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-07-03 20:40:27.423583'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-07-03 20:40:27.431583'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-07-03 20:40:27.438582'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-07-03 20:40:27.447897'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-07-03 20:40:27.457895'),
(16, 'auth', '0011_update_proxy_permissions', '2025-07-03 20:40:27.467583'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-07-03 20:40:27.474623'),
(18, 'usuarios', '0001_initial', '2025-07-03 20:40:27.731271'),
(19, 'admin', '0001_initial', '2025-07-03 20:40:27.835574'),
(20, 'admin', '0002_logentry_remove_auto_add', '2025-07-03 20:40:27.846570'),
(21, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-03 20:40:27.856570'),
(22, 'authtoken', '0001_initial', '2025-07-03 20:40:27.939099'),
(23, 'authtoken', '0002_auto_20160226_1747', '2025-07-03 20:40:27.969101'),
(24, 'authtoken', '0003_tokenproxy', '2025-07-03 20:40:27.972097'),
(25, 'authtoken', '0004_alter_tokenproxy_options', '2025-07-03 20:40:27.978098'),
(26, 'personas', '0001_initial', '2025-07-03 20:40:28.175033'),
(27, 'materias', '0001_initial', '2025-07-03 20:40:28.191031'),
(28, 'clases', '0001_initial', '2025-07-03 20:40:28.326201'),
(29, 'clases', '0002_initial', '2025-07-03 20:40:28.501952'),
(30, 'eventos', '0001_initial', '2025-07-03 20:40:28.545954'),
(31, 'personas', '0002_initial', '2025-07-03 20:40:28.755703'),
(32, 'sessions', '0001_initial', '2025-07-03 20:40:28.788894');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante`
--

CREATE TABLE `estudiante` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo_electronico` varchar(254) DEFAULT NULL,
  `nivel_academico` varchar(50) DEFAULT NULL,
  `curso_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evento`
--

CREATE TABLE `evento` (
  `ID_Evento` int(11) NOT NULL,
  `Titulo` varchar(255) NOT NULL,
  `Descripcion` longtext DEFAULT NULL,
  `Fecha_Inicio` datetime(6) DEFAULT NULL,
  `Fecha_Fin` datetime(6) DEFAULT NULL,
  `Ubicacion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materia`
--

CREATE TABLE `materia` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona`
--

CREATE TABLE `persona` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `tipo_documento` varchar(20) NOT NULL,
  `numero_documento` varchar(20) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `usuario_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `persona`
--

INSERT INTO `persona` (`id`, `nombre`, `apellido`, `telefono`, `tipo_documento`, `numero_documento`, `direccion`, `fecha_nacimiento`, `usuario_id`) VALUES
(1, 'Juan', 'Pérez', '3101234567', 'CC', '10000001', 'Calle 1 #1-01', '1985-01-01', 1),
(2, 'Carlos', 'Vega', '3101234568', 'CC', '10000002', 'Calle 2 #2-02', '1984-02-02', 2),
(3, 'Miguel', 'Soto', '3101234569', 'CC', '10000003', 'Calle 3 #3-03', '1983-03-03', 3),
(4, 'Ana', 'Rodríguez', '3101234570', 'CC', '10000004', 'Calle 4 #4-04', '1982-04-04', 4),
(5, 'Pedro', 'López', '3101234571', 'CC', '10000005', 'Calle 5 #5-05', '1981-05-05', 5),
(6, 'Luis', 'Martínez', '3101234572', 'CC', '10000006', 'Calle 6 #6-06', '1980-06-06', 6),
(7, 'Laura', 'Gómez', '3101234573', 'CC', '10000007', 'Calle 7 #7-07', '1979-07-07', 7),
(8, 'Jorge', 'Pérez', '3101234574', 'CC', '10000008', 'Calle 8 #8-08', '1978-08-08', 8),
(9, 'Esteban', 'Jiménez', '3101234575', 'CC', '10000009', 'Calle 9 #9-09', '1977-09-09', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona_estudiante`
--

CREATE TABLE `persona_estudiante` (
  `id` bigint(20) NOT NULL,
  `parentesco` varchar(30) NOT NULL,
  `estudiante_id` bigint(20) NOT NULL,
  `persona_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `rol` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `rol`) VALUES
(1, 'pbkdf2_sha256$600000$qON7mpci8AQ9bOZ8Ey7qzd$7wal2GxZLRFAoNxS7uHF4DElxydhtMCCWL8OHnx2MMM=', NULL, 0, 'admin', '', '', 'admin@school.com', 0, 1, '2025-07-03 20:44:07.349730', 'Administrador'),
(2, 'pbkdf2_sha256$600000$bB5vksd9QLzIjkAcygW79u$AwF6n799Z0BOvN8H/k93Bko76eWy3bo0BZcHlMsMjb0=', NULL, 0, 'profesor1', '', '', 'cvega@school.com', 0, 1, '2025-07-03 20:45:27.667250', 'Profesor'),
(3, 'pbkdf2_sha256$600000$TYf6rotGdP7sbqPyNWNZXz$9mUbjN72naCDbRpx/67FY3USp3wnyC/dgDFgXOTIrb8=', NULL, 0, 'acudiente1', '', '', 'msoto@school.com', 0, 1, '2025-07-03 20:48:50.469849', 'Acudiente'),
(4, 'pbkdf2_sha256$600000$LxyTGmBntkH3hHngHYgRvk$XVfvmEZxwL5aGHDgX7OKgEE7NmYGQJZ7QjxI28Ml1NY=', NULL, 0, 'acudiente2', '', '', 'arodriguez@school.com', 0, 1, '2025-07-03 20:50:06.513990', 'Acudiente'),
(5, 'pbkdf2_sha256$600000$KmEgpLEy7nnivQ4ZwAMLe0$XaZI8cX0u4pN33PgO37gy6MitEmgHfFX+5ndbX4Bfgk=', NULL, 0, 'profesor3', '', '', 'plopez@school.com', 0, 1, '2025-07-03 20:50:25.924102', 'Profesor'),
(6, 'pbkdf2_sha256$600000$eqQplyQU4yPw0VXZcjMQcb$DBHcqNAmiptdBv1mwGipsHe6T35eMOW15rJfXQ6VQ2g=', NULL, 0, 'acudiente3', '', '', 'lmartinez@school.com', 0, 1, '2025-07-03 20:50:35.818228', 'Acudiente'),
(7, 'pbkdf2_sha256$600000$oRfmrlOP0je6r33lU6sCSe$Q8L48UHCr2Xbm37SB8FD1XEqPutPELPgDJJIeHosGQ8=', NULL, 0, 'profesor4', '', '', 'lgomez@school.com', 0, 1, '2025-07-03 20:50:45.479408', 'Profesor'),
(8, 'pbkdf2_sha256$600000$RGnCcdRAXODoyCtV1Zg6vp$9DL4aLqzam94/egFx4uUYENdKDZEYCCDgq3wXhvz4Is=', NULL, 0, 'acudiente4', '', '', 'jperez@school.com', 0, 1, '2025-07-03 20:50:53.811287', 'Acudiente'),
(9, 'pbkdf2_sha256$600000$EhaRjhJX2uYaq99zV1mNut$QSASySEhYoCnfAp6n4Gw8GGl8wCqOvNwf8jYKAZIhuM=', NULL, 0, 'profesor5', '', '', 'ejimenez@school.com', 0, 1, '2025-07-03 20:51:05.240683', 'Profesor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_evento`
--

CREATE TABLE `usuario_evento` (
  `id` bigint(20) NOT NULL,
  `ID_Usuario` int(11) NOT NULL,
  `ID_Evento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_groups`
--

CREATE TABLE `usuario_groups` (
  `id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_user_permissions`
--

CREATE TABLE `usuario_user_permissions` (
  `id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD PRIMARY KEY (`id`),
  ADD KEY `actividad_curso_id_61a248c0_fk_curso_id` (`curso_id`);

--
-- Indices de la tabla `actividad_estudiante`
--
ALTER TABLE `actividad_estudiante`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `actividad_estudiante_estudiante_id_actividad_id_06818fc8_uniq` (`estudiante_id`,`actividad_id`),
  ADD KEY `actividad_estudiante_actividad_id_76ef88c1_fk_actividad_id` (`actividad_id`);

--
-- Indices de la tabla `asistencia`
--
ALTER TABLE `asistencia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `asistencia_clase_id_b47b835a_fk_clase_id` (`clase_id`),
  ADD KEY `asistencia_estudiante_id_2e46a738_fk_estudiante_id` (`estudiante_id`);

--
-- Indices de la tabla `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `clase`
--
ALTER TABLE `clase`
  ADD PRIMARY KEY (`id`),
  ADD KEY `clase_curso_id_997684b9_fk_curso_id` (`curso_id`),
  ADD KEY `clase_materia_id_78dba710_fk_materia_id` (`materia_id`),
  ADD KEY `clase_profesor_id_7dee4225_fk_persona_id` (`profesor_id`);

--
-- Indices de la tabla `curso`
--
ALTER TABLE `curso`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `curso_profesor`
--
ALTER TABLE `curso_profesor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `curso_profesor_curso_id_e5f9ed66_fk_curso_id` (`curso_id`),
  ADD KEY `curso_profesor_persona_id_47ea44cb_fk_persona_id` (`persona_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_usuario_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD PRIMARY KEY (`id`),
  ADD KEY `estudiante_curso_id_8470b0e6_fk_curso_id` (`curso_id`);

--
-- Indices de la tabla `evento`
--
ALTER TABLE `evento`
  ADD PRIMARY KEY (`ID_Evento`);

--
-- Indices de la tabla `materia`
--
ALTER TABLE `materia`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `persona`
--
ALTER TABLE `persona`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_documento` (`numero_documento`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `persona_estudiante`
--
ALTER TABLE `persona_estudiante`
  ADD PRIMARY KEY (`id`),
  ADD KEY `persona_estudiante_estudiante_id_961c45d8_fk_estudiante_id` (`estudiante_id`),
  ADD KEY `persona_estudiante_persona_id_99d5a601_fk_persona_id` (`persona_id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `usuario_evento`
--
ALTER TABLE `usuario_evento`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_evento_ID_Usuario_ID_Evento_6bf276be_uniq` (`ID_Usuario`,`ID_Evento`);

--
-- Indices de la tabla `usuario_groups`
--
ALTER TABLE `usuario_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_groups_usuario_id_group_id_2e3cd638_uniq` (`usuario_id`,`group_id`),
  ADD KEY `usuario_groups_group_id_c67c8651_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `usuario_user_permissions`
--
ALTER TABLE `usuario_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_user_permissions_usuario_id_permission_id_3db58b8c_uniq` (`usuario_id`,`permission_id`),
  ADD KEY `usuario_user_permiss_permission_id_a8893ce7_fk_auth_perm` (`permission_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividad`
--
ALTER TABLE `actividad`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `actividad_estudiante`
--
ALTER TABLE `actividad_estudiante`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asistencia`
--
ALTER TABLE `asistencia`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT de la tabla `clase`
--
ALTER TABLE `clase`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `curso`
--
ALTER TABLE `curso`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `curso_profesor`
--
ALTER TABLE `curso_profesor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `evento`
--
ALTER TABLE `evento`
  MODIFY `ID_Evento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `materia`
--
ALTER TABLE `materia`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `persona`
--
ALTER TABLE `persona`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `persona_estudiante`
--
ALTER TABLE `persona_estudiante`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `usuario_evento`
--
ALTER TABLE `usuario_evento`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario_groups`
--
ALTER TABLE `usuario_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario_user_permissions`
--
ALTER TABLE `usuario_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD CONSTRAINT `actividad_curso_id_61a248c0_fk_curso_id` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`);

--
-- Filtros para la tabla `actividad_estudiante`
--
ALTER TABLE `actividad_estudiante`
  ADD CONSTRAINT `actividad_estudiante_actividad_id_76ef88c1_fk_actividad_id` FOREIGN KEY (`actividad_id`) REFERENCES `actividad` (`id`),
  ADD CONSTRAINT `actividad_estudiante_estudiante_id_c577952c_fk_estudiante_id` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`);

--
-- Filtros para la tabla `asistencia`
--
ALTER TABLE `asistencia`
  ADD CONSTRAINT `asistencia_clase_id_b47b835a_fk_clase_id` FOREIGN KEY (`clase_id`) REFERENCES `clase` (`id`),
  ADD CONSTRAINT `asistencia_estudiante_id_2e46a738_fk_estudiante_id` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`);

--
-- Filtros para la tabla `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `clase`
--
ALTER TABLE `clase`
  ADD CONSTRAINT `clase_curso_id_997684b9_fk_curso_id` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`),
  ADD CONSTRAINT `clase_materia_id_78dba710_fk_materia_id` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  ADD CONSTRAINT `clase_profesor_id_7dee4225_fk_persona_id` FOREIGN KEY (`profesor_id`) REFERENCES `persona` (`id`);

--
-- Filtros para la tabla `curso_profesor`
--
ALTER TABLE `curso_profesor`
  ADD CONSTRAINT `curso_profesor_curso_id_e5f9ed66_fk_curso_id` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`),
  ADD CONSTRAINT `curso_profesor_persona_id_47ea44cb_fk_persona_id` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD CONSTRAINT `estudiante_curso_id_8470b0e6_fk_curso_id` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`);

--
-- Filtros para la tabla `persona`
--
ALTER TABLE `persona`
  ADD CONSTRAINT `persona_usuario_id_848d1235_fk_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `persona_estudiante`
--
ALTER TABLE `persona_estudiante`
  ADD CONSTRAINT `persona_estudiante_estudiante_id_961c45d8_fk_estudiante_id` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`),
  ADD CONSTRAINT `persona_estudiante_persona_id_99d5a601_fk_persona_id` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`);

--
-- Filtros para la tabla `usuario_groups`
--
ALTER TABLE `usuario_groups`
  ADD CONSTRAINT `usuario_groups_group_id_c67c8651_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `usuario_groups_usuario_id_161fc80c_fk_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `usuario_user_permissions`
--
ALTER TABLE `usuario_user_permissions`
  ADD CONSTRAINT `usuario_user_permiss_permission_id_a8893ce7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `usuario_user_permissions_usuario_id_693d9c50_fk_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
