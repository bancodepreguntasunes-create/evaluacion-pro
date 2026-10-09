// =============================================
// UNES - data.js  ·  Datos maestros del sistema
// =============================================

const NUCLEOS = [
  "LA GUAIRA",
  "CEFE CARMEN DE URIA",
  "CARACAS",
  "JUNQUITO",
  "HELICOIDE",
  "SAN PEDRO - COMUNAL",
  "EL LLANITO",
  "CAFETAL",
  "EJE ALTOS MIRANDINOS",
  "EJE VALLES DEL TUY",
  "EJE BARLOVENTO",
  "EJE METROPOLITANO",
  "EJE GUARENAS - GUATIRE",
  "ARAGUA",
  "CARABOBO",
  "YARACUY",
  "FALCÓN",
  "LARA",
  "EJE LA GUAJIRA",
  "ZULIA",
  "EJE SUR DEL LAGO",
  "APURE",
  "BARINAS",
  "COJEDES TINAQUILLO",
  "COJEDES",
  "GUÁRICO",
  "PORTUGUESA",
  "MÉRIDA",
  "TÁCHIRA",
  "TRUJILLO",
  "ANZOÁTEGUI",
  "MONAGAS",
  "NUEVA ESPARTA",
  "CARUPANO",
  "SUCRE",
  "AMAZONAS",
  "BOLÍVAR - PTO. ORDAZ",
  "BOLÍVAR - ANGOSTURA",
  "DELTA AMACURO"
];

const PNF_LIST = [
  {
    id: "servicio-policial",
    nombre: "PNF en Servicio Policial",
    corto: "Serv. Policial",
    descripcion: "Formación integral de funcionarios para el CPNB, policías estadales y municipales.",
    color: "#6366f1"
  },
  {
    id: "investigacion-penal",
    nombre: "PNF en Investigación Penal",
    corto: "Inv. Penal",
    descripcion: "Formación técnico-científica para la investigación de hechos delictivos y apoyo al CICPC.",
    color: "#8b5cf6"
  },
  {
    id: "criminalistica",
    nombre: "PNF en Criminalística",
    corto: "Criminalística",
    descripcion: "Capacitación en análisis de evidencias físicas, ciencias forenses y técnicas auxiliares de la justicia.",
    color: "#06b6d4"
  },
  {
    id: "ciencias-fuego",
    nombre: "PNF en Ciencias del Fuego y Seguridad Contra Incendios",
    corto: "Ciencias del Fuego",
    descripcion: "Dirigido a cuerpos de bomberos y especialistas en prevención, combate de incendios y rescate.",
    color: "#f59e0b"
  },
  {
    id: "proteccion-civil",
    nombre: "PNF en Protección Civil y Administración de Desastres",
    corto: "Protección Civil",
    descripcion: "Gestión integral de riesgos, prevención, mitigación y atención de emergencias.",
    color: "#10b981"
  },
  {
    id: "servicio-penitenciario",
    nombre: "PNF en Servicio Penitenciario",
    corto: "Serv. Penitenciario",
    descripcion: "Formación de profesionales para la custodia y gestión penitenciaria con enfoque en derechos humanos.",
    color: "#f43f5e"
  },
  {
    id: "emergencias-prehospitalarias",
    nombre: "PNF en Emergencias Prehospitalarias",
    corto: "Emergencias Prehospitalarias",
    descripcion: "Capacitación en atención médica primaria, soporte vital básico y avanzado en urgencias.",
    color: "#ec4899"
  },
  {
    id: "seguridad-nacion",
    nombre: "PNF en Seguridad de la Nación",
    corto: "Seg. de la Nación",
    descripcion: "Formación analítica y estratégica en inteligencia, contrainteligencia y soberanía nacional.",
    color: "#64748b"
  }
];

const TRAYECTOS = ["Inicial", "I", "II", "III", "IV"];
