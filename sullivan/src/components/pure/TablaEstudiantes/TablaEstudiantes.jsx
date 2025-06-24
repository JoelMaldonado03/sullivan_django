import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { getEstudiantes } from '../../../api/estudiantes.api';

const TablaEstudiantes = () => {
  const [estudiantes, setEstudiantes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function cargandoEstudiantes(){
      const res = await getEstudiantes()
      console.log(res)
      setEstudiantes(res.data)
    }
    cargandoEstudiantes()
  }, []);

  return (
    <div>
      <h2>Listado de Estudiantes</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Correo</th>
            <th>Curso</th>
          </tr>
        </thead>
        <tbody>
          {estudiantes.map(est => (
            <tr key={est.id_estudiante}>
              <td>{est.id_estudiante}</td>
              <td>{est.nombre}</td>
              <td>{est.apellido}</td>
              <td>{est.correo_electronico}</td>
              <td>{est.curso}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaEstudiantes;
