const express = require("express");
const app = express();
app.use(express.json());
const estudiantes = [
    { numero_control: "91650064", nombre: "Juan Pérez" },
    { numero_control: "91650065", nombre: "María López" }
];
app.get("/", (req, res) => {
    res.json({ mensaje: "Hola desde Node.js y Express" });
});
app.get("/estudiantes", (req, res) => {
    res.json(estudiantes);
});
app.get("/estudiantes/:numero_control", (req, res) => {
    const estudiante = estudiantes.find(
        e => e.numero_control === req.params.numero_control);
    if (!estudiante) {
        return res.status(404).json({ detail: "Estudiante no encontrado" });
    }
    res.json(estudiante);
});
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`API disponible en http://localhost:${PORT}`);
});