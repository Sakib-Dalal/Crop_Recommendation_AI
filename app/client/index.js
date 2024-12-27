import express from "express";
import bodyParser from "body-parser";
import axios from "axios";

const app = express();
const port = 3000;

app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", async(req, res) => {
    const data = await axios.get("http://127.0.0.1:5000/");
    console.log(`Backend Status: ${data["data"]["status"]}`);
    res.render("home.ejs", {data: data["data"]["status"]});
});

app.post("/submit", async (req, res) => {
    const data = {
        "Nitrogen": req.body.Nitrogen,
        "Phosphorus": req.body.Phosphorus,
        "Potassium": req.body.Potassium,
        "Temperature": req.body.Temperature,
        "Humidity": req.body.Humidity,
        "Ph": req.body.Ph,
        "Rainfall": req.body.Rainfall,
    };

    console.log("Data received from client:", data);

    try {
        // Send data to Flask server
        const response = await axios.post("http://127.0.0.1:5000/submit", data);
        console.log("Response from Flask server:", response.data);
        const prediction = response.data.prediction;
        const llm_message = response.data.llm_message;
        const crop_image = response.data.crop_image;
        res.render("submit.ejs", {prediction: prediction, llm_message: llm_message, crop_image: crop_image});
        // res.send(response.data.Message); // Send Flask's response back to the client
    } catch (error) {
        console.error("Error communicating with Flask server:", error.message);
        res.status(500).send({ message: "Error communicating with Flask server" });
    }
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});