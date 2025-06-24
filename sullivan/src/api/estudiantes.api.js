import axios from "axios"

export const getEstudiantes = () => {
    return axios.get('http://localhost:8000/estudiantes/')
}